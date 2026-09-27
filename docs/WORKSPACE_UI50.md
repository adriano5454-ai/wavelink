# Wavelink UI50 — consistent handover editing and a stable day journal

**Core 1.34.19 · UI50 · Company C01 and demo G01 preserved · 27 September 2026.**
Compact update on the exact UI49 repository from this conversation. Not a complete repository,
company backup, live deployment or a native Windows installer.

## Install using GitHub Desktop

Preserve your backup, approved commit, outside edits and unsent browser/separate-log work.
Extract the update and copy **everything inside UPLOAD_TO_GITHUB into your existing UI49 application
repository folder**. Replace matching filenames; review, commit and **Push origin** in GitHub Desktop.
Do not replace the whole repository or delete files absent from this patch. Not Wavelink-Website.

CHECK_UI50_UPDATE.ps1 is an optional read-only baseline/installed checker, not an installer or required
upload. It has not been executed on Windows here. Both services may auto-deploy the same branch;
review Sulmara's and the demo's settings before pushing. Nothing was pushed or deployed from here.

No new environment settings, dependencies, permissions, API routes or database tables are introduced.
Keep Sulmara's activated COMPANY/C01 identity, domain, disk and marker, INITIALISE_COMPANY=NO and
removed bootstrap secrets. Preserve the separate demo's G01, DEMO_PUBLIC_ENTRY=YES,
INITIALISE_FICTIONAL_DEMO=NO, guest configuration and disk. No reset, re-import, sync disabling or
browser-storage clearing. Do not use incompatible pre-C01 or pre-UI34 evidence writers/exporters.

## One familiar routine editor

All four Create handover choices remain. **Daily / shift handover**, **My assigned shift** and the
normal **Start next shift** now lead to the same seven-section notes editor and optional Photos & files.
**Save & close** keeps your notes private. **Finish handover** saves and first-publishes them together.
Neither normal action needs a typed reason, routine review page or confirmation checkbox.

Start next shift displays the calculated complete period from the selected publication's recorded
schedule. Manual/irregular predecessors retain explicit period controls; there is no fabricated intervening
shift. **Shift date and hours** lets you inspect/change the proposal. The default board date never silently
moves the predecessor's next period to today. The original exact-source, department, copy and no-fork rules
are checked at opening and again when saving. A changed source is refused, not substituted.

**Carry selected previous notes (optional)** starts with nothing selected. Read a section, select only
what is useful to recheck, then choose **Write handover**. The existing allowed-section and attributed-copy
rules remain; summary, completed work, files and signatures are not copied. The previous publication stays
available as an exact read-only reference. This preview creates no record. An existing private daily draft for that same day and department
is offered for explicit resumption rather than duplicated; its saved wording/period is never overwritten
by the abandoned setup choices. An already-published successor must be opened from the saved journal;
the existing fork check refuses creating another chain from its predecessor.

**Full-hitch handover** now uses the same editor, with visible title, subject/site, complete period, time
basis and recipient fields. Search preserves selected recipients outside the results. Its header reflects
your edited period/title, but this is still unsaved context until Save. A private draft can be kept before
its period/audience is complete; Finish requires the existing complete publication information. Full-hitch
is not assigned to a fabricated daily shift or department roster. Your signed-in account remains its author.

Existing own full-hitch drafts also open here. They now use the same supported photo/file controls,
private downloads, immutable publication references and atomic save/first-finish behaviour as daily notes.
Six files, 5 MB each and 10 MB total; supported formats and evidence limits are unchanged. Saved files removed
from a correction remain in the earlier publication. Historical copying does not copy file bytes.

## Issued information still has a deliberate correction path

A published handover is not reopened as if it had never been issued. Start its permitted private correction;
save your private context/notes/files in the familiar editor, then use **Review issued correction** to issue
it through the existing change-summary/review process. A new revision does not inherit signatures or
acknowledgements of different wording. Another person does not gain access to your private draft.

The advanced multi-source **Prepare from previous**, explicit **Manual / irregular daily period** setup,
history/comparison, recipient review, acknowledgement, QR invitations and signing PDF remain available.
Their specific source-copy/exceptional reviews are not blanket-removed. Selecting a recipient is not assigning
them as author or giving permission to edit a private draft. People & shifts keeps its existing manager authority.

## Compact journal, with the place you were reading retained

One heading keeps **Create handover**, **People & shifts**, Refresh, More actions and separate-tab Help
visible. Four direct views are **By day / subject · My shift · My saved notes · Incoming**. My saved notes
lists only your own active saved daily/full-hitch drafts and corrections, not unsaved text in another tab.
View-only access gets the saved-reader action rather than a nonworking edit button.

The subject selector, **Export PDF (N)**, Refresh days, optional date/archive controls and Jump to day sit
above the actual days. The first day is substantially closer to the top in the tested phone layouts.
The original subject rule remains: saved department + normalised subject/vessel/site, not matching titles
or an invented project/topic model. Full-hitch records keep the existing ungrouped/period-start behaviour.

Same-account **Refresh days** preserves opened days, the number of loaded days, selected date/range and
reading anchor. Unchanged cards keep their nodes. **Back to Handovers** returns to the opened day and position;
opening a new editor deliberately starts at its form. Removing or reordering the anchor can limit exact pixel
restoration. State is held only during this current workspace/session, not promised across logout or reload.

A temporary retrieval error leaves the last overview labelled and its old record-opening actions disabled
until a successful refresh. Definitive denial/unavailability clears protected content. Late requests cannot
replace a different account, subject, route or editor. The legacy All saved handovers filter resets between
accounts/projects and has Reset filters; a same-account refresh preserves intended filters. An exact open
publication never silently switches to a newer revision.

## Export and save boundaries are unchanged

The subject journal exports the current permitted publications in the selected subject/date scope, with
chronological index and complete text. No private drafts/corrections, duplicate history, embedded file bytes
or visitor drawings are added; attachment references and separate signing reports remain. The 200-publication
and text-size limits remain explicit. This release does not redesign PDF pagination.

Notes, context, selected files and the next-shift choices are in-tab until explicitly saved, not autosaved
or durable offline drafts. Dirty-close, sign-out and retained-work protections remain. An uncertain save
retains its exact operation ID/payload for retry. Server conflict/ownership/source checks refuse an unsafe
new request without overwriting saved work. Finish does not complete Tasks, release equipment, acknowledge
for incoming people or prove physical attendance.

## One acceptance session

With fictional data and two named accounts, finish a day shift with a small photo. Read/acknowledge it as the
incoming person, use Start next shift, deliberately carry one permitted section, then save and finish the night
shift. Reopen the original account's full-hitch draft, set its period/recipients, add a disposable file and save.
Check another person's permitted publication, not their private correction. Expand an older journal day, read,
return, refresh and export the selected subject. Check the same route on a phone. Do not use valuable unsent
work to test discard or interrupted requests.

## Actual local verification

**920 selected Python tests and 124 compound browser checks passed**, plus syntax checking
of 76 JavaScript files and parsing of 193 application Python modules. The final ZIP replay reproduced
1823 tracked runtime files. Two application Python modules change; the other191 remain unchanged.
Only deploy/extract_source.py changes among existing executable repository files. C01/G01/Nginx are exact
baseline bytes. Approved Home/Tasks/Checklists/Logs code and layout are preserved apart from necessary shared
asset-cache references. Handovers and continuity Help changed;74 other article bodies and all76 catalogue
text/headings were checked. Native and master PDF guides were not rebuilt.

The new checks cover full-hitch atomic save/finish/files/privacy/context corrections, exact next publication
and selected carry, actor-bound proposals, duplicate/stale requests, unchanged retries, day/scroll restoration,
account filters and reading interruptions. Existing handover/day/copy/attachment/QR/signing-report suites and
selected approved-section, builder, sign-out, company/gateway checks were also run. Two fictional reports
were generated, rendered and inspected with their exact publication/acknowledgement/file reference checks.

Earlier failed/partial/superseded attempts are retained separately, not counted as passes. Browser tests use
actual assets, fictional TestClient APIs and injected fetch/hash/staged in-memory state: not real navigation,
durable IndexedDB, service-worker lifecycle or physical camera acceptance. No full-suite, live Sulmara/GitHub/
Render, Windows/PowerShell/native, full accessibility/security/load, Docker or accepted off-host recovery claim.
Use the separate verification report for exact counts, exceptions and file identities.

The wider roadmap and section-by-section process remain. First check this complete Handovers path, then
review the next agreed section rather than silently redesigning approved ones. No automatic background work.
