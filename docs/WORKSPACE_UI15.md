# Wavelink — Workspace UI15

**Core 1.34.19 · cumulative UI01–UI15 · prepared 25 September 2026.** Built from the supplied complete UI14 package. Implemented and tested locally; no live GitHub fetch or Render deployment.

## Create maintenance for the exact inventory item

From **Inventory → open an item → Maintenance**, use the existing new-work-order action. The form now follows **Work & exact item → People & instructions → Due date & cycle → Review order**.

The item name, serial number and asset reference appear together. Item ID, model and recorded location are available in an identity disclosure; the final review includes the exact inventory item ID. These values come from the selected inventory record, not a typed equipment-name match. Missing identity data is labelled rather than invented. The link is fixed to that item; to select different equipment, preserve or discard the current draft deliberately and reopen the intended item.

Choose an available published routine explicitly; none is preselected. Review the work title, optional work-order reference, named assignees, instructions, optional UTC due time and one-off or recurring settings. A one-off order does not acquire a made-up due date or cycle. With no named assignees selected, the form explains the existing permitted-maintenance-worker semantics; it is not an assignment to every user and does not grant access.

The final page needs explicit fresh confirmation. Going back, editing values or resuming a draft requires another review. **Create linked work order** saves one open order with empty results through the existing service, then opens the saved work order after the shared draft writer finishes. Opening the form or moving between pages does not create an order.

**Keep draft & close**, discard, the existing draft kind/context, operation-ID retry protection and shared local writer are retained. Resuming re-reads the currently available routine directory, as the earlier asset form did; it does not freeze a published routine version in the local draft. Review the displayed revision again. After an uncertain response, check saved work before changing the request or routine and submitting again. A locally retained form is not a server-saved order, and a server backup does not include browser-only work.

The current view, account, project, token and dialog are checked during preparation and submission. A delayed preparation must not open this form over another operation. Existing server revision, permission, item-state and custody-related checks remain authoritative. Linking an item does not move it, confirm receipt, release quarantine or declare it ready to operate.

## Read the saved result and photographs without editing

Use the existing saved-step details/evidence action in an opened Maintenance work order. The **Saved readings & evidence** viewer now re-reads the saved work order and selected step before opening. It has three tabs:

- **Readings & notes:** the saved result, field labels/units and work note. A disclosure shows saved order/item identity. Unrecorded steps are explicitly identified.
- **Photographs:** submitted photographs attached to that result, with available caption, submitter, received time and stored SHA-256. Open a photograph larger without replacing the evidence viewer.
- **Approval:** the saved approval state, decision, reviewer, time, note and same-person indication where recorded. This is not an approval form.

The viewer shows result revision, saved time and retrieval time. It is a **saved snapshot**, not a continuously updating monitor or a browser-local draft viewer. **Refresh saved step** retrieves it again and discards the old display while loading. If refreshing fails, the prior readings are not left presented as current; a read-only retry is offered.

Photographs load when their tab opens, using fresh authorised requests rather than the shared gallery's previous successful cache. Each image must decode before it is shown as loaded. One unavailable image does not prevent trying the others. The loaded/submitted count distinguishes unavailable content from no submitted photos. Refresh retries the saved step and its photographs. Received times are hub timestamps, not verified camera-capture times; displaying a stored checksum is not an independent forensic authenticity assessment.

Arrow keys, Home and End move between tabs. The body scrolls separately from the close/refresh footer on narrow screens. Route/session/dialog guards discard late responses and block further scoped interactions after the initiating context changes. This is a focused guard on the changed paths, not a general security or offline-storage certification.

The viewer has no save, edit, approve, completion or automatic-queue action. **Viewing does not approve anything.** Use the separate authorised UI14 approval workflow. Step approval is not work-order completion, equipment readiness, quarantine release or permission to operate.

## Existing workflows and Help

Home remains **UI13**. UI14 approval and pending-follow-up-release guides remain intact; a successful follow-up review save can still retain a block instead of creating a successor. The existing UI11 general creation/step guide, UI12 close/cycle/stop guide, Inventory/boxes, Record management, shipments, receiving, Checklists, Tasks and other earlier changes remain included.

Maintenance Help is re-reviewed for the two UI15 paths and their actual save/read-only effects. The other **75 instructional article bodies remain unchanged**; all 76 topics retain the shared reader. There are still **four distinct bounded wording-reviewed articles**: daily, records, maintenance and dashboard. This repeat Maintenance review is not a fifth reviewed topic. Native Help, the original all-in-one reference and master PDF remain unchanged. Original Files logical-folder organisation remains pending; no original documents are moved.

## Update through the existing GitHub Desktop workflow

1. Preserve unsent Wavelink work in every browser and separate log window, outside repository edits, the previous approved commit and your established backup. Fetch/pull the intended branch in the existing checkout. Update outside a presentation.
2. Extract the complete ZIP. Copy the **contents of `UPLOAD_TO_GITHUB`** into the current repository root, retaining subfolders. Do not copy its enclosing folder, remove `.git` or upload `REFERENCE_ONLY`, `PREVIEWS` or `VALIDATION` as application files.
3. Review the diff, commit and push. Compared with the supplied complete UI14 upload repository, **only `deploy/extract_source.py` changes among existing executable files**. Release documentation and checksum manifests also change. Reconcile other edits before overwriting them.
4. Deploy the approved commit through the existing Render service. Keep the working domain, passwords, guest settings and persistent disk unchanged:

```text
PUBLIC_URL=https://demo.mywavelink.com
INITIALISE_FICTIONAL_DEMO=NO
```

Keep initial-admin bootstrap removed. Expected build output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 15: exact-item work orders and read-only saved evidence; includes UI01-UI14; no automatic data changes.
```

After a healthy deployment open an exact-item maintenance form or saved-evidence viewer and look for **UI 15**. Core remains **1.34.19** and Home still shows **UI13**. Preserve unsent work before closing/reopening old tabs for the service-worker update. **Do not clear site data, reset the project, re-import the demonstration or re-enable first-deploy initialization.** No inventory upload or automatic category application is required.

## Local validation

**453 selected Python cases and 140 compound browser checks passed**, with no failed/errored/skipped cases in those completed selections and no recorded browser errors. All **44 JavaScript files** passed syntax checks. The selected runs cover the new source/Help contracts, authorised linked creation and read-only evidence, maintenance approval/follow-up, Home, prior maintenance forms, inventory, Record management, shipments and related service/deployment contracts. Counts do not combine partial attempts or count repeats as extra distinct coverage.

The browser harness runs the actual shipped scripts/styles in local Chromium with temporary fictional databases and TestClient-backed HTTP. Browser persistence is injected in memory; this is not durable IndexedDB, service-worker lifecycle or physical-device acceptance. Preview images are local fictional renderings, not screenshots of the live custom domain. Test photographs are deliberately synthetic fixture images.

The first fresh-extraction browser repeat exposed a test sequencing race: it started another case before the saved order's destination finished rendering. The test now waits for that destination; the corrected complete run is counted. Application source was not changed to hide the failure. Earlier fixture/expectation corrections and interrupted/timeout runs are retained under development. Bounded broader browser-template/Task-checklist diagnostics did not complete and are excluded. They do not resolve the inherited incomplete-run question or establish its cause.

This release does **not** claim the full product suite, Docker image build, live GitHub/Render deployment, physical phones/Windows, durable browser storage, off-host restore, full accessibility, production security or multi-company isolation. Hosted availability does not imply vessel/cloud synchronisation.

## Operator acceptance and rollback

On the intended hosted service, check normal/guest entry and restricted roles; exact-item identity and real reviewed fictional creation; one-off/cycle/assignment settings; retained draft/retry behaviour; saved readings/photos/approval; unavailable evidence; Inventory/boxes/shipments and existing approval/closing workflows. Confirm identity and persistence through an intentional restart outside the presentation. Check real phones and intended desktop displays. Preserve work before exercising any recovery procedure.

Rollback by reverting the extractor commit or using the exact UI14 extractor in the full ZIP at **`REFERENCE_ONLY/Workspace_UI15/rollback/deploy/extract_source.py`** (not a file installed in the upload repository). Rollback is an interface change, not a database reset. The pristine-source recovery helper remains **unapproved for the overlaid runtime**; do not bypass its checks. Accepted overlay-compatible off-host recovery is separate work.

All **176 application Python files**, hosting/gateway/guest/supervisor files, Dockerfile, dependencies, vendor source parts/seed and recovery helper remain byte-identical to the supplied UI14 package. No new API, SQL format, authentication rule or browser database is introduced. This package is not a live-service backup and contains no current live database or passwords. Native vessel installations and the CCVD relay are outside this browser update.

Next: actual hosted Home/inventory/maintenance feedback; remaining detailed checklist forms; continued Help wording/entry-point review and Original Files logical folders, preserving original bytes, identity, links, permissions and audit. This is a development order, not an automatically running background task.
