# Wavelink UI79 — Native Inventory, Asset and Certificate Records

**Core 1.34.19 · parent UI78 + UI77 + UI76 + UI75 + UI74 + UI73 + UI72 + UI71 + UI70 + UI69 + UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 1 October 2026**

UI79 moves the remaining main-application equipment records to direct, route-owned Wavelink workspaces:
Inventory catalogue, Inventory record, stock verification, asset/equipment record, Certificate register and
Certificate record.

## Why this release exists

The shell and Fleet journey were stable by UI78, but main Inventory and Certificate pages still loaded three
separate historical presentation stylesheets. Those sheets contained important functional rules, but their
independent cascade could make record pages look like another GUI generation and made future changes harder to
reason about.

UI79 removes those three links from the active document and service-worker cache. Required functional rules are
retained inside one final stylesheet loaded after the established shell and route styles:

`app/static/equipment_workspace_ui79.css`

This is a presentation-ownership cutover, not another post-render decorator. The new layer creates no buttons,
moves no DOM, observes no route for restyling and adds no timer.

## Native route ownership

UI79 marks and styles six direct workspaces:

- Inventory catalogue;
- Inventory record, boxes and subitems;
- stock verification;
- asset/equipment record;
- Certificate register;
- Certificate record and evidence.

Inventory and Certificate summaries are calculated only from records already returned to the signed-in route.
They do not claim fleet-wide completeness, physical stock truth, certificate authenticity or equipment
readiness.

## Stable manual refresh

An unchanged asset refresh keeps the mounted asset host and record surface, updating only the compact snapshot
message. An unchanged Certificate refresh keeps both the register host and its card nodes, reporting a benign
checked state without marking the route stale.

UI79 adds no independent polling loop. A real-timer browser scenario kept an asset record open for more than
9.2 seconds after settlement and recorded zero workspace mutations.

## Runtime delta

UI79 embeds **10 runtime records** over the exact UI78 parent:

- 6 modified runtime files;
- 4 new runtime/test files;
- 0 removed runtime files;
- 2,013 final manifest-tracked runtime files.

Modified application files:

- `app/static/index.html`;
- `app/static/fieldwork.js`;
- `app/static/inventory_workspace.js`;
- `app/static/assets.js`;
- `app/static/certificate_workspace.js`;
- `app/static/sw.js`.

New files:

- `app/static/equipment_workspace_ui79.css`;
- `tests/ui79_native_equipment/__init__.py`;
- `tests/ui79_native_equipment/test_native_equipment.py`;
- `tests/ui79_native_equipment/browser_checks.py`.

Final runtime variant:

`workspace-ui79-native-equipment-records-2026-10-01`

## Authority and operational boundary

Opening, searching, filtering or refreshing these pages does not:

- change quantity, custody or equipment location;
- close or edit a stock verification;
- create or approve maintenance or Tasks;
- authenticate a Certificate or declare equipment ready;
- award contribution points;
- expand the viewer's source permissions.

Existing service-side permissions, record scopes, versions, custody rules and write validation remain
authoritative.

UI79 adds no database migration, reset, account conversion, permission key, operational API, recognition rule,
completion adapter, environment variable or browser-storage writer.

Mail Startup M01 remains byte-identical at:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

## Verification performed

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files, produced
2,013 manifest files and matched the curated UI79 runtime byte-for-byte. Manifest integrity passed.

Completed focused checks include:

- 7 dedicated UI79 static/architecture tests;
- 38 asset-summary permission, privacy, custody and read-only cases;
- 49 Certificate register lifecycle, reason, retry, evidence and rollback cases;
- 21 stock-verification scope, provenance, retry and closure cases;
- 4 Inventory category/label cases;
- 15 retained Certificate revision/retry cases;
- 14 Chromium equipment-record scenarios at 1440, 390 and 320 CSS pixels.

Repository, M01 and retained UI65/UI66 checks are recorded in `DELIVERY_CHECKS.json` after the final repository
and fresh reconstruction are verified.

The browser checks use fictional local records. They are not live Render, SMTP, DNS, physical-device,
production-data or independent security acceptance.

## Apply the compact GitHub update

1. Keep the current UI78 commit available as the source rollback point.
2. Extract the UI79 update ZIP.
3. Optionally run `VERIFY_UI79_UPDATE.py --repository "PATH" --state before`.
4. Copy everything inside `UPLOAD_TO_GITHUB` into the Wavelink application repository.
5. Replace matching files; do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. Confirm GitHub Desktop reports 9 modified files, 2 new files and no deleted files.
7. Review, commit and push normally.
8. Optionally run the verifier with `--state after`.
9. After the intended service reports healthy, reload one Wavelink tab once or close and reopen the installed app.

A company reset, database deletion, project import, browser-storage clear, repeated company setup or SMTP
reconfiguration is not required.

## Demo acceptance

After deployment to the fictional/demo service:

1. Open Inventory catalogue, an Inventory, an asset, stock verification, Certificate register and a Certificate.
2. Confirm all six screens use one consistent hierarchy and no old page flashes first.
3. Refresh an unchanged asset and Certificate; confirm the screen stays mounted.
4. Leave an asset record open for at least 15 seconds and confirm it does not blink or rebuild.
5. Repeat representative pages at phone width and confirm no document-level horizontal scrolling.
6. Exercise permitted and denied write actions to confirm existing service authority remains unchanged.
7. Confirm the sidebar remains left aligned and account/dialog surfaces stay above route content.

## Recovery boundary

UI79 itself has no schema migration. The existing UI66 recognition database boundary still applies: a database
already opened under UI66 recognition must remain paired with UI66-or-later application software. A rollback
should use the matching application commit and corresponding database backup rather than mixing release states.
