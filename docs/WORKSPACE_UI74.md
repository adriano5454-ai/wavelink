# Wavelink UI74 — GUI Recovery Baseline

**Core 1.34.19 · parent UI73 + UI72 + UI71 + UI70 + UI69 + UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI74 is a corrective release. It does not add another interface layer. It repairs three regressions confirmed
in the exact UI73 runtime after the aggressive shell cutover:

1. the permanent sidebar inherited the legacy `.workspace-nav` centring and mobile-column rules because the
   new navigation still carried both the old and new classes;
2. removing the UI69/UI70 decorator scripts exposed route-owned pages whose legacy markup had not yet been
   given a complete native presentation;
3. the central route controller continued loading checklist records and calling `safeRender()` on unrelated
   routes, including an eight-second maintenance cycle, causing repeated page repainting and visible blinking.

## Corrective architecture

### One uniquely owned sidebar

The permanent sidebar navigation now uses only `.shell-navigation`. It no longer carries the legacy
`.workspace-nav` class. A final static recovery stylesheet owns the vertical navigation direction, full-width
rows, left-aligned labels and mobile row layout. The rules are deliberately scoped under the UI74 body classes
so older horizontal workspace navigation cannot recapture the shell.

This is not a post-render fix. The corrected class is present in the entry HTML before first paint.

### Route-owned workspaces, one static visual layer

UI74 adds `gui_recovery.css` as the last application stylesheet. It styles the existing route-owned headings,
controls, list/detail panes, cards and empty states without creating, moving or cloning controls. It contains
no JavaScript, animation, route observer, shell mutation observer or DOM re-parenting.

This restores one visual hierarchy to Tasks, Maintenance, Checklists, Handovers, Toolbox Talks,
Administration and the connected logistics screens while the deeper native-markup replacement can continue
in later grouped releases.

### Checklist refresh cannot repaint unrelated pages

The central route controller now treats checklist records as checklist-list data:

- entering `#checklists` refreshes the collection before one checklist-list paint;
- a checklist WebSocket record event refreshes the list only while that list is open;
- the eight-second maintenance loop refreshes/repaints the collection only while that list is open;
- Tasks, Maintenance, Profile, Administration and other routes are no longer repainted by an unrelated
  `/api/records` completion.

The existing current-checklist editor refresh, heartbeat, queue sync and live connection behavior remain.

### Fleet uses the same recovery boundary

Fleet receives the same UI74 body marker, last-loaded recovery stylesheet, shell controller version and cache
cutover. The Fleet navigation stays a left-aligned vertical sidebar at desktop and phone widths.

## Runtime delta

UI74 embeds **9 runtime records** over the exact UI73 parent:

- 5 modified runtime files;
- 4 new runtime files;
- 0 removed runtime files;
- 1,993 final manifest-tracked runtime files.

Modified application files:

- `app/static/app.js`;
- `app/static/fleet.html`;
- `app/static/index.html`;
- `app/static/nav_shell.js`;
- `app/static/sw.js`.

New files:

- `app/static/gui_recovery.css`;
- `tests/ui74_gui_recovery/__init__.py`;
- `tests/ui74_gui_recovery/test_gui_recovery.py`;
- `tests/ui74_gui_recovery/browser_checks.py`.

Final runtime variant:

`workspace-ui74-gui-recovery-baseline-2026-09-30`

## Data and authority boundary

UI74 adds no database migration, destructive reset, account conversion, permission key, operational API,
recognition rule, points adapter, source-completion adapter, environment variable or browser-storage writer.
It does not complete, approve, publish, receive, move or score an operational record.

Mail Startup M01 remains byte-identical at:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

C01 company identity, G01 demonstration isolation and the existing UI66 recognition schema remain unchanged.

## Verification performed

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files,
produced 1,993 manifest files and matched all nine UI74 payload files byte-for-byte. Manifest integrity passed.

Dedicated UI74 checks verify:

- no `.workspace-nav` class on the permanent main sidebar;
- one last-loaded recovery stylesheet in main and Fleet entry points;
- vertical, full-width, left-aligned sidebar rows at 1440, 390 and 320 CSS pixels;
- no document-level horizontal overflow in those checks;
- no new decorator script, animation or route-time DOM movement;
- checklist record refresh ownership is limited to the checklist-list route;
- Tasks remains mutation-free for more than nine seconds after route settlement with real timers;
- the UI74 service-worker cache and exact UI74 asset URLs;
- zero browser JavaScript errors in the focused fictional TestClient browser run.

These are local fictional checks, not live Render, SMTP, DNS, physical-device, production-data or independent
security acceptance.

## Apply the compact GitHub update

1. Keep the current UI73 commit available as the source rollback point.
2. Extract the UI74 update ZIP.
3. Optionally run `VERIFY_UI74_UPDATE.py --repository "PATH" --state before`.
4. Copy everything inside `UPLOAD_TO_GITHUB` into the existing **Wavelink application** repository.
5. Replace matching files; do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. Review the changed/new files in GitHub Desktop, commit and push normally.
7. Optionally run the verifier again with `--state after`.
8. After the intended service becomes healthy, reload one open tab once or close/reopen the installed app.

A database reset, company recreation, project import or browser-storage clear is not required for this GUI
recovery.

## Acceptance after deployment

Use the fictional/demo service first:

1. open and close the sidebar on desktop and phone and confirm every icon/label row is left aligned;
2. switch repeatedly among Home, Tasks, Maintenance, Checklists, Handovers, Profile and Administration;
3. leave Tasks or Maintenance open for at least 15 seconds and confirm the content does not flash or rebuild;
4. open Checklists and confirm its list still refreshes normally;
5. open Fleet Receiving and confirm its navigation uses the same left-aligned hierarchy;
6. open the account menu and a dialog and confirm they remain above the content;
7. exercise representative existing controls with permitted and denied fictional accounts.

No GitHub push, Render deployment, live database operation, external email, DNS/Zoho change or production-data
inspection was performed while preparing UI74.
