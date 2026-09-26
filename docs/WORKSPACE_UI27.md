# Wavelink UI27 — author recipient and acknowledgement review

**Core 1.34.19 · UI27 · working G01 unchanged · 26 September 2026.**
Grouped handover update for the exact **UI26 + G01** supplied-UI18 lineage from this
chat. Incremental patch, not a full repository or a live-project backup.

## Review the people who can currently access a publication

As its author, open a published handover and choose **Current recipients**. The
**Recipients & acknowledgements** panel retrieves the exact current publication's
recipient roster. It does not use unpublished audience changes in a private draft.
Recipients and other administrators do not gain this author-only view.

Summary buttons show **Current recipients**, **Not yet recorded · may acknowledge**,
**Personally acknowledged** and **View only**. Archived handovers also distinguish
**Archived · not recorded**, with no new acknowledgements available. Each account
is counted once, including a person selected both by name and department.

Click a summary to filter, use **Acknowledgement state** or **Current audience
source**, and search by name, login, account ID or department. **Reset filters**
restores the whole retrieved list. The displayed row count is separate from the
summary counts, which always describe the complete retrieved snapshot.

These are **not unread messages, delivery receipts, required signatures, a crew
roster or operational completion**. Shared logins are shared identities. Department
routes reflect current membership, not membership at publication. A recorded
acknowledgement remains visible if its account becomes view-only; the saved name
and timestamp are distinguished from current account details.

## Audience exceptions and retained evidence

**Audience exceptions & retained acknowledgements** jumps to a separate section.
Current-list search/status filters do not hide or recalculate this evidence.

Unavailable named selections and inactive selected departments are shown separately.
No replacement is assigned. The response does not identify a specific cause for an
unavailable account; an administrator must review access deliberately. Active
selected departments with no eligible members are not enumerated by this endpoint.

Acknowledgements for this exact revision from accounts outside the current roster
remain separate evidence, not people currently awaiting a signature. Earlier
publications keep their own acknowledgement history. Nothing here sends reminders,
changes permissions, acknowledges on another person's behalf, publishes or saves.

## Refresh and interrupted work

**Refresh current recipients** clears the old names and counts before a fresh
read. The response must contain a valid exact identity/revision/actor, complete
consistent counts and unique entries with valid acknowledgement states. Missing
counts are not shown as zero. Invalid or incomplete responses clear the panel and
offer **Retry this publication**, rather than leaving stale or partial results.

A newer publication is not silently substituted: use **Reload saved record**, then
open Current recipients again. **Hide recipients** closes only the panel, including
while a read is pending. Delayed responses cannot reopen it over an editor, another
route or a different account/session. An interrupting dialog requires explicit
retry after closing that dialog; the editor and unrelated local work remain intact.

The hub's observation time is shown. This is a retrieved snapshot, not a live feed,
a record of delivered notifications or proof that someone read the wording.

## Existing workflows and installation

UI20 automatic shifts, saved-draft continuation, publication/acknowledgement guides,
previous-shift reference, draft review, incoming publications and UI26 history/
comparison remain included. **Unsent notes and reasons are still in-tab only until
explicitly saved**; this update does not add offline drafts or autosave.

Preserve the approved commit, complete project backup, outside edits and unsent
browser/separate-log work. In the extracted patch folder run:

```powershell
.\CHECK_UI27_UPDATE.ps1 -RepositoryPath "C:\path\to\wavelink" -Mode Baseline
```

After a passing check, copy the **contents of UPLOAD_TO_GITHUB into the existing
repository**, retaining subfolders. Review the diff, commit and push through your
normal workflow. Run `-Mode Installed` to check the resulting repository. Stop and
reconcile a mismatch. Do not replace the repository or delete absent patch files.

Only `deploy/extract_source.py` changes among existing executable upload files.
All 181 application Python modules, G01 gateway/entrypoint, dependencies, source
parts and startup remain unchanged. No new API, tables, saved formats, dependencies,
environment variables or required deletions. Handovers displays UI27; Home UI13
and Original Files UI19 remain. The code changes no automatic action or permission.

Keep **DEMO_PUBLIC_ENTRY=YES**, **INITIALISE_FICTIONAL_DEMO=NO**, required access
password, matching non-admin guest credentials, named administrator, domain, disk
and removed initial-admin bootstrap. No reset, re-import or browser-storage clearing.
Rollback source via the approved UI26 + G01 commit, not an older full ZIP or a data
rollback. The pristine-source recovery helper is still unapproved for overlays.

## Local checks and remaining acceptance

**433 selected Python tests** (342 application + 91 gateway/package), **126 compound
Chromium checks** and **56 JavaScript syntax checks** passed on freshly extracted
frozen source. All 1,677 runtime manifest entries were verified. Four historical
assertions also fail on untouched UI26 and remain explicitly excluded, not passed.

Tests use shipped assets, fictional data and controlled transport/in-memory browser
storage. No live-service, full-suite, physical-device, durable-storage, service-worker,
Windows/PowerShell, Docker, security/isolation or off-host acceptance is claimed.
Nothing was pushed to GitHub or deployed to Render here. Evidence is separate.

Handovers and continuity Help are updated; 74 other bodies remain unchanged. The
wider roadmap remains in DEVELOPMENT_TODO. Handovers stay first: check the complete
named-author/incoming shift workflow on the hosted service, then address feedback
before unrelated expansion. Continue grouped releases, not isolated tiny patches.
