# Wavelink UI40 — reporting and follow-up workflow bundle

**Core 1.34.19 · UI40 · working G01 unchanged · 26 September 2026.**
One grouped release covers Fault Reports and HSE / QSHE from initial report through assignment,
progress, closure request and review. Compact patch for the matching **UI39 + G01** repository,
not complete source or a live-project backup. Nothing deployed here.

## Install once using GitHub Desktop

Preserve your complete backup, approved commit and unsent browser/separate-log work. Extract this
ZIP. Copy **everything inside UPLOAD_TO_GITHUB into your existing UI39 application repository**,
replace matching files, then review in GitHub Desktop, commit and **Push origin**. Deploy the
intended commit through your usual service workflow. Do not use the separate website repository.

Do not replace the whole repository or delete files absent from this patch.
**CHECK_UI40_UPDATE.ps1 is optional, read-only checking**, not an installer or mandatory upload.
Reconcile independently modified source rather than overwrite it. Keep G01, DEMO_PUBLIC_ENTRY=YES,
INITIALISE_FICTIONAL_DEMO=NO, required gate secret, matching non-admin guest, named administrator,
domain, disk and removed bootstrap. No reset, re-import or browser-storage clearing.

No new environment variables, permissions, dependencies, database tables or migrations. The
existing catalogue gains an optional responsibility filter and saved records a read-only hint;
there are no new endpoints or persistent formats. Keep compatible UI34+ evidence writers/exporters.

## One consistent workflow across both report types

**Report → Assign & follow up → Progress note → Send for closure review → Review decision.**

The shared one-page form keeps the action at the bottom of its own scrollable area. Initial
observations and immediate actions are visible first; optional source links and dates expand
only when needed. The concise privacy summary can be expanded to its complete access explanation.
There is no routine create/review wizard or confirmation checkbox for ordinary saves.

The report remains private under existing reporter, owner, authorised-head and administrator rules.
HSE/QSHE retains category, location and requirement fields; nonconformities/audit findings still
require the relevant expected condition. The default category/normal priority are not a safety
assessment. Use your organisation's immediate reporting procedure for urgent concerns.

## Responsibility and ownership without repeated searching

Both lists offer **All accessible reports**, **Assigned to me**, **Reported by me** and
**Unassigned**, alongside their existing status, text and HSE/QSHE category filters. The server
filters all currently permitted records before page counts and pagination; these are not totals
of hidden reports, a live workload measurement or a project-wide private-record directory.

**Assign & follow up** shows owner, department, priority and target date together. Owner search
retains the selected identity outside the visible search results. An unavailable saved owner is
shown rather than silently removed; choose a current eligible person or Unassigned explicitly.
The server rechecks authority/eligibility and changes recipient access using the existing rules.
Target dates do not create automatic reminders. A progress note does not complete a linked Task.

## Fewer routine prompts, meaningful exceptions retained

No generic reason or checkbox for creating the report, updating your own initial observation
before assignment/work, ordinary same-department owner or due-date changes without lowering
priority, writing progress or requesting closure. Automatic actor/time/version/before-and-after
history is retained. No made-up reason is inserted.

A report unassigned again after work does not become a new initial observation. Corrections to
established reports, another reporter's wording, or incomplete history need a real explanation.
Department transfers and priority reductions also need review because they change audience or
handling. Closure decisions and Hold/Resume/Cancel/Reopen/Archive/Task-link actions keep their
existing authority and real explanations. Exceptional lifecycle choices are under **More report
actions**, not removed. Current privacy and separate work/review permissions remain unchanged.

Identical initial-observation/assignment saves leave version and audit unchanged after current
permission/version checks. Stale editors are still refused. Legacy clients explicitly sending
confirmed=false are not silently overridden; the new routine form omits that unnecessary field.

## Closure is still a deliberate decision

The assigned worker records **Corrective work / proposed resolution** and **Verification performed
and remaining limitations**, then selects **Send for closure review**. Both substantive fields
remain required; there is no additional generic reason or routine checkbox. The report becomes
Awaiting review, not Closed.

An authorised manager sees that exact proposed resolution, selects **Close after review** or
**Return for further work**, adds real review findings and confirms. No decision is preselected.
Same-person review remains explicitly labelled where permitted; this release does not introduce
an independent-review policy. Report closure never releases equipment, approves maintenance or
closes a linked Task. Fault → corrective Task retains its separate source-sharing review; HSE
can still link an existing Task rather than automatically create or share one.

## Keep references and unsent wording safe

Optional equipment/Task searches retain the chosen exact ID/version when the search changes.
Failed or malformed reads cannot leave stale results available for saving. Retry the search or
explicitly remove the optional link; your other wording remains. Links do not grant source access.
A saved report changed since selection is refused rather than silently swapped into the editor.

Closing an untouched form is direct; edited or uncertain work still asks before discarding.
Notes stay **only in the open tab until saved**, not an offline draft. There is no photo/file
upload addition to these report forms. Losing/reloading the tab can lose unsaved wording.
Changed accounts, routes and interrupted dialogs cannot replace the current form or display
stale results. The original account/form is rechecked after the asynchronous lease wait, just
before request headers are captured. A delayed old form cannot be sent under a newly signed-in
account. A definitely unsent new attempt stays editable; earlier uncertain operations remain retained. A modal-interrupted list offers explicit refresh rather than indefinite loading.

A lost response retains **Retry unchanged request** with the original operation and payload.
That does not create another report or progress note. A conflict keeps local wording without
overwriting newer work. Closing cannot undo an already-sent request. Existing unsent work in
other modules is not cleared or submitted by this update.

## One short user acceptance session

Use fictional records and two named accounts: an authorised manager and an eligible worker.
Create one Fault Report and one HSE/QSHE observation. Assign both to the worker in the same
department, then use **Assigned to me** as that worker to add progress and send a resolution
for review. As manager, return one report for further work and close the other after reviewing.
Confirm that the first remains active, the second is closed, the named history is present and
linked equipment/Tasks are unchanged. Use the phone once during that same session if available.
The internal regression suite covers the additional failure/permission/retry permutations—you do
not need a separate installation or test session for each form.

## Verification and boundaries

**809 selected Python tests** (718 application + 91 gateway/package),
**179 compound Chromium checks**, **11 actual loopback gateway/application checks**,
**66 JavaScript syntax checks** and
**188 application Python parses** passed on frozen source.
Final ZIP replay matches **1759 tracked runtime files**. The new paired
workflow includes creation, assignment, owner filtering, progress, return/resubmit/closure,
lost responses, stale edits and modal/account changes. Twelve pure Node helper assertions run
inside one Python case, not twelve extra Python tests.

Four existing Python modules change (Fault/HSE services and their optional query wrappers) plus
one new shared read-only policy helper. The other 183 application Python modules remain
unchanged, including simple handovers/files, QR grants/signatures/PDFs, maintenance, certificates,
Tasks, Toolbox, presence and Original Files. Icons and support@mywavelink.com remain. Only the
extractor changes among existing executable GitHub files. Two Help bodies/outline entries are
updated;74 other bodies unchanged and all76 catalogue headings/text match.

Tests use fictional SQLite/TestClient, shipped assets and injected browser transport/in-memory
state. No full-suite, live HTTPS, physical-device/camera, durable browser storage/SW lifecycle,
Windows/PowerShell/native GUI, complete security/accessibility/load/isolation, Docker or accepted
off-host recovery result. Native binaries/master PDF guides were not rebuilt. Earlier failed or
superseded attempts are excluded; no unrelated historical test failure is claimed fixed.
No real project data, credentials, GitHub or hosting actions were taken.

Approved UI39 source rollback restores its older reporting forms/reason rules, not a data rollback.
Never use incompatible pre-UI34 writers/exporters for projects with signing/file evidence.
Next: this complete reporting acceptance session and actual feedback before the next grouped
workflow batch. Wider roadmap retained; no automatic background development.
