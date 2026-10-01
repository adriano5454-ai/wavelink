# Wavelink UI77 — Native Fleet and Vessel Logs

**Core 1.34.19 · parent UI76 + UI75 + UI74 + UI73 + UI72 + UI71 + UI70 + UI69 + UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI77 continues the native-workspace cutover after UI76 operational records. It replaces the active Fleet and
vessel-log presentation with direct route-owned markup, one authoritative Fleet stylesheet and a quiet
saved-entry refresh model. It does not add another global shell, decorator or page-rebuilding timer.

## Why this release exists

The Fleet document still loaded twelve historical stylesheets from several interface generations:

- `fleet.css`;
- `save_status.css`;
- `workspace_continuity.css`;
- `ui_polish.css`;
- `logistics_workflow.css`;
- `preparation_ui.css`;
- `manifest_ui.css`;
- `interface_components.css`;
- `fleet_workspace.css`;
- `deployment_branding.css`;
- `unified_ui.css`;
- `gui_recovery.css`.

Those files included useful functional selectors, but loading all twelve allowed old spacing, card, table,
navigation and responsive rules to compete by stylesheet order. UI77 consolidates the Fleet presentation into:

`app/static/fleet_workspace_ui77.css`

The historical assets remain in the cumulative source lineage for audit and recovery. They are no longer
loaded by `fleet.html` or cached as active Fleet presentation assets by the service worker.

## Native Fleet route ownership

The following Fleet areas now create their final hierarchy directly inside the existing stable shell:

- Vessels & shore bases;
- Fleet access & setup;
- Shipment & log calendar;
- Vessel logbooks;
- Assigned log issues;
- Vessel logbook setup;
- Vessel log permissions.

Their headings, data-grounded summary cards, forms, tables, notices, empty states and responsive layouts are
owned by the route renderer. The left navigation remains full-width and left aligned. At phone widths, wide
operational tables scroll inside their own cards rather than expanding the document.

This release does not duplicate equipment identities, move assets, change custody, publish a Manifest, grant
log access or write a vessel-log entry merely because a page opens.

## Quiet saved-entry refresh

The selected vessel logbook previously performed a visible `load()` every eight seconds. Even when the saved
entries had not changed, that path could rewrite status or table content while someone was reading or entering
work.

UI77 changes the background check to a quiet 30-second comparison:

1. unchanged saved entries produce no visible DOM update;
2. changed saved entries leave the current rows in place;
3. a small **Show new saved entries** control appears with an explicit status;
4. the user applies the new rows deliberately;
5. a manual refresh still applies current server data immediately.

The existing API, permissions, draft safeguards, local-save behaviour and log-entry validation remain
unchanged. UI77 adds no independent refresh system outside the existing vessel-log controller.

## Runtime delta

UI77 embeds **7 runtime records** over the exact UI76 parent:

- 3 modified runtime files;
- 4 new runtime/test files;
- 0 removed runtime files;
- 2,005 final manifest-tracked runtime files.

Modified application files:

- `app/static/fleet.html`;
- `app/static/fleet.js`;
- `app/static/sw.js`.

New files:

- `app/static/fleet_workspace_ui77.css`;
- `tests/ui77_native_fleet/__init__.py`;
- `tests/ui77_native_fleet/test_native_fleet.py`;
- `tests/ui77_native_fleet/browser_checks.py`.

Final runtime variant:

`workspace-ui77-native-fleet-vessel-logs-2026-09-30`

## Data and authority boundary

UI77 adds no database migration, reset, account conversion, permission key, operational API, recognition rule,
points adapter, completion adapter, environment variable or browser-storage writer. It changes presentation
and the timing/visibility of an existing read-only saved-entry check, not operational authority.

Mail Startup M01 remains byte-identical at:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

C01 company identity, G01 demonstration isolation, UI66 recognition data, existing Fleet records and backend
authority remain unchanged.

## Verification performed

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files, produced
2,005 manifest files and matched all 7 UI77 payload files byte-for-byte. Manifest integrity passed.

Dedicated UI77 checks verify:

- one authoritative Fleet stylesheet is loaded;
- the twelve historical Fleet stylesheets are absent from the active Fleet document and service-worker cache;
- the listed Fleet/setup/log routes own their final hierarchy;
- Fleet navigation rows remain vertical, full-width and left aligned;
- mobile tables remain contained inside their cards;
- the old 8-second vessel-log refresh is absent;
- unchanged background checks make no visible update;
- changed data presents **Show new saved entries** without moving the current rows;
- applying that control updates the visible table;
- a real-timer vessel-log view remains mutation-free for more than 9.2 seconds after settlement;
- 1440, 390 and 320 CSS-pixel checks have no document-level horizontal overflow.

The browser checks use fictional local fixtures. They are not live Render, SMTP, DNS, physical-device,
production-data or independent security acceptance.

## Apply the compact GitHub update

1. Keep the current UI76 commit available as the source rollback point.
2. Extract the UI77 update ZIP.
3. Optionally run `VERIFY_UI77_UPDATE.py --repository "PATH" --state before`.
4. Copy everything inside `UPLOAD_TO_GITHUB` into the existing **Wavelink application** repository.
5. Replace matching files; do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. Review the changed/new files in GitHub Desktop, commit and push normally.
7. Optionally run the verifier again with `--state after`.
8. After the intended service becomes healthy, reload one open tab once or close/reopen the installed app.

A database reset, company recreation, project import or browser-storage clear is not required.

## Acceptance after deployment

Use the fictional/demo service first:

1. open Vessels & shore bases, Fleet setup, Calendar and all vessel-log setup/list routes;
2. confirm one Fleet stylesheet governs the final layout and no older cards/headings flash first;
3. leave a selected vessel log open for at least 15 seconds and confirm it does not repaint;
4. create or inject a new fictional saved entry from another session and confirm the current rows remain fixed
   until **Show new saved entries** is selected;
5. confirm manual refresh still applies current saved entries immediately;
6. repeat the Fleet sites, logbooks and setup routes at 390 and 320 CSS pixels;
7. confirm wide tables scroll inside their cards and the overall page does not scroll sideways;
8. exercise representative existing save/permission controls with permitted and denied fictional accounts.

No GitHub push, Render deployment, live database operation, external email, DNS/Zoho change or production-data
inspection was performed while preparing UI77.
