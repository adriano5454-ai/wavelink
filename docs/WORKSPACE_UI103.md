# UI103 — combined inventory imports and part numbers

Core version remains 1.34.19. This release builds on exact UI102 and includes the previous account, email, recovery, import and interface changes.

## Import several worksheets into one inventory

Open **Setup & builders → Import a document**, choose the workbook, and keep **Import as → Inventory**. The item worksheets are selected together. Summary, review, logbook and checklist worksheets remain unselected unless explicitly chosen. Review the selected sheets, each sheet's column mapping, and the editable **Location for these items**. The selected sheets save together in one inventory.

Each nonempty reviewed sheet location applies to all its imported items. Original mapped physical locations remain in Notes. Clear that sheet's location to use source locations where present, with the sheet name as the fallback for blanks. The built-in Unassigned and In use choices remain available; the four occupied locations in the example do not imply only four configured location choices.

Switching the mapping sheet preserves the other sheets' edited rows, mappings and selection. A different location, mapping, selection, row edit or destination invalidates the review and confirmation. Check the edited draft again before saving. Formula-only names and non-item headings are excluded with located warnings; ambiguous quantities remain Unknown. Unmapped source fields are retained as evidence, not silently discarded or interpreted as completed work.

For the supplied MR07 shipping workbook, the default proposal contains **220 records**, with 56 / 58 / 4 / 102 in Vehicle MR 07 / Pallet 1 / Pallet 2 / Pallet 3,4. The commercial invoice cover remains unselected because it repeats shipping content. All 220 PN and 66 SN values survive exactly, including leading-zero strings. The VEHICLE-only row is a heading, not an omitted item. Eleven expected quantities remain Unknown: ten blank cells and one literal X. The old Excel Counted column stays source evidence; Wavelink records the actual verification count separately. Source indentation does not invent boxes or assembled kits.

## Add items to an existing inventory

Choose **Destination → Add to an existing inventory**, or open a saved inventory and use **Import items**. The latter preselects that inventory for document review. New items receive new identities, and reviewed locations are added as needed. Existing items, quantities, verification results, private task scopes, Fleet custody, custom field definitions and category assignments stay in place. An existing open verification keeps its fixed original scope; imported items can be checked in a new verification.

If the destination changes after review, saving stops before any additions. **Refresh inventories** explicitly refreshes its version while keeping edited rows and locations, then requires a fresh review. A repeated or overlapping source import stops the whole batch; it does not silently merge objects by name, serial or PN. When original row evidence is unavailable for a worksheet already imported, the importer stops because it cannot establish which rows are distinct. An uncertain save retries the identical operation, so the receipt cannot create another copy.

Adding document items requires a current named account with inventory view, inventory edit and inventory builder permissions. Administrator status is not required. Native .ajinventory packages retain their existing separate-inventory import flow; document additions support the reviewed Excel/CSV/PDF/DOCX and other document path.

## Serial and part numbers

**Serial number (SN)** and **Part number (PN)** are separate native fields. Recognized headers include SN, S/N, S.N., Serial Number, Serial No., Serial Nr., S No.; PN, P/N, P.N., Partnumber, Part Number, Part No., Part Nr., P No., Manufacturer Part Number and MPN, plus supported Portuguese spellings. Related prose such as Paired SN or Previous Part Number does not steal those mappings. PN is not mapped to the asset/tag field.

Part number is editable and visible in inventory identities, item details, asset/Fleet views, verification and assigned tasks. It is included in native inventory packages, CSV and relevant PDF reports. Existing records without the field display it blank without a migration or read-time rewrite. Punctuated and compact identity searches both work: a full PN must match as one identifier rather than fragments assembled from unrelated Notes or dates. Repeated PN/SN values still represent separate records.

## Apply and review

The full ZIP contains the complete GitHub deployment repository. Copy the contents of its REPOSITORY folder into the checkout root, including the two ignore files. Dockerfile belongs at the root. Back up mixed-up local folders first, preserve .git, private settings and local project data, and follow README_FIRST.md. The optional compact ZIP supports exact UI98, UI99, UI100, UI101 and UI102 baselines with before/after checks. The Docker build applies the exact UI103 overlay after UI102.

No SQL migration, reset, browser-storage clearing, credential changes, mail setting changes or source dependency changes are required. All 72 artwork files are unchanged. Tests use disposable fictional companies; the supplied workbooks are read-only acceptance sources and are excluded from repository ZIPs.

Read UI103_REVIEW_REPORT.json for executed checks and limitations. Physical QR/camera, Windows native display, live mail/Render deployment, actual service-worker upgrade/WebSocket/BFCache acceptance are not claimed. Document proposals still require review.
