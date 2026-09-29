# Company membership and controlled access — UI64

**Core 1.34.19 · UI64 · Stage B · C01 company deployment.**
This describes the delivered invite-only workflow, not verified corporate-domain self-registration,
a shared identity provider, or approval of any real person's access. `sulmara.com` remains the
user-supplied intended domain for Stage C, unverified and not used as an authentication rule.

## Two distinct sign-ins

Normal company sign-in continues to use the established User ID and password. Existing accounts keep
their IDs, passwords, roles, explicit policies, records and signatures. New invitees choose their own
User ID and passphrase after verifying the invited mailbox. Once approved with operational access,
they use that User ID on normal company sign-in. Verified email or User ID can be used on the separate
**Membership status** page (`/join-team`), but this page issues only an own-status credential. Its token
never becomes a normal project session, even after approval.

There is no automatic linking of existing accounts by name or email. Invite-only enrollment is for new
company members. Existing staff are managed without recreating their identity. Main-site email sign-in,
verified-domain discovery, SSO, account recovery by email, MFA and automatic corporate self-registration
remain Stage C/separate scope. Temporary document QR visitors remain separate identities and never become
members or acquire retroactively attributed signatures.

## Operator prerequisites and email

Installation creates the schema but **does not enable sending**. Keep `WAVELINK_MEMBERSHIP_MODE=OFF`
until the operator has configured and reviewed the intended company service. Existing named login does
not depend on the SMTP settings. The demo cannot enable membership mail. No real email was sent or inbox
delivery verified while preparing this release.

Use the existing activated C01 COMPANY service, company identity and exact HTTPS PUBLIC_URL. Do not repeat
company setup, add demo credentials or use the public demonstration's shared guest as a personal account.
Set these service-level secrets/settings outside GitHub:

| Setting | Meaning |
|---|---|
| WAVELINK_MEMBERSHIP_MODE | INVITE_ONLY to enable; OFF by default |
| MEMBERSHIP_SMTP_HOST | Your approved authenticated SMTP server |
| MEMBERSHIP_SMTP_PORT | Provider-approved port; 587 default for STARTTLS |
| MEMBERSHIP_SMTP_TLS | STARTTLS or SSL; no plaintext mode |
| MEMBERSHIP_SMTP_USERNAME | Authorised sender account |
| MEMBERSHIP_SMTP_PASSWORD | Sender credential/app password as required by your provider |
| MEMBERSHIP_SMTP_FROM | Mailbox authorised for this sender |

The stdlib sender verifies the TLS server certificate before authenticating. Invalid/incomplete settings
leave invitations unavailable rather than preventing existing company login. SMTP connection attempts have
a 12-second timeout. There is no background mail queue or claim of exactly-once email delivery. The UI
reports **submitted to mail server**, not delivered to inbox. A failed/unknown transport outcome is
**unconfirmed**: check the invitation before using deliberate Resend. Resend rotates the old link/codes.
The sender address does not prove control of a recipient's corporate domain. Configure sender DNS and
provider requirements through the operator; they were not inspected or changed here.

Review the safe blank `deploy/membership.env.example`; it is documentation, not an automatically loaded
configuration. Never put actual credentials, invitation URLs or verification codes in GitHub, screenshots,
logs or support exports. Membership secrets are not included in public API info.

## Invitation and verification

A named administrator or authorised inviter opens **Invitations & access → Invite person**, enters an
exact email and proposed department, then Send invitation. Personal email is supported. A coordinator
can propose only an active department inside their current envelope. An administrator can leave the
department unassigned for later administrator review. No department membership or operational permission
is created by an invitation.

A link lasts seven days and identifies the company and masked recipient. It is removed from the address
fragment on entry. Opening the page or a mail scanner visiting it does not consume acceptance. The person
must enter the exact invited mailbox and request an independent eight-digit code delivered to it. Codes
last ten minutes, allow five failed attempts, and have resend/rate limits. A forwarded link without the
mailbox code is insufficient. Old links/codes are invalid after resend, revocation, expiry or loss of the
inviter's authority. The person verifies the code, supplies their name and chooses a User ID and passphrase
(14–128 characters with at least six different characters). Ordinary ASCII email syntax is supported;
quoted and internationalised mailbox local parts are not supported in this release.

Acceptance atomically creates one disabled account, an explicit deny-all policy, a verified-email binding
and a Pending membership with no approved department. Invitation/status/code secrets are hash-only in the
database; operation fingerprints covering submitted passwords/codes use a keyed HMAC. The exact acceptance
request can be retried after a lost response without creating another user. Correcting a definitely refused
request is different from replacing an uncertain request. If acceptance saved but status sign-in fails,
the page explicitly says the request was saved and offers status sign-in with the chosen User ID.

Verification/pending/approved/rejected/suspended outcomes remain distinct. Pending and suspended membership
are enforced before operational APIs. A missing or corrupt policy cannot restore Technician defaults.
An approved account with zero effective rights still cannot receive a normal project session. The waiting
page exposes only that person's name, verified email, User ID, company and access status, plus Help and
sign-out. It has no colleagues, presence, inventories, records, audit lists or normal operation tokens.
Status sessions last up to eight hours and remain memory-only in the page; after a reload sign in there again.

## Review and grant access

A reviewer sees only scoped pending requests, including **Home → Needs my action → Review access**.
The page has explicit Access requests, Members, Invitations and Access history views. Administrators also
have Delegation. Request review starts with no decision and no operational permissions selected. Approve
membership alone may leave zero permissions. A meaningful access-decision note is required once, not a
series of generic review pages. The user refreshes their own status, then signs into the company only after
approval and actual grants. Approval never silently logs the person into operational records.

A requested department is confirmed by the reviewer. Non-admin review stays in that requested department
and current scope; department-less requests go to administrators. Existing manually created accounts keep
their existing policy, rather than receiving the new pending state retroactively. The old manual administrator
Create user route retains its explicitly chosen role semantics; it is not the invitation workflow.

## Bounded permission delegation

Three keys appear in the existing permission catalogue: `members.invite`, `members.review`, `members.manage`.
They default OFF for non-admins. Administrators configure actions, up to twenty active departments and an
allowlist of grantable capabilities together under **Invitations & access → Delegation**. Checking the three
flags alone without a valid envelope gives no effective coordination authority. The coordinator must be an
active department member and independently hold each capability they may grant, including prerequisites.
A department head has no automatic membership-admin authority merely because of their title.

The effective allowance is the intersection of current independently held operational rights, the explicit
admin-approved allowance, active department membership and target scope. Rights received through another
coordinator cannot be delegated onward. An ordinary project-wide module flag retains that meaning: department
scope controls whose access the coordinator manages, not a fabricated department-only content boundary.
Private Task/Handovers, designated approvers and site restrictions continue to apply.

No self-approval/escalation, administrator editing, other-coordinator management, onward-delegation keys,
backup export or all-departments shift extension is available through delegated grants. Fleet roles, domain
ownership, user roles and password recovery remain separate administrator functions. The normal operational
preset excludes membership-management flags. Permission prerequisites cannot be bypassed using templates or
raw requests. Reviews and exact retries recheck current actor session, credentials, scope, target version
and authority inside the transaction.

Independent administrator policy and each donor's grant records are separate. Withdrawal changes only the
selected source; a coordinator cannot remove another donor's or administrator's independent grant. Donor
access/role/envelope/membership changes invalidate that donor's grants; restoring authority does not silently
reactivate them. Recipient department/Fleet scope changes stop prior dependent grants. Password-only changes
revoke sessions but do not erase dependent operational grants. Grant provenance and revoked reasons remain
in history. Existing normal sessions are revoked after access changes; preserve work and sign back in as
the same account. The effective policy is also recomputed on every operational request.

Suspension or return to review is an administrator action preserving identity and history. Enrolled identity
records cannot be purged as unused accounts. The original unused, never-enrolled account retirement route
remains supported. This is not secure erasure of personal data; retention and privacy handling need the
company's policy. General security-administration history is not added to My activity.

## Persistence, compatibility and transfer

UI64 adds eleven versioned `company_*` tables and `users.membership_required` automatically in one transaction.
Unknown, partial or malformed membership storage is refused, never reset/reseeded. Existing accounts get
marker 0; new verified members marker 1. Three permission keys are additive; no existing policies are expanded.
There are twelve membership API routes (seven isolated-entry routes and five authenticated management routes)
and an isolated `/join-team` page. The C01 runtime admits only the exact entry route/method allowlist after
initial company activation; existing ordinary protection remains. There are no new dependencies or browser
storage-version changes. The main queue, same-account draft vault semantics and company/domain/disk identities
are not replaced.

**Keep UI64-or-later software for upgraded membership projects. Earlier source does not enforce the pending
marker or delegated provenance. Do not downgrade software against the new database or reset the database for
an interface problem.** Back up the complete company directory/disk, including C01 activation/identity metadata,
before installation. No accepted off-host recovery or production rollout is claimed by the local tests.

Same-company database backups retain memberships, email bindings, policies, grants and audit. All verification
challenges, status sessions and rate keys are removed from the COPY, and issued invitations are closed. The
live project's proofs and accounts are not altered. This backup contains sensitive identity/access information
and is not encrypted by the export. Selective workspace exports retain security metadata as required, not a
recipient-filtered membership report. Native whole-project imports create a NEW project identity: enrolled
members are suspended/disabled and grants/envelopes deactivated until administrator review. IDs and historic
attribution remain; domain verification and operational access do not automatically cross company identities.
The imported original administrator can sign in; this does not transfer a live C01 host setup or SMTP secret.

## Browser and failure boundaries

Access-management forms and selected invitation proofs remain in-tab until saved. No new durable offline
identity store exists. Close/Escape/sign-out wait for active requests; dirty or uncertain forms have a deliberate
exit warning. A lost action response keeps its exact request for retry. A delayed lookup cannot replace a
newer form, and an old form cannot pick up another account's credentials after the write-lease wait.
Help opens separately. Unchanged list refreshes retain keyed rows, while temporary failures label last-saved
information and pause stale actions. Definitive denial clears protected background rows without deleting
another editor's wording. No new periodic timer is added; personal Home and the existing shared refresh remain.
The isolated entry page and APIs are no-store/network-only and never fall back to the cached main application.
Its own-status credential cannot log into the app, Fleet, files or private reports. Real browser persistence,
HTTPS, SMTP inbox delivery, load, independent security review and actual recovery remain deployment acceptance
steps; local simulated transport/storage tests are not evidence of those.

## First acceptance session

Use a staging company and disposable mailboxes. Keep existing login working, configure TLS SMTP, invite a
specific mailbox, verify the actual received code and check the zero-access pending screen. An authorised
reviewer approves with zero rights first, then deliberately grants a limited set. Confirm the normal User ID
login exposes only those capabilities. Give a second non-admin a small delegation envelope; check they cannot
grant a stronger right, another department or onward delegation. Remove one authority and confirm dependent
rights stop without removing independent admin grants. Reopen the same person's work after sign-in, inspect
named history and try the phone layout. Verify sender/inbox, restart persistence and an actual backup/restore
before relying on this for real company onboarding. Do not use valuable unsent work for destructive tests.
