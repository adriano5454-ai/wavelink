# Current continuation checkpoint — UI96

Repository: adriano5454-ai/wavelink. Current baseline main `dd8eff975a594e41b10bf5e589577bcf4e954cee` contains UI95; all 258 tracked Git blob hashes match the prepared UI95 repository. Current candidate: UI96 clear, responsive sign-in. Core 1.34.19.

User scope: modernise the outdated login page and remove confusing 01/02 numbering. Implemented coherent account, existing legacy-code, MFA and first-administrator setup screens; approved offshore artwork on desktop and form-first phone layout; clear help, password reveal and submitting/error states. Corrected a reproduced MFA transport bug: the journal now excludes the exact sign-in verification endpoint, allowing it before an account scope exists; other writes remain guarded. Existing approved-email/User ID auth, MFA and saved-work ownership checks remain. Ordinary healthy sign-in status is quiet; real warnings/recovery stay available.

Authoritative build: unchanged vendor/extract_source.py -> UI92 -> unchanged apply_ui93.py -> unchanged apply_ui94.py -> unchanged apply_ui95.py -> new pinned apply_ui96.py once. No auth/backend/schema change, reset, storage clearing, operational write, permission grant or artwork rewrite. Email/document import behavior and previous Toolbox/header/account fixes are retained.

Use only the current UI95-to-UI96 compact source ZIP against the verified UI95 checkout. Read WORKSPACE_UI96.md. Final exact hashes/results are in DEPLOYMENT_FILES.json, DELIVERY_CHECKS.json, UI96_SOURCE_PROVENANCE.json and UI96_REVIEW_REPORT.json. Bulky screenshots/logs remain separate. This is the single current checkpoint; retained prior release documents are historical.

No remote commit, PR or deployment. GitHub read worked; earlier integration writes returned 403. Next: usual commit/push/deployment, then actual company-address sign-in and physical-device/autofill/keyboard acceptance. Previous pending deployment, native Windows, service-worker lifecycle, real network and inbox/OCR-language acceptance remains separate. Optional email remains off unless deliberately enabled. Do not repeat setup, import fixtures or clear browser storage to test this release.

Existing access-code hubs also avoid named-account-only profile/action background reads that previously signed them out immediately. Legacy Home uses the existing Workspace directory, personal profile/Team links require a named account, and operational permissions remain server-controlled.
