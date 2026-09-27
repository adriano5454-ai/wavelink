# Wavelink checkpoint — UI51 + Company C01 + working G01

27 September 2026; core1.34.19. Implements the previously completed Calendar review as one coherent
section update. Easier means polished, discoverable, fully capable; keep the agreed review then build
cycle. Compact GitHub copy/review/commit/push, optional PS1, separate evidence. No assumed live UI51.

## Verified source

Parent full UI50 archive a9e3452da15435653281425696449aefe1afadb88a1630ac949f4b2a08f1e8d2:
152 repository and1823 runtime files verified. Parent extractor
75059dd5c30110258165938c888fbb98ff4cb8293bd33425a0ab767396cb23f0.
UI51 extractor 338f9a5e1dfa212f8f8d8afed544c54eff8f4a936694a25871eaf8b0699f3aee.
PatchID workspace-ui51-calendar-navigation-stability-2026-09-27.
94 changed/new runtime resources, 511 cumulative overlays, 1832 tracked runtime.
C01 entrypoint f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2;
G01 gate9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701;
Nginx752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8 unchanged.
Only existing executable repository change: deploy/extract_source.py. No source reset or branch substitution.

## Implemented

Compact Month/Agenda/period controls, expandable categories+title/source/date search; all8sources and
4defaults retained. Search is limited to returned month; explicit2000cap/total/truncation. Agenda dated
event distinct from source status, no universal overdue/readiness meaning. Auth-scoped temporary prefs/
reading anchors reset on account/project; same-account return/refresh preserves where applicable.
Stable keyed grid/day/event rows; temporary error labels last saved data and disables stale opening;
definitive denial clears dates even behind interrupted modal, preserves editor/local work. Account/token/
query/route/root/request/modal generations reject superseded callbacks, no persist/save writer added.
Checklist backend href/status selects recognised saved phase; normal click freshly rechecks firstunfinished/
lastfinal phase and uses normal router/participation. Manifest exact embeddedFleet route. Log lookup guards
both reads through old Calendar context; cannot open over Home/newer form. Source access not expanded.

Only app/project_calendar.py changes among193existing Python modules (192unchanged); read-only projection,
no new routes/tables/permissions/dependencies/environment/stores. New scoped project_calendar.js/css;
assets.js Calendar delegation+log handoff only; remaining asset/cert/maintenance form spans byte-identical.
Main app.js only render sync hook; approved operational scripts, shared writers, C01/G01 and report generators
unchanged. All 77 JS syntax checks; Python parses193. UI45 signout/localowner and all evidence preserved.
Only assetcalendar Help body changes,75otherssame,all76 catalogue matches. No native/masterPDF rebuild.

## Verification and limits

**502 selected Python tests** and **132 compound browser checks** passed, plus syntax checks for **77 application JavaScript files** and parsing of **193 Python modules**. The frozen runtime contains **1832 tracked files**. Python groups: calendar_py=54, c01_py=71, gateway_py=107, local_builders_py=47, approved_py=192, handovers_py=31. Browser groups: checklists_browser=10, builders_browser=9, signout_browser=13, stability_browser=16, tasks_browser=31, home_browser=15, logs_browser=13, calendar_browser=25. All final selected groups were rerun after the test-only cache-version correction; production application bytes were unchanged by that correction. Source audit and final ZIP replay are separately recorded. These are selected tests, not a full-suite result.

Earlier partial combined pytest and browser runs excluded. Harness arguments/path-hold selection and
permission-dependency restoration corrected; inherited Home service-worker cache assertion advanced toUI51
without dropping its cache tests. No unrelated historical failure declared fixed. Final candidate tests
and archive replay recorded in DELIVERY_CHECKS and verification, repeated gateway checks not extra coverage.
Actual shipped browser assets, fictional SQLite/TestClient, controlled fetch/hash and staged store; not
live/normalnavigation/durableIDB/SW/physical/WindowsPowerShell/native/fullsuite/fullsecurityaccessibilityload/
Docker/offhost acceptance. No navigation-policy bypass, real data/credentials or remote operations.

## Preserve and next

Keep separate activated Sulmara C01 company ID/domain/disk/marker, INITIALISE_COMPANY=NO/removedbootstrap;
separate G01demo settings/users/permissions/domain/disk, approvedcommit/backup/.git/outsideedits/unsentwork.
No reset/reimport/site-data clear/syncdisable/incompatiblepreC01/preUI34writer/exporter. UI50 source rollback
can restore old Calendar presentation but never recover local entries deliberately discarded; no data rollback.
Calendar does not edit source dates, complete/sign work, send reminders, or introduce independent scheduling.

One real fictional named-user Calendar/source/changed-date/return/permission/phone check, then next agreed
sidebar-section review, not an unrequested redesign of approved sections. Wider roadmap retained in
DEVELOPMENT_TODO, including imports/evidence/maintenanceQR/admission/recovery/security. New calendar event
creation/export/additional sources/recurrence are separate future scope. Nativevessel/CCVD/cloudsync/local
phone-network work remain outside this update. No automatic background development.
