#!/usr/bin/env python3
"""Check local HTML/CSS references and optionally retry unresolved site URLs on Wayback."""

from __future__ import annotations

import argparse
import html.parser
import json
import mimetypes
import posixpath
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_ROOTS = {"original": ROOT / "original", "modern": ROOT / "modern"}
MANIFEST = ROOT / "recovery-manifest.json"
REPORT = ROOT / "broken-resource-report.json"
CDX_URL = "https://web.archive.org/cdx/search/cdx?"
SITE_HOSTS = {"www.ul.ie", "www3.ul.ie"}
SITE_PREFIXES = ("/~rynnet/orthographic_projection_fyp/", "/%7Erynnet/orthographic_projection_fyp/")
URL_ATTRS = {"href", "src", "srcset", "data", "background", "poster", "action", "codebase", "archive", "longdesc", "data-src"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
CSS_IMPORT = re.compile(r"@import\s+(?:url\()?\s*['\"]?([^\s'\")]+)", re.IGNORECASE)


class ReferenceParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs if key}
        for key, value in attrs:
            if key and value and key.lower() in URL_ATTRS:
                if key.lower() == "srcset":
                    self.references.extend(("srcset", item.strip().split()[0]) for item in value.split(",") if item.strip())
                else:
                    self.references.append((key.lower(), value.strip()))
            elif key and value and key.lower() == "style":
                self.references.extend(("inline-css", item) for _, item in CSS_URL.findall(value))
        if tag.lower() == "param" and (values.get("name") or "").lower() in {"movie", "src"} and values.get("value"):
            self.references.append(("param", values["value"].strip()))


def html_references(path: Path) -> list[tuple[str, str]]:
    try:
        text = path.read_text(encoding="latin-1")
    except OSError:
        return []
    parser = ReferenceParser()
    parser.feed(text)
    refs = parser.references
    if path.suffix.lower() == ".html" or path.suffix.lower() == ".htm":
        for css in re.findall(r"<style[^>]*>(.*?)</style>", text, flags=re.IGNORECASE | re.DOTALL):
            refs.extend(("css", value) for _, value in CSS_URL.findall(css))
            refs.extend(("css", value) for value in CSS_IMPORT.findall(css))
    return refs


def css_references(path: Path) -> list[tuple[str, str]]:
    try:
        text = path.read_text(encoding="latin-1")
    except OSError:
        return []
    refs = [("css-url", value) for _, value in CSS_URL.findall(text)]
    refs.extend(("css-import", value) for value in CSS_IMPORT.findall(text))
    return refs


def normalize_site_url(url: urllib.parse.ParseResult) -> str | None:
    host = (url.hostname or "").lower()
    path = urllib.parse.unquote(url.path)
    if host in SITE_HOSTS:
        for prefix in SITE_PREFIXES:
            if path.startswith(prefix):
                return path[len(prefix):]
    return None


def resolve_reference(page: Path, webroot: Path, raw: str) -> tuple[Path | None, bool]:
    raw = raw.strip()
    if not raw or raw.startswith(("#", "javascript:", "mailto:", "tel:", "data:", "blob:")):
        return None, True
    parsed = urllib.parse.urlsplit(raw)
    if parsed.scheme.lower() in {"http", "https"} and parsed.hostname not in SITE_HOSTS:
        return None, True
    if parsed.scheme.lower() not in {"", "http", "https"}:
        return None, True
    if parsed.scheme and parsed.hostname in SITE_HOSTS:
        rel = normalize_site_url(parsed)
        if rel is None:
            return None, True
        path = webroot / rel
    else:
        ref_path = urllib.parse.unquote(parsed.path)
        if not ref_path:
            return None, True
        path = (webroot / ref_path.lstrip("/")) if ref_path.startswith("/") else (page.parent / ref_path)
    try:
        resolved = path.resolve(strict=False)
        resolved.relative_to(webroot.resolve())
    except (ValueError, OSError):
        return None, True
    if resolved.is_dir() or parsed.path.endswith("/"):
        resolved = resolved / "index.html"
    return resolved, False


def collect_broken(webroot: Path, label: str) -> list[dict]:
    broken: list[dict] = []
    pages = sorted([*webroot.rglob("*.html"), *webroot.rglob("*.htm")])
    for page in pages:
        for attribute, raw in html_references(page):
            resolved, external = resolve_reference(page, webroot, raw)
            if external or resolved is None or resolved.is_file():
                continue
            broken.append({
                "site_copy": label,
                "source_page": page.relative_to(ROOT).as_posix(),
                "attribute": attribute,
                "reference": raw,
                "expected_local_path": resolved.relative_to(ROOT).as_posix(),
            })
    for sheet in sorted(webroot.rglob("*.css")):
        for attribute, raw in css_references(sheet):
            resolved, external = resolve_reference(sheet, webroot, raw)
            if not external and resolved is not None and not resolved.is_file():
                broken.append({"site_copy": label, "source_page": sheet.relative_to(ROOT).as_posix(), "attribute": attribute, "reference": raw, "expected_local_path": resolved.relative_to(ROOT).as_posix()})
    return broken


def archive_lookup(reference: str, source_page: str) -> tuple[list[list[str]], str | None, str | None]:
    parsed = urllib.parse.urlsplit(reference)
    local_relative: str | None = None
    if parsed.scheme and parsed.hostname in SITE_HOSTS:
        path = urllib.parse.unquote(parsed.path)
        site_prefix = next((prefix for prefix in SITE_PREFIXES if path.startswith(prefix)), None)
        if site_prefix is not None:
            relative = path[len(site_prefix):]
        elif path.startswith("/icons/"):
            local_relative = path.lstrip("/")
            candidates = [f"http://www3.ul.ie{path}", f"http://www.ul.ie{path}"]
            return query_cdx_candidates(candidates, local_relative)
        else:
            return [], "reference is outside the recovered site root", None
    else:
        path = urllib.parse.unquote(parsed.path)
        if not path:
            return [], "reference has no path", None
        if path.startswith("/icons/"):
            local_relative = path.lstrip("/")
            candidates = [f"http://www3.ul.ie{path}", f"http://www.ul.ie{path}"]
            return query_cdx_candidates(candidates, local_relative)
        if path.startswith("/"):
            relative = path.lstrip("/")
        else:
            page_parent = Path(source_page).relative_to("original").parent.as_posix()
            relative = posixpath.normpath(posixpath.join(page_parent, path))
        if relative == ".." or relative.startswith("../"):
            return [], "reference resolves outside the recovered site root", None
        local_relative = relative
    candidates = [
        "http://www3.ul.ie/~rynnet/orthographic_projection_fyp/" + relative,
        "http://www.ul.ie/~rynnet/orthographic_projection_fyp/" + relative,
    ]
    if parsed.path.endswith("/") and local_relative and not local_relative.endswith("/index.html"):
        local_relative = local_relative.rstrip("/") + "/index.html"
    return query_cdx_candidates(candidates, local_relative)


def query_cdx_candidates(candidates: list[str], local_relative: str | None) -> tuple[list[list[str]], str | None, str | None]:
    errors = []
    for original in candidates:
        query = urllib.parse.urlencode({
            "url": original, "output": "json", "filter": "statuscode:200",
            "fl": "timestamp,original,statuscode,mimetype,digest,length",
        })
        req = urllib.request.Request(CDX_URL + query, headers={"User-Agent": "orthographic-projection-recovery/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                rows = json.loads(response.read())
            if len(rows) > 1:
                return rows[1:], None, local_relative
        except Exception as exc:
            errors.append(f"{type(exc).__name__}: {exc}")
        time.sleep(0.8)
    return [], "; ".join(errors) if errors else None, local_relative


def cached_cdx_by_path() -> dict[str, list[list[str]]]:
    """Index the full saved CDX namespace inventory by its site-relative path."""
    archive_dir = ROOT / "archive-data"
    path_map = {}
    map_path = archive_dir / "cdx-path-map.json"
    if map_path.exists():
        try:
            path_map = json.loads(map_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            path_map = {}
    by_path: dict[str, list[list[str]]] = {}
    inventories = [p for p in sorted(archive_dir.glob("cdx-*.json")) if p.name != "cdx-path-map.json"]
    for inventory in inventories:
        try:
            rows = json.loads(inventory.read_text(encoding="utf-8"))[1:]
        except (OSError, json.JSONDecodeError):
            continue
        for row in rows:
            original_url = row[1]
            relative = path_map.get(original_url)
            if not relative:
                path = urllib.parse.unquote(urllib.parse.urlsplit(original_url).path)
                if "/orthographic_projection_fyp/" not in path:
                    continue
                relative = path.split("/orthographic_projection_fyp/", 1)[1]
                if not relative or relative.endswith("/"):
                    relative += "index.html"
            by_path.setdefault(relative, []).append(row)
    return by_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", choices=["original", "modern", "both"], default="both")
    parser.add_argument("--lookup-archive", action="store_true", help="check each unresolved same-site URL against CDX")
    parser.add_argument("--cached-cdx-only", action="store_true", help="look up each broken path in the full saved CDX inventory without network access")
    args = parser.parse_args()
    labels = list(SITE_ROOTS) if args.site == "both" else [args.site]
    broken = []
    for label in labels:
        broken.extend(collect_broken(SITE_ROOTS[label], label))
    if args.lookup_archive:
        inventory_by_path = cached_cdx_by_path() if args.cached_cdx_only else {}
        found_rows: dict[tuple[str, str], list[str]] = {}
        path_map: dict[str, str] = {}
        missing_entries: dict[str, dict] = {}
        grouped: dict[tuple[str, str], list[dict]] = {}
        for entry in broken:
            grouped.setdefault((entry["site_copy"], entry["expected_local_path"]), []).append(entry)
        unique_paths = list(grouped.items())
        previous_results = {}
        if REPORT.exists():
            try:
                previous_report = json.loads(REPORT.read_text(encoding="utf-8"))
                for previous in previous_report.get("unresolved_references", []):
                    key = (previous.get("site_copy"), previous.get("expected_local_path"))
                    if previous.get("wayback_lookup") == "no successful capture found" and not previous.get("wayback_lookup_error"):
                        previous_results[key] = ([], None, None)
                    elif previous.get("wayback_capture"):
                        previous_results[key] = (previous["wayback_capture"], None, None)
            except (OSError, json.JSONDecodeError):
                pass
        for index, (key, path_entries) in enumerate(unique_paths, start=1):
            result_rows, lookup_error, local_relative = previous_results.get(key, ([], None, None))
            if args.cached_cdx_only:
                relative = path_entries[0]["expected_local_path"].removeprefix(f'{path_entries[0]["site_copy"]}/')
                result_rows = inventory_by_path.get(relative, [])
                local_relative = relative
                lookup_error = None
            elif key not in previous_results:
                # Multiple references can resolve to one local path. Try each spelling
                # until one has a capture, or all candidates return a clean negative.
                lookup_errors = []
                for candidate in path_entries:
                    result_rows, lookup_error, local_relative = archive_lookup(candidate["reference"], candidate["source_page"])
                    if result_rows or lookup_error:
                        break
                    if local_relative:
                        break
                if lookup_error:
                    lookup_errors.append(lookup_error)
                    lookup_error = "; ".join(dict.fromkeys(lookup_errors))
            lookup_state = (
                "capture found; added it to the CDX cache; rerun tools/download.py"
                if result_rows else (
                    "no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json"
                    if args.cached_cdx_only else "no successful capture found" if not lookup_error else "lookup failed; retry before classifying as missing"
                )
            )
            for entry in path_entries:
                entry["wayback_lookup"] = lookup_state
                entry["wayback_capture"] = result_rows
                entry["wayback_lookup_error"] = lookup_error
            entry = path_entries[0]
            original_url = result_rows[0][1] if result_rows else None
            if result_rows:
                found_rows.update({(row[0], row[1]): row for row in result_rows})
                if local_relative:
                    path_map.update({row[1]: local_relative for row in result_rows})
            elif (not lookup_error or args.cached_cdx_only) and entry["site_copy"] == "original":
                local_path = entry["expected_local_path"]
                relative = local_relative or local_path.removeprefix("original/")
                if relative and relative not in {"index.html"}:
                    is_directory_reference = any(urllib.parse.urlsplit(candidate["reference"]).path.endswith("/") for candidate in path_entries)
                    if (local_relative or relative).endswith("/index.html") and is_directory_reference:
                        relative_url = (local_relative or relative).removesuffix("index.html")
                    else:
                        relative_url = relative
                    original_url = (f"http://www3.ul.ie/{relative_url}" if relative_url.startswith("icons/") else "http://www3.ul.ie/~rynnet/orthographic_projection_fyp/" + relative_url)
                    mime = mimetypes.guess_type(relative)[0] or "unknown"
                    missing_entries[relative] = {
                        "original_url": original_url,
                        "local_path": f"original/{relative}",
                        "resource_type": mime,
                        "archived_timestamp_selected": None,
                        "http_status": None,
                        "mime_type": mime,
                        "downloaded": False,
                        "exact_original": False,
                        "recovery_status": "MISSING",
                        "discovery_source": "local-link-crawl",
                        "notes": "Found in archived HTML/CSS reference scanning. No capture exists in the saved full-period namespace inventory; see archive-data/live-lookup-status.json for the direct lookup timeout and rate-limit result. An alternate-host capture could not be ruled out.",
                    }
            if index % 10 == 0 or index == len(unique_paths):
                print(f"Wayback lookup progress: {index}/{len(unique_paths)} unique local paths", flush=True)
            if not args.cached_cdx_only:
                time.sleep(1.0)
        if found_rows:
            cdx_path = ROOT / "archive-data" / "cdx-on-demand.json"
            current = []
            if cdx_path.exists():
                try:
                    current = json.loads(cdx_path.read_text(encoding="utf-8"))[1:]
                except (OSError, json.JSONDecodeError):
                    current = []
            by_key = {(row[0], row[1]): row for row in [*current, *found_rows.values()]}
            cdx_path.write_text(json.dumps([["timestamp", "original", "statuscode", "mimetype", "digest", "length"], *by_key.values()], indent=2) + "\n", encoding="utf-8")
        if path_map:
            map_path = ROOT / "archive-data" / "cdx-path-map.json"
            current_map = {}
            if map_path.exists():
                try:
                    current_map = json.loads(map_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    current_map = {}
            current_map.update(path_map)
            map_path.write_text(json.dumps(current_map, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if missing_entries and MANIFEST.exists():
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
            resources = [entry for entry in manifest.get("resources", []) if entry.get("discovery_source") != "local-link-crawl"]
            resources.extend(missing_entries.values())
            manifest["resources"] = resources
            MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(json.dumps({"unresolved_references": broken}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Unresolved local references: {len(broken)} (report: {REPORT.relative_to(ROOT)})")
    for item in broken[:40]:
        print(f"{item['source_page']}: {item['attribute']}={item['reference']} -> {item['expected_local_path']}")
    if len(broken) > 40:
        print(f"... {len(broken) - 40} additional references are in the JSON report.")


if __name__ == "__main__":
    main()
