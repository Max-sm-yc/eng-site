# Orthographic projection archive reconstruction

This repository preserves the University of Limerick orthographic projection learning module from Internet Archive captures. The historical copy is in `original/`; `modern/` is generated from it with a local Ruffle runtime for Flash content. The existing top-level lesson app is retained separately.

- Source root: <http://www3.ul.ie/~rynnet/orthographic_projection_fyp/>
- Primary page: <https://web.archive.org/web/20130812122849/http://www3.ul.ie/~rynnet/orthographic_projection_fyp/webpages/basics.html>
- Target snapshot: 2013-08-12 12:28:49 UTC

## Run locally

Use HTTP rather than opening HTML files directly:

```sh
python -m http.server 8000 --directory original
```

Open `http://localhost:8000/`. The root entry links to the archived home page and the requested `basics.html` page.

For Flash compatibility:

```sh
python -m http.server 8001 --directory modern
```

Open `http://localhost:8001/`. `modern/` bundles the pinned Ruffle self-hosted release and keeps the original SWF files alongside the historical markup.

## Deploy on Vercel

`vercel.json` configures a static deployment with `modern/` as the output directory and no build step. Import the repository with the repository root as the Vercel project root; the production domain will serve the Ruffle-compatible reconstruction at `/`. The preserved `original/` copy, recovery data, tooling, and existing top-level lesson app are retained in the repo and excluded from the Vercel output.

Vercel applies the configured `application/wasm` and Flash MIME types needed by the compatibility copy. See the [Vercel project configuration reference](https://vercel.com/docs/project-configuration/vercel-json).

For Hobby, Vercel’s Git integration is the practical deployment route: `modern/` is about 135 MB, above the CLI’s 100 MB Hobby source upload limit. Hobby Git integration does not deploy from private repositories owned by a Git organization; check Vercel’s [Git deployment rules](https://vercel.com/docs/git) if that applies. The Pro CLI source upload limit is 1 GB. `.vercelignore` omits the separate preservation tree and recovery tooling from CLI uploads, but the modern site itself remains above the Hobby CLI limit. See [Vercel limits](https://vercel.com/docs/limits).

No Vercel project has been linked and no deployment has been launched. The historical content’s copyright and reuse notes remain in `RECOVERY_REPORT.md`.

## Recovery workflow

Python 3 standard library only; there are no build dependencies.

```sh
python tools/discover.py
python tools/download.py --workers 1
python tools/check_links.py --site original --lookup-archive
# If direct CDX lookup is unavailable, use this instead:
# python tools/check_links.py --site original --lookup-archive --cached-cdx-only
python tools/download.py --workers 1
python tools/fetch_ruffle.py
python tools/build_modern.py
python tools/check_links.py --site both --lookup-archive --cached-cdx-only
python tools/validate_http.py --original http://127.0.0.1:8000 --modern http://127.0.0.1:8001
python tools/report.py
```

`discover.py` saves the CDX inventory under `archive-data/`. `download.py` chooses the newest successful capture at or before the target timestamp for each path and uses a later capture only when no earlier one exists. It makes a small number of concurrent Wayback requests, retries transient failures, verifies payload digests, preserves exact HTML responses under `archive-data/raw-source/`, and localizes same-site absolute links in the runnable HTML copy. The local copy retains the old filenames and directory layout.

The validation command assumes the `original/` and `modern/` HTTP servers shown above are running in separate terminals.

## Recovery records

- `recovery-manifest.json` records one selected archived resource per site path, its source URL, timestamp, MIME type, status, digest, local path, and recovery category.
- `RECOVERY_REPORT.md` summarizes fidelity, missing resources, obsolete technologies, and known reuse considerations.
- `broken-resource-report.json` and `.md` list broken internal references and, when requested, their last Wayback lookup result.
- `archive-data/cdx-*.json` stores the successful capture inventory used for selection.

See the recovery report for source fidelity, limitations, and copyright notes. Vercel deployment settings are prepared, but no deployment has been launched.

## Recovery summary and limits

- The saved Wayback namespace inventory contains 174 unique site paths: 167 exact captures (96.0%) and 7 later nearby captures. The unresolved link crawl found 168 additional expected paths without a capture in that saved inventory; the full reference list is in `broken-resource-report.md`.
- Major unresolved items are 59 WAV files, 29 AVI clips, 17 SWF paths, 15 eDrawings HTM pages, 24 JPGs, three ZIP archives, and one PDF. The detailed report includes all 168 expected paths and all broken references.
- Direct CDX lookup timed out, and the Wayback availability API returned HTTP 429 for an unresolved audio URL. Further live requests were stopped to respect the rate limit. `check_links.py --cached-cdx-only` checks every distinct expected local path against the saved full-period CDX inventory; paths absent from that inventory are recorded as missing, with alternate-host uncertainty noted. Details are in `archive-data/live-lookup-status.json`.
- The recovered site contains Flash SWFs and three SolidWorks eDrawings pages with the obsolete ActiveX control. `modern/` uses Ruffle for SWFs; the eDrawings pages expose no embedded model data or model filename in their recovered markup.
- HTTP checks passed for all 55 historical HTML pages and all 56 compatibility-copy HTML pages, plus representative image, SWF, Ruffle JavaScript, and WebAssembly responses. A headless Firefox attempt to exercise an embedded SWF timed out with a graphics framebuffer error, so Ruffle playback remains unverified.
- Two broken directory-listing links are restored as documented aliases: `next_button.jpg` uses the captured same-name 953-byte image with matching 136×55 dimensions, and `sp.swf` uses the captured root SWF whose size matches the listing’s 59K entry. Both are marked `RECONSTRUCTED` in the manifest.
- Copyright footers identify Steven Colgan and state “All Rights Reserved.” No redistribution license was found. Obtain rights-holder permission before publicly redistributing the recovered text, images, or SWFs. The local copy is for preservation and educational review.
