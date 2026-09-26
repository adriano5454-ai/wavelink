# Wavelink UI39 — simpler toolbox-talk preparation

**Core 1.34.19 · UI39 · working G01 unchanged · 26 September 2026.**
Compact changed-file update for the exact **UI38 + G01** application repository on the
actual uploaded UI30 lineage. Not complete source or a project backup. Nothing deployed here.

## Copy, review, commit and push

Preserve your approved commit, complete project backup and unsent browser/separate-log work.
Extract the ZIP. Copy **everything inside UPLOAD_TO_GITHUB into your existing UI38 Wavelink
application repository folder**, accepting replacement of matching files. In GitHub Desktop,
review the changes, commit and **Push origin**, then deploy the intended commit normally.
Do not replace the whole repository, delete files absent from the patch or use the website repo.

**CHECK_UI39_UPDATE.ps1 is optional read-only checking**, not an installer or mandatory upload.
Reconcile independently changed source rather than overwrite it. No environment changes:
keep G01, DEMO_PUBLIC_ENTRY=YES, INITIALISE_FICTIONAL_DEMO=NO, the required gate secret,
matching non-admin guest, named administrator, domain, disk and removed bootstrap. No reset,
re-import or browser-storage clearing. Keep compatible UI34+ evidence writers/exporters.

## Choose the form and prepare the briefing

Open **Toolbox Talks → New toolbox talk**. Find the published form by title or document code
and select its exact revision. No form is preselected, and opening the picker creates nothing.
The browser checks the chosen version at opening and again at creation; a changed form is
refused rather than silently substituting a newer version. Legacy clients omitting that optional
version field retain their existing behaviour. Saved talks still keep a fixed form snapshot.

The new compact one-page editor puts **site, UTC time and work description** first. The time
starts with the device's current UTC value as before; check it against the actual briefing.
**Project & references**, **People with accounts** and **Named guests** expand only when needed.
Record the actual discussion and understanding answers, then select **Save briefing**. The
save controls remain reachable while the content scrolls on a phone. No routine extra review
page or confirmation checkbox is added.

Understanding answers start Unanswered. No topic, participant or Yes answer is selected for you.
The summary describes the open form's ticks, answers and listed people, not saved attendance,
signatures or operational readiness. Incomplete preparation may be saved with required details;
it cannot bypass the existing discussion and understanding requirements for signing.

## Find people without losing selections

Search by name, login or account ID. **Select visible eligible people** and **Clear visible
selections** affect only the current search results; choices outside the results stay selected.
The total selected and displayed counts are separate. Missing or newly ineligible saved/draft
references remain explicit rather than being silently removed. The service may refuse them
until the roster is deliberately corrected.

Optional Named guests retains the existing facilitator-witnessed method. Removing a newly added
unsaved guest row is direct; removing a saved guest still asks for confirmation. Listing someone
is not acknowledging for them. Up to 150 named people/guests remain supported. For QR visitors,
use the separate existing invitation workflow after saving the ready briefing; a manual guest
and a self-declared QR visitor are not automatically merged into one identity.

## Routine preparation needs no generic reason

Repeated changes to **your own open talk before any acknowledgement or issued QR invitation**
need no generic explanation. Genuine actor, time, saved version and before/after values still
record automatically. The former synthetic initial-save reason is not inserted. Any real note
retained in an older local form stays available as optional wording.

Correcting **another author's talk**, **previously signed or QR-shared information**, or a record
with **missing/inconsistent local history** still needs a short explanation. Closing/expiring a
QR does not erase the fact that wording was shared. Retained signatures and audit history are
checked even if a later correction cleared the current acknowledgement list. Server validation
runs inside the existing write transaction; a stale editor cannot bypass it.

Unchanged content remains a no-op, including an unchanged signed record saved without a reason.
Changed briefing content/roster advances the content version and clears current acknowledgements;
previous evidence remains retained, and outstanding QR grants for the old content become invalid.
Finalised/cancelled talks remain locked. This does not remove every reason prompt in Wavelink.

## Saving, signing and finalising stay separate

**Save briefing** creates or updates preparation only. It does not acknowledge, claim attendance,
open an invitation, finalise the talk or authorise work. Use the existing personal/witnessed
acknowledgement or **Invite to sign / signatures** actions afterward. The five-minute joining
window, document-only visitors, expiry/revocation, signatures, ordinary PDFs and signing PDFs
are unchanged. The Toolbox Help retains the full existing QR and signing-PDF guidance.

Reusable-form authoring/publishing, cancellation and finalisation controls are unchanged.
Your simplified Tasks, maintenance, certificates, handovers, photos/files, Original Files,
project activity, approved icons and **support@mywavelink.com** remain intact.

## Keep work and retry safely

**Keep draft & close** and resuming existing local forms preserve notes, answers, guest IDs,
attendee selections and the original saved version. A fresh read checks current access but
does not silently replace that original version with another tab's edits. Conflicts preserve
your wording without overwriting newer saved data. Unavailable references remain visible.

The saved talk opens only after the hub save and local-draft cleanup succeed. A lost response
or local cleanup failure retains the exact operation/request for retry, without duplicate talks
or audit events. Changed account, token, route or interrupted dialogs invalidate late reads.
No new persistent store, automatic signing or autosave system was added. Existing local-draft
behaviour still needs real-device durability acceptance; do not clear browser storage.

## Verification and boundaries

**689 selected Python tests** (598 application + 91 gateway/package),
**153 compound Chromium checks**, **11 actual local gateway/application checks**,
**65 JavaScript syntax checks** and
**187 application Python parses** passed on the frozen source.
The final ZIP replay matches **1752 tracked runtime files**. The totals include
27 new Python cases and 16 new compound browser checks;
11 pure Node helper assertions run within one Python case, not additional Python tests.

Only app/toolbox.py changes among 187 existing application Python modules: three class methods
and the bounded reason helper. The existing acknowledgement, guest-witnessing, finalisation and
cancel methods, shared browser writer/transaction/retry, other module services and G01/Nginx stay
unchanged. No new APIs, tables, permissions, dependencies, environment variables or migrations.
One Toolbox Help article/outline updated;75 other bodies unchanged;76 catalogue entries match.
Native forms, the master guide and installed Windows binaries were not redesigned or rebuilt.

Tests use fictional SQLite/TestClient data, shipped assets and injected browser transport/
in-memory persistence through set_content. Actual proxy checks are loopback, not live TLS.
No full-suite, live HTTPS, physical-device/camera, durable IndexedDB, service-worker lifecycle,
Windows/PowerShell, complete accessibility/security/isolation/load, Docker or accepted off-host
recovery claim. Preliminary and superseded runs are separate and excluded. Previous unrelated
historical assertions were not selected or declared fixed. No real data or credentials accessed.

Approved UI38 source rollback restores its older Toolbox form/reason policy without data rollback.
Do not use incompatible pre-UI34 writers/exporters for projects containing evidence. Next: actual
Toolbox/QR/phone and routine workflow feedback first, then the remaining grouped usability cleanup.
