# Wavelink — Workspace UI 06

**Core 1.34.19. Cumulative UI01–UI06. Prepared 25 September 2026. This package is a local implementation, not an update already deployed to GitHub or Render.**

## What changes

UI06 continues the inventory and shipment usability work after UI05. It improves the **shipment catalogue** and the remaining **dispatch, cancellation and closure reviews**. The inventory folder navigation, categories, Asset details, Record management and Receiving & placement workspaces from UI01–UI05 are retained.

This is the browser interface on computers and phones, not a new native Windows installer. Relative to the supplied complete UI05 package, five browser resources change. Backend Python business services, category storage and operational save payloads do not change. The sole changed existing executable file in the upload-ready repository is `deploy/extract_source.py`; it reconstructs and verifies the original 1.34.19 archive before applying the cumulative overlay.

The current live GitHub repository was not retrieved. Reconcile any changes made outside the supplied packages before overwriting them.

## Shipment catalogue: find, inspect, then open

Open **Fleet & vessels → Manifests**. The heading has a small **UI 06** badge.

The catalogue places compact stage views above the list: **All shipments, Open shipments, Drafts, Ready for dispatch, In transit, and To place**. Closed and Cancelled are also available within **Stage, route & sort**. These are views of existing saved states, not new workflow states or actions.

Search can match several words across the manifest number, title, route and displayed status. For example, two search terms can match a shipment number and its destination. Optional exact origin/destination filters and sorting stay under **Stage, route & sort**, with the active selections visible when collapsed. Sorting offers the existing saved order, manifest number, or earliest planned arrival; unplanned arrivals sort last. Sorting never changes saved dates or records.

Stage-button counts refer to accessible manifests before search/route filters. Views can overlap: a partially received shipment can have records still **In transit** and other records **To place**. Equipment figures are **inventory record counts, not summed stock quantities**. Draft and Ready show zero in transit until physical dispatch is recorded. Counts never certify readiness or grant permission.

### Desktop and mobile

On desktop, the shipment list sits beside a selected-shipment summary. Each card has its number, title, route, state, counts and a next-step explanation. Choose **View details** to inspect the summary, or the manifest-number link to open the saved record directly.

The summary brings together the recorded route, counts and **Open saved manifest**. It is read-only: opening or selecting a card does not dispatch, receive, cancel or close equipment. The saved record is fetched again before its current permitted actions appear. No old catalogue summary is submitted as a lifecycle change.

On screens at or below 900 pixels, selecting a card shows its detail instead of leaving the entire list stacked above it. **Back to shipments** returns to the same list context. Fleet's internal navigation uses a horizontal scrolling row on narrower screens; the main application's sidebar/menu remains unchanged.

### Return to the work you were doing

Opening a saved record from this catalogue provides a named return action such as **Back to shipment search**, **Back to filtered shipments**, or **Back to shipments**. Returning retains the catalogue search, stage, route, sort, selection and scroll context during the same authorised session.

A filter that hides the selected shipment clears that selection and its preview with a notice. An origin or destination no longer present in the accessible summaries is cleared deliberately. Empty results offer a clear route back to the unfiltered catalogue.

Refresh retains same-session choices but re-reads the accessible shipments. A failed read clears previous private information before Retry. Late responses are checked against the latest request, current route, navigation generation and current authorised session. Open forms block replacement of the record underneath the form.

These are page-memory preferences, not permanent navigation history or a new offline queue. This is a catalogue-to-manifest return trail, **not a universal trail connecting all Inventory, Assets, Tasks and Fleet screens**.

## Dispatch, cancellation and closure: review first

The saved-manifest actions now use a compact two-page guide:

**Saved shipment → Confirm action**

The first page shows the exact manifest, route, saved revision, intended action and its operational limits. **Review saved packing** expands the original complete shipment groups and included records. It starts collapsed so a long packing list does not obscure the action.

The second page repeats the action summary and requires the applicable note/reason, exact manifest number, and explicit review checkbox. Dispatch also retains its **actual UTC departure time** field. Going Back preserves entered notes/time but clears the confirmation and acknowledgement, so a revised review cannot reuse an old acceptance.

### Confirm actual dispatch

This records a physical departure of the saved groups, using the original dispatch service and its version/custody/full-box checks. A planned departure is not evidence that equipment has left. Merely opening the guide does not change inventory or mark a shipment In transit.

### Cancel before dispatch

Cancellation remains limited to Draft or Ready shipments. The manifest is retained as Cancelled; no receipt, return or physical movement is invented. Dispatched equipment must follow the appropriate receipt/return workflow rather than being cancelled through this form.

### Close reviewed manifest

Close is offered only when the existing permission is present, the manifest is received and no records are still awaiting final placement. The server remains the authority and checks again when saving. Equipment in holding must be placed before closure.

When the saved lines include damaged or returned records, the separate exceptions acknowledgement is required. **Closing does not release quarantine, verify stock, renew certificates, complete maintenance or authorise equipment use.**

### Saves and unfinished work

The lifecycle operation IDs, saved revisions, payload fields, original group roots and conflict/retry semantics are retained. The new presentation checkbox is local confirmation, not a new API field. Retrying an unchanged request after an uncertain response uses the existing duplicate-prevention path. A stale revision is rejected rather than silently refreshed and submitted.

These Fleet forms are online and page-memory-only; closing or reloading can lose unsubmitted wording. They do not acquire Inventory's separate saved-form store. UI05's movement, receipt and placement guide helpers remain unchanged. Existing receipt/placement and quarantine rules are not replaced by this update.

## Install the complete package with GitHub Desktop

1. Preserve unfinished work in every Wavelink tab and separate log window. Retain the previous approved GitHub commit and your established project backup. Update outside the client presentation. Do not clear browser storage.
2. In GitHub Desktop select the existing **wavelink** checkout. Fetch/pull the intended branch after preserving uncommitted edits.
3. Extract the ZIP and open **UPLOAD_TO_GITHUB**. Copy its **contents** into the local repository root, keeping the directory structure. Do not copy the enclosing folder, delete `.git`, or import the ZIP as an inventory.
4. Review the diff. Against the supplied UI05 repository, the only changed existing executable file is **deploy/extract_source.py**. Notes, tests and checksum records are separate. Stop and reconcile outside edits rather than overwriting them blindly.
5. Commit, **Push origin**, then deploy the approved commit through your existing Wavelink Render service. Keep the existing environment values, passwords, URL and persistent disk. In particular, keep **INITIALISE_FICTIONAL_DEMO=NO** and leave the initial administrator bootstrap password removed.
6. The build is designed to report:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 06: shipment browsing and status reviews; includes UI01-UI05; no automatic data changes.
```

7. After a healthy deployment, reload **Fleet & vessels → Manifests** and check **UI 06**. The core version stays **1.34.19**. Inventory and Receiving retain their preceding UI05 presentation. Preserve unsent work before closing/reopening older tabs to activate the updated service worker. Do not delete site data.

Normal administrator sign-in and the guest link use unchanged files. The ZIP contains no current live project, passwords or recovery keys. The original fictional seed remains only for authorised first provisioning; it is **not re-imported** during this update.

## Categories and existing records

No inventory upload, automatic assignment or reseeding is needed. Already-saved category choices remain in the hosted project. For the original demo categories that have not yet been applied, sign in as the named administrator and use:

**Inventory → DEMO Offshore equipment → Category: All categories → Manage categories → Preview demo categories → review and apply.**

Repeat in DEMO Consumables. The original unchanged examples propose 56 equipment records across 13 categories and 12 consumables across five categories. Existing choices, changed identities and additional records retain the UI03 protections. UI06 does not move or rename original documents.

## Rollback and recovery boundary

Revert the extractor commit and redeploy to return to the prior interface. The exact UI05 extractor is included in **REFERENCE_ONLY/Workspace_UI06/rollback/deploy/extract_source.py**. This keeps category support and does not reset the database.

Do not clear `/var/data`, re-import the project, or re-enable first provisioning to change the interface. Do not restore the original deployment ZIP over the working gateway/authentication fixes.

The supplied **ops/staging_recovery.py** helper is still pinned to pristine 1.34.19 and has not been accepted for this overlaid runtime. **Do not bypass its source check.** This UI release does not certify an overlaid-runtime backup/restore procedure, off-host recovery or production deployment.

## Acceptance on the actual hosted copy

After deployment, test the catalogue as administrator and restricted guest. Search/filter, inspect a saved record, return, and verify the correct account and selection. On a real phone check that Back returns to the list without horizontal page overflow and that the principal action is reachable.

Using expendable fictional equipment only, review dispatch without submitting, then cancel the form and confirm nothing changed. In a controlled scenario, record a dispatch, receipt and placement through their separate actions; inspect the unchanged equipment IDs and saved history. Confirm Close is not offered while equipment awaits placement. Review damaged/returned exceptions and ensure closure does not release quarantine.

Retest normal sign-in and the guest quick link before sharing with the client. A successful build or a hosting "Live" label does not establish all these acceptance results.

## Validation and evidence

See **DELIVERY_CHECKS.json**, **VALIDATION/** and the separate final ZIP verification for exact tests and limitations. Automated browser checks use local Chromium with the shipped application scripts/styles, fictional SQLite/TestClient services and controlled transport. Browser persistence is injected in memory, not a demonstrated durable IndexedDB/offline workflow. Previews are local actual application renders, not live Render or Windows captures.

Initial failed/incomplete development runs are kept separately from accepted runs. Repeated checks after packaging are not counted as additional distinct coverage. The full application regression suite, all inherited browser harnesses, Docker image build, live GitHub/Render deployment, physical devices, durable storage, off-host restore and complete assistive-technology acceptance were not performed.

### Completed local results

**320 distinct targeted Python cases passed**: 20 UI06 scope/structure cases, 205 inherited operational cases, 38 category cases and 57 deployment cases. Their 320 JUnit identities are unique; none failed, errored or skipped. One structural case also ran 23 pure JavaScript helper assertions, recorded separately rather than counted as extra Python cases.

**118 compound browser checks passed across eight harnesses**, including 18 new UI06 checks and 100 inherited checks. All 36 JavaScript files passed syntax checking; 428 runtime Python files and 13 upload-repository Python files parsed successfully.

An initial identical-source inherited regression run exceeded a 180-second runner allowance at 38 percent progress. A complete unchanged-source/unchanged-test rerun with a 900-second allowance passed all 205 cases in 334 seconds of pytest time. The incomplete run is retained and not counted. One early new-browser fixture used a future receipt timestamp; the service correctly refused it. Only the fictional fixture timestamp was corrected. Final application tests followed the last CSS polish; earlier snapshots/retakes are not added to the totals.

Final ZIP re-extraction and repeat checks are reported separately from these distinct totals.

## Continue from here

Inventory, boxes, manifests, movement/receiving and Record management remain the priority for actual hosted feedback. This pass completes another bounded part of that interface work; it does not declare it finished. Next, continue the remaining long forms and apply the same focused organisation to standalone checklists and maintenance. Original Files logical folders remain a separate pending feature. Wider hosting security, company isolation, verified recovery and vessel/cloud synchronisation remain separate work, not delivered by this UI patch.
