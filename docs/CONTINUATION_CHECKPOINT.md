# Wavelink checkpoint — UI58 + Company C01 + G01

28 September 2026; core1.34.19. User asks explicit permissions for new actions such as creating shifts,
then interrupts to report too much unrelated information under My shift. Both treated as one update.
Polished/full capabilities, user-friendly not basic; compact GitHub copy/review/commit/push, PS1 optional.

## Verified source
Exact UI57 over full UI50 and verified UI51–57; 166 parent repository files/1856 runtime hashes checked.
Parent extractor0eb0cfca3ca0955f710f4e10dbc227f5ba2ced3f015597b464e8897ce7e9a0a1.
UI58 extractor b26af15ffa197f2ef92f8dd04411d658b19b37c9f7c7cecda9864bc80d171a86.
PatchID workspace-ui58-explicit-shift-permissions-2026-09-28.
95 incremental resources / 542 overlays / 1857 tracked runtime.
Target168repo/167deployment rows. Only existing executable repository change deploy/extract_source.py.
C01entrypointf754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2;
G01gate9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701;
Nginx752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8 unchanged.

## Explicit permissions
Three new keys: handovers.shifts_manage (schedule names/hours/site/basis), handovers.shifts_assign
(people in existing schedule), handovers.shifts_all_departments (scope extension, not an action).
Base handovers.view dependency; extension requires at least one action. Defaults all OFF for non-admins,
including existing heads and supervisors. No automatic user/role/roster rewrite. Admin retains all.
No implicit department-head fallback. Administrator reviews old coordinators once and grants deliberately.
Permission edits retain meaningful reason and session revocation; no new session/authentication policy.
Existing policy JSON/additive operation receipt keys, no new table/schema/API/env/dependency/browser store.

Scope is current active membership unless explicit all-department extension. That scope applies to
coordination only: private notes, personal handover creation outside membership, My shift assignments,
user administration and other modules retain their own boundaries. Schedule/assign-only UI differences
match actual backend changed-field validation. A coordinator does not need handovers.create but newly
assigned authors do. Retained unchanged unavailable members remain; new/reassigned ones must be eligible.
Schedule-only cannot shorten shifts by removing assignments. Exact-operation retries require current
scope and original action grants; no recreated requests or assignment drops to recover uncertain saves.

Access review and actual permission editor show groups/hints. Existing five builder and three QR flags
are reused, not duplicated. Operational preset excludes all-departments shift scope and backups.
Five existing appPython changed: access, access_review, simple_handovers (coordination functions only),
handover_overview projection and handover_shifts._rows. 189 existing Python modules unchanged,194total.
SimpleHandovers.open/action, original note editor, evidence/QR/reports/transfer/routes unchanged.

## Personal tab isolation
Parent UI57 actual-asset check: incoming panel hidden in tested My shift route, but eagerly rendered
(37descendants), and common All saved handovers & advanced tools visible on every tab. User's exact
live/install version was not inspected, so don't claim all incoming symptoms were independently reproduced.
UI58 incoming/saved-note content rendered only on their selected tab, removed otherwise; tab-owned hidden
and inert state plus scoped CSS. Common legacy daily/library tools only in By day / subject disclosure.
My shift retains own occurrence/record/direct action/datefallback and creation choices; duplicate header
team/advanced/globalrefresh and duplicate ready-card shortcuts omitted only there because tabs/personal
refresh retain access. Incoming acknowledgement not deleted or moved into own notes. No automatic saves.

No extra timer or forced shift-boundary navigation. Current account/route/read/dialog guards remain;
late personal reply cannot switch tabs. Parent personal clock/occurrence functions unchanged. All notes
remain optional. New explicit workspace error is visible without opening hidden advanced tools.
Five hosted Help bodies/outlines/catalogue updated (permissions, accessreview, departmentheads, handovers,
handovercontinuity);71others unchanged/76entries match. No native/masterPDF redesign.

## Actual checks
**575 selected Python tests, 78 compound browser checks and 81 JavaScript syntax checks passed.** All 194 application Python modules parse; 189 remain unchanged. The frozen runtime contains 1857 tracked files. Python groups: permissions_py=222, handover_history_py=175, hosting_py=178. Browser groups: permissions_browser=9, tabs_browser=9, shifts_browser=19, certificates_browser=15, refresh_browser=26. Selected checks, not full-suite or live acceptance.

Final counted tests use frozen source after the interruption's panel fix. Earlier initial/pre-interruption
runs and fixture failures excluded; complete parent tabs observation separate from passing fix checks.
Source-audit pre-setup span assertion corrected to actual mountEditor span (unchanged); old board wording
is explicitly changed. No unrelated historical failure declared fixed. Exact commands/frozen-source/ZIP
replay in verification. Actual-assetsTestClient/injectedfetch/hash/stagedmemory; not normalnavigation,
durableIDB/SW/livecompany/physical/WindowsPowerShell/native/fullsuite/securityaccessibilityload/Docker/
offhost acceptance. Report renderer unchanged, not newly exercised as report acceptance. No remote actions.

## Preserve / next
Activated Sulmara C01 ID/domain/dedicateddisk/marker INITIALISE_COMPANY=NO removedbootstrap; independent
G01demo users/settings/domain/disk; backups/approvedcommit/.git/outsideedits/unsentmain+separatelogwork.
No reset/reimport/site-data clearing/sync disabling/repeatsetup/incompatible preC01/preUI34 writers.
Older UI57 restores implicit head shift authority; review permissions before any source rollback, never
rollback data to obtain interface. No assumed live UI58. After update grant needed non-admin shift roles
and sign back in with same account. One permission/ownshift/tab/mobile acceptance then section review.
Chrome install confirmed; old desktop shortcut is chrome_proxy/Default/app-ID from prior record, presumed
demo by offline calculation not live inspection. Supplied ICO is appearance-only; focus-existing safe
launch remains pending and no PWA/native icon/launch changes here. Do not close/reload unsent app windows.
Widerroadmap retained in DEVELOPMENT_TODO. Nativevessel/CCVD/cloudsync/localnetwork out of scope; no
background development or implied monitoring.
