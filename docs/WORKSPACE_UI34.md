# Wavelink UI34 — QR invitations to read and sign one document

**Core 1.34.19 · UI34 · 26 September 2026.** Compact update for the exact UI33 + G01
from this chat, on the actual uploaded UI30 repository lineage. Not a full repository,
a live backup or a deployed update. Simple notes/attachments/reason-free saves are retained.

## Update using GitHub Desktop

Preserve your approved commit, complete project backup and unsent work. Extract this ZIP,
copy **everything inside UPLOAD_TO_GITHUB into your existing UI33 Wavelink application
repository folder**, replace matching files, review in GitHub Desktop, commit and **Push origin**.
Deploy the intended commit through the existing service. Do not replace the whole repository
or delete files absent from the patch. CHECK_UI34_UPDATE.ps1 is optional read-only checking,
not an installer or a required upload. Stop and reconcile independent changes.

**Copy both deployment files together:** deploy/extract_source.py supplies the application;
deploy/nginx_config.py permits the isolated signing page through the outer gateway.
The G01 gate.py and entrypoint.py themselves remain unchanged; normal staff sign-in and
public-demo entry are retained. No new environment variables or dependencies are needed.
Keep DEMO_PUBLIC_ENTRY=YES, INITIALISE_FICTIONAL_DEMO=NO, required gate secret, matching
non-admin demo guest, named admin, domain/disk and removed bootstrap unchanged.

**Database compatibility:** this update automatically creates five new invitation/evidence
tables transactionally. No manual SQL is needed. It does not change existing users, permissions,
records or files during initialization. Keep **UI34 or later** for the updated project and
selective exports; do not use an older source rollback or delete tables. Full backups retain
signature evidence. Selected module transfers retain only selected document evidence, clear
temporary grants and close retained invitations. An application restart ends unfinished QR
invitations and visits but preserves saved signatures. No project reset/re-import/site-data clearing.

## Organiser: open the saved document → Invite to sign → Show QR

For a **Toolbox talk**, save the actual discussion and understanding answers before opening
**Invite to sign / signatures** on that talk. At least one topic must be marked discussed and
all understanding answers must be Yes. The talk must still be open. An empty initial attendee
roster is allowed: each QR participant is added when their signature actually saves.

For a **Handover**, finish/publish it first, open its current published reader and choose
**Invite to sign / signatures**. This never shares a private draft or copies notes. An older
reader cannot silently issue an invitation for a newer publication.

The creator also needs **Document invitations → Issue document-specific QR invitations**.
Administrators already have access; ordinary account permission sets are not expanded by this
update. An administrator can deliberately enable it for the named people who will host talks.
They also need the module's normal conduct/create permission and must be the actual author.
Being Administrator does not turn another person's publication into your own invitation.

Press **Show QR · 5 minutes**. The panel shows the QR, countdown, **Copy link** and
**Close invitations**. Once generated, optional settings collapse beneath the QR on phones.
Several people may use the same QR during its five-minute joining window (up to150 admissions).
Creating a new QR explicitly ends older invitations and their unfinished visits.

**Allow temporary guests** starts off and requires the separate permission
**Allow temporary external document visitors**. **Include these published attachments**
also starts off and is available only when that handover revision has files. Select it only
when those exact files should be shared. No unrelated files or newer private attachments are shared.

**Hide panel** does not revoke an invitation. **Close invitations** stops new admissions and
all unfinished visits immediately. The panel refreshes saved participants/signatures about
every five seconds while visible; Refresh people & signatures is also available.

## Participant: scan → read → Sign & finish

The link opens a separate **/sign/** page, not the ordinary demo login or workspace.
A current signed-in personal account can be used without replacing its normal session or
saved work. Otherwise choose **Sign in**, or **Continue as visitor** when explicitly enabled.
Visitors supply their own name and optional company; no full account registration is created.
The shared public-demo guest is deliberately not a personal signing identity.

Named accounts need **Join and sign a specifically invited document** plus the module's
acknowledgement permission. Role defaults allow joining, but older explicitly saved permission
sets do not gain new keys automatically. Review participants' permissions once as needed.
The invitation grants only this document's signing action, not project membership, future
audience access, editing authority, another record, search or directory access.

Read the exact saved wording and declaration. Optionally expand **Draw signature (optional)**,
or simply use your name. Choose **Sign & finish** to record the signature and end document
access. No reason, proxy signature or extra publication wizard. The author cannot acknowledge
their own handover as an incoming participant. The page displays a saved receipt, not Home.

Each admitted reader has up to **10 minutes** from admission, with **3 minutes idle expiry**.
A visible page sends a keepalive every30 seconds. The five-minute QR countdown stops new
admissions; it does not cut off someone who just joined. Hidden/closed pages stop keepalives.
Server expiry, explicit finish/revocation, changed document or restart enforces the boundary.
Tab closure is best effort, not a reliable security event. Refreshing loses in-tab access.
Existing normal Wavelink sessions and unsent notes in other tabs are not logged out or cleared.

The signing page requires **HTTPS**. An ordinary unencrypted local-vessel URL is not enough;
local certificate/network commissioning is outside this hosted update. A real phone needs to
reach the same service. No offline signing or vessel/cloud synchronisation is added.

## Meaning of the evidence

Named-account signatures and **Visitor / self-declared** signatures are visibly distinct.
A drawn mark does not verify identity, physical attendance or authority to start an operation.
A shared QR can be forwarded/rescanned under another name. Individually issued invitations and
optional organiser-admission/presence confirmation are future features, not delivered controls.
Downloaded copies and screenshots cannot be recalled after access ends.

Toolbox signing adds the actual participant and their acknowledgement together, preserving
the discussion/content revision and existing signatures. Joining alone does not add an attendee.
Ordinary content/roster edits still reset acknowledgements and require re-signing. Finalisation
remains a separate authorised action requiring all current listed acknowledgements. A QR never
bypasses a No/unanswered response. Manual facilitator-witnessed guest acknowledgements remain
available; QR visitors are explicitly **not** described as witnessed. The PDF shows their method.

For handovers, named signatures use the existing personal acknowledgement record. Visitors live
in the separate invitation evidence, not fabricated user/recipient rows. No tasks are completed,
maintenance work approved, equipment released, notes copied or new shift created. A previously
saved named acknowledgement is recognised without changing its timestamp or retroactively adding
a drawn mark. Updating/reissuing wording ends outstanding access to the old signing invitation.

The author can view saved marks in the invitation panel and **Download signing evidence**.
The JSON export includes exact document snapshots, fingerprint, organiser, participant type/name,
server timestamp and optional drawing coordinates. It separately records the complete source and
exact displayed wording/shared file IDs, so unshared files are not claimed as seen. File bytes
are not embedded. Panel: latest500
signatures; export: latest2000 with explicit total/truncation. Ordinary PDFs do not embed these
drawn marks; handover visitor evidence is in the invitation panel/export, not its regular PDF roster.

A lost admission or signing response retains the same in-tab request. **Retry same signature**
or **Check saved outcome** can recover its receipt without duplicating evidence or restoring
ended document access. Keep the page open during an uncertain request. Signatures are retained
for history; no automatic retention purge or production policy is introduced.

Your separately enabled public demo is still publicly reachable at its normal address. This
restricted invitation does not make that independent public demo private. Use fictional public-demo
documents and remember that anyone holding an enabled guest QR may join during the open window.

## Checks and retained work

**305 selected Python tests** (214 application + 91 gateway/package),
**78 compound Chromium checks**, **8 actual local Nginx/G01/application checks**,
**62 JS syntax checks** and **186 Python parses** passed
on the final frozen source. The 1,725 tracked runtime files are verified.
Tests cover exact revisions, multiple participants, auth/grant isolation, wrong origin/host,
expiry/revoke/restart, duplicate/lost responses, private file access, rollback/concurrency,
local backup/restore and selective export, with actual QR decoding. The fictional toolbox PDF
was rendered and inspected. Repeated tests are not added as new coverage.

Browser tests use injected transport and storage through set_content; normal navigation was
policy-blocked before acceptance. No real hosted HTTPS, physical camera/phone, durable IndexedDB,
service-worker lifecycle, full-suite, complete security/accessibility/load, Windows/PowerShell,
Docker, signed installer or accepted off-host recovery result is claimed. Nothing was deployed,
no real user data/credentials were accessed, and no account or permission was changed for you.

UI33 photo/file notes and simple Save & close/Finish, schedules/assignments, routine-reason cleanup,
presence, Original Files, approved website branding and support@mywavelink.com are retained.
Maintenance invitation rules are intentionally not implemented in this first release.

**Next:** test one fictional talk with your named account and a private-window visitor; check
signatures, expiry and closure on a real phone before operational use. Continue broad routine-reason
cleanup and coherent usability groups without complicating ordinary work. The retained roadmap,
native-vessel/CCVD exclusion and parked independent sync/local-network work remain.
