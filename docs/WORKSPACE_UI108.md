# UI108 — review imported tables and recover Toolbox reads

Core remains 1.34.19. UI108 follows the exact delivered UI107 repository and includes its full work. GitHub main now matches all 327 delivered UI107 files at 1d71f5bbd2fa2af01a405c6bc3d8aeb8b76b0de1, with UI106 commit a7e5d4dfac358744599939b1a861309476a1ccc3 as its parent. UI108 was prepared from the verified UI107 ZIP before its commit was observed, so frozen build provenance retains the archive input and a null preparation-time parent commit; the final GitHub verification separately records the equivalent committed parent. The compact updater supports either exact delivered UI106 or UI107 repository.

## Review document tables

Open **Setup & builders → Import a document** and read the source. Clear label/value tables and labelled rows can retain descriptions, instructions, tools, supervisor guidance and declaration wording. Changed printed headers define the following table segment, including before/after fields and readings. Exact short stage headings organize subsequent checks. Source review points identify uncertain or unsupported interpretation where the extractor provides evidence.

Compare **Review source interpretation** and the editable proposal with the actual document. Printed answer definitions can create empty fields; completed answers, names and signatures do not become new responses. Recognition does not establish procedural correctness. Correct unclear layouts manually. For a toolbox talk, deliberately copy retained instructions and tools into discussion prompts when needed; the native Toolbox schema remains unchanged.

## Review inventory source rows

Review each selected worksheet and mapping. **Choose items → Needs source review** shows conservative advice for rows resembling repeated headers, titles, summaries, instructions or footers. Every mapped row remains included until you explicitly exclude it. Advice refers to the original extracted source, rather than proving that an item is invalid. Real items can be named Total or Instructions, and name-only items can have an Unknown expected quantity.

Search and page through the rows, compare the source and use the existing Include/exclude actions. Searching, filtering and paging leave approval intact. Changing inclusion requires checking again. Source Counted columns remain Notes: the app records verification during the stock check. SN and PN aliases, leading zeros, zero expected quantities, worksheet locations, full Notes and separate repeated identifiers remain supported.

## Find the actual worksheet header

Automatic header discovery and the normal selector inspect the first 250 extracted nonempty rows. Open **Find header row** to search and page through any extracted row within existing extraction limits. Compare the preview and select deliberately. Proven Excel coordinates appear when available; other labels honestly describe extracted positions.

Review notices about nonempty rows before the selected header and alternative header candidates. A later stronger header can exclude earlier source rows from mapping. Choose an earlier header when it describes the intended table, or correct the source/manual proposal for multiple different layouts. Changing the header invalidates approval and requires **Apply mapping**. The importer does not silently combine different column layouts into one mapping.

Editing the complete raw table clears provenance, selection and advice when those facts cannot be established. Field-only relationship edits retain source references and original-source advice, which may no longer describe the corrected row. Reapplying mapping replaces mapped corrections. Pending or uncertain saves retain their original retry request.

## Keep boxes, locations and existing verification

**Boxes and contents** retains UI107's editor. Parents are exact unique included explicitly marked boxes in the same incoming worksheet. There is no inferred hierarchy from appearance, SN/PN or item names, and no import link to a box on another sheet or already in the destination. Contained items use the root box's effective location; differing reviewed mapped locations remain in Notes. Unknown-or-one box quantity, ordinary zero quantity and the native eight-ancestor limit remain.

Combine selected sheets into one inventory using separate worksheet locations, or append new rows to a permitted existing inventory. Existing stock, checks, task scopes and custody stay intact. Check the corrected proposal and summary before saving. Original source files remain read-only and are not included in release archives.

## Recover Toolbox Talks loading

If opening another form interrupts the first Toolbox Talks read, the selected Toolbox page shows a recoverable waiting/retry state. Finish and close the form, then retry. The retry reads the current workspace without discarding unsent work or accepting late data from a previous route. Existing request ownership, permissions and form guards remain in effect.

## Apply and verify

Extract the full ZIP and copy the contents of **REPOSITORY** into the checkout root. Preserve Git metadata, private settings and company data. Run the outer read-only verifier. The compact updater first verifies either exact supported parent, copies the cumulative update, then verifies the complete UI108 target. All five vendor parts and ordered overlays are present.

Read **UI108_REVIEW_REPORT.json** for executed checks and limitations. Local tests cover disposable fictional C01 APIs and browser state. They do not establish live Render/SMTP, physical camera, Windows display, actual service-worker upgrade, WebSocket transport or browser back/forward-cache acceptance. No migration, data reset or dependency change is needed.
