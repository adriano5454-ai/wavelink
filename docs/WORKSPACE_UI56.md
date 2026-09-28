# Wavelink UI56 — Certificates, source files and reliable revision work

**Core 1.34.19 · UI56 · Company C01 and demo G01 retained · 28 September 2026.**
One complete section update on the exact UI55 repository. This is a changed-files update, not a
full source repository, live database, company backup or native Windows installer.

## Install through GitHub Desktop

Preserve your approved commit, complete company backup, independent edits and unsent main/separate-log
work. Extract this ZIP and copy **everything inside UPLOAD_TO_GITHUB into your existing UI55 Wavelink
application repository folder**, replacing matching filenames. Review in GitHub Desktop, commit and
**Push origin**. Do not replace the repository, delete unrelated files or use Wavelink-Website.
CHECK_UI56_UPDATE.ps1 is an optional read-only baseline/installed checker, not an installer. It was
not executed on Windows here. Reconcile independent source differences instead of overwriting them.

Both company and demo can deploy the same branch: review each service's auto-deploy setting first.
Keep activated Sulmara COMPANY/C01 identity, domain, dedicated disk and activation marker, with
INITIALISE_COMPANY=NO and bootstrap secrets removed. Preserve the independent demo's G01 settings,
credentials, domain and disk. No new environment settings, database tables, permissions, dependencies
or API routes are required. Do not repeat setup, re-import demo data, reset a disk, clear browser
storage or disable synchronisation. Save open editors before reloading the newly deployed scripts.

## Find the source you need

Certificates keeps **Add certificate** and its existing one-page editor, with searchable equipment,
retained references, optional contact/follow-up and Keep draft & close. The catalogue now offers
**Current revisions · Due soon · Expired · Drafts · All revisions**, a title/number/issuer/type/equipment
search and a responsible-contact filter. **Reset filters** restores the ordinary view.

Current means nonarchived and nonsuperseded, not necessarily valid: it can contain Draft and Withdrawn
records. Due soon/Expired are calculated date states; All revisions deliberately includes archived and
superseded sources. My named contact records matches your exact account, not every record you can view
or every member of your department. Contact metadata does not grant privacy, create a Task or send a reminder.

Cards show the source revision, recorded expiry, responsible contact, equipment and current file count.
**Open record** and the file-count action lead to the exact saved certificate. **Open source files**
on its record focuses the file section near the top. Recorded dates/scope/notes and exact equipment
stay available in expandable panels; source revisions and earlier files remain accessible.

History now uses the actual /api/certificates/<id>/history endpoint. It remains a read-only, permissioned
view of saved changes. Register authorship is not the source issuer or signatory. Draft is a shared
register state for permitted viewers, not a personal private-draft boundary.

## Stable refresh, with current authority

Same-session filters remain during normal refresh and navigation; changed authorised accounts/projects
reset them. Unchanged or ordinary changed-source updates reuse keyed cards and keep expanded record
sections. When changed update-order moves a card, the visible reading anchor is retained where it still
exists; scroll coordinates can legitimately change to keep that same content in place. Removed anchors
or structural changes can limit exact restoration. This is not persistence across logout/reload/devices.

A temporary failure leaves a labelled **Last saved view**, with stale record actions blocked until
Refresh succeeds. Definitive access denial clears protected background records even when a form has
intervened; it does not delete its stored draft or replace typed wording. Later saves still need current
permissions. Account, token, route, record and dialog guards reject obsolete responses.

UI55's quiet cached writes, eight-second overlap protection and real save/error warnings remain unchanged.
The main storage/sync/sign-out functions and approved section designs are not rewritten by this release.

## Attach the source without disturbing another editor

**Attach source file** selects a supported file and optional caption, then **Save attachment** uploads
it. The existing limits remain 20 MB per file and 12 files per revision. Byte-preserving format checks
are not malware scanning, metadata removal, authenticity checking or approval to operate equipment.
Avoid enabling macros/active content in untrusted downloads.

The selection/file bytes are in-tab only until uploaded, not a new durable offline draft. Normal Close,
Escape and sign-out wait during file preparation or sending. On an uncertain response, keep the form
open for **Retry same upload**; the exact payload and operation ID stay locked. No automatic retries or
new-operation fallback create a duplicate file. Closing an uncertain action warns that you must check
that exact record before starting another upload. An already-sent request can still succeed.

A delayed upload cannot close or refresh a replacement editor. Certificate saves recheck the original
account/form after the existing write-lease wait and before capturing credentials. An obsolete unsent
request is refused rather than adopting a different user. Late save errors are also scoped to their
original form, not inserted into a newer editor. Stored local drafts and receipt handling are preserved.

## Renew without unnecessary preparation paperwork

**Prepare renewal / revision** creates one unpublished replacement directly, without a generic reason or
confirmation step. It copies the existing descriptive context under the established rules, but its dates,
source revision and source files start blank. It does not activate the new record or copy old evidence.
The previous source remains current until activation. Preparing an additional draft remains an explicit
new action; the same lost-response request can retry without creating a second replacement.

Complete the new source details and files, then select **Review replacement**. One comparison shows the
previous/new source, dates and file counts. Enter the meaningful replacement review note and select
**Activate replacement** deliberately. The server checks both the selected replacement version and the
reviewed previous version. An archived or already superseded predecessor cannot be activated over by
this action. No generic extra checkbox or separate browser prompt is added.

Earlier records/files/history remain. Unknown expiry stays explicitly unknown; the register does not
require an actual issuer-authenticated attachment to label a record Active. Activation is a recorded
replacement decision, not proof of certificate validity or equipment release.

Routine draft edits, working notes and contacts remain reason-free. A validated unchanged Save with no
new typed note leaves the certificate version/edit audit unchanged, while retaining the operation receipt.
Current permissions, version, archive state, reason type and refreshed linked snapshots are still checked.
A changed equipment/contact snapshot is a real change; an explicit new note remains intentional audit
information. Corrections to recorded source details, state changes, archive/restore and attachment removal
retain their appropriate explanations. Removed attachment bytes are retained evidence, not securely erased.

## Register PDF, not an issued certificate

**Record PDF** exports this saved register revision, source metadata, links, fingerprints and supported
source images. Original PDF attachments remain separate files, not pages silently merged into the report.
The file-section heading/explanation now stay with the table. The fictional two-page example was rendered
and checked; no universal page reduction or very-large-report acceptance is claimed.

The report is not the whole register, complete correction history, company backup or an issued original.
Automatic expiry email/push, renewal Tasks, PDF data extraction, combined register export and certificate
QR approval remain future work. Original Files is still a separate document-library workflow.

## One practical acceptance session

With a named permissioned editor and fictional data, register a certificate for exact equipment, keep/resume
its draft and attach a small source. Open History, prepare a renewal, enter the new source, review/activate it
and reopen the earlier file. Try the status/contact filters, change a working note from a second account and
watch the lower list retain its reading anchor. Export the register PDF and check the same route on a phone.
Use disposable data for revocation, uncertain-request, account-change or deliberate-discard testing.

## Local checks and limits

**456 selected Python tests, 73 compound browser checks and 80 JavaScript syntax checks passed.** All 193 application Python modules parse; 191 are byte-identical to UI55. The frozen extractor produces 1851 tracked runtime files. Python groups: certificates_py=101, extra_files_py=5, stability_py=93, maintenance_py=79, hosting_py=178. Browser groups: certificates_browser=20, certificate_form_browser=14, refresh_browser=26, signout_browser=13. Eight integrated date/source/permission/replacement/report checks are additional, reported separately rather than counted as pytest cases.

These are selected checks, not a full suite. Actual shipped scripts and fictional SQLite/TestClient data
were used with injected fetch, simulated hash routing and staged in-memory browser transactions. The retained
UI55 stability test ran its original periodic callbacks concurrently for 33.5 seconds. This is not real
persistent IndexedDB, actual normal navigation, service-worker/WebSocket lifecycle, live Sulmara, physical
camera/device, Windows/PowerShell/native, full accessibility/security/load, Docker or accepted off-host recovery.

Two inherited save-status version/hash assertions were reproduced failing on unchanged UI55 and explicitly
excluded; they were not fixed or counted as passes. An earlier broader maintenance invocation collected five
native-window tests that could not connect to a display; the final complete server selection excludes those
native-window tests. Other initial incomplete/fixture runs, a retained harness teardown warning and superseded
pre-refinement checks are recorded separately. The final counted selections were rerun on the final frozen
source after correcting input styling and a reproduced obsolete-error callback. No unrelated historical
failure is presented as resolved. Only Certificates Help was updated; 75 other article bodies remain unchanged.

All existing company/gateway/deployment files and 191 of the 193 application Python modules are unchanged.
certificates.py adds validated no-op/preparation/previous-source review checks; asset_reports.py adjusts the
file-heading grouping. Shared frontend form changes are Certificate-scoped; the underlying main store,
API transport, queue, sign-out, UI55 stability, other module writers and permissions remain.

**Nothing has been pushed or deployed from here.** Keep C01/UI34-or-later compatible evidence handling; source
rollback cannot restore local entries deliberately discarded or undo a completed replacement. Do not roll
company data back for an interface change. After this section's acceptance, resume the next sidebar review.
