# Wavelink UI76 — Native Operational Records

**Core 1.34.19 · parent UI75 + UI74 + UI73 + UI72 + UI71 + UI70 + UI69 + UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI76 continues the stable native-workspace cutover after UI75 Administration. It replaces the active presentation
for Logs, Calendar, Fault Reports, HSE/QSHE and the shared report editor with direct route-owned markup and one
authoritative static stylesheet. It does not add another global shell or post-render decorator.

## Why this release exists

Source review found that the operational-record routes still loaded five historical stylesheets from different
interface generations:

- `logs_workspace.css`;
- `project_calendar.css`;
- `report_forms.css`;
- `fault_reports.css`;
- `qshe_reports.css`.

The old files contained useful functional selectors, but loading them independently let their spacing, cards,
forms, responsive rules and detail panes compete through stylesheet order. UI76 consolidates the required rules
into:

`app/static/operations_workspace_ui76.css`

The historical files remain in the cumulative source lineage for audit and recovery, but the active entry page
and service-worker cache no longer load them.

## Native route ownership

The following routes now render their final hierarchy directly inside the stable Wavelink shell:

- Logs catalogue and selected logbook;
- Calendar;
- Fault Reports;
- HSE / QSHE;
- shared Fault/HSE report editor.

The native screens provide consistent headings, data-grounded at-a-glance values, filters, saved-record cards,
master/detail presentation, forms, empty states and responsive stacking. The summary values are calculated only
from records already returned to the authorised route; UI76 does not create fictional operational totals.

## In-place list refresh and shared-host correction

Fault Reports and HSE/QSHE now refresh within the existing list host when that exact list route owns it:

- the current screen remains mounted;
- `aria-busy` communicates a refresh;
- returned records replace the list content without a loading-page flash;
- the shared report editor cannot be mistaken for the list merely because earlier generations reused a host ID.

This correction preserves the existing endpoints, permissions, assignment rules, report lifecycle and error
handling. UI76 adds no independent timer, route animation, MutationObserver or DOM re-parenting layer.

## Runtime delta

UI76 embeds **12 runtime records** over the exact UI75 parent:

- 8 modified runtime files;
- 4 new runtime/test files;
- 0 removed runtime files;
- 2,001 final manifest-tracked runtime files.

Modified application files:

- `app/static/fault_reports.js`;
- `app/static/index.html`;
- `app/static/logs.js`;
- `app/static/nav_shell.js`;
- `app/static/project_calendar.js`;
- `app/static/qshe_reports.js`;
- `app/static/report_forms.js`;
- `app/static/sw.js`.

New files:

- `app/static/operations_workspace_ui76.css`;
- `tests/ui76_native_operations/__init__.py`;
- `tests/ui76_native_operations/test_native_operations.py`;
- `tests/ui76_native_operations/browser_checks.py`.

Final runtime variant:

`workspace-ui76-native-operational-records-2026-09-30`

## Data and authority boundary

UI76 adds no database migration, reset, account conversion, permission key, operational API, recognition rule,
points adapter, completion adapter, environment variable or browser-storage writer. It does not create,
complete, approve, publish, close, assign or score an operational record merely by opening or filtering a page.

Mail Startup M01 remains byte-identical at:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

C01 company identity, G01 demonstration isolation, UI66 recognition data, saved records and existing backend
authority remain unchanged.

## Verification performed

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files, produced
2,001 manifest files and matched all 12 UI76 payload files byte-for-byte. Manifest integrity passed.

Dedicated UI76 checks verify:

- one authoritative operational-record stylesheet is loaded after the stable shell, recovery and Administration
  styles;
- the five historical route stylesheets are absent from the active document and service-worker cache;
- no new decorator, MutationObserver, timer, route animation or DOM re-parenting path is introduced;
- Logs, Calendar, Fault Reports, HSE/QSHE and the shared report editor own their final route hierarchy;
- Fault/HSE forced refresh reuses the exact list host and does not confuse the editor with the list;
- Fault Reports remained mutation-free for more than 9.2 seconds after settlement with real timers;
- 1440, 390 and 320 CSS-pixel checks have no document-level horizontal overflow.

The browser checks use fictional local fixtures. They are not live Render, SMTP, DNS, physical-device,
production-data or independent security acceptance.

## Apply the compact GitHub update

1. Keep the current UI75 commit available as the source rollback point.
2. Extract the UI76 update ZIP.
3. Optionally run `VERIFY_UI76_UPDATE.py --repository "PATH" --state before`.
4. Copy everything inside `UPLOAD_TO_GITHUB` into the existing **Wavelink application** repository.
5. Replace matching files; do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. Review the changed/new files in GitHub Desktop, commit and push normally.
7. Optionally run the verifier again with `--state after`.
8. After the intended service becomes healthy, reload one open tab once or close/reopen the installed app.

A database reset, company recreation, project import or browser-storage clear is not required.

## Acceptance after deployment

Use the fictional/demo service first:

1. open Logs, Calendar, Fault Reports and HSE/QSHE;
2. open and close one Fault or HSE report editor and confirm the correct list returns;
3. refresh the Fault and HSE lists and confirm the existing page remains mounted;
4. leave Fault Reports open for at least 15 seconds and confirm it does not blink or rebuild;
5. repeat Logs, Calendar and Fault Reports at phone width;
6. confirm account menus and dialogs stay above all operational-record content;
7. exercise representative existing create/edit controls with permitted and denied fictional accounts.

No GitHub push, Render deployment, live database operation, external email, DNS/Zoho change or production-data
inspection was performed while preparing UI76.
