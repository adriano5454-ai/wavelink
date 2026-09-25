# Wavelink — Workspace UI 14

**Core 1.34.19 · cumulative UI01–UI14 · prepared 25 September 2026.** Built from the supplied full UI13 package. Implemented and tested locally; the live GitHub checkout was not fetched and this package was not deployed to Render.

## This update: two clearer Maintenance review flows

UI13 Home and earlier inventory, shipment, checklist and maintenance improvements remain included. UI14 continues the pending detailed-form work rather than replacing Home or changing the hosting setup.

### Review a saved maintenance step

In **Maintenance**, open an order, go to its work steps and use the existing approval/review action where your account is authorised. The form now separates **Saved result & evidence → Decision & note → Confirm review**.

The first page reads the current saved step and identifies its result revision, recorder and saved time. Review its readings and supporting photographs; missing/unavailable photographs block progression and approval. Browser-local step drafts are not submitted by this review.

Choose **Approve** or **Request changes** explicitly; Approve is no longer preselected. Request changes requires a review note. The final page shows the exact decision and note, then requires fresh confirmation. Going Back or changing the reviewed values clears that confirmation. A stale result is rejected by the existing server version checks rather than overwriting someone else's work.

**Save review decision** records a review of the saved step only. It does not close the work order, rewrite the readings/photos, release quarantined equipment or authorise operations. Existing reviewer permissions and same-person review recording are retained. Approval notes are not browser-local drafts and are not queued for automatic submission: a project connection is required.

### Review a pending follow-up

For an eligible completed order with a blocked/pending next cycle, use the existing review-pending-follow-up action in the order's review/cycle area. The form now separates **Pending date & routine → People & review note → Confirm next order**.

It shows the saved pending due date, why the follow-up needs review and the current published routine. Review available people and add a reason, then inspect the proposed order before **Create reviewed follow-up**. Previous assignees unavailable in the current directory are called out. No named people selected means any account with Maintenance-work permission may record steps; it does not mean nobody or a private assignment.

An eligible save requests one open follow-up with empty results, using the existing pending date. The completed order's evidence is retained. Existing local draft, version, operation-ID and retry mechanisms are unchanged; resumed forms do not retain final confirmation.

**A saved response does not by itself prove that a next order was created.** The existing service can instead save a continuing block, for example when the procedure changed during review. Check the saved Maintenance-cycle state afterwards: a created next-order link and a follow-up-needs-review state have different meanings. No new success notification claims creation unconditionally.

### Old responses must not open the wrong form

The two preparation reads are tied to the current route, account/token, exact workspace view and dialog state. An old response is discarded after navigation or when another operational form has opened. Approval submission and photograph rendering also check that their original review is still current. These are bounded guards on the changed paths, not a claim of a new global security model.

## Where the version appears

The first pages of the changed Maintenance review forms show **UI 14**. The Home workspace retains its **UI 13** badge and unchanged implementation. Other workspaces retain their own earlier badges. Core Wavelink remains **1.34.19**. This is not a native Windows interface update.

## Help and remaining development

The **Maintenance** article now explains these two guides, their permissions, final effects, local/server distinctions and saved-block outcome. Its outline and search catalogue are aligned. The other **75 instructional article bodies are unchanged**. All 76 topics retain the shared reader; common cache references advance with UI14.

There are still **four distinct bounded wording-reviewed articles**: daily, records, maintenance and dashboard. Re-reviewing Maintenance does not make a fifth. The remaining 72 article bodies, complete entry-point/accessibility review, native Help, all-in-one reference and master PDF have not been brought fully up to date by this release.

Exact-asset work-order creation and the separate saved-evidence viewer remain pending detailed-form reviews. Existing versions of those functions are not removed. Actual Home/inventory/boxes/manifests/receiving feedback remains first priority when supplied. Original Files logical-folder organisation is still pending; this update does not move source documents or change their revision identities.

## Install through the existing GitHub Desktop workflow

1. Preserve unsent work in every browser and separate log window. Retain the last approved commit and established backup. Preserve uncommitted/outside edits, then fetch/pull the intended branch in the existing **wavelink** checkout. Choose a time outside a presentation.
2. Extract the complete ZIP. Open **UPLOAD_TO_GITHUB** and copy its **contents** into the repository root, preserving subfolders. Do not copy the enclosing folder, delete `.git`, or upload the outer `REFERENCE_ONLY`, `VALIDATION` or `PREVIEWS` folders as application files.
3. Review the diff, reconcile outside edits, commit and **Push origin**. Compared with the supplied UI13 upload repository, only **deploy/extract_source.py** changes among existing executable files. Documentation and checksums also change.
4. Deploy the approved commit using the existing Wavelink Render service. Keep the working domain, passwords, guest settings and persistent disk unchanged:

```text
PUBLIC_URL=https://demo.mywavelink.com
INITIALISE_FICTIONAL_DEMO=NO
```

Keep the initial-admin bootstrap setting removed. Expected build output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 14: maintenance approval and pending-follow-up reviews; includes UI01-UI13; no automatic data changes.
```

Preserve unsent work before closing/reopening older tabs for the service-worker update. **Do not clear site data.** No new project, inventory upload, category reset, demo re-import or first-deploy initialization is required. Unapplied fictional categories retain their existing explicit administrator preview/apply process.

## Acceptance and rollback

Check normal and guest entry, Home, inventory/boxes, shipments/receiving, Record management, checklists and maintenance. With fictional records and authorised accounts, exercise an actual approval and an eligible pending-follow-up save; also verify a continuing-block case and restricted-user controls. Confirm identity/persistence after a deliberate service restart outside a presentation and test the intended phones/desktop displays. UI14 has not performed those live checks for you.

Rollback by reverting the extractor commit or using the exact UI13 extractor at **REFERENCE_ONLY/Workspace_UI14/rollback/deploy/extract_source.py**. Do not reset the project, clear the disk, clear browser storage or re-enable initialization to roll back this interface.

The original recovery helper remains pinned to pristine source and is **unapproved for the overlaid runtime**. Do not bypass its checks. A source package is not a backup of your live service, and server backups do not include browser-only unsent work. Overlay-compatible off-host recovery remains separate acceptance.

## Local validation and its limits

**405 selected Python cases and 119 compound browser checks passed**, with no failed, errored or skipped cases in those completed Python runs and no recorded errors in those browser runs. All **43 JavaScript files** passed syntax checks. Tests include real explicit approval and follow-up saves, stale-result conflicts, lost-response retry, missing photographs, route/token changes and five viewport widths for the new forms.

The browser runs use local Chromium, actual application scripts/styles, TestClient-backed HTTP and temporary fictional databases, with injected in-memory browser persistence. Previews are actual local renderings, not live-domain or native screenshots.

**Broader inherited template/Task-checklist attempts did not finish cleanly in this environment.** Their partial results and earlier runner/exit stalls are retained under `VALIDATION/development` and excluded from the passing totals. The cause of the waits is unestablished. The full product suite, Docker build, live deployment, physical-device/durable-storage/off-host restoration and complete accessibility/security/company-isolation acceptance are not claimed. See `VALIDATION/FINDINGS.md` for the exact boundary and completed selection.

## Source and package boundary

All **2,959** listed parent UI13 package files were verified. Parent ZIP SHA-256: `29e233233b14de9e71123392184100da3e2a6a89a0d3b46b9cbcb050ca516981`. Original upstream source remains pinned to `8c1b6a8d731d01b05a1290d3a1dd1a544054147aac9048ca345af7983613cd9e`.

UI14 changes **85 incremental resources**, mostly shared Help cache wrappers; the cumulative extractor contains **119 overlays** and produces **1,625 tracked files**. Extractor SHA-256: `750c43d16d0752873cf49bc54469df98f64de0bcdded36db919f2b6c06f2d292`. All application Python files are byte-identical to supplied UI13. Existing hosting/gateway/guest/bootstrap/supervisor/Docker/dependency/vendor/seed/recovery files remain unchanged. No new API, SQL format, browser database, permission or authentication rule is introduced.

This package contains no live project database or passwords. It adds no vessel/cloud synchronisation and performs no automatic data categorisation or development. The native vessel installation and CCVD relay remain outside this update.
