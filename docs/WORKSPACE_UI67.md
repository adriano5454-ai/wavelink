# Wavelink UI67 — Experience Foundation

**Core 1.34.19 · parent UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI67 is a cumulative application release built on the verified UI66 profiles and recognition runtime. It
introduces the shared Wavelink experience foundation requested after reviewing the new visual concept. It is
not a replacement backend, a company reset, or the full future Home/dashboard redesign.

## Delivered experience

### Permanent identity and badge

After a named user signs in, the top bar now keeps the selected contribution badge visible while the user
moves between authorised modules. On wide screens it shows the badge name, tier and shareable point total;
on phones it collapses to the emblem. Selecting it opens **My profile**. The value comes from the existing
UI66 profile service and refreshes after a successful profile edit without adding a polling timer.

Badge identity remains cosmetic. It does not alter permissions, role, department, approval authority,
competency or operational access.

### First-class Profile and Team navigation

**My profile** and **Team** are now clear destinations in the left sidebar under **People & recognition**.
They retain the existing UI66 server checks for company membership, source privacy and record visibility.
Profile is no longer discoverable only through content near the bottom of Home.

### Compact account menu

The top-right account control now opens a compact identity-led menu containing only:

- My profile
- Account & access
- Workspace tools
- Sign out

The established full account/workspace dialog remains available through **Workspace tools**. When an editor
or unsent operational form is open, the account button keeps the existing safe-session behavior rather than
opening a second control surface over unfinished work.

### Account & access destination

**My profile → Account & access** presents sign-in ID, company workspace, project, controlled job role,
department, security account type, selected badge and the active session capability names. It provides the
existing change-password and Workspace tools actions. It is intentionally read-only for role, department,
permissions and points; it cannot be used for self-promotion.

### Supplied badge artwork

The user-supplied Wavelink badge exploration artwork was converted into 30 production WebP assets:

- ten cumulative tiers;
- Compass, Survey-wave and Subsea/sonar families at every tier;
- stable IDs matching the UI66 recognition service;
- 300 × 300 RGBA files with transparent outside pixels;
- image presentation at profile, feed, account and persistent-header sizes;
- retained inline non-authoritative fallback if an image is unavailable.

The original poster itself is not loaded by the application and its labels are not used as authority.

## Runtime delta

UI67 adds 41 embedded runtime records over the exact UI66 parent:

- 6 modified runtime files;
- 35 new runtime files, including 30 badge assets, two shared-shell resources and three UI67 tests;
- 1,965 final manifest-tracked runtime files;
- no removed runtime file.

No database schema, permission key, operational API, recognition rule, source adapter or environment variable
is added. Existing UI66 profile and recognition data is reused.

## Preserved boundaries

- Mail Startup M01 launcher remains byte-identical at
  `2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`.
- Company C01 identity, activation and persistent disk remain separate from demo G01.
- Existing UI66 users, passwords, invitation roles, permissions, recognition ledger, source records,
  signatures, shifts, notes and original files are not rewritten.
- Device-local unsent work, refresh protections and the established session-exit guard remain.
- Advanced account, backup, recovery, install and device controls remain reachable under Workspace tools.
- No secret, live database or company backup is included.

UI67 makes no schema change, but the existing UI66 forward-compatibility rule still applies: any database
already opened by UI66 recognition should remain paired with UI66-or-later software. A rollback must restore
the matching application commit and complete predeployment database backup.

## Local verification

The final cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files,
produced 1,965 manifest files, matched all 1,964 non-generated curated files byte-for-byte and passed complete
manifest integrity.

Local checks performed on the shipped/reconstructed runtime:

- UI67 experience tests: 8 passed;
- retained UI66 recognition tests: 18 passed;
- JavaScript syntax checks for all changed/new scripts;
- Chromium experience acceptance: 9 checks at 1440, 390 and 320 CSS pixels;
- no browser JavaScript errors;
- no horizontal-overflow failure.

The browser run used fictional TestClient data and local static assets. It did not inspect Render, production
IndexedDB, SMTP, DNS, real mobile hardware or production data.

## Apply the compact GitHub update

1. Preserve the current approved UI66 commit, full database backup, persistent-disk configuration and
   unfinished browser work.
2. Extract the UI67 delivery ZIP.
3. Optionally run `VERIFY_UI67_UPDATE.py --repository "PATH" --state before`.
4. Copy **everything inside `UPLOAD_TO_GITHUB`** into the current Wavelink application repository.
5. Replace matching files. Do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. Review the real GitHub Desktop diff, commit and push normally.
7. Optionally run the verifier again with `--state after`.
8. Preserve C01/G01 disks, identities, activation markers, secrets, SMTP configuration and service modes.
9. Do not reset, re-import, repeat company setup or clear browser storage.

The package changes repository source only. It does not push, deploy, migrate production, send email, change
DNS, validate Zoho or inspect live data.

## Staging acceptance

Using disposable named accounts and fictional records:

1. confirm the persistent badge follows the selected unlocked profile badge;
2. confirm Profile and Team are visible from the sidebar on desktop and phone;
3. confirm the compact menu contains only the four intended actions;
4. confirm Workspace tools still exposes the established advanced controls;
5. start an operational form, open Account and confirm the existing unsaved-work guard remains authoritative;
6. confirm Account & access is read-only for role, department, permissions and points;
7. change biography/badge and confirm the top-bar badge refreshes after the committed save;
8. revoke a source permission and confirm UI66 Team/profile privacy remains enforced;
9. verify offline reload after one connected load, including the selected badge asset;
10. verify no operational completion, approval, points or ledger behavior changed.

## Next visual batch

UI68 should use this foundation to redesign the real Home and Profile presentation around actual Wavelink data:
My shift, My work, Needs my action, saved handovers, open tasks, maintenance/certificate alerts and compact
Team recognition. It must not display invented vessel, staff or activity figures merely to reproduce the
concept image.
