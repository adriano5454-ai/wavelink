# Wavelink continuation — after UI18

## Verified release boundary

Core stays 1.34.19; cumulative UI01–UI18. UI18 implements project-shared logical folders for the existing Originals library, exact-revision moves, administrator preview/confirmation and audit, snapshot/idempotency guards, selected-transfer preservation, and the fifth bounded Help wording review (originals). No original bytes or document-reference structures are rewritten. This release includes five changed/added application Python modules and three additive metadata tables; it is not static-only.

UI17 checklist approval/readiness/finalisation, UI16 result editor, UI15 asset creation/saved-evidence viewer, UI14 maintenance reviews and UI13 Home remain included. Native vessel/CCVD are outside scope.

## Next work in order

1. Record real hosted/user feedback for Home, inventory/boxes, maintenance, checklists and the new Originals library. Verify normal/guest/restricted roles, real devices, file downloads, saved folder changes and restart persistence. Preserve deployment and unsent work before any update.
2. Continue the Originals workflow with a separately reviewed browser upload/add-revision design and explicit destination at import. Reuse existing byte/type/size/identity/reference checks. Do not invent a revision-family move, upload permission, document ACL or ability to organise every attachment. New current imports start at the root; native folder-authoring is not implemented. Confirm how native/other attachment entry points should display the same metadata before widening scope.
3. Continue Help wording and entry-point review. Five distinct topics reviewed: daily, records, maintenance, dashboard, originals. Seventy-one remaining article bodies, the shared authoring pipeline, native Help, all-in-one/master PDF and complete accessibility acceptance remain pending. Preserve unrelated wording and identify hosted versus native paths accurately.
4. Continue lifecycle acceptance: durable local work and service-worker update with unfinished forms, offline/conflict recovery, independent browser/device concurrency, multi-device access revocation, and folder action lost-response handling. The new organisation form is online, memory-only, with no automatic queued retry; lost tabs require saved-history review. Local test cases are not broad security or isolation certification.
5. Validate overlay-compatible off-host recovery separately. The pristine helper remains unapproved. Do not weaken checksum/unknown-table checks. UI17 rollback hides folder metadata and may refuse older selected exports; do not delete tables to bypass that. Preserve complete backups and browser-only work independently. No vessel/cloud synchronisation.

## Continuity and packaging

Continue from verified full UI18 bytes; verify parent manifest and final extraction before editing. Include exact parent extractor rollback, readable runtime/diffs, old evidence history, new final and preliminary evidence separated, and updated checksum manifests. The deployment extractor remains the only changed existing executable upload file; app changes are embedded, not separate executable upload patches. Keep gateway/guest/supervisor/Docker/dependencies/vendor/seed/recovery unchanged unless a separately scoped update explicitly requires them.

Keep `https://demo.mywavelink.com`, current secrets and guest/disk settings, `INITIALISE_FICTIONAL_DEMO=NO`, removed initial-admin bootstrap, `.git` and outside changes. No reset, demonstration re-import, automatic categorisation, site-data clearing or background development. No live repository was fetched or deployed for UI18.
