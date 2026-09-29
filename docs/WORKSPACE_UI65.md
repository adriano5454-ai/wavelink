# Wavelink UI65 — role-ready invitations and controlled access

**Core 1.34.19 · UI65 · Mail Startup M01, Company C01 and demo G01 preserved · 29 September 2026.**
This is a compact source update for the exact verified **UI64 + M01 + C01 + G01** application repository.
It is not a project/database backup, full repository replacement, live deployment, SMTP acceptance or
profiles/recognition release.

## Before updating

Preserve the approved Git commit, a complete same-company backup, C01 identity/activation metadata,
persistent disk, Render settings and unfinished work in every main/separate-log browser window. Both company
and demo services may deploy the same branch; review that before pushing. Do not remove `.git`, copy this into
the Wavelink-Website repository, recreate the company, repeat first setup, re-import data, clear browser
storage or disable synchronisation.

UI65 advances the company-membership schema from version 1 to version 2 in one transaction. It retains every
existing account, account ID, password hash, invitation, membership, receipt key, grant and audit row, then
adds five role/scope tables and nine explicit initial role revisions. Existing UI64 invitations do not gain
a guessed role or access. **Keep UI65-or-later application software after this migration.** UI64 and earlier
do not understand the new authority records; application rollback against the upgraded database is not a
safe UI troubleshooting step.

## Install through GitHub Desktop

1. Extract the delivered ZIP.
2. Copy **everything inside `UPLOAD_TO_GITHUB`** into the existing UI64+M01 Wavelink application repository.
   Replace matching files; do not delete files absent from the update and do not replace `.git`.
3. Review the changes. The cumulative application change is in `deploy/extract_source.py`; the existing
   `deploy/company_entrypoint.py` must remain at SHA-256
   `2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`.
4. Commit and Push origin. Let each intended service use its normal deployment action. Do not alter C01/G01
   disks, identities or modes. No new environment key is required.
5. After the intended service is healthy, sign in with the existing named administrator, open
   **Invitations & access**, and use fictional/disposable staging identities for the checks below.

The optional verifier in the outer ZIP is read-only. It checks the parent hashes and payload; it is not an
installer and was not run on Windows here.

## One deliberate invitation workflow

The new form is:

**Recipient email → Department → Job role → Access summary → Send invitation**

Department and role begin blank. Role selection resolves a company-controlled, immutable revision. The
summary shows the exact permission count and whether the proposal can activate after mailbox verification.
A folded **Adjust access** section lets an authorised inviter narrow a participant profile; it cannot expand
permissions or alter management/administrator profiles per invitation.

The service snapshots company, exact recipient, department, profile/revision, displayed role, core security
role, explicit permissions, membership actions, delegation ceiling, task-management flag, authorising actor
and authority versions. It signs and revalidates that snapshot at issue, resend, preview, code verification
and acceptance. It never silently adds prerequisites or truncates an unavailable role.

## Roles are not security shortcuts

UI65 stores three separate concepts:

- **Department:** the approved organisational placement.
- **Job role:** Survey, Survey Tech, Processor, Geo, Trainee, Contractor, Supervisor, Party Chief,
  Administrator, or an administrator-created company profile.
- **Access profile:** exact permissions, core security role and bounded management/delegation scope.

The existing core security roles remain Technician, Supervisor and Admin. The six participant profiles use
an explicit 28-capability operational allowlist and do not obtain builders, task assignment, independent
approval/finalisation, account management or complete backup access by title. Role profile changes create a
new immutable revision; they do not rewrite old invitations or existing members.

Only an existing administrator can issue Supervisor, Party Chief or Administrator. Supervisor and Party
Chief create a real server-side management scope for the approved department. Task management still checks
current approved membership, department placement, `tasks.manage` and that active bounded scope; the text
label alone is never authority. Administrator remains the explicit complete administrator boundary.

## Acceptance outcomes

No operational access exists before verification of the exact invited mailbox and committed acceptance.

- A valid, still-authorised pre-approved invitation atomically creates one enabled account, approved
  membership/department, exact explicit policy, captured role revision and any bounded management scope.
  No second routine approval is required.
- A sender with proposal-only authority may send a participant proposal, but the interface says
  **Approval required**. Verified acceptance creates a disabled deny-all Pending account.
- Every unchanged UI64 invitation follows the legacy Pending/no-access route. No role is guessed.
- If issuer authority, department, role revision/profile status, delegation version, company, proof or expiry
  no longer validates, the link cannot activate stale or partial authority.
- Same-operation/concurrent acceptance is idempotent and returns one saved identity/grant set.

A pending participant proposal may later be narrowed inside its signed department/access ceiling; approval
cannot move it or add permission. A stale profile proposal may be rejected but not approved into authority.

## M01, mail and sign-in boundaries

The M01 company launcher is byte-identical and still forwards only the validated company identity and
INVITE_ONLY SMTP allowlist to the company application. Mail remains OFF/fail-closed unless the existing
configuration is complete. This update neither sends an invitation nor validates credentials, DNS, the
sender domain, public HTTPS or inbox delivery. SMTP acceptance means submitted to the mail server, not
received. Existing User ID/password operational sign-in remains; public email-first sign-in/domain routing
is separate work.

Do not put SMTP passwords, codes, invitation links or setup secrets in GitHub, screenshots or support files.
The demo child and Nginx environments remain isolated from mail credentials.

## Persistence, backup and recovery

Same-company backups retain role revisions, invitation/member snapshots, scopes and audit while purging
short-lived challenges/sessions/rate keys and closing open invitations. New-company/project import preserves
attribution but suspends enrolled memberships, role assignments and scopes for administrator review. The
archive remains sensitive and unencrypted. A real same-company recovery also requires the matching company
identity/activation metadata and disk procedure.

M01 startup, C01 identity, G01 separation, Original files, shifts, notes, guest signatures, UI55 refresh
protections and device-local unsent work are not replaced. A temporary QR visitor never becomes a member,
profile or recognition identity.

## Staging acceptance

Use a staging company and disposable mailboxes:

1. Confirm existing named administrator login and a current complete backup.
2. Send Survey Tech with the normal 28-capability profile; verify the exact mailbox and confirm the account
   activates with that signed revision only.
3. Repeat with one participant permission deliberately removed; verify the 27-key snapshot remains exact.
4. Give a coordinator invitation-only authority; verify the form says Approval required and acceptance stays
   disabled/Pending.
5. Send Supervisor for one department; verify task management works only within the approved department and
   that the account is not Administrator.
6. Edit a role; verify revision 2 is used for future invitations while revision 1 remains readable/immutable.
7. Remove an inviter's supporting authority before an outstanding acceptance; verify activation is refused.
8. Accept one unchanged UI64 invitation and confirm the legacy Pending wording/no operational access.
9. Restart, inspect audit/history, then perform and verify a real same-company backup/restore before use.

## Verified local scope and limitations

A fresh extraction from the unchanged five source parts produced 1,922 tracked runtime files and matched the
prepared UI65 tree byte-for-byte outside generated manifests. The 632-record cumulative overlay retains M01's
launcher separately. Selected Python regressions, all 58 original UI64 membership cases, static syntax checks
and nine shipped-asset browser scenarios passed. Browser scenarios covered 1440, 390 and 320 pixels without
horizontal overflow or JavaScript errors.

These are local fictional checks, not a full application suite, independent security audit, live Render/DNS,
real SMTP/TLS inbox, production load/concurrency, Windows/installed-PWA, real-device service-worker upgrade or
accepted off-host recovery. No repository push, deployment, database/account write on the live service or
external email occurred.

## Not included

Profiles, avatars, Team updates, likes, contribution points, 1/3/5 controls, tiers and badges are the next
coherent implementation batch. Email-first operational sign-in/domain routing remains a separate requirement.
Do not present either as delivered by UI65.
