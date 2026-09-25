# Wavelink UI23 — write handover notes alongside the previous shift

**Core 1.34.19 · Workspace UI23 · Gateway G01 unchanged · 25 September 2026.**
Small changed-files update for the exact **UI22 + G01** repository from this chat,
on the supplied-UI18 → UI19 → UI20 → UI21 → UI22 lineage. Not a full repository
and not a project backup.

## What changed

Open a private handover and choose **Edit private draft → Work & priorities**,
or use **Continue my draft** for your saved daily shift.

The old section dropdown is replaced by visible, left-aligned section buttons:
Situation / summary; Work completed; Equipment / system status; Outstanding work /
issues; Hazards, restrictions and controls; Priorities for the incoming team;
Additional notes. **Previous section / Next section** moves through the same
sections without discarding your current wording. Your title, complete shift
period and stated time basis stay above the notes.

**Text present / No text** indicates only where wording exists—not completion,
approval or operational readiness. **Edited here** and the section count compare
with the private draft loaded when the form opened, not a fresh hub read. A new
unsaved handover has no saved comparison. The counter follows the existing
browser's 8,000-input-unit maximum; some characters such as emoji take two units.
Nothing is truncated, auto-inserted or automatically marked done.

## Read the previous shift without leaving your current notes

A daily draft created from an earlier shift offers **Read previous shift**.
It explicitly retrieves the exact published revision linked when this draft was
prepared. It appears beside the note editor on wide desktops and below it on
narrower layouts. Selecting a different note section changes the reference section
too. Your current wording stays separate and editable.

The reference shows only the earlier publication, never an author's newer private
working draft. It can be an older saved revision when a newer publication exists:
it deliberately does not switch to the latest one. Its publication time and
device-clock UTC retrieval time are labelled separately. This is historical
communication, not live equipment status.

**Refresh exact revision** clears the old reference and checks current access.
Missing, archived, mismatched, malformed or no-longer-permitted sources do not
fall through to another record. Failure leaves your current in-tab notes intact.
**Hide reference** clears that view; leaving Work & priorities clears it too.
Reading again after returning makes a fresh request. Delayed responses cannot
reopen a hidden view, overwrite a replacement form or display under a changed
account/session. An unrelated modal interruption requires an explicit refresh
after closing the modal; it does not freeze the editor.

New daily shifts without a predecessor and the separate full-hitch multi-source
preparation workflow do not invent a previous-shift reference. Their note editor
still gets the visible section buttons; existing multi-source links are unchanged.

## Saving is still explicit

The note view performs no automatic copying, save, publication, acknowledgement,
Task completion or evidence approval. It changes no audience or permission.

Use the existing **Audience / Review**, reason, confirmation and **Save private
hub draft** actions. Unsent wording remains **only in the open tab**, not a durable
offline draft. Switching note sections is not saving. Dirty Close protection,
conflict handling, the existing action IDs and unchanged-request retry remain.
A read-only source request does not discard or change draft confirmation; editing
your notes still clears confirmation.

All UI20 automatic shift schedules, UI21 day/resume/source selection and UI22
publication/acknowledgement guides remain included. Home stays UI13; Original Files
UI19. Handovers displays UI23. The working G01 public entry is untouched.

## Apply over the matching UI22 + G01 only

Preserve your approved commit, established complete project backup, outside edits
and unsent browser/separate-log work. From the extracted patch folder run:

```powershell
.\CHECK_UI23_UPDATE.ps1 -RepositoryPath "C:\path\to\wavelink" -Mode Baseline
```

This helper checks expected source hashes without copying files, changing accounts,
reading SQL, calling the network or resetting anything. Stop and reconcile a
mismatch. Only explicitly listed UTF-8 text files may differ by CRLF line endings.
It was not run on Windows here; the hash/CRLF contract is checked locally.

After a passing baseline check, copy the **contents of UPLOAD_TO_GITHUB into your
existing repository**, keeping the subfolders. Do not replace the repository,
delete files absent from the patch, or copy the enclosing folder as a subfolder.
Review the Git diff, commit and push using your established workflow. Run
`-Mode Installed` to check the resulting target.

No new tables, migrations, dependencies, environment variables or required deletions.
Only `deploy/extract_source.py` changes among existing executable repository files.
All 181 application Python modules and the G01 gateway/entrypoint are unchanged.

Keep `DEMO_PUBLIC_ENTRY=YES`, `INITIALISE_FICTIONAL_DEMO=NO`, the current domain,
required access password, matching non-admin guest credentials, persistent disk
and removed initial-administrator bootstrap. No project reset, demo re-import or
browser-storage clearing. Nothing was pushed to GitHub or deployed to Render here.

## Help and local checks

Handovers and Handover continuity Help are re-reviewed. Other 74 article bodies
are unchanged (their shared-reader cache URLs update outside the bodies).
All 76 search entries match their articles. Eight distinct topics have had a
bounded wording review; 68 plus native/master-PDF/entry-point work remain.

**378 selected Python tests passed** (287 application + 91 gateway/package),
along with **57 compound browser checks** (16 notes + 16 review + 13 board + 12
schedule) and syntax checks for **52 JavaScript files**. All 181 application
Python modules remain byte-identical to UI22. The 125 pure-Node checks overlap the
Python selection; they are not extra Python tests. The frozen derived runtime has
1,660 tracked files. Final ZIP replay and hashes are reported in the separate
compact verification report.

One real modal-interruption lock issue was found and fixed during development.
The original failed run and corrected fixture/report attempts are retained
separately, not counted as final passes. The same four historical release assertions
fail on untouched UI22; they remain explicitly excluded, not removed or passed.

Browser checks use the shipped assets, fictional TestClient API and injected
transport/in-memory storage. No live HTTPS, physical-device/Windows, durable
IndexedDB, service-worker lifecycle, full accessibility/security/isolation/load,
Docker, full-suite or off-host recovery acceptance is claimed. Measured section
button contrast/focus/layout checks are not a complete accessibility assessment.

Rollback through the exact approved UI22 + G01 source commit, not an older full
ZIP. Do not roll back data or re-enable initialization. The pristine-source
recovery helper remains unapproved for this overlaid runtime.

## Next

Hosted handover feedback remains first: real shift notes, named outgoing/incoming
authors, phone use and the unchanged save/publication flow. Continue the remaining
Help and module usability work after reported handover problems. The retained
larger roadmap, local-vessel/CCVD exclusion and parked vessel/cloud synchronization
are unchanged.
