# Wavelink checkpoint — UI47 + Company C01 + working G01

27 September 2026. Core1.34.19. User approved Home and the complete UI46 Tasks review.
One Tasks workflow batch, not a basic replacement: preserve all four cards, exact stock scopes,
checklists, lifecycle/privacy/QR/report functionality. Approved Home remains unchanged.

## Exact source
UI46 from actual uploaded UI30 repository plus verified UI31–43/C01/UI44–46 lineage.
144 parent repository files /1795 parent runtime hashes verified.
Parent extractor 4840018d682133736b820bc61ad185e66bb74e16406aabdf913820f6e3024243.
UI47 extractor 52bb01721e148714cd9c8d908263d18ade5341095629eceda17f8a390b22ad9a.
Patch ID workspace-ui47-tasks-workflow-2026-09-27.
96 incremental resources /479 cumulative overlays /1803 derived runtime files.
C01 entrypoint f754d4db367983a75473f1d525183b618a25c265837a317df66ffabaf8f4c1e2;
G01 gate 9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701;
Nginx 752563759fd82e20eacc62379f7a3082a8074675a747214a16cff0b9b90b99b8 unchanged.
Only changed existing executable repository file deploy/extract_source.py.

## Implemented
Admin My tasks now true assignee scope; All accessible retains authority. Direct My/All/Review/
Completed/Postponed, searchable compact cards, readable UTC/clock-based overdue. Full filters/reset,
account/project scoped state, same-account refresh retains choices. Review is initially undecided;
no automatic completion. Overview foregrounds instructions/next action, expandable facts/progress,
all checklist/work/discussion/link/history/PDF/management controls retained. Current task forms
and integrated two-author submit/return/correct/complete behaviour exercised.

Inventory creation single page What/Who/Scope, searchable retained people, six base scopes/three
box modes. Fixed scope and partial-container movement rules preserved. Stored optional preview
snapshot and attempted payload are not silently rebased on resume. Deliberate Refresh scope preview;
server compares exact expanded IDs. Original operation ID/payload shape retained for unchanged retry,
including older requests omitting new optional expanded preview. New task navigation waits for save
and local-draft cleanup. Phone item cards, desktop table, find/filter cannot reduce completion gates.
Found/Missing/Discrepancy remain; no bulk verify. Successful move/check and scope-denial tests retained.

Date-only/unchanged or raised priority with same people needs no generic reason. Changed people or
lowered priority still needs one. Own never-submitted/unmoved stock-result correction reason-free;
other/unknown author, submitted/moved evidence and substantive exception notes retain requirements.
Standalone inventory correction policy unchanged. Real actor/time/version/before-after audit,
no fabricated explanation. Published/closed lifecycle and no-op permission/version checks retained.

Task delayed reads capture actor/token/route/view/modal generation, including intervening closed editor.
Before-send guard after lease renewal prevents replacement-account submission. History/PDF cannot
replace active work. Task-local drafts, global local manager, sign-out same-account recovery and
source/checklist protections preserved. No new API route, table, permission, dependency, environment,
browser store/version or native binary. Optional metadata is inside an existing local-form value.

Only app/work_tasks.py (list,create,check,reassign) and app/inventory.py (check_item) change;
191 other Python modules unchanged,193 total. Shared app.js function declarations/fieldwork writer,
Home files, task_checklists/verification modules, operational authority and C01/G01 files unchanged.
New task_workspace.js/css; operations/general_tasks/task_workflow presentation/guard changes audited.
Tasks and General Tasks Help/outlines updated;74otherbodies unchanged,76catalogue matches. Native
master guides not rebuilt; no general Task attachments/recurrence/edit-instructions/batchPDF/QR claim.

## Completed selected checks
690 Python = 282 Tasks +44 Home/attention +186 retained authoring/local work
+71 C01 +107 demo/gateway/provision/package. 111 compound browser checks include
31 complete Tasks/stock cases,16 retained creation/checklist cases,8 postpone/resume cases,
15 Home,19 shortcuts,9 builders and13 sign-out.10 pure Node assertions overlap one Python case.
73 JavaScript syntax checks/193 Python parses. Final ZIP replay/hashes separately verified.

Initial broad attempt included native Tk cases with no display (34 errors) and historical release
assertions:26 also failed on untouched UI46; one old work_tasks never-changes invariant is deliberately
superseded. Not counted as passes or broadly repaired. Initial Help article attribute-order replacement,
Playwright pending-function monkeypatch and simulated-route/teardown fixtures corrected before final
freeze. Earlier partial and complete superseded runs retained/excluded. A final stock-search touch-control/
preview-scroll refinement was refrozen; all chosen tests rerun after that refinement.
Actual assets/fictional SQLite+TestClient/injected fetch/hash/in-memory state, not durable IndexedDB
or normal navigation (policy restriction not bypassed). Per-task PDFs rendered and visually inspected;
no report source changed. No fullsuite/liveHTTPS/physicalcamera/SW/WindowsPowerShell/native/fullsecurity/
accessibility/load/Docker/offhost acceptance. No live data, credentials or remote operations.

## Preserve and next
Preserve independent Sulmara C01 company identity/domain/activated disk/marker and existing G01 demo,
current permissions/accounts, bootstrap removal/INITIALISE_COMPANY=NO after activation, initial demo
import OFF, approved commit/backups/.git/outside edits and unsent work. No reset/reimport/storageclear
or incompatible pre-C01/pre-UI34 writer/exporter rollback. UI46 source rollback brings old Tasks/reasons
back; protect retained scope/ownership metadata first. Cannot restore deliberately discarded local work.

Compact GitHub changed files; copy/review/commit/push. Optional read-only PS1. Evidence separate.
Next one named-manager/worker fictional Task+inventory exception/review/PDF/phone acceptance session;
then next agreed section review, not automatic unrelated implementation. Larger roadmap retained.
Task files, recurrence/reminders, multi-links/instruction revisions/subtasks/combinedPDF and Task QR
remain future, not hidden working controls. Nativevessel/CCVD/cloudsync/localnetwork outside this batch.
No automatic background work or assumption that the live service matches the prepared release.
