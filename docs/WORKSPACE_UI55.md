# Wavelink UI55 — shared refresh stability

**Core 1.34.19 · UI55 · Company C01 and demo G01 preserved · 28 September 2026.**
A stability update for the exact prepared **UI54 + C01 + G01** repository. This is not a
new section design, full repository, company backup or evidence of a deployed version.

## What caused the remaining flicker

The main eight-second refresh saves its downloaded checklist catalogue, snapshots and device
heartbeats in the existing browser workspace. UI54 counted these cache writes as user work for
the full-width **Saving local workspace** banner. With no actual draft or pending result, that
banner appeared and disappeared around the cache transaction, changing page height.

This is a shared path outside the individual section renderers. Reproduction with actual UI54
assets and a controlled 180 ms local-write delay found two banner appearances during two idle
rounds on Home and Setup & builders. The 390 px Home page's scroll coordinates varied between
500 and 620 pixels; native anchoring compensated for some visible content movement there.
Fault Reports opened by an exact-record link additionally rebuilt the report on each round.
These are local reproductions, not an inspection of the user's browser or every live symptom.

## Quiet cache writes, real work still protected

Downloaded snapshots and heartbeat caches now use the SAME guarded transaction without the
transient user-saving banner. They are still stored, and they still count as active local
writes for sign-out, write-lease and batch-discard protection. This does not disable sync,
skip data persistence, cancel requests, clear local work or falsely mark work saved to the hub.

Actual draft writes, queued results, uncertain outcomes, conflicts, offline states and storage
failures retain their original feedback. Cache success does not dismiss an unresolved save.
The connection/project labels and save-status visibility are not reassigned when unchanged.
The presence label follows the same rule; its heartbeat, permissions and expiry are unchanged.

Eight-second refresh rounds no longer overlap when the earlier round is still running. The
existing in-progress round finishes normally; this is not turning off timers or dropping user
operations. Presence, notifications, real saved updates and the original queue remain active.

## Direct Fault / HSE report views stay in place

An already-mounted exact-report route now refreshes saved data instead of navigating back
through a loading screen. Unchanged rows and the report remain mounted; changed saved content
updates with the existing keyed display helper. Selecting another report while the original
URL remains present does not force selection back on the next poll.

Reading History stays on that history, with expanded sections retained. It is not a live
rewriting of the history being read; the existing Return/reopen action retrieves current details.
Current report/catalogue access is still checked. A definitive denial clears protected report
content, including behind an intervening shared dialog, without deleting that dialog's text.
A temporary failure labels the last saved report view; existing edit routes still fetch/check
current state. An old success cannot take over a changed account, route, selection or dialog.

Report actions, assignments, explanations, review/closure rules and API payloads are unchanged.
The approved Home/Tasks/Checklists/Logs/Handovers/Calendar/Inventory/Maintenance designs remain.
This does not promise that genuine navigation, connection transitions, removed content or a
new deployment can never affect layout. It addresses the identified shared path and report
refresh defect rather than suppressing every update or warning.

## Apply through GitHub Desktop

Save or deliberately keep current work, preserve the approved commit and your established
complete backup. Extract the ZIP; copy **everything inside UPLOAD_TO_GITHUB into the existing
UI54 Wavelink application repository**, replace matching files, review in GitHub Desktop,
commit and **Push origin**. Not the separate website repository. Do not replace the repository,
delete unrelated files or copy the enclosing UPLOAD_TO_GITHUB folder as another subdirectory.

The included CHECK_UI55_UPDATE.ps1 is OPTIONAL read-only checking, not an installer. It was
not run on Windows here. Independent source changes must be reconciled, not overwritten blindly.
No new environment variables, permissions, dependencies, API routes or database tables are needed.

Keep activated Sulmara C01 identities, domain, disk and activation marker, INITIALISE_COMPANY=NO
and removed bootstrap secrets. Keep the independent G01 demonstration's existing settings,
domain, disk and credentials. Both services may auto-deploy from the same branch; review that
before pushing. No reset, re-import, browser-storage clearing or repeated company setup.

Once the intended deployment is healthy, SAVE open editors before reloading once to load the
new scripts. In-tab-only wording is not a durable draft. Do not clear site data to force an update.

## One stability check

Leave Home or Setup & builders scrolled down for about 40 seconds without editing. The temporary
Saving local workspace banner should not appear just because a refresh ran. Then open a Fault
or HSE report by its exact link, read lower content or History, and let another named user save
a real progress update. The saved change should appear without repeatedly remounting the page.
Actual save warnings must still show when you deliberately save work or encounter a failure.
Use disposable records for interrupted-save, account-change or revocation tests.

## Checks and limitations

**342 selected Python tests, 93 compound browser checks and 79 JavaScript syntax checks passed.** All 193 application Python modules remain byte-identical to UI54. The frozen extractor produces 1846 tracked runtime files. Python groups: refresh_py=93, reports_py=36, checklist_py=35, hosting_py=178. Browser groups: refresh_browser=26, signout_browser=13, checklists_browser=10, reports_browser=26, maintenance_browser=18. Two intentionally excluded historical assertions were reproduced failing on untouched UI54. No full-suite claim.

The primary browser run samples frames during delayed local writes, including seven workspace
entry points and direct Fault/HSE pages. It also runs the actual periodic callbacks concurrently
for 33.5 seconds (at their normal intervals), rather than testing only one manual refresh.
Transport, routing and atomic browser storage remain simulated; WebSocket and normal browser
navigation are not accepted by that run. Real service writes and permission checks use temporary
fictional SQLite/TestClient projects.

Two old version/hash assertions also fail on untouched UI54 and are explicitly excluded—not
reported as fixed or passed. The initial tool-interrupted browser attempt and superseded shorter
run are retained separately. Final runs use the frozen extractor. No production Python module,
normal save function, company startup or gateway has been rewritten for this update.

No live Sulmara/GitHub/Render access, physical-device, durable IndexedDB, service-worker lifecycle,
Windows/PowerShell/native, full-product-suite, full security/accessibility/load, Docker or accepted
off-host recovery result is claimed. No live credentials, records or hosting settings were changed.
One hosted Save-status Help body/outline is updated; 75 other bodies and all 76 catalogue entries
are retained/verified. Native/master PDF guides are unchanged.

**Nothing has been pushed or deployed from here.** Address any remaining actual refresh feedback
before the next section; Certificates remains the next planned section review.
