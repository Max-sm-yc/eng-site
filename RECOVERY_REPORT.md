# Recovery report

## Scope and source

- Canonical root: `http://www3.ul.ie/~rynnet/orthographic_projection_fyp/`
- Primary page: `https://web.archive.org/web/20130812122849/http://www3.ul.ie/~rynnet/orthographic_projection_fyp/webpages/basics.html`
- Target snapshot: `20130812122849` UTC
- Unique resources tracked in the recovery manifest: 344
- Unique paths enumerated in the saved site namespace CDX inventory: 174
- Retrieved exactly from archived response: 167 (48.5% of all tracked paths; 96.0% of namespace paths)
- Retrieved from a later nearby capture: 7 (2.0% of all tracked paths)
- Reconstructed entries: 2 (0.6%)
- Missing archive payloads: 168 (48.8%)
- Combined archive payload coverage of the saved site namespace: 174/174 (100.0%)
- Combined archive payload coverage of all tracked paths: 174/344 (50.6%)
- Reconstructed local support files: 15 (listed separately from archived site resources).

The archive inventory came from the Internet Archive CDX API, querying every successful capture through the target date and then captures after it. For each path, the newest successful capture at or before the target timestamp was selected. If none existed, the first successful capture after the target was selected. The exact raw response for each HTML file is retained under `archive-data/raw-source/`; the runnable historical copy localizes same-site absolute URLs and removes one trailing encoded space from a malformed navigation reference. Two explicitly documented same-site aliases are also materialized from matching archived files.

## Recovery status

| Category | Count |
|---|---:|
| `RECOVERED_EXACT` | 167 |
| `RECOVERED_FROM_NEARBY_CAPTURE` | 7 |
| `MISSING` | 168 |
| `RECONSTRUCTED` | 2 |
| `OBSOLETE_RUNTIME` | 20 (Flash SWF files) |
| `SERVER_SIDE_UNRECOVERABLE` | 0 server-side resources identified |

- HTML responses inventoried: 73.
- GIF/SWF assets inventoried: 51.
- Local HTML files with same-site URL localization: 51.

## Obsolete runtimes and behavior

The archive contains Shockwave Flash (`.swf`) lessons and exercises. The SWF files and historical markup are preserved in `original/` and marked `OBSOLETE_RUNTIME` in the functionality field. `modern/` bundles the official Ruffle self-hosted WebAssembly runtime and adds it to the archived pages. Direct SWF links route to a small local Ruffle player. Ruffle's upstream self-hosted build is designed to polyfill existing Flash elements when its script is included ([upstream instructions](https://github.com/ruffle-rs/ruffle/blob/master/web/packages/selfhosted/README.md)).

Animated GIFs are served as the original archive payloads. No replacement animation was drawn. JavaScript files and the archived page markup are kept as captured, apart from local URL path rewrites in the runnable historical copy.

Three legacy eDrawings pages use a SolidWorks ActiveX class identifier and say Internet Explorer 5.5 or later is required. Their recovered markup contains no model filename or embedded model data, and no model resource was captured under the site path; those controls therefore remain unavailable in current browsers. The recovered pages contain no CGI/PHP/ASP form handler or other server-side behavior, so no server-side source or unrecoverable server workflow was identified.

## Documented local aliases

- `original/flash_pictures/test/next_button.jpg` is reconstructed from `original/images/next_button.jpg`. The archived Apache directory listing links to a 953-byte next_button.jpg dated 13-Nov-2008. The archived images/next_button.jpg is also 953 bytes and 136x55, matching the dimensions used by neighboring lesson pages. Reused as a documented local alias; no capture of the target path was present in the saved namespace inventory.
- `original/flash_pictures/test/sp.swf` is reconstructed from `original/sp.swf`. The archived Apache directory listing links to a 59K sp.swf dated 13-Nov-2008. The archived root sp.swf is 60,774 bytes (59.3 KiB) and is embedded by neighboring lessons. Reused as a documented local alias; no capture of the target path was present in the saved namespace inventory.

## Validation

- Unresolved local references: 520 total (260 in `original/`, 260 in `modern/`); the historical copy has 168 expected local paths (see `broken-resource-report.md` and JSON).
- Each unresolved local path was checked against the saved full-period namespace CDX inventory. A direct CDX query timed out, and the Wayback availability API returned HTTP 429 for an unresolved audio URL; further live requests were stopped to respect the rate limit. Alternate-host captures cannot be ruled out for paths absent from the saved inventory. See `archive-data/live-lookup-status.json`.
- Media integrity scan: 16 animated GIFs and 20 valid SWF files; 0 invalid media assets.
- HTTP smoke check for `original/`: 55/55 HTML pages and 3/3 selected media/runtime resources passed.
- HTTP smoke check for `modern/`: 56/56 HTML pages and 5/5 selected media/runtime resources passed.
- Browser Flash playback: UNVERIFIED. A headless Firefox attempt to open a SWF-backed lesson through Ruffle timed out with a graphics framebuffer error and produced no screenshot.
- The link checker covers HTML attributes, frames, media, download links, Flash object parameters, CSS `url()` and CSS imports.
- Serve with HTTP using the README commands; do not use `file://` because Ruffle's WebAssembly runtime requires HTTP serving.

## Fidelity and reuse

- Approximate exact recovery of the archived site namespace: 167/174 (96.0%); another 7/174 came from later captures.
- Across all 344 tracked archive and linked paths, 167/344 (48.5%) have exact payloads and 2/344 (0.6%) are explicitly reconstructed resources.
- The two reconstructed aliases use evidence recorded in the manifest. Other unresolved resources were not replaced with similarly named files.
- Fidelity confidence: high for captured static bytes and image/GIF assets; moderate for local navigation after URL localization; conditional for Flash behavior until each SWF is exercised through Ruffle.
- Copyright/republication: recovered page footers state `Copyright © Steven Colgan. All Rights Reserved.` No redistribution license was found in the captured pages. The local copy is preserved for research and educational review; obtain rights-holder permission before redistributing original site text, images, or SWFs publicly. Ruffle is separately licensed under the included MIT/Apache license files.

## Known unresolved resources

- 168 expected paths remain unresolved in `original/`; every reference in both copies and its lookup result is listed in `broken-resource-report.md`.
- Missing path types: `.wav` 59, `.avi` 29, `.jpg` 24, `.swf` 17, `.htm` 15, `.db` 10, `.gif` 5, `.html` 4, `.zip` 3, `.png` 1, `.pdf` 1.
- `original/audio/10.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/11.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/12.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/13.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/14.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 2 page(s)).
- `original/audio/15.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/16.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/17.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/18.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/2.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/23.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/24.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/25.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/26.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/28.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/29.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/3.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/30.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/31.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/32.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/33.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/34.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/35.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/36.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/37.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/38.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/39.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/4.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/40.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/41.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/42.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/43.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/44.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/48.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/5.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/50.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/51.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/52.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/53.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/54.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/55.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/56.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/57.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/58.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/59.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/6.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/60.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/61.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/62.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/63.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/64.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/65.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/66.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/67.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/68.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/69.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/7.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/8.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/audio/9.wav` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/PS2.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/coffeecup.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/ipod.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/object_10.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/object_12.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/object_15.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/object_2.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/object_3.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/object_4.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 2 page(s)).
- `original/edrawingshtml/object_5.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/object_6.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/object_8.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/tent.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/toaster.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/edrawingshtml/toastersimple.htm` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/orthoexercises/index.html` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/flash4.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/flash5.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/flash7.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/gamecube/3views.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/gamecube/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/gamecube/assem3.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/hiddendetail/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/hiddendetail/assem3.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/hiddendetail/object_16.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/hiddendetail/object_16.png` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/ipod/3views.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/ipod/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/ipod/assem4.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object10/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object10/assem9.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object10/flash11.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object4/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object4/assem3.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object4/flash4.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object5/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object5/assem4.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/object5/flash5.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/ps2/3view.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/ps2/assem1.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/section/Chap14_14_0002.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/section/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/tent/3views.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/tent/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/tent/assem1.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/toaster1/3view.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/toaster1/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/toaster1/assem2.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/toaster2/3views.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/toaster2/Thumbs.db` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/flash_pictures/test/toaster2/assem5.jpg` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/icons/back.gif` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 13 page(s)).
- `original/icons/blank.gif` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 13 page(s)).
- `original/icons/folder.gif` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 2 page(s)).
- `original/icons/image2.gif` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 12 page(s)).
- `original/icons/unknown.gif` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 12 page(s)).
- `original/pdfs/Orthographic_Activity_Sheets.pdf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/pdfs/firstangleposters/firstangleposter.zip` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/pdfs/thirdangleposter/Posters.zip` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/ppts/ortho.zip` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/quiz.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/Section Views[1].avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/gamecube/elevation.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/ipod/elevation.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object10/p10.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object11/ee11.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object12/e12.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object13/object13e.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object14/object14p.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object15/object15e.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object16/object16ee.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object16/object16p.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object2/e1.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object2/ee1.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object3/e3.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object4/e4.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object4/p4.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object5/p5.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object6/e6.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object7/e7.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/object8/ee8.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/ps2/plan.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/section movies/ccs.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/section movies/o1s.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/section movies/ps.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 2 page(s)).
- `original/solidworks_animations/movies/tent/endelevation.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/toaster1/endelevation.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/solidworks_animations/movies/toaster2/elevation.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/tv_animations/firstangle.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/tv_animations/thirdangle.avi` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/b2.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/b3.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/b4.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/b5.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/b6.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/c2.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/c5.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/c6.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/ce3.html` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/ce4.html` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/h2.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/h3.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/h4.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/oe1.html` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/s2.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/s3.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/s4.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/s5.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).
- `original/webpages/s6.swf` (no successful capture in the complete saved namespace inventory; live endpoint outcome is recorded in archive-data/live-lookup-status.json; referenced by 1 page(s)).

## Later capture substitutions

- `original/Templates/template.dwt` from capture `20140928032556`.
- `original/audio/45.wav` from capture `20160328095443`.
- `original/audio/46.wav` from capture `20160328095554`.
- `original/audio/47.wav` from capture `20160328113243`.
- `original/audio/49.wav` from capture `20160328095503`.
- `original/soildworks_objects_images/curved/gamecube/ea-0000.bmp` from capture `20150218192954`.
- `original/soildworks_objects_images/curved/gamecube/ea-0000.png` from capture `20150218192958`.
