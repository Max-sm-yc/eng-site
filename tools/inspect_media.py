#!/usr/bin/env python3
"""Check recovered GIF animation blocks and legacy SWF headers without extra packages."""

from __future__ import annotations

import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "original"


def gif_metrics(data: bytes) -> dict:
    if data[:6] not in (b"GIF87a", b"GIF89a") or len(data) < 13:
        raise ValueError("invalid GIF header")
    width, height = struct.unpack_from("<HH", data, 6)
    packed = data[10]
    pos = 13
    if packed & 0x80:
        pos += 3 * (1 << ((packed & 7) + 1))
    frames = 0
    duration_cs = 0
    while pos < len(data):
        marker = data[pos]
        pos += 1
        if marker == 0x3B:
            break
        if marker == 0x2C:
            if pos + 9 > len(data):
                raise ValueError("truncated image descriptor")
            image_packed = data[pos + 8]
            pos += 9
            if image_packed & 0x80:
                pos += 3 * (1 << ((image_packed & 7) + 1))
            pos += 1  # LZW minimum code size
            pos = skip_subblocks(data, pos)
            frames += 1
        elif marker == 0x21:
            if pos >= len(data):
                raise ValueError("truncated extension block")
            label = data[pos]
            pos += 1
            if label == 0xF9 and pos + 6 <= len(data) and data[pos] == 4:
                duration_cs += int.from_bytes(data[pos + 2 : pos + 4], "little")
            pos = skip_subblocks(data, pos)
        else:
            raise ValueError(f"unexpected block marker 0x{marker:02x} at byte {pos - 1}")
    return {"width": width, "height": height, "frames": frames, "duration_seconds": round(duration_cs / 100, 2), "animated": frames > 1}


def skip_subblocks(data: bytes, pos: int) -> int:
    while pos < len(data):
        length = data[pos]
        pos += 1
        if length == 0:
            return pos
        pos += length
    raise ValueError("unterminated data sub-block")


def swf_metrics(data: bytes) -> dict:
    signature = data[:3].decode("ascii", errors="replace")
    if signature not in {"FWS", "CWS", "ZWS"} or len(data) < 8:
        raise ValueError("invalid SWF header")
    return {"signature": signature, "version": data[3], "declared_uncompressed_bytes": int.from_bytes(data[4:8], "little"), "file_bytes": len(data)}


def main() -> None:
    results = []
    errors = []
    for path in sorted(ORIGINAL.rglob("*")):
        if not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix not in {".gif", ".swf"}:
            continue
        try:
            data = path.read_bytes()
            metrics = gif_metrics(data) if suffix == ".gif" else swf_metrics(data)
            results.append({"local_path": path.relative_to(ROOT).as_posix(), **metrics})
        except Exception as exc:
            errors.append({"local_path": path.relative_to(ROOT).as_posix(), "error": f"{type(exc).__name__}: {exc}"})
    output = {"gif_and_swf_assets": results, "invalid_assets": errors}
    (ROOT / "media-inspection.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    animated = sum(item.get("animated", False) for item in results)
    swfs = sum("signature" in item for item in results)
    print(f"Inspected {len(results)} GIF/SWF files: {animated} animated GIFs, {swfs} SWFs, {len(errors)} invalid assets.")


if __name__ == "__main__":
    main()
