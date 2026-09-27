# Wavelink UI51 — stable Calendar navigation and a compact Month / Agenda

**Core 1.34.19 · UI51 · Company C01 and demo G01 preserved · 27 September 2026.**
This complete Calendar workflow update is for the verified **UI50 + Company C01 + G01**
repository, including the full UI50 ZIP supplied in this conversation. It is an incremental
code update, not a company database, backup or deployed service.

## Install using GitHub Desktop

Preserve your approved commit, independent edits, complete backup and unsent main/separate-log
work. Extract this update and copy **everything inside UPLOAD_TO_GITHUB into your existing UI50
application repository folder**. Replace matching filenames, review in GitHub Desktop, commit
and **Push origin**. Do not replace the whole repository, delete missing patch files or upload
this into the separate Wavelink-Website repository. The optional CHECK_UI51_UPDATE.ps1 is a
read-only baseline/installed checker, not an installer; it was not run on Windows here.

Sulmara and the demo may auto-deploy from the same branch; review each service's existing settings.
Keep the activated COMPANY/C01 identity, PUBLIC_URL, dedicated disk, activation marker,
INITIALISE_COMPANY=NO and removed bootstrap secrets. Preserve separate G01 demo credentials,
domain, disk, DEMO_PUBLIC_ENTRY=YES and INITIALISE_FICTIONAL_DEMO=NO. No new environment variables,
permissions, dependencies, API routes, SQL tables or migrations are required. Do not reset,
re-import, clear site data, disable synchronisation or repeat company setup. Do not use incompatible
pre-C01 or pre-UI34 evidence software. Nothing was pushed or deployed from here.

## The actual dates come before the settings

Calendar now has visible **Month / Agenda** controls, compact previous/next/month-picker and
**This month**, and expandable **Filters** with an active summary. All eight existing categories
and their colours remain. Certificates, Maintenance, Tasks and Toolbox talks are still the four
defaults. Checklists, Asset dates, Log events and authorised Manifest dates remain selectable.
Use All available categories, Clear categories or Reset filters deliberately; no category choice
creates or changes a record. Permission-revoked categories and their events disappear on a fresh
successful read. The interface does not grant the administrator's options to another account.

The Monday-start month keeps date/event counts on phones and event titles on wider screens.
Selecting a day shows that day's agenda; **Whole month** restores the month's entries. Agenda is
also a direct view, not a hidden dropdown option. The first month dates are visible in the initial
390- and 320-pixel test viewports. This is measured local layout, not a physical-phone acceptance.

**Find a title or source in this month** filters the returned title, category, event description,
source status and date. It does not search every project record or private notes. Filters reset
between accounts/projects; same-account normal refresh and navigation back retain month, view,
category, search and selected-day choices. The reading anchor is temporary in this workspace
session; it is not stored across browser reload, logout, devices or a new account.

## Open the exact source in its normal workspace

Checklist dates now contain a valid saved stage. A normal checklist click retrieves the record
again and opens its first unfinished pre/post stage, or its last finalised stage when all are
finished. It does not just append a guessed stage. The existing checklist router and device
participation rules remain; browsing the calendar does not complete results or join every event.

Manifest dates use the main application's existing embedded Fleet route and exact manifest ID,
not a /fleet page departure. Existing administrator/Fleet rights and session handoff apply.

Log entries preserve the originating Calendar account, route, page and dialog through both
metadata reads and the saved-entry handoff. A delayed response cannot open an Activity modal over
Home or another editor, even if an intervening editor has already closed. Open saved entry and
Back to calendar remain available. The improved Logs editor and operational writer are unchanged.

Tasks, certificates, maintenance, toolbox talks and assets keep their existing exact-record
routes and normal permission checks. A source link never grants new access.

## Refresh without blanking or rebuilding the whole page

An unchanged automatic or manual check keeps the same grid, day and agenda row nodes. A genuinely
changed source updates only the affected keyed content; unrelated entries remain. Current search,
selected day, focus and reading anchor are retained where the anchor still exists. Synchronisation
is not disabled. Opening a new source still follows its ordinary workflow.

A temporary connection failure leaves a clearly labelled **Last saved view** with stale source
opening disabled until a successful refresh. A definitive 401/403/404/409/access or account change
clears protected displayed dates. A Calendar denial arriving while another dialog is open clears
the calendar behind it without discarding that form. Normal shared API session-expiry rules still
apply; this release does not rewrite global authentication or automatically clear local drafts.

An interrupted, superseded or mismatched response cannot overwrite a newer account/month/form.
An explicit Refresh is available after a dialog interrupts a read. There is no silent substitute
for a source identity, incomplete event or missing count. These are separate reads, not a live
atomic snapshot across every underlying module.

## Keep the meaning of each date clear

Agenda rows distinguish the date/event description from **Source status** (or **Certificate status**),
and Past date / Today / Future date. These are not universal overdue, attendance or readiness
judgments. A cancelled Task can have a historical due date; a briefing time is not proof it was
conducted; a checklist's record date is not a newly invented deadline; a renewal target is distinct
from expiry. Date-only values remain dates and timed values are labelled UTC. Unknown dates are
not guessed, and a source correction moves its event to the new month.

The existing 2,000-event response bound remains explicit. On a truncated result the page states
the returned and total counts; its search/day counts cover the returned subset, not the whole
month. Narrow categories or use the original workspace rather than assuming completeness.

Calendar remains a linked date view, **not an appointment scheduler**. No independent event creation,
drag-to-reschedule, automatic recurrence, email/push reminders, Calendar PDF/CSV/ICS export, external
calendar sync or additional Handovers/Fault/HSE category is added by this update. Edit dates in the
source record. Existing source-module reports remain available there.

## Preserved sections and review process

The approved Home, Tasks, Checklists, Logs and Handovers layouts and their writers remain. The
asset/certificate/linked-maintenance forms, four Task choices, permissioned builders, separate-tab
Help, local-work manager, keep-drafts sign-out, handover attachments, QR signing/PDFs, presence,
website icons and support@mywavelink.com remain. Company/demo startup and all report generators
are byte-identical to the verified UI50 baseline.

Only Calendar Help is rewritten; the other 75 article bodies remain unchanged. Their external
reader-cache links advance, and all 76 search entries match. This is not a native/master-guide
rewrite or universal Help acceptance. Native installed applications are not rebuilt.

## One acceptance session

Using fictional data and named manager/worker accounts, choose Month and Agenda, search and select
a day, open a before/after checklist and a saved log, then return to your place. Open an authorised
manifest in embedded Fleet. Let another user change a Task date and confirm that it moves between
months without unrelated rows rebuilding. On a disposable account, revoke Calendar permission and
check that old events clear without deleting drafts. Check both 390/320-type phone and desktop
layouts during the same session; never use valuable unsent work for destructive tests.

## Local verification

**502 selected Python tests** and **132 compound browser checks** passed, plus syntax checks for **77 application JavaScript files** and parsing of **193 Python modules**. The frozen runtime contains **1832 tracked files**. Python groups: calendar_py=54, c01_py=71, gateway_py=107, local_builders_py=47, approved_py=192, handovers_py=31. Browser groups: checklists_browser=10, builders_browser=9, signout_browser=13, stability_browser=16, tasks_browser=31, home_browser=15, logs_browser=13, calendar_browser=25. All final selected groups were rerun after the test-only cache-version correction; production application bytes were unchanged by that correction. Source audit and final ZIP replay are separately recorded. These are selected tests, not a full-suite result.

Tests use the actual shipped source and temporary fictional SQLite/TestClient services, with
injected browser transport, simulated hash navigation and staged in-memory storage. Not full-suite,
live Sulmara/Render/GitHub/HTTPS, physical device/camera, actual durable IndexedDB/service-worker,
Windows/PowerShell/native, full accessibility/security/load, Docker or accepted off-host recovery.
Normal browser navigation remains restricted in this environment and was not bypassed. No real
company data or credentials were accessed. Earlier incomplete/failed fixtures and the inherited
old service-worker version assertion are retained separately, not counted as passes. That test
expectation was updated to UI51; its other cache assertions were retained. Exact source and ZIP
replay are reported separately. Nothing has been deployed from here.
