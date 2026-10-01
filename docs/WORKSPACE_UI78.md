# Wavelink UI78 — Native Fleet Logistics Journey

**Core 1.34.19 · parent UI77 + UI76 + UI75 + UI74 + UI73 + UI72 + UI71 + UI70 + UI69 + UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI78 continues the native Fleet cutover with the record journeys that remained visually inconsistent after
UI77: Manifests, saved shipment records, Receiving & placement, Assets & transit, asset detail and Item journey.
The routes now own their final hierarchy directly and use explicit readable surfaces instead of inheriting
low-contrast rules from older logistics generations.

## Why this release exists

UI77 established one Fleet shell and one authoritative shared Fleet stylesheet, but several dense logistics
routes still rendered historical route structures. Their pale text, mixed card rules and old headings could
look like the previous GUI had returned. UI78 corrects that at the route itself rather than adding a decorator
or moving completed DOM after first paint.

The UI77 stylesheet remains the Fleet shell foundation. UI78 adds one final logistics stylesheet after it:

`app/static/fleet_workspace_ui78.css`

That stylesheet is scoped to the UI78 Fleet body and logistics route markers. It does not reactivate retired
Fleet stylesheets or create another navigation frame.

## Native logistics route ownership

UI78 directly owns the final hierarchy for:

- Manifests overview and saved shipment inspector;
- Receiving & final placement;
- Assets & transit catalogue;
- equipment/container detail;
- item custody journey.

The pages now use consistent module headers, data-grounded summary cards, filters, readable record cards,
contained tables, details and operational-boundary notices. Counts are calculated only from records already
returned to the authorised route.

Opening, searching or filtering these pages does not dispatch a Manifest, receive equipment, record final
placement, release quarantine, change quantity or approve equipment. Existing services and permission checks
remain authoritative for every write.

## Stable refresh behaviour

Receiving manual refresh now keeps the mounted workspace visible while the current saved records are read. It
uses `aria-busy` and a compact status chip rather than replacing the route with a temporary loading page.
UI78 adds no independent timer or polling loop to the logistics routes.

A real-timer browser scenario kept Receiving open for more than 9.2 seconds after settlement and recorded zero
workspace mutations.

## Runtime delta

UI78 embeds **7 runtime records** over the exact UI77 parent:

- 3 modified runtime files;
- 4 new runtime/test files;
- 0 removed runtime files;
- 2,009 final manifest-tracked runtime files.

Modified application files:

- `app/static/fleet.html`;
- `app/static/fleet.js`;
- `app/static/sw.js`.

New files:

- `app/static/fleet_workspace_ui78.css`;
- `tests/ui78_native_logistics/__init__.py`;
- `tests/ui78_native_logistics/test_native_logistics.py`;
- `tests/ui78_native_logistics/browser_checks.py`.

Final runtime variant:

`workspace-ui78-native-fleet-logistics-2026-09-30`

## Responsive behaviour

Browser acceptance covers all six logistics surfaces at 1440 CSS pixels, selected Manifests, Receiving, Assets
and asset-detail routes at 390 CSS pixels, and Item journey at 320 CSS pixels. Wide asset tables scroll inside
their own card; the document itself remains contained. Fleet navigation remains full-width and left aligned.

## Data and authority boundary

UI78 adds no database migration, reset, account conversion, permission key, operational API, recognition rule,
points adapter, completion adapter, source adapter, environment variable or browser-storage writer.

Mail Startup M01 remains byte-identical at:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

C01 company identity, G01 demonstration isolation, UI66 recognition data, saved Fleet records and backend
authority remain unchanged.

## Verification performed

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files, produced
2,009 manifest files and matched the curated UI78 runtime byte-for-byte. Manifest integrity passed.

Completed focused checks:

- 7 dedicated UI78 static/architecture tests;
- 16 retained UI65 roles/access tests with the exact M01 repository launcher;
- 18 retained UI66 recognition tests;
- 33 read-only logistics model/helper tests;
- 18 focused Fleet authentication, scope, receipt, placement, quarantine and journey lifecycle cases;
- 12 Chromium logistics scenarios at 1440, 390 and 320 CSS pixels;
- JavaScript syntax validation for the changed Fleet and service-worker scripts.

The browser checks use fictional local fixtures. They are not live Render, SMTP, DNS, physical-device,
production-data or independent security acceptance.

## Apply the compact GitHub update

1. Keep the current UI77 commit available as the source rollback point.
2. Extract the UI78 update ZIP.
3. Optionally run `VERIFY_UI78_UPDATE.py --repository "PATH" --state before`.
4. Copy everything inside `UPLOAD_TO_GITHUB` into the existing **Wavelink application** repository.
5. Replace matching files; do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. Review the changed/new files in GitHub Desktop, commit and push normally.
7. Optionally run the verifier again with `--state after`.
8. After the intended service becomes healthy, reload one open tab once or close/reopen the installed app.

A database reset, company recreation, project import or browser-storage clear is not required.

## Acceptance after deployment

Use the fictional/demo service first:

1. open Manifests, one saved shipment, Receiving, Assets, one asset and Item journey;
2. confirm no pale text or older heading/card presentation appears on those routes;
3. confirm the Fleet sidebar remains left aligned and account/dialog surfaces remain above content;
4. leave Receiving open for at least 15 seconds and confirm it does not blink or rebuild;
5. select Refresh and confirm the mounted route stays visible while records are read;
6. repeat Manifests, Receiving and Assets at phone width;
7. confirm the asset table scrolls inside its card and the overall document does not scroll sideways;
8. exercise representative existing dispatch, receipt, placement and quarantine actions with permitted and denied fictional accounts.

No GitHub push, Render deployment, live database operation, external email, DNS/Zoho change or production-data
inspection was performed while preparing UI78.
