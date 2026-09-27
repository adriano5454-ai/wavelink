# Wavelink UI43 — handover creation, day overview and combined PDF

**Core 1.34.19 · UI43 · working G01 unchanged · 26 September 2026.**
One grouped workflow update on the exact UI42 application repository. The hosted deployment
and the reported phone account were not inspected. Not a full source or project-data backup.

## Update with GitHub Desktop

Extract and copy **everything inside UPLOAD_TO_GITHUB into your existing UI42 application
repository folder**, replacing matching files. Review in GitHub Desktop, commit and Push origin;
deploy the intended commit through your established service. This is not the website repository.
Do not delete files absent from the patch or replace the entire repository. The optional
CHECK_UI43_UPDATE.ps1 only checks source hashes; it is not an installer or required upload.

Keep approved commit/complete backup, outside edits and unsent browser/separate-log work.
Preserve G01, DEMO_PUBLIC_ENTRY=YES, INITIALISE_FICTIONAL_DEMO=NO, required gate secret,
matching non-admin guest, named administrator, existing domain/disk and removed bootstrap.
No new environment settings, dependencies, database tables, migrations or permissions.
No reset, re-import or browser-storage clearing. Compatible evidence handling remains required.

## Create a daily handover with clear context

Use **Create handover → Daily / shift handover**. Department, subject/vessel/site label,
operational day, first start time, shift pattern and your shift are together. Current roster
hours are proposed when available, and can be changed for this one-off handover. The full
start/end dates show overnight boundaries: 06:00 produces 06–18/18–06 next day; 12:00 produces
12–00/00–12 next day. Other/custom complete 24-hour patterns remain available. Device Today
and saved time-basis labels do not perform an automatic ship-time/time-zone conversion.

**Who receives this handover?** selects named people and recipient departments. Searching
preserves hidden selections. The selected department is proposed for a new form; review it.
These people can receive the finished publication, not your private draft. Your signed-in
account remains the author; choosing a name is not creating a handover on someone else's behalf.

**People & shifts** is in the heading and the creation form. A named administrator or current
department head with existing create authority can assign eligible members to recurring shifts.
Open it from creation, save or return, and the one-off subject/period/recipients are retained.
Normal department members may select their own shift and recipients but cannot assign colleagues.
The public guest is not promoted. One-off creation never changes the recurring staff roster.

**Write handover** validates the proposal and opens the existing notes without creating a
record. Write, add optional photos/files and **Save & close** or **Finish handover** as before:
no routine reason, confirmation checkbox or new publication wizard. Each person keeps their own
notes. The same-day/shift duplicate guard reopens a matching existing handover instead of copying
it or rewriting its saved period/audience. Later membership changes can require a fresh proposal.

My assigned shift, Full-hitch handover, Prepare from previous and More actions → Manual /
irregular daily period remain available. Existing saved period/author/attachment boundaries remain.

## A day-by-day view for the same subject

Handovers now opens on **By day / subject**. Pick a subject to see all permitted saved days,
newest first. Expand a day or use **Jump to day**, then **Edit my notes** or **Read handover**.
Cards show author, shift, actual recorded period, summary preview and draft/published status.
Other people's private notes never appear; your own private corrections are clearly labelled.

A subject reuses the saved **department plus subject/vessel/site label**, not matching titles.
No separate project-topic IDs are added and no old labels are rewritten. Use the same label for
related entries. Other/full-hitch records without daily department metadata remain separate and
use their saved period-start date. Current department assignments are not historical crew records.

All dates is the default; Date range, All dates and Include archived deliberately change scope.
The retained **My shift** tab gives the familiar assigned-day cards and Continue saved notes.
Empty days are not invented or marked complete. Summary text is shortened; the reader/PDF is full.

## Export the subject in one PDF

Choose **Export N published handovers to PDF**. One PDF contains the entire selected subject/date
range, including collapsed days: chronological clickable index, complete notes, recorded periods,
authors, exact current revisions and permitted account acknowledgements. It is not restricted to
which cards are currently expanded. Private drafts/corrections are excluded; an existing published
version is used instead. Historical revisions remain in per-record history rather than duplicating
all versions into the journal. Handovers export permission is still required.

Attachment names, sizes and SHA-256 fingerprints are listed, not embedded files/photos. Visitor
signatures/drawn marks remain in the separate signing PDF. An author receives their acknowledgement
roster; another permitted reader receives their own acknowledgement view, not an expanded roster.

Maximum 200 current publications / 1.2 million section characters; larger exports are explicitly
refused and require a narrower range. The day view has an explicit 2000-record cap. No silent partial
report. Publication/evidence/access changes during export require refresh; no old PDF is released.
A downloaded copy cannot enforce later revoked access. Export does not sign, finish work or publish.

## One mobile acceptance session

With fictional data and a named lead, select Daily / shift handover on a phone. Choose department,
subject, 12-hour shift and a named recipient. Visit People & shifts and return to confirm choices
remain. Write notes and save privately, then Finish when ready. From a second permitted named
account, read that publication (not the other person's private notes). Return to the same subject,
expand another day and export one combined PDF. Check its date index and full text. Use disposable
data first. Existing account capabilities, not a public-guest role promotion, control assignments.

## Actual local checks and boundaries

568 selected Python tests (477 application + 91 gateway/package), 130 compound
Chromium checks, 11 actual loopback gateway/application checks and 70
JavaScript syntax checks passed. 190 Python modules parse; the final
runtime has 1776 tracked files. Two existing Python files change and two modules
are added; 186 existing Python files remain byte-identical.
All frozen-source results are in the verification report; final-ZIP repeats add no coverage.

Browser checks use actual application assets, fictional SQLite/TestClient and injected transport/
in-memory persistence. They are not full-suite, physical-phone/camera, real HTTPS/navigation,
durable IndexedDB/service-worker, Windows/PowerShell/native UI, full accessibility/security/load,
Docker or accepted off-host recovery results. Native installers were not rebuilt. Unsent text and
setup choices remain in-tab until saved. Nothing was pushed to GitHub or deployed to Render here.
