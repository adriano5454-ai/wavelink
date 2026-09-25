# Wavelink — Workspace UI17

**Core 1.34.19 · cumulative UI01–UI17 · prepared 25 September 2026.** This complete package continues from the supplied Full UI16 archive. Implemented and tested locally; no live GitHub repository was fetched and no Render deployment was performed.

## Review a standalone checklist item

The existing item approval action now follows **Saved result & evidence → Decision & note → Confirm review**.

The form reads the current saved record and authorised account before showing the exact checklist, stage, item, readings, checker, note and assigned reviewer. Expand **Saved review identity & timing** for record identity, revisions and UTC retrieval times. This is a fresh saved snapshot, not continuously refreshed proof of the current state.

Submitted photographs are requested afresh through the existing authorised endpoint and decoded before being shown. The viewer distinguishes a submitted photograph that cannot be loaded from a result with no submitted photographs. It reports the available/submitted count and opens an enlarged image separately. All submitted photographs must be viewable before either review decision. Required-but-missing evidence still blocks approval. Received timestamps are hub timestamps, not verified camera capture times.

Choose **Approve checked item** or **Request changes** explicitly; neither is preselected. Request changes requires a note. A designated reviewer who also checked the item can still perform the existing permitted self-review, but the form says that this is not an independent second-person review. Administrator status is not an approval override.

The final page summarises the exact proposed decision and requires confirmation. Back, editing or refreshing resets confirmation. Saving uses the existing operation ID and item-revision payload; the hub independently rechecks permissions and saved state. A decision resets stage readiness and does not finalise the stage.

**Review notes are not local drafts and are not queued offline.** Refresh keeps the note only in the open form while clearing its decision. Closing an unsaved nonempty note asks before discarding it. Preserve unfinished notes before leaving or replacing the page.

## Mark this device ready

The existing **Done on this device** action now follows **Saved stage & this device → Confirm readiness**.

It shows the saved stage counts, signed-in person, exact device ID, stage revision and reported unsent-work count. The review uses the existing stage heartbeat, so opening or refreshing this guide can register/update this device's participation; that heartbeat is not a readiness or finalisation action.

Readiness means this device has finished its contribution for the saved revision. It does not complete checks, approve results, mark another device ready or finalise the stage. **Unfinished saved checks do not by themselves prevent this device being marked ready.** Local drafts, queued work and conflicts retain their existing gate. Already-ready devices use the separate existing **Resume editing** action to change answers.

## Finalise the saved stage

The existing finalisation action now follows **Saved checks & N/A → Participating devices → Confirm finalisation**.

Review saved counters, outstanding checks, N/A reasons and required approval rows. Missing/invalid counters are shown as unavailable, not zero. The next page lists every participating device returned for this stage, including identity, online status at the saved snapshot, reported pending work and readiness revision. This is not a complete crew roster or a count of all offline browser installations.

Known blockers are listed and prevent submission: unfinished checks, outstanding approvals, missing counts, a required earlier stage that is not finalised, missing own-device participation, or participants not online/synchronised/ready for the saved revision. A **No listed blocker** result is preliminary and applies only to that snapshot. The hub independently validates current saved answers, evidence, permissions and device readiness on submission.

The final explicit confirmation calls the existing finalisation endpoint and saves the existing receipt. **Finalisation locks the whole selected stage; it does not just close a form.** A checklist decision/readiness/finalisation is not an authorisation to launch or use equipment. Follow the approved project and manufacturer procedures.

## Interrupted requests and saved outcomes

These forms capture the record, stage, account, token, route, device and exact open form. A changed scope or new local work prevents a new submission, including a check after asynchronous lease renewal. Ordinary Close/Escape and duplicate submit are blocked while an explicit save is in progress. Old reads and responses do not replace a different open form.

An action already sent can still complete even after the user changes context; the safeguards do not cancel a completed server write. A refusal clears confirmation and requires a refreshed review. A lost response is reported as an unconfirmed outcome, not proof that nothing saved. No automatic offline retry is added. When the hub confirms a write but local snapshot persistence fails, the form says the hub saved it and warns **Do not resubmit**. Check the existing save-status strip and refresh the saved record.

## Earlier workflows and Help

The UI16 standalone result editor, draft/queue/conflict behavior and photo editor remain unchanged. Home stays UI13, the stage workspace stays UI09, and these three review forms show UI17. Earlier maintenance guides, exact-item creation, saved-evidence viewer, inventory, boxes, shipment and receiving improvements remain included. Task-owned checklists are not redesigned by this increment.

Daily checks Help is re-reviewed for these flows; its outline and full-text search are updated. The other **75 instructional article bodies remain unchanged**, with shared reader cache references advanced. There are still four distinct bounded wording-reviewed topics: daily, records, maintenance and dashboard. This is not completion of all Help, entry-point, native or master-PDF review. Original Files logical folders remain pending; no original document bytes or links are moved.

All **176 application Python files** match UI16 byte-for-byte. Only **deploy/extract_source.py** changes among existing executable upload-repository files. Incremental runtime changes are browser assets. The shared API wrapper gains an optional post-lease scope hook for these new calls; all existing callers omit it. The server, payloads, permissions, SQL, shared journal, queues, synchronisation, local storage formats, hosting, gateway, guest bootstrap, supervisor, Docker, dependencies, vendor source parts, seed and recovery helper remain unchanged.

## Install through the existing checkout

1. Preserve unfinished work in every browser and separate log window, retain your approved previous commit and established backup, and preserve outside/uncommitted edits. Fetch/pull the intended branch in your existing Wavelink checkout. Deploy outside a presentation.
2. Extract the full ZIP and copy the **contents of UPLOAD_TO_GITHUB** into the repository root, preserving subfolders and `.git`. Do not upload the enclosing folder, REFERENCE_ONLY, PREVIEWS or VALIDATION as application files.
3. Review the diff, commit and push. Reconcile outside edits rather than blindly overwriting them. Only the extractor changes among existing executable files compared with the supplied Full UI16 tree.
4. Deploy the approved commit through the existing Wavelink Render service, retaining the domain, current passwords, guest settings and persistent disk:

```text
PUBLIC_URL=https://demo.mywavelink.com
INITIALISE_FICTIONAL_DEMO=NO
```

Keep the initial-admin bootstrap setting removed. Expected build output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 17: guided checklist approvals, device readiness and finalisation; includes UI01-UI16; no automatic data changes.
```

Preserve unsent work before closing/reopening old tabs for the service-worker update. Check UI17 inside the new review forms, not Home's older badge. **Do not reset the project, re-import the demo, clear browser/site data or enable first-deploy initialization.** An interface update requires no equipment upload or category reset. A server backup does not include browser-only unfinished work.

## Acceptance and rollback

Check normal and guest entry, permitted and unassigned reviewers, required/missing photographs, approval and Request changes, unfinished-but-ready device behavior, peer offline/not-ready refusal and one actual fictional finalisation. Recheck result editing, drafts, Home, Tasks, Maintenance, Inventory, boxes and receiving. Verify identities and persistent data through a deliberate restart outside presentations. Real phones/Windows, service-worker lifecycle and durable local work still require operator acceptance.

Revert the approved extractor commit or use the exact UI16 extractor in **REFERENCE_ONLY/Workspace_UI17/rollback/deploy/extract_source.py**. Never reset the project/disk or re-enable initialization to roll back the interface.

The pristine-source recovery helper remains **unapproved for overlaid runtime**. Do not bypass its checks. This package contains no live database or live secrets and is not a live-service backup. Overlay-compatible off-host recovery is separate acceptance work. Native vessel installation, CCVD and vessel/cloud synchronisation are outside this update.

## Local validation

**730 selected Python tests, 245 compound browser checks and syntax checks for all 46 JavaScript files passed** in the completed final runs. Counts exclude repeats and partial/development attempts. Final archive byte verification and fresh-extraction equivalence are recorded separately in Wavelink_UI17_Final_ZIP_Verification.json.

The browser checks use actual shipped scripts/styles in local Chromium, TestClient-backed HTTP, temporary fictional databases, synthetic photographs and injected in-memory browser persistence. Screenshots are actual local renders, not hosted-domain screenshots or physical-phone captures. All 76 Help routes were checked with Tk imports blocked during requests; this is not a fully desktop-import-blocked application startup test.

The selected template and Task-checklist groups completed cleanly in this release's final runs (49 and 47 cases). Earlier incomplete attempts are historical, excluded from these totals, and their causes are not inferred.

The full product suite, Docker build, live deployment, physical devices, durable browser storage, service-worker lifecycle, off-host restoration, production security, multi-company isolation and complete accessibility acceptance are **not claimed**. Development fixture/orchestration findings and excluded attempts are retained under VALIDATION, separately from the completed final evidence.

Next: hosted Home/inventory/maintenance/checklist feedback, continuing Help wording and entry-point review, and Original Files logical-folder design preserving file bytes, identity, references, permissions and audit. This roadmap is not an automatic background task.
