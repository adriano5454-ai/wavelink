# Wavelink UI93 — Optional email alerts and account layout

Core **1.34.19**, based on verified UI92 / GitHub main `ba27ddeee79fd77579beecb02d601ec09443b8dc`.

## User settings

Open **Account & security → Email alerts** (also available through the new Email alerts shortcut). Email starts **off for every user**. Choose your categories, optionally use the notification quiet hours, and save. Turning email off preserves in-app alerts and all assigned work.

Approved members use their verified company membership mailbox. Existing User ID accounts can verify an alert-only address using their current password and a six-digit email code. This does not change sign-in or enable alerts automatically. Changing that alert-only mailbox turns email off until the user enables it again.

Summaries cover the existing authorised work and attention categories: Tasks, Maintenance, Checklists, Handovers, Toolbox Talks, Logs, Inventory (including low stock), Certificates, Fault Reports, HSE/QSHE, Receiving and Membership. The first summary includes current unread alerts; subsequent summaries cover new or changed alert identities. Complete email projections page through assignments and include all eligible date/stock/acknowledgement attention items, rather than only the Home preview. Read/dismissed or no-longer-authorised items are excluded. Main account settings remain for named project accounts; Fleet-only accounts retain their existing restricted portal.

Email contains category counts and a company workspace link. Record titles, private notes, attachments, sign-in tokens and operational documents remain in the app. Email never approves, signs, acknowledges, completes or grants access to a record.

## Company service activation

After deploying UI93, set **`WAVELINK_ALERT_EMAIL=ON`** on the intended **COMPANY** service. Leave it absent or `OFF` elsewhere. Reuse the existing complete M01 membership mail configuration (`WAVELINK_MEMBERSHIP_MODE=INVITE_ONLY` and the private `MEMBERSHIP_SMTP_*` values); do not put credentials in GitHub. This code does not edit hosting environment settings.

The company supervisor forwards only the new switch alongside its existing allowlisted identity/mail settings. The demo and Nginx child environments retain their existing isolation. The default local hub and public demo do not send alert email, even if a demo operator accidentally sets the switch.

A server-side scan runs approximately once a minute when mail is enabled and configured. Operational saves do not wait for SMTP. Quiet hours defer mail without claiming delivery. Before submission, the worker checks current user access, verified recipient, preferences, read state and source visibility again. Durable receipt claims prevent repeated sends across scans, concurrent workers and restarts. SMTP acceptance means the mail server accepted submission, not that the inbox received it. Unconfirmed/interrupted submissions are retained and never blindly retried; later new or changed alerts remain eligible. Review the displayed last-delivery status and the provider if delivery is unconfirmed.

## Layout and build

The account cards regain their missing grid, spacing, facts layout and responsive stacking. Email controls fit desktop/tablet/phone layouts and use the established colours. The single authoritative visual asset is now `visual_system_ui93.css` in the main app and Fleet; browser assets are versioned and precached for UI93. Help guidance for assignments, expiry and low stock now describes optional company email.

The original large UI92 extractor and pinned vendor source parts are unchanged. Docker copies the small `deploy/apply_ui93.py` companion and invokes it **once after** the existing verified UI92 extraction. The companion checks the exact UI92 manifest and all parent resources before writing, then verifies the derived UI93 manifest. Keep the companion and Docker change together.

The email schema upgrade only adds `email_alert_*` tables. Complete backups preserve preferences, verified mailboxes and delivery receipts. Selective workspace transfers clear personal mail state and retain its schema marker. Preserve normal backups; use UI93-compatible code with upgraded projects. No database reset, demo import, setup repetition or browser-storage clearing is required.

## One acceptance session

1. Deploy the reviewed UI93 commit to the intended company service and enable the operator switch.
2. Open Account & security, verify the intended test mailbox if required, choose Tasks and enable email.
3. Assign one fictional task to that user. Check inbox/spam after the next scan and follow its link using normal sign-in.
4. Leave the task unchanged: it must not create repeated emails. Turn email off, assign another fictional task, and confirm its in-app alert remains while email stays off.
5. Review account cards on desktop and phone; revisit Certificates, Original Files and Fleet. Use a temporary test account/data for acceptance.

Local evidence: 1,083 broad selected checks passed; two harness-path failures passed on corrected rerun. Eleven historical source assertions also fail on unchanged UI92. The legacy exact M01 launcher hash assertion is intentionally superseded by the updated allowlist/process tests. Final focused checks: 237 passed; build/replay checks: 3 passed. Browser checks cover the main route matrix, navigation, Fleet, certificate races, equipment/work execution and email settings. See `UI93_REVIEW_REPORT.json` and `DELIVERY_CHECKS.json` for scope. No live deployment, real inbox delivery, actual mobile device, Windows GUI, full legacy suite pass or service-worker lifecycle acceptance is claimed.
