# Wavelink — Workspace UI 10

**Core 1.34.19 · cumulative UI01–UI10 · prepared 25 September 2026.** Local implementation and targeted tests. Not deployed to the user's GitHub repository or Render; the live repository was not fetched.

## Scope and the working domain

This increment organises the browser **Maintenance catalogue and opened work order**. It retains Inventory/boxes/categories, Asset details, Record management, receiving, manifests, standalone Checklists and the Help reader from UI01–UI09. It is not a native Windows Admin update.

The user confirmed `https://demo.mywavelink.com` and the normal/guest entry are working. **Keep the existing live PUBLIC_URL, passwords, guest settings and disk unchanged.** This update does not contain DNS changes or require another hostname. It does not recreate accounts or sign anyone into a different project.

Source: the supplied complete UI09 ZIP. Its **1,650 package-manifest entries** were verified before editing. The original 1.34.19 five source parts remain pinned and unchanged. Against that supplied upload repository, **only `deploy/extract_source.py` changes among existing executable code files**; it applies the cumulative, hash-checked overlay during Docker build. Login, gateway, supervisor, Dockerfile, dependencies, vendor seed and recovery helper remain byte-identical to the supplied UI09 package. Review outside repository edits before overwriting files.

## Find maintenance work before opening its editor

Open **Maintenance** in the main sidebar. **New work order** is available when the account has Maintenance manage permission. **Refresh**, **Saved forms** and **Help** remain directly available.

**Search work orders** matches reference, equipment, title, instructions, cycle wording and named assignee. **Open work** is the default. Other views are **Overdue**, **Due within 7 days**, **Follow-up review**, **Completed**, **Cancelled** and **All orders**. A phone uses the equivalent **Show orders** selector instead of duplicating all status buttons.

Due views use the recorded due timestamp and this browser's current time. Dates are labelled UTC. Overdue means an open order whose date has passed; Due within 7 days includes the next seven elapsed days and excludes already-overdue work. Missing or invalid dates do not become imaginary due dates. These views change neither the order nor its schedule. Follow-up review shows a saved blocked successor decision, including when the original work order is already completed; it is separate from open overdue work.

**Routine, people & sort** expands the available-routine, assignment and sort controls. **Assigned to me** selects explicit named assignments, not everything a manager may work on. **No named assignees** shows team work accessible to permitted maintenance workers. Sort by earliest due date, recent update or reference; absent due dates appear last. Counts on status controls cover accessible saved orders before the search and other filters. The matching count includes the selected filters.

A routine is the reusable procedure; a work order retains one reviewed revision and saved results. The administrator's template shortcut lives under **Routines, permissions & work rules** and opens the existing **Administration → Templates & routines** workspace. This is not a new template builder.

## Read-only summary beside the list

Click the work-order title or **View summary**. On desktop, the summary is beside the list; on a phone it replaces the list. It shows the equipment, reference, due date, saved progress, assigned people and the relevant next step. **Open work order** retrieves the current order and opens the working view.

Selecting a summary does not record a reading, approve, complete, cancel, create a successor or change custody. Catalogue progress combines saved Complete/N/A counts; the opened order shows those two outcomes separately. Counts are not an approval or return-to-service decision.

Mobile **Back to work orders** returns to the saved list context. Returning from an order opened through the catalogue uses **Back to maintenance search**, **Back to filtered work orders** or **Back to work orders**, retaining the same-session search, filters and selection. Direct external entry uses **All work orders**. Internal list scroll is retained; mobile detail returns to its captured page position. This is not a universal cross-module history.

Filtering the selection out of sight clears it with a notice. A failed refreshed read removes the old private detail before Retry. An older delayed read cannot replace a newer route. Session changes clear the catalogue/working view's private state and reset its choices. These preferences are memory-only, not another permanent browser store.

## An opened order has four focused sections

| Section | Contents |
|---|---|
| **Work steps** | Existing result cards and recording/approval/evidence controls, with saved-step search and filters. |
| **Review & cycle** | Whole-order outstanding counts, existing completion/cancellation controls and existing cycle settings/follow-up review. |
| **Instructions** | The frozen procedure, introduction, references, assigned people and work instructions. |
| **Linked tasks** | Existing linked Tasks the current account is separately allowed to access. |

**Order tools** groups History, Export report and Help. Reading source instructions remains necessary even when the initial section is Work steps. Reference pictures do not count as required completion photographs.

Use **Search steps**, **Section** and **Show** to find All steps, Needs attention, Item approvals or Recorded. Search includes step number/wording, section/phase label, saved notes and recorded values. A section without a title is labelled Unsectioned. The routine's step order is preserved. Complete/N/A results can still require approval.

**Find next unfinished** clears narrow choices, opens Needs attention across the order and focuses the first matching saved step. It never fills a result or opens a submitting form. A zero attention count does not validate required readings, photographs or eligibility to close. Hidden steps still count toward completion.

## Save evidence and complete deliberately

The existing reading/photo/approval/cycle/completion editors are not redesigned internally. Their validation, saved revisions, operation IDs, retries and API payloads are unchanged. Existing result data is not copied into a new order or manufactured by browsing.

**Saved forms** and the maintenance-specific local-form banner expose the existing account-scoped fieldwork drafts. Local wording and uncertain saves are not added to the saved result count. Keep and resume use the established store. An open operational form blocks the new navigation/refresh controls from replacing its target. No new background queue, browser database or automatic submission is introduced.

Maintenance view remains project-wide for accounts granted that permission. Assignment limits who may perform work; it is not a private Task. Maintenance managers can record work under the existing rules, but are not automatically assigned item approvers. A required reviewer can approve their own saved check under the existing labelled policy; this release does not impose independent review.

Completion requires the existing service's step, reading, evidence, approval and version checks. Cancellation retains unfinished results. Completed/cancelled work stays locked. Existing cycles create a next order only through their approved completion/review path; passing a date or filtering a list never generates one. Linked in-transit assets retain the existing service restrictions. Completing maintenance does not verify inventory, release quarantine, change custody or authorise operation. Completing a linked Task is separate.

## Related Help review

**Record maintenance work** (`maintenance`) now reflects the catalogue, four sections, local versus saved results, review controls and actual browser template route. It separates native **Projects → Export** wording from hosted operation and corrects the browser asset path to **Asset details → Maintenance → New linked maintenance**.

Detailed existing recurrence guidance remains. The other **75 registered article bodies keep their instructional text**, including the earlier daily/records reviews. Shared Help cache links advance; native Help, original all-in-one reference and master PDF remain unchanged. Three distinct articles have now had bounded browser wording reviews (`daily`, `records`, `maintenance`), not the entire Help library. Further detailed-form, entry-point, hosted/local and native/PDF reviews remain explicit tasks.

## Install the complete ZIP through GitHub Desktop

1. Preserve unfinished Wavelink work in every browser and separate log window. Retain the previous approved commit and an appropriate project backup. Preserve local uncommitted edits and fetch/pull the intended branch in the existing **wavelink** checkout. Deploy outside a client presentation.
2. Extract the ZIP. Copy the **contents of `UPLOAD_TO_GITHUB`** into the repository root, preserving folders. Do not copy the enclosing folder, remove `.git`, or upload `REFERENCE_ONLY`, `PREVIEWS` or `VALIDATION` as application source.
3. Review the diff, commit and **Push origin**. Relative to the supplied UI09 package, the only changed existing executable code file is **`deploy/extract_source.py`**. Reconcile any other live or local edits before replacing them. Documentation/checksums also update.
4. Deploy that approved commit through the existing Wavelink service. Keep disk, URL, passwords and guest settings unchanged. Keep **`PUBLIC_URL=https://demo.mywavelink.com`**, **`INITIALISE_FICTIONAL_DEMO=NO`**, and the initial-admin bootstrap setting removed.
5. Expected build output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 10: maintenance catalogue and focused work orders; includes UI01-UI09; no automatic data changes.
```

After a healthy deployment, open Maintenance and look for **UI 10**. Core Wavelink remains **1.34.19**, and other workspaces retain their earlier UI badges. Preserve unsent work before reloading/closing older tabs for the service-worker update. **Do not clear browser storage.**

No inventory upload, category reset, new project, database migration or demonstration re-import is needed. Existing saved category assignments, users, equipment, manifests and uploaded documents remain on the persistent disk. Unapplied category proposals still use the administrator's explicit preview-and-apply workflow.

## Hosted acceptance and recovery boundary

Use fictional data. Confirm the existing normal sign-in and guest link still work. Check due filters, summary selection and contextual Back, open a saved order, inspect the four sections, save one harmless test reading and verify saved/local distinction. Use a view-only account and a completed order. Confirm Inventory, categories, Record management, manifest/receiving and Checklists still behave as expected. Test a phone and deliberate restart persistence outside the presentation.

**Do not bypass the pristine-source recovery helper's checks to use it on an overlaid runtime.** Overlay-compatible off-host recovery remains an operator acceptance item, not something implemented or proved by this interface release.

Rollback is the extractor commit revert; an exact UI09 extractor is included at **`REFERENCE_ONLY/Workspace_UI10/rollback/deploy/extract_source.py`**. Do not reset the project, clear the disk or enable first-deploy initialization for an interface rollback.

## Validation and continuation

Exact local results and initial findings are in `DELIVERY_CHECKS.json` and `VALIDATION/`. Browser tests use actual shipped scripts and temporary fictional Wavelink services, with controlled transport and injected in-memory persistence. Previews are actual local rendering, not the live custom-domain service or native Windows UI.

The full application suite, Docker build, live GitHub/Render, physical phones/Windows display acceptance, durable browser storage, off-host restore and full accessibility are not claimed. No new hosted security approval, production multi-company isolation or vessel/cloud synchronisation is implied.

Next: remaining detailed working forms and actual hosted feedback, with inventory/box/manifest/receiving problems taking priority. Continue the Help review and professional consistency across existing modules. Original Files logical folders remain separate pending work; no original documents are moved. The development order is not an automatically running background task.


## Final local validation results

**639 distinct targeted Python cases and 127 compound browser checks passed**, with no unresolved failed/errored/skipped cases after the documented test-runner corrections. All **40 JavaScript files** passed syntax checks. The source remained frozen throughout the final runtime tests.

The selected inherited run initially hit an obsolete 36-file JavaScript expectation and two missing-display setup errors. The old script-count failure was reproduced on unchanged UI09; the adapter advances that expectation to 40 and executes the same scenarios under Xvfb. A relative helper file needed by the copied adapter was then supplied unchanged, and that complete helper suite passed on repeat. Original failures, adapters and reruns are retained; results are reconciled, not presented as an all-clean first run. No runtime code changed for these test corrections.

The entire 76-topic Help route set also returned successfully with Tk imports blocked and no operational DB content changes. Fresh final-ZIP verification is recorded separately; repeats are not additional distinct coverage.
