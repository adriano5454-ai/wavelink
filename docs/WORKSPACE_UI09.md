# Wavelink — Workspace UI 09

**Core 1.34.19 · cumulative UI01–UI09 · prepared 25 September 2026.** Local implementation and targeted validation. Not deployed to GitHub or Render by this session; the live repository was not fetched.

## Scope

UI09 organises the **opened standalone checklist stage**. UI08's catalogue, prior inventory/categories, Asset details, Record management, receipt/placement and shipment workspaces are retained. Task-owned checklists stay in Tasks. This is browser work for computers and phones, not a native Windows Admin release.

The complete package is derived from the supplied Full UI08 ZIP (SHA-256 `395206604e68908897aac96ff7da3e5803715654050977982ba52c471a06b09d`). All 1,305 parent package hashes were verified before editing. Original source parts remain the checked 1.34.19 archive. Only **deploy/extract_source.py** changes among existing executable upload-repository files; it applies the cumulative checked source overlay at image build. Docker, login, gateway, guest links, startup, dependencies, vendor parts and seed are unchanged relative to that supplied package. Reconcile outside repository edits before replacement.

## Find the check, not another long page of controls

Open **Checklists → select a record → Open [stage name]**. The opened stage now has three focused areas:

| Area | Purpose |
|---|---|
| **Checks** | Search, choose a section, inspect results and open the existing check/reading/evidence forms. |
| **Team & stage review** | Review whole-stage outstanding work, required approvals and participating devices; deliberately use existing readiness/finalisation actions. |
| **Instructions & source** | Read the saved template instructions, exact source links, document metadata, tools and authorised live-edit tools. |

The record reference, template revision, stage links and final/ready state remain visible. **Record tools** contains Record details, Export PDF and Help. On a phone, the header avoids repeating all job metadata; Record details retains the full saved values. The main application sidebar stays.

### Search and filter within the actual stage

**Search this stage** matches check number, wording, group/section, displayed reading labels/values and current displayed notes. **Section** narrows the scope. Desktop uses status buttons; mobile uses the **Show** selector with the same choices:

- **All checks** — every applicable item in the chosen scope.
- **Needs attention** — unfinished results, local drafts/queued/conflicting work or outstanding required item approval.
- **For later** — deferred items in the selected section. They are not appended from unrelated sections below every view.
- **Item approvals** — checked entries pending sync/approval or with requested changes.
- **Local work** — item drafts and queued/conflicting results, not a claim of server confirmation.
- **Recorded** — saved Complete/N/A entries without local pending work. Required item approval may still be outstanding.

Filters preserve the template's item order. Status-button counts are for the selected section before text search; the matching count uses all selected filters. Expand **How counts and filters work** for the distinction. **Hidden checks still count toward finalisation.** Categories, physical boxes and inventory data are not involved in these checklist filters.

**Clear filters** returns to all checks/all sections. **Find next unfinished** clears narrow filters, opens Needs attention across the stage and focuses the first matching check in template order. It does not mark Complete, open a submitting form, approve a result or advance a stage. It is a navigation action, not operational automation.

### Saved results and work held on this device are separate

The saved-stage summary uses the last server snapshot. Queued edits and local drafts are excluded from these totals. An individual card may show a local proposed result while its saved total remains unchanged. Completed and N/A remain separate counts; neither is finalisation or authorisation to operate equipment.

The stage's local-work notice offers **Show local work** and **Review saved work**. The latter opens the established local-work review. No new browser database, local queue or automatic background save is added. A local draft is not a server-confirmed check.

### Team review is separate from working through the list

Open **Team & stage review** to inspect required approvals, participating devices and outstanding checks across the **whole stage**. Its shortcut filters deliberately clear narrower section/search filters. A zero attention count is not an approval decision or a replacement for server checks.

**Done on this device**, **Finalise stage**, **Resume editing** and **Leave checklist** retain their existing dialogs, permission checks and API payloads. Opening the review area does not post a readiness or finalisation request. Opening a stage still uses the existing participant/heartbeat workflow; this update does not redefine participation.

Pending/Issue/For later results, local work, required evidence/readings, missing/invalid item approvals and device readiness keep their existing rules. Changing tabs or filtering does not bypass any of them. A finalised stage stays locked. Resuming a ready device requires a connection. Same-person approval remains labelled according to the existing rules; administrator status does not make someone an assigned item approver.

The existing reading/photo/check, approval, conflict and finalisation editors are **not redesigned internally** in this increment. Their validation, draft recording, confirmation and service writes are preserved.

## Navigation and unfinished-work protections

Stage view choices are held in memory for the same record/stage/authorised session. A change of stage or session resets these filters. A numeric view generation, not a session token in the DOM, prevents the generic redraw helper from restoring old-account field values. If live template changes remove the selected section, the view falls back to All sections without restoring the obsolete selector.

The new tabs, status/section controls and navigation refuse to replace the workspace beneath an open operational dialog. Same-view redraw retains existing disclosure and scroll behavior. Existing save strips, conflict notices, finalisation and ready-lock notices remain available. Disconnection displays the boundary between local work and confirmed server results.

This is not a new universal cross-module return history, a persistent draft store for Fleet, or vessel/cloud synchronisation. Existing prior module behavior is unchanged.

## Help review

**Complete a checklist** (`daily`) now explains the current stage areas, scope-aware filters, saved/local totals, Record tools, and team readiness. The associated inline “For later” hint no longer incorrectly says that all deferred checks move to the bottom of every view.

The other **75 topic articles keep their instructional text**. Their shared reader script URL changes only to refresh the search catalogue. The **Manage checklist records** article retains its UI08 wording review. Previous article content is preserved in the parent checkpoint and readable diffs. Native Help, the original all-in-one guide and master PDF remain unchanged. Full HELP-04 through HELP-10 review remains partly complete/pending; this does not declare the whole Help library current.

## Install the complete ZIP through GitHub Desktop

1. Preserve unfinished Wavelink work in all tabs and separate log windows. Retain the previous approved commit and an appropriate project backup. Preserve local uncommitted edits, then fetch/pull the intended branch in your existing **wavelink** checkout. Deploy outside a client presentation.
2. Extract the ZIP and open **UPLOAD_TO_GITHUB**. Copy its **contents** into the local repository root, preserving the folders. Do not copy the enclosing folder, delete `.git`, or upload REFERENCE_ONLY/VALIDATION as runtime files.
3. Review the diff, commit and **Push origin**. Against the supplied UI08 upload repository, only `deploy/extract_source.py` is intentionally changed executable code. Additional notes/checksums are separate. Reconcile any outside edits before overwriting them.
4. Deploy the approved commit through the existing Wavelink Render service. Keep URL, guest settings, passwords, persistent disk and environment unchanged. Keep **INITIALISE_FICTIONAL_DEMO=NO** and the initial-admin bootstrap setting removed.
5. Expected build output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 09: focused checklist stages and review navigation; includes UI01-UI08; no automatic data changes.
```

After a healthy deployment, open a checklist stage and look for **UI 09**. Core Wavelink remains **1.34.19**; the catalogue and other workspaces retain their preceding UI badges. Preserve unsent work before reloading or closing older tabs for the service-worker update. **Do not clear browser storage.**

No inventory upload, category reset, data migration, new project or demonstration re-import is needed. Existing category assignments, users, equipment, shipments and uploaded documents remain on the existing persistent disk. Categories not yet applied use the unchanged administrator preview-and-apply action.

## Acceptance on the hosted copy

Use fictional data. Check normal named sign-in and the restricted guest link. Open a test record, use each stage tab and filter, inspect a reading, save a harmless result and confirm its saved/local status. Inspect required evidence and approvals without treating simulated data as an operational sign-off. Try a finalised record and a view-only account. On a phone verify the Section/Show controls, record tools, outstanding-work shortcut, scroll and open-form guard. Confirm inventory/categories and shipment workflows still behave as expected.

**Do not use the pristine-source-pinned recovery helper on an overlaid runtime by bypassing its checks.** Overlay-compatible off-host backup/restoration remains an operator acceptance item, not something implemented or proved by this UI release.

## Rollback and continuation

Revert the extractor commit and redeploy; the exact UI08 extractor is also preserved at **REFERENCE_ONLY/Workspace_UI09/rollback/deploy/extract_source.py**. Do not reset the database, enable seeding, or re-import the project for an interface rollback.

Next: maintenance UI and remaining detailed working forms, alongside the full Help wording/entry-point/native/PDF review. Actual inventory/box/manifest/receiving feedback takes priority. Original Files logical folders, hosted security/company isolation and recovery remain separate pending work. The roadmap is a development order, not an automated background job.

## Validation limits

See DELIVERY_CHECKS.json and VALIDATION/final for exact results. Testing uses actual shipped scripts, temporary fictional application services and controlled browser transport/storage. Screenshots are local browser renderings, not live Render or Windows captures. No complete product regression run, Docker build, live deployment, physical phone, durable browser-storage, off-host recovery or full accessibility acceptance is claimed.


## Final local validation results

**572 distinct targeted Python cases and 97 compound browser checks passed**, with no failures, errors or skipped cases in the final targeted runs. All 39 JavaScript files passed syntax checking.

The first selected inherited run had two obsolete assertions (pristine cache name and a pre-category inventory hash). Both were reproduced on unmodified UI08. The original tests remain untouched; the saved-work adapter checks the current cache name and exact UI08 business-service preservation while retaining all inherited delivery scenarios. Initial failures and the UI08 reproduction are retained in VALIDATION. Final suites were rerun on a fresh extraction after the last scoped navigation fix.

Fresh final-package extraction and repeat checks are recorded separately; they are not counted as additional distinct test coverage.
