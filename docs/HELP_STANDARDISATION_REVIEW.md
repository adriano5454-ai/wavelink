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


## UI09 progress — 25 September 2026

The UI07 checklist and UI08 updates above are retained as history. This increment does not mark all Help reviewed.

| Item | UI09 change | Still required |
|---|---|---|
| HELP-04 | Rechecked `daily` against the actual opened-stage controls: Checks, Team & stage review, Instructions & source, scoped For later, saved/local counts, Record tools and readiness. `records` retains its UI08 review. | Remaining 74 topic articles and detailed editor/evidence/reviewer wording; continue reviewing the two revised topics as controls evolve. |
| HELP-05 | Daily guidance keeps hosted internet/local-vessel distinctions and does not present local drafts as server saves. | Other local/hosted instruction paths, server operation, imports and recovery. |
| HELP-06 | Stage Help/Record tools routes use the existing browser Help reader. The inline For later hint now describes the real filtered behavior. | All other menu/dialog/special-page links and return contexts. |
| HELP-09 | Actual shipped layout checked at 390px/320px, escaped content and scoped dialog/keyboard controls. | Real phones, durable storage, full assistive-technology and live acceptance. |
| HELP-10 | Tests require unchanged source text for the other 75 articles, matching daily catalogue/outline, and unchanged business functions. | Shared authoring/CI and native/PDF consistency. |

Only the daily article's instructional wording changes. The other 75 article bodies remain exact, including the UI08 records article; cache references advance for the updated catalogue. No native guide, all-in-one reference or master PDF is rebuilt.


## UI10 progress — 25 September 2026

The earlier checklist and increments remain historical records, not implied whole-library completion.

| Item | UI10 change | Still required |
|---|---|---|
| HELP-04 | Reviewed `maintenance` against actual catalogue/filter/detail/step/review/cycle controls; current labels and action effects verified. | Remaining73 unreviewed article bodies, finer evidence/approval/editor paths and continuing review as the three revised articles evolve. |
| HELP-05 | Maintenance article distinguishes browser Templates & routines and hosted saves from native Projects export and unapproved overlay recovery. | Remaining hosted/local instruction paths, operator procedures and actual accepted recovery. |
| HELP-06 | Maintenance Help and template shortcuts use existing routes without submitting an operational form. | All remaining menu/dialog/install/contact/example links and cross-workspace return contexts. |
| HELP-09 | Local Maintenance Help rendering, narrow layout, current-topic/outline/search and print checks; no Tk dependency in all76 browser topic routes. | Real devices, complete accessibility and durable-storage acceptance. |
| HELP-10 | Tests preserve the other75 article bodies and native/PDF output, match catalogue text and assert unchanged business services/action editors. | Shared authoring pipeline/CI and full native/PDF consistency. |

Only the Maintenance article's instructional text changes in UI10. The daily and records reviews from prior increments remain, giving three distinct bounded article reviews. Detailed recurring-maintenance guidance is retained. No master PDF or native guide is regenerated; reference files remain original. Original Files logical folders remain pending, not implemented by a Help restyle.


## UI11 progress — 25 September 2026

The historical checklist and UI07–UI10 findings above are preserved. UI11 rechecks the Maintenance article again; it does not count as another distinct completed topic.

| Item | UI11 change | Still required |
|---|---|---|
| HELP-04 | Maintenance article now describes the four-page catalogue creation form and three-page step form, actual labels, original limits, photo requirements and Saved/Proposed review. | Remaining73 unreviewed article bodies, finer approval/cycle/close paths, continuous review of the three revised topics. |
| HELP-05 | Keeps server-saved versus local-draft distinction and the separate exact-asset linked-creation route; hosted/local export/recovery caveats retained. | Other hosted/local instruction paths and accepted operator recovery. |
| HELP-06 | Existing Maintenance Help opens the reviewed article; guide controls do not submit on intermediate pages. | Every other menu/dialog/special-page entry point. |
| HELP-09 | Local article/current-topic/full-text/print checks and new form viewports320–1512; original proof rules retained. | Physical devices, real storage, full keyboard/screen-reader/contrast/zoom acceptance. |
| HELP-10 | Tests require75 untouched article bodies, matching maintenance outline/catalogue and identical original create/step API payloads. | Consolidated authoring/CI/native/PDF pipeline. |

All76 registered topics retain the shared reader. Only Maintenance instructional text changed; native Help, all-in-one reference and master PDF remain unchanged. Three distinct bounded reviewed topics remain daily, records and maintenance. Source preservation is not proof that all instructions are current for hosted operations. Original Files folder organisation is still pending.


## UI12 progress — 25 September 2026

Prior checkpoint sections remain historical. `maintenance` now documents Saved work & note / Confirm completion or cancellation, saved/proposed cycle reviews, and stopping a blocked pending follow-up. UI12 keeps the original named fields, actions and service meanings. Home refinement is separately pending in the active development list, not a Help-review completion.

| Work item | UI12 progress | Remaining work |
|---|---|---|
| HELP-04 current controls | Updated Maintenance with closing/cycle/stop form navigation and their exact effects. | Remaining 73 unreviewed articles plus finer existing topics, screenshots and control alignment. |
| HELP-05 hosted/local distinction | Retained local-draft versus server-save distinction and no hosted recovery approval. | Full hosted/local wording and native/PDF review. |
| HELP-06 entry points | Existing Maintenance Help route and shared outline/catalogue stay aligned. | Every other inline/special/modal entry point. |
| HELP-09 accessibility | Narrow widths, text-only rendering, active topic, print styles and focus checks on changed browser surfaces. | Physical devices and complete keyboard/screen-reader/contrast/zoom acceptance. |
| HELP-10 regression protection | All76 routes checked with Tk imports blocked;75 other instructional bodies remain text-identical. | Consolidated authoring/build/CI and all-format parity. |

There remain **three distinct bounded wording-reviewed articles** (daily, records, maintenance). Updating maintenance again does not add a fourth. Native Help, reference HTML and master PDF remain unchanged. Original Files folder organisation remains pending.


## UI13 progress — 25 September 2026

Earlier sections remain historical. `dashboard` (Use Home) now describes equipment navigation, Continue/Start, local/server drafts, per-category scope and failure states, capability limits and hosted/local operation. Outline and search catalogue match the article. Other75 article bodies remain unchanged, including daily,records,maintenance. Native/master PDF/reference HTML are unchanged.

There are now **four distinct bounded wording-reviewed articles**, leaving72 without that current wording review. HELP-04 and HELP-05 advance for Home only. HELP-06 covers its verified existing Help route and no form submission. HELP-09 has local five-width, focus/landmark/error tests; physical devices and complete accessibility remain pending. HELP-10 checks75 preserved bodies and all76 routes with Tk blocked; consolidated authoring/all-format CI remains pending. The entire Help library is not marked complete.
