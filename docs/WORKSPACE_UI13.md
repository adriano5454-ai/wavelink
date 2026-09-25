# Wavelink — Workspace UI 13

**Core 1.34.19 · cumulative UI01–UI13 · prepared 25 September 2026.** Local implementation and targeted checks only. The current live GitHub repository was not fetched and this package was not deployed to Render.

## Home now separates finding, continuing and creating

Open **Home** in the existing main sidebar. The current project and signed-in person are shown in a compact heading. **Saved local work** and **Home help** remain directly available. This is a browser update for desktop and phones; native Windows Home is unchanged.

**Equipment & shipments** puts **Inventory & boxes** near the top when the account has inventory access. Project administrators also get **Manifests & shipments** and **Receiving & placement**, using the existing authorised Fleet workspace. Project-mode users do not gain Fleet authority merely because they can see inventory. Vessel-only accounts retain their separate entry. These links do not create records, move stock or acknowledge receipt.

**Continue work** lists permitted Tasks, Standalone checklists, Logs, Handovers and Maintenance. Each link opens the existing workspace so the user can select the actual record. It is not a fabricated “most recent” record or a claim that every accessible record is personally assigned.

**Start something new** is a separate panel. On an initial wide view it is expanded; on an initial phone view it is collapsed. Resizing the same view may retain its current open/closed choice. The controls use existing forms and existing permissions:

- **New checklist / dive** opens the existing new-record form. An existing retained new-checklist draft changes the label to **Continue new checklist**.
- **New task** opens the existing work-type chooser, with its administrator/department-head authority checked by the server. Confirming creation opens the saved Task using its existing detail and alert-acknowledgement behaviour.
- **New work order** opens the existing UI11 form after reading the current Maintenance directory. No routine is automatically selected. A confirmed create saves one open order with empty results, then refreshes Home. The order is available in Maintenance. Exact-asset linking remains in Asset details.

Opening a form does not create the record. Review and save remain explicit, using the existing payloads, operation IDs, confirmations, local drafts and validation. A short explanation distinguishes a Task-owned checklist from a standalone checklist. The start actions are disabled during their preparation to prevent competing form opens. Late preparation responses are discarded if the account, route or Home view changed.

## Saved work overview: read each scope separately

The existing attention endpoint remains the sole source. The layout divides its categories into **Your follow-up** and **Accessible project work** instead of presenting every accessible record as a personal assignment.

| Category | Actual scope |
|---|---|
| Your follow-up — Handovers | Your private server-saved drafts and publications awaiting your personal acknowledgement. These are not browser-local drafts. |
| Your follow-up — Assigned log issues | Open issues assigned to you or your departments, with unread alerts separately stated. Not every Task, Fault Report or HSE report. |
| Accessible project work — Open tasks | Open Tasks you can access, not only Tasks assigned to you. Overdue, awaiting your review, unread, postponed and postponement-review indicators retain their existing meanings. |
| Accessible project work — Maintenance due & follow-up | Project-wide permitted maintenance due/overdue plus blocked follow-ups. Open orders without dates are separate and are not included in that count. |
| Accessible project work — Certificate dates | Expired records or records within their saved reminder window. Unknown dates remain separate, not deemed valid. |
| Accessible project work — Received groups to place | The administrator's received-group queue. Groups are not summed quantities or in-transit shipments. |

Expand a category to see its limited record preview and full-workspace link. A preview's length need not equal the full count. There is no total combining these different scopes, no invented in-transit counter and no equipment-readiness certification.

Only returned categories are displayed. A missing or invalid required count is shown as unavailable rather than zero. A failed request clears the previous private summary and offers **Retry overview**. The checked timestamp is displayed in UTC. The existing thirty-second refresh runs only while the Home overview is active and the page is not protecting busy input or an operational form.

Request generations, exact target elements, project/user IDs and the current authorised token prevent a delayed response from replacing a newer route or account. Returning Home fetches again. Same-account token renewal refreshes control closures. Expansion preferences are temporary and reset across authorised sessions; no new persistent private-data store is introduced.

## Local work and connection warnings remain above navigation

The existing local-work calculation and review functions are unchanged. Where that main workspace holds drafts, queued changes or conflicts, an **Unsent work** notice precedes ordinary navigation. Counts remain local proposals, not saved server completion totals. **Review unsent work** opens the established review/resume/recovery controls and does not submit or delete anything.

**Saved local work** is always accessible from the heading, even with no currently counted items. **Review separate log windows** uses the existing log-window review for accounts with log access. Neither is a count of every device, nor a claim that unsaved text in a memory-only editor is permanently retained.

An unconfirmed connection is stated separately. Do not clear browser storage, change domains or uninstall an installed browser app while work is unsent. A server backup does not include browser-only work. The local-work export is not an accepted full off-host project recovery procedure.

New Home navigation and refresh controls cannot replace an open operational form. **Home help** opens separately without submitting the form. The main sidebar and other workspaces remain available as before.

## A small post-save routing correction

Testing creation from Home exposed the shared fieldwork form's old inventory/toolbox fallback. Without a dedicated Home return, saving a maintenance order started on Home could display Toolbox under the Home address.

UI13 adds one narrow post-save branch: when that form is still on Home after a confirmed save, redraw Home instead of using the fieldwork fallback. The existing submit functions, payload factories, persistence, operation IDs and other workspace branches remain unchanged. A Task still uses its existing saved-detail destination and alert acknowledgement. The tests exercise actual explicit creation, not just opening dialogs.

## Home Help and remaining review

**Use Home** (`dashboard`) is reviewed against this implementation, including capability restrictions, personal/project scopes, local/server drafts, creation and final destinations. The other **75 registered instructional article bodies remain unchanged**, including the earlier daily, records and maintenance reviews. All 76 topics keep the shared Help reader.

There are now **four distinct bounded wording-reviewed articles**: daily, records, maintenance and dashboard. The native Help, original all-in-one guide and master PDF remain unchanged. Full current-wording, entry-point, hosted/local, native/PDF and accessibility review continues. Updating this article is not completion of the entire Help library.

The original Home request is retained with a progress table in **HOME_PAGE_IMPROVEMENT_PLAN.md**. This is a first implemented Home pass, not a claim that all Home usability is finished. Personalised shortcuts, cross-module return history, physical-device feedback and further role-specific refinement remain review items rather than invented completed features.

## Install through the existing GitHub Desktop workflow

1. Preserve unfinished Wavelink work in every browser and separate log window. Retain the previous approved commit and your established backup. Preserve any uncommitted edits, then fetch/pull the intended branch in the existing **wavelink** checkout. Deploy outside a presentation.
2. Extract the complete ZIP and open **UPLOAD_TO_GITHUB**. Copy its **contents** into the repository root, preserving subfolders. Do not copy the enclosing folder, delete `.git`, or upload `REFERENCE_ONLY`, `PREVIEWS` or `VALIDATION` as application files.
3. Review the diff, commit and **Push origin**. Compared with the supplied complete UI12 upload repository, only **deploy/extract_source.py** changes among existing executable files. Documentation and checksums also change. Reconcile any other outside edits before overwriting them.
4. Deploy the approved commit through the existing Wavelink Render service. Keep the working URL, passwords, guest settings and disk unchanged:

```text
PUBLIC_URL=https://demo.mywavelink.com
INITIALISE_FICTIONAL_DEMO=NO
```

Keep the initial-admin bootstrap setting removed. Expected build output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 13: Home navigation, scoped saved-work overview and reviewed Home Help; includes UI01-UI12; no automatic data changes.
```

After a healthy deployment open Home and look for **UI 13**. Core Wavelink remains **1.34.19**, and other workspaces retain their earlier badges. Preserve unsent work before closing/reopening older tabs for the service-worker update. **Do not clear site data.**

No inventory upload, category reset, new project or demonstration re-import is required. Existing users, equipment, categories, manifests, original documents and uploads remain in the persistent project. Unapplied demo categories retain the explicit administrator preview-and-apply workflow.

## Acceptance, rollback and boundaries

Test normal and guest entry, role-restricted Home destinations, local-work notices, unavailable overview, and at least one actual reviewed fictional Task/work-order creation. Check Inventory, nested boxes, categories, Record management, manifests, receiving, Checklists and Maintenance after updating. Verify same-project record identity and persistence through a deliberate restart outside the presentation. Test real phones and the intended desktop displays.

Revert the extractor commit or use the exact UI12 extractor at **REFERENCE_ONLY/Workspace_UI13/rollback/deploy/extract_source.py**. Do not reset the project, clear the disk or re-enable first-deploy initialization to roll back an interface.

The original recovery helper is still pinned to pristine source and **unapproved for the overlaid runtime**. Do not bypass its checks. Overlay-compatible off-host recovery remains separate operator acceptance.

This package contains no live secrets or current database. It is not a live-service backup. Gateway, guest bootstrap, supervisor, Dockerfile, runtime dependencies, vendor source parts/seed and recovery helper remain byte-identical to the supplied UI12 package. All application Python services remain unchanged. No new API, SQL format, browser database or authentication rule is introduced. The native vessel installation and CCVD relay are outside this work.

## Validation and continuation

Results use local Chromium and the shipped application scripts/styles with temporary fictional Wavelink databases, TestClient-backed HTTP and injected in-memory browser persistence. Before/after previews are actual local rendering, not live custom-domain screenshots or native Windows captures. All Help routes are checked with desktop imports blocked.

The full product suite, Docker image build, live GitHub/Render deployment, physical phones/Windows, durable browser storage, off-host restoration and complete accessibility acceptance are **not** claimed. This is not production-security, multi-company isolation or vessel/cloud-synchronisation approval.

Next: actual Home and inventory feedback; remaining maintenance approval, pending-follow-up release and linked-asset forms; continuing Help review and Original Files logical-folder work. No original documents are moved. The development order is not an automatically running background task.

## Final selected local results

**527 distinct targeted Python tests and 100 compound browser checks passed** in the final selected runs, with no failed, errored or skipped Python cases and no recorded browser errors. All43 JavaScript files passed syntax checks. Actual Home-initiated create/save routes were exercised with fictional data, including the existing Task alert acknowledgement. Source and extractor remained frozen throughout these final runs.

Fresh final-ZIP verification is recorded separately; repeats are not additional distinct coverage. Initial findings and preliminary tests are retained separately.
