# Wavelink — Workspace UI 07: Help reader and Help review checklist

**Core 1.34.19 · cumulative UI01–UI07 · prepared 25 September 2026.** This package is implemented and tested locally, not already deployed to the live GitHub repository or Render service.

## This increment

The latest request adds a full Help-standardisation review to the development list. UI07 begins that work with a common **browser Help centre and reader for all 76 registered topic pages**. It carries forward the UI01–UI06 inventory, category, box, asset, Record management, movement, receiving and manifest changes without changing their operational code.

This is a presentation and navigation pass, **not a claim that every instruction has been rewritten or verified against the latest online screens**. Existing topic wording, steps, examples, warnings and source version labels remain. The native Help files, PDF guide, installation/support/example pages and operator documentation need their own editorial and mode-specific review. The detailed checklist is in `HELP_STANDARDISATION_REVIEW.md`.

## Open the Help centre

Use the existing **Account / workspace menu → Help / user guide**, or open `/help` on the same Wavelink site. No new login, repository, account or data import is required. The Help header shows **UI 07**; operational workspaces retain their preceding UI badges and the core version remains **1.34.19**.

The Help centre offers eight areas: Inventory & equipment; Vessels & shipments; Checklists & evidence; Tasks & maintenance; Logs & handovers; Safety & quality; Administration & documents; and Getting started & support. Its first shortcuts lead to finding equipment, receiving a shipment and managing unfinished work.

### Search guide wording, not operational records

**Find a Help topic** searches the retained topic titles and instructions. **Area** narrows the result. Clear restores all topics. Search snippets are displayed as text, never interpreted as HTML.

Full-text search loads a static documentation catalogue on demand. If it is unavailable or malformed, titles remain searchable and **Retry full-text search** is offered. This does not search inventory records, private reports, account information or uploaded documents. No operational API calls or writes are part of this reader.

### One consistent topic layout

Every registered topic now uses the same Help stylesheet and script, with a Help-centre link, grouped topic navigation, current-topic indication, readable headings and spacing, styled notes/tables/code examples and an **On this page** section list. The actual instruction text is preserved; intentional literal examples remain literal rather than being mistaken for broken formatting.

**Print this topic** opens the browser print dialog with article-focused print styling. It is not a regenerated master PDF. The existing core PDF opens separately and remains explicitly labelled as a retained reference.

The old all-in-one HTML guide is preserved byte-for-byte at `/static/help_reference.html`, rather than being deleted when `/help` becomes a topic catalogue. Existing `/help#topic` bookmarks resolve to the registered topic; the special task-details anchor retains its original-guide destination. Without JavaScript, all normal topic links and article text still work; full-text search and automatic legacy-bookmark resolution require JavaScript.

### Phone layout

On narrow screens, **Search and browse Help** begins collapsed so the guide itself is visible sooner. Expanding it exposes the searchable topic list and reference links. The selected topic loads into the same Help site. Tables own their horizontal scrolling instead of forcing the whole page wide. Ordinary keyboard focus, a skip-to-content link and a reduced-motion style are included. These checks are not full assistive-technology or physical-device acceptance.

### Read the source scope

**About these instructions** explains that some retained topics describe local Windows operation or older interface labels. Do not use old local backup/setup instructions as approval to operate the hosted demonstration. The complete local-versus-hosted wording review is pending. Viewing a guide never approves a procedure, acknowledges work, changes inventory or releases equipment.

## A narrow server-side cleanup

The public Help-topic route now reads its unchanged 76-ID allowlist from the new headless `app/help_topics.py`, rather than importing the desktop `help_ui.py` module. The route no longer needs to import Tkinter just to serve a guide. Unknown topic names still return 404; the route URL, response type and access boundary are unchanged.

The Dockerfile and Tk package installed during the earlier deployment fixes are deliberately **not changed**. This does not claim every possible desktop dependency has been removed from the application. The native Help module and all native/PDF files remain byte-identical to UI06.

## Install the complete ZIP with GitHub Desktop

1. Preserve unfinished work in every Wavelink tab and separate log window. Retain the current approved commit and your established recovery/export arrangements. Keep any uncommitted local changes before replacing files. Make the deployment outside a client presentation.
2. In the existing **wavelink** checkout, fetch/pull the intended branch. Extract this ZIP and open **UPLOAD_TO_GITHUB**.
3. Copy that folder's **contents** into your local repository root, preserving the subfolders. Do not copy the enclosing folder, delete `.git`, upload a project database, or import this ZIP as inventory.
4. Review the diff, commit, and **Push origin**. Against the supplied complete UI06 package, the only changed existing executable repository file is `deploy/extract_source.py`; documentation and checksums also change. The live GitHub tree was not fetched. Reconcile any additional outside edits before replacing them.
5. Deploy the approved commit through the existing Wavelink service. Keep the existing passwords, URL, disk, guest settings and other environment values. Keep **INITIALISE_FICTIONAL_DEMO=NO** and leave the initial administrator bootstrap password removed.
6. The build is designed to report:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 07: consistent browser Help and headless topic routes; includes UI01-UI06; no automatic data changes.
```

7. Once the deployment is healthy, reload Help and look for **UI 07**. Preserve unsent work before closing/reopening older application tabs to activate a new service worker. **Do not clear browser storage, reset the disk or re-import the demonstration.**

The full upload-ready repository is supplied for convenience. For an exact UI06 checkout, replacing just `deploy/extract_source.py` is sufficient for the runtime change. It reconstructs the same pinned original source, then verifies all before/after hashes while applying the cumulative overlay. Runtime project data is not opened by the build.

## Inventory categories and existing data

No inventory upload or category reset is needed. Applied categories and existing records remain on the same persistent project. To apply the original fictional categories for the first time, use the named administrator and the unchanged route:

**Inventory → DEMO Offshore equipment → Category: All categories → Manage categories → Preview demo categories → review and apply**, then repeat for **DEMO Consumables**.

This release does not automatically assign categories, reseed users, change movement or shipment states, move original documents or add vessel/cloud synchronisation. Hosted authentication and the guest-link implementation remain unchanged.

## Rollback and recovery limits

Revert the extractor commit and redeploy, or use the exact UI06 extractor under `REFERENCE_ONLY/Workspace_UI07/rollback/deploy/extract_source.py`. It retains category support and does not reset the database.

Do not re-enable first provisioning or delete `/var/data` to change the interface. The preserved `ops/staging_recovery.py` remains pinned to pristine 1.34.19 and is **not approved for an overlaid runtime**. Do not disable its source checks to force backup or restoration. Verified overlay-aware off-host recovery remains separate operator work.

## Acceptance on the actual hosted site

Test normal administrator sign-in and the restricted guest link. Open Help through existing controls, search for a phrase within the guide text, filter by area, follow a topic link, use the section list, and inspect Fault Reports, HSE / QSHE and Record management on desktop and a real phone. Verify the same guide content, not just a successful homepage load.

Confirm Inventory, categories, box contents, saved manifests and Receiving & placement still open as before. Do not make operational changes merely to verify this Help update. Check the source-mode warning before relying on local/native instructions in the hosted browser.

No Docker build, live deployment, physical-phone use, complete screen-reader acceptance, durable browser-storage test or off-host recovery was performed in this increment. Actual URL navigation in managed Chromium was blocked; local rendering checks use the shipped markup, CSS and JavaScript with controlled TestClient-backed reads. The routing endpoints themselves are separately tested against the real application.

## Progress

The Help review is a development checklist, not an automatically running scheduled job. Continue with its wording/link/mode checks alongside the remaining checklist and maintenance UI work. Inventory and shipment issues reported from the actual hosted demo still take priority. Original Files folder organisation and broader hosted authentication, company isolation and verified recovery remain separate pending work.

See **DELIVERY_CHECKS.json**, **VALIDATION/** and **HELP_STANDARDISATION_REVIEW.md** for exact test results, retained initial findings and unfinished items.
