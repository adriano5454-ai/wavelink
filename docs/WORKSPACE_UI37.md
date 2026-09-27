# Wavelink UI37 — simpler certificate register

**Core 1.34.19 · UI37 · G01 unchanged · 26 September 2026.** Compact changed-file update
for exact **UI36 + working G01**, based on the actual uploaded UI30 repository and verified
UI31–36 lineage. Not a complete repository or a live-project backup. Nothing deployed here.

## Copy / GitHub Desktop / push

Preserve unsent work, your approved commit and complete project backup. Extract the ZIP.
Copy **everything inside UPLOAD_TO_GITHUB into the existing UI36 Wavelink application
repository folder**, replacing matching files. Review in GitHub Desktop, commit and
**Push origin**, then deploy the intended commit through the established service workflow.
Do not replace the whole repository, delete absent patch files or use the separate website repo.

The **CHECK_UI37_UPDATE.ps1** file is optional read-only checking, not an installer or a
required extra upload. No new environment variables, dependencies, permissions or tables.
Keep G01, DEMO_PUBLIC_ENTRY=YES, INITIALISE_FICTIONAL_DEMO=NO, required gate secret, matching
non-admin guest, named administrator, existing domain/disk and removed bootstrap unchanged.
No reset, re-import or browser-storage clearing. Keep UI34+ compatible evidence writers/exporters.
Reconcile independently changed source rather than overwriting it.

## One page to add or edit a certificate

Open **Certificates → Add certificate**, or a saved record → **Edit certificate**.
The old five-step wizard is replaced by one scrolling form and **Save certificate**.
Title, source number/issuer/revision, dates and notes stay together; optional scope/conditions,
exact equipment links and responsibility/follow-up expand only when needed. No Next/Back
sequence or routine review checkbox. New records start as Draft unless another state is
explicitly selected. Opening the form creates nothing.

## Exact equipment without losing selections

Expand **Linked equipment** and search by name, serial, asset reference or ID. Search only
hides rows: selected records remain selected. The total selected count is separate from the
number of visible results. Up to 50 exact links, optional; names do not infer an identity.

Existing links and saved local selections missing from the refreshed directory remain
visible as retained references. They are not silently erased or replaced. The service may
refuse an unavailable newly selected item; unlink it explicitly only when appropriate.
Retained responsible-person/department choices are also identified rather than defaulted away.
A contact assignment grants no permission and creates no Task.

## Ordinary edits need no explanation

**Draft edits** need no reason while the record stays Draft. **Working notes, responsibility,
due-soon window and renewal target** can be changed on recorded/withdrawn records without a
reason. The existing actor, timestamp, version and before/after audit remain. No invented
reason is written for you.

A genuine **Correction note** appears for source corrections to a recorded/withdrawn record
(title/number/type/issuer/revision, source dates, inspection date, scope/conditions, exact
asset links), or any existing record-state change. Correcting issuer evidence is different
from updating your own administrative follow-up. Earlier actual reasons in local drafts
remain available as optional text; they are never discarded just because no longer required.
Replacement revision, activation, archiving and attachment-removal safeguards are unchanged.

## Dates and source files remain explicit

Unknown expiry stays unknown. Use **Source explicitly declares no expiry** only when the
source says that. Choosing a different expiry basis never silently deletes a date: an
explicit **Clear the recorded expiry date** action is offered when required. Source date
ordering/limits are still validated; no expiry is calculated or extended automatically.
The due-soon window is an in-app date status, not an automatic email reminder.

Save the record, then use its existing **Attach certificate file** action. This release
changes neither file limits nor file permissions and adds no combined upload or QR signing
for certificates. Existing files remain tied to their saved record; a replacement revision
does not automatically copy their evidence. The certificate register is not authentication
of the source or approval to use equipment.

## Local drafts, exact retries and saved destination

**Keep draft & close**, saved-form resumption and explicit discard retain existing behaviour.
Resume keeps the saved draft's original version; it does not silently rebase over newer work.
Its current directory is re-read. Conflicts keep your wording and do not overwrite the newer
record. Only the form's own corrected input warning clears; server-save errors remain visible.

After a successful save, navigation waits for shared local-draft cleanup. A confirmed hub
save followed by local cleanup failure keeps the form and the original request for retry.
A lost response also retries the same operation ID, not another record or attachment.
No timer-based navigation, autosave, new browser store or automatic reminder was added.
Preserve any unsent work. Real-device durable storage remains an acceptance item.

The one-page layout and late-response guards are for the hosted browser. Native wizard
layout and installed Windows executables are not rebuilt. Simple handovers, files, QR
signing/PDFs, maintenance, Original Files, presence, approved icons and support@mywavelink.com
are unchanged. The changed form displays UI37; other feature badges can keep their version.

## Verification

**528 selected Python tests** (437 application + 91 gateway/package),
**121 compound browser checks**, **11 actual local proxy checks**, **63
JavaScript syntax checks** and **187 Python parses** passed on
frozen source. Final archive replay verifies **1740 tracked runtime files**.
Includes 49 new backend cases and 14 certificate browser checks,
plus current asset/date status, maintenance/cycle, file, handover, signing/PDF, presence and
navigation regressions. Pure-JS/server rule parity is part of one Python test, not added counts.

Tests use fictional data, injected browser transport/in-memory persistence and local loopback.
Not full-suite, live HTTPS, real phone/camera, durable IDB, service-worker lifecycle, Windows,
full accessibility/security/isolation/load, Docker or accepted off-host recovery. Earlier
historical assertion failures were not rerun or declared fixed; preliminary failed attempts
are retained separately and excluded. No real account, project data or deployment touched.

Only **app/certificates.py** changes among existing 187 application
Python modules; one do_save reason rule plus a pure helper. The shared transaction, file,
renewal, actor/version and permission code remain. The existing executable GitHub change
is only deploy/extract_source.py. One Certificates Help article updated, 75 others unchanged;
all 76 search entries match. No native/master-guide or universal procedural review claimed.

Next: actual certificate/maintenance and phone-QR feedback first, then remaining routine
reason/click-count cleanup in coherent batches. Do not add everyday friction to handovers.
