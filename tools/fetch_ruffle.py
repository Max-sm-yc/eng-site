#!/usr/bin/env python3
"""Fetch the pinned official self-hosted Ruffle release used by modern/."""

from __future__ import annotations

import io
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "vendor" / "ruffle"
TAG = "nightly-2026-10-06"


def main() -> None:
    api_url = f"https://api.github.com/repos/ruffle-rs/ruffle/releases/tags/{TAG}"
    request = urllib.request.Request(api_url, headers={"User-Agent": "orthographic-projection-recovery/1.0", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        release = json.load(response)
    asset = next((entry for entry in release["assets"] if "web-selfhosted.zip" in entry["name"]), None)
    if asset is None:
        raise SystemExit(f"no self-hosted web runtime found in {TAG}")
    request = urllib.request.Request(asset["browser_download_url"], headers={"User-Agent": "orthographic-projection-recovery/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()
    DESTINATION.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        for entry in archive.infolist():
            if entry.is_dir():
                continue
            target = DESTINATION / Path(entry.filename).name
            target.write_bytes(archive.read(entry))
    metadata = {
        "upstream": "https://github.com/ruffle-rs/ruffle",
        "release_tag": TAG,
        "asset_name": asset["name"],
        "asset_url": asset["browser_download_url"],
        "asset_bytes": len(payload),
        "asset_sha256": hashlib.sha256(payload).hexdigest(),
    }
    (ROOT / "vendor" / "ruffle-release.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Installed {asset['name']} ({len(payload)} compressed bytes) in {DESTINATION.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
