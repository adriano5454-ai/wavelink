# Wavelink UI68 — Data-grounded Home and Profile

**Core 1.34.19 · parent UI67 + UI66 + Mail Startup M01 + Company C01 + G01 · 30 September 2026**

UI68 is a cumulative presentation release built on the verified UI67 experience shell and UI66 recognition
services. It brings the real Personal Home and My profile closer to the accepted Wavelink visual direction
without adding fictional dashboard figures or replacing the operational backend.

## Delivered experience

### A real personal Home

Home now opens with a compact Wavelink maritime header and a personal operational overview. Every number and
record shown comes from an existing authorised source:

- **My work** uses the current personal-home work count and records;
- **Needs my action** uses the current authorised action queue;
- **Saved handovers** uses the current member's saved handover count and records;
- **My shift** uses the established simple My-shift service;
- **My activity** keeps the existing personal activity view;
- **My profile** uses the current company-scoped profile and recognition progress;
- **Team updates** uses the existing privacy-aware recognition feed.

The existing status/type filters, pagination, direct record actions, manual Home refresh, unsaved-work access
and Workspaces link remain. Opening Home does not create, complete, approve or score operational work.

UI68 deliberately does not invent active-vessel, staff-online, task, maintenance or certificate totals merely
to reproduce a concept image. An unavailable value remains absent or is described as unavailable.

### A clearer Profile destination

My profile now presents:

- member identity, controlled job role and department;
- selected contribution emblem;
- editable introduction and existing profile action;
- real team-shareable contribution total, current tier and next threshold;
- an auditable contribution-history section;
- all ten cumulative badge tiers in a progressive-disclosure gallery.

The current tier is expanded and immediately selectable. Earlier unlocked designs remain available. Locked
future tiers stay visible but collapsed, so the page is understandable without rendering thirty large cards at
once. Badge choice, biography and avatar remain the only profile-controlled identity fields; role, department,
permissions and points remain server-controlled.

### Professional responsive presentation

The new Home and Profile surfaces use the UI67 shell, account menu, permanent badge, sidebar and shared Help
behavior. A new original local SVG scene supports the Home header without remote resources or third-party
tracking. The layouts were exercised at 1440, 390 and 320 CSS pixels.

## Runtime delta

UI68 adds 11 embedded runtime records over the exact UI67 parent:

- 8 modified runtime files;
- 3 new runtime files: one local visual asset and two UI68 verification files;
- 1,968 final manifest-tracked runtime files;
- no removed runtime file.

No database schema, permission key, operational API, recognition rule, source adapter, environment variable or
backend writer is changed. Existing UI63 personal-home and UI66 profile/recognition endpoints are reused.

## Preserved boundaries

- Mail Startup M01 launcher remains byte-identical at
  `2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`.
- Company C01 identity, activation and persistent disk remain separate from demo G01.
- Existing accounts, invitations, roles, permissions, operational records, recognition ledger, award rules,
  source privacy, signatures, shifts, notes and original files are not rewritten.
- Device-local unsent work and established request/session guards remain.
- UI68 adds no independent polling timer.
- No secret, live database or company backup is included.

UI68 makes no schema change, but the existing UI66 forward-compatibility rule still applies: any database
already opened by UI66 recognition should remain paired with UI66-or-later software. A rollback must restore
the matching application commit and complete predeployment database backup.

## Local verification

The final cumulative extractor was replayed from the pinned source parts. It verified 1,605 upstream files,
produced 1,968 manifest files and passed complete manifest integrity. The curated and freshly reconstructed
runtime matched byte-for-byte outside generated release/provenance files.

Checks performed on the reconstructed runtime include:

- UI68 Home/Profile tests;
- retained UI67 experience tests;
- retained UI66 recognition tests;
- JavaScript syntax and SVG parse checks;
- Chromium Home/Profile acceptance at 1440, 390 and 320 CSS pixels;
- real fictional personal counts, records, profile progress, authorised Team updates and collapsed tier gallery;
- no browser JavaScript error or horizontal-overflow failure.

The browser run used fictional local TestClient data and local assets. It did not inspect Render, production
IndexedDB, SMTP, DNS, real mobile hardware or production data.

## Apply the compact GitHub update

1. Preserve the approved UI67 commit, complete database backup, persistent-disk configuration and unfinished
   browser work.
2. Extract the UI68 delivery ZIP.
3. Optionally run `VERIFY_UI68_UPDATE.py --repository "PATH" --state before`.
4. Copy **everything inside `UPLOAD_TO_GITHUB`** into the current Wavelink application repository.
5. Replace matching files. Do not replace `.git`, delete unrelated files or use `Wavelink-Website`.
6. Review the real GitHub Desktop diff, commit and push normally.
7. Optionally run the verifier again with `--state after`.
8. Preserve C01/G01 disks, identities, activation markers, secrets, SMTP configuration and service modes.
9. Do not reset, re-import, repeat company setup or clear browser storage.

The package changes repository source only. It does not push, deploy, migrate production, send email, change
DNS, validate Zoho or inspect live data.

## Staging acceptance

Using disposable named accounts and fictional operational records:

1. confirm Home counts equal the member's actual authorised personal queues;
2. confirm My work, Needs my action, Saved handovers and My activity keep their filters and links;
3. confirm My shift truthfully shows the assigned shift or the empty state;
4. confirm the Home profile summary and permanent header badge reflect the committed profile;
5. confirm Team updates exclude private/restricted records and likes remain non-scoring;
6. confirm Profile shows real contribution progress and only the current/unlocked tier is expanded by default;
7. confirm an unavailable backend value is not replaced with a fictional statistic;
8. confirm Home/Profile at laptop and phone widths have no horizontal overflow;
9. confirm opening or refreshing Home performs no operational completion, approval or scoring write;
10. confirm the compact account menu, Account & access, Workspace tools and unsaved-work guard remain intact.

## Next visual batch

UI69 should apply the shared design system to the first operational workflow group—Tasks, Maintenance,
Checklists, Handovers and Toolbox Talks—without changing their authority, evidence or completion semantics.
