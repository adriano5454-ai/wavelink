# Wavelink checkpoint — UI63 + Company C01 + G01

29 September 2026; core1.34.19. User approves Personal Home/Workspaces first, then controlled membership and
professional email/domain sign-in. User supplied sulmara.com; recorded unverified, not enabled for routing.
Polished/full capabilities, shared components, compact changed-file delivery, optional PowerShell, separate evidence.

## Exact source

Full UI50 and verified UI51–62 patches;178 parent repository/1889 runtime hashes and every ZIP CRC checked.
Parent UI62 extractor71274333207a3eea26842272ecc42ee33e53edd1ece00cf83c2b226dd45f214b.
UI63 extractor a544a88123072907bf718f56cde2abf7dd70ecb1a19f4e6020d2a7f1acfe3d82.
PatchID workspace-ui63-personal-home-workspaces-2026-09-29.
97 changed/new runtime resources;603 cumulative overlays;1897 tracked runtime files.
Target181 repository/180 deployment-manifest rows. Only existing executable repo change deploy/extract_source.py.
No deployment identity/config/image change. C01entrypoint
f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2;G01gate
9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701;Nginx
752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8 unchanged.

## Implemented stage A

Home personal name/company, exact existing own-shift projection/direct editor, four views: My work, Needs my
action, Saved handovers, My activity. No module catalogue/team totals or empty-company onboarding on Home.
Workspaces separate route+sidebar afterHome: all17 permissioned cards, activity search, category filters,
existing creation/import/verification and full Task chooser preserved. No new role/default grant.

New readonly personal_home summary: exact named Tasks/Maintenance; shared checklists created/contributed via
reliable actor IDs; assigned log Issues, owner Fault/HSE; explicit pending handover/Toolbox acknowledgements;
configured checklist/Maintenance reviews and actual responsible-head Task reviews, not admin-all. All work
pages/date/state meanings explicit; per-source unavailable fails visibly; limits and totals not all-clear.
Saved handover private notes separate from device-local forms/queues. No text content exposed from audits.

Activity reads existing fieldwork/checklist/handover/log audits through allowlisted types/actions, immutable
account IDs, current module/source/private access. No name-matched guests, visits/heartbeats/cache activities.
Ten supported operational source categories; not all historical/native/builder/Fleet/security events. Default
30days, All dates/type filter,20/page; context-bound keyset cursor,5000candidate scan/explicit continuation,
no fabricated full-total claim. Older unsupported actors omitted. Handover publication/ack links pin exact
revision; ordinary names/status use permitted current source. Original histories unchanged, no new audit table.

Two auth/no-store GET routes /api/home/personal and /api/home/activity in operations_api.py; new personal_home.py.
Only one existing Python module changed,197 unchanged,199 total. No schema/tables/dependencies/env/permissions.
Snapshot read then current identity/policy recheck; vessel-only denied. Normal project+site mode keeps current
project access. Existing data/current users/memberships/identity/auth boundaries untouched.

New personal_home.js/css; scoped app Home/render/nav, oldhome directory->Workspaces, nav_shell/index/catalogue,
interface-topic registry and handover #handovers/mine routing. Keyedrows, current account/token/hub/view/query/
root/dialog/closed-dialog generations, immediate denial even behind modal or slower sibling read. Transient
last-saved view pauses stale opening; current editor retained. No new interval; existing idle renders refresh
at most about29s; no shift-boundary forced navigation. All local queues/leases/save/signout/discard bodies
unchanged. Declaration-span audit includes new Home constants after discardLocalBatch; actual function body
is identical. UI55 cache, UI58 Myshift, UI59 signatures, UI60 components, UI61 Original Files, UI62 Admin/Fleet
and branding preserved.21PDFs/32icons/PWAidentity exactparent; no native/browserlaunch/report redesign.

Five Help bodies/outlines dashboard/navigation/users/departments/browseradmin updated;71otherbodies same;
all76 catalogue entries match. Shared external cache URLs advance. New runtime/repo
 docs/PERSONAL_HOME_ACCESS_ROADMAP.md stores stagesB/C and unverified intended domain. No mail/authconfig.

## Actual checks

**368 selected Python tests, 53 compound browser checks and 87 JavaScript syntax checks passed.** All 199 application Python modules parse; 197 existing modules are byte-identical to UI62. The frozen runtime has 1897 tracked files. Python groups: personal_py=22, sources_py=16, restricted_py=1, contract_py=7, shifts_py=66, retained_py=78, hosting_py=169, package_py=9. Browser groups: personal_browser=13, refresh_browser=26, signout_browser=13, changed_browser=1. The separately run restricted-account test is counted once; its earlier deselection from sources_py avoids duplicate coverage. Nine package tests are counted separately from the 169 other hosting tests. Preview renderings and repeated archive checks are not extra behaviour-test cases.

Earlier combined development runs did not reliably finish within their bounded run, including one with completed-looking output but no accepted clean process outcome. They are not counted. The final selected source tests were split into bounded groups, each with exit status 0 and complete test XML. The exact cause of every earlier process stall has not been established. Initial fixtures used a nonexistent permissions column, had SQL quoting mistakes and assumed an unadorned h1; those fixtures were corrected. A browser assertion confused CSS uppercase presentation with text content. Development also corrected a real Toolbox title projection, preserved the unaugmented checklist-definition hash for review checks, and used the existing in_progress shift-record state for direct draft continuation. Current regression tests cover those cases. The current UI63 cache/storage contract verifies all main scripts and styles; older release-specific cache-name tests are not claimed as current passes. No unrelated historical failure or native execution is declared fixed. All final counted selections used the same frozen application bytes; the last additional real-update browser scenario changed no application or shipped test files.

Final statuses/XML/browser results/sourceaudit/replay are authoritative; don't inherit older release counts.
Shipped assets and temporary fictional SQLite/TestClient projects, controlled fetch/hash and staged memory.
No live Sulmara/credentials/GitHub/Render/realTLS/WebSocket/navigation/durableIDB/SW/physical/Chromeinstall/
WindowsPowerShell/native/fullsuite/fullsecurityaccessibilityload/Docker/offhost/emaildelivery acceptance.
No new PDF rendering check; existing reports exact bytes. No real permission/domain/account changes.

## Preserve and next

Keep independent activated C01 company IDs/domain/disk/marker INITIALISE_COMPANY=NO removedbootstrap;
G01demo config/domain/disk/guest; backups/approvedcommit/.git/independentcompanyidentitylogos/unsentmain+logs.
No reset/reimport/storageclear/syncdisable/repeatsetup/incompatiblepreC01/preUI34writer or database rollback.
Current named login unchanged. UI62 source rollback returns old Home, cannot recover deliberately discardedwork.

User-supplied company email domain sulmara.com is unverified planning metadata. StageB next: verified mailbox
invitations and truly pending/no-operational-access membership, requests and capped delegation. Missing-policy
role defaults are not safe pending accounts. Grantable=currenteffective ∩ explicitdelegateallowance ∩ scope,
all dependencies; no self/strongeradmin/onward escalation, preserve unrelated/admin-origin grants. Keep stable
localuser IDs/audit; QRtemporaryvisitor is never automatic member. Requires its own reviewed backend/data work.
StageC: professional main-site email-first entry, verified exactdomain/allowlistedcompanyroutes and chosen
trusted tenant handoff; no naked address authentication, parent-domain shared operationalcookies or user-chosen
redirect. Real transactional email/domain/HTTPS acceptance needed; nothing enabled/sent in this release.
One practical personal-assignment/contribution/history/revocation/Workspaces/phone check first. Chrome safe
focus-existing window and broader roadmap remain separate. No automatic background work or live-version claim.
