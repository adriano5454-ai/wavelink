# UI110 — Tasks and Maintenance browsing

UI110 continues the verified GitHub UI109 release at commit `3329dddcf39bc7065d53b731ca3524f508183dcf`. Core remains **1.34.19**. The supplied UI92 compact package is valid but older; apply UI110 from UI109 or use the complete repository.

## Browse Tasks

Tasks has a compact left list and a larger right summary. Select a row to read the current authorised task, assignment, due date, instructions and saved progress. The preview does not acknowledge unread updates or save results. **Open task & saved work** opens the existing full task screen, where the established acknowledgement, work, discussion, submission and review actions remain available.

Search, task views, status, type and access scope remain available. Refresh and return from a full task preserve an eligible selection but obtain a fresh authorised detail response. A filtered-out, denied, changed-scope or mismatched record cannot keep its old preview. Late responses from another task, route or session are ignored. An open editor blocks browsing changes and retains its typed work.

On screens up to 850 pixels wide, selecting a task opens its summary and **Task list** returns to the list with the existing filters, selection and position. Desktop lists scroll independently beside the summary.

## Browse Maintenance

Selecting a work-order title now shows its existing read-only summary. **Continue work** or **Open order** still opens the exact saved work order. Compact rows leave more room for the right detail panel. On phones, **Back to work orders** restores the selected title and list position.

Work steps, evidence, assignments, frozen routine revisions, cycles, approvals and local forms retain their existing behavior. Summary browsing records no result and does not authorise equipment use.

## Apply

Use the Wavelink application repository. From the full package, copy the **contents of REPOSITORY** into the checkout root; preserve Git metadata, private settings and company data. The compact package contains only changed repository files and accepts the exact UI109 parent. Its read-only verifier checks the parent before copying and the completed target afterward.

The existing Docker build applies the new UI110 overlay after UI109. The Task script, Maintenance script and existing work-execution style bundle use UI110 cache versions. No setup change, dependency replacement, database migration, reset or browser-storage clearing is required.

## One acceptance session

Open Tasks, select two records, search for one, and confirm the right summary follows only the visible selection. Open the full task to continue work, then return. On a phone, use Task list. Open Maintenance, select a title, then use Continue work and return. Keep a genuine draft open and confirm it remains intact.

See `UI110_REVIEW_REPORT.json` for executed checks and their limits. Local browser fixtures use fictional records. They do not establish live Render behavior, actual phone hardware or service-worker upgrades.
