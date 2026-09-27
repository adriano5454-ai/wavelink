# Wavelink UI33 — people, handover files and fewer routine reasons

**Core 1.34.19 · UI33 · working G01 unchanged · 26 September 2026.**
A compact changed-files update for the exact UI32 + G01 repository from this chat,
based on your actual uploaded application repository. Not a complete source repository
or live-project backup. Nothing was deployed from here.

## Update using GitHub Desktop

Preserve your complete project backup, approved commit and unsent work. Extract the ZIP;
copy **everything inside UPLOAD_TO_GITHUB into your existing Wavelink application repository
folder**, replacing matching filenames. Review in GitHub Desktop, commit, and **Push origin**.
Deploy the intended commit through your existing service workflow.

Do not replace the whole repository or delete files absent from this patch. The optional
CHECK_UI33_UPDATE.ps1 is a read-only baseline/installed checker, not an installer or a
required extra upload. Reconcile independent source changes rather than overwriting them.

No new environment variables, dependencies, tables or required deletions. Keep
**DEMO_PUBLIC_ENTRY=YES**, **INITIALISE_FICTIONAL_DEMO=NO**, your gate secret, matching
non-admin guest credentials, named administrator, domain, persistent disk and removed
bootstrap unchanged. Do not reset, re-import or clear browser storage.

**Compatibility:** after saving handover attachments, keep UI33 or later. This adds a
handover file owner kind and exact publication references to existing tables/JSON.
An older source rollback may omit attachment handling or refuse selective exports.
Do not use UI32/older writers or exporters for this new data, delete rows or reset the
project to bypass that. Preserve your backup and use an attachment-aware reviewed repair.
Normal application updates preserve existing handovers without re-importing them.

## People & shifts: assign the team once

Open **Handovers → My shift → select department → People & shifts** using a named
administrator or the current department head with Handovers creation permission.
Existing eligible department members have a shift selector; several people can share
a shift, but everyone keeps their own notes. A person needs Handovers create permission
to be assigned. This is not a create-user screen and never grants account permissions.

Search by name/login and filter by shift or unassigned members. Filtering does not
remove hidden choices. **Save people & shifts** saves the assignments without a reason.
Saved hours and vessel/site are under **Shift hours & vessel / site**; a new setup opens
those fields automatically. Existing 12-hour defaults/custom schedules are unchanged.

For accounts without setup authority, the button remains visible but disabled with an
explanation. The demo guest may lack that authority; no live guest settings were inspected.
Do not turn the public guest into Administrator to reveal a feature.

## Add a photo or file to the notes—one save, not another upload workflow

In simple daily notes, use **Add photo / file**, or **Take photo** on a supported phone.
The camera input may open a picker instead on devices/browsers without direct capture.
Camera behavior has not been tested on physical phones here.

A preview/list appears in **Photos & files**. Remove or Undo removal changes only the
open form. Choose **Save & close** to save notes and files privately, or **Finish handover**
to save the notes/files and first publication together. There is no separate upload or
extra confirmation screen. A failed save rolls back the whole transaction; an uncertain
response retains the same request for retry rather than duplicating the handover/files.

Limits: **six files, 5 MB per file, 10 MB combined**. Supported: JPEG/PNG, PDF, DOCX,
XLSX, UTF-8 TXT and CSV. Export HEIC as JPEG first. Files are format-checked, not scanned
for malware; use trusted files. Original bytes and photo metadata are retained, without
automatic compression or EXIF removal.

Your private files stay with your personal draft. A permitted reader receives only the
files attached to the exact published revision. **Read previous shift** can display that
publication's files without copying them into your new notes or acknowledging anything.
The ordinary saved reader and publication review display the exact saved file list.

Adding/removing files in a later correction does not rewrite earlier publications.
Removing a draft link does not purge its stored bytes or history. Full backups and
Handovers-selected component exports retain the data; excluding Handovers removes its
file data from that exported snapshot. Disk usage grows with retained files; no retention
purge or quota manager is introduced. Private filenames can be included in approved full
project backups just like private notes.

The handover PDF lists attached filenames, sizes and recorded SHA-256 fingerprints.
**The PDF does not embed the files**; open the permitted saved publication to download them.
Preparing a handover from historical notes does not automatically copy attachments.

**Unsent notes and selected local files remain in the open tab until saved.** This is not
autosave or durable offline drafting. Keep an uncertain save open for its exact retry.
Existing publication corrections still require the separate change-summary review.

## Fewer routine reasons: first cross-module batch

Routine **Task work notes**, **inventory item-detail edits**, **asset-profile edits** and
**asset-photo caption changes** now accept an empty reason. The browser's Task work,
inventory-item and asset-profile forms no longer show a required reason field. Real
actor, timestamp, version and before/after changes remain in the existing audit trail;
no invented user explanation is inserted.

This does not remove permissions, conflicts, custody rules or every review control.
Task return/rejection/cancellation/reopening, destructive actions, equipment movements
and corrections to issued handovers retain their separate rules. Existing item/profile
review controls remain. The rest of the program and native dialogs still need a bounded
reason-prompt/usability audit; this is not a completed program-wide cleanup.

## Preserved and tested

Automatic shifts and UI32 saved-draft/old-site overview remain. G01, transient project
presence, Documents → Original files, approved website icons and support@mywavelink.com
are unchanged. No native Windows executable/installer or mailbox was rebuilt/tested.

**417 selected Python tests** (326 application + 91 gateway/package),
**95 compound Chromium checks**, **60 JavaScript syntax checks**
and **184 Python parses** passed on frozen source.
The runtime has 1,715 verified tracked files. This includes real fictional
SQLite/API transactions, private versus published file access, lost-response retry,
large-file request limits, local backup/restore, component exclusion, assignment and
routine edit forms, alongside the retained simple handovers/presence/Originals/contact checks.

Browser tests use shipped assets, TestClient-backed fictional APIs and controlled transport/
in-memory storage through set_content. No full-suite, live-service, physical-device,
Windows/PowerShell, durable IndexedDB/service-worker, complete security/accessibility/load,
Docker or accepted off-host recovery result is claimed. Earlier historical release assertions
were not selected or declared fixed. Evidence is separate; partial/preliminary attempts do
not count as final passes. Nothing was pushed to GitHub or deployed to Render here.

## Next

Keep the simple daily workflow. Prioritise actual surveyor feedback on people assignments,
phone photos/files, save/finish and exact published files. Continue removing routine reason
prompts in coherent module groups without weakening exceptional corrections or approvals.
The wider roadmap is retained in docs/DEVELOPMENT_TODO.md. No automatic background work.
