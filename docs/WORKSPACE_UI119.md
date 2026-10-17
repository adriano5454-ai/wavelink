# UI119 — Corcovado password minimum

Built on main 7cb37e6d6c1a997438e87d62e41f97439ea56514, retaining UI117 HR and UI118 Portuguese.

The deployment owner requested a minimum of eight characters for Corcovado. The validated COMPANY child environment selects this policy only for COMPANY_ID=corcovado. Browser hostnames, request fields and persisted user input cannot select it. Other deployments keep their previous thresholds (14 for membership/recovery, 6 for legacy account changes).

Invitation acceptance, verified-email recovery, ordinary account changes/admin resets and first-company activation now use the shared server policy. The browser receives the same public limits in its existing uncached locale bootstrap. Authentication of existing passwords is unchanged; this release performs no data reset, password rewrite, user deletion or mail delivery.

The maximum of 128 characters, six-distinct-character checks in invitation/recovery/setup, mailbox proofs, expiry, rate limits, hashing, MFA and session revocation remain in place. Portuguese hints and relevant asset cache versions are updated.

## Build

Apply the existing Docker build through UI118, then deploy/apply_ui119.py. It requires the exact UI118 manifest and refuses any changed parent file before writing. deploy/build_ui119_overlay.py reproduces the frozen overlay from verified parent/target runtime folders. UI119_SOURCE_PROVENANCE.json lists every changed file and digest.

## Verification

Local tests use fictional accounts and captured mail, never a real mailbox. tests/test_password_policy_ui119.py covers 7/8-character boundaries in invitation, recovery, own change and admin reset; other-deployment isolation; 128-character/diversity limits; session revocation; and Portuguese/bootstrap policy values. Existing membership/recovery regression tests are run alongside it. The release is also checked by replaying the overlay against verified UI118, rejecting a simulated newer HR edit before writes and comparing every resulting resource hash.

## Rollback

Revert this commit and redeploy the existing service. No persistent data conversion is required. Passwords already created with 8–13 characters continue to authenticate; the earlier stricter threshold applies to subsequent changes. Account cleanup and real mailbox activation/recovery are separate operator actions with their own backup and evidence.
