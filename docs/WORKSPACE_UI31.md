# Wavelink UI31 — activity, Original Files access and website icons

Core **1.34.19**. Prepared from Adriano’s actual uploaded **UI30 + working G01** repository. No live GitHub/Render access or deployment.

## Update with GitHub Desktop

1. Preserve unsent work and your approved project backup. Extract the ZIP.
2. Copy **everything inside UPLOAD_TO_GITHUB** into the **existing Wavelink application repository folder**. Accept replacement of the same filenames. This is not the separate Wavelink-Website repository.
3. Open GitHub Desktop, review, commit and **Push origin**. Deploy the intended commit through the established service workflow.

Do not delete files missing from this small patch or replace the whole repository. The optional **CHECK_UI31_UPDATE.ps1** only checks files; it is not the installer or a required extra upload. This update is for the actual UI30 folder you sent. Stop and reconcile independently changed source instead of overwriting it.

No environment changes: preserve **DEMO_PUBLIC_ENTRY=YES**, **INITIALISE_FICTIONAL_DEMO=NO**, required access password, matching non-admin guest credentials, separate named administrator, existing domain/persistent disk and removed bootstrap. No reset, demo re-import or clearing browser storage.

## Subtle project activity

A small **N active** control sits beside the project name. Click it for names; Close, Escape or clicking away hides the panel. It includes you and counts each account once across tabs/sessions. A shared guest is one account, not identifiable visitors. Any signed-in project account, including your public demo guest, can view this project activity list; no cross-project or vessel-only directory is exposed. Any signed-in project account, including your public demo guest, can view this project activity list; no cross-project or vessel-only directory is exposed.

Visible, online, signed-in project browser workspaces send an empty heartbeat about every **30 seconds**. The list expires entries after **90 seconds** and rechecks saved sessions, enabled accounts and current project scope on each request. A closed/hidden tab can remain briefly; an idle but visible tab still counts. This is connection presence, not attendance, productive work, shift assignment, a read receipt or proof of location.

The feature keeps only session hashes and short-lived contact times in one application instance’s memory. No new SQL tables, durable presence history, operational text, page names, IP/location fields or client-supplied target users are stored by the indicator. Existing platform/access logging is not changed. A restart clears the list. The current single-worker deployment is retained; this is not a distributed multi-worker presence service.

Anonymous, legacy-code and vessel-only sessions are excluded. Standalone native/Fleet pages do not send these heartbeats. The main workspace continues reporting while using embedded Fleet. Activity failures show **Activity unavailable** rather than zero; they do not use the operational queue, save a handover, renew a local-write lease, sign out or clear drafts. API responses are not cached. A separate safety bound limits tracked sessions to 512, not a load-test claim.

## Original Files directly in the sidebar

Use **Documents → Original files**. This opens the existing folder/revision library without replacing the underlying page. **Account → Original files** remains available. Existing UI19 folder/upload/revision features are unchanged.

The account needs **Original documents → View and download original documents**. The public demo runs as your non-admin guest; it may have that viewing permission without becoming Administrator. Upload, Add revision and folder organisation remain named-administrator actions. No permission is granted by this patch, and the live guest settings have not been inspected. On your existing site, try the Account entry first and review that permission from a separate named administrator.

The library retains its UI19 feature badge; the new sidebar access does not mean its source revisions have been recreated. Existing files, IDs, hashes, folders, references and audience rules are untouched.

## Same icon family as the website

The exact assets were retrieved from **Wavelink Website 2.3.1**, not redrawn. The app header, Fleet header and served Help/contact pages use its mint **wavelink-mark.svg**. Browser tabs and app/home-screen icons use the website’s navy **favicon.svg**; 192/512 PNGs and a multiresolution Windows ICO were converted from that vector. The website’s 32px/favicon and Apple touch icon are copied unchanged. Native icon source assets are also updated.

Publisher **AJ Offshore Solutions**, **support@mywavelink.com**, website sales contact, customer report branding and archived PDFs are unchanged. No installed Windows executable/installer was rebuilt; those receive source icons on a later native build. Existing browser/OS shortcuts may retain an old cached icon until their normal update. Do not uninstall or clear site data to force it while work is unsent.

## Preserved handovers

My shift, default/custom schedules, private **Save & close** and ordinary **Finish handover** remain unchanged. No routine reason, confirmation checkbox or review screen has been reintroduced. Unsent notes remain in-tab until an explicit save; this is not offline autosave.

## Verification and limits

See the current verification report for the tests actually completed on frozen source. Previous partial/failing runs are kept separately and are not counted as passes. Selected fictional SQLite/API checks and Chromium with controlled transport/in-memory storage are not live-service, physical-device, durable IndexedDB, service-worker lifecycle, Windows/PowerShell, full-suite, load, full accessibility/security/isolation, Docker or off-host recovery acceptance. No mailbox test, account change or deployment occurred.

The actual uploaded repository contains 100 non-.git files. Its old deployment manifest references 14 absent historical documentation files and two differing documentation/launcher files; executable UI30 and G01 source matches. UI31 preserves the actual folder contents and rebuilds the manifest rather than fabricating those historical files or asking you to delete anything. These metadata gaps do not establish which commit is live.

Rollback source through your approved UI30 + G01 commit; never reset data or apply old full archives. Keep UI29 selective-transfer safeguards; the pristine-source recovery helper remains unapproved for the overlaid runtime.


## UI31 final local results

317 selected Python tests (226 application + 91 gateway/package), 58 compound Chromium checks, 59 JavaScript syntax checks and 183 Python parses completed successfully on the frozen runtime. These counts include no partial/failed attempts. Final ZIP replay/hashes are recorded in the separate verification report.
