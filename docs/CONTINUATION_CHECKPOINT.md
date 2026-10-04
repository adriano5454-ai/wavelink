# Wavelink continuation checkpoint — UI93

## Current prepared release

- Core **1.34.19**; `workspace-ui93-email-alerts-account-layout-2026-10-04`.
- Exact parent: all 243 UI92 repository files verified against the supplied ZIP and GitHub main `ba27ddeee79fd77579beecb02d601ec09443b8dc`.
- Parent extractor remains `57550f076fe6474523d77ecb9fc5b119c0a183f0f6a45be3361c61de0c381fc1`; vendor/source parts are unchanged.
- UI93 is applied by the pinned companion `deploy/apply_ui93.py` once after UI92 extraction in Docker.
- Runtime manifest: 2,084 tracked entries plus generated RELEASE_FILES.json. Parent manifest: `071e70c9b15d81fb0c0ffeea9c25cf2efb2eb8ff93679c0458cb9043e74e1525`.
- One authoritative visual asset: `app/static/visual_system_ui93.css` in the main app and Fleet.
- GitHub main was readable, but creating the review branch returned 403 Resource not accessible by integration. No remote branch, commit or pull request was created. A verified compact UI92-to-UI93 update bundle is the delivery fallback. Hosting configuration and live deployment remain separate actions. No live company data, credentials or inboxes were used.

## Implemented

Optional personal email alerts, category choices, notification quiet-hours integration, verified membership/alert-only mailbox routing, background scans and durable delivery claims. Email starts off; the COMPANY service also requires `WAVELINK_ALERT_EMAIL=ON` and its existing M01 mail settings. Read/dismissed and currently inaccessible sources are excluded. Complete projections include assignments beyond the first 50 and date/stock/acknowledgement attention beyond Home's previews. Operational writes remain independent of SMTP. Unconfirmed/interrupted mail is never automatically resent.

Account & security regains the card layout/facts/spacing omitted during earlier CSS consolidation and gets a visible Email alerts shortcut. Email controls and their mailbox verification flow are responsive. Three relevant Help articles now describe optional company email. Other UI92 list/detail, folder tree, route, badge and recovery behaviors remain intact.

## Preserve

Company C01 / M01 / G01 separation, persistent disk/database, company identity/logo, named administrator access, exact verified membership state, MFA/session rules, existing permissions, source identities, signatures, audit, daily handover continuation and assigned shifts, task chooser and inventory verification. Keep the sidebar, primary actions, approved artwork and permanent badge. Help opens in a separate tab. Report Branding remains report/export-only. Keep DEMO_PUBLIC_ENTRY=YES and INITIALISE_FICTIONAL_DEMO=NO on the demo. Do not reset, import fixtures, repeat setup or clear browser storage.

## Verified boundary

See UI93_REVIEW_REPORT.json. Broad selected review: 1,083 passed / 14 initial failures / 1 skip. Two initial failures were harness paths and pass with correct paths; eleven source assertions reproduce on the unmodified UI92 runtime; the final legacy launcher byte assertion is superseded by the deliberate new switch plus updated M01 tests. No historical assertion was rewritten to manufacture a pass. Final targeted run: 237 passed; companion build/replay checks: 3 passed; no candidate manifest mismatch. Browser main/Fleet/email/selection/navigation/equipment/work checks pass on fictional fixtures. Actual inbox, deployed service, devices, Windows and service-worker update lifecycle remain acceptance work.

## Next grouped work

First complete hosted UI93/mail acceptance with a mailbox the operator controls and address any actual regression. Then continue the UI92 roadmap: suitable Tasks/Maintenance record inspectors, unified forms/source evidence and phone ergonomics, while retaining all capabilities and actual unsaved editors. Keep wider operations, fault/HSE workflows, QR invitations, company administration and later English/Portuguese localisation in the retained DEVELOPMENT_TODO. Unconfirmed-delivery review/resend tooling may be a separate consequential-action batch; do not silently add automatic uncertain retries.
