# UI101 — worksheet roles and native logbook designs

The supplied inventory workbook starts with a reconciliation summary. Previously this was selected as inventory data, while a broad location alias selected the original “Location cell” before “Imported location”. The actual records are on a later worksheet. The supplied native logbook has a precise saved schema but its pictures made the original file too large for browser upload.

## Workbook review

1. Choose a spreadsheet in Setup & builders → Import a document.
2. Inspect the worksheet roles and recommended data sheet. A summary or exception review is available for deliberate selection; its rows are not automatically added. Multiple real data sheets remain separately selectable, including their individual headers.
3. Inspect the chosen header and mapping. Reviewed/imported physical location takes priority over original source-location columns. Unknown location markers become Unassigned; missing quantities remain unknown. Repeated names and assets remain separate, and text such as BOX does not imply a container.
4. Inspect source Notes: selected filename/worksheet/actual Excel row and unmapped source columns. Original workbook/tab/row/date/department/verification labels describe the source only; they do not create custody, department assignment or verified Wavelink stock.
5. Apply changed mappings deliberately. Direct edits to mapped rows are retained until you choose Apply mapping again. Check the current draft, confirm the source review and create a separate inventory.

Formula cells are omitted without evaluating their expressions. Formula-only names are excluded, formula quantities stay unknown and formula locations remain Unassigned, with omissions explained. Hidden worksheets, macros, links, embedded objects and images do not execute. Source row indices preserve blank-row gaps. Generic recognition uses headers and source identities; it does not rely on the supplied filenames or merge repeated names.

The example yields three visible sheet roles: Source Reconciliation (summary, 26 formulas omitted), All Source Items (315 records, recommended), and Location Review (8 overlapping exception records, not appended). Imported location correctly retains 92 Unassigned records. All 315 source departments are Unassigned; 86 source onboard dates are evidence only. No quantity or container is invented.

## Native logbook design

Select .ajlogs from Import a document or Logbook designs → Import existing. A same-origin worker reads the native ZIP locally, checks member names/bounds/CRC/manifest hash and strict bounded JSON, and builds a deterministic native design package. Limits are 150 MB original/expanded data and 12 MB prepared upload; a 65-second worker deadline and cancellation protect the active form. Unsupported browser compression gives a clear update message; the original history-bearing file is never uploaded as a fallback.

Review the sections/fields and omitted-count summary. Name, description, IDs, types, units, required flags and choices come directly from the validated native definition. The original source filename/hash/size and omitted counts are explicitly browser-reported. The server validates only the received prepared package and binds review/save/idempotent receipts to that package and the current account. Existing measurements and offset values are saved entries, not new form defaults.

The example becomes a deterministic 11,426-byte design ZIP from a 44,943,684-byte original, retaining all 9 sections and 103 fields. Its 561 entries, 562 history records, 30 reference pages and 216 pictures are excluded. Saving creates an empty logbook design. The existing desktop reviewed full transfer remains the route for retaining saved entries, history, references and media.

## Delivery and preservation

This compact update includes prepared UI99 and UI100, accepts exact UI98/main, UI99 or UI100, and applies after the pinned UI100 runtime. Use the wrapper before/after verifier, then commit/push/redeploy normally. Core stays 1.34.19. Accounts, MFA, SMTP, password recovery, alert preferences, tab recovery, frozen records, source dependencies, schema and all 72 artwork/icon files remain intact. No reset or browser-storage clearing.

Read UI101_REVIEW_REPORT.json for executed tests and methods. Actual C01 browser tests use a fictional disposable company, actual server APIs and real IndexedDB. Local extraction uses a real static Worker under CSP. Full service-worker upgrade/WebSocket/BFCache, live Render/Nginx/SMTP and physical/native display acceptance remain pending. Unusual layouts, ambiguous headers and OCR still need review. No universal recognition claim; no source examples are bundled in the update.
