# Wavelink checkpoint — UI43 + optional Company C01 + working G01

26 September 2026; core1.34.19. User approved Sulmara as a separate company installation with
normal named login. Code/empty-local-project prepared; no live service/DNS/account/deployment.
Main workflow remains compact changed-file patch → copy/review/commit/push; optional PS1.

## Exact source

Actual uploaded UI30 wavelink.zip SHA25605d6e0966ef03ea7e72feb6641f8ed6f4fd0495ad8b8b50a418c0611dc3b6b0b
plus verified UI31–43 chain. UI43 patch SHA256479b47abecb9d766999c74309f3117b2bb290bd9b670f50ad6f15139710923da.
126 parent repository files/125manifest rows verified; 1776 runtime files unchanged.
Application UI43 extractor remains 56a0ea34f7bd6bb4648b464edf4d6746df6df4b9dc808e163757e33acbe16243.
C01 entrypoint f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2 replaces old entrypoint
 a2bbac57635ac6e0b12400bbcbfc7382416ed3d5c7525e4218b7e38c2e7a633f.
G01 gate unchanged 9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701.
Original demo/signing Nginx unchanged 752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8.
All190appPython/70appJS unchanged. New deployment modules/assets only; Docker/dependencies/vendor/
seed/ordinary writers/QR evidence formats untouched. .gitignore/.dockerignore add secret protections.

## Company semantics

WAVELINK_DEPLOYMENT_MODE defaults DEMO; COMPANY is explicit. New dedicated /var/data disk,
/var/data/wavelink-company project, independent company/hub/install/account IDs. No inherited demo
users/records/files/templates; supported sample-template purged marker only in new empty company.
Fresh explicit initialization required; unknown, partial, symlink, wrong-company or demo storage
refused. Repeated start never resets credentials. Existing demo settings remain untouched.

Private first-sign-in setup key hash + existing salted initial password, 24h window, normal API/
QR/WS locked until password change. New permanent passphrase14–128, six distinct chars; atomic
BEGIN IMMEDIATE password/version/session clear+activation audit. Same-request HMAC retry/outcome
is receipt-only. No password/key literal in source; private user settings delivered separately,
never include them in future memory/evidence/GitHub. Setup key renewal only pending with new key
and free project leases, no SQL/account reset; activated installation refuses renewal.

After activation root serves normal UI43 named login; no outer demo gate/shared guest/join codes.
Every ordinary API needs current company named session; info/login minimal exceptions; isolated
QR endpoints keep their own exact-document grants. Exact HTTPS Host/Origin/proxy boundary; 4KB
setup/login requests; default unknown host421; health works pending. Single-worker unchanged.
No new app database tables/API payload/storage format/permissions/dependencies. New deployment
setup endpoints/marker use existing audit for activation, not a UI44 application release.

Retain initial marker and activation evidence together in backups. No older helper approval,
no pre-C01 company rollback, no disk reset/reimport/site-data clearing. Company mode stays an
inspected/staging candidate internally, not a production-security assertion or new MFA policy.

## Completed selected checks

301Python=71C01+107demo/gateway/package+123hosted.19compoundChromium=14firstsetup+5normalapp.
22real loopback Nginx/company/core checks with simulatedTLSattestation, notHTTPS. 70 unchangedapp
JS+1newsetupJSsyntax;190unchangedappPython+newdeploy/testparse. Local requested initial account
verified with empty operationaltables; localDBnotshipped. Source manifest/replay finalreport.

Browser controlledfetch/storage/history/fragment/hash,set_content; mainapp real TestClient API.
Initial incorrect fixturetable names, absent defaultbrowser executable and superseded69-passrun
excluded/retained. Final usedinstalled/usr/bin/chromium, no navigationpolicybypass/download.
No fullsuite/liveGitHubRenderDNSHTTPS/realphones/durableIDB/SW/WindowsPowerShell/native/Docker/
fullsecurityaccessibilityload/offhostacceptance. Nothing remotely written/provisioned/deployed.

## Preserve / next

Existing demo G01/publicentryYES/fictionalinitNO/guest/domain/disk/backups/unsentwork unchanged.
New Sulmara company: dedicated service/disk, companymode, exactPUBLIC_URL; private firstsetup,
thenINITIALISE_COMPANY=NO/removebootstrapsecrets; never copydemocredentials or seed. Never infer
liveaccount/version from this package. Render/GitHub available-notconnected; cards suggested.

Verify real company firstsign-in/normalaccount/permissions/files/QR/restart/backup independently;
UI43 user-mobile/day/combinedPDF feedback remains first operational UX priority. Samepolished
fullcapabilities/simpledefaults/groupedupdates direction. Wider roadmap preserved inDEVELOPMENT_TODO.
Nativevessel/CCVD/cloudsync/localnetwork remain outofscope. No automatic background development.
