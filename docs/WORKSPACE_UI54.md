# Wavelink UI54 — reliable Maintenance assignments and a stable work view

**Core 1.34.19 · UI54 · Company C01 and demo G01 preserved · 27 September 2026.**
One workflow update on the exact UI53 application repository. This is a changed-files package,
not a live project backup, full repository or installed Windows update.

## Update through GitHub Desktop

Extract the ZIP and copy **everything inside UPLOAD_TO_GITHUB into your existing UI53 Wavelink
application repository folder**. Replace matching filenames, review the changes in GitHub Desktop,
commit and Push origin. Do not replace the whole repository, delete files absent from this patch,
or use the separate website repository. CHECK_UI54_UPDATE.ps1 is optional read-only checking,
not an installer; it was not executed on Windows here.

Preserve the approved commit, complete backup, outside changes and all unsent main/separate-log
work. Demo and Sulmara may auto-deploy the same branch; review their settings before pushing.
Keep the activated Sulmara COMPANY/C01 identity, PUBLIC_URL, dedicated disk and activation marker,
INITIALISE_COMPANY=NO and removed bootstrap secrets. Preserve the separate demo G01 configuration,
guest, domain and disk, DEMO_PUBLIC_ENTRY=YES and INITIALISE_FICTIONAL_DEMO=NO.
No new database tables, API routes, permissions, dependencies or environment variables. No reset,
re-import, repeated setup, browser-storage clearing or disabled synchronisation is required.

## People do not disappear from a retained work-order draft

**People allowed to record work** now has **Find people**. Searching name, login or account ID does
not uncheck selected people outside the results. The selection count remains visible.

When a previously selected person becomes unavailable, their exact retained ID remains checked
and labelled unavailable. A new creation cannot proceed until you explicitly remove or replace
that selection. It is not silently changed into an unrestricted order. Deliberately removing all
names allows any user with Maintenance work permission to record; managers retain their existing
authority. The recording scope is shown even while the optional people section is folded.
Maintenance viewing remains project-wide for permitted viewers, not a private assignment model.

The same retained-person treatment applies to exact-asset creation and pending follow-up release.
Pending follow-up reviews still require their real note and confirmation and can retain a block;
a successful review request does not by itself establish that a successor was created.

## The selected procedure revision stays explicit

Creating a work order still requires a deliberate published-routine selection. Its revision is
retained with the local form. If the current routine differs, choose **Use current published revision**
or another routine deliberately. An older draft without a recorded revision also requires that
explicit selection; no source revision is guessed. The retained revision is not a frozen local
copy of the procedure. Existing saved orders keep their original frozen procedure.

An unchanged previously attempted creation can retry the exact original payload and operation ID,
including its selected people, even when directories have subsequently changed. The server can
return its existing saved receipt; a new or changed proposal must still pass current validation.
It never removes people to make the retry succeed or creates another order under a new request.

A free-text equipment description remains distinct from an inventory link. Use **Asset details →
Maintenance → New linked maintenance** for an exact item. That identity remains fixed and the
saved order opens only after the ordinary save and local-draft cleanup have finished.

## Get directly to work or to the routine builder

Maintenance exposes **New work order** separately from **Create routine · Import routine · View routines**.
Those routine actions use existing Maintenance Builder plus base module permissions. A permissioned
Technician or Supervisor does not need general Administration. Import opens the existing reviewed
.ajcheck definition importer, not a job-history/workbook import. No templates or roles are created
merely by browsing.

Select an order title or **Continue work / Open order** to open its working screen directly.
**View summary** remains separately available, including the desktop side summary and phone Back
route. Existing status, routine, assignee and sort filters remain; Assigned to me keeps its already
correct personal meaning. Dates are readable and explicitly UTC.

The compact order heading retains **Work steps · Review & cycle · Instructions · Linked tasks**.
**Search & filter steps** expands the original search/section/status controls. **Find next unfinished**,
History and PDF remain available. Filtering does not reduce the required work or approvals.
The existing one-page creation/result forms, readings, notes, photos and Keep draft & close stay.
No extra routine reason, review step or approval shortcut is introduced.

## Saved updates do not replace unrelated work

Unchanged and ordinary changed-order/result refreshes reuse existing nodes, preserve expanded
filters and retain the visible reading anchor where it still exists. New record navigation starts
at the intended work view. Structural changes or removal of the anchor can limit exact restoration.
These are scoped Maintenance fixes, not universal live-update acceptance across the application.

A temporary connection failure leaves a labelled **Last saved Maintenance view** and blocks stale
record actions until Refresh succeeds. A definitive permission denial clears protected background
records even when a form has intervened; it does not delete the retained local draft or replace
typed wording. Saving later still requires the original account, current permissions and version.

Delayed History and directory reads cannot replace a newer editor. Maintenance saves now carry their
original account/form check through the asynchronous write-lease wait and recheck immediately before
credentials are captured. An obsolete unsent request is refused. An already-sent request is not
cancelled by navigation; keep its exact original request to check its outcome safely.

## Evidence, approval and cycles remain separate

Your own unapproved step updates remain reason-free. Issue/N/A descriptions, required readings and
photos remain mandatory where the routine specifies them. Correcting approved or another person's
work retains its explanation rules. A saved step is not an approved result or completed order.

The existing saved-evidence viewer, explicit step-approval guide, completion/cancellation and cycle
review guides remain. They were not replaced with one-click approval. A manager is not automatically
the configured approver; a permitted same-person review is labelled rather than called independent.
Completion still checks every required result, evidence and approval and creates at most one empty
successor under the existing cycle rules. No automatic stock consumption, custody release, hourly
trigger, QR maintenance adapter, email reminder or batch report is added.

All application Python modules and report generators remain byte-identical to UI53. Existing Home,
Tasks, Checklists, Logs, Handovers (including optional notes), Calendar and Inventory remain intact
apart from shared asset-cache references and the narrowly scoped shared Maintenance form guards.
C01/G01, website icons, support@mywavelink.com, separate-tab Help, sign-out and local-work management remain.

## One practical acceptance session

With fictional data and named accounts, open routine Create/Import/View as a permitted builder.
Create a named-worker order, preferably through exact Asset details, with required reading/photo and
a repeating schedule. Keep/resume the creation and a result draft. Search the people without losing
selections; deliberately resolve an unavailable selection in a disposable setup. Record the work,
review its saved evidence as the configured reviewer, then complete and check one empty successor.
Read lower steps while another person saves a change; open History without losing newer editor work.
Export the order and check the same phone path. Use only disposable records for account revocation,
lost-response, directory-change and discard testing.

## Actual verification and boundaries

**445 selected Python tests, 45 compound browser checks and 79 JavaScript syntax checks passed.** All 193 application Python modules remain byte-identical to UI53 and parse; 1844 tracked runtime hashes verified. Python groups: maintenance_py=96, inventory_py=94, preserved_py=77, hosting_py=178. Browser groups: maintenance_browser=18, inventory_browser=20, handover_browser=7. Twelve Node helper assertions run inside one Python case, not extra tests. The actual browser worker-photo/readings, separate reviewer approval and manager completion produced the authenticated example PDF; its unchanged renderer retained the saved reading, photograph, names and completion. Existing repeat-cycle service tests check single successors and blocked follow-ups. No full-suite claim.

Browser checks use shipped application assets, real fictional SQLite/TestClient services, injected
fetch/hash navigation and staged in-memory local transactions. These are not live Sulmara/GitHub/
Render/HTTPS, normal browser navigation, durable IndexedDB/service-worker, physical-camera/phone,
Windows/PowerShell/native, full-suite/security/accessibility/load, Docker or accepted off-host
recovery tests. No company credentials or real operational records were accessed.

Earlier incomplete, failed and superseded runs are retained separately and excluded. An initial
reading-anchor bug was corrected before the final freeze. Later browser fixture mistakes used the
request's asset_id instead of the saved asset snapshot's id; correcting those test lookups did not
change the application. A completed handover regression emitted a test-bridge teardown warning; the complete clean retry is counted instead. No unrelated historical test failure is claimed fixed. Maintenance Help
was updated;75 other article bodies and the native/master guides were not rewritten.

Keep compatible C01/UI34+ company/evidence writers. An approved UI53 source rollback would restore
its old Maintenance presentation/selection behavior; preserve new locally pinned-revision drafts
before such rollback and never roll the database back for a UI change. Deliberately discarded local
work cannot be recovered by a source rollback. The old pristine-source recovery helper is not approved.

**Nothing has been pushed or deployed from here.** Check this Maintenance workflow, then continue
with the next agreed section review rather than silently redesigning previously approved sections.
