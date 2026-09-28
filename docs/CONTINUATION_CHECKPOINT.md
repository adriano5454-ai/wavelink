# Wavelink checkpoint — UI57 + Company C01 + G01

28 September 2026; core1.34.19. User explicitly requests a visible shift-creation/coordinating area and
My shift opening only the signed-in person's actual assigned shift. Preserve polished/full capabilities,
minimal routine friction, section review→coherent build→one acceptance. No assumed deployed UI56/UI57.

## Verified source
Exact current/second UI56 package on full UI50 + verified UI51–55, not the earlier different UI56 report.
All164parent repository/1852runtime hashes verified; no live repository or company data read.
Parent extractor e88dfd8243b25708ba41fd4ed110bfe938360859f4efdd270fea9aa4924ddfa8.
UI57 extractor 0eb0cfca3ca0955f710f4e10dbc227f5ba2ced3f015597b464e8897ce7e9a0a1.
PatchID workspace-ui57-shift-workspaces-2026-09-28.
88 changed/new runtime resources / 539 cumulative overlays / 1856 tracked files.
Target166repository/165deploymentrows. Existing executable upload change only deploy/extract_source.py.
C01entrypoint f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2;
G01gate9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701;
Nginx752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8 unchanged.

## Implemented as one assignment/entry workflow
Separate Shifts & people tab/area, existing People & shifts heading shortcut. Authorized department cards
show current setup/shift names/hours/members, Create shifts or Edit, and View department handovers through
existing subject journal. Existing setup editor/transaction/permission roles retained; labels clarified.
Admin or current department head with create authority manages; ordinary members view their own department.
No new permission, automatic assignment/account, shared private note or attendance inference.

My shift no longer mounts the whole department board or uses a department selected elsewhere. New read-only
HandoverShifts projects only current own assignments and one resolved occurrence/own matching record. Admin
visibility is not assignment. Unassigned has explicit empty state. Multiple own assignments choose a unique
active one only if all clocks known, otherwise only-own chooser. UTC/GMT/Z or explicit UTC/GMT±HH:MM supports
server-clock active/next occurrence and previous operational day overnight; no inferred ship clock/IANA/DST.
Unknown descriptive basis requires explicit operational day, with device-only initial date suggestion.
Old unmatched personal work remains My saved notes; existing duplicate/period/context rules reopen retained
records without changing them. By day/subject and Incoming retain team/recipient views. All notes optional.

Two new authenticated/no-store read endpoints /api/handovers/simple/shifts and /api/handovers/simple/my-shift;
only existing appPython handovers_api.py attachment changes + new handover_shifts.py. 192 unchanged existing
app modules/194 total. Existing SimpleHandovers, DailyHandovers, Handovers, setup/open/action writers,
attachment/evidence/transfer formats unchanged. No new table/schema/permission/dependency/env/store.
One current 24h cycle per department: NOT multiple concurrent site rosters, rotation/leave/historic crew
planner. Read views don't create notes; normal open/save recheck authority/source/version and reuse receipts.

Frontend new shift_workspace.js/css plus scoped handovers controller and setup-heading help. Entire simple
notes editor/writers unchanged. Account/token/hub/route/root/read/modal epochs reject late/closed-dialog reads;
definitive denial clears protected background without touching open editor/local work. Refresh never auto
switches an active editor at shift boundary; no new interval timer. Same reply retains DOM/button closures.
No cache/queue/lease/signout/PWA/signing changes; other approved module bodies unchanged. Two hosted Help
bodies/outlines/catalogue updated,74otherssame/76matches; cache refs advance. No native/master PDF rewrite.

## Actual checks
**495 selected Python tests, 60 compound browser checks and 81 JavaScript syntax checks passed.** All 194 application Python modules parse; 192 existing modules remain unchanged. The frozen runtime has 1856 tracked files. Python groups: shifts_py=37, handovers_py=280, hosting_py=178. Browser groups: shifts_browser=19, certificates_browser=15, refresh_browser=26. These are selected checks, not full-suite or live deployment acceptance.

Final logs/commands/source audit and archive replay are authoritative, not inherited totals. Initial helper/fixture errors and two actual UI57 entry issues are retained/excluded: unchanged-response
button ownership and a just-closed creation chooser invalidating its own read. Both corrected before final
source freeze and covered by regressions. Earlier complete runs are superseded; final complete selections
rerun after the chooser correction. Screenshot waits allow the existing five-second toast to expire.
No unrelated historic test failure claimed fixed. No new report/rendering acceptance in this release.
Actual assets/fictitious SQLiteTestClient/injected fetch/hash/staged in-memory store, not durable IDB/SW,
normal navigation/WebSocket/physical/WindowsPowerShell/native/fullsuite/securityaccessibilityload/Docker/
offhost recovery acceptance. UI55 concurrent33.5s refresh and UI56 certificate browser checks retained.
No real credentials, data, external network, remote deployment or company settings touched.

## Preserve / next
Keep activated Sulmara C01 ID/domain/dedicateddisk/marker INITIALISE_COMPANY=NO removedbootstrap; separate
G01demo settings/users/domain/disk. Backups/approvedcommit/.git/independent edits/unsentmain+separatelogwork.
No reset/reimport/site-data clear/syncdisable/repeatedsetup/incompatiblepreC01/preUI34writer rollback.
Source rollback cannot recover deliberately discarded work; unsent notes remain in-tab until saved.
Use compact changed-file copy/review/commit/push, optional checker; both services may auto-deploy samebranch.
Next real named lead/worker/overnight/unassigned/phone/oldrecord resumption check, then resume section review.
Wider roadmap preserved; no automatic background work or assumed live UI57.

Installed-app follow-up still pending: user confirms Chrome-installed app (older native .exe also existed);
provided shortcut chrome_proxy.exe --profile-directory=Default --app-id=bfoeojghfbddilebjmmlpobdfopiongn.
Prior offline identity calculation matched demo origin, not live verification. Approved ICO already supplied
for shortcut appearance; current PWA manifest still has no launch_handler. Desired focus existing correct
company/profile mainwindow without closing/reloading unsent work; don't collapse intentional logwindows.
This release does not change launcher/icon/native binary. Verify current browser support/installed behaviour
before delivering that change; no browser-storage reset/uninstall. Nativevessel/CCVD/cloudsync/localnetwork
remain outside current hosted work.
