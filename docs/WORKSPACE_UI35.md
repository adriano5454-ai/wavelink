# Wavelink UI35 — readable signing PDFs

**Core 1.34.19 · UI35 · 26 September 2026.** Compact read-only report update over exact
**UI34 + working G01**, on the actual uploaded UI30 application repository lineage.
No live deployment, main account or project data was changed here.

## Update with GitHub Desktop

Preserve unsent work, your approved commit and complete project backup. Extract the ZIP,
copy **everything inside UPLOAD_TO_GITHUB into your existing UI34 Wavelink application
repository folder**, replace matching files, review in GitHub Desktop, commit and **Push origin**.
Deploy the intended commit through the usual service. Do not replace the whole repository,
delete files absent from this patch, or use the separate website repository.
The included **CHECK_UI35_UPDATE.ps1** is optional read-only checking, not an installer.
Stop and reconcile independently edited source rather than overwriting it blindly.

No new environment variables, dependencies, permissions or database tables are introduced.
Only deploy/extract_source.py changes among existing executable repository files. The working
G01 gate.py/entrypoint.py and UI34 Nginx signing routes remain byte-identical. Keep
DEMO_PUBLIC_ENTRY=YES, INITIALISE_FICTIONAL_DEMO=NO, required gate secret, matching non-admin
guest, separate named admin, domain/persistent disk and removed bootstrap unchanged.
Keep UI34 or later for the existing invitation/evidence and handover-attachment data. No
older source rollback, table deletion, project reset, re-import or browser-storage clearing.

## One author-side download

Open your saved toolbox talk or published handover → **Invite to sign / signatures** →
**Saved signatures** → **Download signing PDF · revision N**. The button is above the list of
signatures, not buried below it. No reason field, new signing step, separate form or account.
The author needs their current named account and existing document-management access.
A visitor grant, shared public-demo guest, unrelated account or another administrator cannot
use this report endpoint to bypass the document's creator rule.

The revision opened has its own download. **Other signed revisions** is collapsed; choose
an older revision explicitly. If the current revision has no invitation signatures, that is
shown instead of automatically exporting an older version. Up to200 recent signed revisions
are listed, with a clear bound; the exact opened revision is counted independently.

The PDF contains a participant summary, saved account or self-declared visitor names, saved
acknowledgement timestamps, optional drawn marks, and the exact displayed document wording.
It uses the existing selected company PDF branding profile when applicable. Signatures retain
their saved names rather than silently using a renamed account's current directory entry.
A previously recorded ordinary acknowledgement keeps its actual older timestamp and method;
no new drawing or signature time is invented by exporting it.

Where some participants were offered the published attachments and others were not, separate
**Read sets** show the scope each acknowledged. Only the offered set includes its filenames,
IDs, sizes and fingerprints. File bytes are not embedded or re-downloaded. The full-source
and displayed-snapshot fingerprints are distinguished; an unshared attachment is not claimed
as seen. The report never substitutes the author's newer private draft or a later publication.
An older selected revision has an explicit historical notice.

## Evidence boundaries

This is all invitation signing evidence for that selected revision at the recorded snapshot,
not the complete normal attendee roster. Acknowledgements performed solely outside the QR
invitation feature are not silently added. Named account and **Visitor / self-declared** are
separate labels. No drawn mark is shown honestly as no drawing supplied, not a blank signature
presented as evidence. Drawing alone does not verify identity or physical presence.

The PDF is a separate **signing report**. Ordinary toolbox/handover PDFs and their existing
scope remain unchanged. **Raw evidence → Download signing evidence (JSON)** retains the original
technical archive with exact snapshots and drawing coordinates. It is not replaced by the PDF.

Downloading does not sign, add an attendee, publish, acknowledge, change permissions, finish
work or close invitations. Saved evidence can be exported after invitations end or the record
is archived/finalised, as long as the author still has current permitted access. Access is
rechecked after rendering; failed or inconsistent evidence produces an error, not a partial
report. A failed download uses the same button for a simple retry. Closing the panel or changing
account/route during preparation prevents the delayed download from continuing in a new view.

Share exported PDFs only with authorised people. A downloaded copy cannot enforce later access
revocation. The PDF is not digitally certified or tamper-proof; its printed SHA-256 values
identify the saved JSON snapshots, not legal identity, attendance or operational approval.

A PDF contains one revision up to300 invitation signatures. More than300, over1MB of snapshot
wording or over16MB generated output is refused without silent truncation; use the JSON archive
or a separately reviewed larger export. JSON retains its own latest2000 limit with explicit
counts/truncation. Two simultaneous report renders and six author requests per minute are local
safety bounds, not production-load certification. Characters outside the installed report font
are displayed as explicit [U+code] notation; exact original text remains in the JSON evidence.

## Preserved workflows

UI34's five-minute QR and document-only named/visitor access, optional marks, timeouts,
revocation and atomic same-request signing remain unchanged. No additional joining or signing
questions. My shift, people assignments, reason-free Save & close / first Finish handover,
photo/file privacy, Original Files, presence, website icons and support@mywavelink.com remain.
Unsent notes/files still need the existing explicit save; this is not offline autosave.

## Verification and limits

**358 selected Python tests** (267 application + 91 gateway/package),
**92 compound browser checks**, **11 actual local proxy checks**, **62
JavaScript syntax checks and 187 Python parses passed on the frozen source.
1730 tracked runtime files verified. Three existing application Python modules
change (read-only invitation options/route plus narrow PDF response headers); one new report
module; 183 existing modules unchanged. All invitation writer/entry/signature
methods except the read-only options method remain byte-identical. Three Help article bodies
updated and73 unchanged; all76 search catalogue entries match.

Tests use temporary fictional SQLite/TestClient, shipped browser assets and injected
transport/storage via set_content. Local Nginx/G01/core HTTP is not live HTTPS or Render.
No full-suite, real-phone camera, durable IndexedDB, service-worker, Windows/PowerShell,
full accessibility/security/isolation/load, Docker, email or off-host recovery acceptance.
Earlier historical assertions were not selected or declared fixed. Partial/fixture attempts
are retained separately and excluded. Final ZIP replay is reported separately; repeats are
not additional coverage. Nothing was pushed to GitHub or deployed to Render from here.

Next: real-phone invitation/read/sign/download feedback, then the retained cross-module
routine-reason cleanup and practical click-count reductions. Do not add review-heavy daily
handover forms. Maintenance, individually issued QR invitations and organiser admission checks
remain separately scoped future work. Native vessel/CCVD and cloud sync remain outside scope.
