# Wavelink checkpoint — UI42 + working G01

26 September 2026. Core1.34.19. Simpler means user-friendly, polished and discoverable, not basic,
removed capability or hidden primary actions. Group whole related workflows; compact GitHub patch,
copy/review/commit/push; optional PS1. Do not assume the live deployment matches UI41 or UI42.

## Exact source

UI41 over actual uploaded UI30 wavelink.zip plus verified UI31–41 patches. 122 parent
repository files/1766 runtime hashes verified. Parent extractor:
af52a5481f2d971c8a4d9bd854eb59ce28c1ab062eb9a9054361957ecb170145
UI42 extractor: 73d911265cceb301c291608ce653763e19dfbdfddcb1d8593a5f11d26f0bcda0
Patch ID: workspace-ui42-home-workspace-discovery-2026-09-26
Upstream: 8c1b6a8d731d01b05a1290d3a1dd1a544054147aac9048ca345af7983613cd9e
G01 gate: 9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701
G01 entrypoint: a2bbac57635ac6e0b12400bbcbfc7382416ed3d5c7525e4218b7e38c2e7a633f
Signing Nginx: 752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8
92 incremental resources/431 overlays/
1770 runtime. All188appPython unchanged, only existing executable repository
change deploy/extract_source.py. No new APIs/tables/permissions/dependencies/environment/formats.

## Implemented

16 static permission-gated Home destinations in5groups, distinct Open/Create actions. All visible
initially; query/group filters, zero state/reset, keyboard focus only. Available destination count
not workload. Shared sidebar vocabulary matches static terms, never private records. Admin Fleet
scope unchanged. Existing UI41 Task cards/stock verification/Create handover/Help/local manager
retained. Home shortcuts to existing certificate, toolbox, maintenance, checklist and stock forms;
original file modal same route. Actual saves checked for stock/certificate/toolbox with fictional
API. No record creation on browse, automatic signing or data movement.

Same-session redraw retains filters, leaving Home or changed auth resets. Home lookup closure
checks root/generation/account/token/route and intervening dialog child, including a form closed
before response. No writer code changes. All138 existing app.js function declarations unchanged;
only home adapter expanded. Operational controllers/forms/local manager/signing assets intact.
Existing attention endpoint/category scopes/local-work warnings above cards unchanged.

Home and Navigation Help rewritten to actual current controls;74otherbodies unchanged,76catalogue
entries match; original saved-overview scope table retained. Cache references updated to a fixed
point, new catalogue script present before nav and in SW. No native/masterPDF redesign.

## Tests

881Python=790app+91gateway;218compoundChromium;11actual loopback;
69JSsyntax/188Pythonparse.14newPython and19newbrowser
inside those totals; Node assertions overlap one Pythoncase. Final logs only; partial/fixture/error
runs retained excluded. Certificate/Task browser harnesses pause unrelated polling during fake
token/route changes; complete corrected runs passed. All application files stayed byte-identical
during the fixture-only refreeze. Exact cause of every earlier timeout is unestablished.
Two inherited old save-status version/hash assertions remain excluded,
not claimed fixed; other journal cases retained. Final ZIP replay hashes separately recorded.

Initial UI42 Home hash-event invalidation corrected; not claimed live/UI41 regression. Browser
normal navigation policy-blocked; tests assert links then dispatch hash through actual router.
No policy bypass. Actual assets/fictionalSQLiteTestClient/injectedfetch+memory/set_content.
No fullsuite/liveHTTPS/physical/durableIDB/SW/WindowsPowerShell/fullsecurityaccessibilityload/
Docker/offhost acceptance. No real data/credentials/remote operations/deployment.

## Preserve and next

Keep G01,DEMO_PUBLIC_ENTRY=YES,INITIALISE_FICTIONAL_DEMO=NO,gate secret/matchingnonadminguest,
namedadmin/domain/disk/removedbootstrap/backup/approvedcommit/.git/outsideedits/unsentwork.
No reset/reimport/storageclear/incompatiblepreUI34writers. UI41 source rollback does not recover
local entries deliberately discarded. Native installed program not rebuilt.

Next one fictional named-user Home/task/stock/handover/Help/phone acceptance session, then grouped
module usability with visible choices. Wider roadmap retained below in DEVELOPMENT_TODO. No more
hiding capability to simplify. Nativevessel/CCVD/cloudsync/localphone investigation out of scope.
No background development or assumption of live UI42.
