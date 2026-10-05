# Wavelink UI99 — Normal tabs and Back navigation

Prepared from exact GitHub main `80e9090500c33e80c97bcf2296c84d4772870e19` (UI98). All 273 parent repository blob hashes match. Core remains 1.34.19. UI98 company/demo recovery routing and the existing email, account, permission and operational backends are retained.

## What changes

The screenshot was a local draft-store lock, not evidence of a second login. Previously every ordinary page wrote the same IndexedDB `main` record and held one origin-wide lease. Another tab or an unreleased navigation lease could replace the entire application with “Waiting for the other Dive Check tab.” The old behavior was reproduced with real browser IndexedDB before this correction.

Normal tabs now have independent state, drafts, checklist queues, cached records, save receipts and project archives in the existing database/store/version. A tab handle survives Back and Reload. A live Web Lock protects its exact saved workspace; copied sessionStorage or a second opening of that workspace forks to a fresh empty workspace. With exclusive proof, an abandoned managed lease can be recovered immediately. Without Web Locks the guarded lease remains, and a competing page forks instead of blocking the whole app. The original `main`, lease and project archives remain readable; an old-version page never has its lease stolen. No draft or queue is copied to a second writer.

New empty tabs reuse the latest shared account session only after a successful live `/api/me` validation. Seeds contain account/session information, not draft payloads, queues, receipts or cached private records. Unverified seeds are marked pending on disk and fail closed if the API is unavailable, including after reload. A failed connectivity check does not clear another tab’s shared sign-in. Existing saved workspaces retain their established offline recovery behavior. Actual server logout and password-reset revocation still invalidate sessions. A stale tab’s local sign-out cannot clear a different tab’s newer token. Existing account-adoption/unsent-work guards remain byte-for-byte unchanged.

Saved server records remain shared. New local receipts are checked atomically against other tabs’ pending/uncertain receipts for the same account and target before a write can be sent. That warning blocks the matching action; navigation and different-record saves continue. Reviewing the original receipt releases the guard and does not claim the server saved anything. Existing operation IDs, server versions, conflicts and permission checks remain. There is no automatic draft merge or new server synchronization protocol.

Open **Workspace options → Connection & saves → Other tabs & saved drafts**, or the corresponding device-tools entry in Workspace tools. The panel lists only the current account/company workspaces and offers reopening of closed tabs and the original workspace. If that exact workspace is still open, the new page starts separately and leaves its drafts with the original writer. Counts cover drafts, queued changes and unresolved receipts. Each tab’s existing recovery export remains available. Explicit separate-log windows retain their existing database and one-use session handoff; opening the same saved detached log twice still protects its single writer.

Only already durable local forms/queues can be restored. Unsubmitted memory-only Fleet/admin/dialog forms still need saving or preserving before closing. The change does not turn every form into an offline queue or claim every save succeeded. Genuine quota/storage failures still stop editing/sending, retain the last saved bytes and expose recovery.

## Apply and accept

1. Extract the UI98-to-UI99 compact ZIP outside the checkout and preserve local changes.
2. Run `python VERIFY_UI99_UPDATE.py --repo /path/to/wavelink --mode before`. Reconcile a newer/edited checkout first.
3. Merge the contents of COPY_TO_REPOSITORY into the exact UI98 checkout. Run the verifier with `--mode after`, then review, commit, push and redeploy normally.
4. Sign in, open a second normal tab and navigate both. Open Help in the first tab, use Back, then Reload. Both should remain usable without the origin-wide tab warning.
5. Save a local draft in each tab, close one, and reopen its saved entry through Other tabs & saved drafts. Check that each draft stays in its own tab and the original workspace is discoverable. Do not clear site data.
6. Check ordinary saves and sign-out. A same-record uncertain result must point to review in the original tab; unrelated work remains usable. Confirm the main shell’s new worker/assets are active on the real deployment, including an installed/offline browser if used.

No new Render settings, SMTP permissions, setup repetition, fixture import, server-schema migration, project reset or browser-storage clearing is required. Docker applies apply_ui99.py once after the pinned UI97 runtime; UI98 had no runtime overlay, so its two hosted routing files remain in place. Seven runtime overlay resources change/add (including patch metadata), with 2103 final manifest entries. All 72 existing art/icon files and all non-browser operational/authentication runtime resources retain their bytes.

## Evidence and remaining acceptance

See UI99_REVIEW_REPORT.json and DELIVERY_CHECKS.json for exact final counts and limits. The new browser harness uses real shared-origin IndexedDB, Web Locks, sessionStorage and browser history with actual C01 hosted/core API responses in a temporary fictional company. WebSockets and worker registration are suppressed in that harness; real service-worker lifecycle, BFCache engine caching, physical devices, live Render/Nginx/SMTP and native Windows acceptance are not claimed. Retained sign-in/MFA layout tests use their established simulated-persistence harness. The selected functional suite includes retained password-recovery, account-security and save-delivery tests plus hosted UI98 guards and exact cumulative replay/tamper rejection.

One historical UI63 fixture is unavailable and its corresponding test skips. Four old static contracts still expect UI83/unversioned worker naming, a historical Fleet CSS URL or 1.26-era account bytes; the same assertions are already incompatible with UI98. They are deselected in the current selected suite. Current UI99 asset ordering/caching and unchanged UI98 account/backend bytes have dedicated build checks. This is not a full historical-suite or live-deployment claim.

No remote commit/PR/deployment was performed. Earlier integration writes returned 403; use the usual compact-update workflow. The single current checkpoint is CONTINUATION_CHECKPOINT.md; historical guides and the wider roadmap remain.
