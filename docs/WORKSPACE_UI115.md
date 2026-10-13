# UI115 — review possible overlap between inventory worksheets

Wavelink, AJ Offshore Solutions. Core **1.34.19**. Parent: verified UI114 at GitHub commit `b444631404fe9c358cec74f2947252896c8a8b63`.

Open **Review possible overlap** under the worksheets to import. It compares included rows in different included worksheets by exact serial number (SN) or asset reference, ignoring only surrounding whitespace. Case and leading zeros remain significant. Each identifier group shows item names, locations, part numbers and available source references.

These groups are suggestions for your review. A shared identifier may describe the same item or separate records. Names and part numbers alone do not identify overlap. Excluded sheets and rows are outside the comparison; rows without either identifier cannot be compared. No exact matches does not prove the workbook has no overlap.

Use **Inspect items** to open the mapped row, or **Inspect source row** to open its unique original Excel row. Manual mapped-row edits, missing or ambiguous references, and source rows beyond the existing 5,000-row browser limit keep source inspection unavailable. Compare those rows with the original file. Pending mapping choices are labelled explicitly; the panel compares the currently applied rows.

Groups and their rows are paginated. Inspecting rows or changing overlap pages preserves the completed check, confirmation and unchanged retry request. Editing identifiers, inclusion or mapping still requires a fresh **Check edited draft**. Busy or uncertain saves lock these controls.

## Install and exercise

The compact update supports only exact UI114. Run the included verifier in `before` mode, copy the **contents** of `COPY_TO_REPOSITORY` into the application repository root, then run it in `after` mode. Use the full repository package for mixed or older source folders. Preserve Git metadata, company data and private settings. Docker applies UI115 after UI114.

On a disposable workbook, include two worksheets containing an explicit shared SN or asset reference. Check and confirm the proposal, open the overlap groups, inspect items and source rows, and confirm the checked proposal remains available. Review different locations carefully. A PN shared by separate units should not create an overlap group by itself.

See `UI115_REVIEW_REPORT.json` for executed checks and their limits. Production mail, physical devices, service-worker upgrades and live synchronization require actual-environment acceptance. UI115 deployment status is recorded separately from local tests.
