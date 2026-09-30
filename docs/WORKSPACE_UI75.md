# Wavelink UI75 — Native Administration and Setup

**Core 1.34.19 · parent UI74 + UI73 + UI72 + UI71 + UI70 + UI69 + UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI75 continues from the accepted UI74 recovery baseline. It does not add another global shell or post-render
decorator. It replaces the active Administration/setup presentation with route-owned markup and one
authoritative final stylesheet.

## Why this release exists

The UI74 recovery stopped the most visible sidebar regression and unrelated checklist repaint loop. Source
review then found that Administration and setup still loaded six historical stylesheets at the same time:

- `browser_admin.css`;
- `company_branding.css`;
- `record_management.css`;
- `setup_builders.css`;
- `browser_templates.css`;
- `browser_logs.css`.

Those files came from different interface generations. Keeping all six active made spacing, cards, panes and
mobile rules depend on stylesheet order. Several routes also replaced their whole content with a loading page
during refresh, which could look like the old interface flashing back.

UI75 consolidates the necessary functional rules into one final asset:

`app/static/admin_workspace_ui75.css`

The six historical files remain in the cumulative source lineage for audit/recovery, but the active entry page
and service-worker cache no longer load them.

## Native route ownership

The following routes now render their final hierarchy directly inside the stable UI74 shell:

- People & access;
- Departments;
- Templates & routines;
- Logbook designer;
- Builders;
- Record management;
- Imports & examples;
- Company branding & reports.

The shared style layer provides consistent headings, summary metrics, master/detail panes, cards, forms, empty
states and responsive stacking. It does not create, clone, move or replace operational controls.

## Route-ownership correction

A latent Administration navigation bug was also corrected. Previously, returning from Company Branding or
another setup route to People could stop early because any existing `#admin-workspace` element was treated as
the People directory. UI75 gives the actual directory an explicit `data-admin-directory="true"` ownership
marker. A route is reused only when both the route context and that marker match.

## In-place refresh instead of a loading flash

People/Departments and Company Branding now refresh within the existing route host:

- the current page remains mounted;
- `aria-busy` communicates the refresh state;
- the page is not replaced with a blank or temporary loading screen;
- no independent timer, animation, shell observer or DOM re-parenting layer is added.

This preserves route stability while retaining the existing data calls, permissions and error handling.

## Runtime delta

UI75 embeds **12 runtime records** over the exact UI74 parent:

- 8 modified runtime files;
- 4 new runtime/test files;
- 0 removed runtime files;
- 1,997 final manifest-tracked runtime files.

Modified application files:

- `app/static/browser_admin.js`;
- `app/static/browser_templates.js`;
- `app/static/company_branding.js`;
- `app/static/import_centre.js`;
- `app/static/index.html`;
- `app/static/nav_shell.js`;
- `app/static/record_management.js`;
- `app/static/sw.js`.

New files:

- `app/static/admin_workspace_ui75.css`;
- `tests/ui75_native_admin/__init__.py`;
- `tests/ui75_native_admin/test_native_admin.py`;
- `tests/ui75_native_admin/browser_checks.py`.

Final runtime variant:

`workspace-ui75-native-administration-2026-09-30`

## Data and authority boundary

UI75 adds no database migration, reset, account conversion, permission key, operational API, recognition rule,
points adapter, completion adapter, environment variable or browser-storage writer. It does not create,
complete, approve, publish, receive, move or score an operational record.

Mail Startup M01 remains byte-identical at:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

C01 company identity, G01 demonstration isolation, UI66 recognition data, saved records and current backend
authority remain unchanged.

## Verification performed

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files, produced
1,997 manifest files and matched all 12 UI75 payload files byte-for-byte. Manifest integrity passed.

Dedicated UI75 checks verify:

- one authoritative Administration stylesheet is loaded after the shared shell/recovery styles;
- the six historical route stylesheets are absent from the active document and service-worker cache;
- no new decorator, MutationObserver, timer, route animation or DOM re-parenting path is introduced;
- People/Departments, Templates, Records, Imports, Company Branding, Builders and Logbook Designer open as
  route-owned workspaces;
- Company-to-People navigation cannot reuse the wrong Administration host;
- People and Company Branding refresh in place;
- People remained mutation-free for more than 9.2 seconds after settlement with real timers;
- 1440, 390 and 320 CSS-pixel checks have no document-level horizontal overflow.

The fictional browser fixture produced one expected failed WebSocket connection to the placeholder `ws://ws/`
address. It recorded zero unexpected application JavaScript errors. This fixture warning is not a live-service
WebSocket result.

These are local fictional checks, not live Render, SMTP, DNS, physical-device, production-data or independent
security acceptance.

## Apply the compact GitHub update

1. Keep the current UI74 commit available as the source rollback point.
2. Extract the UI75 update ZIP.
3. Optionally run `VERIFY_UI75_UPDATE.py --repository "PATH" --state before`.
4. Copy everything inside `UPLOAD_TO_GITHUB` into the existing **Wavelink application** repository.
5. Replace matching files; do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. Review the changed/new files in GitHub Desktop, commit and push normally.
7. Optionally run the verifier again with `--state after`.
8. After the intended service becomes healthy, reload one open tab once or close/reopen the installed app.

A database reset, company recreation, project import or browser-storage clear is not required.

## Acceptance after deployment

Use the fictional/demo service first:

1. open People, Departments, Templates, Logbook Designer, Builders, Records, Imports and Company Branding;
2. switch Company Branding → People and confirm the People directory always replaces the company page;
3. refresh People and Company Branding and confirm the existing screen stays in place;
4. leave People open for at least 15 seconds and confirm it does not blink or rebuild;
5. repeat People, Templates and Company Branding at phone width;
6. confirm account menus and dialogs stay above all Administration content;
7. exercise representative existing controls with permitted and denied fictional accounts.

No GitHub push, Render deployment, live database operation, external email, DNS/Zoho change or production-data
inspection was performed while preparing UI75.
