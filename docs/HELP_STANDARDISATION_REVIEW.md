# Wavelink development list — Help standardisation

Requested by Adriano on 25 September 2026: review all Help because presentation is inconsistent and some pages appear as plain text files. This list is retained alongside the inventory-first and app-wide interface roadmap.

## Source findings in the supplied UI06 package

The registered browser guide contains **76 HTML topic files**. Of these, **69** link one older-version Help stylesheet URL, **two** another Help stylesheet URL, **four** define their own inline styles without that shared stylesheet, and **one** (Fault Reports) links the application stylesheet. This is a verified inconsistency in presentation; the registered browser topics are HTML, not evidence that every file the user described is literally a `.txt` file.

Four independently styled pages are **Company branding, Imports & examples, HSE / QSHE, and Record management**. The audit also found **73 relative `.html` topic-link occurrences** in the old topic pages. Their shared navigation is replaced with canonical `/help/topics/<id>` links. The source-content link adjustments are individually listed in `VALIDATION/HELP_AUDIT.json`.

The browser Help endpoint imported `TOPIC_IDS` from the desktop module, thereby importing Tkinter for a public static page. UI07 moves that server import to a headless allowlist with exactly the same IDs and labels. Desktop code is not opened or changed by this route.

One registered topic contains an intentional plain-text checklist example in `<pre>`. That example is preserved as code/text. Existing wording and historical version labels are not silently rewritten during styling.

## Checklist and acceptance criteria

| ID | Work item | State after UI07 | Completion criterion |
|---|---|---|---|
| HELP-01 | Inventory all registered browser topics and their presentation | Completed for the 76 registered topic pages | Inventory, file hashes, source stylesheet signatures and link findings recorded. Other help surfaces are not implied to be covered. |
| HELP-02 | Common browser Help centre and topic layout | Implemented; locally tested | All registered topics share navigation/styles, have one main landmark and a readable heading, preserve instructional text, and offer topic search and section links. Live-device acceptance remains. |
| HELP-03 | Remove the Help route's desktop-module import | Implemented; locally tested | All 76 topics return HTML while Tkinter/desktop Help imports are deliberately blocked; unknown topics remain 404. No operational writes. |
| HELP-04 | Recheck the wording against current UI01–UI07 controls | Pending | Verify actual labels, paths, action effects, role restrictions, saving/retry behaviour and screenshots topic by topic. Retain documented limitations and distinguish historical notes from current instructions. |
| HELP-05 | Separate local-vessel and hosted-browser instructions | Pending | Clearly distinguish Windows setup, native imports, local saved forms, browser administration, hosted recovery and server operation. Never imply cloud/vessel synchronisation, multi-company isolation or approved recovery without corresponding implementation and tests. |
| HELP-06 | Review every Help entry point and special page | Pending | Audit Account menus, inline hints, modal Help, tooltips, `/install`, `/contact`, `/examples`, source/README links and missing-page behaviour; preserve unfinished operational forms and useful return destinations. |
| HELP-07 | Standardise native/local Help and the master PDF from reviewed source | Pending | Keep native topic IDs, local file opening, readable style, contents, bookmarks and numbering consistent. Rebuild and visually inspect each output; do not replace them with unreviewed generated summaries. |
| HELP-08 | Review examples, downloads and links across all guide formats | Pending beyond registered browser navigation | Verify each supported importer and version boundary, filenames, sample packs, report examples and original-document references. Do not describe planning CSV/XLSX files as supported importers. |
| HELP-09 | Accessibility and physical-device acceptance | Partial local checks; not complete | Keyboard and screen-reader tests; contrast/focus/zoom; phone/tablet and desktop layouts; print output; tables; slow/failed connections; no browser-storage loss. |
| HELP-10 | Prevent future style and Help/desktop dependency regressions | Partly implemented | Shared template/route tests included in UI07. Consolidate authoring/build scripts and CI so future releases do not overwrite styled pages with unrelated formats or drift the native and headless catalogues. |

## Source fidelity and scope

UI07 preserves every registered topic's instructional text, including paragraphs, list steps, warnings, code examples and table values. The build checks a normalised text hash before and after wrapping; it also normalises heading levels/landmarks and known topic links. The original all-in-one guide remains an exact reference copy. The original source parts, native guides and PDF remain unchanged.

**Preserving wording is not the same as validating that wording as current.** For example, source topics retain local Windows wording and some old release/interface labels. The reader states this explicitly. The new source-mode notice is not a substitute for HELP-04 and HELP-05.

No automatic rewrite, deletion of old evidence, operational data mutation, permission change or reassignment is part of this checklist.

## Continue the existing development order

Keep actual hosted inventory, boxes, manifests, movement/receiving and Record management feedback first. Continue focused checklist and maintenance layouts. Carry HELP-04 through HELP-10 as explicit follow-up items, not as a completed Help library. Original Files logical folders remain pending; do not move stored original documents to achieve a cosmetic folder layout.


## UI08 progress — 25 September 2026

The original UI07 checklist above is preserved as a historical baseline. This section records the bounded UI08 increment; it does not mark the entire review complete.

| Item | UI08 update | Still required |
|---|---|---|
| HELP-04 current UI wording | Reviewed `daily` (Complete a checklist) and `records` (Manage checklist records) against the actual catalogue, stage and browser Record management controls. Old text retained in the parent and diff. | Remaining 74 registered topic articles, screenshots and finer author/reviewer interactions. |
| HELP-05 local versus hosted | Those two articles now explicitly separate browser workflows from local-vessel connectivity and legacy native deletion labels. No cloud-sync or universal offline/recovery claim. | All other local/hosted instruction paths; full native/PDF audit. |
| HELP-06 entry points | New Checklists Help and retained-record/template links point to verified routes. Help does not submit the current operational form. | Every other menu, modal, tooltip, install/contact/example page and source link. |
| HELP-09 accessibility | Local keyboard/landmark, narrow-width, section-link and print-style checks for the changed browser surfaces. | Physical device, complete screen-reader/zoom/contrast and live hosted acceptance. |
| HELP-10 regressions | New tests require exact unchanged instructional text for the other 74 topics, matching catalogue/outline content for the revised two, no desktop import in Help routes, and preserved operational actions. | Consolidated authoring/build workflow and broader CI. |

All 76 browser topics keep the UI07 reader. The other 74 instructional articles remain text-identical, aside from their shared reader's cache-reference change. Native Help, original all-in-one reference and PDF guides are untouched. UI08 source review is explicit; preserving or styling text is not the same as accepting it for current operations.
