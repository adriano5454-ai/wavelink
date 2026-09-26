# Wavelink continuation checkpoint — UI30 + working G01

Prepared 26 September 2026. Core **1.34.19**. User-requested support-contact update
before resuming simplified handover work. Related feature work stays grouped;
contact changes are deliberately isolated from new functionality.

## Verified source

Parent **UI29 + G01**, exact supplied-UI18 lineage, not the other UI18 variant.
112 parent repository files / 111 deployment rows / 1689 runtime files verified.
Core archive remains 8c1b6a8d731d01b05a1290d3a1dd1a544054147aac9048ca345af7983613cd9e.
Parent extractor: 8920f81cd4b9eff51278e97b264fcbb7a325e15c4600a5e3f14dd931ae71027a.
UI30 extractor: 5c1fe86a42ecf38d37bbcbbc3d2c00744354fdd9aa3834d254af964fc0084e15.
Patch ID: workspace-ui30-support-contact-2026-09-26.
G01 gate: 9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701.
G01 entrypoint: a2bbac57635ac6e0b12400bbcbfc7382416ed3d5c7525e4218b7e38c2e7a633f.
193 changed/new runtime resources, 305 cumulative overlays, 1691 runtime files.
Only existing executable upload file changed: deploy/extract_source.py.

## Implemented / not implemented

support@mywavelink.com is the current product support address: hosted contact/compose/
copy/fallback, hosted and native Help, search, preview footer, guide builders, support
material and eight bundled PDFs (six unique contents). No change to author credit,
website sales address, project/customer data, user/login emails, credentials or mail
provider configuration. No automatic email sending or mailbox existence verification.
Legacy PDF/source filenames and archived evidence/vendor parts retained.

Two app Python modules change by email substitution only: branding.py and
checklist_preview.py. 180 other modules unchanged. G01, operational services/APIs,
UI29 simple handover writers, shifts/permissions/audit/import rules unchanged.
No new tables/dependencies/environment/API/storage/deletion/migration. Source for
native contact is updated, but no Windows installer/executable was rebuilt.
Contact/Help cache URLs and shell cache advance. Same-origin cache identities and
all IndexedDB formats/queued work remain. Unsent wording remains in-tab until saved.

All 76 hosted Help catalogue entries still match their topics. Only the hosted
support article's contact wording changes; 75 other article bodies unchanged.
Native topic footers and PDF contacts updated, not a procedural rewrite. Eight
previously bounded topics / 68 plus native/master-PDF/entrypoint review still pending.

## Completed selected local checks

165 Python = 18 contact/branding + 56 simple handover/API/transfer + 91 gateway/package.
31 compound Chromium = 13 contact + 18 simple handover; 58 JS syntax, 182 app Python
parses. Test callbacks run real shipped contact logic with simulated Tk/clipboard.
Browser is set_content/controlled fetch/in-memory persistence, not live navigation.
PDFs: 172 unique pages compare exact email text substitution, bookmarks/links and
pixels outside email-containing lines; longer inline address shifts its following
words within the same line. Poppler master support-page render and six footer crops
inspected. Alias PDFs stay byte-identical to each other.

Initial PDF check failed on Identity-H glyph encoding, then on expected inline text
movement. Encoding and comparison-scope handling corrected before final PDF checks;
failed attempts retained, not counted. No operational application-code finding.
Prior UI29 historical assertion failures not rerun/claimed fixed here. No full suite,
real email, live GitHub/Render/deployment/data/secrets, physical/Windows/PowerShell,
durable IndexedDB/service-worker lifecycle, full accessibility/security/isolation,
load/Docker/off-host acceptance. Original recovery helper remains unapproved.
Contact inherited version overline and low-contrast Write email CTA remain; visible
email hyperlink and copy/fallback verified. Further visual hygiene is separate,
not a reason to add complexity to daily handovers.

## Preserve and next

Keep G01 user-confirmed working, DEMO_PUBLIC_ENTRY=YES, INITIALISE_FICTIONAL_DEMO=NO,
required access password, matching non-admin guest, named admin, demo.mywavelink.com,
disk, removed bootstrap, approved commit/complete backup, .git/outside edits and
unsent browser/separate-log work. No reset/re-import/storage clearing or assumed
live UI29/UI30. Rollback via approved UI29+G01 source, not old full archives/data.
Preserve UI29's selective export privacy for shift setup/audit; do not downgrade it.

Continue **simple handovers first**: setup once, own shift notes, Save & close / first
Finish without typed reason or routine review wizard. Real surveyor feedback before
unrelated expansion. Subtle scoped active-user presence is a separate future feature,
not implemented. Group related substantial releases; compact GitHub changed files,
short readme, one current checkpoint, bulky evidence separate. Never delete absent
patch files. Wider roadmap retained in DEVELOPMENT_TODO. Native vessel/CCVD excluded;
vessel/cloud sync and local phone network investigation parked. No background work.
