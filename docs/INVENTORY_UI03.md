# Wavelink Inventory UI 03 — categories and cleaner browsing

**Cumulative update for the hosted 1.34.19 fictional demonstration. Prepared 24 September 2026. Not deployed to the live Render service by this session. Includes UI01 and UI02.**

## Two steps, not a reset

**First install the single-file update. Then apply the proposed categories from inside each existing demo inventory.** Building or starting the app never re-imports a project or changes inventory records automatically.

The only GitHub replacement is **`upload/deploy/extract_source.py`**, installed at **`deploy/extract_source.py`** in the existing repository. The five source parts must remain the reviewed original 1.34.19 set. The embedded update verifies original and replacement file hashes before application.

Unlike UI01/UI02, this increment also adds server-side category metadata and guarded actions. It is not merely CSS, and it is not a new Windows installer or a 1.34.20 release.

## Install through the existing GitHub/Render workflow

1. Preserve or synchronise unfinished work in every browser and separate log window. Take the normal project backup. Deploy outside the client presentation; the current service may briefly restart. Do not clear browser storage.
2. Extract the update ZIP. In GitHub, open **`adriano5454-ai/wavelink` → `deploy`** and replace **`extract_source.py`** with **`upload/deploy/extract_source.py`** from this pack. Do not create `upload/deploy` or `deploy/deploy` inside the repository.
3. Review and commit only that file. Merge/deploy the approved commit through the existing service. Do not change the live `gate.py`, `entrypoint.py`, `nginx_config.py`, Dockerfile, `requirements.lock`, vendor parts, fictional seed, secrets or persistent disk.
4. Keep **`INITIALISE_FICTIONAL_DEMO=NO`**. No seed rerun is required. Expected build messages:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Inventory UI 03: category tools and cumulative UI; demo data changes require explicit administrator review.
```

5. Once deployment is healthy, reload Inventory and check **UI 03**. Core Wavelink still shows **1.34.19**. Existing browser apps may need their tabs closed/reopened after unsent work is preserved to activate the updated service worker. Do not delete site data.

Stop on a source-check failure rather than disabling the verification. This package has not been deployed to Render or tested against the user's current live repository by this session.

## Apply the missing demo categories

Use your normal administrator sign-in, **not the restricted guest quick link**. Definition management and the demo setup require a current project administrator with inventory view/edit access.

### DEMO Offshore equipment

Open **Inventory → DEMO Offshore equipment → Manage categories → Preview demo categories**.

For the original unchanged inventory, the preview lists **56 records and 13 proposed categories**. Review the equipment references, assignments, proposed new category names and any skipped records. Type **`DEMO Offshore equipment`** exactly, enter/review the reason, tick the confirmation and select **Apply reviewed categories**.

### DEMO Consumables

Repeat in **Inventory → DEMO Consumables → Manage categories → Preview demo categories**.

The original inventory proposes **12 records and five categories**. Type **`DEMO Consumables`** exactly, review, confirm and apply.

The setup matches the original list ID and name and each original item ID, name, reference and box/item flag. A renamed list or an independently imported copy with different IDs is not automatically treated as the original. Create categories manually there. Missing, identity-edited or archived records are skipped; already categorised records retain their choices; additional custom records remain untouched. Changes to other item details are not overwritten. The preview is rechecked at save time; intervening list/item changes require a fresh review.

Applying again does not duplicate categories or replace existing assignments. Existing active categories with the same name are reused. A matching archived category is not silently restored. The preview and apply are separate operations—looking at the proposal changes nothing.

## The category scheme

| Equipment categories | Records in original example |
|---|---:|
| Acoustic equipment | 4 |
| Boxes & transport cases | 10 |
| Cables, connectors & spares | 2 |
| Calibration & test equipment | 5 |
| Computers & interfaces | 1 |
| Deck & mobilisation | 5 |
| General training equipment | 1 |
| Inspection equipment | 4 |
| Packing & logistics equipment | 2 |
| Survey & navigation | 9 |
| Vehicle support & telemetry | 4 |
| Workshop & repair spares | 4 |
| Workshop & service tools | 5 |

Consumables are grouped into **Labels & identification, Protection & packing, Cable management, Cleaning supplies, and Documents & stationery**. The full record-to-category proposal is in `docs/DEMO_CATEGORY_MAP.md` and the readable `inventory_demo_categories.json` source.

These are fictional example categories, not a prescribed operational taxonomy. Administrators can rename them or create their own.

## Cleaner inventory interface

### Inventory catalogue

The Inventory start page now offers a search by inventory name/description, an explicit include-archived choice and consistent inventory cards. Cards show active record count, active category count, uncategorised active records and open stock verifications. Counts refer to records, **not summed quantities**. The catalogue filter is local to the view; it is not a saved project preference.

### Categories inside each inventory

A dedicated category panel sits above the existing equipment search and filters. **All categories**, **Uncategorised** and individual categories have counts. At inventory root those counts cover active records at all levels; inside a box they cover its descendants. They are calculated before the other search/type/custody filters and labelled accordingly.

Selecting a category deliberately searches across nested records within the current box/inventory scope. Results keep their physical box/location information. Clear filters returns to normal folder browsing. Category labels also appear in inventory rows, the selection summary and the existing item popup.

Categories are not introduced as another physical folder hierarchy. You can continue to open boxes, use Back/Up, search, inspect Asset details, prepare shipments and receive/place equipment using the existing workflows. Asset details retains the cumulative UI02 improvements; no new category field is added to its separate Overview editor in this increment.

On mobile, **Show categories / Hide categories** controls the panel so equipment is not permanently pushed below a long category list. Category buttons remain touch-sized and scroll within the panel when needed. The sidebar stays.

### Manage and assign

**Manage categories → New category** opens a focused form for the name, description, reason and reviewed confirmation. Names must be unique within the inventory, including archived definitions. Renaming keeps the stable category ID and existing assignments.

Select visible item/box rows and choose **Categorise selected** to assign a category or deliberately choose **Uncategorised (clear category)**. This requires inventory-edit access; administrator status is required for definitions/setup, not merely assigning an existing category. One category is supported per record in each inventory. Selecting a box classifies only the box; its children are not selected automatically for classification.

Archiving a category is blocked while any active or archived item uses it. Reclassify/clear those assignments first. Restore retains the definition and history; there is no permanent category-delete action.

Category changes use the existing confirmed-action, current-permission, saved-version, audit-history and operation-ID retry rules. An intervening change causes a conflict rather than silent replacement. A saved/resumed form keeps the reviewed IDs/versions and resets confirmation. **Saved forms** remains available; no new automatic background queue is added.

View/search preferences are temporary and current-account/session scoped. Existing local saved-form protections remain; the category definitions and assignments themselves are saved in the hosted project when explicitly applied.

## What category actions never do

Classification writes only optional `classification` JSON in the inventory list, its list revision and the existing audit/operation records. It does not rewrite item rows or their versions, quantities, source references, container parentage, verification results, Fleet custody, holding, quarantine or shipment records.

A descriptive category may be assigned to an item currently in transit or quarantine because it does not move or release that item. Physical move/receipt/placement and export restrictions remain enforced by their existing services. Old stock-verification snapshots and historical report values are not retrospectively relabelled.

Categories do not create permission boundaries, separate companies or synchronise vessel/cloud projects. Type and Sub type remain unchanged. Hierarchical subcategories, multiple category tags per record, category-based access controls and bulk category-CSV import are not included.

## Persistence, exports and compatibility

No new SQL table or database migration is required. Existing inventories read without any automatic metadata initialisation. New definitions/assignments are kept in the same SQLite project backup as their parent inventory. A local coherent snapshot/reopen test covers those fields; actual Render restart/redeploy restoration still needs acceptance.

Inventory CSV adds a **Category** column, retaining spreadsheet formula-protection behavior. A separate inventory export with categories uses **`ajinventory-3`** and remaps category/item IDs on import into a new inventory. **Export category structure** exports definitions without item records. Existing Fleet-bound item export restrictions still apply.

Category-bearing imports require this category-aware implementation. Older application builds reject `ajinventory-3`; do not remove its format marker or downgrade it. This update does not add a new browser file-import page or migrate the native desktop installation. Use the normal full-project backup for recovery, not a structure-only file.

Limits: up to 100 retained category definitions per inventory, 5,000 classified records per inventory, and 500 explicitly selected records per classification action. Name 80 characters; description 500; reason 1,000. These are implementation limits, not demonstrated multi-user hosting capacity.

## Rollback and unchanged deployment files

Revert only the `deploy/extract_source.py` commit and redeploy. The included `rollback/deploy/extract_source.py` is the exact UI02 extractor. It temporarily hides category controls; it does not instruct deletion or reset of the database. Preserve the UI03 package and a backup before reverting, and prefer a forward correction once categories or category drafts have been used. Older category-unaware exports may omit the new metadata, and older forms cannot resume category operations; use UI03 for those operations.

No vessel installation, CCVD relay, login credentials, public hostname, environment variables, gateway, worker count or dependency settings are changed. Source parts and the original fictional seed remain unchanged. Never re-enable initialisation or clear the disk to obtain these categories.

## Test the actual hosted copy

After deployment, verify the UI03 badge as administrator and restricted guest. Apply each preview only after reviewing its proposed records. Confirm one known sensor and one box retain their identity, quantity, location and manifest association. Open the category filter while inside a nested box, clear it and use Back/Up. A selection filtered out of sight must not remain an invisible movement target.

Create/rename one harmless category, categorise one chosen record and inspect category/inventory history. Check that the restricted guest cannot manage definitions or perform writes without its existing permissions. Preserve unfinished work, then perform a deliberate service restart and confirm saved categories and attachments remain. Test desktop and a real phone before inviting the client.

## Validation

**221 targeted inherited Python tests, 38 new category service/API tests and 29 extraction/overlay tests passed: 288 tests total. All 144 compound browser checks across ten harnesses passed on the final code.** All 36 JavaScript files were syntax checked, along with the Python source.

Browser checks use actual Chromium and shipped scripts/styles with fictional SQLite/FastAPI fixtures, controlled HTTP and injected in-memory persistence. Screenshots are actual local rendering, not live Render or Windows captures. The unmodified preview shell may say Local hub; live presentation substitutions remain separate. The full-page phone image and an explicitly cropped viewport image are provided. No image controls were redrawn.

Two initial test-fixture failures were corrected: a fixture used an old item version after a Fleet allocation, and an in-memory SQLite deserialize could not open the seed's WAL-mode snapshot. Existing safeguards were not relaxed. Those findings and subsequent complete runs are retained. The final runtime was re-extracted after a small CSS-only polish and all targeted suites rerun.

The full application regression suite was not rerun. No Docker image was built, no GitHub/Render service was modified, and physical-phone, durable-browser-storage, full screen-reader, live restart or off-host recovery acceptance was not performed. The demo remains fictional and access-restricted; this is not production-readiness approval.

## Continue from this checkpoint

Inventory, boxes, manifests and movement/receiving usability remain the priority. Keep the next increment bounded around actual inventory feedback and remaining long forms, then apply the same consistent organisation to checklists, maintenance and other workspaces. Original Files folder organisation remains a separate pending feature; no original documents were moved.

The pack was then zipped and freshly extracted: the single-file build path reproduced all **1,608 tracked output hashes**; **67 category/overlay tests and all 13 new browser checks passed again** using the extracted files. Final packaging adds only this evidence, documentation and checksums; the extractor and application bytes are unchanged. These repeat runs are not added to the distinct totals above.
