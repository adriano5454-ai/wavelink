# Wavelink — Workspace UI 04

**Core 1.34.19. Cumulative UI01 + UI02 + UI03 + UI04. Prepared 25 September 2026. Local implementation and tests only; not deployed to GitHub or Render by this session.**

## What this update changes

This is the next inventory-first interface increment. It also redesigns **Administration → Record management**, as requested. It does not add another operational module or change database, lifecycle, custody or permission rules. Native Windows Admin is outside this browser update.

The complete package is built from the supplied `Wavelink_Online_Demo_Full_UI03.zip`. The current live GitHub tree was not retrieved. The only existing executable repository file changed relative to that package is `deploy/extract_source.py`. Documentation and evidence are updated separately. Existing gateway, normal login, guest-link, initialization and disk handling files remain byte-identical to the supplied full UI03 package.

## Inventory: navigation beside the records

The distant Back / Up / All inventory row is replaced with a compact current-location header directly above search and the equipment list. The path shows real names: **Inventories › inventory › parent box › current box**. Select a parent name to jump there. There is no separate Up button or disabled Back at the root of a new view.

The return button names the view it restores: **Back to Survey kit**, **Back to search results**, or the previously selected category. The in-memory trail restores the prior box, search/filter choices, selected records and list scroll. It is not a new permanent browsing-history store. This pass covers inventory-to-inventory navigation; a universal cross-workspace return trail from Tasks, Assets and Manifests is still pending.

Click an item name to open its existing detail popup. Click a box name or **Open box** to enter that box. Checkboxes select records for actions. Clicking ordinary row space still supports selection, including the existing keyboard/modifier behaviour. A scoped single-click-name option was added to the shared selection helper; its default behaviour for other workspaces is unchanged.

**Category: All categories** sits beside Search. Open it for searchable category choices and counts; selecting a category closes the panel while retaining its visible label. **Manage categories** is inside this panel for authorized administrators. Category counts keep UI03's meaning: records within the current inventory/box scope, including descendants—not summed stock quantities.

The longer source/location/department controls and type/custody choices sit inside Filters. Active filters remain described when collapsed. QR/export/verification and shipment/receiving shortcuts are grouped in More tools. Saved forms and Add item / box remain available in the top toolbar when authorized.

The selected-record action bar appears only when at least one visible record is selected. It shows the existing complete whole-box movement scope without counting a selected child twice. It disappears when selection is cleared. This means selecting records can change the vertical layout; it is not a fixed-height, no-shift table. Filtering out a selection removes it with a notice. Nothing moves merely by browsing or selecting.

Desktop equipment lists scroll within their working area; the path stays above that area. The mobile page itself can scroll—the path is not advertised as an always-fixed phone header. Deep paths wrap, categories are collapsible, and no permanent second box tree is introduced.

## Record management: find → review → confirm

The browser workspace organizes the existing 19 record types into four groups: Daily work; Equipment & logistics; Safety & quality; Templates & original files. The type catalogue is not a permission boundary. Current named-administrator access and the owning service still govern record visibility and every change.

Choose Record type, Show and Search, then press **Search / refresh**. Changing a filter alone does not run a write. Results show the record's name, context and saved status. Search and paging still use the existing endpoint and limits; this is not a new global cross-type search.

On a wide screen the record list and selected detail sit side by side. The selected row is highlighted. On a narrow screen the list opens a full-width detail view, with **Back to [record type]** retaining the list filter and scroll context.

The detail presents only the actions returned by the server. Action cards explain both their intended use and effect before opening confirmation:

- **Postpone:** pause delayed unfinished work while keeping its saved work.
- **Cancel:** retain a cancelled record; do not call it completed.
- **Archive / Restore:** change normal visibility without erasing evidence or unlocking completed stages.
- **Void / Restore entry:** correct a log's active view while keeping the original and correction history.
- **Resume / Reopen:** retain their existing, different meanings for postponed versus cancelled/completed task work.

Availability remains record- and state-specific. A completed checklist does not gain Postpone merely because another checklist has it. A shipped manifest is not silently cancelled, and a box with dependency restrictions is not forcibly archived. Fault and HSE/QSHE management retain their links to the owning workspaces. There is no new blanket delete/purge or bulk processing action.

Selecting an action opens a focused confirmation with its exact record, effect, required reason, exact-name confirmation and initially unchecked acceptance. The API action names, revisions, operation IDs, retry behaviour and server checks are unchanged. **Back without saving** asks before discarding entered confirmation text; it does not undo an action whose server result is uncertain. A lost response retains the original operation for an unchanged retry.

Record switching, filter/search, or navigation must not replace an open confirmation. In-flight reads are invalidated when the account or workspace changes so an older private response cannot populate a newer selection. These record-management forms remain page-memory/online-only; they are not permanent offline drafts. Existing browser draft stores elsewhere are not cleared by this update.

## Install the complete ZIP with GitHub Desktop

1. Preserve unfinished work in every Wavelink tab and separate log window. Retain the previous GitHub commit and your established project backup. Deploy outside the client presentation. Do not clear browser storage.
2. In GitHub Desktop, make sure **Current Repository is `wavelink`**, not CCVD Relay. Fetch/pull the intended branch first. Preserve any uncommitted edits before replacing files; do not discard them blindly.
3. Extract the package. Open `UPLOAD_TO_GITHUB`. Copy its **contents** into the root of the local Wavelink checkout, preserving subfolders and allowing intended file replacement. Do not copy the enclosing folder. Do not delete `.git`, the repository, Render disk or existing project.
4. Review the diff. Against the supplied full UI03 package, only `deploy/extract_source.py` should differ among existing executable/deployment code files. Other changes are documentation, checksums or tests. If unrelated login/gateway edits appear, stop and reconcile them with your current repository; this package is not a live repository backup.
5. Commit the approved changes and **Push origin**. Use the existing Render service and approved commit. A push may trigger deployment if enabled. Do not create another service or modify the vessel/CCVD setup.
6. Keep all Render values as they are, especially **`INITIALISE_FICTIONAL_DEMO=NO`**. Leave the initial-administrator bootstrap password removed. Keep the existing persistent `/var/data` disk and hostname.
7. The build should print:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 04: inventory navigation and record management; includes UI01-UI03; no automatic data changes.
```

8. When the actual deployment is healthy, reload Inventory and open Administration → Record management. Each shows **UI 04**. Core version remains **1.34.19**. Preserve unsent work before closing/reopening any older tab to activate the new service worker; do not delete site data.

For an already matching UI03 deployment, it is also sufficient to replace only `deploy/extract_source.py`. The full ZIP is supplied for convenience, not because users or project data need re-importing.

## Existing demo categories: no upload or reseed

The UI03 definitions, record mappings and services are included unchanged. Category assignments already applied remain in the project. Deploying this update never assigns them automatically.

To apply the missing original demo categories, use the normal named administrator—not the guest quick link:

**Inventory → DEMO Offshore equipment → Category: All categories → Manage categories → Preview demo categories → review/confirm/apply**.

Repeat for **DEMO Consumables**. The original unchanged examples propose 56 equipment records in 13 categories and 12 consumables in five. Existing category choices and changed/custom records are retained; missing or identity-changed demo records are skipped. Copies with different list IDs are not mistaken for the original. No quantities, container links, shipment states or original evidence are overwritten.

## Rollback and retained metadata

Revert the extractor change to the prior approved commit and redeploy. An exact UI03 extractor is included under `REFERENCE_ONLY/Workspace_UI04/rollback/deploy/extract_source.py`. It returns to UI03 without removing category support or instructing any database reset. Keep category-bearing exports/drafts on a category-aware version.

Never re-enable first initialization, clear `/var/data`, re-import the original demo or restore an old hosting ZIP just to change the interface.

The preserved `ops/staging_recovery.py` helper is pinned to the pristine 1.34.19 source. It has **not** been revised or accepted for an overlaid `/opt/wavelink/app` runtime. Do not disable that source check to force a backup/restore. Recovery for the hosted overlaid build remains a separate operator acceptance item; this UI package does not claim a completed backup-restoration procedure.

## Validation and boundaries

See `DELIVERY_CHECKS.json` and `VALIDATION/` for exact passed counts, initial findings and final reruns. Tests use actual shipped scripts/styles, Chromium, fictional SQLite/TestClient requests and injected in-memory browser persistence. Screenshots are local captures, not your Render service or native Windows Admin. No mocked-up controls or generated product screenshots are used.

No Docker image was built here; no current GitHub tree was fetched and no Render service was deployed. The full application regression suite, full browser suite, real devices, durable browser storage, live restart/redeploy, off-host recovery and complete assistive-technology acceptance were not rerun. These targeted checks are not production readiness, multi-company isolation or vessel/cloud synchronization approval.

## Next agreed improvements

Keep inventory/boxes/movement/receiving first, with record-management usability now part of the same interface roadmap. Check this deployment's actual client workflow before expanding it. Next candidates: remaining dense item forms and context-aware return between Assets/Manifests/Inventory; clearer record-management action discovery where an action is blocked; then consistent checklist and maintenance layouts. Original Files logical folders remain a separate pending feature. No original files are moved by UI04.

### Final local results

**297 distinct Python cases and 96 compound browser checks passed** on the final source. This includes 16 UI04 workflow checks, 5 shared-selection checks, 13 adapted category-flow checks, and existing record-management, asset-details, movement, preparation and saved-manifest checks. All 36 JavaScript files passed syntax checking. Initial findings, harness changes and complete final reruns are preserved. These counts do not include repeats of the same test or historical UI03 evidence.
