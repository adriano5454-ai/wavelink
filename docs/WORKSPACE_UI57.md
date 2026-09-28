# Wavelink UI57 — Shifts & people, and only your assigned shift

**Core 1.34.19 · UI57 · Company C01 and demo G01 preserved · 28 September 2026.**
A grouped handover coordination update for the exact current **UI56 + C01 + G01** repository.
This is an incremental source patch, not a complete repository or a live-company backup.

## Update through GitHub Desktop

Extract this ZIP. Copy **everything inside UPLOAD_TO_GITHUB into your existing UI56 Wavelink
application repository**, replace matching filenames, review in GitHub Desktop, commit and **Push
origin**. Keep the repository and its .git folder; do not delete files absent from the patch or
upload into the separate marketing-website repository. The PowerShell checker is optional read-only
checking, not an installer or required upload, and was not run on Windows here.

Preserve your approved commit, independent edits, established full backup and unsent main/separate-log
work. Sulmara and the demo may auto-deploy the same branch; review their settings before pushing.
Keep activated C01 company identity, PUBLIC_URL, dedicated disk/activation marker, INITIALISE_COMPANY=NO
and removed bootstrap secrets. Leave G01's separate demo credentials/domain/disk and existing
DEMO_PUBLIC_ENTRY=YES / INITIALISE_FICTIONAL_DEMO=NO configuration alone. No reset, re-import,
site-data clearing, repeated company setup or disabled synchronisation is required.

No new environment settings, dependencies, permission flags or database tables. Two authenticated
read-only endpoints project the existing department setup; its saved format and writers are unchanged.
A nonmatching or independently modified UI56 source must be reconciled rather than blindly overwritten.

## Set the department's shifts in one visible area

Open **Handovers → Shifts & people**. The existing **People & shifts** heading button also opens this
area. Cards show each available department, its configured shift names/hours and current assigned people.
A department without a saved setup has **Create shifts**; a configured one has **Edit shifts & people**.

The existing editor lets you set the subject/vessel/site, time basis, first start and shift names,
then assign existing eligible department members and **Save people & shifts**. Default two 12-hour
shifts; three 8-hour shifts, four 6-hour shifts and custom 24-hour patterns remain. Searching for a person
does not drop a hidden selection. No routine typed reason or separate review wizard is added.

This keeps the established authority: a project administrator or the current department head with
Handovers create permission can change that department's setup. Other members can see their department's
setup, but do not gain management rights. Administrators can coordinate available departments without
being automatically assigned to any shift themselves. People must first exist in the relevant department;
this workspace does not create accounts or grant permissions.

**View department handovers** opens the normal permitted day journal for that setup's department/site.
Private colleague drafts do not become shared. Several people can be in the same shift, but each keeps
their own handover. Earlier handover authors, periods, files, publications and signatures are not rewritten.

This is **one current cycle per department**, reusing existing data—not a new multiple-site roster,
rotation/leave planner, attendance tracker or historical crew roster. Existing setups are reused without
re-entering them. No records or assignments are seeded automatically.

## My shift means only the signed-in person's assignment

**My shift** now reads your current department memberships and saved shift assignment rather than the
last department selected on another board. It shows the resolved occurrence and only your matching
handover, not the department's other shifts or colleagues' records.

- **Open my notes** starts the existing editor without creating a record until you save.
- **Edit my notes** resumes your exact saved private draft.
- **Read my finished handover** opens your saved publication instead of making a duplicate.

The normal **Save & close / Finish handover**, optional notes/photos/files, exact-source links,
acknowledgement, correction and retry rules stay unchanged. A finished handover does not complete
outstanding work or prove physical attendance. A newer private correction is not shared automatically.

When you are unassigned, My shift says **No shift is assigned to your account**. It does not choose another
person's shift, the first department or all shifts because you are an administrator. Shifts & people and
My saved notes remain available to resolve setup or continue earlier work.

When you have more than one department assignment, a unique currently scheduled assignment is selected
only when all its clock bases can be resolved. Otherwise, choose from **your own assignments only**.
The team remains accessible separately through **By day / subject**, Shifts & people and Incoming.

## Overnight shifts and the operational date

For UTC or explicit fixed offsets such as **UTC+01:00** / **UTC-03:00**, the server selects your assigned
occurrence in progress, otherwise its next occurrence. At **02:00**, an assigned **18:00–06:00** shift
belongs to yesterday's operational day; a noon-start cycle handles the midnight boundary too. Full dates
are displayed. The badge **Scheduled now** describes the timetable, not whether a person is working.

Outside your hours the next assigned occurrence is labelled. Use **Another day of my assigned shift**
for a deliberate earlier/later operational day, or **My saved notes** for older work, one-off handovers and
records remaining after an assignment changes. Saved periods that differ from the current setup are
identified and reopened unchanged—not replaced or silently relabelled.

A descriptive basis such as **Ship local** is not treated as a verified time zone. My shift asks for the
operational day explicitly; its initial date suggestion is the device's date, not a verified ship clock.
An explicit fixed offset is not an automatic daylight-saving rule. Setup labels and older dates are not
changed to make a clock calculation succeed.

Assignments are checked on entry or Refresh and rechecked by the existing save/open services. The view
does not add a timer that navigates away from an editor when the clock reaches a boundary. Selecting another
day is a current-view preference, not a permanent change to the roster or saved notes.

## Stable reads, unchanged operational work

Unchanged assignment refreshes retain the displayed elements. Late responses after account, route, form
or intervening-dialog changes cannot replace newer work. A failed read disables stale opening actions;
Refresh checks again. Definitive denial clears the protected view even behind an open dialog, without
clearing that editor or unrelated stored work. No new autosave, queue or local-account vault is introduced.

The new endpoints are /api/handovers/simple/shifts and /api/handovers/simple/my-shift. They use the existing
project and named-account checks and return no-store responses. Read-only database comparisons confirm
that browsing shifts does not create a handover or alter assignments.

The existing simple/advanced handover writers, setup transaction, dates validation, duplicate protection,
attachments, signatures, subject journal/PDF, private drafts, UI55 quiet caching, sign-out and other approved
sections are preserved. This is not a native/Chrome launcher update. The prior old-icon/duplicate-window
request remains separate; don't uninstall, clear browser storage or close unsaved windows to address it.

## One practical acceptance session

Using fictional data and named lead/worker accounts, open Shifts & people and create two 12-hour shifts
for a department. Assign the accounts to different shifts. Each person's My shift should show only their
own assigned occurrence. Save notes, leave and return to resume the same record; Finish may have no notes.
Check the overnight date and the separate team journal. Check an unassigned test account receives the clear
setup message, not somebody else's shift. Use a phone during that same session. Test changed access or
discard only with disposable work, never valuable unsent data.

## Verification and limitations

**495 selected Python tests, 60 compound browser checks and 81 JavaScript syntax checks passed.** All 194 application Python modules parse; 192 existing modules remain unchanged. The frozen runtime has 1856 tracked files. Python groups: shifts_py=37, handovers_py=280, hosting_py=178. Browser groups: shifts_browser=19, certificates_browser=15, refresh_browser=26. These are selected checks, not full-suite or live deployment acceptance.

Tests use shipped assets and fictional SQLite/TestClient accounts, injected fetch/hash navigation and a
staged in-memory browser transaction store. They are not full-suite, live Sulmara/demo/Render/GitHub,
physical-phone, normal browser navigation, durable IndexedDB/service-worker, Windows/PowerShell/native,
full security/accessibility/load, Docker or accepted off-host recovery tests. The retained certificate and
shared-refresh browser suites were run; reports and real device clocks were not newly accepted.

Two actual UI57 entry issues were found and corrected before the final freeze: an unchanged response
invalidating its own button closure, and the initiating handover chooser's close event invalidating the new
assigned-shift read. Regression checks cover both. Earlier fixture errors and superseded complete runs are
kept separately and excluded. Final screenshots wait for the existing five-second toast to disappear. No unrelated historic failure
is claimed fixed. The package report verifies the delivered repository and fresh runtime separately.

**Nothing has been pushed or deployed from here.** Keep compatible C01/UI34+ company/evidence software and
UI56 certificate behaviour. Source rollback cannot recover deliberately discarded local work. Resume the
agreed section-by-section review after this complete shift workflow is checked.
