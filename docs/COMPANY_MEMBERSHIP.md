# Company membership, role-ready invitations and controlled access — UI65

**Core 1.34.19 · UI65 · Company C01 + demo G01 compatible · requires Mail Startup M01.**

UI65 adds company-owned job-role profiles and signed invitation access snapshots to the existing
invite-only membership workflow. It does not implement corporate-domain self-registration, a shared
identity provider, email-first operational sign-in, SSO, MFA or automatic account linking. The intended
`sulmara.com` domain remains unverified and is not an authentication rule. Temporary document QR visitors
remain separate identities and never become company members or receive role/recognition history.

## Three separate concepts

UI65 stores these independently:

1. **Department** — the active company department in which membership is approved.
2. **Displayed job role** — for example Survey, Survey Tech, Processor, Geo, Trainee, Contractor,
   Supervisor, Party Chief or Administrator.
3. **Access profile** — the exact versioned permissions, membership actions, delegation ceiling and
   management scope captured for that assignment.

The existing core account security roles remain `technician`, `supervisor` and `admin`. A displayed role
name cannot create authority by itself. Renaming a role profile creates a new revision and does not change
an earlier invitation or existing member. Record privacy, assignment, custody, site, Fleet and designated-
approver rules continue to apply after module permissions are granted.

## Existing sign-in and operator prerequisites

Normal company sign-in still uses the established User ID and password. Existing accounts retain their
IDs, passwords, roles, explicit policies, records and signatures. New invitees choose a User ID and
passphrase only after verifying the exact invited mailbox. The separate **Membership status** page
(`/join-team`) accepts that User ID or verified email, but issues only an own-status credential. It never
becomes an operational project session.

Email sending remains OFF until the operator deliberately configures the existing activated company
service. Keep `WAVELINK_MEMBERSHIP_MODE=OFF` until the exact company origin and TLS-protected sender are
reviewed. Existing named login does not depend on SMTP. The demo service cannot enable membership mail.
UI65 preserves Mail Startup M01 environment forwarding; it does not change sender addresses or credentials.

Required service settings remain:

| Setting | Meaning |
|---|---|
| `WAVELINK_MEMBERSHIP_MODE` | `INVITE_ONLY` to enable; `OFF` by default |
| `MEMBERSHIP_SMTP_HOST` | Approved authenticated SMTP server |
| `MEMBERSHIP_SMTP_PORT` | Provider-approved port; 587 is the STARTTLS default |
| `MEMBERSHIP_SMTP_TLS` | `STARTTLS` or `SSL`; plaintext is refused |
| `MEMBERSHIP_SMTP_USERNAME` | Authorised sender account |
| `MEMBERSHIP_SMTP_PASSWORD` | Sender credential/app password |
| `MEMBERSHIP_SMTP_FROM` | Mailbox authorised for the sender |

The UI reports submission to the mail server, not inbox delivery. An unknown transport result remains
**unconfirmed**; inspect the saved invitation before deliberately using Resend. Resend rotates the proof
and codes while retaining the reviewed snapshot only when it is still valid. Never store SMTP credentials,
invitation links or mailbox codes in GitHub, screenshots, logs or support bundles.

## Role profiles

A company administrator maintains versioned profiles under **Invitations & access → Role profiles**.
UI65 seeds nine explicit profiles:

- Survey, Survey Tech, Processor, Geo, Trainee and Contractor use the participant family and the explicit
  28-capability participant allowlist. They do not receive reusable builder, assignment, approval,
  finalisation, account-management or complete-backup authority by title.
- Supervisor and Party Chief use bounded management profiles. Only an administrator can issue them. Their
  management power is tied to the approved department, exact permissions and an auditable management scope.
- Administrator is complete explicit administrator authority and can be issued only by an existing
  administrator.

Saving a role creates an immutable revision. A future edit affects future invitations by default; it does
not rewrite previous revisions, invitation snapshots or member assignments. Deactivating a profile prevents
outstanding links based on it from activating. Participant invitations may be deliberately narrowed through
**Adjust access**. Management and Administrator invitations must use their complete reviewed profile and
cannot be expanded or partially altered in the invitation form.

## Send a role-ready invitation

The normal form is:

**Recipient email → Department → Job role → Access summary → Send invitation**

Department and Job role start blank and require deliberate selection. Selecting a role shows its revision,
family, exact permission count and whether access can activate after verification. Personal and corporate
mailboxes are both supported. An invitation lasts seven days.

An administrator can pre-authorise any valid built-in/company profile within their current authority. A
non-admin coordinator can propose only a participant profile inside their approved department scope. That
proposal becomes pre-authorised only when the coordinator currently holds all three membership actions,
every proposed permission and the matching current delegation envelope. Invitation-only authority can send
a proposal, but the interface states **Approval required** and acceptance remains no-access pending.

The service stores the company, exact recipient, department, profile ID and revision, role name, security
role, explicit permissions, membership actions, delegation capabilities, task-management flag, authorising
actor, current authority epoch/version and an HMAC-protected snapshot. It refuses unknown permissions,
missing dependencies, silent expansion, stale editors and management roles from non-admin issuers.

## Verify the exact mailbox

Opening a link, forwarding it or allowing a mail scanner to preview it never creates a member. The recipient
must enter the exact invited mailbox and receive a separate eight-digit code. Codes last ten minutes, allow
five failed attempts and retain the existing resend/rate limits. The recipient then enters their full name,
chooses a unique User ID and creates a 14–128 character passphrase with at least six different characters.

Acceptance rechecks, inside the same write transaction:

- invitation company, state, expiry and proof;
- exact mailbox and one-time code;
- active department and active role profile;
- immutable historical role revision and signed snapshot;
- current inviter identity, authority epoch, delegation version, department scope and permission ceiling;
- unique account identity and idempotent operation receipt.

Two concurrent retries of the same operation return the same saved outcome and create one identity,
membership and role assignment.

## Pre-authorised activation versus pending review

A still-valid pre-authorised invitation atomically creates and enables the account, stores the approved
membership/department, writes an explicit account policy, assigns the captured job-role revision and enables
normal company sign-in. No operational access exists before successful mailbox verification and committed
acceptance.

For Supervisor and Party Chief, acceptance additionally creates a department-bounded management scope and
delegation record. Task review/management uses that real server-side scope plus current membership,
department membership and `tasks.manage`; the displayed title alone is insufficient. Administrator access
uses the existing administrator security boundary.

A legacy UI64 invitation has no role snapshot and remains the original path: acceptance creates one disabled
Technician account with explicit deny-all permissions and a Pending membership. A valid proposal-only invite,
or one that never carried pre-approval, also stays pending. Existing UI64 links are never assigned a guessed
role. An authorised inviter may revoke/replace one with a newly reviewed UI65 invitation.

A pre-authorised link whose inviter lost authority, department was disabled, profile was deactivated,
snapshot was altered or delegation version changed is refused; it is not partially activated. A proposal
that required approval can be reviewed within the signed participant ceiling. Approval may narrow it but
cannot move it to another department or add permissions outside the proposal. A stale proposed role may be
rejected, never approved into authority.

## Bounded delegation and independent grant sources

The existing `members.invite`, `members.review` and `members.manage` capabilities remain separate.
Administrators configure a coordinator's current actions, departments and grantable capabilities.
Effective delegation is always:

**current independently held authority ∩ administrator-approved allowance ∩ active department scope**

Dependencies must also be present. Delegated rights cannot be delegated onward. No self-promotion,
Administrator creation by a Supervisor, management of another coordinator, complete backup grant or
all-department shift authority is available through a participant delegation. Losing the donor's independent
authority or scope stops dependent grants; restoring it does not silently revive them.

Administrator policy and each donor's grants remain separate sources. Withdrawing one source does not remove
another source. Suspension preserves identity and recorded work while stopping operational/community access.
Normal password changes revoke sessions but do not silently rewrite valid independent grants.

## Persistence, migration and transfer

UI65 migrates membership schema version 1 to version 2 in one transaction. It retains every UI64 account,
password hash, account ID, invitation, receipt key, membership, grant and audit row unchanged, then adds:

- `company_role_presets`
- `company_role_revisions`
- `company_invite_proposals`
- `company_member_roles`
- `company_management_scopes`

Nine initial role revisions are seeded explicitly. Existing users and invitations are not mass-updated.
Unknown, partial or malformed storage is refused rather than reset. Keep **UI65 or later** once this schema
is present; UI64 and earlier do not understand the role/scope authority records. Do not roll back the
application or database to fix an interface problem.

Same-company backups retain role revisions, invitation/member snapshots, scopes and audit. Temporary codes,
status sessions and rate keys are removed from the copy, and open invitations are closed. Import into a
new company/project preserves attribution but suspends enrolled memberships, role assignments and management
scopes for administrator review. The export is unencrypted and remains sensitive. A complete same-company
restore still needs the company identity/activation metadata. M01 startup forwarding, C01 tenant identity,
G01 demo separation, original documents, guest signatures, shifts and device-local unsent work are not
replaced by UI65.

## Browser and failure boundaries

Access forms remain in the open tab until saved; they are not offline identity drafts. Closing a dirty or
uncertain form warns. A lost response can retry the exact operation ID and payload. A definitely unsent old
form cannot silently use a replacement account. A delayed request cannot overwrite a newer editor. Help
opens in a separate tab. Membership entry is network-only/no-store and never falls back to the main cached
application.

Role-ready browser checks use the shipped assets with a fictional TestClient/SMTP sender. They cover 1440,
390 and 320 pixel layouts, deliberate blank selections, participant narrowing, exact management profiles,
immutable revisions, verified activation and legacy-link wording. These checks do not establish live SMTP
inbox delivery, public DNS/HTTPS, service-worker upgrade on a real device, production load, an independent
security review or an accepted off-host restore.

## First staging acceptance

Use disposable mailboxes and a staging company. Confirm existing named login first. Configure the real TLS
sender, send a Survey Tech invitation, inspect the received role/access wording and verify the separate code.
Confirm immediate access contains only the signed permissions. Repeat with a narrowed participant profile.
Test one invitation-only coordinator and confirm the result remains pending. Test a Supervisor in one
department and verify they can manage only eligible tasks in that scope. Remove the inviter's authority before
another acceptance and confirm activation is refused. Inspect role revisions, audit history, restart
persistence and an actual same-company backup/restore before operational use. Do not use valuable unsent work
for destructive testing.
