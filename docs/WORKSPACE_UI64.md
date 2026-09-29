# Wavelink UI64 — invitations, pending membership and controlled access

**Core 1.34.19 · UI64 · Company C01 and demo G01 preserved · 29 September 2026.**
Stage B of the approved personal Home and company-access plan. This is an update for the exact **UI63 + C01 + G01** repository, not a full repository, a live company backup, or a completed email/domain deployment.

## Important before installing

This release adds a forward database upgrade: **eleven company-membership tables and one users.membership_required column**. They are created and validated transactionally; no manual SQL or reset is needed. Existing accounts keep their identities, passwords, policies and evidence. Preserve the complete company backup, approved commit, independent code/identity-logo changes and unsent main/separate-log work first.

**Keep UI64-or-later software for projects upgraded to this membership schema.** Earlier software does not enforce the new pending marker or delegated-grant provenance. Do not downgrade against that database, roll data back merely for a screen change, recreate the company, re-import the demo or clear browser storage. Existing C01 activation/disk/identity metadata must remain with the full company backup.

## Update through GitHub Desktop

Extract the ZIP and copy **everything inside UPLOAD_TO_GITHUB into the existing UI63 Wavelink application repository**. Replace matching files, review, commit and Push origin. Keep .git and files absent from the patch; do not use Wavelink-Website.

**Copy the complete payload, not only the extractor.** This release also changes deploy/company_runtime.py for the exact isolated enrollment routes, and adds a blank optional deploy/membership.env.example. The optional PowerShell script is a read-only checker, not an installer; it was not run on Windows here.

Both services may auto-deploy the same branch. Keep activated Sulmara COMPANY/C01 IDs, PUBLIC_URL, disk and activation marker, INITIALISE_COMPANY=NO and removed bootstrap secrets. Keep the separate G01 demonstration settings/disk unchanged. Operator-owned company_identities.json and company_logos are not replaced. No new dependencies or browser-store version are required.

## New workspace: Invitations & access

A named administrator opens **Administration → Invitations & access**. Delegated coordinators have their own **Invitations & access** navigation entry, without gaining Administration. The views are **Access requests · Members · Invitations · Access history**; administrators also have **Delegation**.

A scoped pending request appears on the authorised reviewer's **Home → Needs my action**. It is not a company-wide list for every user or a private Task. Existing personal assignments/history and the separate Workspaces directory remain.

## Invite, verify, then approve

**Invite person → exact email and proposed department → Send invitation.** Personal email is supported, as well as corporate addresses. Invitations expire after seven days. The recipient must verify the exact mailbox using an independently emailed eight-digit code, then choose their name, User ID and passphrase. Code lifetime is ten minutes with five failed attempts and resend limits. Opening an email link does not create an account; forwarding it without mailbox verification is insufficient.

Acceptance creates **one disabled Pending account, an explicit all-false policy and no approved department**. A pending or suspended member cannot receive a normal project session, and a missing policy cannot restore Technician defaults. Their isolated **Membership status** page exposes only their own name, verified email, User ID, company and status. No colleague lists, presence, equipment, operational records, files or private histories are available there.

The reviewer explicitly chooses Approve or Reject and confirms the department. No permission is selected automatically. **Approval with zero permissions still leaves the user on the status page.** Granting access does not automatically sign that page into operations: once approved with effective permissions, the person uses their chosen **User ID and password** at normal company sign-in. Verified email or User ID works on Membership status only in this stage. Existing company accounts are never auto-linked or recreated by matching an email/name.

Status sessions last up to eight hours and are held only in the page's memory; after reloading, sign in to status again. They never become operational tokens. Lost acceptance or management responses retain the exact original request for retry. If the account was created but status sign-in then fails, the page explicitly says the request was saved and offers status recovery instead of creating another account.

## Configure delegation, not just a broad permission checkbox

Three new catalogue keys are **Invite members, Review membership requests, and Manage permitted access**. They default OFF for non-admins. Under **Invitations & access → Delegation**, the administrator sets those responsibilities, the person's active departments and the precise operational permissions they may grant.

The coordinator must independently hold those permissions and their prerequisites. Having the permission is necessary but not sufficient: it must also be in the explicit delegation allowance and authorised target scope. Ticking a membership-action flag without an applicable envelope gives no effective coordinator authority. Department-head status alone is not an implicit grant.

No self-promotion, administrator editing, other-coordinator editing, onward delegation, backup export or all-departments shift extension is available through this workflow. Site logistics roles, user roles, domain ownership and identity recovery remain separate administrator controls. Department scope limits whose access the coordinator can manage; a project-wide module permission is not falsely relabelled department-private.

Only selected grants change. Independent administrator policy and each donor's grants retain their own provenance. Revoking a coordinator's supporting authority stops that donor's rights without removing independent administrator/other-donor grants. Restoring authority does not silently reactivate earlier grants. Recipient scope changes also stop dependent grants. Current authority, prerequisites, session and versions are checked again inside the save transaction and on exact retries.

Access changes revoke affected normal sessions; preserve work and sign in again with the same account. Password-only changes revoke sessions but do not erase valid dependent grants. Pending members cannot be enabled by bypassing membership review in the old permission editor. The existing manual administrator Create user route retains its distinct role semantics; it is not the invitation route.

## Email sending is OFF until configured

**Installing this package does not send invitations, verify sulmara.com or enable self-registration.** The interface states when email is not configured. Existing named company login keeps working. Demo mode cannot send membership mail.

On the intended activated company service, the operator may set WAVELINK_MEMBERSHIP_MODE=INVITE_ONLY together with MEMBERSHIP_SMTP_HOST, PORT, TLS, USERNAME, PASSWORD and FROM. TLS is STARTTLS or SSL with certificate verification; no plaintext mode. Keep actual values in the service's secret settings, never in GitHub or a shared screenshot. See **docs/COMPANY_MEMBERSHIP.md** and the blank environment example for exact requirements and failure behaviour.

Submission accepted by SMTP is labelled **submitted to mail server**, not delivered to inbox. Unknown transport outcomes remain unconfirmed; Resend issues a replacement link. There is no background mail queue. Actual SMTP delivery, sender-domain setup and public HTTPS were not tested here. Check one disposable real mailbox before using invitations operationally.

**sulmara.com remains user-supplied and unverified.** Main-site email-first sign-in, domain verification, trusted multi-company routing, existing-account email linking, SSO/MFA and email password recovery are not added by UI64. These remain Stage C/separate scope. QR document visitors are not company membership accounts.

## Local work, Help and backup boundaries

Management forms remain in-tab until saved, with active-write/Close/Escape/sign-out protection and a warning before discarding dirty or uncertain proposals. No new offline identity/draft store is created. Delayed reads cannot replace newer forms; pre-send checks prevent an old form from adopting replacement credentials. Temporary failure labels a last-saved list; definitive denial clears protected background rows without deleting another editor's text. Help opens separately. Unchanged rows and UI55's quiet cache/refresh behaviour remain.

Same-company backup copies retain identity/grant evidence but purge verification codes/challenges, status sessions and rate keys, and close outstanding invitations. The active database remains untouched. Full and selected-workspace exports contain sensitive membership/verified-email data: they are unencrypted security-bearing archives, not recipient-filtered reports. New-project import suspends enrolled members and deactivates delegation until administrator review; it does not carry live verified authority to another company automatically. Keep C01 metadata with the complete company backup.

## One acceptance session

Use a staging company and disposable mailboxes. Confirm existing login and a complete backup first. Configure the chosen TLS SMTP sender; invite, receive the independent code, join pending, approve with zero rights, then grant a small set. Verify normal User ID sign-in exposes only those capabilities. Give a non-admin a limited delegation and check they cannot grant stronger rights or another department. Withdraw a supporting grant and verify independent administrator rights remain. Test retained personal work, phone layout, restart persistence and actual restore before company operational acceptance.

## Verification and limitations

**417 selected Python tests, 59 compound browser checks, 89 JavaScript syntax checks and 203 Python parses passed.** The frozen runtime has **1,917 tracked files**. Eleven existing application Python modules change; four are added and 188 existing modules remain byte-identical. The normal PWA identity, icons, QR-signing assets, handover note editors, report generators and existing PDFs remain unchanged. The actual UI63 project upgrade, same-company backup and full/selected new-project imports were exercised with fictional identities.

The five new C01/hosted membership checks use the actual local factory with simulated trusted HTTPS headers. Browser checks use shipped assets, real fictional SQLite/TestClient APIs, injected fetch/hash navigation and staged in-memory storage; the separate invitation page uses no main workspace store. The retained 33.5-second concurrent refresh test and sign-out suite passed. SMTP tests use stubbed transports, not external delivery. New Help plus seven existing articles/outlines are updated; all77 catalogue entries match.

A final hosted-test runner initially omitted WAVELINK_TEST_REPOSITORY; its exact frozen tests were rerun with the required environment and five passed. Earlier fixture failures, interrupted/superseded runs and historical release-specific assertions are excluded, not claimed fixed. Current UI64 asset/storage/entry contracts were checked rather than counting old hardcoded cache-name tests as current acceptance. Exact commands/results and source integrity are in the separate verification/evidence.

No full-product suite, live Sulmara/GitHub/Render, real email/HTTPS, physical phone/camera, installed Chrome, durable IndexedDB/service worker, Windows/PowerShell/native, load/security/accessibility certification or accepted off-host recovery is claimed. No live account, credential, permission, domain or deployment was changed. The Chrome focus-existing-window follow-up remains separate.
