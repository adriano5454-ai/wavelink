# Wavelink UI62 — Administration, logistics and company identity

**Core 1.34.19 · UI62 · Company C01 and demo G01 retained · 29 September 2026.**
One grouped implementation over the exact supplied UI61 repository, including the reported invisible
Company Branding form and small-logo save error. This is a changed-files source package, not a live
company backup, Windows installer or confirmation of the deployed version.

## Update through GitHub Desktop

Preserve the approved commit, independent source/configuration edits, complete backup and unsent
main/separate-log work. Extract and copy **everything inside UPLOAD_TO_GITHUB into the existing UI61
Wavelink application repository**, replacing matching files. Review in GitHub Desktop, commit and
Push origin. Keep the existing repository and .git; do not delete files absent from this package or
copy this into Wavelink-Website. The PowerShell checker is optional read-only checking, not an installer.

Copy the entire payload: this release includes **deploy/company_identities.json** and
**deploy/company_logos/README.md**, not only the application extractor. Future independently customised
company-identity entries and artwork must be reconciled, not overwritten by a default configuration.
Both the demo and Sulmara may auto-deploy the same branch; review their settings before pushing.

Keep activated Sulmara COMPANY/C01 identity, PUBLIC_URL, dedicated disk and activation marker,
INITIALISE_COMPANY=NO and removed bootstrap secrets. Keep the separate G01 demo settings and disk.
There are no new environment variables, database tables, dependencies or project-permission flags.
One explicitly selected Fleet account-mode value and one public selected-logo route are added.
No reset, re-import, browser-storage clearing, disabled sync or repeated company setup is required.
Save or deliberately keep open editors before reloading once after the intended deployment is healthy.

## A retained branding draft is not an invisible blocking form

The parent UI61 Company Branding module reported a form even after its page was left, because its
retained draft was treated as the visible editor. Fleet then refused entry despite no form on screen.
This was reproduced against unchanged UI61, not assumed from the user's screenshot.

Report-branding edits now remain a clearly indicated **Resume report branding** draft when you move
elsewhere. The draft no longer falsely blocks entry to Fleet. Return to it to save or deliberately
discard it. Leaving does not silently publish the profile or blank its report-type selections; HSE/QSHE
is included in that selection. Its original saved profile version is retained, so a newer saved
profile cannot be silently overwritten when you return.

This is **in-tab retention**, not a new durable offline draft store. Reloading or confirming sign-out
can discard unsaved in-tab wording. The existing sign-out warning includes a retained branding proposal.
Active image preparation, preview/import requests and profile saves remain protected; navigation and
sign-out must wait for active work. Older requests cannot close or redraw a replacement editor.
No generic reason is required merely to navigate; actually saving a report-branding change retains its
existing meaningful review.

## Why a small logo could fail at Save

The unchanged UI61 reproduction used a **31,634-byte JPEG**. Its valid normalised PNG was **222,398 bytes**,
and the complete JSON profile request was **297,067 bytes**. The logo preview succeeded, but profile Save
returned 413 because the common server rejected its Content-Length above 100,000 bytes before the
Company Branding service's existing 3,000,000-byte validator could run.

The four report-branding routes now use that existing **3 MB request bound**, including streamed requests.
Other routes retain their own limits. The actual image limits remain **2 MB**, at most **4,096 pixels
per side** and **8 million pixels** before accepted normalisation. This is not an unlimited upload or
proof that every small file is valid. The user's specific reported 45 KB file was not available for
inspection, so its exact dimensions/format/cause were not established.

Report branding still changes database-owned PDF/report presentation. It is separate from the operator
identity described next, and does not replace an original certificate or authenticate a document.

## Per-company application header, selected by the server deployment

The existing COMPANY_ID in COMPANY mode selects a code-owned entry in **deploy/company_identities.json**.
The main application header and standalone Fleet display the selected name and, when supplied, the
validated logo. Embedded Fleet avoids a duplicate plaque. Wavelink/AJ Offshore Solutions product identity
stays visible; a compact white panel provides contrast and preserves the logo's proportions.

This release includes:

```json
{
  "sulmara": {"name": "Sulmara", "logo": null}
}
```

**No usable Sulmara logo artwork reached this build.** The available attachments were hosting/login
screenshots, not the requested corporate mark. They were not embedded, and no guessed logo is supplied.
Sulmara therefore appears as text until its actual approved image is added.

To add the approved image later, put it at **deploy/company_logos/sulmara/logo.png** and change the entry's
logo value to **logo.png**. Commit the image and configuration together. For another company, add an entry
and directory matching that service's existing COMPANY_ID. The shared repository remains reusable; the
current process exposes only its own selected public artwork, never another company's arbitrary path.

Supported header artwork is a single bounded PNG/JPEG: <=2,000,000 bytes, <=4,096 pixels per side and
<=8 million pixels. Missing or invalid artwork falls back to the configured name. Public artwork must
not contain credentials or private reports. The selected descriptor and versioned logo route are available
through the actual hosted factory as well as the local app, with existing company host/setup boundaries
retained. Selection occurs at process startup, not from a browser-supplied company ID or Host header.

This does not change PDF Company Branding, Chrome app identity/icons/window reuse, the isolated visitor
signing page, historical Help/manual pages or the company first-sign-in design. No new environment setting
or database initialisation is needed. See deploy/company_logos/README.md for operator instructions.

## One persistent Administration navigator

The same authorised sections now stay in the same order through People & access, Departments,
Record management, Imports & examples, Company branding, Templates & routines and Logbook designer.
The navigator remains while creating a logbook and during **Fleet & site access**, which is deliberately
hosted through #admin/fleet in the existing embedded Fleet view. Only the content below changes.

Phones show the same choices in a consistent wrapping navigator. UI60 controls and contextual Help
remain; Help opens separately. Existing dirty-form and active-write guards still prevent a section
change from silently discarding an unfinished user, definition or Fleet form.

Shared builders remain available to permissioned non-admins through their appropriate builder choices.
They do not receive People, Departments or other administrator controls. Existing operational workspaces
and their sidebar are not replaced. No new polling timer or DOM-moving observer is added by the navigator.

## Normal project work plus explicit site logistics

As an administrator, open **Administration → Fleet & site access → select the account's access control**.
Choose **Project + site logistics**, then the appropriate roles for each site, with the existing
meaningful permission-change review. This lets that account retain its normal project permissions while
using the Fleet actions assigned at those sites. It does not automatically grant Tasks, Handovers or
Inventory permissions that the person did not already have.

| Mode | Meaning |
|---|---|
| Project only — no Fleet access | Ordinary project permissions; no site-logistics grant from this mode. |
| Project + site logistics | Existing project permissions plus explicitly saved site roles. |
| Vessel-only | Remains restricted to the authorised site workspaces; no broad project access. |

Existing accounts are not converted and old stray site grants do not activate additive access.
The saved mode is project_logistics in the existing scope table. Changing access revokes existing
sessions; preserve the person's work, then sign in again as that same account.

Existing site roles retain their meaning: **Viewer** views; **Operator** can also prepare, dispatch and
receive; **Manager** can additionally close shipments and release quarantine. Actions still require the
appropriate origin/destination site. Site creation, initial equipment allocation and account grants
remain administrator operations. Site roles do not grant separate vessel-log editing/export permissions.
No company-wide administrator promotion or automatic access expansion is used.

## Fleet navigation, refresh and logout behave consistently

Late allocation, asset, history and other reviewed lookups retain their originating account, route and
dialog generation. They cannot replace a newer site form or paint an asset over a different selected
workspace, including after an intervening form has closed. Existing placement lookup protection remains.
An older operation completion is also scoped to its original form; sent requests can still commit and
must retain their exact operation identity for retry rather than being treated as cancelled.

Definitive access/session denial clears protected rows, including behind an open form, without deleting
that form's text. A temporary connection failure labels the last-saved view and blocks stale actions
until a successful refresh. The connection timer is not disabled or converted into automatic shipment
writes. Unsent Fleet proposals remain in-tab, not a new durable draft vault.

A same-record manifest refresh preserves the selected Packing/Files & history tab, loaded history,
filters, disclosures and reading anchor when it still exists. Receive selections are deliberately cleared
for a new exact-scope review. Keeping your place does not retain outdated dispatch or receipt authority.

Standalone Fleet sign-out now distinguishes confirmed server logout from local-only sign-out when the
server could not confirm revocation. An old token may then remain valid until expiry/revocation. Pending
work is protected and a dirty in-tab form needs a deliberate exit decision. It does not claim to sign out
other devices or close another window. Embedded Fleet retains the host's existing sign-out boundary.

The embedded phone header is compact, with the logistics sections discoverable under one labelled
navigator. Route, status, groups, files/history and primary actions remain. The useful Route → Items & boxes
→ Transport → Review creation guide stays; routine draft editing reasons were not broadly removed here.

## Shipping meaning and report evidence remain intact

Ready now accurately explains the existing reservation: it prevents conflicting ready/active shipments
for the same pending equipment. It does not physically move equipment, verify its condition or release
quarantine. Drafts can coexist before that review; current item/contents versions are checked again.

Prepare → Ready → Dispatch → Receive → Hold/place → Close still uses the same equipment identities,
whole nested groups, exact versions and actor/time history. Partial receipts concern complete stored
records/groups, not partial quantity inside one stock row. Missing remains pending/in transit; damaged
receipt remains quarantined through final placement and shipment closure until separately released.
No automatic receipt, stock adjustment, loss settlement or equipment release is introduced.

Manifest PDF changes are limited to typography/spacing. The same fictional box-and-child example went
from two pages to one while retaining every report body word, saved exception and action history. Other
large reports can still need more pages; this is not a universal reduction or long-volume acceptance.
Original attachments stay separate. The report is not carrier paperwork or a return-to-service certificate.

## One practical acceptance session

Use fictional data. Keep a disposable report-branding proposal, leave it and open Fleet; Resume report
branding must return to the unchanged proposal. Test the supplied valid small raster file and save the
profile after review. Move through all Administration sections and its Fleet access page on a phone.

Grant a normal project worker appropriate roles at two fictional sites. Create/ready/dispatch a kit and
independent item; receive in separate complete groups, record a damaged test outcome, place from holding,
review closure and release quarantine separately when authorised. Check the same ID, files, history and
report. Confirm a vessel-only test account stays restricted. Never test revoked access or discarded work
using valuable unsent operational information.

## Verification and limitations

**619 selected Python tests, 92 compound browser checks and 86 JavaScript syntax checks passed.** All 198 application Python modules parse; 190 existing modules are byte-identical to UI61. The frozen source has 1889 tracked runtime files. Python groups: workspace_py=97, hosted_http_py=53, admin_branding_py=108, originals_py=65, preserved_py=118, hosting_py=178. Browser groups: admin_browser=12, fleet_browser=20, interface_browser=7, refresh_browser=26, signout_browser=13, originals_browser=14. Six additional integrated C01/hosted-branding checks and a read-only, same-record manifest PDF comparison completed. The 16-workspace × three-width shared-interface comparison is inside its browser group, not 48 extra functional tests. The retained refresh group includes the normal 33.5-second concurrent timer check.

One historical UI60 test hard-codes its retired asset-cache URLs and was deliberately deselected; the new UI62 contract retains the complete current main-script/stylesheet precache and storage-identity assertions. Other operational assertions were not removed. Initial service/browser fixture and selector failures, earlier complete development runs and a prior full candidate run are retained separately and excluded. An actual C01-boundary check caught a missing hosted /api/info identity projection after the earlier candidate passed local-app checks; the projection was fixed, a hosted-factory regression added, and every final counted test group rerun on the refrozen source. An initial new-test anonymous profile read omitted the required project header and correctly received 409; the corrected test supplies the project header and verifies authentication refusal. A source-audit script initially used a nonexistent invitation-module filename; the exact real module is now checked unchanged. After the full final run, the Fleet browser harness's inherited method label was corrected from UI61 to UI62 and that entire browser group rerun; application bytes were unchanged. Earlier runs and these repeat checks are not added to the totals. No unrelated historical failure, native execution or live deployment is claimed fixed.

Tests use actual application assets and disposable SQLite/TestClient services, controlled fetch/hash
routing and staged browser memory/sessionStorage. The hosted and C01 checks use ASGI with simulated
trusted HTTPS headers, not real TLS or a deployed proxy. The Original Files retained harness provides a
test-only SHA-256 primitive at its set_content origin. No live Sulmara/demo records, credentials, disks,
DNS, GitHub/Render configuration, actual installed Chrome, physical phone/camera/printer, durable IndexedDB,
service-worker lifecycle, native Windows binary/PowerShell, full-product suite, security/accessibility/load
certification, Docker build or accepted off-host recovery was tested or changed.

The shared interface, existing original-source links, guest participation/PDFs, personal shifts, quiet
cache writes, ordinary operational writers and C01/G01 startup remain. Seven hosted Help article bodies
are updated; the other69 and all76 catalogue/outline entries are checked. Historical PDF guides and PWA
identity/icons remain unchanged. No native executable was rebuilt; its access-chooser source recognises
the new mode, but Windows execution is not accepted here. No unsafe old-source recovery or database
rollback is recommended; earlier software does not implement additive logistics and new identity handling.

**Nothing has been pushed or deployed from here.** Resume the agreed section-by-section process after
checking this connected workflow. The Chrome safe focus-existing-window follow-up remains separate.
