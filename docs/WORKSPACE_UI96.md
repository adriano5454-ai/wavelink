# Wavelink UI96 — Clear, responsive sign-in

Built on GitHub main `dd8eff975a594e41b10bf5e589577bcf4e954cee` (UI95), verified against all 258 tracked file Git blob hashes. Core 1.34.19.

The entrance now has a focused sign-in card, a quiet desktop panel using the approved offshore photograph, and a form-first phone layout. The unexplained `01 / 02` and `02 / 02` counters are removed. Company identity comes from the existing public workspace information. Account help expands when requested, and Membership status remains a separate link.

Password and existing legacy access-code forms have accessible Show/Hide controls, appropriate autofill hints, visible submission feedback, duplicate-submit prevention and inline errors that receive focus. Authenticator and recovery codes have distinct labels, input lengths and keyboard hints; changing methods clears the previous code. Verification can return to sign-in. A hub awaiting its first administrator has a matching setup screen and an explicit status recheck.

A healthy sign-in page no longer needs the large routine save-status strip. Connection & saves is still directly available below the form, and Workspace options retains installation/help tools. Offline, uncertain, pending-save, storage and workspace-mismatch warnings remain visible. Saved-work ownership checks and recovery export remain active. The shared save journal now recognises the exact `/api/login/mfa` endpoint as sign-in: previously it blocked verification because no operational account scope existed yet. Other write paths retain their normal guards. These screens use the existing authentication endpoints and permissions; there is no new reset-email service or third-party login provider.

## Apply the compact update

1. Extract the UI95-to-UI96 source ZIP outside your checkout and keep existing changes safe.
2. Run its `VERIFY_UI96_UPDATE.py --repo /path/to/wavelink --mode before`. Reconcile a newer or locally edited checkout before applying.
3. Merge the contents of `COPY_TO_REPOSITORY` into your verified UI95 checkout.
4. Run the verifier with `--mode after`, then review, commit and push using your usual workflow.
5. After deployment, check the entrance and normal sign-in on the intended company address.

The build keeps the existing UI92 vendor/extractor and UI93/UI94/UI95 companions, then applies the pinned UI96 companion once. Original artwork, email preferences, document imports, Toolbox repair, authenticated layouts, backend auth and database schema are retained. No fixtures, data reset, setup repetition, storage clearing or new hosting variables are needed.

## Acceptance

- At desktop, tablet and phone widths, inspect the company name, field labels, button, expandable help and membership link. Check a long company name and a short landscape viewport.
- Confirm User ID and approved verified-email sign-in, a rejected password, Show/Hide, keyboard submission and loading feedback. Use your own account.
- If two-step verification is enabled, test your authenticator code, a wrong code followed by retry, and one unused recovery code. Recovery codes work only once. An expired sign-in challenge requires a fresh sign-in.
- Verify an existing local draft is preserved through sign-out and same-account sign-in; another account must not adopt it. Keep a recovery copy where required.
- Disconnect and inspect the warning; Connection & saves must remain usable. Check normal navigation, profile/menu alignment and imports after sign-in.

Local evidence covers the current sign-in states, real auth APIs in fictional temporary projects, emulated widths, saved-work guards and current authenticated-route regression checks. Timers/WebSockets and persistence are simulated in the browser harness. This does not establish live hosting, actual service-worker updates, physical phone keyboards/autofill, Windows/native setup, production network behavior or inbox delivery. Full historical-suite acceptance is not claimed. Exact executed results and limits are in `UI96_REVIEW_REPORT.json` and `DELIVERY_CHECKS.json`.

GitHub main was read successfully; no remote commit, pull request or deployment was performed for this update. The earlier integration write attempt returned 403, so the source ZIP follows the established apply/commit/push workflow. Screenshots and logs are supplied separately from the compact source package.

Existing access-code hubs also avoid named-account-only profile/action background reads that previously signed them out immediately. Legacy Home uses the existing Workspace directory, personal profile/Team links require a named account, and operational permissions remain server-controlled.
