# Wavelink — Workspace UI18

**Core 1.34.19 · cumulative UI01–UI18 · prepared 25 September 2026.** Built from the verified supplied complete UI17 archive, not from a fetched live repository. Implemented and tested locally; not deployed to Render.

## Original files now have shared folders

In the existing browser **Workspace menu → Original files**, open the new saved library. It stays in the current application and project. Close an unfinished operational form before opening the library; opening Help does not submit or replace that form.

The folder pane has **All files**, the **Original files** root and nested saved folder paths. Search matches title, code, revision, original filename and folder path across the entire library, even when a particular folder had been selected. Each result shows its saved location. **Include archived revisions** is explicit; archived revisions are not deleted files.

Counts refer to individual stored revisions, not document families. Folder counts are direct contents under the current archived filter, not subtree totals. **Details** shows the exact revision/family IDs, file size, checksum and import information. **Open / save original** keeps the existing authorised, checksum-checked file download.

The phone layout has a collapsible **Browse folders** pane; the dialog scrolls. Desktop keeps folders alongside the file cards. Local Chromium renders at 390 and 320 pixels are included; they are not physical-phone acceptance.

## Reviewed organisation, not automatic classification

A named project administrator with the existing Original files access can create a folder, rename it, move it under another folder or remove it only when empty. An archived revision or a child folder still counts as content for removal. This library has no file-delete button.

Administrators can select and move up to **100 exact revisions** together. Each selected revision can have its own location: moving revision A does not move revision B or all members of the family. Switching a folder, search or archived filter clears the selection so hidden items are not moved inadvertently.

Every change follows **Choose the change and reason → Review exact scope → Confirm → Save folder change**. The preview states the current/destination paths and exact revision IDs when files are selected. Folder rename/reparent reviews state their descendant-path impact. Going back clears confirmation. Reasons can contain ordinary line breaks and are limited to 1,000 characters.

Folders are project-shared metadata, not private browser preferences or physical filesystem directories. **A folder is not a permissions boundary.** Existing viewers retain the existing Originals permission; organisation and **Folder history** require a current named administrator. Vessel-only and unauthorised sessions do not gain access. There is no new role or permission toggle.

The limits are **200 folders**, **six levels below the library root** and **100 revisions per move**. Folder names are one segment, not paths, and sibling names cannot differ only by case/Unicode composition. Cycles and moves that push descendants beyond the depth limit are refused. There are no automatically created folders, inferred categories or automatic revision moves.

## What is preserved

Folder operations do not rewrite original source bytes, filenames, stored document rows, revision/family IDs, checksums or published checklist source references. They write separate location/folder metadata and append audit records. Existing audit entries remain. A folder move does not revise, approve or publish a linked checklist.

**Folder history** shows the latest 100 saved organisation operations, with administrator identity, reason and before/after paths or affected exact revisions. Older operation records remain in storage; the current view is limited to 100. Moving a revision also appends its existing original-document audit. Renaming a parent is recorded as a folder operation with affected paths, not a fabricated content revision for each child.

Initial startup adds empty folder tables without classifying existing files. Originals without a location appear in the root. The local upgrade test opened a real UI17-created project using UI18 and checked unchanged original rows/audit, exact bytes and empty new metadata. A restart test and selected transfer tests also ran locally; this is not a live-service or off-host restoration test.

## Saved snapshots, connection failures and unfinished work

Reading the library is read-only. Changes require a connection to the current project hub and its current saved catalogue snapshot. A concurrent import, archive, deletion or organisation change refuses an older proposal as a whole. Refresh and review it again; no subset of a refused bulk move is applied.

An operation ID makes a repeated identical request return its recorded result rather than apply a second mutation. A lost response is an **unconfirmed outcome**, not proof that no change was saved. The open form retains that exact request and offers **Retry same operation**. After a confirmed response the library reloads its saved state. A failed reload is distinguished from a failed save.

This editor does **not** add an offline queue or persistent browser draft. Do not close an unconfirmed operation casually. Closing an unsaved/uncertain proposal asks first. After a tab or browser is lost, inspect the saved library and administrator history before proposing a replacement action. A replay acknowledges the original recorded operation; it does not recreate something subsequently changed or removed.

Account, token, route, project and dialog guards prevent new stale actions and delayed reads from replacing other work. Duplicate save and ordinary Close/Escape are blocked while saving. Already-sent actions can still complete. Unrelated operational drafts, checklist queues and conflict handling are not changed.

## Uploads, revisions and project transfers

This release organises **already stored Originals**. It is not a new browser uploader, universal attachment manager or native folder editor. Existing Add original, Add revision, source-linking and lifecycle tools keep their previous locations and rules. Newly imported originals/revisions start in the library root and can then be organised explicitly. Destination choice during upload and native folder-authoring remain follow-up work.

Complete project transfers retain folder metadata. Selected workspace exports/imports that include the **documents** module retain its folders, locations and history; excluding documents omits them together, not as orphaned folder records. Reusable setup/template exports retain their existing format and do not carry shared folder organisation. This is not vessel/cloud synchronisation.

## Server changes in this release

Unlike the preceding static-only increments, UI18 includes a small server extension. Three existing Python files change: `app/original_documents.py`, `app/project_modules.py` and `app/server.py`. Two modules are added: `app/original_folders.py` and `app/original_folders_api.py`. The other **173 existing application Python files remain unchanged**.

Normal store startup ensures three additive tables: `original_document_folders`, `original_document_locations` and `original_document_folder_audit`, with a sibling-name index. Authorised explicit organisation writes are transaction-scoped and audited. The new catalogue/history/organisation endpoints are under the existing Original documents permission route; existing file/list endpoints and document-reference formats remain unchanged.

All source changes are carried by the cumulative verified extractor. Among existing executable files in **UPLOAD_TO_GITHUB**, only `deploy/extract_source.py` changes. Hosting gateway, guest configuration, supervisor, Dockerfile, dependencies, source parts, fictional seed and recovery helper remain byte-identical to supplied UI17. No new production dependency is added. The core version remains **1.34.19**, with the deployment variant identifying UI18.

## Help and retained workflows

**Original files Help** is reviewed against this release, including browser/native distinctions, exact revision moves, permissions, saving/retry and transfer limits. The other **75 article bodies remain unchanged**, including the four previously reviewed topics. There are now **five distinct bounded wording-reviewed topics**: daily, records, maintenance, dashboard and originals. The remaining 71, broader entry-point/authoring/accessibility acceptance, native Help and master PDF still need review.

Home remains **UI13**; the standalone checklist stage remains **UI09**, result editor **UI16**, and approval/readiness/finalisation guides **UI17**. Earlier maintenance, inventory, boxes, shipment/receiving and administration work remains cumulative. No native vessel installer or CCVD component is changed.

## Update through the existing GitHub Desktop workflow

1. Preserve unfinished work in every browser and separate log window, the previous approved commit and the established project backup. Preserve outside edits and fetch/pull the intended branch in the existing Wavelink checkout. The ZIP is source and fictional fixtures, **not a current live-project backup**.
2. Extract the full ZIP. Copy the **contents of `UPLOAD_TO_GITHUB`** into the repository root, preserving subfolders and `.git`. Do not upload the enclosing folder, `REFERENCE_ONLY`, `PREVIEWS` or `VALIDATION` as application files.
3. Review the changes, commit and **Push origin**. Reconcile outside modifications before overwriting anything. Deploy the approved commit to the existing Render service outside a presentation.
4. Keep the current domain, secrets, guest settings and persistent disk, with:

```text
PUBLIC_URL=https://demo.mywavelink.com
INITIALISE_FICTIONAL_DEMO=NO
```

Keep the initial-admin bootstrap removed. Expected extraction output:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 18: shared original-file folders and reviewed Originals Help; includes UI01-UI17; no automatic document classification.
```

After healthy startup, open **Workspace menu → Original files** and look for **WORKSPACE UI18**. Home still has its earlier badge. Preserve unsent work before reopening older tabs for the service-worker update. **Do not clear site data, reset the project or re-import the demo.** Existing files initially remain in the root until explicitly organised.

## Rollback and acceptance

The exact UI17 extractor is included at **`REFERENCE_ONLY/Workspace_UI18/rollback/deploy/extract_source.py`**. Reverting the extractor returns the old flat library; it does not reverse folder changes or remove the new metadata. UI17 does not display these folders. Its selected-workspace exporter can refuse unknown UI18 tables: do not delete metadata or weaken transfer checks to force an older export. Return to UI18 or use an accepted complete-project backup process. Never reset the disk to roll back an interface.

After deployment verify normal/guest/restricted entry; reader versus administrator controls; file details/download; at least one reviewed fictional folder/revision move; a stale review; saved history; and persistence through a deliberate service restart. Check the existing inventory, receiving, maintenance and checklist workflows. Test real phones/Windows and the intended project-transfer procedure. A restart check is not an off-host recovery acceptance.

The original pristine-source recovery helper remains **unapproved for the overlaid runtime**. Do not bypass its checks. Preserve browser-only unsent work separately; a server backup does not include it.

## Local validation

**534 selected Python cases, 268 compound browser checks and 47 JavaScript syntax checks passed** in the final selected runs. All 178 application Python modules parsed. The new folder tests use real temporary SQLite projects and TestClient HTTP; browser tests use local Chromium with shipped scripts/styles, fictional projects and injected in-memory browser persistence. Actual old/new store startup and selected project transfers were exercised. The archive and fresh-extraction byte proof are in the external final ZIP verification JSON.

Preliminary/incomplete harness attempts are retained separately and excluded from passes. This is **not the full product test suite**. No live GitHub fetch/Render deployment, Docker build, physical phone/Windows, durable browser storage/service-worker lifecycle, full accessibility, production-security/isolation or accepted off-host restoration is claimed.

Next: hosted/user feedback, browser upload with explicit destination and revision workflow, native-folder/attachment scope decisions, and further bounded Help review. These are recorded development steps, not background work running after this delivery.
