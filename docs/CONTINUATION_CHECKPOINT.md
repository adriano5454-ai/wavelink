# Wavelink continuation checkpoint — UI94

## Current prepared release

Core **1.34.19**; `workspace-ui94-quiet-header-anchored-profile-2026-10-04`. Exact repository parent is verified UI92 / GitHub main `ba27ddeee79fd77579beecb02d601ec09443b8dc`; UI93 is included. Docker runs the unchanged UI92 extractor, UI93 companion once, then UI94 companion once. One authoritative visual asset is visual_system_ui94.css. UI94 makes no additional database change; UI93's additive personal mail tables and company-only explicit opt-in remain.

GitHub read access worked; writes were denied by the integration with 403. No remote branch, commit, pull request, hosting configuration or deployment was made. Compact changes and separate evidence are the delivery fallback.

## Implemented

Optional verified per-user email/categories/quiet hours from UI93. Quieter single-row header; persistent badge without three-line summary; one action bell/count; role/progress/healthy connection details in Account. Account menu anchored to its button and constrained to viewport, with resize/scroll support, keyboard Escape/focus return and preserved existing actions. Current offline/saving warnings and actual unsaved work remain reviewable. Responsive Home/Profile banner improvements prevent narrow tablet copy and collapsed profile headings. Both approved cover images and all thirty badges remain byte-identical.

## Preserve

Company C01 / M01 / G01 separation, persistent disk/database, company identity/logo, named administrator access, exact verified membership state, MFA/session rules, existing permissions, source identities, signatures, audit, daily handover continuation and assigned shifts, task chooser and inventory verification. Keep the sidebar, primary actions, approved artwork and permanent badge. Help opens in a separate tab. Report Branding remains report/export-only. Keep DEMO_PUBLIC_ENTRY=YES and INITIALISE_FICTIONAL_DEMO=NO on the demo. Do not reset, import fixtures, repeat setup or clear browser storage.

## Verification boundary

See UI94_REVIEW_REPORT.json and DELIVERY_CHECKS.json. Current UI94 browser/overlay/mail regression checks are reported separately from inherited UI93 evidence; counts overlap. Main banners and controls were reviewed at five widths; header/menu at fourteen widths. Fictional projects, in-process API bridge, emulated widths and suppressed timers. Actual inbox/deployment/device/native GUI/service-worker update acceptance remains separate. Previous broad tests contain eleven historical assertions that also fail on unchanged UI92, plus the superseded M01 byte hash; they are not represented as a green full suite.

## Next grouped work

Complete hosted UI94 visual/account/mail acceptance, then address concrete regressions. Continue the retained Tasks/Maintenance inspectors, unified forms/source evidence, phone ergonomics, broader operations/fault/HSE workflows, QR invitations and company administration. English/Portuguese localisation follows visual stability. Unconfirmed mail review/resend tooling remains separate; do not silently retry uncertain submissions.
