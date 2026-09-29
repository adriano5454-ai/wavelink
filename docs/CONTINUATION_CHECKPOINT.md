# Continuation checkpoint — UI65 role-ready invitations and controlled access

**Prepared 29 September 2026 · core 1.34.19 · exact parent UI64 + Mail Startup M01 + Company C01 + G01.**

UI65 is now an actual cumulative source release, not the earlier design-only review. It implements versioned
company job-role profiles, exact invitation access snapshots, verified pre-authorised activation, preserved
legacy/proposal-only Pending outcomes and bounded department task-management scopes. Department, displayed
job role and actual security/access are distinct. Nine initial profiles are seeded; participant profiles use
an explicit 28-capability allowlist. Existing accounts and UI64 invitations are not mass-rewritten.

Membership storage upgrades transactionally from schema version 1 to 2 by adding role presets/revisions,
invitation proposal snapshots, member-role assignments and management scopes. Preserve the full company
backup and keep UI65-or-later software after migration. Do not reset/re-import, clear browser storage,
recreate C01 or run UI64 against upgraded membership data.

The cumulative extractor was rebuilt from the verified UI64 extractor and fresh extraction matches the
prepared UI65 runtime exactly outside generated manifests: 1,922 tracked runtime files, 632 overlay records.
The M01 launcher remains byte-identical at
`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`.
Nothing was pushed, deployed, emailed or inspected on live Render/SMTP/DNS/company data.

Local release checks completed: 57 selected Python cases passed with one environment-dependent skip; all 58
original UI64 membership cases passed in isolated groups; nine real shipped-asset browser scenarios passed at
1440/390/320 pixels. Package/repository checks are recorded in DELIVERY_CHECKS.json. These are local fictional
checks, not full-suite, independent security, live SMTP, production load or accepted off-host recovery.

**Next coherent batch:** profiles, privacy-aware Team updates, reversible likes, duplicate-safe contribution
points, 1/3/5 reward controls, tier progression and original selectable badge designs. Preserve UI65 authority
and migration boundaries. Email-first operational sign-in/domain routing remains separate.

--- Retained prior checkpoint history ---

# Current checkpoint — UI64 + Mail Startup M01 + C01 + G01

29 September 2026. Focused repair after the user supplied correct Render INVITE_ONLY/Zoho
settings but invitations still reported unconfigured. Existing username admin is a valid
invitation manager; retain legacy stable IDs/login until the approved email-first replacement.

Actual root cause: deploy/company_entrypoint.py launched company_runtime with only the generic
minimal_environment plus PYTHONPATH. MembershipSettings.from_environment in the CHILD consequently
saw default OFF and no company/SMTP values. UI64 factory tests injected membership settings and
missed this supervisor-to-child boundary. New tests explicitly exercise it using fresh processes.

Only existing executable changed: deploy/company_entrypoint.py. New helper
company_application_environment copies the exact company identity/membership/SMTP allowlist after
prepare_company validates its captured operator environment; PUBLIC_URL is the validated cfg origin.
No arbitrary inheritance, bootstrap secrets, demo-password leakage, Nginx mail credentials or logging.
OFF/invalid/incomplete configurations remain disabled; mail credentials forwarded only for INVITE_ONLY.
Generic deploy/entrypoint.py, deploy/company_runtime.py and extractor are EXACT UI64 bytes.
Application runtime remains 1917 tracked files / 203 app Python / 89 JS; no UI65 application claimed.
No added tables, migration, permissions, routes or browser stores. UI64 schema compatibility remains.

User selected contact@mywavelink.com, confirmed separate mailbox. Supplied Zoho screenshot gives
smtp.zoho.com, 465/SSL or 587/STARTTLS; selected 465/SSL. Actual SMTP secret stays in Render only.
No live settings, SMTP/password validation, email delivery, domain proof, account change or deployment.
The user-supplied sulmara.com remains unverified for future Stage C; sender domain is not domain proof.

Apply compact payload over UI64, copy/review/commit/push. Preserve independent company_entrypoint edits,
company identities/artwork/.git/backup/unsent main+log work, C01 activation metadata and removedbootstrap,
independent demo data/settings/disk. No reinstall, browser clearing, service/disk recreation, syncdisable
or repeated setup. Stay UI64+ on membership data. Future full builds must carry this M01 launcher change.
Next: actual clean deployment -> existing admin Invitations & access Refresh -> one disposable invitation,
mailbox code and pending/no-rights acceptance; then continued bounded-delegation and Stage C sign-in work.
Chrome focus-existing remains pending. Do not promise background work.

Read docs/MAIL_STARTUP_M01.md, docs/MAIL_STARTUP_M01_PROVENANCE.json and DELIVERY_CHECKS.json for the
actual patch/test boundaries. Earlier UI64 release details retained below; their test counts are historical.

--- Retained UI64 checkpoint ---

# Wavelink checkpoint — UI64 + Company C01 + G01

29 September 2026; core1.34.19. Implements Stage B after UI63 personal Home. User supplied sulmara.com is unverified, not an auth/routing rule. No current domain research, real email, company data or deployment. Keep polish/full capabilities and shared UI60 controls; normal User ID login retained.

## Exact source

Parent181 repository /1897 runtime files verified from actual fullUI50 + UI51–63. Parent extractor a544a88123072907bf718f56cde2abf7dd70ecb1a19f4e6020d2a7f1acfe3d82.
UI64 extractor 815a635818cb4268957c090e091dab50a95c72b1b6e0bc9f103276fdc630ae09; patchID workspace-ui64-membership-access-2026-09-29.
122 incremental resources /626 cumulative overlays /1917 tracked runtime;203 appPython/89JS. Existing executable upload changes: deploy/extract_source.py AND deploy/company_runtime.py (cff4d9ecafdd048377f46000f2d706745efef164f27a22e9301bb1d5ceb68a27). New blank deploy/membership.env.example. C01entrypoint/G01gate/signingNginx/companyidentityJSON unchanged. Preserve operator company logos/config.

## Membership/authority implementation

Eleven company_* tables + users.membership_required marker, atomic version1 creation, exact schema/constraints checks, refuse partial/unknown state. Existing users marker0 and old policies preserved; new verified invitees marker1 disabled, explicitallfalse and no departments. Membership state/policy enforced before normal login and Store sessions; enabled/cached flags cannot bypass Pending. Approvedzero remains status-only.

Opt-in COMPANY-only TLS SMTP (INVITE_ONLY vs defaultOFF); stdlib STARTTLS/SSL certificate verification, no plaintext. Operator env outside source. Submitted/unconfirmed, not inbox claim; no background mail queue. Exact recipient link7days + separate mailboxcode8digits/10min/5tries/rates; GET/link scanner noaccept. Hash-only proofs/status sessions, HMAC op receipts, same-request idempotency. Status8h onlyown name/email/UserID/state/company, memoryonly, neveropcredential. Acceptedbutstatusloginfailure explicitlysaved andrecoverable. Normal UserID/password required after rights; verifiedemail/statuslogin is not StageC email app login.

members.invite/review/manage flags defaultOFF; admin envelope active departments and independentlyheld allowed keys. Effective=currentbase ∩ explicitallowance ∩ active target scope/prerequisites. No onward/nondelegablebackup/all-deptshift/self/admin/othercoordinatorescalation. Preserve independentpolicy and eachdonor grants. Donorauthority/envelope/department/rolescope change stopsdependents; noautomaticrevival. Recipientdepartment/Fleet scope invalidates receivedgrants. Passwordonly sessionrevoke preservesparentgrants. Current normal session/actor/target/version checks insidewritesandreceiptretries. OldmanualCreateuser role semantics remain separate; no implicit pending of existingstaff.

AdminpersistentInvitations&access, nonadmin ownworkspace, HomeNeedsmyaction scopedrequests. Explicitapproval/no defaults; multiplepermissiongroups carrydependencies; accessdecisionnote retained. Formsintab/dirtywarn,busysignout/Close, originalbeforeSend/latecallbacks. Keyedrows/tempstaleactionsdisabled/denialbehindmodal. UI63personalHome, UI55quietcache, source/evidence/privateconstraints and PWA/QR files retained. Main critical writeWorkspace/apiTransport/queueChange/syncQueue/commitLocalSignOut/renewLease/persist/loadRecords/refreshRecord/heartbeat declaration spans exactlyparent.

Seven public entrymethodroutes +five managerAPIroutes and /join-team. C01 onlyexactpublicmethodallowlist afterinitialactivation, strictorigin/body/CSP/no-store/networkonly/nooffline-mainfallback. Existing setup/gatewayunchanged. Minimalanonymousinfo onceemailenabledoranymanageduser; validnormalusersretainprivatecurrentinfo. PersonalHome pendingqueue readonly.

BackupCOPY purgeschallenges/status/rateproofs/closesissuedinvites; preservesemails/policies/grants/audit. Newproject full/selectedimport suspends enrolledusers anddeactivates grants/envelopes, stableIDs remain; importedoldadminloginworks. Do not represent a projecttransfer as current verifiedauthority. Enrolled IDs cannot purge asunused; neverusedlegacy accounts stillcan. KEEP UI64+ onnew schema, no oldwriter downgrade/reset; fullcompanybackupmustretainC01metadata.

## Tests and limits

417 finalselectedPython /59 compoundbrowser /89JSsyntax /203Pythonparse. Python groups: membership_core=59, mail_boundaries=24, upgrade_transfer=6, hosted_membership=5, contract=6, admin_retained=63, scope_retained=37, personal_retained=39, company_retained=71, gateway_retained=107. Browser20membership+26sharedrefresh+13signout. ActualUI63upgrade, backupcopy, full/selectednewprojectimport, simultaneousaccept/review, expired/forwarded/wrongcompany/codes, grantcascade/independentscope checks. SMTPstubonly. ActualC01factorysimulatedTLS, not liveproxy/SMTP. All counted commands exit0/XMLnofails/noskips. Firstfinalhostedrunmissingenv corrected byexactfrozengroupretry; no source/testbyteschanged. Previouscountsnotinherited.

Earlier failures/superseded runs retained in evidence: collectioninit, SQLquoting, receiptbranchregressionfixed, fixturewrongFleetservice/Path/auditseq, mobilelocator/evaluatefunction/asyncsettle, contractpredicatefilename. No unrelatedhistoricalfailure claimedfixed. Oldreleasecacheinvariants notused ascurrent passes; UI64 fullasset/entry/storage/Helpcontract passed. All77Helpentriesmatch;7existingbodieschanged+1new,69unchanged; no manualPDF rewrite.

11 existing appPython changed,4new,188existingunchanged. No report/QR/signaturewriter changes;21existingPDFs unchanged. Browser actualassets/fictionalSQLiteTestClient/injectedfetch/hash/stagedstore andtestcryptoUUID; no realnavigation/WebSocket/durableIDB/SW/physical/WindowsPowerShell/Chromeinstall/fullsuite/securityaccessibilityload/offhost/emaildelivery acceptance. FinalZIP replay/hash/fresh extraction separatelyverified. Nothingdeployed.

## Preserve/next

C01companyIDs/PUBLIC_URL/disk/activationmarker INITIALISE_COMPANY=NO removedbootstrap; independentG01democonfig/disks;backup/approvedcommit/.git/independentcode/logos/unsentmain+logs. No reset/reimport/site-dataclear/syncdisable/repeatedsetup. Copyentirepayloadincludingcompany_runtime, optionalPS1. No source rollbackbelowUI64 onmembershipdata.

Next operatorSMTPsenderconfiguration andrealdisposableinvite/status/zerogrant/limitedgrant/delegation/revocation/restart/restore session. StageC verifieddomain/main-siteprofessionalemailentry stillpending; sulmara.com remainsunverified. No automaticaccountlinking/domainSSO/MFA/emailrecovery, no grants from typingemail. Chromefocus-existing and widersectionroadmap remain. No automaticbackgroundwork.

## M01 completed checks

135 selected pytest cases passed with exit 0 and complete XML: 26 new process/configuration
checks, 71 retained C01 checks, 29 retained membership mail/hosted checks and 9 package checks.
89 unchanged runtime JavaScript files pass syntax and 203 unchanged app Python modules parse.
All 1917 runtime hashes still match UI64. The initial interrupted company run is excluded;
its complete retry is counted once. No browser, live email or production deployment acceptance.
