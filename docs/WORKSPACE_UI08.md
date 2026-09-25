# Wavelink — Workspace UI 08

**Core 1.34.19. Cumulative UI01–UI08. Prepared 25 September 2026. Local implementation and validation; not deployed to the live GitHub repository or Render by this session.**

## Scope

UI08 applies the cleaner list/detail pattern to the browser **standalone Checklists catalogue**, and reviews two related Help articles against current browser controls. Task-owned checklists retain their separate Tasks workflow. The individual check/reading/photo/approval/participant/finalisation editors are not redesigned by this increment.

The source is the supplied complete UI07 ZIP. Its 1,069 package hashes were verified before editing. The original five source parts remain the pinned 1.34.19 archive. Against that supplied upload repository, **only `deploy/extract_source.py` changes among existing executable files**. It applies the cumulative checked resources during image build. Hosting/gateway/login/startup/Docker/dependencies/vendor/seed/recovery files remain unchanged. The live repository was not fetched; reconcile outside edits before replacing anything.

## A clearer starting point for standalone checklists

Open **Checklists** in the main sidebar. **New checklist / dive** opens the existing new-record form when you have creation access. **Refresh** rechecks saved records; **Help** opens the reviewed browser instructions. Assigned work with a Task-owned checklist remains in **Tasks**, not automatically linked to a standalone record.

Search by record reference or identity, type/revision, project, vessel, equipment, client, record date or notes. **Type & sort** contains the checklist-type filter and Recently updated, Recently created or natural Reference A–Z order. Selected choices remain readable when the panel is closed. Search and filter preferences are temporary for the current authorised session, not permanent browser storage.

| View | Meaning |
|---|---|
| Open work | A listed record has at least one unfinished stage. |
| Issues & review | An unfinished stage has saved issues, For later/deferred checks, pending item approvals or approval changes requested. Ordinary Pending checks alone do not enter this view. |
| Closed | Every existing stage has been explicitly finalised. |
| All records | Both open and closed records in normal active selection; not postponed, cancelled or archived records. |

The status counts precede search/type filters. The matching-record count describes the current filtered result. Neither is a count of assets or summed stock quantities. Retained records remain in the existing **Record management** workspace.

## View a summary before opening the work

Select the reference or **View summary**. On desktop the summary appears beside the list. On a phone it opens full-width instead of leaving a long list above it; **Back to checklist records** returns to the list context. The mobile heading is compact, but unsent-work and failed-refresh warnings remain available.

The summary shows the saved type revision, job details, stage outcomes and the next unfinished stage. **Open [stage name]** enters the established checklist workflow. When every stage is finalised it instead offers viewing the finalised record. Each individual stage remains available, and record notes/identity expand deliberately.

**Selecting the summary does not join a stage, post a heartbeat, record a result, approve or finalise anything.** Opening a stage is a separate deliberate action and retains its existing participant/heartbeat, refresh and synchronisation behaviour. A read-only account gets only the controls allowed by the existing services.

Completed and N/A counts are separate. The combined progress indicator is descriptive only: it is not finalisation or approval. Issues, For later/deferred work, required evidence, readings, item approvals and team readiness keep their existing rules. No action certifies equipment as safe to operate.

Opening a stage from a search provides **Back to checklist search**; other filtered views provide **Back to filtered checklists**. Returning in the same authorised session preserves the selected record and filters. Internal list scroll is retained on redraw, and Clear filters deliberately returns that list to the start. This is not a universal cross-module history.

## Unsent work and refreshed information

The catalogue displays **Unsent checklist work on this device** when the existing checklist queue, item drafts or new-record draft contain work. **Review saved work** opens the existing review dialog. **Continue new checklist** opens the established creation draft when access permits. Local item drafts/queued changes for the selected record are shown separately from saved server counts.

No new storage format, automatic queue or offline capability is added. Existing browser recovery and account-scoped saved-work rules remain. Creating records, approving and live structure changes still require their existing server access.

If a refreshed filter no longer contains the selection, its summary clears rather than retaining a hidden target. A failed network/server refresh marks the retained list **Saved list — refresh failed** and clears the selected summary; local saved work is not discarded. An authorisation failure hides the previous private list/details. Old-account and superseded list responses cannot overwrite newer records.

Open operational forms block catalogue controls from replacing the current view underneath them. Help opens separately without submitting a form. Do not clear site data, change hostname or uninstall an installed browser app while work is unsent.

## Templates and retained records are secondary tools

Expand **Templates, retained records & work rules** for the administrator's **Checklist template library** and **Record management** links. The template route uses the existing browser **Administration → Templates & routines** workspace, not a newly invented editor or importer.

The new-record form's supporting wording now points to that browser route rather than implying that Windows Admin is required to manage every published type. Its fields, validation, save payload and definition limits are unchanged.

## Help wording review: two articles, not the whole library

UI07 standardised the presentation of all 76 registered browser topics while retaining their source instructions. UI08 explicitly reviews and updates **Complete a checklist** (`daily`) and **Manage checklist records** (`records`). These two now describe the current browser catalogue, action meanings and browser/local distinctions. Their previous exact content remains in the preserved parent checkpoint and readable source diff.

The records article separates browser **Postpone, Cancel, Archive and Restore** from legacy native **Delete active checklist / Deleted** labels. It also distinguishes standalone record restoration from Task postponement/reopening, and keeps disconnected-device, conflict, evidence and finalisation limitations.

The other **74 articles' instructional text is unchanged**; their shared reader cache-reference version changes only. The all-in-one reference, native Help and master PDF remain unchanged. HELP-04 through HELP-10 are still partially complete or pending as documented in **HELP_STANDARDISATION_REVIEW.md**. This is not a claim that all current wording, screenshots, imports, native/PDF output or accessibility have been rechecked.

## Apply the complete ZIP through GitHub Desktop

1. Preserve unfinished Wavelink work in every browser and separate log window. Retain the previous approved commit and an appropriate project backup. Make changes outside the client presentation. Do not clear browser storage.
2. Select the existing **`wavelink`** repository in GitHub Desktop. Preserve uncommitted edits, then fetch/pull the intended branch.
3. Extract the full ZIP and open **`UPLOAD_TO_GITHUB`**. Copy its **contents** into the local repository root, preserving subfolders. Do not copy the enclosing folder, remove `.git`, or upload `REFERENCE_ONLY`/`VALIDATION` as application files.
4. Review the diff, commit, then **Push origin**. Only the extractor is an intentionally changed executable file relative to the supplied UI07 upload repository; reconcile any other outside edits before overwriting them.
5. Deploy that approved commit through the existing Wavelink Render service. Leave disk, passwords, guest settings, URL and environment unchanged. Keep **`INITIALISE_FICTIONAL_DEMO=NO`** and the initial-admin bootstrap variable removed.
6. Expected build output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 08: checklist catalogue and reviewed browser Help; includes UI01-UI07; no automatic data changes.
```

After a healthy deployment, open Checklists and check **UI 08**. Core Wavelink remains **1.34.19**. The shared Help viewer and other workspaces keep their earlier badges; the two reviewed articles identify their UI08 wording review. Preserve unsent work before closing/reopening older tabs to activate changed service-worker resources. Do not delete site data.

**No inventory re-upload, category reset, new project or demo reseeding is needed.** Already-applied categories, equipment identities, manifests, users and uploaded files stay in the existing persistent project. Unapplied demo categories retain the explicit administrator preview-and-apply flow.

## Validation and limits

See **DELIVERY_CHECKS.json**, **VALIDATION/final/** and the final-package verification for exact commands, distinct case counts, errors and reruns. Tests use temporary fictional databases, actual Wavelink services and shipped scripts, a controlled browser transport and injected in-memory browser persistence. Screenshots are actual local rendering, not live Render or native Windows captures.

The complete application suite, Docker image build, live GitHub/Render deployment, physical phones/Windows, durable browser storage, real HTTPS navigation, off-host recovery and complete assistive-technology acceptance are not claimed. An unchanged-source full set of selected regressions is not the full product test suite.

The original recovery helper is pinned to pristine source and remains **unapproved for an overlaid runtime**. Do not remove its source checks to force backup or restoration. Operational recovery acceptance is separate from this interface update.

## Rollback and continuation

Revert the extractor commit and redeploy, or use the exact UI07 extractor at **REFERENCE_ONLY/Workspace_UI08/rollback/deploy/extract_source.py**. Do not reset the persistent database, re-enable initialization, or re-import the original project. Keep category operations on the compatible category-aware runtime.

Next: the remaining checklist working forms and maintenance layouts, plus HELP-04–HELP-10. Actual inventory/box/manifest/receiving feedback keeps priority. Original Files logical folders, hosted security/isolation/recovery and vessel/cloud synchronisation remain separate pending work. The development order is not an automated background task.
