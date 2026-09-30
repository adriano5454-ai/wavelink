# Wavelink UI69 — Professional Work Execution

**Core 1.34.19 · parent UI68 + UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI69 is a cumulative presentation release built on the exact verified UI68 runtime. It brings the first
operational workflow group—Tasks, Maintenance, Checklists, Handovers and Toolbox Talks—into the shared
Wavelink visual and interaction system without changing the services that decide access, saved evidence,
approvals, completion or recognition.

## Delivered experience

### One operational visual language

All five workspaces now share:

- a compact maritime module header with a recognisable module mark, purpose statement, Help and daily actions;
- a clear primary action, quieter refresh/draft controls and consistent 40–44 px targets;
- segmented operational views, consistent search/filter surfaces and calmer empty states;
- consistent list/inspector cards for saved work;
- responsive desktop, phone and narrow-phone layouts;
- the existing UI67 top bar, permanent selected badge, compact account menu and left navigation.

The module header is intentionally smaller and more operational than the Home concept hero. It establishes
identity without pushing the current work below the fold.

### Daily work before setup tools

Reusable builders and administrative setup remain available, but no longer compete with the daily primary
action in a long button row:

- Maintenance groups Create routine, Import routine and View routines under **Routines & setup**;
- Checklists groups the existing template-library action under **Templates & setup**;
- Handovers groups People & shifts and the existing preparation actions under **People & preparation**;
- Toolbox Talks groups Create form, Import form and View forms under **Forms & setup**.

The existing control nodes are moved into progressive-disclosure containers after their module has rendered;
they are not re-created and their established handlers remain attached. New task, new work order, new
checklist, create handover, new toolbox talk, refresh and local-draft controls stay directly visible.

### Shared operational forms

Existing Task, Maintenance, Checklist, Handover and Toolbox form surfaces receive a consistent hierarchy for
sections, fields, notices and action footers. UI69 does not change required fields, validation, signatures,
acknowledgements, evidence, result choices, save/submit/finalise boundaries or unsent-work behavior.

## Runtime delta

UI69 embeds **9 runtime records** over the exact UI68 parent:

- 4 modified runtime files;
- 5 new runtime files: `work_execution.css`, `work_execution.js` and three UI69 verification files;
- 1,973 final manifest-tracked runtime files;
- no removed runtime file.

The new decorator is presentation-only. It performs no API request, polling timer, browser-storage write or
workflow transition. Backend and authority modules remain byte-identical to UI68.

## Preserved boundaries

- Mail Startup M01 launcher remains byte-identical at
  `2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`.
- Company C01 identity, activation and persistent disk remain separate from demo G01.
- Existing accounts, invitations, roles, permissions, records, recognition data, source privacy, files,
  signatures, shifts, notes and audit history are not rewritten.
- Private Tasks remain private; UI69 does not expand list or record audience.
- Checklist item approval/finalisation, Maintenance completion, Handover publication and Toolbox personal
  acknowledgement keep their established meanings.
- Device-local drafts, queued work, unsaved-work guards and request/session controls remain.
- No database schema, permission key, operational API, scoring rule, source adapter or environment variable is
  added.

UI69 has no schema migration. The existing UI66 compatibility boundary still applies: a database already
opened by UI66 recognition should remain paired with UI66-or-later application software. A rollback must
restore the matching application commit and corresponding complete database backup.

## Local verification

The cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files,
produced 1,973 manifest files and passed manifest integrity. All 9 embedded UI69 files matched the curated
build byte-for-byte.

Checks on the freshly reconstructed runtime include:

- 6 dedicated UI69 presentation and source-boundary tests;
- 6 retained UI68 Home/Profile tests;
- 8 retained UI67 experience-shell tests;
- 32 General Tasks functional tests;
- JavaScript syntax validation;
- Chromium acceptance for all five workspaces at 1440 and 390 CSS pixels, plus Tasks, Handovers and Toolbox
  Talks at 320 CSS pixels;
- 13 browser scenarios with no page JavaScript error or document-level horizontal overflow.

Three separate native Tk General Tasks tests require a graphical display and therefore error in this headless
container before exercising application behavior; the browser workspace was tested instead. Historical
exact-release/cache assertions from earlier releases are not represented as current UI69 passes.

The browser run uses fictional local TestClient data and local assets. It does not inspect Render, production
IndexedDB, SMTP, DNS, physical devices or production data.

## Apply the compact GitHub update

1. Preserve the approved UI68 commit, complete company/database backup, persistent-disk configuration and
   unfinished browser work.
2. Extract the UI69 delivery ZIP.
3. Optionally run `VERIFY_UI69_UPDATE.py --repository "PATH" --state before`.
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

1. open all five workspaces as Administrator and as a participant and confirm the same authorised records and
   actions remain available;
2. verify the primary daily action stays visible and setup/builder actions remain reachable in their grouped
   control;
3. start and close each create form without saving; confirm existing unsaved-work protection still applies;
4. complete one ordinary workflow in each module and compare its saved evidence/state with UI68 behavior;
5. confirm private Tasks and restricted source details remain inaccessible to an unauthorised account;
6. confirm Help still opens in a separate tab;
7. confirm desktop, phone and narrow-phone routes have no document-level horizontal scroll;
8. confirm the permanent selected badge, compact account menu and Account & access page remain available;
9. confirm opening, filtering or changing a visual tab creates no operational write or recognition award;
10. restart the intended staging service and re-check one saved record in each module.

## Next coherent visual batch

UI70 should apply the same design system to equipment and logistics: Inventory, boxes/subitems, Manifests,
item movement/receipt, stock verification, Certificates and Fleet context. Keep QR, custody, quantity,
certificate and manifest authority unchanged.
