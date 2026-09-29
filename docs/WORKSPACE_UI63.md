# Wavelink UI63 — Personal Home and separate Workspaces

**Core 1.34.19 · UI63 · Company C01 and demo G01 retained · 29 September 2026.**
Stage A of the approved Personal Home and company-access plan, on the exact supplied UI62 repository.
This is a changed-files application package, not a company database, new login system or live deployment.

## Apply through GitHub Desktop

Preserve your approved commit, independent source changes, complete backup and unsent main/separate-log work.
Extract this ZIP and copy **everything inside UPLOAD_TO_GITHUB into your existing UI62 Wavelink application
repository**, replacing matching files. Review the changes, commit and **Push origin**. Keep the repository
and `.git`; do not delete files absent from this patch or copy into the separate Wavelink-Website repository.
The PowerShell checker is optional, read-only hash checking, not an installer; it was not run on Windows here.

Sulmara and the demo may auto-deploy the same branch. Review that before pushing. Keep activated C01 company
identity, PUBLIC_URL, dedicated disk and activation marker, INITIALISE_COMPANY=NO and removed bootstrap
secrets. Preserve the separate G01 demo configuration and data. **Operator-owned company_identities.json
and company_logos are not replaced by this update.** Keep your customised company names and artwork.

There are two new authenticated, read-only endpoints, but **no new database tables, permission flags,
dependencies, environment settings or browser-store versions**. No reset, demo import, repeated company
setup, site-data clearing or disabled synchronisation. Save in-tab editors before reloading once after the
intended deployment is healthy. The current named login remains available and unchanged.

## Home belongs to the signed-in person

Home identifies the person and current company, then shows their assigned shift and four personal views:
**My work · Needs my action · Saved handovers · My activity**.

There is no full workspace catalogue, generic company-setup checklist or project-wide certificate/maintenance
summary mixed into this page. Administrators see their own work rather than everything they can administer.
Project-wide records and their existing filters remain in the individual modules, reached through Workspaces
or the direct sidebar links.

### My shift

The card uses the existing personal-shift service: current/next occurrence, midnight boundaries, exact saved
record and the existing time-basis rules. It opens the person's existing notes or publication when matched.
When no exact record is available, **Open My shift** goes to the actual personal shift tab rather than the
team journal. Ambiguous assignments and descriptive clock labels retain their deliberate choice route.

My shift never adopts a colleague's assignment because the signed-in person is an administrator. There is no
new shift-boundary timer or automatic navigation away from an open editor. Optional notes, photos/files,
publication, current recipients and original-version checks remain in the existing Handovers workflow.

### My work

This list includes actual named Task and Maintenance assignments, assigned log Issues, owned Fault/HSE reports,
and standalone shared checklists the account created or contributed a reliably attributed result/review to.
A shared checklist contribution is labelled as such; it is not a newly private assignment. General viewing
access does not turn every record into personal work. Unassigned maintenance orders are not called yours.

**Active · Postponed / on hold · Completed / closed · All my work** and Type filter the list, with ordinary
page controls beyond the old five-preview limit. The initial work page has up to 12 records. Counts describe
matching permitted records, not quantities, productivity or operational readiness. Task and Maintenance due
dates, where saved, are shown separately and explicitly in UTC. No missing date is invented.

### Needs my action

This view includes incoming handover publications the person is eligible to acknowledge and has not yet
acknowledged, listed Toolbox briefings awaiting their personal acknowledgement, and saved checklist or
maintenance results assigned to them for review. A Task review appears for its designated responsible
department head with the required management permission, not for every administrator by role alone.

Reading or opening is not signing, approving or completing anything. A particular result's configured reviewer
still controls its approval; a general approval capability is not assignment to all pending checks. Future
membership-access requests are not implemented or displayed yet.

### Saved handovers and device-local work

Saved handovers contains the person's company-saved private drafts and corrections across dates, with direct
continuation where editing is permitted. It never lists colleagues' private notes. Existing publication
history remains exact.

**Manage unsaved work** and any actual local-work warning remain separate. Stored local forms, queues and
receipts are not renamed, moved or deleted. The existing same-account sign-out/resumption rules apply.
In-tab-only wording is still not a durable draft. This release does not add autosave or a multi-account vault.

## My activity is recorded contribution history

The timeline uses supported actions already recorded by the existing Task, Maintenance, Checklist, Handover,
Log, Toolbox, Inventory, Certificate, Fault and HSE/QSHE audit sources. It matches immutable account IDs,
not names, initials, a guest's typed identity or the account that most recently changed a shared record.

Examples of distinct event labels are **Recorded a checklist result**, **Saved task findings**, **Added a log
entry**, **Published a handover** and **Acknowledged a toolbox talk**. Recording one result is not completion
of the entire job. A device-ready event is labelled as device readiness, not checklist completion. Visits,
reads, heartbeats and background cache writes are not presented as accomplishments.

The initial date range is the last 30 days. Choose **Date range**, From/Through (UTC), Apply dates or **All
dates**, and an activity Type. Pages hold up to 20 entries, with Previous/Older activity. Underlying histories
are not rewritten or deduplicated into fabricated events. A bounded scan can require another page before
finding accessible older actions; that state is labelled rather than inventing a complete total.

**This is not a complete security audit or a guarantee that every historical/native/import action appears.**
Events without supported reliable account attribution and unsupported action types are omitted. Builder,
Fleet and security-administration histories are not added to this first personal timeline. The original
module histories remain their authority.

Every read and source opening still applies current company and record access. A contribution does not grant
continued access to a private Task or handover after permissions/audience change. Inaccessible entries are
omitted, not exposed with their old titles. Event timestamps describe the recorded action; ordinary titles
and status are taken from the currently permitted source, not a fabricated old-content snapshot. Handover
publication/acknowledgement links retain their exact recorded revision.

## Workspaces is a separate destination

**Workspaces** is immediately below Home in the sidebar. It contains the existing complete, permission-aware
card directory, category controls, activity search and supported **Open / Create / Import / Verify** actions.
The direct sidebar routes remain. All 17 possible module cards are retained; an account sees only its permitted
ones. Disabled creation actions retain their existing explanations and server-side authority checks.

The four-card Task chooser, real Inventory verification, builders/importers and Original Files remain their
actual existing workflows. Company setup work is found in Setup & builders, not imposed on every personal Home.
No record is created by opening a workspace or searching the directory.

## Stable refresh and safe read boundaries

Personal Home reuses keyed rows for ordinary changes. Unchanged refreshes keep the row and filter elements and
the tested reading position. When the existing shell renders, an idle Home rechecks at most about every 29
seconds; **no additional interval is created**. There is also an explicit Refresh action. Active editors and
focused filter controls are respected. My activity is not an atomic snapshot across multiple page requests.

Temporary read failures identify the last-saved personal view and pause stale opening actions until a successful
refresh. A failed category is labelled unavailable and its counts may be incomplete, never an all-clear.
Definitive denial or changed identity clears protected personal content, including behind another editor,
without deleting its local wording. An earlier account, filter, page or dialog response cannot replace a newer
view. Leaving and returning makes a fresh read; filters are current-session state, not promised across logout.

UI55 quiet cached writes and nonoverlapping refresh rounds remain. Actual save/error/offline feedback, write
leases, queues, identity, sign-out and bulk-discard transaction bodies are unchanged. UI60 shared controls and
separate-tab Help remain. The application does not close or reload another installed window.

## Sulmara email domain and later access stages

The user supplied **sulmara.com** on 29 September 2026. It is recorded in
`docs/PERSONAL_HOME_ACCESS_ROADMAP.md` as the intended company email domain, **not verified ownership**.
No DNS challenge, mailbox verification, email invitation, domain routing or automatic signup is enabled here.
The repository's company presentation configuration is not an authentication registry.

Next stage B must implement verified membership invitations, server-enforced pending/deny-all accounts and an
access-request queue with bounded delegation. Grantable rights must remain inside the coordinator's current
authority, explicit delegation allowance and authorised company/department/site scope, including dependencies.
No self-promotion, stronger-user editing or onward delegation by default; existing account IDs/history remain.

Stage C adds professional main-site sign-in, actual domain verification and trusted company routing with tested
email delivery. Typing an @sulmara.com address must not itself authenticate someone. Company membership
invitations remain separate from temporary exact-document QR visitors. Existing operational login and company
isolation remain in place during the staged transition. No email was sent by this release.

## One practical acceptance session

Use fictional data and two named accounts. Assign each a different Task and shift; check Home as each person
and as an administrator. Record a checklist result on a record created by the other account, then find it in
My work and My activity. Save/continue a handover, read an incoming publication without signing automatically,
and open an assigned review. Change a saved Task result and refresh while reading a lower row.

Use the Type/date filters and Older activity; open Workspaces and its real four-choice New task panel. Keep
one disposable local draft, sign out while retaining it, and return with the same account. Check the same
phone layout. Use disposable records only for permission revocation, delayed requests and discarded-work tests.

## Actual verification

**368 selected Python tests, 53 compound browser checks and 87 JavaScript syntax checks passed.** All 199 application Python modules parse; 197 existing modules are byte-identical to UI62. The frozen runtime has 1897 tracked files. Python groups: personal_py=22, sources_py=16, restricted_py=1, contract_py=7, shifts_py=66, retained_py=78, hosting_py=169, package_py=9. Browser groups: personal_browser=13, refresh_browser=26, signout_browser=13, changed_browser=1. The separately run restricted-account test is counted once; its earlier deselection from sources_py avoids duplicate coverage. Nine package tests are counted separately from the 169 other hosting tests. Preview renderings and repeated archive checks are not extra behaviour-test cases.

Earlier combined development runs did not reliably finish within their bounded run, including one with completed-looking output but no accepted clean process outcome. They are not counted. The final selected source tests were split into bounded groups, each with exit status 0 and complete test XML. The exact cause of every earlier process stall has not been established. Initial fixtures used a nonexistent permissions column, had SQL quoting mistakes and assumed an unadorned h1; those fixtures were corrected. A browser assertion confused CSS uppercase presentation with text content. Development also corrected a real Toolbox title projection, preserved the unaugmented checklist-definition hash for review checks, and used the existing in_progress shift-record state for direct draft continuation. Current regression tests cover those cases. The current UI63 cache/storage contract verifies all main scripts and styles; older release-specific cache-name tests are not claimed as current passes. No unrelated historical failure or native execution is declared fixed. All final counted selections used the same frozen application bytes; the last additional real-update browser scenario changed no application or shipped test files.

All counted tests use the frozen extractor/source. Browser checks use actual shipped assets, fictional
SQLite/TestClient services, injected transport, simulated hash navigation and staged in-memory transactions.
The retained refresh check runs the original callbacks concurrently for 33.5 seconds; it is not a new
production-load or real browser-storage test. Additional screenshots are fictional previews, not live Sulmara.

No full-product suite, live GitHub/Render/company-data access, actual HTTPS/WebSocket/browser navigation,
durable IndexedDB/service-worker lifecycle, physical phone, installed Chrome, Windows/PowerShell/native
binary, full security/accessibility/load certification, email delivery/domain verification or accepted off-host
recovery is claimed. Existing report/PDF generators and 21 PDF files are unchanged; no new report-design test.
The package's exact repository replay and fresh runtime extraction are checked separately from behaviour tests.

**Nothing has been pushed or deployed from here.** The Chrome safe window-reuse follow-up remains separate.
