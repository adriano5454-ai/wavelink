# Wavelink UI32 — continue saved notes and keep the correct shift period

**Core 1.34.19 · UI32 · working G01 unchanged · 26 September 2026.**
Compact update for the exact UI31 built from your uploaded application repository.
It is not a complete repository or a live-project backup. Nothing was deployed here.

## Update using GitHub Desktop

1. Preserve unsent work, your approved commit and complete project backup. Extract this ZIP.
2. Copy **everything inside UPLOAD_TO_GITHUB** into your **existing Wavelink application repository folder**, accepting replacement of the matching files.
3. In GitHub Desktop, review the changes, commit and **Push origin**. Deploy the intended commit through your usual service workflow.

Do not replace the repository, delete files absent from the patch, or copy the enclosing
UPLOAD_TO_GITHUB folder as an extra subfolder. This is not the separate website repository.
The `.ps1` is an **optional read-only checker**, not an installer or a required upload:

```powershell
.\CHECK_UI32_UPDATE.ps1 -RepositoryPath "C:\path\to\wavelink" -Mode Baseline
```

`-Mode Installed` checks after copying. Reconcile independent changes instead of overwriting
them. No new environment settings, endpoints, dependencies, tables, migrations or deletions.
Keep **DEMO_PUBLIC_ENTRY=YES**, **INITIALISE_FICTIONAL_DEMO=NO**, the required gate secret,
matching non-admin guest, named administrator, domain, disk and removed bootstrap unchanged.
Preserve in-tab work before reopening older application tabs. No reset, re-import or site-data clearing.

## Resume without searching dates or advanced tools

In **Handovers → My shift**, **Continue saved notes** shows your saved private daily drafts
for the selected department across dates and sites. The most recently saved draft has
**Continue my notes** immediately visible; **Other saved drafts (N)** expands the others.
The panel is above the operational-day controls. Selecting today cannot hide yesterday's
saved notes. Other people's private drafts, archived handovers and full-hitch drafts are
not included; the existing advanced tools remain available for their permitted workflows.

Opening retrieves the current saved record. It does not create another handover or use
wording from the list snapshot. Editing revoked by a permission change is not restored by
this panel. Unsent text in another tab is not a saved draft and does not appear here.

## See the team under the correct recorded shift

For the selected operational day, your notes and accessible colleagues' publications are
shown under the shift whose **saved start, end, time basis and site** actually match.
Current assignments are labelled **Assigned now**; they are not a historical crew roster.
Colleagues' newer private corrections are not displayed as finished notes.

Older records that do not match the current setup appear under **Other saved handovers**
with their original period and site. An existing saved record does not become a new one
just because the schedule changed. Where the existing duplicate rule identifies that
record, the board points to it instead of offering another Open my shift action.

A new site can still have its own group under the existing rules. The update does not
rewrite saved dates, relocate notes, reassign their authors or invent missing shifts.

## Fixed: changing or removing setup could hide saved records

The UI31 simple board filtered the day to the setup's current site and returned early
when no current setup existed. Local reproduction confirmed that saved handovers could
disappear from this view while still existing in the database. UI32 retains permitted
saved records and own drafts in both cases. Starting a new assigned shift still needs
valid setup; a corrupt or inaccessible configuration is not silently ignored.

Changing the date, department or refreshing clears the old overview before retrieval.
Failed, mismatched or interrupted reads do not leave stale cards available for opening.
Late responses cannot replace a newer day, account or editor. A modal interruption leaves
an explicit refresh path rather than a stuck loading message.

## Writing stays simple

**Open yours → write → Save & close or Finish handover.** The existing simple editor,
setup form and save/finish/retry functions are unchanged. No routine reason, checkbox,
publication wizard, automatic copying or acknowledgement has been added. Finished means
handed over, not that all outstanding work is complete. Issued corrections still use
the existing separate reissue rules. Unsent wording remains in-tab until explicit save.

UI31 presence, Documents → Original files, website icons and support@mywavelink.com remain
intact. Original upload/folder changes remain administrator-only; no permission is granted.

## Verification and limits

**338 selected Python tests** (247 application + 91 gateway/package),
**76 compound browser checks**, **59 JavaScript syntax checks** and
**183 Python parses** completed successfully on frozen source. The new
29 Node checks are included through Python, not extra Python tests. 1,707 tracked
runtime files are verified. Only one existing application Python module changes: the read-only
`SimpleHandovers.board` method; its other methods and 182 other application Python files remain unchanged.
Only `deploy/extract_source.py` changes among existing executable GitHub files.

The browser uses fictional TestClient data and injected transport/in-memory storage. No
full-suite, live-service, physical-device, durable-storage, service-worker lifecycle,
Windows/PowerShell, security/accessibility/load, Docker or accepted off-host recovery result
is claimed. Earlier historical release-assertion failures were not rerun or declared fixed.
Preliminary attempts and the collection-name collision are excluded and retained separately.

Rollback source using the approved UI31 + G01 commit, not an old full archive or data rollback.
Keep UI29 selective-transfer protections; the pristine recovery helper remains unapproved
for this overlaid runtime. The next priority is actual surveyor feedback on this simple
workflow, followed by the retained grouped roadmap—not more daily review screens.
