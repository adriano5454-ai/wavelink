# Wavelink UI47 — Tasks from assignment to review

**Core 1.34.19 · UI47 · Company C01 and demo G01 retained · 27 September 2026.**
One complete Tasks update on the verified UI46 + C01 source, following the approved Tasks review.
The approved Home is unchanged. This is a changed-files update, not a complete repository or company backup.

## Update with GitHub Desktop

Extract the ZIP. Copy **everything inside UPLOAD_TO_GITHUB into your existing UI46 application
repository folder**, replacing matching files. Review in GitHub Desktop, commit and Push origin.
Do not replace the repository or delete files absent from this patch. Not the Wavelink-Website repository.
CHECK_UI47_UPDATE.ps1 is an optional read-only source checker, not an installer or required upload.

The demo and Sulmara can use the same branch; check their auto-deploy settings and deploy an approved
commit deliberately. Preserve a complete backup, your approved commit, outside edits and unsent work.
C01 company identity, activated dedicated disk, activation marker and normal login remain unchanged.
After company activation keep INITIALISE_COMPANY=NO and bootstrap secrets removed. Keep the independent
G01 demo configuration, its existing public-entry choice and INITIALISE_FICTIONAL_DEMO=NO. Do not reset,
re-import demonstration content, clear site data, repeat company setup or change credentials for this update.
No new environments, dependencies, API routes, database tables, roles or permission keys are introduced.

## Find your own work without losing the full choices

**My tasks** now means explicitly assigned to your account, including administrators. **All accessible**
retains the administrator's wider view and every other account's existing permitted scope. **Awaiting
review**, **Completed** and **Postponed** are visible first-level choices. More filters retains task type,
all statuses including Cancelled, and department-review scope. Search titles, assignees and department
labels. Reset filters returns to open personal work. Account/project changes reset filters; same-account
refresh keeps intentional choices. These controls never expand private access.

Compact cards show status, people, useful recorded progress and readable UTC due dates. Overdue is based
on the device clock and excludes paused/closed work, not an attendance, competence or equipment score.
Counts describe the current accessible list and applied filters, not the whole company's workload.

**New task** retains its four cards: General task, Verify inventory, Maintenance activity, Certificate
check. The existing ordinary one-page form, compatible scratch/template checklist choices, exact source
links and deliberate creation remain. No missing capability has been replaced with a generic text field.

## Instructions and the next permitted action first

The ordinary Task overview places instructions and the next action above expandable assignment details.
**Save progress** records findings, not completion. Checklist, Work & review, Discussion, Linked records,
History, per-task PDF and authorised management actions remain. Saved progress is expandable, not removed.

**Send for review** uses the saved findings and checklist results. The reviewer must deliberately choose
Complete or Return; neither decision is preselected on a new general or verification review. Existing
meaningful review findings, confirmation where applicable and explicit exception acceptance remain.
Returning, correcting, resubmitting and completing preserve named history. Completion does not complete
linked maintenance, renew a certificate, close a Fault Report or release equipment.

Postpone/Resume remains manual, keeps prior findings/checklist results and preserves the prior working
state. A review date does not run a scheduler or send an email. Cancellation/reopening retain existing
rules; inventory verification is not silently reopened as a fresh scope.

## Inventory verification uses the same clear layout

**What to verify · Who will verify it · Scope preview** are together on one scrolling page with reachable
save/draft controls. Assignees are searchable; hidden selections and unavailable retained references are
not silently dropped. The current service still validates eligible people and designated-department-head
creation authority; the update grants no new access.

All six scopes remain: individual items, all active inventory, location, department, original source tab
or one box. Keep the separate Selected records / Boxes and contents / Boxes only choices. Search filters
the visible preview, not the selected records. The expanded count is shown before creating.

A retained local preview includes its exact IDs and box expansion. Reopening it does not silently add new
inventory. **Refresh scope preview** deliberately reloads and recalculates; the server refuses changed
scope on a new save. A retry after a lost creation response preserves the original payload and operation
ID even if inventory changed meanwhile; it retrieves the one saved task, not a duplicate. Existing older
attempted payloads keep their original shape when unchanged. This is optional metadata in the existing
local form, not a new browser database or separate autosave engine.

**Create verification task** opens the exact saved task only after hub acknowledgement and local-draft
cleanup. Results start empty. A box result never marks its contents verified.

Phone layouts use individual item cards; desktop keeps the useful table. Find scoped items and filter
Still to verify / Verified / Missing-discrepancies / All. Hidden or stale results still count. Record
Found, Missing or Discrepancy, a counted quantity where known and useful notes. QR lookup still identifies
one scoped item without verifying it. **Found elsewhere? Move & verify** retains its separate authority,
destination/version checks and real movement reason; contents outside the task cannot be moved here.

## Routine reasons versus consequential changes

- Due-date updates, or unchanged/increased priority with the same assignees: no generic reason.
- Replacing your own never-submitted, unreviewed and unmoved inventory result: no generic reason.
- Changed assignees, lowered priority, another person's or unknown-authorship result, previously
  submitted evidence, moved evidence, reset/cancel/lifecycle corrections: existing applicable explanation.
- Missing, Discrepancy, Issue and N/A: meaningful result information still required.

Actor, server time, saved version and before/after audit remain. No artificial user explanation is
inserted. Standalone inventory verification's separate correction policy is unchanged.

## Local drafts and interrupted work

**Task drafts** opens this account's stored Task forms on this device, with direct resume and access to
Manage all unsaved work. It is not the list of hub-saved work, not a multi-account vault and not every
separate log window. Keep draft & close, UI45's one-warning sign-out and same-account recovery remain.

Late Reassign, History and saved-record reads cannot replace a newer editor, including one opened and
closed while the earlier request was outstanding. A save checks the originating account/form again
after lease renewal and immediately before credentials are captured. A changed account cannot send
an older form under its new credentials. No other account's local work is discarded.

A lost response retains Retry unchanged request; failed local cleanup also retains the original retry
rather than navigating early. Conflicts do not overwrite newer records. A request already sent may
still complete; changing views is not server cancellation. Do not clear storage or change domains to
force a retry. Local saving must be confirmed before treating text as a recoverable draft.

## Boundaries retained, not missing buttons

Task checklists are one shared result set with authorship, not separate runs per assignee. Templates
requiring Task-unsupported photo evidence or per-item approval remain explicitly refused, not weakened.
Task-specific file attachments, automatic recurrence/reminders, multiple linked sources, general
instruction revision, a subtasks engine, batch Task PDF and Task-specific visitor signing remain future
work. Existing handover attachments, QR/signing evidence and PDF writers are unchanged. Native Windows
Task dialogs/executables and the master guides were not redesigned or rebuilt.

## One acceptance session

Use fictional records and named manager/worker accounts. Create an ordinary checklist task and a stock
verification task. The worker finds both in My tasks, saves/reopens findings, records one explicit missing
item and submits. The manager returns the ordinary task, reviews its corrected resubmission, and completes
the inventory task only after accepting the recorded discrepancy. Export both reports. Check the same
paths on a phone, and confirm New task still has all four choices. Keep valuable unsent work out of tests.

## Verified locally, not deployed

690 selected Python tests and 111 compound browser checks passed, plus syntax checks for
73 application JavaScript files and parses of 193 application Python modules. 1803 tracked runtime
files match the final extraction. Two existing app Python modules change; 191 others and all company/
demo hosting files remain byte-identical. The approved Home and shared fieldwork writer are preserved.
Tasks and General Tasks Help/outlines are updated; 74 other bodies remain, all 76 catalogue entries match.

Actual application services/assets with fictional SQLite/TestClient and injected browser transport,
simulated route transitions and in-memory storage are used. No real Sulmara data, credentials or live
GitHub/Render actions. No full-suite, physical camera, durable IndexedDB, service-worker lifecycle,
Windows/PowerShell/native, full security/accessibility/load, Docker or off-host recovery acceptance.

An initial overbroad run included native Tk tests without a display and historical release-hash assertions.
26 historical assertions fail on untouched UI46; an additional old no-service-change invariant is knowingly
superseded by this service fix. They are not removed or counted as passes. Preliminary harness failures,
outline correction and teardown attempts are retained separately and excluded. Current functionality,
privacy, version, retry and source audits are checked directly rather than claiming those old assertions
were repaired. The verification report records the exact final commands and limits.

Rollback source only through the approved compatible UI46+C01 baseline; the old Tasks layouts and reason
rules return. Retained UI47 scope-preview metadata must be protected before using an older editor. Never
roll back company/evidence data, use pre-C01/pre-UI34 writers/exporters, reset the project or clear storage.

**Nothing was pushed or deployed from here.** After the Tasks acceptance session, continue the agreed
section-by-section review; no next section was silently redesigned or scheduled in the background.
