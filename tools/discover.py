#!/usr/bin/env python3
"""Inventory Internet Archive captures for the University of Limerick site."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timedelta
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DATA = ROOT / "archive-data"
PREFIX = "www3.ul.ie/~rynnet/orthographic_projection_fyp/*"
FIELDS = "timestamp,original,statuscode,mimetype,digest,length"


def query_capture_range(label: str, params: dict[str, str], destination: Path) -> None:
    params = {"url": PREFIX, "output": "json", "filter": "statuscode:200", "fl": FIELDS, **params}
    url = "https://web.archive.org/cdx/search/cdx?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": "orthographic-projection-recovery/1.0"})
    last_error: Exception | None = None
    for attempt in range(1, 5):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read()
            rows = json.loads(body)
            if not rows or rows[0] != FIELDS.split(","):
                raise ValueError("unexpected CDX response schema")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(body)
            print(f"{label}: {len(rows) - 1} successful captures saved to {destination.relative_to(ROOT)}")
            return
        except Exception as exc:  # archive returns transient 503s for wide queries
            last_error = exc
            if attempt < 4:
                delay = 2 * attempt
                print(f"{label}: attempt {attempt} failed ({exc}); retrying in {delay}s")
                time.sleep(delay)
    raise RuntimeError(f"could not query {label}: {last_error}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cutoff", default="20130812", help="CDX date cutoff in YYYYMMDD form")
    args = parser.parse_args()
    ARCHIVE_DATA.mkdir(exist_ok=True)
    query_capture_range(
        "captures through target date",
        {"to": args.cutoff},
        ARCHIVE_DATA / f"cdx-through-{args.cutoff}.json",
    )
    next_day = (datetime.strptime(args.cutoff, "%Y%m%d") + timedelta(days=1)).strftime("%Y%m%d")
    time.sleep(2)
    query_capture_range(
        "captures after target date",
        {"from": next_day},
        ARCHIVE_DATA / f"cdx-after-{args.cutoff}.json",
    )


if __name__ == "__main__":
    main()
