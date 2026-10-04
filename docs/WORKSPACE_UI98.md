# Wavelink UI98 — Hosted recovery routing correction

Prepared against exact GitHub main `c1c7151fdce67dc6ab76836c9463480298194af3` (UI97), verified across all 268 tracked Git blob hashes. Core 1.34.19; all 2102 UI97 runtime resources and its release manifest retain their exact bytes. This is a deployment-boundary correction, with no additional runtime overlay, schema or data migration.

## Cause and correction

The supplied screenshot's recovery page loaded, but its initial information request failed. A local reproduction using the actual hosted company factory returned 200 for the page and 401 for recovery info/request/reset, with `Sign in with your company account.` The C01 outer gateway demanded a normal session even though recovery must happen before sign-in. The UI97 core and browser tests exercised the inner application and missed that outer boundary.

CompanyAccess now admits only these exact public authentication method/path pairs after first-company activation: GET /api/info, POST /api/login, POST /api/login/mfa, and the recovery service's GET info, POST request and POST reset routes. Membership entry and document-signing retain their existing narrow credentials. Unrelated operational/security APIs, path suffixes and wrong methods still require a valid named company session. Pending first-administrator activation remains closed; no recovery or MFA request can bypass setup. Exact host, proxy/TLS, origin, hub, code/expiry/attempt, JSON/body and account eligibility checks remain at their existing layers.

The demo has a separate admission gate. The recovery client intentionally omits ordinary cookies, so its fetch would also be refused there. Nginx now passes only the three exact recovery API methods to the core independently of demo admission, preserving the canonical host/TLS checks and header whitelist and adding a 4 KiB body cap. There is no public API prefix bypass. Ordinary demo page/application/API admission and guest behavior remain. Demo mail remains disabled; recovery can honestly display unavailable mail/admin assistance. This correction does not enable invitations or SMTP on a demo.

With configured company mail, the recovery form now opens before sign-in and can request/redeem its verified-email code. With unconfigured mail it shows administrator assistance instead of treating a gateway 401 as a lost connection. Existing UI97 session revocation, MFA retention, idempotent reset retries and recovery safeguards are unchanged.

## Apply

1. Extract the UI97-to-UI98 ZIP outside the checkout and keep local changes safe.
2. Run `python VERIFY_UI98_UPDATE.py --repo /path/to/wavelink --mode before`. Reconcile a newer or edited checkout first.
3. Merge the contents of COPY_TO_REPOSITORY into the exact UI97 checkout; do not copy its wrapper directory into GitHub.
4. Run the verifier with `--mode after`, then review, commit and push through the usual workflow. Redeploy the existing service normally so it uses the corrected gateway modules/configuration.
5. Open Forgot password at the intended company HTTPS address. Expect either the email/User ID form or clear email-not-configured assistance. With an authorised account and configured company SMTP, confirm code arrival and normal MFA sign-in after reset.

No environment change, setup repetition, fixture import, project reset, browser-storage clearing or source-vendor replacement is required. UI97's existing company SMTP and verified company-account email requirements remain; optional alert opt-out stays independent. See WORKSPACE_UI97.md for the retained recovery policy/mail configuration.

## Validation and limits

210 selected tests pass: 30 new hosted authentication/boundary/configuration cases and 180 retained C01, M01, private-demo and G01 public-guest cases. Tests use the real HostedBoundary, CompanyAccess, core runtime, fictional prepared company storage and captured mail. Actual MFA challenge completion works before a normal session, anonymous recovery completes, old sessions stop working, and unrelated APIs remain closed. Browser recovery request/code/success and unconfigured states pass 15 checks at 1440, 390 and 320 px through that actual company middleware. Screenshots were visually inspected. All core/UI97 runtime bytes are unchanged and the four new/changed Python source files parse.

Nginx configuration generation/exact location guards are tested; an Nginx binary is not available here, so an actual Nginx listener/syntax run is not claimed. No live company service, real SMTP inbox delivery, Render/Docker deployment, service-worker update, physical device or Windows/native setup was exercised. Historical UI97 proofs remain historical, not a new full-app run. Current results are in UI98_REVIEW_REPORT.json and DELIVERY_CHECKS.json; bulky screenshots/logs are separate.

GitHub main was read successfully and the exact UI97 source verified. This correction was not remotely committed, merged or deployed. Integration writes previously returned 403, so delivery follows the established compact apply/commit/push workflow.
