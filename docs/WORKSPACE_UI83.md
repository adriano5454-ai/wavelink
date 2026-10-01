# Wavelink UI83 — Account Security and Sessions Batch

**Date:** 1 October 2026  
**Core:** 1.34.19  
**Exact parent:** UI82 Authorised Search and Personal Action Centre Batch  
**Runtime variant:** `workspace-ui83-account-security-sessions-batch-2026-10-01`

## Purpose

UI83 adds a bounded account-security layer to the already-selected Wavelink company service. It combines exact verified-email sign-in aliases, TOTP two-step verification, one-time recovery codes, short-lived login challenges, and active-session review/revocation.

This is deliberately **not** the public email-first company router. A mailbox is accepted only when it exactly matches one approved, verified membership row in the company database that the user has already reached. Typing a company-looking address or sharing a domain suffix does not select a company or grant access.

## Sign-in behaviour

The normal sign-in field accepts either:

- the existing personal User ID; or
- the exact verified membership mailbox inside the selected company.

Unknown, disabled and ambiguous identities return the same generic credential response. User ID login remains available during the reviewed transition.

When two-step verification is not enabled, a successful password check creates the normal 12-hour account session. When it is enabled, the password step creates only a five-minute opaque challenge. It does not issue an operational bearer token or expose company records. A current authenticator code or unused recovery code must complete the challenge.

Each login challenge:

- is stored only as a SHA-256 digest;
- is bound to user, credential version and device ID;
- expires after five minutes;
- records up to eight failed factor attempts;
- is consumed after success, expiry, account change or the attempt limit;
- cannot be reused to create another session.

## Two-step verification

Members can manage two-step verification from **Account & security**.

Enrolment requires the current password and provides:

- an authenticator QR code;
- a manual Base32 key;
- a standard `otpauth://` URI;
- ten recovery codes shown once after confirmation.

The TOTP secret is encrypted at rest using a Fernet key derived from the company membership receipt key. Recovery codes are stored only as keyed SHA-256 HMAC digests and are consumed once. Regenerating recovery codes invalidates the previous set. Enabling or disabling MFA increments credential version and revokes existing sessions.

UI83 does not claim hardware-backed key storage, passkeys, enterprise SSO, an external penetration test or production identity certification.

## Sessions

**Account & security** lists only the signed-in member's active sessions, including:

- device ID;
- issue time;
- expiry time;
- authentication method;
- whether the session completed MFA;
- the current-session marker.

A member can revoke one session or revoke all other sessions. Revoking the current session requires signing in again. Session IDs exposed to the browser are random IDs for new sessions, with a keyed deterministic fallback only for retained legacy sessions.

## Additive storage

UI83 introduces schema version 1 with:

- `account_security_meta`
- `account_mfa`
- `account_recovery_codes`
- `account_login_challenges`
- `account_security_operations`
- `account_security_audit`

The migration is additive, transactional and idempotent. A partial or unexpectedly shaped schema fails closed.

Complete-company backup preserves MFA configuration, recovery-code digests and account-security audit. A selective workspace transfer retains only the schema marker and clears account-bound security state, challenges, operation replays and security audit so copied accounts must enrol again deliberately.

After a database has been opened by UI83, keep UI83-or-later software with it. A rollback requires the matching predeployment application commit and complete database backup.

## APIs

UI83 adds:

- `POST /api/login/mfa`
- `GET /api/security/status`
- `GET /api/security/sessions`
- `POST /api/security/mfa/start`
- `POST /api/security/mfa/cancel`
- `POST /api/security/mfa/confirm`
- `POST /api/security/mfa/recovery-codes`
- `POST /api/security/mfa/disable`
- `POST /api/security/sessions/revoke`
- `POST /api/security/sessions/revoke-others`

Authenticated security routes require the current bearer token and exact selected hub header. No permission key, security-role mapping, recognition rule or operational completion adapter is added.

## Preserved boundaries

UI83 adds no new environment variable, GUI decorator, shell re-parenting, MutationObserver-based restyling or background polling timer. It does not alter Tasks, Maintenance, Checklists, Handovers, Toolbox Talks, inventory custody, Certificates, recognition points, badges or source completion rules.

The M01 company launcher is preserved byte-for-byte. C01 identity, separate G01 demonstration data, existing records, files, signatures, shifts and device-local unsent work remain separate.

## Not completed by UI83

The following remain separate work:

- public email-first entry from `www.mywavelink.com`;
- verified company-domain registry and company discovery/routing;
- safe multi-company account selection;
- password-recovery email delivery;
- real Zoho sender, SPF/DKIM/DMARC and inbox acceptance;
- browser/mobile push notifications;
- passkeys, SSO and external security assessment.

## Apply and accept

1. Preserve the exact UI82 commit and a complete database backup.
2. Copy the UI83 `UPLOAD_TO_GITHUB` contents over the application repository.
3. Confirm GitHub Desktop shows 9 modified files and 2 new files.
4. Commit and push normally.
5. After the intended Render service reports healthy, reload one Wavelink tab once.
6. Enrol a disposable account in TOTP, save recovery codes, sign in with authenticator and recovery code, review sessions, revoke another session and disable MFA.
7. Confirm User ID sign-in still works and an unverified/wrong-company email does not.
8. Confirm no operational token is returned before the second factor succeeds.
9. Do not clear browser storage, reset the company, re-import data or repeat company setup.

Local fictional tests are not live SMTP/DNS, production-data, physical-device or independent penetration-test acceptance.
