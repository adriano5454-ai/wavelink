# Wavelink UI94 — Quieter header and anchored account menu

Core **1.34.19**. Cumulative update from verified UI92 GitHub main `ba27ddeee79fd77579beecb02d601ec09443b8dc`, retaining the prepared UI93 email release.

The product bar now uses one compact row: navigation, Wavelink, search, the permanent selected badge, the action bell/count and account. Badge name/progress, role/department and ordinary connection details live in the account menu. Actual offline/saving-problem indicators and unsaved-work warnings remain visible. Search and My actions use their existing dialogs. On a narrow phone the product mark stands in for the wordmark; all controls retain accessible labels.

The account menu is positioned from the button's actual rectangle, rather than the header edge or the old second mobile row. It follows resize/scroll/visual-viewport changes, stays inside the screen and scrolls on short landscape screens. Escape closes it and returns focus. Outside clicks and route changes close it. Existing account, security, recovery, workspace and sign-out actions remain. Connection & saves opens the existing save panel.

The artwork review covers both approved Home/Profile images and all thirty badges. Their bytes are unchanged. Main banners were checked across seventeen routes and five widths; the header/menu were checked at fourteen widths from 320 to 1440 CSS pixels. Home uses the available tablet width, and Profile stacks identity/badge panels before the title becomes squeezed. Long names wrap within their banner; the profile title is sized to fit ordinary names naturally. This release adds no new operational schema or application dependency.

## Email retained from UI93

Users configure optional email in **Account & security → Email alerts**. It starts off for every user. After deployment, the intended COMPANY service needs `WAVELINK_ALERT_EMAIL=ON` and its existing private M01 membership/SMTP configuration. Approved membership recipients are reused; User ID accounts can verify an alert-only mailbox. Categories, quiet hours, current access/read-state checks and durable delivery claims are retained unchanged. Read WORKSPACE_UI93.md for activation and live mailbox acceptance. The demo stays off.

## Build and apply

The compact bundle accepts an exact UI92 checkout or the exact prepared UI93 checkout. Copy only the contents of COPY_TO_REPOSITORY into the existing application repository. Keep normal backups, existing company identity/logos, environment, disk/database, activation and demo settings. Do not reset projects, import fixtures, repeat setup or clear browser storage.

Docker runs the unchanged UI92 extractor, applies the pinned UI93 companion once, then the UI94 companion once. The latter checks every exact UI93 parent resource before writing. Both companions are included, so UI93 does not have to be installed as a separate update first.

## One acceptance session

1. Open Home, My profile, Team, Tasks, Certificates, Original Files and Administration on desktop, tablet and phone; compare banner alignment and readability.
2. Open the top-right account button. Its menu must appear beside the button. Resize or rotate, then close with Escape or an outside click.
3. Confirm the badge remains visible; open it to the profile. Confirm the action bell and search still open their existing dialogs.
4. Open Account → Connection & saves. Review a temporary fictional draft through the existing Unsaved work path; do not discard real work as part of testing.
5. For email, follow the single fictional-task inbox/optout session in WORKSPACE_UI93.md after enabling the intended company mail service.

## Review boundary

See UI94_REVIEW_REPORT.json and DELIVERY_CHECKS.json for final executed results. Evidence is a separate download. Chromium used fictional local projects, an in-process API bridge, suppressed browser timers and emulated viewport widths. No live deployment, real inbox, physical mobile device, Windows/native GUI or service-worker update lifecycle acceptance is claimed. The previous GitHub write attempt returned 403 integration permissions; no remote branch/commit/PR has been created.
