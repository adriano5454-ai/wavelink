# Wavelink UI41 — restore choices, separate Help and manage local work

**Core 1.34.19 · UI41 · working G01 unchanged · 26 September 2026.**
One combined usability fix on the matching **UI40 + G01** repository. Easier to use means
clear choices and discoverable capabilities, not removing options or hiding them in menus.
No live site version or account permissions were inspected. This is a patch, not a full backup.

## Install once using GitHub Desktop

Preserve your complete project backup, approved commit and unsent browser/separate-log work.
Extract the ZIP and copy **everything inside UPLOAD_TO_GITHUB into your existing UI40 application
repository folder**. Replace matching files, review in GitHub Desktop, commit and **Push origin**.
Deploy the intended commit using your established workflow. This is not the separate website repo.

Do not replace the entire repository or delete files absent from this patch. The included
**CHECK_UI41_UPDATE.ps1** is optional read-only checking, not an installer or required upload.
Reconcile independently changed source rather than overwrite it. Keep the working G01, domain,
persistent disk, named administrator, required access password, matching non-admin guest,
removed bootstrap, **DEMO_PUBLIC_ENTRY=YES** and **INITIALISE_FICTIONAL_DEMO=NO**.
No reset, demo re-import, browser-storage clearing or old evidence-table deletion.

There are no new backend APIs, tables, permissions, dependencies, environment variables or
storage migrations. Optional local ownership/delivery hints are added without a new object store
or browser database version. All 188 application Python modules are unchanged.

## New task: the choice panel is back

**Tasks → New task** and the Home task shortcut open a square/card choice panel:
**General task · Verify inventory · Maintenance activity · Certificate check**.
General task, Maintenance activity and Certificate check retain their appropriate single-page
creation forms. Choosing a card creates
nothing by itself. No routine reason or extra review page was added to them.

**Verify inventory** opens the original inventory-specific workflow: choose the inventory,
assignees and exact items/boxes/sections to verify. It is not a generic Task relabelled as stock
verification. Normal inventory viewing/task authority still applies. A missing inventory permission
is explained on the disabled card, not hidden. Assignment does not mark stock verified.

## Create handover is visible again

The **Create handover** button is directly in the Handovers heading, not tucked in More.
Its choices are **My assigned shift**, **Daily / shift handover**, **Full-hitch handover** and
**Prepare from previous**. The assigned option uses the simple reason-free note editor and reopens
an existing matching handover instead of duplicating it. Where assignment/setup is unavailable,
the card explains why; other permitted handover types remain accessible.

Custom periods and historical-copy preparation retain their existing review/source rules. The
simple **Save & close / Finish handover**, current People & shifts setup, private notes and exact
previous publication references are unchanged. These entry points do not grant extra permissions.

## Help opens separately

Main/account, module, form and Help-search links open a separate browsing context, with opener
isolation, leaving the working tab and its unsent form untouched. **Setup & offline help** also
opens the relevant Help page instead of replacing the working dialog. In-page section links stay
in the Help tab. Browser preferences determine tab versus window; the application requests a new tab.

The actual installation prompt remains the installation prompt. The isolated QR document-signing
page and its token/session behaviour are unchanged. Native Windows Help was not rebuilt.

## Manage unsaved work in one place

Open **Manage unsaved work** from Home, Account, or **Connection & saves**. Existing operation/log
draft lists also link to it. It lists supported entries for **your named account in this main
browser workspace**: saved operation forms (including Task/certificate/maintenance forms), log
drafts, checklist item drafts, new-checklist/dive drafts and queued checklist results.

Select entries or choose **Discard all eligible**, review the exact list and confirm once.
No typed reason, no opening each draft to remove it. Selection starts empty; Cancel removes nothing.
Only those local copies and files held inside them are removed. Hub-saved records, published files,
signatures, personal-account identity, save receipts, other-account drafts and unknown local fields
are preserved. Discarding a local copy does not reverse a completed server save.

Active/in-flight or uncertain saves remain protected. Some older unowned drafts and queues whose
send status is unknown require review in their original workflow first. **Connection & saves**
provides that evidence; clearing a warning does not prove the request failed. The list explicitly
shows protected entries rather than offering an unsafe delete-all button.

The current account, every selected fingerprint and the browser-write lease are rechecked. One
readwrite transaction removes the selected stored batch; a changed entry, lost lease or aborted
transaction leaves that batch untouched. Automatic checklist delivery pauses while the manager is
open. No operational HTTP mutation is sent by batch discard.

**Scope matters:** unsaved text only in an open form, private drafts already saved on the hub,
separate log-window stores and other devices are not in this list. Keep or close the active form
first. It is not a cross-account wipe, a way to delete saved handovers or a browser reset.

Under **Scope, protected work & recovery**, the existing recovery export remains available. It
contains the broader main workspace and may include other accounts' retained data. Treat it as
sensitive; it is not a complete project backup or an accepted automatic restore process.

## One short acceptance session

Use a named account with normal creation permissions and fictional records. Open New task and
choose Verify inventory; check the inventory/people/scope controls. Open Create handover and
choose your assigned shift or another type. While a form contains unsaved wording, open its Help
and confirm the original form stays put. Keep a disposable operation draft, then use Manage
unsaved work to cancel a selection, discard that one test entry and check the remaining work.
Test Discard all only with disposable eligible entries after reviewing the exact confirmation.
No extra installation is needed between these checks.

## Verification and limits

**867 selected Python tests** (776 application + 91 gateway/package),
**199 compound browser checks**, **11 actual loopback gateway/core checks**,
**68 JavaScript syntax checks** and
**188 Python parses** passed on the final frozen source.
Final replay verifies **1766 tracked runtime files**.

The new browser checks create a real fictional inventory-verification task and inspect it as the
assignee, open all handover choices, preserve an unsent form while opening Help, and exercise
selective/all/cancelled discard, transaction abort, lost lease, changed account, stale fingerprints,
protected uncertainty and narrow layouts. Other modules' existing regression checks were retained.

Browser transport uses fictional SQLite/TestClient and injected fetch/in-memory state. Bulk local
writes use a controlled staged transaction/lease fixture, **not durable real IndexedDB acceptance**.
Real navigation is blocked by this environment's browser policy; it was not weakened. No live
HTTPS, physical-device, service-worker lifecycle, full-suite, full security/accessibility/load,
Windows/PowerShell/native binary, Docker or accepted off-host recovery claim. Two old release-hash
assertions also fail on untouched UI40 and are explicitly excluded, not counted as passes.
Earlier partial/failed/refinement runs are retained separately and add no coverage.

**Nothing was pushed to GitHub or deployed to Render from here.** Rollback of source cannot
restore deliberately discarded local entries. Keep UI34+ compatible evidence writers/exporters.
The next direction remains user-friendly workflows with clear choices, not fewer capabilities.
