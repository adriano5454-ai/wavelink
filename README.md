# Gateway addition G01 — optional public guest entry

This repository is **Workspace UI19 + Gateway G01** (core 1.34.19). For password-free
entry by fresh visitors, deploy this code and explicitly set **DEMO_PUBLIC_ENTRY=YES**.
Default is NO. Keep DEMO_ACCESS_PASSWORD and the matching Wavelink guest credentials
configured. Public visitors get the existing non-administrator guest's actual rights,
not automatic read-only access. Normal staff entry remains at `/__demo/login`.

Read [G01 setup, source checks and boundaries](docs/GATE_PUBLIC_ENTRY_G01.md) first.
G01 changes only the deployment gate and supervisor; it does not change UI19's
application, database or initialization. The UI19 notes below remain historical
application-release documentation, not a claim that its old tests were rerun for G01.

---

# Wavelink UI19 — small GitHub update

Core **1.34.19**. Prepared **25 September 2026**. This is a changed-files update, not a full repository and not a live backup.

## Required baseline — check before copying

This release continues only from the actual UI18 archive Adriano supplied, whose extractor SHA-256 is:

`d63d6de8b7b076893e44c8faf5122be5ac136539685d7744a44adae85b01d980`

The other previously reported UI18 extractor (`ee322dc48e08a29a284066e10bb9cb7e2396100c4b5348d521ec08f6966ebc5d`) is **not this baseline**. UI19 does not silently reconcile it, downgrade it, or migrate its different folder schema. A UI18 label alone is not sufficient. Do not apply to UI17, the other UI18, a newer release or an independently modified checkout.

The included read-only **CHECK_UI19_UPDATE.ps1** checks the complete expected repository baseline, not just the version label. It accepts exact bytes or UTF-8 text differing only by Windows CRLF line endings; binary source parts always require exact bytes. It does not copy files, edit data, connect online or deploy anything. Run it from an extracted patch folder under your approved PowerShell policy:

```powershell
.\CHECK_UI19_UPDATE.ps1 -RepositoryPath "C:\path\to\your\wavelink" -Mode Baseline
```

A failed check means **stop and reconcile the identified source differences**. Do not reset the repository, discard outside edits or edit database tables to bypass it. If your checkout is already UI19, use `-Mode Installed` instead. PowerShell itself was not executable in the Linux test environment; the checksum manifests and matching reference checks were tested, not native Windows execution of this helper.

## What UI19 adds

Open **Workspace menu → Original files** as a permitted, named project administrator. This is the existing workspace entry in the supplied UI18 branch, not an invented sidebar replacement.

- **Upload new original:** File & document → Destination & reason → Review upload. Choose one file; enter the document information; explicitly choose Library root or an existing folder; add a reason; then confirm the final review.
- **Add revision:** use the action on the exact active original revision or its details. Enter a new revision label and explicitly choose the new revision's folder. The selected document family is fixed. Earlier revision bytes, identities, folders, archives and existing checklist/maintenance links are not replaced or repointed.
- **Saved outcome:** a successful upload shows the saved revision ID, bytes, SHA-256 and destination, with an explicit link to the exact saved revision in the library.

Supported browser originals: **PDF, DOCX, PNG/JPEG, XLSX, XLSM, XLSB, XLS, XLTX and XLTM**, one file from **1 byte to 20,000,000 bytes (20 MB)**. Excel shares this browser limit; the existing native-admin Excel import still allows its existing 100 MB limit. The browser requires its normal HTTPS/localhost file-digest capability; it does not bypass insecure-origin restrictions. Upload is a byte-preserving library operation, **not** checklist extraction, publishing, approval, a macro/virus scan or a certification that the document is safe/current.

Folders are not access-control boundaries. Existing Original documents access, named-admin upload authority and exact-project checks apply. No new role or permission is invented. Archived parent revisions cannot be used for Add revision. New files are not automatically filed, linked to equipment, made active procedures or assigned to Tasks.

## Unfinished work, uncertainty and retries

The selected file and form are **memory-only**. They are not an offline draft and are never put into the checklist outbox. Closing asks before discarding; ordinary Close/Escape and duplicate submissions are blocked during file preparation or an explicit save. Reloading, crashing or losing the tab can still lose this unsent upload form. Other operational drafts/queues are not cleared.

Changing the review clears confirmation. A stale library snapshot is refused without creating a partial original; refresh the review and confirm again. File bytes, chosen location, original audit and duplicate-request receipt commit together in the existing database transaction. No UI19 tables are added.

If the response is lost, the hub may already have saved the upload. The open form retains the exact request/reference for **Retry same upload**, or **Check saved upload outcome** without resending the file. A matching explicit receipt lookup may settle only this upload's local warning, not unrelated warnings. No visible receipt yet is **not proof of failure**; a request may still be running. Do not start a replacement upload merely because a response was lost. Once the tab/request has been lost, inspect the saved library and audit before starting different work.

If local receipt storage fails before sending, the form says the upload was not sent. If the hub has saved but local warning storage fails, the confirmed hub result and remaining local warning are distinguished. The retry cache is not portable across selective project/workspace transfers; those retain document bytes/folder audit but clear operations. Do not replay an old upload into a transferred or restored project.

## Apply after a passing baseline check

1. Preserve unfinished browser and separate-log-window work, a complete approved project backup, the current approved Git commit and any outside/uncommitted edits. Deploy outside an operational presentation. A source ZIP and a browser-local recovery export are not complete live-service backups.
2. Copy the **contents of this patch's UPLOAD_TO_GITHUB** into the existing repository root, preserving the subfolders. **Do not replace the repository with this small patch and do not delete files missing from the ZIP.** There are no required deletions, dependencies, environment changes or UI19 table additions.
3. Check the installed files with `CHECK_UI19_UPDATE.ps1 -RepositoryPath "C:\path\to\your\wavelink" -Mode Installed`. Review the Git diff. Only `deploy/extract_source.py` changes among existing executable repository files; application changes are embedded there. Other changed/new files are current instructions/provenance/checksums.
4. Commit and push the reviewed change through the existing GitHub workflow; deploy the intended commit through your established service. This package has not pushed or deployed anything for you.

Preserve **https://demo.mywavelink.com**, current passwords/secrets, guest settings, persistent disk, `.git`, outside changes, and:

```text
PUBLIC_URL=https://demo.mywavelink.com
INITIALISE_FICTIONAL_DEMO=NO
```

Keep the initial-admin bootstrap setting removed. **No reset, demonstration re-import, category reset, browser-storage clearing or domain change.** Preserve unsent work before the normal browser/service-worker update; actual service-worker lifecycle acceptance remains outstanding.

Expected build message:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 19: browser original uploads, new revisions and reviewed destination; supplied UI18 lineage; no new tables or automatic document changes.
```

Original Files shows UI19. Home stays UI13; existing checklist/maintenance badges retain their earlier versions. UI19 retains the supplied UI18 folder semantics, not the other unrecovered variant's descriptions.

## Schema check and rollback

Before ordinary Store initialization writes, a read-only guard refuses the known alternate UI18 folder tables or incomplete/unexpected versions of the supplied folder schema. It is a safeguard, not a general migration tool, database-history proof or off-host recovery acceptance. A refusal means stop and restore the previously approved source/deployment path without resetting data, then reconcile the actual source/schema.

Rollback source: your preserved matching supplied-UI18 Git commit, not the unrelated UI18 report. UI19 adds no tables; originals explicitly uploaded during UI19 remain in the library after rollback and are not erased. A local fictional source-upgrade/rollback read check passed, but this is not a complete live/off-host restoration drill. The old pristine-source recovery helper is still unapproved for the overlaid runtime; do not bypass its checks.

## Validation and boundaries

See `DELIVERY_CHECKS.json` and the separate final packaging report for the completed selected test groups. Local browser tests used delivered assets, fictional SQLite projects and real local TestClient-backed API handling, with injected fetch, in-memory browser persistence and injected SHA-256 because managed Chromium blocked URL navigation. They do not establish native hosted WebCrypto, TLS, durable storage, physical-device or service-worker acceptance. Partial/failed preparatory runs are excluded.

No full-product suite, Docker image, live GitHub/Render deployment, real phones/Windows, malware scanning, load/security/company-isolation/full-accessibility acceptance or accepted off-host recovery is claimed. Backend changes are limited to three existing modules and two new upload modules; the other 175 existing application Python modules are byte-identical to the supplied UI18. Hosting, gateway, guest bootstrap, dependencies, source parts, seed and recovery helper are unchanged. Native vessel UI and CCVD remain out of scope; no vessel/cloud synchronization.

Originals Help is re-reviewed. The other 75 instructional article bodies remain unchanged (shared reader cache URLs update); five distinct topics are wording-reviewed and 71 remain, plus native/master-PDF and wider entry-point work.

Next: actual hosted Home/inventory/Originals feedback; continue the Help review and remaining workflow refinements. Native folder authoring, broader attachment/import formats, production readiness and the retained larger roadmap remain separate work. Development is not running automatically in the background.
