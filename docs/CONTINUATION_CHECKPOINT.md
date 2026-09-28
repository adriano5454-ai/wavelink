# Wavelink checkpoint — UI55 + Company C01 + working G01

28 September 2026; core1.34.19. User reports persistent app-wide flicker after UI54.
Stability takes priority over the next Certificates review. Polished/full capabilities,
no routine friction, same compact copy/review/commit/push delivery; PS1 optional.

## Verified source
Full UI50 archive a9e3452da15435653281425696449aefe1afadb88a1630ac949f4b2a08f1e8d2 + exact
UI51–54 patches, every baseline/target hash and ZIP CRC checked. 160 parent repository files,
1844 runtime files. Parent extractor d38981772e96b7c4f4b10bd7cd1ae8dfab06b9acbb1a21569dc82c4081a930da.
UI55 extractor a3204bb604d0ea9fd62157738ae28cbab030b59fea2cdc85145be9f57678a0a2.
PatchID workspace-ui55-shared-refresh-stability-2026-09-28.
90 changed/new runtime resources; 528 cumulative overlays; 1846 runtime files.
C01 entrypoint f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2;
G01 gate9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701;
Nginx752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8 unchanged.
Only existing executable repository change deploy/extract_source.py. Target162repo/161deployment rows.

## Findings and implemented correction
UI54 shared persist showed full-width Saving local workspace during eight-second cached catalogue/
record/heartbeat writes, not only user edits. Actual-asset delayed-write180ms mobile reproduction:
Home/builders two appearances over two idle rounds, scroll500–620; native anchoring partly compensated.
Exact Fault route additionally remounted; do not claim all live symptoms or hidden tab/version verified.

persist({background:true}) only at loadRecords/refreshRecord/heartbeat. SAME writeWorkspace(true),
transaction/storage-error path, lease checks and overall localWriting counter. Separate foreground
localFeedbackWriting drives transient banner only. Real drafts/queues/uncertain/conflict/error/offline
feedback retained. Background writes still block unsafe logout/discard; no skipped persistence.
Idempotent connection/project/presence text and save-strip attr assignments when unchanged.
One shared eight-second timer round at a time, finally resets; active writes finish, sync remains on.

Fault/HSE direct-route refresh: no full-shell/loading navigation on every render. Exact read context,
current report/list authority, stable keyed rows and saved-data fingerprints. Other selection retained
while old URL remains. Reading History not automatically rewritten; current read access still checked.
Changed account/route/form/modal/selection/generation invalidates delayed success. Definitive denial
clears protected report rows behind shared modal without deleting its text. Transient last-saved label,
existing edit fresh-read/version rules retained; not a blanket disabling of all old form actions.
Report submit/create/review/assignment/lifecycle functions and server payloads unchanged.

All193applicationPython unchanged;79JS syntax. Shared main function audit: only persist/updateConnection/
loadRecords/refreshRecord/heartbeat declarations changed,143others byte-identical. Timer callback changed
outside declarations. writeWorkspace/apiTransport/queueChange/syncQueue/commitLocalSignOut/sessionExitBusy/
render/safeRender/renewLease unchanged. Fault/HSE only open/detail changed,3read helpers each added;
writers and form logic unchanged. view_stability adds report row keys only. Approved designs retained.
No new APIs/tables/permissions/dependencies/environment/saved formats/browser-store versions.
One Help body savestatus+outline/catalogue;75others unchanged;76 matches. No native or PDF redesign.

## Actual checks
**342 selected Python tests, 93 compound browser checks and 79 JavaScript syntax checks passed.** All 193 application Python modules remain byte-identical to UI54. The frozen extractor produces 1846 tracked runtime files. Python groups: refresh_py=93, reports_py=36, checklist_py=35, hosting_py=178. Browser groups: refresh_browser=26, signout_browser=13, checklists_browser=10, reports_browser=26, maintenance_browser=18. Two intentionally excluded historical assertions were reproduced failing on untouched UI54. No full-suite claim.
Frame-sampled delayed cache writes, actual report writes/access revocation and concurrent original timers
for33.5s; seven workspace idle entries, report history/selection/modal/network states; actual user-save
feedback, overlapping user/cache writes, held transaction/no timer overlap, quota failure and retained
unknown fields/uncertain receipts. Separate retained signout/checklist/paired-report/maintenance browsers.
Same shipped assets and real fictional SQLite/TestClient services, injected fetch/hash/staged atomic store;
not durable IndexedDB, real navigation, WebSocket, SW lifecycle or physical-device acceptance.
Initial interrupted run and superseded short development run excluded. Two old save-status version/hash
assertions reproduced failing untouchedUI54 and deselected from current selection, not removed/fixed.
No fullsuite/livecompany/credentials/hosting/WindowsPowerShell/native/Docker/fullsecurityaccessibilityload/
offhost acceptance. Source/CRC/checksum/replay/fresh runtime verification separate, repeats add no coverage.

## Preserve / next
Separate activated Sulmara C01 identity/domain/disk/marker, INITIALISE_COMPANY=NO and removed bootstrap;
independent demo G01settings/domain/disk/guest; backups/approvedcommit/.git/outsideedits/unsentmain+logs.
No reset/reimport/site-data clearing/sync disabling/repeatsetup/incompatiblepreC01/preUI34writers.
Test same-account idle Home/builders/report+real-update on the actual deployed build; do not assume UI55live.
Prior section-specific fixes alone did not cover slow global cached writes. Remaining symptoms need the
actual tab, top status, deployed build and preferably a short recording; don't claim universal flicker cure.
Then resume Certificates review→agreed build, keeping approved sections. Wider roadmap retained.
Nativevessel/CCVD/cloudsync/localnetwork remain outside scope. No automatic background work.
