# UI116 — review source table headers

Wavelink, AJ Offshore Solutions. Core **1.34.19**. Parent: verified UI115 at GitHub main `7838e5787b81dc2fe2a024630b6f75c722b30df2`, live on Sulmara and the client demo.

Open **Review source table headers** beside the source/header browser for the worksheet you are inspecting. It lists possible inventory headers in the first 5,000 extracted rows. Candidates are paginated. Alias recognition is advice; it cannot establish a complete table or a consistent layout.

Compare each candidate against all **13 recorded last-applied mapping choices**. The comparison shows the original source column/heading and the candidate text occupying that same column. Alternative recognized columns, moved or missing headings and ambiguous repeated aliases stay explicit. Pending choices are not presented as applied mapping. If a valid applied record is unavailable, comparison remains unavailable. Full mapped-row edits may differ from the earlier applied source mapping.

**Inspect source row** opens the exact extracted row without changing the chosen header. **Inspect mapped item** is available only when that source row has a unique confirmed original Excel coordinate still associated with a nonmanual mapped item. Source inspection can remain available when an item link is unavailable. These are view actions: accepted or blocked checks, confirmation, signed receipts and unchanged retries remain intact. Busy, uncertain and unrelated-modal states lock them.

The panel does not select a header, apply mapping, combine tables, remove/exclude rows or infer table boundaries/record counts. Use the existing header chooser and Apply controls for deliberate mapping changes, then check again. Review the complete file for merged, adjacent and unrecognized tables, and for source rows beyond the browser limit.

## Install and verify

The compact update supports exact UI115 only. Run the package verifier before copying the contents of `COPY_TO_REPOSITORY` into the application checkout root, then verify afterward. The full package includes `REPOSITORY` for older or mixed checkouts. Preserve private settings, company data, Git metadata, disks and environment settings. Docker applies UI116 after UI115.

Use a disposable worksheet with repeated or reordered headers. Check and confirm first, then browse source-header candidates, compare fields and inspect source/mapped rows. The checked proposal and mapping should remain intact. Refer to `UI116_REVIEW_REPORT.json` for executed checks and limitations.
