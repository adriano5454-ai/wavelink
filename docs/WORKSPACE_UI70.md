# Wavelink UI70 — Equipment and Logistics Experience

**Core 1.34.19 · parent UI69 + UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI70 is a cumulative presentation release built on the exact verified UI69 runtime. It brings Inventory,
boxes and subitems, stock verification, Certificates, connected asset identity and Fleet logistics into the
same Wavelink visual and interaction system as Home, Profile and the UI69 work-execution modules. The services
that decide custody, quantities, manifest state, receiving, placement, document access, QR identity and audit
history remain authoritative.

## Delivered experience

### One equipment identity across the workflow

The equipment-and-logistics surfaces now share a compact maritime module header, consistent actions, cards,
forms, filters and responsive spacing. The presentation explicitly reinforces that the same controlled item
continues through:

- Inventory catalogues, boxes and subitems;
- equipment identity and connected asset details;
- Fleet allocation and current custody;
- Manifest planning, dispatch, receiving and final placement;
- item journey and movement evidence;
- stock verification and low-stock attention;
- linked Certificates and source files;
- Fleet calendar, setup and vessel logbook context where already authorised.

Browsing a view does not create a physical movement, receipt, placement or quantity change.

### Daily actions before setup and report tools

Existing controls remain reachable while less-frequent controls no longer compete with the primary workflow:

- Inventory create/import controls are grouped under **Inventory setup**;
- stock verification history/PDF controls are grouped under **Evidence & reports**;
- Certificate local forms/calendar controls are grouped under **Register tools**;
- direct refresh, new-record, back and saved-form controls stay visible where already provided.

UI70 moves the existing DOM nodes after their workspace has rendered. It does not create replacement workflow
buttons, and their established event handlers remain attached.

### Fleet context without a second visual product

The separate Fleet document keeps its own session and routes but now uses the same equipment-and-logistics
language. Sites, Manifests, receiving, assets in transit, item journey, calendar, setup and logbooks receive a
consistent header and responsive treatment without changing Fleet APIs or access decisions.

## Runtime delta

UI70 embeds **8 runtime records** over the exact UI69 parent:

- 3 modified runtime files: `index.html`, `fleet.html` and `sw.js`;
- 5 new runtime files: `logistics_experience.css`, `logistics_experience.js` and three UI70 verification files;
- 1,978 final manifest-tracked runtime files;
- no removed runtime file.

The new decorator is presentation-only. It performs no API request, polling timer, browser-storage write or
workflow transition. Backend, authority, inventory, Fleet, certificate and recognition services remain
byte-identical to UI69.

## Preserved boundaries

- Mail Startup M01 launcher remains byte-identical at
  `2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`.
- Company C01 identity, activation and persistent disk remain separate from demo G01.
- Existing accounts, invitations, roles, permissions, records, recognition data, files, signatures, shifts,
  notes and audit history are not rewritten.
- QR labels remain identifiers/locators; UI70 does not turn a scan into authority or verification.
- Receipt, placement, custody release, quantity adjustment and stock-verification closure retain their existing
  confirmation and permission rules.
- A Certificate register entry remains evidence/administration, not equipment approval or operational release.
- Unknown quantity remains unknown rather than being presented as zero.
- Device-local drafts, queued work, unsaved-work guards and request/session controls remain.
- No database schema, permission key, operational API, scoring rule, source adapter or environment variable is
  added.

UI70 has no schema migration. The existing UI66 compatibility boundary still applies: a database already
opened by UI66 recognition should remain paired with UI66-or-later application software. A rollback must
restore the matching application commit and corresponding complete database backup.

## Local verification

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files,
produced 1,978 manifest files and passed manifest integrity. All 8 embedded UI70 files matched the curated
build byte-for-byte.

Checks on the freshly reconstructed runtime include:

- 6 dedicated UI70 presentation and source-boundary tests;
- JavaScript syntax validation for 111 JavaScript files;
- Chromium acceptance at 1440, 390 and 320 CSS pixels;
- 23 browser scenarios spanning Inventory, boxes, stock verification, Certificates, connected asset, low-stock,
  Fleet sites, Manifests, receiving and current assets;
- no browser JavaScript error, duplicate Help link or document-level horizontal overflow in those scenarios;
- action targets measured at 40 px or greater in the checked equipment/logistics headers.

Historical exact-release service-worker cache assertions from UI67–UI69 are not represented as current UI70
passes because UI70 deliberately advances the cache identifier. Slow environment-heavy QR/PDF suites are not
claimed as complete by this focused release verification.

The browser run uses fictional local TestClient data and local assets. It does not inspect Render, production
IndexedDB, SMTP, DNS, physical devices or production data.

## Apply the compact GitHub update

1. Preserve the approved UI69 commit, complete company/database backup, persistent-disk configuration and
   unfinished browser work.
2. Extract the UI70 delivery ZIP.
3. Optionally run `VERIFY_UI70_UPDATE.py --repository "PATH" --state before`.
4. Copy **everything inside `UPLOAD_TO_GITHUB`** into the current Wavelink application repository.
5. Replace matching files. Do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. GitHub Desktop should show 9 modified repository files and 2 new repository files.
7. Review the diff, commit and push normally.
8. Optionally run the verifier again with `--state after`.
9. Preserve C01/G01 disks, identities, activation markers, secrets, SMTP settings and service modes.
10. Do not reset, re-import, repeat company setup or clear browser storage.

The package changes repository source only. It does not push, deploy, migrate production, send email, change
DNS, validate Zoho or inspect live data.

## Staging acceptance

Using disposable named accounts and fictional records:

1. open Inventory, stock verification, Certificates, a connected asset and all relevant Fleet routes as
   Administrator and as a participant; confirm the same authorised records/actions remain;
2. verify direct daily actions remain visible and grouped setup/report controls remain reachable;
3. create a box and subitem, then confirm their identity and containment are unchanged after refresh/restart;
4. create one fictional Manifest and exercise dispatch, receipt and placement using the existing confirmations;
5. confirm browsing alone never moves an item, changes quantity or closes a verification;
6. confirm QR output and scans preserve existing scope and do not grant authority;
7. confirm Certificate source files and linked assets retain the same audience and evidence semantics;
8. confirm Help still opens in a separate tab and there is no duplicate Help action;
9. confirm desktop, phone and narrow-phone routes have no document-level horizontal scroll;
10. restart the intended staging service and re-check one saved Inventory, Manifest and Certificate record.

## Next coherent visual batch

UI71 should bring Administration, Members/Roles, builders, Calendar/Logs, Fault/HSE/QSHE and remaining report
surfaces into the shared design system while preserving every existing authority, privacy and evidence rule.
