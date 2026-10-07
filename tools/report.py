#!/usr/bin/env python3
"""Render RECOVERY_REPORT.md and a human-readable broken-resource report."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "recovery-manifest.json"
BROKEN = ROOT / "broken-resource-report.json"
MEDIA = ROOT / "media-inspection.json"
HTTP_VALIDATION = ROOT / "validation-report.json"


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit("recovery-manifest.json is missing; run tools/download.py first")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("resources", [])
    statuses = Counter(entry.get("recovery_status", "MISSING") for entry in entries)
    unresolved = json.loads(BROKEN.read_text(encoding="utf-8")).get("unresolved_references", []) if BROKEN.exists() else []
    media_info = json.loads(MEDIA.read_text(encoding="utf-8")) if MEDIA.exists() else {"gif_and_swf_assets": [], "invalid_assets": []}
    http_validation = json.loads(HTTP_VALIDATION.read_text(encoding="utf-8")) if HTTP_VALIDATION.exists() else {}
    media_assets = media_info.get("gif_and_swf_assets", [])
    animated_gifs = sum(item.get("animated", False) for item in media_assets)
    valid_swfs = sum("signature" in item for item in media_assets)
    support_files = manifest.get("support_files", [])
    aliases = [entry for entry in entries if entry.get("discovery_source") == "documented-local-alias"]
    exact = statuses.get("RECOVERED_EXACT", 0)
    nearby = statuses.get("RECOVERED_FROM_NEARBY_CAPTURE", 0)
    reconstructed = statuses.get("RECONSTRUCTED", 0)
    missing = statuses.get("MISSING", 0)
    obsolete_runtime = sum(entry.get("functionality_status") == "OBSOLETE_RUNTIME" for entry in entries)
    server_side = sum(entry.get("recovery_status") == "SERVER_SIDE_UNRECOVERABLE" for entry in entries)
    total = len(entries)
    captured = exact + nearby
    pct = lambda count: f"{100 * count / total:.1f}%" if total else "0%"
    namespace_total = manifest.get("archive_namespace_path_count", total)
    namespace_exact_pct = f"{100 * exact / namespace_total:.1f}%" if namespace_total else "0%"
    namespace_combined_pct = f"{100 * (exact + nearby) / namespace_total:.1f}%" if namespace_total else "0%"
    original_unresolved = [item for item in unresolved if item.get("site_copy") == "original"]
    unresolved_paths = len({item.get("expected_local_path") for item in original_unresolved})
    unresolved_extensions = Counter(
        Path(path).suffix.lower() or "[no extension]"
        for path in {item.get("expected_local_path", "").removeprefix("original/") for item in original_unresolved}
    )
    unresolved_by_copy = Counter(item.get("site_copy") for item in unresolved)
    html = [entry for entry in entries if (entry.get("mime_type") or "").startswith("text/html")]
    animations = [entry for entry in entries if (entry.get("mime_type") or "").lower() in {"image/gif", "application/x-shockwave-flash"}]
    lines = [
        "# Recovery report",
        "",
        "## Scope and source",
        "",
        f"- Canonical root: `{manifest.get('source_root')}`",
        f"- Primary page: `{manifest.get('primary_archived_page')}`",
        f"- Target snapshot: `{manifest.get('target_timestamp')}` UTC",
        f"- Unique resources tracked in the recovery manifest: {total}",
        f"- Unique paths enumerated in the saved site namespace CDX inventory: {namespace_total}",
        f"- Retrieved exactly from archived response: {exact} ({pct(exact)} of all tracked paths; {namespace_exact_pct} of namespace paths)",
        f"- Retrieved from a later nearby capture: {nearby} ({pct(nearby)} of all tracked paths)",
        f"- Reconstructed entries: {reconstructed} ({pct(reconstructed)})",
        f"- Missing archive payloads: {missing} ({pct(missing)})",
        f"- Combined archive payload coverage of the saved site namespace: {exact + nearby}/{namespace_total} ({namespace_combined_pct})",
        f"- Combined archive payload coverage of all tracked paths: {captured}/{total} ({pct(captured)})",
        f"- Reconstructed local support files: {sum(entry.get('recovery_status') == 'RECONSTRUCTED' for entry in support_files)} (listed separately from archived site resources).",
        "",
        "The archive inventory came from the Internet Archive CDX API, querying every successful capture through the target date and then captures after it. For each path, the newest successful capture at or before the target timestamp was selected. If none existed, the first successful capture after the target was selected. The exact raw response for each HTML file is retained under `archive-data/raw-source/`; the runnable historical copy localizes same-site absolute URLs and removes one trailing encoded space from a malformed navigation reference. Two explicitly documented same-site aliases are also materialized from matching archived files.",
        "",
        "## Recovery status",
        "",
        "| Category | Count |",
        "|---|---:|",
        f"| `RECOVERED_EXACT` | {exact} |",
        f"| `RECOVERED_FROM_NEARBY_CAPTURE` | {nearby} |",
        f"| `MISSING` | {missing} |",
        f"| `RECONSTRUCTED` | {reconstructed} |",
        f"| `OBSOLETE_RUNTIME` | {obsolete_runtime} (Flash SWF files) |",
        f"| `SERVER_SIDE_UNRECOVERABLE` | {server_side} server-side resources identified |",
        "",
        f"- HTML responses inventoried: {len(html)}.",
        f"- GIF/SWF assets inventoried: {len(animations)}.",
        f"- Local HTML files with same-site URL localization: {sum(bool(e.get('local_copy_rewritten')) for e in entries)}.",
        "",
        "## Obsolete runtimes and behavior",
        "",
        "The archive contains Shockwave Flash (`.swf`) lessons and exercises. The SWF files and historical markup are preserved in `original/` and marked `OBSOLETE_RUNTIME` in the functionality field. `modern/` bundles the official Ruffle self-hosted WebAssembly runtime and adds it to the archived pages. Direct SWF links route to a small local Ruffle player. Ruffle's upstream self-hosted build is designed to polyfill existing Flash elements when its script is included ([upstream instructions](https://github.com/ruffle-rs/ruffle/blob/master/web/packages/selfhosted/README.md)).",
        "",
        "Animated GIFs are served as the original archive payloads. No replacement animation was drawn. JavaScript files and the archived page markup are kept as captured, apart from local URL path rewrites in the runnable historical copy.",
        "",
        "Three legacy eDrawings pages use a SolidWorks ActiveX class identifier and say Internet Explorer 5.5 or later is required. Their recovered markup contains no model filename or embedded model data, and no model resource was captured under the site path; those controls therefore remain unavailable in current browsers. The recovered pages contain no CGI/PHP/ASP form handler or other server-side behavior, so no server-side source or unrecoverable server workflow was identified.",
        "",
        "## Documented local aliases",
        "",
        *[
            f"- `{entry.get('local_path')}` is reconstructed from `{entry.get('source_local_path')}`. {entry.get('notes', '')}"
            for entry in aliases
        ],
        "",
        "## Validation",
        "",
        f"- Unresolved local references: {len(unresolved)} total ({unresolved_by_copy.get('original', 0)} in `original/`, {unresolved_by_copy.get('modern', 0)} in `modern/`); the historical copy has {unresolved_paths} expected local paths (see `broken-resource-report.md` and JSON).",
        "- Each unresolved local path was checked against the saved full-period namespace CDX inventory. A direct CDX query timed out, and the Wayback availability API returned HTTP 429 for an unresolved audio URL; further live requests were stopped to respect the rate limit. Alternate-host captures cannot be ruled out for paths absent from the saved inventory. See `archive-data/live-lookup-status.json`.",
        f"- Media integrity scan: {animated_gifs} animated GIFs and {valid_swfs} valid SWF files; {len(media_info.get('invalid_assets', []))} invalid media assets.",
        *[
            f"- HTTP smoke check for `{name}/`: {copy.get('html_pages_passed', 0)}/{copy.get('html_page_count', 0)} HTML pages and {len(copy.get('assets', {})) - len(copy.get('asset_failures', []))}/{len(copy.get('assets', {}))} selected media/runtime resources passed."
            for name, copy in http_validation.get("copies", {}).items()
        ],
        f"- Browser Flash playback: {http_validation.get('browser_flash_playback', {}).get('status', 'not attempted')}. {http_validation.get('browser_flash_playback', {}).get('note', '')}".rstrip(),
        "- The link checker covers HTML attributes, frames, media, download links, Flash object parameters, CSS `url()` and CSS imports.",
        "- Serve with HTTP using the README commands; do not use `file://` because Ruffle's WebAssembly runtime requires HTTP serving.",
        "",
        "## Fidelity and reuse",
        "",
        f"- Approximate exact recovery of the archived site namespace: {exact}/{namespace_total} ({namespace_exact_pct}); another {nearby}/{namespace_total} came from later captures.",
        f"- Across all {total} tracked archive and linked paths, {exact}/{total} ({pct(exact)}) have exact payloads and {reconstructed}/{total} ({pct(reconstructed)}) are explicitly reconstructed resources.",
        "- The two reconstructed aliases use evidence recorded in the manifest. Other unresolved resources were not replaced with similarly named files.",
        "- Fidelity confidence: high for captured static bytes and image/GIF assets; moderate for local navigation after URL localization; conditional for Flash behavior until each SWF is exercised through Ruffle.",
        "- Copyright/republication: recovered page footers state `Copyright © Steven Colgan. All Rights Reserved.` No redistribution license was found in the captured pages. The local copy is preserved for research and educational review; obtain rights-holder permission before redistributing original site text, images, or SWFs publicly. Ruffle is separately licensed under the included MIT/Apache license files.",
        "",
        "## Known unresolved resources",
        "",
    ]
    if unresolved:
        grouped_unresolved = {}
        for item in original_unresolved:
            grouped_unresolved.setdefault(item.get("expected_local_path", ""), []).append(item)
        lines.append(f"- {len(grouped_unresolved)} expected paths remain unresolved in `original/`; every reference in both copies and its lookup result is listed in `broken-resource-report.md`.")
        lines.append("- Missing path types: " + ", ".join(f"`{extension}` {count}" for extension, count in unresolved_extensions.most_common()) + ".")
        for path, references in sorted(grouped_unresolved.items()):
            state = references[0].get("wayback_lookup", "")
            source_pages = sorted({item.get("source_page", "") for item in references})
            lines.append(f"- `{path}` ({state or 'local file missing'}; referenced by {len(source_pages)} page(s)).")
    else:
        lines.append("- None reported by the local checker.")
    nearby_entries = [entry for entry in entries if entry.get("recovery_status") == "RECOVERED_FROM_NEARBY_CAPTURE"]
    lines.extend(["", "## Later capture substitutions", ""])
    if nearby_entries:
        lines.extend(f"- `{entry.get('local_path')}` from capture `{entry.get('archived_timestamp_selected')}`." for entry in nearby_entries)
    else:
        lines.append("- None.")
    (ROOT / "RECOVERY_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    broken_lines = ["# Broken resource report", "", f"Unresolved same-site references: {len(unresolved)}", ""]
    if unresolved:
        broken_lines.extend(["| Source page | Reference | Local path | Wayback lookup |", "|---|---|---|---|"])
        for item in unresolved:
            values = [item.get("source_page", ""), item.get("reference", ""), item.get("expected_local_path", ""), item.get("wayback_lookup", "not checked")]
            broken_lines.append("| " + " | ".join(value.replace("|", "\\|").replace("\n", " ") for value in values) + " |")
    else:
        broken_lines.append("The local checker found no unresolved same-site references.")
    (ROOT / "broken-resource-report.md").write_text("\n".join(broken_lines) + "\n", encoding="utf-8")
    print(f"Wrote RECOVERY_REPORT.md and broken-resource-report.md ({len(unresolved)} unresolved references).")


if __name__ == "__main__":
    main()
