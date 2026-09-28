# Wavelink UI61 — Original Files and exact source links

Core **1.34.19**. Company C01 and demo G01 preserved. Read docs/WORKSPACE_UI61.md and docs/CONTINUATION_CHECKPOINT.md.

Visible uploads/folders, delegated actions, source history/usage and reversible lifecycle, exact checklist/maintenance source links. Original bytes, existing references and publications remain. No resets or environment changes. Copy update contents into the existing application repository; review, commit and push.

--- Retained repository/build guidance ---

# Wavelink UI60 — shared browser interface

Core **1.34.19**. Company C01 and demo G01 preserved. Read docs/WORKSPACE_UI60.md and docs/CONTINUATION_CHECKPOINT.md.

Common Help, headings, action/view/form presentation; all existing application Python, authority, data and report semantics retained. No reset or environment change. Copy the supplied GitHub files into the existing application repository, review, commit and push.

--- Retained repository/build guidance ---

# Wavelink UI59 — participants, signatures and browser consistency

Current application core **1.34.19**, Company C01 and G01 retained. Read docs/WORKSPACE_UI59.md and docs/CONTINUATION_CHECKPOINT.md.

New normal document participation/PDF projections read existing saved evidence. No data reset, guest-account creation, mandatory re-signing or environment change. Update by copying the supplied GitHub files into the existing application repository and committing/pushing.

--- Retained repository/build guidance ---

# Wavelink UI58 — explicit shift permissions and a focused My shift

**Core 1.34.19 · UI58 · Company C01 and demo G01 preserved · 28 September 2026.**
This is one update for the exact prepared UI57 + C01 + G01 repository. It is not a full repository,
a project backup or proof of the version deployed to either service.

## Update using GitHub Desktop

Preserve your current commit, independent source changes, complete backup and unsent main/separate-log
work. Extract the ZIP. Copy **everything inside UPLOAD_TO_GITHUB into your existing UI57 Wavelink
application repository**, replacing matching filenames. Review in GitHub Desktop, commit and Push origin.
Do not replace the whole repository, delete files absent from this patch or use Wavelink-Website.
CHECK_UI58_UPDATE.ps1 is an optional read-only checker, not an installer or required upload. It was not
run on Windows here. Both services may auto-deploy the same branch; review that before pushing.

No new environment variables, API routes, dependencies, database tables or browser stores are required.
There ARE three new permission flags in the existing account-permissions JSON. They are not automatically
granted to non-admin accounts. Do not reset data, re-import the demo, clear browser storage, repeat company
setup or disable sync. Keep Sulmara's C01 identity/domain/disk/activation marker and completed-setup settings,
and the separate G01 demonstration configuration. No credentials or live data were inspected or changed.

## Grant the actual shift action

As a named administrator, open **Administration → People & access → select a person → Project permissions**.
The new **Shifts & people** group contains:

| Permission | What it grants |
|---|---|
| Create and edit shift schedules in your departments | Create a department cycle; change its hours, shift names, subject/site and time basis. |
| Assign and remove people from shifts in your departments | Change which eligible existing department members occupy the shifts of an existing cycle. |
| Extend granted shift actions to all active departments | Extend whichever of the preceding actions are granted beyond the person's current department memberships. Does not grant the other action. |

Handovers view is required. The all-departments extension requires at least one shift action. Grant both
first actions when someone should set the hours and assign people. Grant only assignment when they should
manage people without editing hours. Without all-departments scope, the actions apply only to active
departments the person currently belongs to. No department-head appointment or administrator promotion is
needed. This is not a general user/department creator, task-management grant or broader private-record access.

**New flags default OFF for all non-admin accounts, including existing department heads and Supervisors.**
Administrators retain full access. Review existing coordinators and deliberately grant their needed actions
once. Current users/roles/memberships, saved shift setups and handovers are not rewritten. Old explicitly
saved policies missing the new keys receive no implicit delegation. Corrupt policies fail closed.

The ordinary permission-change review/reason remains because it changes access. Saving a policy revokes that
person's existing sessions: preserve their work, then sign in again as the same account. An old permission
form missing the new keys is refused; reopen the current form instead of saving an incomplete policy.

All operational access does not add all-departments shift scope or backup access. Use role defaults restores
that role's defaults, including the three shift flags OFF for non-admin roles. Existing builder/import and QR
invitation groups remain, with short explanations; no duplicate flags or expanded document-sharing rights.
Review effective access includes the shift-scope boundaries. Original Files upload/folder administration and
account/department administration remain governed by their separate existing authorities.

## The setup screen matches the granted capabilities

In **Handovers → Shifts & people**, the action is Create shifts, Edit shifts & people, Edit shift schedule
or Assign people as appropriate. Schedule-only users see people but cannot change their assignments.
Assignment-only users see saved hours as read-only; they cannot create the initial schedule. Both actions
can be saved together by someone with both grants. A coordinator need not have Create handovers simply to
coordinate; each newly assigned author still needs Handovers view/create and current department membership.

The service checks the actual changed fields, not just the hidden/disabled controls. Schedule-only edits
cannot remove people when shortening the number of shifts; assignment-only requests cannot change hours,
names, site or clock basis. A lost-response retry keeps its exact operation ID and payload, with current
department and originally required action grants checked before returning its stored receipt.

Retained unavailable assignments are shown rather than silently removed. A schedule-only edit may retain
them unchanged; a newly assigned/reassigned person must be eligible now. Someone with assignment permission
can remove obsolete assignments deliberately. Changed membership or revoked permission blocks stale saves.
No private handover or publication is changed by coordinating shifts. One current cycle per department is
still the supported setup, not a new multiple-site or historic rotation planner.

## My shift has only your own shift content

My shift shows your own assigned hours, department/site, personal handover status and Open/Edit/Read action.
It no longer includes the common advanced/team panel underneath it. Duplicate team/advanced toolbar controls
are omitted from this personal view; the clearly visible view tabs still provide access to those features.
The current/next occurrence, overnight dates, explicit fallback for an unknown clock basis and only-own
choice for ambiguous assignments remain. All notes are optional; Save & close and Finish are unchanged.

**Incoming** renders its incoming publication list only when selected. **My saved notes** renders the wider
own-draft list only in that tab. **By day / subject → All saved handovers & advanced tools** retains the full
permitted library and old manual department/day board. Shifts & people retains coordination. None of those
features, saved publications, acknowledgements or drafts are deleted. Main Create handover still has its
four choices. The handover editor, files, exact source links, publication/acknowledgement writers, QR signing
and PDF export are unchanged.

In the inspected UI57 build, the incoming panel itself was hidden on the tested My shift route, but its
content was still eagerly built and the expandable all-saved/team tools remained visible beneath every tab.
This does not establish which installed/live build produced every part of the user's reported screen. UI58
makes ownership explicit, renders incoming/saved-note contents only in their views and hides/inactivates
nonselected panels. Tests inspect the entire workspace, not just the inner personal card.

The same personal refreshes keep existing cards. A late read cannot switch the active tab or reveal an
inactive panel. No additional timer, forced reload, automatic handover creation or navigation at a shift
boundary is introduced. Existing local cache, unsent-work, same-account sign-out and bulk-discard safeguards
remain. Navigation and filtering are not security grants; exact backend permissions still apply.

## One acceptance session

Use fictional data and a named administrator plus a non-head Technician/Supervisor. Grant the worker only
Create and edit shift schedules and verify they can create hours but not assign people. Grant assignment
as well (sign back in), assign two existing authors to different shifts, and open My shift as each author.
Each should see only their own shift content; Incoming should appear only under Incoming. Check that the
full library/advanced board is still available under By day / subject and that an existing personal draft
opens unchanged. Check the same route on a phone. No valuable unsent work should be used to test revocation
or discarding.

## Verification and limits

**575 selected Python tests, 78 compound browser checks and 81 JavaScript syntax checks passed.** All 194 application Python modules parse; 189 remain unchanged. The frozen runtime contains 1857 tracked files. Python groups: permissions_py=222, handover_history_py=175, hosting_py=178. Browser groups: permissions_browser=9, tabs_browser=9, shifts_browser=19, certificates_browser=15, refresh_browser=26. Selected checks, not full-suite or live acceptance.

Checks use shipped assets, real fictional SQLite/TestClient APIs, injected fetch/hash navigation and a staged
in-memory browser store. They are not a full product suite, live Sulmara/GitHub/Render, physical device,
durable IndexedDB/service worker, Windows/PowerShell/native installer, production-security/accessibility/load,
Docker or accepted off-host recovery test. UI55's concurrent periodic-callback check and the UI56 certificate
browser checks are retained. Report/QR rendering was not newly accepted for this permission/panel update.

The pre-interruption tests and initial UI58 fixture attempts are not added to final totals. A source-audit
assertion initially compared the entire pre-setup file, including deliberately changed old-board permission
wording; the corrected audit verifies the actual notes-editor span byte-for-byte and separately accounts for
changed board wording. No operational assertion was removed to hide a failure. Specific final commands,
source fingerprints and packaging replay are in the verification/evidence files.

Do not roll the database back for a UI change. Older source does not enforce these explicit delegation flags
and can restore implicit department-head authority; any source rollback needs a permission review and must
retain C01/UI34+ evidence compatibility. Source rollback cannot restore deliberately discarded local work.
The Chrome-installed shortcut/window-reuse follow-up remains separate; no launcher, icon, installer or PWA
identity changes are included. No uninstall or site-data clearing is required.

**Nothing has been pushed or deployed from here.** Resume the section-by-section workflow after checking
these related permission and personal-view changes; the wider roadmap remains in DEVELOPMENT_TODO.
