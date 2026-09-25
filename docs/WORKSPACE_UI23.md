# UI23 implementation boundary

## Presentation-only note editor

The new app/static/handover_notes.js owns the Work & priorities view, not the
handover controller, SQL or action writer. Sections come from the existing directory
and retain its order and names. Plain text stays in the same editor.work properties.
Only explicit input calls the existing changed() handler. Section selection,
reference reads and view clearing do not change dirty state, audience, consent,
periods or an operation ID.

The opened baseline is a clone of the private draft already returned for this form.
It is not a fresh server check. A new draft has no opened saved comparison. Counts
are text-presence indicators, never a completion score. The maximum/count uses the
existing browser UTF-16 maxlength convention and does not truncate existing values.

Only shell (badge), paint (notes view) and lock (note-control sync) change in
handovers.js. Its other 47 top-level functions, including save, saveDaily,
savePreparation, startReview, changed, close and handleError remain byte-identical.
All181 application Python modules, endpoint/payload/permission/storage definitions
and the separately deployed G01 gateway remain unchanged.

## Exact author-selected earlier publication

Only daily_previous saved provenance supplies the source ID/revision. No title
matching, most-recent-publication inference or fake predecessor. The separate
multi-source preparation workflow is not redesigned by this increment.

An explicit read delegates through the existing authorised api helper to
GET /api/handovers/{id}?revision=N. The pure sourceIdentity/referenceShape helpers
check canonical ID, positive integer revision, matching top-level/publication
identity and revision, active (not archived) state and required typed publication
fields. The output is a whitelist of publication notes/identity/period metadata.
Returned draft, audience and other controller fields are never copied into the
reference snapshot. A newer current publication is permitted to coexist, but never
substitutes for the pinned revision. An invalid source identity is refused before
a request is made.

The server remains authoritative for current and historical audience access.
The view is a retrieved snapshot, not continuous permission monitoring or live
equipment status. Refresh/hide/tab disposal clears it. If access is withdrawn,
the saved independent current-shift copy is not retroactively erased.

## Lifecycle guards

Ownership checks tie the module to editor identity, scope including token/user/hub,
exact route, pane/workspace elements and Work tab. Read epoch invalidates delayed
replies after hide/new read/dispose. Modal visibility and busy/uncertain/conflict
state gate request and reply acceptance. Notes are editable while a read is pending;
a save can proceed independently, but a late reference cannot repopulate closed UI.

An initial bug latched disabled controls when a reply was interrupted by a modal.
Persistent disabled state is now only ownership/save/uncertainty/conflict based;
modal checks remain in event/response acceptance, so closing a modal permits an
explicit new reference read without automatic retry or lost notes. Its failing
test run is retained separately.

No source cache, browser storage or offline queue is added. References contain
only in-tab text. Close/reload cannot reconstruct unsaved notes. Existing receipts,
hub saving, unknown-outcome retry and conflict protections remain unchanged.

## Verification and deployment

See DELIVERY_CHECKS.json, UI23_SOURCE_PROVENANCE.json and the small patch manifest.
Full selected tests run on a fresh extraction with complete runtime hash checks.
Browser tests use controlled local transport/storage; live deployment is separate.
The exact UI22+G01 baseline is required. No env/migration/dependency/deletion changes.
Keep fictional demo data, public-entry non-admin boundary and initialization OFF.

General Help/native/PDF/recovery/security acceptance remains separate work.
