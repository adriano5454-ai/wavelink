# Wavelink UI56 — Certificate register, source files and renewal

**Core 1.34.19 · UI56 · Company C01 and demo G01 preserved.**
This is the approved Certificates implementation on the verified UI55 source. It is a changed-files
GitHub update, not a complete repository, a live-project backup or a rebuilt Windows installer.

## Install through your existing GitHub Desktop workflow

Extract and copy **everything inside UPLOAD_TO_GITHUB into the existing UI55 Wavelink application
repository folder**, replacing matching files. Review, commit and Push origin. Do not delete
files absent from this patch or replace the whole repository. CHECK_UI56_UPDATE.ps1 is optional
read-only hash checking, not an installer. Independently modified source needs reconciliation.

Both the demo and Sulmara may deploy the same branch; review their auto-deploy settings. Preserve
your backup, approved commit, outside edits and unsent main/separate-log work. Keep the activated
company C01 identity, public URL, disk and activation marker, INITIALISE_COMPANY=NO and removed
bootstrap secrets. Keep the demo's existing G01 settings and data. No new environment variables,
permissions, API routes, dependencies, tables, migrations or browser-store versions are required.
Do not reset, re-import, repeat setup, clear site data or disable synchronization.

## Find the record and open its sources

The register offers **Current revisions · Due soon · Expired · Drafts · Archived / superseded ·
All revisions**. Search titles, numbers, issuer or linked equipment. The Responsible contact filter
uses the contacts returned in your accessible records; Me means your own named contact, not all
records an administrator can view. Contact metadata does not create a Task or a private audience.
Current revisions excludes archived/superseded records but may include Draft and Withdrawn states.

Cards display source-file count, expiry and recorded contact. The saved record places **Source
files & photographs** near the top, with a direct Source files action. Full dates, scope/conditions,
notes, equipment links, revisions, linked Tasks and Record PDF remain accessible. Existing viewing,
editing and export permissions remain separate; a permissioned non-admin can edit as before.

History now calls the implemented exact-record endpoint instead of the nonexistent reversed URL.
It displays retained named before/after evidence, with no new signature or publication action.

## Keep the one-page editor and your selected equipment

The existing form, equipment search, unavailable retained references, Keep draft & close and
original version checks remain. Routine draft and follow-up edits remain reason-free; recorded
source or state corrections still need a real explanation. A validated same-value save now returns
the current record without adding an edit version or audit event. Permission, type and version
checks still run. A changed equipment/contact snapshot remains a real change. An idempotent request
receipt may be recorded even when the certificate itself is unchanged.

A delayed History/directory response cannot replace a newer form. Certificate saves now carry the
original account and form through the asynchronous write-lease wait, before credentials are read.
An obsolete unsent request is refused rather than recorded under a replacement account. The same
account, request identity and existing local cleanup safeguards remain in force.

## Attach without closing another person's work

Select **Attach source file**, a file and optional caption, then **Save attachment**. File preparation
and upload are marked busy; ordinary Close/Escape and main sign-out cannot interrupt an active save.
If the response is lost, **Retry same upload** uses the exact original file, payload and operation ID.
A completed obsolete request cannot close or redraw a replacement editor, even if an unrelated
navigation has forcibly removed its original dialog. A request already sent may still commit.

The existing limits/formats remain: up to 12 attachments per revision, 20 MB each; supported original
PDF/Office/Excel files and JPEG/PNG. Original bytes are preserved, not malware-scanned or stripped of
all metadata. Treat active content/macros as untrusted. Removing a file from the current list is not
secure deletion; earlier evidence remains retained for authorised viewers.

Selected files and focused renewal/lifecycle forms are **in-tab only**, not new durable offline
drafts. Resolve an uncertain upload in its open form. Closing does not undo it; check the saved
record before starting another upload. Stored normal certificate forms still use Local forms and
the existing same-account draft/sign-out behaviour.

## Prepare a renewal, then deliberately activate its replacement

**Prepare renewal / revision → Prepare draft** now needs no generic reason or checkbox. It creates
a new Draft with copied descriptive context but blank dates/source revision and no attachments.
The earlier source remains current. Edit the new source and attach the actual replacement files.

**Review & activate replacement** shows the earlier source alongside the replacement's recorded
dates and file count. Enter the meaningful review explanation, deliberately confirm the information
and select Activate reviewed replacement. Both reviewed record versions are checked; a changed
predecessor requires a fresh review. Old-client API payloads retain their existing contract when the
optional predecessor-version field is absent. Competing activations remain refused server-side.

Activation supersedes, not deletes, the original evidence. Archive/Restore and file removal retain
meaningful explanation requirements. An active register state is not issuer authentication or an
equipment-release approval; unknown expiry and a missing original remain explicitly unknown/missing.

## Stable updates and readable reports

The register keeps keyed cards, query/contact selections and reading anchors through ordinary
updates. Changing accounts/projects resets filters. A temporary failure labels the **Last saved
certificate view** and blocks stale record actions until Refresh. Definitive access denial clears
protected background content even when an editor intervenes, without deleting its local wording.
Normal global session-expiry rules still apply; removed anchors can limit exact scroll restoration.

UI55's quiet cached writes, real save warnings and synchronization remain. Approved Home, Tasks,
Checklists, Logs, Handovers, Calendar, Inventory and Maintenance behaviour is retained, apart from
narrow shared certificate guards and literal asset-cache wiring.

Record PDF remains a per-revision register report: original PDFs/Office files are listed, not merged.
The files heading now stays with its table. The exact same fictional record remains two pages, with
all report words and embedded image bytes retained; the heading/table now both start on page two.
No universal page-count reduction or long-volume pagination acceptance is claimed.

## Desktop icon / reopening: recorded, not silently implemented

The user reports the installed desktop shortcut still has the old icon and repeat launches open
multiple windows. The installation method is not yet established: browser Install app versus a
native Windows executable needs a different fix. The current source already contains the approved
website-derived icons, but the actual installed shortcut target/cache was not inspected.

Preferred behaviour: focus/restore the existing main window without reloading or closing it and
risking unsent work. Scope reuse to the correct company/origin/profile, keeping the independent demo,
Sulmara and explicitly requested separate log windows distinct. Do not kill unrelated processes,
clear browser storage or force an uninstall. Existing PWA identity/start URL/scope, icon bytes and
native installer sources are unchanged in UI56. No Windows executable was rebuilt or tested.

## One acceptance session

With fictional records and a permitted named editor, open Current/Due soon/Drafts, search, open a
record and its source files, then History. Keep/resume a draft, upload a source, prepare a replacement
and review/activate it. Open the earlier source and history to check retained evidence, then export.
Let another person update a different certificate while you read lower down; check the same route
on your phone. Use only disposable data for permission changes or interrupted-save testing.

## Verification and limits

**383 selected Python tests, 59 compound browser checks and 80 JavaScript syntax checks passed.** All 193 application Python modules parse; 191 remain unchanged. The frozen runtime has 1852 tracked files. Python groups: certificates_py=109, preserved_py=96, hosting_py=178. Browser groups: certificates_browser=15, maintenance_browser=18, refresh_browser=26. Nine additional integrated service/report checks passed, including same-record PDF comparison. Selected checks, not full-suite acceptance.

The same-record PDF comparison retained all words and image bytes and confirmed the heading/table
move together. Final preview pages were rendered and inspected. One historical Maintenance test
still hard-codes the UI54 shell cache and also fails on untouched UI55; it remains explicitly
excluded, not reported as fixed. Three native-window tests could not initialise Tk in the initial
headless run and are outside the final selection. Preliminary fixture errors, a collection-path
typo and pre-freeze cache-reference alignment failures are retained separately, not counted as passes.

Browser tests use shipped assets, actual fictional SQLite/TestClient APIs, injected fetch/hash
routing and staged in-memory storage. They are not live Sulmara, real navigation/IndexedDB durability,
service-worker lifecycle, physical device, Windows/PowerShell/native, full-suite, production-security,
load, accessibility, Docker or off-host recovery acceptance. C01/G01 startup and all normal account
permissions are preserved. Certificates Help is updated; 75 other article bodies are unchanged and
all 76 catalogue entries match. Native/master guides are not rebuilt.

**Nothing has been pushed or deployed from here.**
