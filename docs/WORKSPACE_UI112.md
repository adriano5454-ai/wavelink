# UI112 — move through inventory review

Core **1.34.19**. Built from the exact verified GitHub UI111 commit `cd10b38dcea4e3bca79cd1ac284ce6eb98e4c5ce`. All UI111 safeguards and earlier workflows are included.

## Worksheet inspection and import choices

**Inspect worksheet** changes the displayed worksheet. The adjacent context names it and shows **Included in import** or **Excluded from import**. The checkboxes under **Worksheets to import** decide what will be imported. Each worksheet card also has **Inspect mapping and items**. Inspecting a worksheet preserves those checkboxes, corrected rows, locations, completed check and confirmation.

## Direct navigation

Use **Worksheets**, **Mapping**, **Items**, **Boxes**, **Source** and **Import overview** to move to the corresponding section. Items, Boxes and Source open their panel when needed. The destination receives keyboard focus and scrolls below the fixed header, including narrow screens. These shortcuts inspect the current proposal without collecting a new draft or making an API request. The overview shortcut becomes available after either an accepted check or a blocked conflict check.

Busy or uncertain saves disable inspection and shortcuts. Resolve an uncertain result through **Retry unchanged request**, which retains its original request ID and payload. Old controls cannot operate a replaced source, worksheet, import type or departed session.

## Make mapping choices explicit

Each source option is labelled **Column N · heading**, so repeated or blank headings remain distinguishable. Name is required; trying to apply without it focuses the Name selector. Shared source-column advice names the fields that reuse a column. Reuse remains allowed without automatic remapping.

Changing column choices shows a pending notice. Item rows continue to show the last applied mapping and retain existing corrections until remapping is confirmed. Changed mappings on included worksheets must be applied before a new check can succeed; Save requires a fresh accepted check. Excluded worksheets need not be mapped to check the selected proposal. **Apply mapping** keeps UI111's worksheet-specific confirmation before replacing deliberate corrections. Cancel retains the mapping choices and current corrected rows. Confirming remaps that worksheet requires a fresh check. Other worksheets keep their corrections.

All 13 mapping fields, full source/TSV editing, Notes, SN/PN, expected quantities, row exclusions and explicit box relationships retain their existing behavior. Unknown and zero quantities remain distinct. Importing does not create verified stock counts. A restore-last-applied-mapping action is deferred.

## Apply and check once

From the full package, copy the **contents of REPOSITORY** into the Wavelink application repository root, preserving Git metadata, private settings and company data. The compact update supports only the exact verified UI111 parent. All source parts and overlays are included in the full repository. Docker applies UI112 after UI111.

Use a representative import: inspect an excluded worksheet, navigate to Items and Source, check and confirm, then browse included worksheets and the import overview. The proposal and confirmation should remain. Change a mapping choice and cancel remapping of a corrected row. Material edits require another check. Blocked conflicts keep Save disabled. Preserve genuine unsent work; use disposable data for deliberate remapping and retries.

No reset, re-import, schema/dependency change, account/mail setup or browser-storage clearing is required. GitHub write access rejected branch creation with 403, so this release was not pushed or deployed. Read `UI112_REVIEW_REPORT.json` for executed checks and limits. Browser acceptance uses fictional workbooks and temporary C01 databases; production, physical devices, live mail and service-worker upgrades require their own acceptance.
