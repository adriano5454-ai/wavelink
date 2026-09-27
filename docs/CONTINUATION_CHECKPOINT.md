# Wavelink checkpoint — UI46 + Company C01 + working G01

27 September 2026. Core **1.34.19**. User approved the UI45 Home review and requested section-by-section
reviews afterwards. Easier means polished, discoverable and fully capable, not basic or hidden features.

## Source verified
Exact UI45+C01 reconstructed from the actual uploaded UI30 repository and verified UI31–43/C01/UI44/UI45
patch lineage. 142 parent repository files and1789 parent runtime files verified.
Parent extractor 368ec073eb0a310a27734594a63deff62a916fc3a4a9cb8169a746856558a25f.
UI46 extractor 4840018d682133736b820bc61ad185e66bb74e16406aabdf913820f6e3024243.
Patch ID workspace-ui46-work-focused-home-2026-09-27.
93 incremental resources / 469 cumulative overlays / 1795 tracked runtime files.
C01 entrypoint f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2;
G01 gate 9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701;
signing Nginx 752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8 remain unchanged.
Only existing executable repository change: deploy/extract_source.py.

## Implemented
Work-first Home, compact header without internal badge, four initial personal rows / expandable additional
previews; full category counts, five previews per category. Exact daily-draft editor route, exact pending
published revision, explicitly assigned open Tasks (not all admin-accessible Tasks), own-created unfinished
standalone checklists, existing assigned log-issue inbox. No inferred checklist authorship from a shared name,
no all-participants checklist claim, no completion/attendance/priority score. Postponed assignments separate.
Existing record-open participation/read/alert semantics preserved; Home does not sign, submit or complete work.

Separate project Tasks/maintenance/certificates/admin receiving summaries. Full17 permissioned destinations,
compact grid, complete card choices and existing creation forms. Handovers/Tasks/Inventory/Manifests near
front, then Logs/Checklists; five filters/static activity search retained. No private-record search.
Empty available builder catalogue plus no personal preview entries gives contextual Create/Import. This is
permission-scoped, not proof the entire company database is empty. Existing real builder/importer opened;
non-admin builder authority retained. A saved available definition removes the empty-catalogue prompt.

New read-only home_work.py and additive metadata on existing /api/attention. attention.py is the only
changed existing Python module;191 unchanged,193 total. No new routes/tables/dependencies/permissions/stores.
Shared app.js function declarations/writers unchanged. Handovers load/handles read routing and builders open
routing changed; other controller declarations unchanged. Existing UI45 sign-out and owner-retained local
work, handover files/QR/day journal/PDF, inventory verification, Original Files, presence and branding intact.
Home guards current route/account/token/root/modal/read-generation. A delayed obsolete hash event no longer
invalidates the current Home's shortcuts; entry still makes a fresh read. Failures clear old private results,
explicit retry; separate reads are not an atomic or live snapshot. No new local persistence or autosave.

Home and Navigation Help bodies updated;74 other bodies unchanged;76 catalogue texts/headings match.
Native Home and master guides are not rebuilt. Shared cache URLs update outside article bodies.

## Completed local tests
481 selected Python = 44 Home/assets/existing attention + 186 authoring/local-work +
73 simple/daily-journal handovers + 71 C01 + 107 demo/gateway/package.
56 compound browser =15 Home +19 retained operational shortcuts +9 builders +13 sign-out.
72 JS syntax /193 Python parses. All final selections repeated after the final test-only catalogue correction;
application bytes did not change in that correction. Final ZIP replay and hashes recorded separately.

Preliminary missing fixture metadata/method/start-revision errors, normal-navigation restriction, old catalogue
role assertion and source-audit tooling assumptions retained/excluded. Real delayed hash-event issue fixed;
regression retained. No unrelated historical failures declared fixed. No full-suite claim.
Browser uses actual assets + fictional TestClient + simulated hashes + staged in-memory state. Actual normal
navigation is policy-blocked and not bypassed. No live GitHub/Render/company-data/credentials, real phone,
durable IndexedDB/SW, Windows/PowerShell/native, full security/accessibility/load, Docker or accepted off-host
recovery. Existing handover PDF route tested locally; no report-rendering source changed.

## Preserve / next
Keep separate demo G01 and Sulmara C01, existing domains/settings/IDs/users/permissions/disks/activation marker,
backups/approved commit/.git/outside edits/unsent browser and separate-log work. After company activation retain
INITIALISE_COMPANY=NO and bootstrap-secret removal; never repeat setup or copy demo data/credentials into company.
No reset, re-import, browser-storage clear or incompatible pre-C01/pre-UI34 writer/exporter rollback.
UI45 source rollback preserves the old Home but cannot recover deliberately discarded local entries.

Use compact GitHub copy/review/commit/push; PS1 optional, evidence separate. Do not assume a live UI46 deployment.
Next: one real named-user Home/continuation/empty-builder/mobile check. Then review one section at a time:
current desktop/mobile workflow -> agreed improvement plan -> coherent implementation -> short acceptance.
Keep useful choices/wizards and automatic audit; avoid generic routine reasons or hiding capabilities.
No next section is silently redesigned here. Wider roadmap retained in DEVELOPMENT_TODO, including remaining
routine-prompt cleanup, richer approved imports/evidence, maintenance/signing extensions and recovery/security.
Native vessel/CCVD/cloud synchronization/local phone-network work remain outside this increment.
No automatic background development.
