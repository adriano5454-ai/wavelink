# UI113 — undo pending mapping choices

Core **1.34.19**. Built from the exact verified GitHub UI112 commit `3e3fc54d6a3bf16d085d8e97fad5d34da6799a96`. All UI112 navigation, UI111 import safeguards and earlier workflows remain included.

## Restore mapping choices while keeping corrected items

After changing a worksheet's header or source columns, use **Restore last applied mapping** to discard those pending choices. The action restores the recorded header and all 13 column choices for the worksheet you are inspecting. It keeps current item corrections, full Notes, quantities, row exclusions, source references, manual-row status, box relationships, locations and destination intact. It does not regenerate rows from the source or ask for routine confirmation.

Restoration clears the previous check, confirmation and import overview. Use **Check edited draft** again, then confirm before saving. An excluded worksheet remains separate from the worksheets selected for import. Pending mappings on included worksheets must be applied or restored before a new check can succeed; an excluded worksheet does not need a mapping to check the selected proposal.

## See what is pending

The pending mapping details show changed destination fields and header choices against the recorded applied mapping. Numbered column labels distinguish repeated headings. Current rows continue to show the last applied values and any subsequent corrections while choices are pending.

**Apply mapping to rows** retains its established behavior: it replaces values using the selected source columns and asks before replacing deliberate corrections. Cancel keeps the current rows and the previous recorded mapping. Only a successful Apply records the new mapping for later restoration. Failed or cancelled applies do not replace that record.

## Honest availability and locked requests

The record is created when a worksheet is first mapped in this workflow and after successful Apply. It is tied to the current source and worksheet. Older draft states without that record show restoration as unavailable; prior mappings are never inferred from corrected rows. State-clone tests exercise editor metadata preservation, without claiming browser-reload draft recovery.

Busy or uncertain requests lock restoration and mapping. **Retry unchanged request** retains its original operation ID and payload. Resolve an uncertain save before editing. Controls captured from another source, worksheet, import type, repaint or session cannot restore the current proposal. Existing source evidence in Notes is preserved.

## Apply and check once

Copy the **contents of REPOSITORY** from the full package into the Wavelink application repository root, preserving Git metadata, private settings and company data. The compact update supports only the exact verified UI112 parent. Docker applies UI113 after UI112. No reset, re-import, schema/dependency change or browser-storage clearing is required.

Use a representative import: correct one item, exclude another, then change a source column or header. Review the pending details and restore the previous mapping. Check that corrections and exclusions remain, then check and confirm again. On disposable data, test a successful Apply followed by another pending change and restoration. Preserve genuine unsent work.

Read `UI113_REVIEW_REPORT.json` for executed checks and limits. Browser acceptance uses fictional workbooks and temporary C01 databases. Physical devices, live email, service-worker upgrades and production synchronization require their own acceptance.

GitHub rejected branch creation with 403. This release was not pushed or deployed; the packages provide the complete prepared source.
