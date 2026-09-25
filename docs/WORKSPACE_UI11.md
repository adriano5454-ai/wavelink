# Wavelink — Workspace UI 11

**Core 1.34.19 · cumulative UI01–UI11 · prepared 25 September 2026.** Local implementation and tests. Not deployed to the live GitHub repository or Render. This is a browser update, not a native Windows Admin release.

## Scope

UI11 focuses on two existing Maintenance forms: **New work order** from the Maintenance catalogue and **Record / update step** inside an open order. They use the existing guided-form component, action services, local draft store, operation IDs and saved versions. No new operational API, database schema, permission system, photo store or automatic task/cycle action is introduced.

The earlier inventory, boxes, categories, Record management, manifests, receiving, Checklists and Maintenance workspaces remain included. The only changed existing executable upload-repository file relative to the supplied full UI10 package is **deploy/extract_source.py**. It verifies the original five source parts and applies the cumulative overlay at image build time.

The live repository was not fetched. Reconcile changes you made outside the supplied packages before overwriting them. This ZIP is not a backup of the live project.

## Create a work order without one long form

Open **Maintenance → New work order** using an account with the existing maintenance-management permission.

| Page | What to review |
|---|---|
| Work & equipment | Choose a published routine deliberately, then enter the order title, optional reference and equipment description. |
| People & instructions | Select eligible named workers and record the work instructions. |
| Due date & cycle | Optionally enter the UTC due time and choose One-off or the existing repeat configuration. |
| Review order | Check the intended routine revision, equipment description, assignments, due time, cycle and instructions; confirm and Create work order. |

The first routine is no longer selected automatically. Its summary shows the published title/revision, system, document code and defined-step count. **That summary is not the full procedure**: read the frozen Instructions before performing work. A stale routine revision or invalid assignee is still rejected by the existing service when saving.

Equipment description is text, not an inventory link. For an exact equipment link, use **Asset details → Maintenance → New linked maintenance**. That separate linked-creation form is unchanged in UI11.

No named assignees permits the existing authorised maintenance workers/managers; it is not anonymous access. Assignments restrict who performs work, not project-wide Maintenance viewing. Private assigned Tasks remain separate.

One-off remains the default, with no invented due date. Selecting a repeat reveals its interval/unit/basis fields. Switching back to One-off preserves the entered values in the local form but does not send an enabled recurrence. A fixed scheduled cycle requires a due time; a completion-based cycle keeps its existing completion-time rule. Creating an order saves one open order with empty results, not a completed inspection or automatically approved procedure.

## Record a step in three focused pages

Open **Maintenance → an open work order → Work steps → Record / update step**.

| Page | What belongs there |
|---|---|
| Result & readings | Exact order/step context, previous saved-result details, original guidance, result choice and defined reading fields. |
| Notes & photos | Work notes, change reason and the existing photographic-evidence editor. |
| Review result | Saved versus proposed result, readings, notes and photo counts; explicit confirmation and Save step to project. |

The form shows the step position in routine order, saved status/actor/time/revision and required-approval state. Instruction text and source references remain visible. Existing reference pictures keep their own controls; they are never counted as completion photographs.

Readings retain the actual definition's labels, units, required-for-Complete flag and saved numeric limits. UI11 displays these limits but does not invent any. Missing required readings block Complete. Numeric values outside the saved range remain invalid under the existing service even when Issue is selected. Pending/For later/Issue can retain partial work and missing required evidence where the existing validators allow it.

Explain Not applicable or Issue. Replacing saved work still requires a change reason. Required photographs still apply before Complete or N/A. Photo preparation, compression, captions, removal, five-photo limit, local storage and upload verification use the existing implementation. **There is no new generic file attachment feature.**

Review compares the previously saved result with the proposed values and photo counts/captions. Review the actual photos on the preceding page: a count does not verify content. **Save step to project** saves only that step. It does not grant item approval, complete the order, release quarantine, change custody, verify stock or authorise operation. A changed saved result may require fresh item approval.

## Review, local forms and protection of unfinished work

**Back** preserves the entered values but clears final acceptance. The final checkbox is deliberately unnamed, is not stored as an approval, and is not sent in the API payload. Keep/resume starts at the first page with the existing form values and no retained final acceptance. Browser/autofill changes after a review require another review.

**Keep draft & close** and **Discard draft** remain explicit. A local draft is not a confirmed project result. The draft-status wording now uses the active form's save-button label; the shared component's old default remains unchanged for other forms.

Continuing while photographs are being prepared is blocked. The original saved-version, operation-ID retry, current-permission and local-persistence checks remain. A lost response may still mean the server saved the action; the retained unchanged-request retry does not create a second result. This update does not create a new durable browser store or automatic submission queue.

Existing navigation guards stop the main work-order controls from replacing the record underneath an open form. No live Render process, account, password or project data is changed by the build.

## Desktop and mobile

On desktop, reading fields sit side by side where space permits, and Saved/Proposed comparisons are adjacent. On narrow screens they stack. The form body scrolls separately from its bottom actions, keeping Continue/Back/Save and local-draft actions reachable. First-page Continue cannot accidentally submit the form; the actual action is reserved for the final reviewed page.

This is still a focused dialog. Individual approval, saved-evidence viewing, cycle-change, follow-up, completion/cancellation and linked-asset creation dialogs are not redesigned internally by UI11. Those remain explicit next scopes rather than claimed finished.

## Help review

**Record maintenance work** now describes the catalogue creation guide, three-page result entry, photo review and local-draft distinction. The other **75 registered topic bodies retain their instructional text**. The shared Help reader and catalogue cache references update. Native Help, the all-in-one reference and the master PDF remain unchanged.

Three distinct articles have bounded wording reviews so far (daily checklists, record management and maintenance); revising Maintenance again does not make a fourth completed topic. The full HELP-04–HELP-10 review, hosted/local distinctions, entry points, native/PDF consistency and accessibility remain ongoing.

## Install the complete ZIP with GitHub Desktop

1. Preserve unfinished Wavelink work in every browser and separate log window, retain the previous approved commit and a suitable project recovery copy, and deploy outside a client presentation. Preserve local uncommitted edits before fetching/pulling the intended branch.
2. In the existing **wavelink** checkout, copy the **contents of UPLOAD_TO_GITHUB** from this ZIP into the repository root. Preserve the folders. Do not copy the enclosing folder, delete `.git`, or upload REFERENCE_ONLY/VALIDATION/PREVIEWS as application files.
3. Review the diff, commit and **Push origin**. Against the supplied UI10 upload tree, only **deploy/extract_source.py** intentionally changes among existing executable files; documentation and checksums also change. Reconcile outside edits first.
4. Deploy the approved commit through the existing Wavelink Render service. Leave the working hostname, gate, guest credentials, settings and disk alone. Keep **PUBLIC_URL=https://demo.mywavelink.com**, **INITIALISE_FICTIONAL_DEMO=NO**, and the initial-admin bootstrap setting removed.
5. Expected build output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 11: guided maintenance work and result forms; includes UI01-UI10; no automatic data changes.
```

After a healthy deployment, open New work order or a Maintenance step and look for **UI 11** in the form. Core Wavelink remains **1.34.19**, and workspaces not changed by this update keep their earlier UI badges. Preserve unsent work before reloading/closing tabs to activate the service-worker update. **Do not clear browser storage.**

No inventory upload, category reset, user reset or demonstration re-import is required. Existing categories stay in the persistent project; unapplied demo categories still use the explicit administrator preview-and-apply flow. Never enable initialisation or clear `/var/data` to obtain a UI update.

## Hosted acceptance and rollback

Use fictional data for acceptance. Test normal/guest sign-in on the working domain, create one harmless order, save a partial and a completed step, attach a permitted fictional image, keep/resume a draft and inspect the saved result. Review a read-only account, routine/version conflict, photo requirements and a deliberate restart outside the presentation. Confirm inventory/categories/manifest/receiving navigation remains intact.

Rollback is an extractor-commit revert; the exact UI10 extractor is included in **REFERENCE_ONLY/Workspace_UI11/rollback/deploy/extract_source.py**. It does not reset the database. Preserve pending drafts before any rollback.

**The original pristine-source recovery helper remains unapproved for overlaid runtimes. Do not bypass its source checks.** Overlay-compatible off-host recovery is a separate operator acceptance requirement; a source ZIP is not a project-data backup.

## Validation boundaries and next work

Exact local tests, initial findings and final-package checks are included in DELIVERY_CHECKS.json and VALIDATION. Browser checks execute the shipped scripts/styles against temporary fictional Wavelink services, with controlled HTTP and injected in-memory persistence. Previews show local rendering, not the live domain or a physical phone.

The full application suite, Docker build, live GitHub/Render deployment, durable browser storage, off-host recovery, physical devices and full accessibility were not verified here. No production-readiness, company-isolation or vessel/cloud-synchronisation claim is made.

Next: remaining detailed approval/cycle/close forms, ongoing Help review and actual hosted feedback. Inventory, boxes, manifests and receiving problems retain priority. Original Files logical folders remain a separate pending improvement. No original documents are moved. The roadmap is a development order, not an automated background task.


## Final local results

**510 distinct targeted Python cases and 128 compound browser checks passed**, with no failures/errors/skips in the accepted Python results and no browser-script errors. All **41 JavaScript files** passed syntax checking. The initial new Python run had 14 fixture setup failures; the field-key fixture was corrected without changing runtime and all101 new cases passed on a complete recheck. Those original failures and earlier development corrections are preserved separately from the accepted results. This is a reconciled set of selected tests, not a full product run.

All76 browser Help routes also passed with desktop/Tk imports deliberately blocked and without operational database writes. No runtime/extractor bytes were changed after accepted testing. Fresh final-ZIP extraction and repeat results are recorded in the separate final-package verification file; repeats are not additional distinct coverage.
