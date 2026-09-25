# Wavelink — Workspace UI16

**Core 1.34.19 · cumulative UI01–UI16 · prepared 25 September 2026.** Built from the supplied complete UI15 archive, not a fetched live repository. Implemented and tested locally; no Render deployment has been performed.

## Guided standalone checklist results

The existing action for recording or editing a check now opens **Record checklist result** with three pages:

**Result & readings → Notes & photos → Review check**

The first page identifies the exact checklist, stage, check and instruction group. Expand **Record identity & last known result** for record ID, checklist revision, the last known saved author/time and item revision. Instructions and reference pictures remain available. The result starts from the action selected, the existing result or a retained local draft; opening the form does not complete anything.

Required readings and recorded numeric limits are displayed beside the fields. Existing validation remains authoritative. The second page holds the reason/notes and the existing photo editor. Issue and Not applicable require a reason. Photo-off, required-photo, photo-count, format and size rules remain the existing rules; instructional reference images do not count as submitted evidence.

The final page compares **Last known hub result** with **Proposed result on this device**: result, readings, notes and photograph counts. Proposed photo captions distinguish new local photos from previously attached photos. Review the actual images on Notes & photos; a count or caption is not an image-content check. An approval-rule reminder keeps result recording distinct from approval.

**Last known hub result is the saved snapshot already held by this browser, not a fresh server read.** Another device may have newer work. The review displays the retained draft's base revision and the last known item revision. An older base is not silently replaced; the existing conflict review still applies. A snapshot change observed while reviewing invalidates the confirmation.

An explicit, unnamed confirmation is required before **Save check on this device**. It is not saved in the draft or sent to the service. Going Back, editing values or photo captions, adding/removing photos or resuming a draft requires a fresh review. Enter on an earlier page advances the guide instead of submitting the result.

## Local drafts, queued work and saved hub results stay distinct

**Keep draft & close** saves the existing local draft without queueing the check. Edited input continues to use the existing draft store. Ordinary Close or Escape retains already edited local work; opening and closing an untouched form need not create a draft. The footer distinguishes draft-saving, local confirmation and storage failure. A storage warning means preserve the open form and work; it is not a guarantee of durable browser storage.

**Discard draft** has a separate confirmation. It removes that retained editor draft only; it does not remove a previously queued check or the saved hub result. The local draft is restored in memory when its deletion cannot be persisted.

**Save check on this device** passes the same result envelope and base revision to the existing queue and synchronisation service. An offline save is a queued proposal, not a completed hub transaction. Use the existing save-status strip and unsent-work review to see hub acknowledgement or conflicts. No approval, device-ready or stage-finalisation request is sent by this editor.

The save/write functions, operation IDs, conflict workflow, photo wire encoding, compression and shared local-store formats are unchanged. Existing service permission, locking and approval rules are not relaxed.

## Interrupted editing and photo preparation

The changed result-editor path checks the initiating record, stage, route, account/session and exact form before its actions. A retained draft owned by another account is not opened for editing by the current account. A late response must not close or cover a replacement operational form.

Photo preparation blocks ordinary Close, Escape and competing form actions until attachment preparation finishes. A photo finishing after the initiating context changes is not attached to another form or account; a message tells the user that the new preparation was interrupted. Earlier retained local work is not automatically deleted. The photo viewer's optional activity guard prevents a delayed enlargement from covering a replacement dialog. Existing successful-photo caching remains unchanged here; this editor is not the separate UI15 fresh-read evidence viewer.

A delayed close event from an earlier dialog is ignored while a new dialog is open, preserving the new form's photo/save protection. This was exercised explicitly in the local tests. These guards do not constitute full offline/durable-storage or browser-lifecycle acceptance.

## Desktop and phone-sized layout

Wide views use grouped readings and a side-by-side result comparison. Narrow views stack those panels, scroll within the form and keep Back/Continue, local-save status and draft/save actions reachable. Local Chromium checks cover 390 px and 320 px for this form. Packaged previews are actual local rendering with fictional records and synthetic test photographs, not live-domain or physical-phone screenshots.

The changed editor shows **UI16**. Home remains **UI13**, the standalone stage workspace retains **UI09**, and the UI14 approval/follow-up and UI15 maintenance/evidence forms remain included. Different module badges do not mean earlier improvements were removed.

## Help and unfinished work

The **Daily checks** article is re-reviewed for the three pages, snapshot/queue distinction, retained drafts, required evidence, conflicts and separate approvals/finalisation. Its outline and search catalogue match. The other **75 instructional article bodies are unchanged**; shared Help cache references advance.

There remain **four distinct bounded wording-reviewed topics**: daily, records, maintenance and dashboard. This is another review of Daily checks, not a fifth topic or completion of the remaining Help library. Native Help, the original reference and master PDF are unchanged. Original Files logical folders and the remaining standalone approval/readiness/finalisation form review are not implemented by this release.

## Update the existing checkout

1. Preserve unfinished work in all browsers and separate log windows, your established backup and the previous approved commit. Preserve uncommitted edits, then use the intended branch of the existing Wavelink checkout. Deploy outside a demonstration.
2. Extract the full ZIP. Copy the **contents of UPLOAD_TO_GITHUB** into the repository root, preserving its subfolders and `.git`. Do not upload REFERENCE_ONLY, PREVIEWS or VALIDATION as application files.
3. Review the diff, commit and push. Against the supplied UI15 upload tree, **deploy/extract_source.py is the only changed existing executable file**. Documentation and checksums also change. Reconcile outside changes before overwriting them.
4. Deploy the approved commit through the existing service, keeping its current passwords, guest configuration and persistent disk. Preserve:

```text
PUBLIC_URL=https://demo.mywavelink.com
INITIALISE_FICTIONAL_DEMO=NO
```

Keep the initial-admin bootstrap setting removed. Expected extraction output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 16: guided standalone checklist results and reviewed Daily checks Help; includes UI01-UI15; no automatic data changes.
```

After a healthy deployment, preserve unsent work before reopening an older tab for the service-worker update. Open an editable standalone checklist item and look for the UI16 three-page form. **Do not clear site data, reset the project, re-import the demo or change domains.** No inventory upload, recategorisation, new project or initialization is required.

## Rollback and acceptance

Retain the previous approved commit. The exact UI15 extractor is included in the full ZIP at **REFERENCE_ONLY/Workspace_UI16/rollback/deploy/extract_source.py**; it is not installed in the upload repository. Revert the extractor change to roll back the interface. Do not reset the persistent project or turn initialization back on.

Check normal/guest entry, permitted and restricted result editing, retained drafts, required readings/photos, actual reviewed save and hub acknowledgement, approval separation and the remaining stage lifecycle with fictional data. Check Inventory, shipments/receiving, Home, Maintenance and the UI15 evidence viewer. Test slow/interrupted connection behaviour and persistence after a deliberate restart outside the presentation, on real phones and desktop displays.

All **176 application Python files** remain byte-identical to UI15. Hosting, gateway, login/guest bootstrap, supervisor, Dockerfile, dependencies, vendor source parts, demonstration seed and recovery helper are unchanged. The incremental application changes are browser resources only. The full cumulative overlay also retains earlier approved backend changes; it is not a pristine original-source runtime.

The original recovery helper remains pinned to pristine source and **unapproved for the overlay runtime**. Do not bypass its checks. No live database, password or current service backup is included. Native vessel installations, CCVD and vessel/cloud synchronisation remain separate work.

## Local validation

**729 selected Python cases, 206 compound browser checks and all 45 JavaScript syntax checks passed** in completed final runs. Tests use the shipped scripts/styles, local Chromium, temporary fictional databases and TestClient-backed HTTP. Browser persistence is injected in memory. Final source and extractor hashes are fixed; fresh extraction from the final ZIP is compared with the tested runtime.

The previously incomplete template and Task-checklist groups completed cleanly in the final selected runs (49 and 47 cases respectively). Their earlier time-limited attempts remain excluded; no cause for prior incomplete runs is inferred.

Preliminary interrupted runs and fixture/test corrections are retained separately and excluded from final totals. Repeated checks are not additional distinct coverage. See VALIDATION/RESULTS.json and VALIDATION/DEVELOPMENT_FINDINGS.md. The external Wavelink_UI16_Final_ZIP_Verification.json records final archive hashes and extraction verification.

This is **not** the full product suite, Docker build, live GitHub/Render, physical-device, durable-storage/service-worker-lifecycle, off-host recovery, production-security, multi-company isolation or full-accessibility acceptance. No automatic background development or deployment is running.
