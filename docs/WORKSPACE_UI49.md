# Wavelink UI49 — complete Logs workflow and stable updates

**Core 1.34.19 · UI49 · Company C01 and demo G01 preserved · 27 September 2026.**
Compact changed-files update for the exact UI48 + C01 source. This is not a full repository,
live project backup or remotely deployed service. Home, Tasks and Checklists layouts stay unchanged.

## Apply through GitHub Desktop

Extract the ZIP. Copy **everything inside UPLOAD_TO_GITHUB into your existing UI48 application
repository folder**, replacing matching files. Review, commit and Push origin in GitHub Desktop.
Do not replace the repository, delete files absent from this patch or upload to Wavelink-Website.
The PS1 is an optional read-only hash checker, not an installer or required extra step.

Preserve the approved commit, complete backup, outside edits and unsent main/separate-window work.
Check both services' auto-deploy settings: the same branch may deploy demo and Sulmara. Keep C01
company identity, domain, activated disk/marker, INITIALISE_COMPANY=NO and removed bootstrap secrets;
keep the separate demo's G01 settings. No reset, demo re-import or browser-storage clearing.
One new project-bound follow-up API uses the existing Logs tables. No new tables, permissions,
dependencies, environment settings, browser-store versions or manual SQL are needed.

## Create, import or open

Logs now exposes **Create logbook · Import existing · Open logbook** using current saved permissions.
A Technician or Supervisor with Logbook Builder and its underlying module access can create/import;
no administrator promotion is needed. Create opens the existing structural designer; Import opens
Setup & builders' reviewed `.ajlogs` definition-only import. It does not copy operational history,
entries or reference media from another company. Administration/archive/release retain separate authority.
Complex Excel workbook and full-history transfers remain advanced/native workflows.

## Desktop ledger and readable phone entries

All nine standard sections, custom required fields, LOG ON/OFF and status colours, dates, search,
paging and source references remain. The desktop table scrolls inside the available workspace rather
than widening the entire page; frozen date/event columns and All columns remain. Phone rows show
readable time, event/status, author and a short saved preview, with View entry for complete details.
**Section** selects every configured section; **Full table** keeps the original ledger available.
Expand view, Separate window, Export report, Unsent drafts and separate-tab Help remain visible.
Neither filtering, opening a record nor LOG ON/OFF controls equipment or writes an event automatically.

## Save an entry without a long wall of optional fields

Event/time and required fields come first, then Notes. Position/line/additional values and acquisition
file paths have expandable groups. Existing nonempty values remain shown, and no hidden value is lost.
The existing Calendar & clock picker, explicit UTC time and numeric validation remain. Zero/negative
offsets are retained where valid; no coordinate/time-zone/angle conversion is invented.

Save entry, Keep draft & close and Discard stay reachable in the scrolling form. Typing retains the
existing account-scoped local draft; a hub save remains explicit. Local log drafts are NOT automatically
submitted when connectivity returns. Identical-request retry keeps the original entry/operation identity.
Actual saved corrections still require an explanation and current edit-own/edit-any authority. Saving
genuinely unchanged information is now a no-op without a reason, version bump or extra audit row.

## Stable reads without switching off synchronisation

Unchanged catalogue and opened-book polls retain DOM cards/rows. Changed entries update their keyed
row; the tested nonzero horizontal and vertical table positions remain. Phone scroll, current section,
filters and typing remain during ordinary updates. A temporary connection failure labels the retained
view as last saved, not freshly verified. Definitive denied/unavailable access clears protected displayed
entries without deleting local drafts. Delayed View, History, reference or export reads cannot replace
newer work. A pending request rechecks its original account immediately before sending after the lease wait.
This is a Logs-scoped fix, not an assertion that every tab/deployment/real browser refresh is accepted.

## A limited Update issue action for assignees

For an active unresolved Issue, a current assigned project user or current member of its assigned active
department with log-entry permission can select **Update issue**. This changes only **Status** and
**Response / progress**, not the original description, note, event time, author, source or assignment.
Previous responses remain in named before/after history. A meaningful response is required, but not an
additional generic reason or confirmation wizard. No broad edit-any permission is granted.

Resolved means this account reports the Issue resolved, not independent verification, equipment release
or Task completion. It removes the Issue from the outstanding in-app inbox. Reopening still requires an
authorised explained correction. Current assignment/access, supported field choices and original version
are checked on each save. Archived/voided/resolved entries reject new limited follow-ups. Current authority
is rechecked on a retry; a revoked assignment can refuse access even to a previous request's outcome.

Follow-up text is **in that open form only until saved**, not a stored ordinary log draft. Close warns before
discarding it. An uncertain response offers **Retry same follow-up**; a successful duplicate request returns
its original outcome without adding another revision. Status, response, history, notification and receipt
commit together. This is a browser main-project feature, not a native/vessel workflow redesign.

## Reports and retained boundaries

PDF/CSV export the selected section and current filters across all matching saved pages. Excel offers
one section or all configured sections in separate worksheets. All-column choice and 1,000-entry PDF
limit remain. The example reports contain fictional data and were generated by the unchanged exporter.
Reports omit unsent forms, full correction history and reference images; they are not project backups.
There is no new ordinary entry photo/file attachment, automatic Task/reminder or alter-existing-schema
feature in this release. Separate log windows retain their separate local state and handoff rules.
Main sign-out and bulk discard do not comprehensively manage every separate window or other device.

## One acceptance session

Use a permissioned non-admin with fictional records. Open Create or Import from Logs, then record LOG ON,
Weather and an offset. Keep/resume one draft and save it. Assign an Issue to another user; have that
assignee use Update issue without permission to rewrite the original event. Make an explained correction
as its authorised author and check History. Export a filtered section and an all-section workbook.
On a phone, leave a lower entry open through unchanged and genuinely changed polls. Check the full table
and one separate-window return with disposable work. Do not test discard using valuable unsent entries.

## Verification and limitations

460 selected Python tests, 107 compound Chromium checks, 20 Node handoff simulations,
75 JavaScript syntax checks and 193 Python parses passed. Final ZIP replay verifies 1820
tracked runtime files and the complete target repository. Two application Python modules changed;
191 others, C01/G01 startup and existing report/schema code remain unchanged.

Browser checks use shipped assets, fictional SQLite/TestClient services and injected fetch/hash/staged
in-memory persistence. Not a full-suite, live Sulmara/Render/GitHub, physical phone/camera, real popup,
durable IndexedDB/SW, Windows/PowerShell/native, complete security/accessibility/load, Docker or accepted
off-host recovery result. Earlier partial/failed/refinement runs are excluded and retained separately.
The final selection was repeated after fixture-only corrections; application bytes remained unchanged.

No live records, credentials, hosting configuration or deployments were accessed. Keep compatible C01
and UI34-or-later evidence handling; rollback never restores deliberately discarded local work.
**Nothing was pushed or deployed from here.**
