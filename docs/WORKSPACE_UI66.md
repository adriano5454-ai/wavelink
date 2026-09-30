# Wavelink UI66 — profiles, Team updates and contribution recognition

**Core 1.34.19 · UI66 · Mail Startup M01 · Company C01 · demo G01 · 29 September 2026**

UI66 is an actual cumulative application release built from the clean UI65 repository at commit
`ac05fa4324904fa65efdf4eb2d3f0ff1ce1cbe65`. It adds company-scoped member profiles, a
permission-aware Team feed, reversible likes, an auditable contribution ledger, frozen 1/3/5-point
source values, cumulative tiers and three original badge choices per tier.

This is not the earlier diagnostics-only fallback bundle. The UI66 extractor contains **33 real
runtime deltas** against UI65: **25 modified files and 8 new files**. A clean reconstruction produces
variant `workspace-ui66-profiles-recognition-2026-09-29` with **1,930 manifest-tracked runtime files**.

## What changed

### Profiles

Named approved members receive a per-company profile. A member may edit their biography, verified
avatar and selected unlocked badge. Job role, department, account authority and contribution totals
remain controlled by their source systems. Private email is not exposed through the directory.
Pending, suspended and temporary QR identities do not receive community access.

### Home and Team updates

Home remains personal-first. A compact Team updates panel links to a dedicated Team workspace. One
committed qualifying accomplishment creates one event. Source visibility is rechecked before a title,
contributors, reaction count or link is returned; private tasks and restricted events are not
broadcast. Likes are one-per-member, reversible and idempotent. They never award points or approve an
operational record.

### Contribution points

The public source control is **1 / 3 / 5**, defaulting to 1. Higher values require the existing
source-specific builder or management authority and are rejected server-side when crafted by an
ordinary participant. The value is frozen into a signed-format source marker before work begins.
Existing UI65 records have no UI66 marker and are not retrospectively scored.

Initial source adapters are:

| Source | Qualifying committed outcome |
|---|---|
| Task | Reviewed completion; actual documented workers, not the final reviewer |
| Maintenance | Completed work order; recorded workers, not every step |
| Checklist | Required stages final; one award per reliable contributor for the run |
| Handover | First valid finish/publication of the canonical occurrence |
| Toolbox Talk | Saved named-member acknowledgement; native/QR deduplicated |
| Standalone stock verification | Deliberate closure; task-owned counts do not score twice |

Issue, Missing and N/A results are not penalised. Likes, saves, edits, template cloning, approvals,
incident counts and ordinary audit rows do not score.

### Durable recognition storage

UI66 installs additive recognition schema version 1:

- `recognition_meta`
- `member_profiles`
- `recognition_events`
- `recognition_awards`
- `recognition_ledger`
- `recognition_reactions`
- `recognition_operations`
- `recognition_outbox`
- `recognition_repair_cursors`

The ledger is append-only for awards, reversals and restorations. Natural keys and unique constraints
make retries/concurrent projection duplicate-safe. Recognition projection failure does not roll back a
valid operational save; a durable outbox and repair cursor reconcile committed source audit rows.

### Tiers and badges

Thresholds are cumulative: Starter 0, Bronze 25, Silver 50, Gold 100, Platinum 150, Emerald 225,
Diamond 325, Master 500, Grandmaster 750 and Legend 1,000. Every tier provides three original inline
SVG families: Compass crest, Survey-wave crest and Subsea sonar crest. Badges are cosmetic and never
grant competency, approval, permissions or job authority.

## Migration and recovery

Opening a project under UI66 installs the additive schema and one activation boundary. A direct
UI65-to-UI66 fixture check preserved existing user IDs, password hashes and an existing operational
record byte-for-byte, while creating zero retrospective profiles, events, awards, ledger entries,
reactions or outbox rows.

A complete same-company backup retains recognition history. A selective/new-company transfer retains
only the recognition schema/activation metadata and clears company projection rows so identity,
profiles, points and reactions are not transferred as authority.

After UI66 opens a project, keep UI66-or-later software with that database. Do not run UI65 or earlier
against it as a rollback method. Roll back with the matching pre-deployment application commit and
complete database backup.

## Preserved boundaries

- `deploy/company_entrypoint.py` remains byte-identical at `2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`.
- C01 identity/activation, the separate G01 demo, SMTP configuration, disks and setup markers are not
  changed by UI66.
- Existing UI65 membership roles, invitation snapshots, passwords, account IDs and explicit policies
  are not mass-updated.
- Original files, shifts, saved notes, signatures and device-local unsent work are not reset.
- No secret or live company database is included.

## Local verification performed

- Fresh source-parts reconstruction: 1,605 upstream files verified; 1,930 target manifest files.
- Reconstructed application bytes match the curated UI66 build for all 1,929 non-generated files.
- Dedicated UI66 recognition suite: 18 passed.
- General Tasks functional suite: 32 passed in an isolated process.
- During the build, isolated functional groups also passed for maintenance cycles, inventory review,
  checklist workflow, Toolbox Talks, simple handovers, UI64 membership compatibility, UI65 role/access
  and handover privacy/transfer. Their grouping is recorded in `DELIVERY_CHECKS.json`; a single broad
  combined run is intentionally not claimed because cumulative fixtures exceeded the environment limit.
- Real Chromium asset acceptance: 10 checks at 1440, 390 and 320 CSS px, no JavaScript error and no
  horizontal overflow. It used fictional TestClient-backed data, not a live Render deployment.
- Exact UI65 migration fixture: identities and source record preserved, no retroactive awards.

One direct legacy release-contract test already fails on the unchanged UI65 baseline because its
historical delta stripper predates later source overlays. It is not represented as a new UI66
regression or as a pass.

## Apply the compact GitHub update

1. Preserve the current approved commit, a complete database backup, persistent-disk configuration and
   unsent browser work.
2. Extract the delivery ZIP.
3. Copy **everything inside `UPLOAD_TO_GITHUB`** into the existing UI65 Wavelink application repository.
4. Replace matching files, but do not replace `.git` or delete files absent from the update.
5. GitHub Desktop should show genuine UI66 changes, including a modified `deploy/extract_source.py` and
   two new UI66 documentation files.
6. Review the diff, commit and push to the application repository—not `Wavelink-Website`.
7. Preserve C01/G01 disks, identities, activation markers, environment values and service modes.
8. Do not reset, re-import, repeat company setup or clear browser storage.

The package changes repository source only. It does not push, deploy, migrate the production database,
send email, validate Zoho, change DNS or inspect live data.

## Staging acceptance

Use disposable accounts and fictional records. Confirm existing UI65 access first; then test profile
privacy, restricted-source feed exclusion, one visible accomplishment, like/unlike, exact one-time
award, retry deduplication, reversal/restoration, all six adapters, 1/3/5 authority, tier boundaries,
locked badge refusal, complete backup/restore, and a deliberate projection outage followed by
reconciliation.

## Provenance

- Parent extractor SHA-256: `de8c364f9395fb9ef9ef96d5bff70b5a52670a8d1044404ad85f11a287a3a2c5`
- UI66 extractor SHA-256: `2c9e15d2e653d736bbab91155074f3e5f5846664954a4d7c0bebddb87a783977`
- M01 launcher SHA-256: `2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`
- Final `UI_PATCH.json` SHA-256: `2435b043f0a5d06e433a41356cb373eb79081b638c2e615ebd45b0815898c995`
- Final `RELEASE_FILES.json` SHA-256: `900fe4a39c1140102ac29c02626b15a38ed65c370ba41c727def9f10a40182d5`
