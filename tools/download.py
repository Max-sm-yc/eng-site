#!/usr/bin/env python3
"""Download the best archived capture per discovered site path."""

from __future__ import annotations

import argparse
import base64
import concurrent.futures
import hashlib
import json
import mimetypes
import re
import shutil
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "original"
RAW = ROOT / "archive-data" / "raw-source"
MANIFEST = ROOT / "recovery-manifest.json"
CUTOFF = "20130812122849"
SITE_MARKER = "/orthographic_projection_fyp/"
LOCAL_URL_PREFIX = re.compile(
    rb"https?://(?:www3?\.)ul\.ie(?::(?:80|443))?/(?:%7e|~)rynnet/orthographic_projection_fyp/",
    re.IGNORECASE,
)
LEGACY_ROOT_PREFIX = re.compile(rb"(?<![\w:])/(?:%7e|~)rynnet/orthographic_projection_fyp/", re.IGNORECASE)
MALFORMED_NAV_SPACE = re.compile(rb"(using_the_site\.html)%20(?=[\"'])", re.IGNORECASE)
REQUEST_GAP_SECONDS = 3.0
KNOWN_LOCAL_ALIASES = [
    {
        "source": "images/next_button.jpg",
        "target": "flash_pictures/test/next_button.jpg",
        "mime": "image/jpeg",
        "notes": "The archived Apache directory listing links to a 953-byte next_button.jpg dated 13-Nov-2008. The archived images/next_button.jpg is also 953 bytes and 136x55, matching the dimensions used by neighboring lesson pages. Reused as a documented local alias; no capture of the target path was present in the saved namespace inventory.",
    },
    {
        "source": "sp.swf",
        "target": "flash_pictures/test/sp.swf",
        "mime": "application/x-shockwave-flash",
        "notes": "The archived Apache directory listing links to a 59K sp.swf dated 13-Nov-2008. The archived root sp.swf is 60,774 bytes (59.3 KiB) and is embedded by neighboring lessons. Reused as a documented local alias; no capture of the target path was present in the saved namespace inventory.",
    },
]
_rate_lock = threading.Lock()
_last_request = 0.0


def cdx_rows() -> list[list[str]]:
    paths = [path for path in sorted((ROOT / "archive-data").glob("cdx-*.json")) if path.name != "cdx-path-map.json"]
    rows: list[list[str]] = []
    for path in paths:
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows.extend(content[1:])
    return rows


def local_relative_path(original_url: str) -> str | None:
    path_map_file = ROOT / "archive-data" / "cdx-path-map.json"
    if path_map_file.exists():
        try:
            mapped = json.loads(path_map_file.read_text(encoding="utf-8")).get(original_url)
        except (OSError, json.JSONDecodeError):
            mapped = None
        if mapped:
            parts = PurePosixPath(mapped).parts
            if not PurePosixPath(mapped).is_absolute() and not any(part in ("..", "") for part in parts):
                return str(PurePosixPath(mapped))
    parsed = urllib.parse.urlsplit(original_url)
    path = urllib.parse.unquote(parsed.path)
    if SITE_MARKER not in path:
        return None
    relative = path.split(SITE_MARKER, 1)[1]
    parts = PurePosixPath(relative).parts
    if any(part in ("..", "") for part in parts):
        return None
    if not relative:
        relative = "index.html"
    elif relative.endswith("/"):
        relative += "index.html"
    return str(PurePosixPath(relative))


def preferred_capture(rows: list[list[str]]) -> list[str]:
    before = [row for row in rows if row[0] <= CUTOFF]
    candidates = before if before else [row for row in rows if row[0] > CUTOFF]
    if before:
        stamp = max(row[0] for row in candidates)
        candidates = [row for row in candidates if row[0] == stamp]
    elif candidates:
        stamp = min(row[0] for row in candidates)
        candidates = [row for row in candidates if row[0] == stamp]
    if not candidates:
        return []
    # Prefer the host named by the target page when timestamps tie.
    candidates.sort(key=lambda row: ("www3.ul.ie" not in urllib.parse.urlsplit(row[1]).netloc, row[1]))
    return candidates[0]


def content_digest(payload: bytes) -> str:
    return base64.b32encode(hashlib.sha1(payload).digest()).decode("ascii").rstrip("=")


def is_text_mime(mime: str) -> bool:
    return mime.startswith("text/") or mime in {"application/xhtml+xml", "application/xml", "application/javascript", "application/x-javascript"}


def localize(payload: bytes) -> tuple[bytes, bool, bool]:
    result, substitutions = LOCAL_URL_PREFIX.subn(b"/", payload)
    result, root_substitutions = LEGACY_ROOT_PREFIX.subn(b"/", result)
    result, navigation_fixes = MALFORMED_NAV_SPACE.subn(rb"\1", result)
    return result, substitutions + root_substitutions > 0, navigation_fixes > 0


def support_entry(local_path: str, mime: str, notes: str) -> dict:
    return {
        "original_url": None,
        "local_path": local_path,
        "resource_type": mime,
        "archived_timestamp_selected": None,
        "http_status": None,
        "mime_type": mime,
        "downloaded": True,
        "exact_original": False,
        "recovery_status": "RECONSTRUCTED",
        "notes": notes,
    }


def restore_known_aliases() -> list[dict]:
    """Materialize documented local aliases where the archived source exists."""
    restored = []
    for alias in KNOWN_LOCAL_ALIASES:
        source = ORIGINAL / alias["source"]
        target = ORIGINAL / alias["target"]
        if not source.is_file():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.read_bytes() != source.read_bytes():
            shutil.copy2(source, target)
        restored.append({
            "original_url": "http://www3.ul.ie/~rynnet/orthographic_projection_fyp/" + alias["target"],
            "local_path": f"original/{alias['target']}",
            "resource_type": alias["mime"],
            "archived_timestamp_selected": None,
            "http_status": None,
            "mime_type": alias["mime"],
            "downloaded": True,
            "exact_original": False,
            "recovery_status": "RECONSTRUCTED",
            "source_local_path": f"original/{alias['source']}",
            "functionality_status": "OBSOLETE_RUNTIME" if alias["mime"] == "application/x-shockwave-flash" else None,
            "discovery_source": "documented-local-alias",
            "notes": alias["notes"],
        })
    return restored


def download_one(job: tuple[str, list[str], int, int]) -> dict:
    relative_path, row, completed, total = job
    timestamp, original_url, cdx_status, mime, digest, length = row
    is_text = is_text_mime(mime)
    output_path = ORIGINAL / relative_path
    raw_path = RAW / relative_path if is_text else None
    cached = raw_path if is_text else output_path
    expected_size = int(length)

    if cached is not None and cached.exists():
        payload = cached.read_bytes()
        cached_ok = content_digest(payload) == digest
    else:
        cached_ok = False
        payload = b""

    response_status: int | None = 200 if cached_ok else None
    response_mime: str | None = mime if cached_ok else None
    error: str | None = None
    if not cached_ok:
        archive_url = f"https://web.archive.org/web/{timestamp}id_/{original_url}"
        request = urllib.request.Request(
            archive_url,
            headers={"User-Agent": "orthographic-projection-recovery/1.0", "Accept-Encoding": "identity"},
        )
        for attempt in range(1, 5):
            global _last_request
            with _rate_lock:
                now = time.monotonic()
                wait = max(0.0, REQUEST_GAP_SECONDS - (now - _last_request))
                if wait:
                    time.sleep(wait)
                _last_request = time.monotonic()
            try:
                with urllib.request.urlopen(request, timeout=90) as response:
                    payload = response.read()
                    response_status = response.status
                    response_mime = response.headers.get_content_type()
                error = None
                break
            except urllib.error.HTTPError as exc:
                error = f"HTTP {exc.code}: {exc.reason}"
                if exc.code not in (408, 429, 500, 502, 503, 504) or attempt == 4:
                    break
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                if attempt == 4:
                    break
            time.sleep(attempt * 2)

    exact = bool(payload) and content_digest(payload) == digest
    delivered_payload, patched, navigation_fixed = localize(payload) if is_text and payload else (payload, False, False)
    if exact:
        if cached is not None:
            cached.parent.mkdir(parents=True, exist_ok=True)
            if not cached.exists() or cached.read_bytes() != payload:
                cached.write_bytes(payload)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(delivered_payload)

    recovery_status = "RECOVERED_FROM_NEARBY_CAPTURE" if timestamp > CUTOFF else "RECOVERED_EXACT"
    if not exact:
        recovery_status = "MISSING"
        if payload and not error:
            error = f"archive payload digest mismatch (expected {digest}, received {content_digest(payload)})"
    resource_type = mime or mimetypes.guess_type(relative_path)[0] or "unknown"
    functionality_status = "OBSOLETE_RUNTIME" if mime == "application/x-shockwave-flash" else None
    return {
        "original_url": original_url,
        "local_path": f"original/{relative_path}",
        "resource_type": resource_type,
        "archived_timestamp_selected": timestamp,
        "http_status": response_status if response_status is not None else cdx_status,
        "mime_type": mime or response_mime,
        "downloaded": exact,
        "exact_original": exact,
        "recovery_status": recovery_status,
        "functionality_status": functionality_status,
        "archive_digest": digest,
        "expected_bytes": expected_size,
        "downloaded_bytes": len(payload) if payload else None,
        "raw_source_path": f"archive-data/raw-source/{relative_path}" if is_text and exact else None,
        "local_copy_rewritten": bool(patched or navigation_fixed),
        "notes": error if error and not exact else "; ".join(filter(None, [
            f"Same-site absolute URLs were localized in the runnable copy; raw response retained at archive-data/raw-source/{relative_path}." if patched and is_text else "",
            "Removed the repeated navigation link's trailing encoded space in the runnable copy; exact archived HTML remains under archive-data/raw-source/." if navigation_fixed else "",
            "Recovered as original SWF bytes; the historical Flash runtime is obsolete in current browsers." if functionality_status else "",
            "CDX length metadata differs from replay response bytes; the response SHA-1 digest matches the archived digest." if exact and len(payload) != expected_size else "",
        ])),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=2, help="modest concurrent archive requests (default: 2)")
    parser.add_argument("--limit", type=int, help="download only the first N paths; useful for a smoke run")
    args = parser.parse_args()
    rows_by_path: dict[str, list[list[str]]] = {}
    for row in cdx_rows():
        relative = local_relative_path(row[1])
        if relative:
            rows_by_path.setdefault(relative, []).append(row)
    selected = [(path, preferred_capture(rows)) for path, rows in sorted(rows_by_path.items())]
    selected = [(path, row) for path, row in selected if row]
    if args.limit:
        selected = selected[: args.limit]
    jobs = [(path, row, index + 1, len(selected)) for index, (path, row) in enumerate(selected)]
    print(f"Downloading {len(jobs)} selected paths from the cached CDX inventory.")
    results: list[dict] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(args.workers, 3))) as pool:
        futures = [pool.submit(download_one, job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            entry = future.result()
            results.append(entry)
            state = "ok" if entry["downloaded"] else "missing"
            print(f"[{state}] {entry['local_path']} ({entry['archived_timestamp_selected']})")

    results.sort(key=lambda entry: entry["local_path"])
    prior = {}
    if MANIFEST.exists():
        try:
            prior = json.loads(MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            prior = {}
    selected_local_paths = {entry["local_path"] for entry in results}
    aliases = restore_known_aliases()
    alias_targets = {entry["local_path"] for entry in aliases}
    extras = [entry for entry in prior.get("resources", []) if entry.get("discovery_source") == "local-link-crawl" and entry.get("local_path") not in selected_local_paths and entry.get("local_path") not in alias_targets]
    support = list(prior.get("support_files", []))
    root_index = ORIGINAL / "index.html"
    if not root_index.exists():
        root_index.write_text(
            "<!doctype html>\n<html><head><meta charset=\"utf-8\"><title>Orthographic projection archive</title></head><body>\n"
            "<h1>Orthographic projection archive</h1>\n<ul>\n"
            "<li><a href=\"webpages/home.html\">Archived module home</a></li>\n"
            "<li><a href=\"webpages/basics.html\">Primary archived page: Basics</a></li>\n"
            "</ul></body></html>\n",
            encoding="utf-8",
        )
    support = [entry for entry in support if entry.get("local_path") != "original/index.html"]
    support.append(support_entry("original/index.html", "text/html", "Reconstructed local entry point; the archive has no site-root index page in the discovered inventory."))
    data = {
        "source_root": "http://www3.ul.ie/~rynnet/orthographic_projection_fyp/",
        "primary_archived_page": "https://web.archive.org/web/20130812122849/http://www3.ul.ie/~rynnet/orthographic_projection_fyp/webpages/basics.html",
        "target_timestamp": CUTOFF,
        "archive_namespace_path_count": len(rows_by_path),
        "inventory_source": [str(p.relative_to(ROOT)) for p in sorted((ROOT / "archive-data").glob("cdx-*.json")) if p.name != "cdx-path-map.json"],
        "resources": results + extras + aliases,
        "support_files": support,
    }
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    ok = sum(entry["downloaded"] for entry in results)
    print(f"Downloaded exact archive payloads for {ok}/{len(results)} selected site paths.")
    print(f"Manifest written to {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
