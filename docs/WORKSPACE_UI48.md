# Wavelink UI48 — Checklists and stable background refresh

**Core 1.34.19 · UI48 · Company C01 and demo G01 retained · 27 September 2026.**
One approved Checklists/stability update over the exact UI47 + Company C01 repository. This is
not a full repository, live-project backup or deployment. Home and Tasks retain their approved layouts.

## Update using GitHub Desktop

Extract and copy **everything inside UPLOAD_TO_GITHUB into your existing UI47 application repository**,
replace matching files, review in GitHub Desktop, commit and **Push origin**. Do not replace the whole
repository or delete files absent from this patch. The optional CHECK_UI48_UPDATE.ps1 reads source hashes;
it is not an installer or required upload. Reconcile independently changed files before overwriting them.

The demo and Sulmara may both auto-deploy from the same branch. Review each service's settings and preserve
unsent work, backups, the approved commit and outside changes first. Keep COMPANY/C01 identity, activated
company disk/marker, public URL, INITIALISE_COMPANY=NO after activation and removed bootstrap secrets.
Keep G01 demo entry, current credentials and INITIALISE_FICTIONAL_DEMO=NO unchanged. No new environment
settings, dependencies, tables, permissions, API routes, browser storage version or migration is required.
No reset, re-import, site-data clearing or disabled synchronisation is needed.

## Background refresh should not take your place

The checklist catalogue, selected summary and stage reconcile changed elements instead of replacing every
card. An unchanged poll preserves the same cards, expanded notes, search/section/status choices and scroll
anchors. Empty outgoing queues no longer trigger redundant heartbeat/render cycles. Real saved updates
still arrive, and active result inputs are not overwritten. Existing version/conflict checks still govern
saving older work. A deliberate navigation or filtering out a record can legitimately reposition the view.

Home keeps its last authorised work rows and disclosure state while a same-account refresh is pending;
Checking is a small button state, not a replacement page. A transient failure labels the displayed overview
as last saved. Definitive denied access, a changed identity or mismatched data clears protected content.
A denied stage cannot be repainted from its cached snapshot. Retained local work is not discarded.

These fixes cover the reproduced catalogue/stage/Home refresh defects and the tested shared paths. They
are not a claim that every workspace, service-worker update or real deployment reload has been audited.
Polling, live delivery, session checks and participant coordination remain enabled. The approved Home and
Tasks designs, their writers, and the UI45 sign-out/local-work flow are preserved.

## Continue directly and reach the work sooner

Each saved card offers **Continue checklist**, or **View finalised checklist** after all stages are finalised.
The action enters that exact record's first unfinished stage; showing the card itself does not join a stage.
**Summary** remains alongside it with complete notes, saved metadata and individual stage links.

Compact phone headings, search and filters leave more room for actual records/checks. Type & sort, all
status views, section selection, Find next unfinished, Record tools, Help and source instructions remain.
Extra count explanations sit after the results rather than pushing every check below the first screen.
No filter reduces finalisation requirements. Warnings for genuine unsent or unavailable work stay visible.

## Record one result on one page

Open an item: wording and guidance, result, readings, notes and photographs are together, followed by
**Save check**. No routine Next/Back sequence or review checkbox. This is an explicit result save, not
one-click auto-completion. Completed needs its required readings and numeric limits; Issue and N/A need
useful notes. Required evidence, five-photo limit, JPEG/PNG preparation and captions remain unchanged.

**Last known saved result & identity** retains the original snapshot context, not a fresh online check.
A resumed draft retains its original item version. **Keep draft & close**, ordinary draft-preserving Close,
explicit Discard draft, queued delivery and conflict review keep their existing behaviour. Saving queues
the proposal; check Connection & saves for hub acknowledgement. It does not approve, mark your device ready
or finalise the stage. Required photos and active saves must settle before ordinary closing.

## Finishing remains an explicit, separate decision

**Finish & devices** shows unfinished saved checks, outstanding assigned approvals, local work on this
device and participating devices not ready. These are last-displayed values, not authority to finalise.
The server independently checks the current whole stage, required evidence and participating devices.

Assigned item approval, **Done on this device**, Resume editing and **Finalise stage** retain their existing
review/confirmation and access rules. Device readiness does not complete items or represent a crew roster.
Finalised stages stay locked; finalising Before does not finalise After or authorise equipment operation.

## Builders and complete PDF evidence

**Create / import template** and the template-library shortcut use the existing saved checklist-builder
permission, not an administrator role test. They open Setup & builders, separate from New checklist/run.
Non-admin builders receive no administrator record-management access and no automatic new permissions.

PDF pagination uses available space, more compact result tables and photo headings kept with their first
image. Notes, readings, approvals, finalisation receipt, exact photo bytes/fingerprints, original annotations
and recorded history are retained. The same fictional five-check/one-photo sample is **four pages instead
of six**, with matching complete body-word counts and image checksum (only publisher wording changes).
This is an example, not a fixed page count for other records. Unavailable/corrupt evidence still refuses export.
The publisher wording is role-neutral. This remains a per-record PDF, not a new combined checklist journal.

## One acceptance session

With fictional data, use a published checklist containing a required reading, photo and assigned approval.
Open its Summary, expand notes and stay lower down through several automatic cycles. Continue directly,
record/keep/resume a result, submit evidence and have the assigned person review it. Mark participating
devices ready, explicitly finalise and export. Repeat a background cycle while another named user saves a
real change; the changed row should update without taking your place. Check Home and Tasks during the same
phone/desktop session. Do not use valuable offline work for destructive conflict or discard testing.

## Verification and boundaries

**775 selected Python tests, 100 compound browser checks, 74 JavaScript syntax checks and
193 application Python parses** completed. The final archive reproduces **1813 tracked runtime files**.
The report identifies the exact commands, completed counts, source hashes and excluded preliminary runs.

The new checks exercise actual shipped scripts and actual local fictional TestClient services, captured
real polling callbacks, controlled HTTP failures and staged in-memory transactions. Normal browser navigation
is restricted here; hash fixtures were used, not a policy bypass. No live Sulmara/GitHub/Render, physical
phone/camera, durable IndexedDB, service-worker lifecycle, Windows/PowerShell/native binary, full-suite,
full security/accessibility/load, Docker or accepted off-host recovery result is claimed. Existing historical
failures outside the selected tests are not declared fixed. Native/master-guide PDFs were not rebuilt.

Only app/pdf_export.py changes among existing application Python files; 192 others are unchanged.
Shared frontend read/render code changes are audited; operational queue/result validation, approval,
readiness/finalisation service rules and C01/G01 hosting remain. Two Help article bodies and outlines update;
74 others are unchanged apart from shared asset cache URLs. All 76 catalogue entries match.

Rollback through approved compatible UI47+C01 source restores the former checklist UI/refresh behaviour,
not deleted local entries. Never roll data back or use incompatible pre-C01/pre-UI34 writers/exporters.
**Nothing has been pushed or deployed from here.**

### Test-run accounting

The first new Checklist run had one test-only source-literal expectation failure; the corrected complete
50-case run passed. The first broad retained Tasks run hit its 540-second execution bound and is excluded;
the complete 282-case retry passed with a longer bound. Application files remained byte-identical during
the test-literal correction and these retries. Other completed shards use those same frozen application
bytes. Final-ZIP gateway repeats are verification of the delivered archive, not extra unique coverage.
Neither a timeout nor its successful repeat establishes the cause of the earlier incomplete run.
