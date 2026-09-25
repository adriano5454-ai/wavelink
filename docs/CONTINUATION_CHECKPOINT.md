# Wavelink development checkpoint — UI19, supplied UI18 branch

Prepared 25 September 2026. Core **1.34.19**. Cumulative supplied UI01–UI19; source patch **workspace-ui19-uploaded-ui18-2026-09-25**. Implemented/tested locally; no live GitHub fetch/push or Render deployment.

## Exact source identity

Parent actual supplied Full UI18 SHA-256 `627819205f83d315454a42457ac3ad1c377c4783064ac2249642a1295f53d5a2`; corresponding complete GitHub-only baseline ZIP `8c0bc3092161f463b73040af1b99bc99eec9ad34f3bdd9e77d22846778688fe3`. Required parent extractor `d63d6de8b7b076893e44c8faf5122be5ac136539685d7744a44adae85b01d980`. New UI19 extractor **`ac61f992b3f9f7b4a122b70a7b0dec59c55b5466ebce3d0bb4c92e3c0f6831fa`**.

The other previously reported UI18 extractor `ee322dc48e08a29a284066e10bb9cb7e2396100c4b5348d521ec08f6966ebc5d` remains unrecovered/unsupported. Do not reconcile by version label, overwrite it or claim its old tests. Actual supplied branch uses three folder tables: original_document_folders, original_document_locations, original_document_folder_audit. UI19 checks those exact column sets before Store startup writes and refuses known alternate original_folder_audit/original_folder_operations or incomplete/unexpected schemas. No repair/migration/table deletion.

## Implemented UI19 increment

Workspace menu → Original files retains the actual supplied UI18 workspace. Named project administrators can upload a new original or add a new revision to an exact active original's family. Guide: File & document → Destination & reason → Review upload. No preselected destination; select Library root or a current logical folder. Explicit review/confirmation is invalidated by Back, edits and refresh. Parent revision labels are not reused automatically. Existing bytes, family/revision identities, archived state, old locations and checklist/maintenance references remain unchanged. Success gives an exact saved-revision destination.

PDF/DOCX/PNG/JPEG/XLSX/XLSM/XLSB/XLS/XLTX/XLTM supported. **All browser files 1–20,000,000 bytes**, including Excel. Native Excel import retains 100 MB. Native format/magic/byte/revision-budget checks reused; not malware scanning, procedure approval or checklist extraction. Raw transport is four-byte metadata length + strict UTF-8 JSON + raw file bytes, bounded to 20,016,004 bytes without multipart/base64/dependency changes. Auth/exact project checked before reading and session/permission rechecked at commit. Snapshot conflict check, one transaction for original bytes/location/audit/operations receipt. No UI19 tables.

New original_upload.py and original_upload_api.py; existing original_documents.py, store.py and server.py changed. Other **175** existing application Python modules unchanged; total **180**. New original_upload.js, bounded library and app raw-body/receipt branch, scoped styles/cache and reviewed Originals Help. Shared save_status.js/storage schema unchanged. Explicit verified upload-receipt lookup settles only its matching uncertain upload warning, preserving unrelated warnings. Ordinary GETs do not automatically settle writes.

File/form memory-only: no offline upload queue, automatic persistence or background retry. Close/discard confirmation; ordinary Close/Escape/duplicates blocked while reading/saving. Lost responses retain exact envelope/op-ID for explicit retry or saved-outcome lookup while the form survives. No receipt yet is not failure proof. Lost tab requires library/audit review before different upload. Selective transfers retain bytes/folder audit but clear operation receipts; do not replay across transfer/restore. Preserve unrelated operational drafts/queues and account/route/session/dialog scope.

**90 incremental runtime resources, 135 cumulative overlays, 1,638 derived tracked files.** Pristine upstream remains pinned to `8c1b6a8d731d01b05a1290d3a1dd1a544054147aac9048ca345af7983613cd9e` (1,605 upstream tracked entries). Only existing executable GitHub file changed: deploy/extract_source.py. Gate/guest/supervisor/Docker/dependencies/vendor/seed/recovery unchanged. Home UI13, UI09 stage, UI16/17 checklist guides, UI14/15 maintenance and supplied UI18 folders remain included.

## Actual completed selected validation

**338 distinct selected Python cases**: upload63; actual supplied-UI18 project upgrade and source-rollback read1; folders65; records/originals/storage/transfers70; maintenance52; browser administration30; deployment57. **49 compound browser checks**: uploads21, inherited folders23, Help5 (including all76 routes without Tk imports during requests). **48 JS syntax checks** and **180 Python parses**. All final counted cases passed without skips/errors. Earlier incomplete runs, collection/fixture mistakes and fixed findings are excluded, not hidden as passes. No full-suite claim.

Browser uses actual assets and local fictional TestClient-backed server, injected fetch and in-memory persistence. Managed Chromium blocked URL navigation; tests did not weaken that policy and injected SHA-256 for about:blank. Native hosted HTTPS/WebCrypto remains unaccepted. Real phone/Windows, durable storage/service worker, native PowerShell helper, Docker, live service, off-host recovery, load/security/isolation/full accessibility acceptance remain unperformed. A selected actual UI18 upgrade preserves originals/folder/audit hashes and pinned references; source rollback reads both old/new originals. This is not full recovery acceptance.

Originals is re-reviewed; all75 other article bodies preserved, shared reader cache URLs updated outside bodies. Still **five distinct** reviewed topics (daily, records, maintenance, dashboard, originals), **71 remaining** plus native/master-PDF/wider Help work.

## Deployment and continuation

Default delivery is a small changed-files GitHub patch. Required baseline and complete target checksums plus read-only PowerShell helper are included. It accepts UTF-8 text CRLF-only equivalence, not binary differences. Helper itself was not executed on Windows; reference/manifests tested. No required deletions, dependency/env changes or UI19 table additions. Keep the full source baseline/approved Git history separately; do not re-add old screenshots/test output/rollback packages to routine updates.

Preserve demo.mywavelink.com, existing secrets/guest/disk, INITIALISE_FICTIONAL_DEMO=NO, removed bootstrap, .git/outside edits and browser/separate-log unsent work. Copy only contents of UPLOAD_TO_GITHUB into matching existing checkout, never replace the repository or delete absent files. Preserve approved project backup and commit first. No reset/re-import/site-data clearing. Rollback via preserved matching supplied-UI18 commit keeps uploaded originals; it is not migration to the unsupported branch. Pristine recovery helper stays unapproved for overlays.

Next: actual hosted feedback and continued bounded Help/entry-point and remaining workflow refinements. Native folder authoring, wider attachments/import mapping, larger Tasks/maintenance/handover/HSE/reporting/installer/security backlog remain separate. Consult DEVELOPMENT_TODO.md and existing roadmap records; do not treat basic existing modules as new. Native vessel and CCVD outside scope; phone-network diagnosis and vessel/cloud sync parked; no automatic background development.


---

# Continuation — Gateway G01, 25 September 2026

Current combined source is **UI19 + G01**, core **1.34.19**. This adds opt-in
`DEMO_PUBLIC_ENTRY=YES` for fresh anonymous guest entry at the existing root URL.
Default NO; missing DEMO_ACCESS_PASSWORD still stops startup. Keep the access
password for private entry/gate epoch, matching guest credentials, existing domain,
disk, removed admin bootstrap and INITIALISE_FICTIONAL_DEMO=NO.

Only existing executable changes are deploy/gate.py and deploy/entrypoint.py.
Public entry rejects an administrator/unknown/mismatched guest, creates no accounts
and changes no permissions. Anyone who reaches the public URL has the existing
guest's rights, possibly including writes. It is not read-only or individual visitor
identity. Normal staff entry remains /__demo/login. Public admission cookies use
a separate token kind rejected when public mode is disabled.

The public handoff atomically creates only a fresh browser main record, never
overwriting any saved record. Same-project existing auth is preserved (not
revalidated); signed-out/other-project/unknown saved work is blocked from replacement.
No site-data clearing. Existing quick-link bootstrap remains unchanged.

UI19 extractor unchanged: `ac61f992b3f9f7b4a122b70a7b0dec59c55b5466ebce3d0bb4c92e3c0f6831fa`.
G01 gate: `9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701`.
G01 entrypoint: `a2bbac57635ac6e0b12400bbcbfc7382416ed3d5c7525e4218b7e38c2e7a633f`.

Completed local selection: 90 Python tests, 13 controlled Node handoff checks,
13 local Nginx/Gate checks with a fake core service, one new JS syntax check.
Real Chromium navigation was blocked and no real-IDB assertions passed; retained
separately. Not Docker/live/full-suite/production-security/physical-device acceptance.
No GitHub/Render actions, credential edits or data changes.

Keep this gateway addition in future small updates; do not restore older gateway
files with a cumulative UI archive. Use docs/GATE_PUBLIC_ENTRY_G01.md and the G01
manifest for exact source requirements. Remaining development stays the UI19 Help,
workflow refinements and separately scoped roadmap. No background development.
