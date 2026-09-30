# Wavelink UI73 — Integrated Shell Context and Render Stability

**Core 1.34.19 · parent UI72 + UI71 + UI70 + UI69 + UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI73 continues the aggressive single-interface cutover requested for the test deployment. UI71 established one
static shell and UI72 removed the injected Administration frame. Source and browser review still found three
older top-level context bands outside that shell: project identity, install-app status and Fleet project context.
The save-status controller also began with a visible “checking” state before local state was known. Together,
those elements could shift the content area, compete with the shell and create another small flash during route
or startup rendering.

UI73 moves project/Fleet context and install access into the permanent sidebar, mounts operational save status
once immediately before the content root, and keeps that status hidden until its actual state is known. The main
content offset now has one owner.

## What changed

### One project context inside the sidebar

The main application now has one static `#shell-context` card inside `#shell-sidebar`. It shows the current
project and active signed-in workspaces without creating another horizontal band above the page. The install-app
link is retained in the sidebar footer.

The Fleet entry point has its own static sidebar context card for the current project and Fleet workspace. The
historical `.project-strip`, `.app-install-strip` and `.fleet-context` bands are no longer present in active HTML
or active shell CSS.

### Save status no longer flashes before it knows the state

`save_status_ui.js` creates one status element, marks it hidden initially, and inserts it directly before
`#app` or `#fleet-root`. It becomes visible only when there is useful saved-work or local-storage information to
show. It no longer searches for or anchors itself to the retired context bands.

This preserves meaningful Fleet/local-work warnings while removing the ordinary “Checking saved work…” flash.

### Presence and detached-window status use the same shell

Project presence now opens from the sidebar context card and uses the shared fixed overlay layer, so its panel
cannot be clipped behind the navigation. Its protocol refresh interval remains 30 seconds, but the redundant
one-second wake-up has been removed.

Detached log windows use the shell context’s status label instead of appending content into a retired project
strip.

### One active layout owner

`unified_ui.css` now defines the sidebar rows for project context, workspace finder, navigation and footer.
Desktop content has one sidebar offset; mobile content has no desktop offset. UI73 adds no page decorator,
MutationObserver, route-time DOM re-parenting or replacement navigation layer.

### Cache cutover

The service-worker cache advances to `pxgeo-dive-check-shell-1.34.19-ui73`, includes the exact UI73 shell assets,
activates after the complete cache installs, deletes older Wavelink shell caches and claims open clients.

A normal reload or close/reopen after deployment is sufficient. Clearing browser storage, resetting a company
or re-importing a project is not required.

## Runtime delta

UI73 embeds **12 runtime records** over the exact UI72 parent:

- 9 modified runtime files;
- 3 new runtime test files;
- 0 removed runtime files;
- 1,989 final manifest-tracked runtime files.

Modified application files:

- `app/static/index.html`;
- `app/static/fleet.html`;
- `app/static/unified_ui.css`;
- `app/static/nav_shell.js`;
- `app/static/save_status_ui.js`;
- `app/static/project_presence.js`;
- `app/static/project_presence.css`;
- `app/static/log_windows.js`;
- `app/static/sw.js`.

New files:

- `tests/ui73_integrated_context/__init__.py`;
- `tests/ui73_integrated_context/test_integrated_context.py`;
- `tests/ui73_integrated_context/browser_checks.py`.

## Operational boundaries

UI73 changes the active browser frame aggressively because the current service is not carrying valuable live
forms or inventory. It adds no database migration, destructive reset, permission key, account conversion,
operational API, recognition rule, points adapter, workflow completion adapter or environment variable.

Opening a route or project-presence panel does not create, approve, complete, publish, receive, move or score
an operational record. The presence count remains recent signed-in workspace activity, not attendance, shift
status or proof of work.

Mail Startup M01 remains byte-identical at:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

C01 company identity and G01 demonstration isolation remain unchanged.

## Verification

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files, produced
1,989 manifest files and matched all 12 non-generated UI73 payload files byte-for-byte.

Dedicated UI73 checks cover:

- one main/Fleet context card inside each static sidebar;
- no active project/install/Fleet context band outside the shell;
- save status hidden until its state is known and inserted once before the content root;
- no UI73 shell DOM re-parenting;
- fixed top-layer project-presence panel;
- 30-second presence protocol interval without a one-second wake-up;
- detached log status in the shell context;
- exact UI73 cache and asset URLs;
- desktop 1440 px, phone 390 px and narrow-phone 320 px layouts;
- Home, Tasks, Administration and Fleet Receiving route settlement;
- no tested document-level horizontal overflow or browser JavaScript errors.

These are local fictional TestClient checks, not a live Render, SMTP, DNS, physical-device, production-data or
independent security acceptance.

## Apply the compact GitHub update

1. Keep the current UI72 commit available as the source rollback point.
2. Extract the UI73 update ZIP.
3. Optionally run `VERIFY_UI73_UPDATE.py --repository "PATH" --state before`.
4. Copy everything inside `UPLOAD_TO_GITHUB` into the existing **Wavelink application** repository.
5. Replace matching files; do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. GitHub Desktop should show 9 modified repository files and 2 new repository files.
7. Review, commit and push normally.
8. Optionally run the verifier again with `--state after`.
9. Let Render complete the intended service deployment.
10. Reload one open Wavelink tab or close/reopen the installed application once.

## Acceptance after deployment

Using only the fictional/demo service:

1. open Home, Tasks and Administration and confirm no project or install strip flashes above the workspace;
2. confirm the current project and active-workspace control stay inside the sidebar;
3. open and close the active-workspace panel and confirm it remains above the page;
4. switch routes quickly and confirm the header, sidebar context and content left edge do not jump;
5. open Fleet Receiving and confirm a real local-save warning appears above Fleet content without hiding behind
   the sidebar;
6. repeat the main and Fleet checks at phone width;
7. open a detached log window and confirm its separate-window status appears in the shell context;
8. exercise representative existing forms to confirm established authority and unsaved-work guards remain.

No GitHub push, Render deployment, live database operation, external email, DNS/Zoho change or production-data
inspection was performed while preparing this release.
