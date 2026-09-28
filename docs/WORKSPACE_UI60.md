# Wavelink UI60 — one shared browser interface

**Core 1.34.19 · UI60 · Company C01 and G01 preserved · 28 September 2026.**
This implements the approved UI59 interface review. It is a compact source update for the exact
**UI59 + Company C01 + G01** application repository, not a full repository, project backup or native installer.

## Update using GitHub Desktop

Preserve the approved commit, independent source edits, complete backup and unsent main/separate-log work.
Extract this ZIP. Copy **everything inside UPLOAD_TO_GITHUB into the existing UI59 application repository**,
replace matching files, review in GitHub Desktop, commit and **Push origin**. Keep the repository and .git;
do not delete files absent from the patch or use the separate marketing-website repository.
The PowerShell checker is optional read-only checking, not an installer or a required upload.

Both services may auto-deploy from the same branch. Keep Sulmara's activated C01 company identity, URL,
dedicated disk, activation marker, INITIALISE_COMPANY=NO and removed bootstrap secrets. Keep the separate
G01 demo settings, credentials, domain and disk unchanged. No new environment settings, permissions,
API routes, dependencies, database tables or browser stores are needed. Do not reset, reimport, repeat
setup, clear site data, disable synchronization, uninstall the PWA or close an unsaved editor to update.
After the intended deployment is healthy, save/keep open work before reloading to load the new assets.

## Same purpose, same controls

The main workspaces now use one outlined **Help** control: question-mark icon, visible Help label,
separate-opening indicator and a 44-pixel minimum height, with consistent type, border, corners and
keyboard focus. Help is in the upper-right of the workspace heading, including pages that previously
had only a global documentation route. The URL stays relevant to the section, not just a generic index.
The existing new-tab/opener-isolation behavior remains. Browser settings decide whether the separate
browsing context is a tab or a window; there is no forced navigation of your current working tab.

Contextual dialogs use the same Help/title family, alongside existing Close and Sign out controls.
Original Files uses that single contextual header control instead of duplicating it inside its library.
Inline explanatory links keep their descriptive wording; Help-reader side navigation is not converted
into a page full of large buttons. In-page section jumps still work as before.

Workspace titles share one desktop/phone scale. Supporting action rows wrap beneath the title rather
than using unrelated per-module button sizes. Primary actions, supporting outlined actions and destructive
actions remain distinct. View selectors share selected/unselected presentation. Form fields and labels
share borders, type, spacing and focus; notices share presentation without changing warning/error/saved
meanings. Existing checkboxes, radios, required readings and validation remain.

The Task and Certificate scrolling-form layouts now measure their remaining space through flex layout
rather than subtracting an assumed old heading height. Wrapped dialog titles and the new Help control
therefore do not push their Save/Keep draft action rows outside the dialog.

## Full capability, not identical pages

Inventory still has nested boxes and its useful table. Logs keeps its ledger and green/red LOG ON/OFF
controls. Calendar retains the month grid and Agenda. Tasks keeps all four creation cards and verification.
Handovers keeps the personal My shift, separate Incoming/team views and explicit shift permissions.
Builders keep structured editors, Create/Import/View saved and the current permission boundaries.

Existing draft/save/retry/sign-out/discard controls, source references, genuine confirmations, photographs,
readings, history and signature evidence remain. This release does not create a record, pick a result,
authorise work, broaden access or change completion/publication meaning merely by styling a control.
The normal guest-name/drawing and PDF projection introduced in UI59 is unchanged and regression-tested.

Fleet uses the same heading/control family in its existing separate browser surface and embedded iframe.
The existing main-account handoff and intentionally separate log windows remain. Deeper Fleet sign-out,
Original Files workflow simplification and Chrome window reuse are not silently implemented here.

## Shared components instead of copied overrides

The new interface_components.js adapts detached markup at existing render boundaries before it mounts or
passes through the current keyed reconciler. interface_components.css owns explicit shared component
classes/tokens. Existing module styles keep their original rules in an ordered legacy layer; specialist
layouts and semantic statuses stay with their owner. Two superseded builder typography overrides no
longer force a different button font/height. There is no new global observer moving live content after
polling, no extra timer, fetch, storage writer or permission handler in the presentation helper.

The internal **docs/UI_INTERFACE_STANDARD.md** records the contract for future work. New sections should
use these same components rather than introduce another local Help/button stylesheet.

## What is not changed

All **196 application Python modules** and company/gateway files are byte-identical to UI59. No operational
API/schema, report renderer, signing protocol, queue, write-lease, local storage identity or timer is changed.
UI55's quiet background caching and meaningful user-save warnings remain. Existing synchronization continues.

The isolated visitor-signing page, company first-sign-in page, historical PDF/HTML manuals, native Windows
binaries, PWA identity/icons and installed Chrome launch behavior are separate surfaces and are not redesigned.
Do not interpret shared main-workspace CSS as a new installer or a focus-existing-window fix.
One current Navigation Help article is updated; the other 75 article bodies remain unchanged and all 76
catalogue entries still match. This is not a wholesale manual rewrite or a full accessibility certification.

## One acceptance session

With fictional work, move between Home, Tasks, Inventory, Handovers and Calendar on desktop and phone.
Check the same Help control, clear primary/secondary actions and active views. Open a Task or Certificate
form, type disposable wording, then open its Help: the working form must remain. Check Original Files and
an authorised embedded Fleet page. Leave a page scrolled down through background updates, then return to
your own shift and a previously signed document to confirm the focused view and saved drawing remain.
Do not use valuable unsent work for discard, interrupted-save or permission-revocation testing.

## Local checks and limits

**409 selected Python tests, 107 compound browser checks and 84 JavaScript syntax checks passed.** All 196 application Python modules remain byte-identical to UI59 and parse. The final extractor reconstructs 1868 tracked runtime files. Python groups: interface_py=19, evidence_permissions_py=127, forms_py=85, hosting_py=178. Browser groups: interface_browser=7, refresh_browser=26, participation_browser=15, signout_browser=13, tabs_browser=9, maintenance_browser=18, certificates_browser=15, fleet_browser=4. The 48 main-page style renderings are included in the interface group, not 48 additional functional checks. Expanded Fleet checks supersede the smaller two-scenario run, not duplicate it.

The interface matrix covers 16 main landing pages at 1440, 390 and 320 pixels (48 renderings), plus actual
Task/Original Files forms and the existing embedded-Fleet frame with fictional API transport. Keyboard
Help was checked with default navigation suppressed by the test harness: target/new-tab/opener attributes,
focus and no-submit/no-working-route-change were verified, not a live browser's tab preferences.
Retained tests exercise real fictional service writes, guest drawing/PDFs, My shift isolation, sign-out,
Maintenance, Certificates and concurrent periodic refresh. The new helper has no observer/timer/network
or storage API. Existing click/modified-click handling remains unchanged.

Six UI55-specific cache-name assertions were deliberately deselected because that historical test hard-codes UI55 URLs; the current full main-script/stylesheet precache contract is checked in the new UI60 tests. No operational assertion was removed. Earlier development/partial runs, a test locator using #root instead of the actual #app, and a Help-click test intercepted by the existing capture handler are retained separately. A retained handover test initially waited on an already-enabled People button rather than completion of Incoming refresh; its external harness now waits for the actual reloaded content and keeps every privacy/state assertion. A guessed-header-height footer clipping issue and double-bordered toolbar disclosure were corrected before the final source freeze. The final complete selections were rerun on frozen application bytes; only additional Fleet/preview checks were added afterwards. A packaging-helper path mistake and source-audit expectation of the retired builder declarations are tooling corrections, not hidden application failures.

Browser tests use shipped assets and fictional SQLite/TestClient services, injected fetch/hash navigation,
srcdoc for the Fleet host and staged in-memory transactions. Not full-suite, live Sulmara/Render/GitHub,
physical device/Windows/installed Chrome, ordinary production navigation, durable IndexedDB/service-worker
lifecycle, security/load or accepted off-host recovery. No real company records or credentials were read.
Source integrity and fresh extraction are checked separately; repeated packaging checks add no unique
application-test coverage. **Nothing has been pushed or deployed from here.**
