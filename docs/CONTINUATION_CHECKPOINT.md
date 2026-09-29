# Wavelink checkpoint — UI62 + Company C01 + G01

29 September2026; core1.34.19. Implements approved UI61 Fleet/Manifests/Receiving and persistent
Administration navigation. Interruptions: invisible retained Company Branding form, small logo save413,
per-company operator header identity separate from database report branding. User-friendly/fullcapabilities,
sharedUI60 controls, compact copy/review/commit/push/optionalPS1/evidenceseparate. No assumedliveUI62.

## Source
FullUI50+verifiedUI51–61:174parentrepo/1875runtime. Parent extractor
727ffd799a9b28c4be971ed84938dc2e9f3b8f70fe8ce12c11645b63e770c3c2.
UI62 extractor 71274333207a3eea26842272ecc42ee33e53edd1ece00cf83c2b226dd45f214b.
PatchIDworkspace-ui62-administration-logistics-branding-2026-09-29.
116changed/newruntime, 594overlays, 1889trackedruntime.
Target178repo/177deploymentrows; existing executable uploadchangeonlydeploy/extract_source.py.
Newdeploy/company_identities.json andcompany_logos/README.md. C01entrypoint
f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2;G01gate
9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701;Nginx
752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8 unchanged.

## Implemented
Persistent permission-aware8sectionAdministration registry outsidechildroot, same choices on7subsections,
newlogbook and#admin/fleet. Permissionednonadminbuilder entriesonly. Oldlocalsiblingmenus removed;
existing dirty/busyguardsandsharedcomponents retained. EmbeddedFleet stayswithinparent Administration
route; normal operationalFleet remainsavailable. No addedpoll/MutationObserver.

Fleet explicitproject_logistics modeinexistingscopetable pluscurrentsiteroles; publicfleet_mode remains
project_user forordinaryAPIcompatibility, additivefleet_access bool. Strayoldgrantsnotauthority; oldaccounts
notrewritten; vessel_only staysrestricted. Existingadminset_access/reason/confirmation/revocations used.
Viewer/operator/manageractionsunchanged, sitecreate/initialallocation/accessadminonly, vesselLogs separate.
Nativechooser sourceonlyupdated/noWindowsrebuild. Accessreviewandscopebackup retained.

Fleetcaptureaccount/route/page/dialog/readgenerations; delayedallocation/asset/history cannotreplace
newerform/route. Finalfetchercheckbeforeexistingjournaltransport,no sharedwriterreplacement. Denialclears
protectedbackground/formsretaintext; transientlastsavedviewdisabledstaleactions. Standalonesignout real
JSONlogoutreceiptcheck, truthfulunconfirmedservernote, busy/dirty/storagefailurehandling. No automatic
closeofanotherwindow ornewdraftvault. Manifest tab/history/filter/disclosures/anchor retained, incoming
selectioncleared/reviewed. Ready wordingmatchesexistingreservation. Compactembeddedheader; guideskept.
Manifestreport typography/spacingonly,samefictionalbody2pages→1, nofactremoval/universalclaim.

Parentbrandingreproduction31,634byteJPEG→222,398bytePNG→297,067byteJSON; preview200/save413. Fourprofile
routesnowexisting3MBservicecap ratherthan100Kprecheck, otherlimitsunchanged2MB/4096/8Mpixels. User45Kfile
notreceived/inspected. Retainedoffscreenreportdraftno longerhasForm/blocksFleet; visibleResumereturn;
qshecheckboxretained; originalversionspinned; pre-send/ownership/busyticketsguard. In-tabnotdurable,
signout/reloadwarn, trueactiveworkstillblocked. Noautomaticprofilepublication/discard.

OperatoridentityselectedexistingCOMPANY_ID+COMPANYmodeatstartupfromdeployJSON/rasterfolder. Publicbounded
safePNG/JPEG route/static/company-identity/logo, only selectedbytes; info safe descriptor. LocalANDactual
hosted_runtimeinfoforwardingrequired (boundarytestcaughtmissinghostedprojectionbeforefinalfreeze).
No privatepaths/config/profileinpublicdescriptor; demoabsent. Main+standaloneFleetheaderplaque, embedded
noduplicate. ActualSulmaraartworkNOTavailable: attachmentswerehosting/login screenshots, notcorporatemark;
neverembedthem. ShippedSulmaraentrylogo:null,namefallbackonly. NeedactualapprovedPNG/JPEGviafile/ZIP;
operatoraddscompany_logos/sulmara/logo.png+JSONlogo filename. No guesses/externalart/no PWAiconchange.

SevenexistingappPythonchanged (access_review,fleet,fleet_access,fleet_reports,fleet_ui,server,hosted_runtime)
plusdeployment_brandingnew;190otherssame/198total.86JSsyntax. Maincriticalcache/write/queue/auth/signout
transactionspansunchanged; render/nav/exitbusy/retained-form/openFleetadapterschanged. No newtables,
permissionflags,dependency,env/storeversion/migration. Newexplicitmode +publiclogorouteonly. SevenHelp
bodies/outlinesbrowseradmin/fleetaccess/fleet/manifests/receiving/companybranding/accessreview;69otherssame,
all76match.21existingPDFs32iconfilesunchanged. DocsADMIN_FLEET_COMPANY_IDENTITY.md.

## Actual checks
**619 selected Python tests, 92 compound browser checks and 86 JavaScript syntax checks passed.** All 198 application Python modules parse; 190 existing modules are byte-identical to UI61. The frozen source has 1889 tracked runtime files. Python groups: workspace_py=97, hosted_http_py=53, admin_branding_py=108, originals_py=65, preserved_py=118, hosting_py=178. Browser groups: admin_browser=12, fleet_browser=20, interface_browser=7, refresh_browser=26, signout_browser=13, originals_browser=14. Six additional integrated C01/hosted-branding checks and a read-only, same-record manifest PDF comparison completed. The 16-workspace × three-width shared-interface comparison is inside its browser group, not 48 extra functional tests. The retained refresh group includes the normal 33.5-second concurrent timer check.

One historical UI60 test hard-codes its retired asset-cache URLs and was deliberately deselected; the new UI62 contract retains the complete current main-script/stylesheet precache and storage-identity assertions. Other operational assertions were not removed. Initial service/browser fixture and selector failures, earlier complete development runs and a prior full candidate run are retained separately and excluded. An actual C01-boundary check caught a missing hosted /api/info identity projection after the earlier candidate passed local-app checks; the projection was fixed, a hosted-factory regression added, and every final counted test group rerun on the refrozen source. An initial new-test anonymous profile read omitted the required project header and correctly received 409; the corrected test supplies the project header and verifies authentication refusal. A source-audit script initially used a nonexistent invitation-module filename; the exact real module is now checked unchanged. After the full final run, the Fleet browser harness's inherited method label was corrected from UI61 to UI62 and that entire browser group rerun; application bytes were unchanged. Earlier runs and these repeat checks are not added to the totals. No unrelated historical failure, native execution or live deployment is claimed fixed.
Finalsource/commands/XML/JSON/reportparity/ZIPreplayauthoritative; repeatedchecksaddnocoverage. Actualassets,
fictionalSQLiteTestClient/injectedfetch/hash/stagedmemory+iframe; ASGIhosted/C01simulatedTLSheaders, notlive
HTTPS/Nginx/Docker/normalnavigation/durableIDB/SW/installedChrome/physical/WindowsPowerShell/native/fullsuite/
fullsecurityaccessibilityload/offhostacceptance. No realcompanydata/credentials/deploymentactions.

## Preserve/next
ActivatedSulmaraC01ID/domain/disk/marker INITIALISE_COMPANY=NO removedbootstrap; separateG01demodata/config.
Backup/approvedcommit/.git/independentedits/operatorcompanyidentityconfig/unsentmain+logs. No reset/reimport/
site-data clear/syncdisable/repeatsetup/incompatiblepreC01/preUI34writer. Oldsoftwaredoesnotunderstandnew
additive accessmode; reviewaccessandunsentproposalsbeforeanysource rollback, notDBrollbackforUI.
Onefictionalbrandingretain/smalllogo/adminnav/project+logistics/restrictedaccount/shipment/phonecheck.
ActualapprovedSulmaralogo remainsneeded; namefallbacknotclaimedsuccessfulartworkinstallation. Chrome
focus-existingwindow/nativeiconissueoutsideupdate; do notkill/reloadunsavedwindows. Currentguide/remaining
sectionreviews and widerDEVELOPMENT_TODOretained. No automaticbackgroundworkorassumedliveversion.
