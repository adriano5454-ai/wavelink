# UI111 — protect inventory corrections and keep worksheet review

Core **1.34.19**. Built from the exact verified GitHub UI110 commit `61a18def0e11f4663fb1e23321ed6d6ceecea657`. All UI110 Tasks/Maintenance and earlier import work remains included.

## Inspect worksheets without repeating a check

After **Check edited draft**, use **Review mapping for sheet** to inspect another worksheet. The import overview and your confirmation remain available. The worksheet selector changes the display; the checkboxes decide which worksheets are imported. Save retains the exact previously checked proposal, including all selected worksheets and their locations.

Blocked source-conflict overviews also remain visible during inspection. Their confirmation and Save stay disabled. Correct the source choices or destination and check again. Editing item fields, quantities, box relationships, included rows/sheets, locations or the destination still clears the completed check. Changing the file or import type also requires a fresh check. Busy or uncertain saves remain locked.

## Review before replacing corrections

**Apply mapping** now warns before replacing deliberate corrections in that worksheet. The warning names the worksheet and the affected correction groups. **Cancel** keeps your corrected rows, current mapping proposal, source references, choices and any retained check/request. Confirming reapplies source-mapped values to that worksheet and requires another check. Other worksheets keep their corrections.

Original row choices are carried forward only where their source rows can be confirmed. Full mapped-row editing can lose source-row proof under the existing workflow; the warning does not invent missing provenance. Source Notes, SN/PN and expected quantities retain their established rules. Importing does not create verified stock counts.

## Save and retry

Worksheet inspection retains the exact signed proposal. Real edits cannot use the old approval. If a response is lost after saving, **Retry unchanged request** keeps its original operation ID and payload; it does not add the same items again. Resolve the uncertain result before changing the proposal.

## Apply and check once

From the full package, copy the **contents of REPOSITORY** into the application repository root, preserving Git metadata, private settings and company data. The compact update supports the exact verified UI110 parent only. All source parts and overlays are included in the full repository. Docker applies UI111 after UI110. No schema, dependency, account, mail or data-reset change is required. Do not clear browser storage.

Use a representative import: correct one item, choose Apply mapping and Cancel, then Check edited draft and confirm. Browse another worksheet and confirm the overview remains. Save the reviewed new inventory or append. Use a disposable test for deliberate remapping and retries; keep real work intact.

Read UI111_REVIEW_REPORT.json for executed checks and limitations. Browser acceptance uses generated fictional workbooks and temporary company databases. It does not establish production deployment, physical-device or service-worker-upgrade behavior.
