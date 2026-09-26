# Wavelink UI42 — clear workspaces, familiar choices

**Core 1.34.19 · UI42 · working G01 unchanged · 26 September 2026.**
A grouped Home and sidebar-discovery update on the exact UI41 repository. Easier to use does
not mean fewer features. This is an incremental patch, not a full repository or project backup.

## Update using GitHub Desktop

Extract and copy **everything inside UPLOAD_TO_GITHUB into your existing UI41 application
repository folder**. Replace matching files, review in GitHub Desktop, commit and **Push origin**.
Use your established hosting workflow to deploy that commit. Not the Wavelink-Website repository.
Do not replace the entire repository or delete files absent from this patch. The included
CHECK_UI42_UPDATE.ps1 is optional read-only checking, not an installer or required upload.

Preserve your complete backup, approved commit, outside edits and unsent browser/separate-log
work. Keep DEMO_PUBLIC_ENTRY=YES, INITIALISE_FICTIONAL_DEMO=NO, the existing domain, required gate
secret, matching non-admin guest, named administrator, persistent disk and removed bootstrap.
No environment changes, tables, dependencies, migrations, API or permission changes are needed.
Do not reset, re-import the demo or clear browser storage.

## All the main workspaces, not a basic subset

Home now groups its permitted destination cards into **Daily work**, **Equipment & logistics**,
**Safety & quality**, **Documents** and **Administration**. All groups start visible. Each card
has a purpose description and an **Open** action; supported cards also expose their familiar
New/Add/Verify action. Fleet and administration retain their existing administrator scope.

The cards include Handovers, Tasks, Standalone checklists, Logs, Calendar, Inventory & boxes,
Maintenance, Certificates, Fault Reports, Toolbox Talks, HSE/QSHE and Original files, with Fleet,
Manifests, Receiving and Administration for permitted administrators. The available card count
is not a workload total. View-only users keep Open while disabled creation controls explain
missing authority. Missing viewing authority does not expose the destination.

**New task** keeps the four square choices: General task, Verify inventory, Maintenance activity
and Certificate check. Inventory's **Verify inventory** opens the real fixed-scope verification
form, not a renamed generic task. **Open Handovers** keeps the visible Create handover button,
all four types, My shift and People & shifts in the existing workspace.

**New work order**, **Add certificate** and **New toolbox talk** open the current single-page
forms. Routine and published-form selection remain deliberate. **New checklist / dive** resumes
a retained new-checklist draft when one exists. **Open original files** opens the same permission-
checked library without changing Home's route. No signature, publication, equipment movement,
verification or record creation happens merely by browsing. Saves use the existing writer,
local-draft cleanup, identity, duplicate-request and conflict handling.

## Find a destination by what you need to do

Search Home or the sidebar for **shift**, **verify stock**, **renewal**, **sign toolbox talk** or
a module name. This matches static destination names, descriptions and synonyms—not private
notes, saved records, filenames or document contents. All query words must match a destination.

Home's search combines with group filters. Clear removes the query; **Show all available
workspaces** resets both filters. Enter focuses the first Open action without creating or
opening anything. The sidebar retains its original permission-controlled links. Home filter
choices survive a same-session redraw, but reset on leaving Home or changing the authorised
session. There is no persistent favourites list or global record search.

## Existing work stays protected and visible

**Manage unsaved work** remains in the heading, and any existing unsent/conflict notice stays
above navigation. Saved work overview retains its own category scopes and requests; workspace
search does not filter or recalculate it. Separate-log review is retained. The current-account
local manager, protected uncertain entries and separate-tab Help remain unchanged.

Finish or keep an open form before changing workspace. Home rejects stale creation callbacks
following a changed account, route or intervening form. Failed lookup leaves a readable error
and the same shortcut available for retry. None of this adds autosave or durable offline drafts.

## One acceptance session

With a named account and fictional data, use Home's **verify stock** search, open Inventory's
Verify inventory form and check its actual scope choices. Check New task's four choices and
Open Handovers' Create handover. Clear the filters, start a certificate or toolbox briefing,
and open its Help while test wording is present; the original form should stay put. Check
Original files from its card. Use a phone during this same session. No different installation
is needed for each entry point. Save or discard only disposable test work deliberately.

## Verification and limits

**881 selected Python tests, 218 compound browser checks, 11 actual local gateway/core
checks and 69 JavaScript syntax checks passed** on the frozen
source. All 188 application Python modules remain unchanged;
1770 tracked runtime files verified. The final ZIP replay report verifies
the delivered bytes, not merely a version label. Repeated final-ZIP gateway tests add no coverage.

Browser checks use shipped assets, fictional TestClient APIs and injected transport/in-memory
storage, with simulated router hash transitions. They are not full-suite, actual live HTTPS,
physical-device, durable IndexedDB, service-worker lifecycle, Windows/PowerShell/native UI,
full accessibility/security/isolation/load, Docker or accepted off-host recovery results.
The two inherited old version/hash assertions remain excluded, not repaired or passed.
Earlier partial/fixture/refinement runs are retained separately and excluded from final counts.
Two certificate/task browser harnesses had unrelated periodic polling paused during deliberate
identity changes; their complete corrected runs passed. No application code changed during this
fixture correction. The exact cause of every earlier timeout remains unestablished.

Home and Navigation Help were updated; 74 other article bodies remain unchanged. All 76
catalogue entries match. This does not claim the whole Help library or native/master PDF has
been re-reviewed. This release improves app-wide discovery, not every module's internal layout.

**Nothing was pushed to GitHub or deployed to Render from here.** Rollback through your approved
UI41 source if required; never roll data back or use incompatible pre-UI34 evidence writers.
Keep the full functionality, polished clear choices and grouped-release direction for future work.
