#!/usr/bin/env python3
"""Build a faithful copy with local Ruffle support for archived Flash content."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "original"
MODERN = ROOT / "modern"
RUFFLE = ROOT / "vendor" / "ruffle"
MANIFEST_PATH = ROOT / "recovery-manifest.json"
INJECT = '<script src="/ruffle/ruffle.js"></script>\n<script src="/ruffle-bridge.js"></script>'


def hardlink_or_copy(source: str, target: str) -> str:
    try:
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        Path(target).unlink(missing_ok=True)
        Path(target).hardlink_to(source)
    except OSError:
        shutil.copy2(source, target)
    return target


def copy_site_file(source: str, target: str) -> str:
    if Path(source).suffix.lower() in {".html", ".htm"}:
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        return target
    return hardlink_or_copy(source, target)


def add_runtime(page: Path) -> None:
    content = page.read_bytes()
    if b"/ruffle/ruffle.js" in content:
        return
    html = content.decode("latin-1")
    if re.search(r"</head\s*>", html, flags=re.IGNORECASE):
        html = re.sub(r"</head\s*>", INJECT + "\n</head>", html, count=1, flags=re.IGNORECASE)
    elif re.search(r"<body\b", html, flags=re.IGNORECASE):
        html = re.sub(r"<body\b", "<head>" + INJECT + "</head>\n<body", html, count=1, flags=re.IGNORECASE)
    else:
        html = INJECT + "\n" + html
    page.write_bytes(html.encode("latin-1"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ruffle-dir", type=Path, default=RUFFLE, help="directory containing ruffle.js and its runtime files")
    args = parser.parse_args()
    if not ORIGINAL.is_dir() or not any(ORIGINAL.rglob("*.html")):
        raise SystemExit("original/ is empty; run tools/download.py first")
    if not args.ruffle_dir.joinpath("ruffle.js").is_file():
        raise SystemExit("Ruffle is not installed. Run tools/fetch_ruffle.py first.")

    if MODERN.exists():
        shutil.rmtree(MODERN)
    shutil.copytree(ORIGINAL, MODERN, copy_function=copy_site_file)
    for page in [*MODERN.rglob("*.html"), *MODERN.rglob("*.htm")]:
        add_runtime(page)
    (MODERN / "ruffle").mkdir(parents=True, exist_ok=True)
    for file in args.ruffle_dir.iterdir():
        if file.is_file():
            hardlink_or_copy(str(file), str(MODERN / "ruffle" / file.name))
    (MODERN / "ruffle-bridge.js").write_text(
        """// Route direct SWF links through the local Ruffle player.
document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href]');
  if (!link) return;
  const target = new URL(link.href, location.href);
  if (target.origin !== location.origin || !target.pathname.toLowerCase().endsWith('.swf')) return;
  event.preventDefault();
  location.href = '/player.html?movie=' + encodeURIComponent(target.pathname + target.search);
});
""",
        encoding="utf-8",
    )
    (MODERN / "player.html").write_text(
        """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Flash exercise · Ruffle</title>
<script src="/ruffle/ruffle.js"></script></head><body>
<p><a href="javascript:history.back()">Return to the lesson</a></p><main id="player"></main>
<script>
const movie = new URLSearchParams(location.search).get('movie');
if (!movie || !movie.startsWith('/') || !movie.toLowerCase().split('?')[0].endsWith('.swf')) {
  document.querySelector('#player').textContent = 'No valid local SWF was selected.';
} else {
  const ruffle = window.RufflePlayer.newest();
  const player = ruffle.createPlayer();
  player.style.width = 'min(100%, 960px)'; player.style.height = 'min(80vh, 720px)';
  document.querySelector('#player').appendChild(player);
  player.ruffle().load(movie);
}
</script></body></html>
""",
        encoding="utf-8",
    )
    (MODERN / "THIRD_PARTY_NOTICES.md").write_text(
        """# Third-party runtime

The compatibility copy bundles the official Ruffle self-hosted web runtime.
Pinned release: `nightly-2026-10-06`. Its `LICENSE_MIT`, `LICENSE_APACHE`,
and upstream `README.md` are included under `ruffle/`.

Upstream project: https://github.com/ruffle-rs/ruffle
Release archive: https://github.com/ruffle-rs/ruffle/releases/tag/nightly-2026-10-06
""",
        encoding="utf-8",
    )
    print(f"Built modern/ from {ORIGINAL.relative_to(ROOT)} with Ruffle polyfill and direct-SWF player.")
    if MANIFEST_PATH.exists():
        import json
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        support = list(manifest.get("support_files", []))
        for local_path, mime, notes in [
            ("modern/player.html", "text/html", "Reconstructed compatibility player for direct SWF links; backed by the official Ruffle runtime."),
            ("modern/ruffle-bridge.js", "application/javascript", "Reconstructed bridge to open direct SWF links in Ruffle."),
        ]:
            support = [entry for entry in support if entry.get("local_path") != local_path]
            support.append({"original_url": None, "local_path": local_path, "resource_type": mime, "archived_timestamp_selected": None, "http_status": None, "mime_type": mime, "downloaded": True, "exact_original": False, "recovery_status": "RECONSTRUCTED", "notes": notes})
        for runtime_file in sorted((MODERN / "ruffle").iterdir()):
            if not runtime_file.is_file():
                continue
            local_path = runtime_file.relative_to(ROOT).as_posix()
            mime = "application/wasm" if runtime_file.suffix == ".wasm" else "text/javascript" if runtime_file.suffix == ".js" else "application/octet-stream"
            support = [entry for entry in support if entry.get("local_path") != local_path]
            support.append({"original_url": "https://github.com/ruffle-rs/ruffle/releases/tag/nightly-2026-10-06", "local_path": local_path, "resource_type": mime, "archived_timestamp_selected": None, "http_status": 200, "mime_type": mime, "downloaded": True, "exact_original": False, "recovery_status": "RECONSTRUCTED", "notes": "Official third-party Ruffle self-hosted release asset; not part of the historical website."})
        manifest["support_files"] = support
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
