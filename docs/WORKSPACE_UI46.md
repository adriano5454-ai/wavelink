# Wavelink UI46 — work-focused Home

**Core 1.34.19 · UI46 · Company C01 and demo G01 retained · 27 September 2026.**
A compact update over the exact UI45 + C01 application repository from this conversation.
Not a complete repository, a database backup or a deployed service.

## Update with GitHub Desktop

Extract the ZIP. Copy **everything inside UPLOAD_TO_GITHUB into the existing UI45 application
repository**, replace matching files, review in GitHub Desktop, commit and Push origin. Do not
replace the repository, delete files absent from the patch or copy the enclosing folder itself.
The PowerShell checker is optional read-only checking, not an installer or required upload.

The demo and Sulmara may both auto-deploy from the same branch: review their settings before pushing.
Preserve backups, the approved commit, outside edits and unsent browser/separate-log work. Keep C01
company identity, public URL, dedicated disk and activation marker, and existing G01 demo settings.
After company activation retain INITIALISE_COMPANY=NO and removed bootstrap secrets; never redo setup.
No new environment variables, dependencies, permissions, API routes, tables or browser-store versions.
No reset, demo re-import, account change or site-data clearing is needed.

## Continue saved work first

**Your work** appears before the workspace directory. Its rows open actual saved records:

- **Continue notes** opens your current saved daily-handover editor. Other handover types or
  view-only access open the saved record instead. No duplicate handover is created.
- **Read handover** opens the exact publication awaiting your acknowledgement, never its author's
  newer private correction. Reading is not signing.
- **Open task** shows an open task explicitly assigned to your account. Administrators do not get
  all accessible tasks relabelled as their own assignments. Postponed tasks are counted separately.
- **Open checklist** resumes the first unfinished stage of a standalone checklist you created.
  This does not include every checklist you joined or Task-owned checklists. Its existing device
  participation and read behaviour remain; no results are completed or approved by Home.
- **Open issue** uses the existing log-issue inbox for issues assigned to you or your departments.

Four preview rows are initially visible. **More of your work** reveals further previews when present;
there are up to five per category, with links/counts for the full workspaces. Different categories
are interleaved for discovery, not ranked as a universal priority list. Preview titles do not become
persistent browser drafts. Unavailable information is labelled unavailable, not zero or all clear.

**Project overview** is separate: accessible Tasks, project-wide maintenance dates and follow-ups,
certificate dates and administrator receiving groups. These are not automatically your assignments.
Expand categories for their scope, limited record previews and normal module links. It starts
collapsed on phones and expanded on wide screens; current-session choices remain usable.

## All the workspaces remain

The complete permission-filtered directory is a compact grid below the work summary. Handovers,
Tasks, Inventory & boxes and Manifests & shipments are near the front where allowed, followed by
Logs and Checklists and the other workspaces. **Open** and creation are separate labelled actions.

The four-card New task chooser and real Verify inventory form remain. Handovers retains visible
Create handover, By day / subject, My shift, People & shifts and all creation types. Maintenance,
Certificates, Toolbox Talks and checklist creation use the existing forms and save rules. Original
Files opens the same library. No module has been replaced with a basic subset.

The five category filters and activity search remain. Search shift, verify stock, renewal or a
module name; this matches destination descriptions, not private records or file contents.
**Show all available workspaces** clears filters. Enter focuses a match, not an automatic create.
Directory filtering does not change personal/project counts. Internal UI badges and long navigation
instructions no longer dominate the Home heading. The existing navy/mint identity is unchanged.

## A clear start for empty available builders

When no personal preview entries are returned and every builder available to the current account
has zero saved definitions, **Set up your workspace** offers a builder selector and **Create new /
Import existing**. This is based on the authorised builder catalogue, not a scan declaring the
entire company database empty.

A permissioned Technician or Supervisor gets their applicable choices without being an administrator.
The destination rechecks current access and opens the existing actual builder or focused import form.
No template, inventory, account or demo record is created simply by opening a shortcut. Once a saved
available definition exists, or personal work appears, the normal work-focused layout returns.
Setup & builders stays in the full directory. Failed setup reads do not invent onboarding progress.

## Unsent work and interrupted requests

Manage unsaved work and separate-tab Help remain reachable. Actual connection, unsent-work and
conflict warnings are preserved. UI45's keep-stored-drafts sign-out and same-account resumption
remain unchanged. In-tab-only text still needs an explicit save; this update does not add autosave.

Home refresh clears the previous private snapshot, then reads the current summaries and, where
permitted, builder catalogue. These are separate reads, not a live atomic snapshot. A modal, account,
route, hidden tab or newer request prevents late results from taking over another view. A failed read
has an explicit retry while the full workspace directory remains available.

Testing caught a delayed hash-event problem: an obsolete route event could disable the current
Home shortcuts. The new Home handlers ignore obsolete event destinations and retain the current
account/route/form guards. New requests on entry still run; delayed form lookups remain invalidated.

## One acceptance session

Using fictional data on a named account, open Home, continue one saved handover, return and open
one assigned task. Check that another person's private handover correction does not appear.
Open New task and Verify inventory to see the complete choices. For a separate empty permitted
builder account, try Create new and Import existing from the setup prompt. Open Help while test
wording is present; it must remain in the working tab. Check phone Home during the same session.
Never discard valuable local work for testing.

## Validation and boundaries

481 selected Python tests and 56 compound browser checks passed on the final candidate,
alongside syntax checks for 72 application JavaScript files and 193 application Python parses.
The final ZIP replay reproduces 1795 tracked runtime files. The current verification report
records individual runs and exact hashes; preliminary/failed runs are separate and not passes.

The application change is read-only Home metadata plus presentation and direct-entry routing. One
existing Python module, attention.py, changes and home_work.py is added; 191 existing Python modules
are byte-identical. The shared app.js functions, operational writers, sign-out/local-work helpers,
C01 deployment files, G01 gateway, signing Nginx and all report/PDF generation remain unchanged
apart from asset cache URLs where applicable. No actual Sulmara records, credentials or hosting
settings were inspected or modified.

Browser tests use shipped assets, fictional TestClient APIs, simulated hash navigation and staged
in-memory storage. Normal navigation is blocked by the test environment; its policy was not bypassed.
These are not full-suite, live HTTPS, physical-device, durable IndexedDB, service-worker lifecycle,
Windows/PowerShell/native, full accessibility/security/load, Docker or off-host recovery acceptance.
No unrelated historical test failure is claimed fixed. Native Home and master guides were not rebuilt.

## Section-by-section review from here

Home is the implemented section. For each further section: examine the current desktop/mobile
workflow, identify the user's pain points, agree the changes, then deliver one coherent update
and one short acceptance session. Keep useful choices, wizards, permissions, history and controls.
Do not hide capabilities or turn routine editing into repetitive paperwork. The larger retained
roadmap remains in DEVELOPMENT_TODO. No other section was redesigned here and no background work
is scheduled.

**Nothing has been pushed to GitHub or deployed to Render from here.**
