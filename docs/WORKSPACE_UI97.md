# Wavelink UI97 — Password recovery by email

Prepared against GitHub main `0cd4582d82e1ef8bab6a2b02f41a5264fa0183e2` (UI96), verified across all 263 tracked Git blob hashes. Core 1.34.19.

## User flow

Choose **Forgot password?** from named-account sign-in. Recovery opens separately, retaining the original workspace and local drafts. Enter the existing company email or User ID, enter the eight-digit code from email, and set and confirm a new password. The password uses the existing invitation policy: 14–128 characters and at least six different characters. The code expires after ten minutes; five unsuccessful code attempts end that challenge. A new request is available after 90 seconds, with a maximum of five sends per account per hour.

A confirmed reset ends operational sessions, pending MFA login challenges and membership-status sessions. It does not sign the user in automatically. Normal sign-in still enforces MFA, membership approval and existing permissions. Roles, identity, MFA enrolment/recovery codes, alert preferences and operational records are retained. A same-operation retry can confirm an uncertain reset for ten minutes, without repeating the password change; later account changes invalidate that receipt.

Only the exact, unique, previously verified and approved company-account mailbox is eligible. Disabled, deleted, suspended, pending or unverified accounts do not receive reset email. A separate alert destination is not an authentication identity. Accounts without that verified company email require administrator assistance. Unknown and ineligible accounts receive the same neutral response; this response does not assert SMTP acceptance or inbox delivery.

## Email setup

Recovery reuses the existing M01 transactional company mail configuration. There is no new mail provider or user-mailbox connector. Configured company invitations require `WAVELINK_DEPLOYMENT_MODE=COMPANY`, `WAVELINK_MEMBERSHIP_MODE=INVITE_ONLY`, the exact HTTPS `PUBLIC_URL`, `COMPANY_ID`, `COMPANY_NAME`, and the private `MEMBERSHIP_SMTP_*` settings documented in `deploy/membership.env.example`. TLS remains mandatory. Keep credentials in the deployment environment, never in GitHub or exported project files.

Recovery is available when that configured company mailer is ready. If unavailable, the recovery page shows administrator assistance. The user's ordinary alert-email toggle and `WAVELINK_ALERT_EMAIL` remain independent: turning optional alerts off does not suppress security recovery mail.

Code delivery runs after the generic HTTP response. SMTP uncertainty invalidates the challenge without exposing mail details. The user can request another code after the cooldown. A second notification states that the password changed, without including the password or code; notification failure cannot undo a committed reset. A restarted process may lose an unsent background message; request a new code after the cooldown. Inbox delivery and sender reputation require acceptance on the actual deployment.

## Storage and boundaries

Four additive tables store schema metadata, one-way challenge/code digests, hashed rate-limit scopes and short-lived reset receipts. No raw code, reset token or password is stored in these tables. Reset retries verify the password through the existing slow PBKDF2 verifier; receipts do not contain a fast password fingerprint. Failed-attempt counters commit even when verification fails. Updates recheck the exact hub, verified mailbox, membership revision and credential version inside the write transaction.

The public surface requires the exact configured HTTPS Origin and selected hub, bounded strict JSON, and the precise method/path. It accepts no normal session token and exposes no user lookup or account records. Per-client and global request limits complement the account/send and challenge/attempt limits. The client address comes from the server connection, never a submitted forwarded-for value.

The separate page keeps credentials only in memory and does not load the app, operational save journal, IndexedDB, localStorage or a new service worker. API/page assets are no-store; the retained worker fetches this surface only from the network and never substitutes the cached main workspace. An uncertain reset freezes its original request for Retry same request; refreshing requires a fresh recovery request. Full backups and selective transfers clear temporary recovery proofs/rate limits/receipts in the copy only, retaining the schema marker. Existing backup/account review behavior remains.

## Apply and accept

1. Extract the UI96-to-UI97 update outside your checkout. Keep local edits safe.
2. Run `python VERIFY_UI97_UPDATE.py --repo /path/to/wavelink --mode before`. Reconcile a newer or edited checkout before proceeding.
3. Merge the contents of `COPY_TO_REPOSITORY` into the verified UI96 checkout.
4. Run the verifier with `--mode after`, then review, commit and push using the usual workflow.
5. After deployment, inspect sign-in and recovery at the intended company HTTPS address. With an authorised test account whose company email was already verified, confirm code arrival, wrong-code correction, expiry, successful reset, old-session refusal and normal MFA sign-in. Keep local unsent work and avoid fixture imports, storage clearing or repeated setup.

Docker keeps the original UI92 vendor/extractor and UI93–UI96 companions, then applies pinned UI97 once. Dependencies, hosting configuration, artwork and alert/document-import behavior are retained. No remote commit, PR or deployment was performed; integration writes previously returned 403. Exact executed local results and limitations are in `UI97_REVIEW_REPORT.json` and `DELIVERY_CHECKS.json`. Historical release reports remain historical. The security flow was checked against the [OWASP password-recovery guidance](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).

Local tests use fictional temporary databases and captured mail. Browser tests use Chromium, TestClient endpoints and emulated viewports; operational shell tests suppress timers/WebSockets and simulate persistence. Live SMTP inbox delivery, actual Docker/Render deployment, service-worker lifecycle, physical device/autofill/keyboard behavior, Windows/native setup and production networking are not claimed. The historical UI83 version-specific static contract is deselected; an exact UI63 upgrade fixture is unavailable and skipped. Full historical-suite acceptance is not claimed.
