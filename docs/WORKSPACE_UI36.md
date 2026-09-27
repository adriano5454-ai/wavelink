# Wavelink UI36 — simpler maintenance recording and creation

**Core 1.34.19 · UI36 · G01 unchanged · 26 September 2026.** Changed-files update for the
exact **UI35 + working G01** repository from this chat. Not a complete source or project backup.

## Update using GitHub Desktop

Preserve unsent work, your approved commit and complete project backup. Extract the ZIP and
copy **everything inside UPLOAD_TO_GITHUB into your existing UI35 Wavelink application
repository folder**. Replace matching files, review in GitHub Desktop, commit and **Push origin**.
Deploy the intended commit through your existing service workflow. Do not replace the repository,
delete files absent from the patch or use the separate website repository.

The included **CHECK_UI36_UPDATE.ps1** is optional read-only checking, not an installer. No
new environment variables, permissions, dependencies or tables are needed. Keep G01,
DEMO_PUBLIC_ENTRY=YES, INITIALISE_FICTIONAL_DEMO=NO, the required gate secret, matching non-admin
guest, separate named administrator, domain/disk and removed bootstrap unchanged.
Do not clear site data, reset or re-import. Keep compatible UI34+ invitation/attachment writers
and exporters. Reconcile independently changed source before overwriting it.

## Record a step on one page

Open **Maintenance → a work order → Work steps → Record / update step**. Result, readings,
work note and photographs are now on one scrolling page. **Save step & close** directly saves
through the existing service. The action buttons remain reachable while the content scrolls.
There are no Next/Back review pages or confirmation checkbox on ordinary recording.

**Last saved result** expands the snapshot held when the form opened, not a fresh server read.
Your own unapproved saved result can be updated without a typed reason. Existing account, time,
version and before/after audit remain; no explanation is fabricated on your behalf. A genuine
reason from an older retained local draft stays available as an optional change note.

Required readings, numeric limits and required photographs still apply. **Issue** still needs
a description, and **Not applicable** needs an explanation. Those are result notes, not generic
save reasons. Correcting **approved work** or **another person's saved result** still needs a
short reason and existing editing authority. Changed results need any configured approval again.
Saving a step does not approve it, finish the order, release quarantine or authorise equipment use.

Photo selection and captions use the existing evidence editor. A selected image is prepared in
the local form; notes/photos save together with the result, not through a separate upload wizard.
No photo limits, privacy rules, approval rules or native image formats are changed here.

## Create an order without a four-page wizard

**New work order** now shows the routine, title, equipment description, reference and instructions
on one page. No routine is preselected. The optional **People allowed to record work** and
**Repeat schedule** sections expand only when needed; the current assignment summary stays visible.
No named assignees means any user with Maintenance work permission may record, not a private Task.
Managers keep their existing access. One-off remains the default; no due date is invented.
Fixed scheduled repeats still require a due date/time in UTC.

Choose **Create work order** directly. For an exact inventory link use
**Asset details → Maintenance → New linked maintenance**. The same short form keeps the exact
item name, serial/reference and fixed ID, with **Create linked work order** as the final action.
Creation saves one open order with empty results, never performed work or equipment approval.

## Drafts, conflicts and important exceptions

**Keep draft & close** and **Discard draft** retain their existing behaviour. Closing or resuming
is not a server submission. The normal local draft system remains account/project scoped;
this release adds no new store and does not claim real-device durable-storage acceptance.
Resumed creation uses the currently available routine/people, not a frozen local routine revision.
Unavailable retained assignees are identified; review those current choices before saving.

A lost response can mean the server already saved the work. Preserve the form and retry the
same request; do not change an uncertain request merely to try again. The existing operation IDs,
atomic saves and version conflicts remain. Tests exercise a committed response loss without
another result/photo/order being created. A newer saved step is not overwritten silently.
Only a corrected local input warning clears itself; saved-request errors remain explicit.

**Review approval, completion/cancellation, cycle changes and pending follow-up review remain
separate controls.** Ordinary saving never executes them. Their substantive reasons, evidence,
permissions and confirmation rules are not removed. Native dialog layout is unchanged.

This is the next routine-friction cleanup, not every module completed. Simple handovers,
People & shifts, attachments, QR signing/PDFs, Original Files, presence, approved icons and
support@mywavelink.com are unchanged. Existing workspace badges may retain their earlier
feature version; the two changed forms identify UI36.

## Verification

**441 selected Python tests** (350 application + 91 gateway/package),
**107 compound browser checks**, **11 actual local proxy checks**, **62 JavaScript syntax
checks** and **187 Python parses** passed on the frozen runtime. All **1734
tracked runtime files** are verified. The new maintenance backend has 27 cases plus retained
cycle/API regressions; the separate maintenance browser run has 15 compound checks.

Five native Tk cases did not obtain a completed acceptance result and are excluded. The complete
maintenance API selection was rerun. Other preliminary/failed/partial attempts are retained
separately, not included in these counts. Previous historical assertions were not rerun or
claimed fixed. Tests use fictional data, controlled browser storage/transport and local loopback;
not a full suite, live HTTPS, physical-camera/phone, durable IDB, service-worker, Windows/PowerShell,
full accessibility/security/load, Docker or accepted recovery result. No deployment occurred here.

Only app/maintenance.py changes among the 187 application Python modules; only its do_save_step
reason validation changes. Shared transaction, replay, approval, completion and recurring logic
remain. One Maintenance Help body is updated, 75 unchanged, all 76 search entries match. No
native/master-PDF procedural review is claimed. See the separate verification and test evidence.

**Next:** actual maintenance and QR/phone feedback, then continue remaining routine reasons and
click-count reductions in coherent batches. No new review-heavy everyday workflows.
