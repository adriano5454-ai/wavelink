# Wavelink UI53 — Inventory & boxes, scope and verification workflow

**Core 1.34.19 · UI53 · Company C01 and demo G01 retained · 27 September 2026.**
One grouped update on the exact UI52 repository, resuming the approved UI51 Inventory review.
The optional-handover-notes fix in UI52 is preserved. This is a changed-files package, not a
complete repository, live-company backup, database or deployed service.

## Update using GitHub Desktop

Extract the ZIP and copy **everything inside UPLOAD_TO_GITHUB into your existing UI52 Wavelink
application repository folder**, accepting replacement of matching filenames. Review the changes
in GitHub Desktop, commit and Push origin. Do not replace the whole repository, delete files
absent from the patch or copy it into Wavelink-Website. The CHECK_UI53_UPDATE.ps1 file is an
optional read-only checker, not an installer or required extra upload.

Both services may deploy the same branch: check the demo and Sulmara auto-deploy settings before
pushing. Preserve your backup, approved commit, independent edits and unsent main/separate-log work.
Keep activated Sulmara COMPANY/C01 identity/domain/dedicated disk/marker, INITIALISE_COMPANY=NO and
removed bootstrap secrets. Keep the independent G01 demo settings, credentials and disk unchanged.
No new environment settings, dependencies, permissions, routes, SQL tables or migrations. Do not
reset, repeat setup, import demo data, clear site storage or disable synchronisation.

## Create, import and find equipment

Inventory now offers **Create inventory · Import existing · Open inventory** using the same existing
Inventory Builder and underlying permissions as Setup & builders. A permissioned Technician or
Supervisor can use the actual builder/importer without administrator authority. The importer checks
supported .ajinventory packages and creates new identities, not custody or verification history.
Category definitions, archive and native advanced transfer controls retain separate authorities.

Same-account catalogue search survives a real count change. The box explorer keeps folder/all-level
views, parent/back navigation, source/category/location/department filters, desktop table, phone
cards, selection inspector and Shift/Ctrl selection. Ordinary changed-item refreshes reuse unaffected
rows and preserve expanded More tools and reading position where the anchor remains. Some structural
changes still rebuild the shell. Existing polls pause while rows are selected or a form is active;
this is not a continuously live view during an operation. Current versions are rechecked on save.

Selection remains limited to visible results. Filtering away a selected root removes that selection
with a visible notice, without deleting or moving anything. Included record counts are not quantity
sums, physical checks or confirmation that all contents were found.

## One-page item entry, full equipment model retained

**Add item / box** puts name, quantity/unit, asset reference and serial first, with optional details,
custom/source fields and storage/owning department below. **Add item / box** or **Save item changes**
saves directly, without the old four-page wizard or routine confirmation checkbox. Model/type,
pairing, onboard/offloaded dates, custom fields, notes, source warnings and unknown quantities remain.
Unavailable restored references are displayed and remain subject to current service validation.

Routine descriptive edits need no generic reason. The existing actor/time/version/before-after audit
is retained. The existing service's inventory.move checks still govern storage/department changes;
boxes use **Move location / Put in box / Take out** so included contents move atomically. Exact scope,
destination, quantity splitting, movement explanations, stale-version checks and Fleet holds remain.
An inventory location/owning department is not vessel custody or a private audience.

Ordinary item and result forms retain **Keep draft & close**, Saved forms, original versions and the
existing retry/cleanup writer. Delayed History cannot replace a newer editor, including an intervening
editor that has already closed. The originating account/form is checked again before sending after
the asynchronous lease wait. No earlier form may submit under a replacement account.

## Exact stock-verification scope

**Verify stock** is directly visible in Inventory. Choose all active records within a location or
department, selected records only, selected records with nested contents, or selected boxes only.

**Selected boxes only** now visibly excludes selected ordinary records, lists the exclusions and saves
only the reviewed boxes. The server rejects a client still submitting mixed box-only selections.
With contents includes each descendant once. **Show exact scope** lists the identities and quantities.
**Refresh scope preview** deliberately reads them again. An added/edited/archived record that changes
the reviewed scope causes a conflict rather than silently creating a different verification.

Creation freezes the scope; later additions do not join it. Previously saved scopes are not rewritten by this update. Every box/item starts unrecorded. The setup
form is memory-only until created, not a new durable draft; close warns before discarding a named setup.
An uncertain response keeps **Retry same creation** and its exact payload. Check saved verifications
before starting another after closing an uncertain request.

## Consistent results and deliberate closure

The desktop table and phone result cards show identity, recorded location, expected/count quantity,
outcome, author/time and **Record result**. **Still to record · Recorded · Missing / discrepancy · All
scoped records** and search affect the view, not the required scope. A box's contents need separate
checks. Required quantities and substantive Missing/Discrepancy notes stay enforced.

Your own continuous, non-movement result history in an open standalone stock verification can be
corrected without a generic reason. The writer proves that history again inside the transaction.
Reset, other-author, unknown or movement history is not guessed to be routine. Private Task
verification keeps its existing distinct unsubmitted-result policy and permissions. A genuine typed
movement explanation is reused for the same-author correction when moving and checking together;
there is no invented explanation. Other-author corrections retain their explanation field.

**Review & close** retrieves the same saved version, shows remaining/recheck counts and actual unresolved
outcomes, then asks for the meaningful closing note. When Missing/Discrepancy results remain, one
initially unchecked acceptance identifies those exact outcomes. **Close reviewed verification** is
one explicit action, not the previous two generic prompts. A changed count must be refreshed first.
All scoped results must be current to close. **Cancel verification** remains a separate explained
outcome for unfinished work. Lost-response closure retries use the identical operation/payload.

Closing freezes evidence; it never makes Missing items Found, adjusts inventory quantities or releases
equipment. Closed reports retain close-time records even after later equipment changes. The closing
note form is in-tab only until saved; leaving edited/uncertain wording gives a warning.

## Refresh, supporting tools and reports

Unchanged cards and ordinary real item/result changes preserve unrelated keyed content and controls.
A temporary failure labels the last saved view and blocks stale record actions until refreshed.
A definitive access denial clears protected inventory behind any open form, without deleting its
local draft or forcibly replacing its typed text. Permission/version checks still govern any later save.
This addresses the reviewed Inventory paths, not every possible live update across the application.

Profiles/photos, low-stock rules, linked maintenance/certificates/private Tasks, categories, QR lookup,
A4/70x40 labels, movement/split tools, history and stock PDFs remain. **Export CSV · all records**
explicitly exports active and archived records, not the current search selection. Stock PDFs cover
the complete fixed verification. Neither labels nor scanning verify equipment, grant access or replace
a complete company backup. Reports/QR renderer code, custody services, UI52 handovers and approved
Home/Tasks/Checklists/Logs/Calendar layouts and operational writers are unchanged apart from shared
asset-cache references and the limited shared inventory form/read guards.

## One acceptance session

Use fictional data and named accounts. Create/import an inventory, add a box, nested case, tagged
sensor and loose stock. Check the existing reviewed kit move and permitted quantity split. Select a
box and an ordinary item, choose Boxes only and verify its actual saved scope. Record one Missing
outcome, review it and deliberately accept closure; export the PDF. While editing an item, verify
History cannot replace it; check a genuine item update with More tools expanded. Include phone use
in the same session. Never test discard or revocation on valuable unsent work.

## Verification and limits

**511 selected Python tests, 27 compound browser checks and 78 JavaScript syntax checks passed.** All 193 application Python modules parse; 1841 tracked runtime files verified. Python groups: inventory_py=133, tasks_py=73, preserved_py=127, hosting_py=178. Browser groups: inventory_browser=20, handover_browser=7. Thirteen Node scope assertions run within one Python test and are not additional Python cases. Stock PDF, CSV and two label sizes were generated through existing authenticated services; rendered stock/label examples were inspected. These are selected checks, not a full-suite result.

One inherited UI47 test assumed standalone own-result reasons would always remain mandatory. Its
expectation was intentionally updated for the approved UI53 policy, retaining original actor/version/
audit checks and adding a different-author client-flag refusal. The affected complete Tasks group and
package checks were rerun; other completed groups used byte-identical application and relevant tests.
Earlier partial runs, a protected-selection polling fixture, normal-navigation harness restriction and
native/historical contract attempts remain separately recorded, excluded from the passing totals.

Actual assets and fictional SQLite/TestClient data, simulated hash routing, injected fetch and staged
in-memory transactions were used. Not full-suite, live Sulmara/GitHub/Render, real camera/printer,
durable IndexedDB/service-worker, physical phone, Windows/PowerShell/native, full security/accessibility/
load, Docker or accepted off-host recovery validation. No real company accounts, credentials or records
were inspected. Native installers and master guides were not rebuilt. Four hosted Help bodies/outlines
were updated and all 76 catalogue entries match; 72 article bodies are unchanged.

Use UI52-compatible or later company/evidence software for source recovery; don't downgrade to
incompatible pre-C01/pre-UI34 writers or roll a database back for an interface change. Deliberately
discarded local work is not recoverable by source rollback. No reset/reimport/site-data clearing.

**Nothing has been pushed or deployed from here.** Check the Inventory workflow, then continue the
agreed section-by-section review/build cycle. The wider roadmap remains in DEVELOPMENT_TODO.
