# Wavelink UI92 — Consistent browsing and hosted clarity

Core **1.34.19**. Parent: the supplied working **UI91**, not the failed diagnostic UI92.

## What changes

Normal workspace banners use the same title hierarchy, spacing, Help position and desktop minimum height. The ordinary main-app covers are 188 pixels high in the 1440-pixel acceptance fixture; long text, additional controls and narrow screens may grow rather than clip. Original Files and Administration own their full headings instead of nested miniature banners. Fleet uses the shared heading geometry. Approved Home/Profile artwork and badge assets are unchanged.

Original Files now renders an actual parent-ID folder hierarchy. Expand/collapse is separate from selecting a folder, and direct revision counts remain visible. Selecting revisions and then collapsing a folder does not move or deselect them. Searching still covers all accessible folders. The original upload, move, rename, history, permission and consequential-action review mechanisms remain.

Certificates is the first additional module using a compact left record list and larger right detail preview. The preview reads the current authorised record, dates, source-file names and linked equipment. On phones it uses a list/detail view with a Back control. **Editing, source-file downloads/uploads, history and renewal still use the existing full-record view**, reached with **Open record & source files**. Merely selecting a record does not sign, acknowledge, save, approve or create anything. This does not yet convert Tasks, Maintenance or every other module into inspectors.

Certificates also repaints its register correctly when revisiting an unchanged list; a cached signature no longer leaves the route stuck on its loading message. Late, mismatched, denied, filtered-out and signed-out preview responses are rejected.

The ordinary interface no longer repeats Local hub footer text or no-work recovery prompts on Home and Workspaces. Account > Workspace tools retains a collapsed **Connection, recovery & device tools** section. Actual unsaved work still activates the account indicator and relevant warning areas. Queued changes, conflicts, uncertain saves, storage errors and recovery exports remain intact. The tablet top bar retains the badge, account and action controls inside the screen.

## Apply this release

Use the Wavelink **application** repository, not Wavelink-Website. Preserve the current commit and normal operational backup. Copy the contents of `COPY_TO_REPOSITORY` from the compact update into the existing repository root, keeping paths and replacing matching files. Do not place the wrapper folder itself inside the repository. Review the diff, commit and push using the existing deployment workflow.

Keep `vendor/`, Docker/startup files, company identity and logo files, Render configuration, disks, database, environment variables, initial setup markers, C01/G01 separation and M01 configuration as they are. This update does not require a new setup key, account, SMTP change, fictional-data import, database reset or browser-storage clearing.

The extractor assembles the same pinned source parts and then applies UI92 after all verified predecessors. Its console output ends with **Applied Workspace UI92**. The shell uses the new versioned UI92 assets; core remains 1.34.19.

## One acceptance session

Compare Team, Logs, Certificates, Original Files and Administration banners. Expand Operations > AUV > a subfolder in an appropriate test library, select a revision, and collapse/reopen its parent. Select two certificates, review the right panel, and open the full source record. On a phone, use Certificate list to go back. Check that Home/Workspaces are quieter when there is no unsaved work, then check a genuine draft still has a visible review path. Do not discard real work as part of testing.

## Verification boundary

See `DELIVERY_CHECKS.json`, the current checkpoint and separate evidence ZIP for exact executed checks. Local acceptance uses temporary fictional databases and a Chromium-to-TestClient bridge. It is not a live Render deployment, actual Android/iPhone test, service-worker lifecycle test or complete legacy test-suite pass. Seven historical tests in the selected broad suite also fail on the unchanged UI91 baseline; the comparison is recorded rather than hiding or rewriting them.
