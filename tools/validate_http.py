#!/usr/bin/env python3
"""Check every local HTML page and representative media over HTTP."""

from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "validation-report.json"


def request(base_url: str, path: str, method: str = "GET") -> dict:
    url = base_url.rstrip("/") + "/" + urllib.parse.quote(path.lstrip("/"), safe="/?=&%")
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "orthographic-projection-recovery/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            if method == "GET":
                response.read()
            return {
                "url": url,
                "status": response.status,
                "content_type": response.headers.get_content_type(),
                "content_length": response.headers.get("Content-Length"),
                "error": None,
            }
    except (OSError, urllib.error.URLError) as exc:
        return {"url": url, "status": None, "content_type": None, "content_length": None, "error": f"{type(exc).__name__}: {exc}"}


def validate_copy(name: str, base_url: str) -> dict:
    root = ROOT / name
    pages = sorted([*root.rglob("*.html"), *root.rglob("*.htm")])
    page_results = [request(base_url, page.relative_to(root).as_posix()) for page in pages]
    page_failures = [result for result in page_results if result["status"] != 200 or not (result["content_type"] or "").startswith("text/html")]
    assets = {
        "animated_gif_sample": "images/ee1.gif",
        "swf_sample": "flashanimations/section/section.swf",
    }
    if name == "original":
        assets["documented_swf_alias"] = "flash_pictures/test/sp.swf"
    else:
        assets.update({
            "ruffle_runtime": "ruffle/ruffle.js",
            "ruffle_player": "player.html",
            "ruffle_wasm": next(path.relative_to(root).as_posix() for path in sorted((root / "ruffle").glob("*.wasm"))),
        })
    asset_results = {label: request(base_url, path, "HEAD") for label, path in assets.items()}
    bad_assets = []
    for label, result in asset_results.items():
        mime = result.get("content_type") or ""
        accepted = {
            "animated_gif_sample": mime == "image/gif",
            "swf_sample": "flash" in mime,
            "documented_swf_alias": "flash" in mime,
            "ruffle_runtime": "javascript" in mime,
            "ruffle_player": mime.startswith("text/html"),
            "ruffle_wasm": mime == "application/wasm",
        }.get(label, False)
        if result.get("status") != 200 or not accepted:
            bad_assets.append({"label": label, **result})
    return {
        "base_url": base_url,
        "html_page_count": len(pages),
        "html_pages_passed": len(pages) - len(page_failures),
        "html_failures": page_failures,
        "assets": asset_results,
        "asset_failures": bad_assets,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", default="http://127.0.0.1:8000", help="base URL serving original/")
    parser.add_argument("--modern", default="http://127.0.0.1:8001", help="base URL serving modern/")
    args = parser.parse_args()
    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "copies": {
            "original": validate_copy("original", args.original),
            "modern": validate_copy("modern", args.modern),
        },
        "browser_flash_playback": {
            "status": "UNVERIFIED",
            "note": "A headless Firefox attempt to open a SWF-backed lesson through Ruffle timed out with a graphics framebuffer error and produced no screenshot.",
        },
    }
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    failures = sum(len(copy["html_failures"]) + len(copy["asset_failures"]) for copy in result["copies"].values())
    for name, copy in result["copies"].items():
        print(f"{name}: {copy['html_pages_passed']}/{copy['html_page_count']} HTML pages and {len(copy['assets']) - len(copy['asset_failures'])}/{len(copy['assets'])} sample assets passed.")
    print(f"Browser Flash playback remains unverified. Validation report: {OUTPUT.relative_to(ROOT)}")
    if failures:
        raise SystemExit(f"{failures} HTTP validation check(s) failed")


if __name__ == "__main__":
    main()
