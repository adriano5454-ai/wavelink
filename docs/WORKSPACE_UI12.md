# Wavelink — Workspace UI 12

**Core 1.34.19 · cumulative UI01–UI12 · prepared 25 September 2026.** Implemented and tested locally. Not fetched from the live GitHub repository or deployed to Render.

## Scope and the Home page request

UI12 organises three existing Maintenance management forms: **Complete / Cancel work order**, **Cycle settings**, and **Stop pending follow-up**. The original fieldwork form, submit callbacks, request payloads, service permissions, revisions and local draft store remain unchanged. All application Python files remain identical to UI11.

**Home page improvement is now an explicit pending item in DEVELOPMENT_TODO.md and HOME_PAGE_IMPROVEMENT_PLAN.md. Home itself is not changed by UI12.** The direction is clearer daily actions, less clutter, clear personal/project scope, and a better phone layout, while preserving the visibility of unsent work and failures.

The package starts from the supplied complete UI11 ZIP. All 2,259 parent manifest entries were verified. It retains the inventory/category/box, Asset details, Record management, receiving, manifest, checklist and Help work. The existing domain and login remain unchanged. This is a browser update for computers and phones, not a native Windows release.

## Complete or cancel with a clear review

Open **Maintenance → an open work order → Review & cycle → Complete work order** or **Cancel work order**.

The guide uses **Saved work & note → Confirm completion** or **Confirm cancellation**. The first page identifies the exact order and equipment and shows the saved status/reviewed revision. Complete, Not applicable, unfinished and required-approval counts remain separate. **Review saved steps** expands the saved actor, time, status and evidence counts; inspect the actual readings and photographs in Work steps before closing.

The summary does not include unsent local results. A notice identifies existing matching local maintenance forms. Counts are not evidence verification or permission to complete. The backend still refuses completion when readings, photographs, steps, approvals or versions fail validation.

Enter a completion note (up to 2,000 characters) or cancellation reason (up to 1,000 characters), then review the status change, saved cycle and explicit effect before confirming.

**Completion** locks the saved order. A recurring order uses its existing cycle rules to create one successor with empty results, or retain a blocked follow-up for review. A one-off does not generate a next order. **Cancellation** locks unfinished work while preserving results/history and creates no successor. Cancellation is not a temporary pause or a completed inspection.

None of these actions verifies stock, changes custody, removes quarantine or authorises equipment use. The preview never manufactures a result or approval.

## Change a cycle without confusing the old and new schedule

Open **Review & cycle → Cycle settings**. The guide uses **Schedule → Change reason → Review cycle**.

The currently saved date and cycle are separate from the editable values. One-off hides inactive interval controls but retains their draft values. The final page shows **Saved schedule** beside **Proposed schedule** and the reason.

The original units/basis and due-date validation remain. Fixed scheduled dates require a due time. Completion-based cycles use actual saved completion; the preview does not invent a future due date. Unit-specific limits are still enforced by the server. Dates are UTC.

**Save cycle settings** applies to the current open order and future successors. An enabled cycle starts a fresh schedule anchor at this order. One-off stops future repeats without cancelling the current work. Neither browsing nor changing a schedule immediately creates another job or reminder.

## Stop only a blocked pending follow-up

For a blocked next order, use **Review & cycle → Stop pending follow-up**. The guide uses **Pending follow-up & reason → Confirm stop**. Review the saved pending date, state and explanation, enter a reason and confirm.

This stops the pending successor, not the completed predecessor. It does not erase evidence or mark new work as done. The separate **Review pending follow-up** release form is unchanged. Its procedure/assignee checks have not been removed.

## Review and draft safeguards

The existing **Keep draft & close** and **Discard draft** actions remain. Back retains values but resets acceptance. Resuming starts at the first page with the same fields and original reviewed revision, but no retained confirmation. A stale resumed form conflicts instead of silently using a newer version.

Changing a field after final review, including an autofill change without a normal input event, requires a new review. The original operation ID and unchanged-request retry protect against duplicate saves after a lost response. A local draft is not proof of a confirmed project action.

Open management forms retain the existing work-order navigation guard. The new helpers use no network calls and create no new storage or automatic queue. Desktop comparisons are side by side; narrow screens stack them. The existing guide keeps the action footer reachable while the form body scrolls.

Item approval, saved-photograph viewing, pending-follow-up release and linked-asset creation are not internally redesigned in this increment. Home remains pending rather than being declared finished.

## Help review

**Record maintenance work** now covers these closing, cycle-change and stop-pending guides. The other 75 instructional article bodies, native Help, original reference HTML and master PDF remain unchanged. The shared catalogue and section links reflect the reviewed article.

There are still three distinct articles with bounded wording reviews (daily, records and maintenance), not another completed article for every revision of Maintenance. HELP-04–HELP-10 remain partially reviewed or pending.

## Install with GitHub Desktop

Preserve unfinished Wavelink browser work, local uncommitted changes and the previous approved commit/recovery copy. Deploy outside a client demonstration. A source ZIP is not a backup of the current project data.

1. Open the existing **wavelink** checkout. Fetch/pull the intended branch after preserving local edits.
2. Extract this ZIP and copy the **contents of UPLOAD_TO_GITHUB** into the repository root, preserving subfolders. Do not copy the enclosing folder or delete `.git`.
3. Review the diff, commit and **Push origin**. Only **deploy/extract_source.py** changes among existing executable upload files relative to the supplied UI11 repository. Documentation and hashes also change. Reconcile any separate live or local edits before overwriting them.
4. Deploy the approved commit through the existing Wavelink Render service. Keep secrets, guest settings, disk and the current URL unchanged:

```text
PUBLIC_URL=https://demo.mywavelink.com
INITIALISE_FICTIONAL_DEMO=NO
```

The build should report:

```text
Verified upstream 1.34.19: 1605 tracked files.
Applied Workspace UI 12: maintenance closing and cycle reviews; includes UI01-UI11; no automatic data changes.
```

After a healthy deployment, open **Cycle settings** or a work-order closing form and look for **UI 12** inside the form. Core Wavelink remains **1.34.19**. Other workspaces retain their preceding badges.

No inventory upload, category reset, user reset or demo re-import is required. Never re-enable initialization or clear `/var/data` to change the interface. **Do not clear browser storage.** Preserve unsent work before reloading older tabs for a service-worker update.

## Acceptance and rollback

Use fictional data for testing: normal/guest login, a cycle change, cancelled work with retained results, a completed recurring order and a blocked-follow-up stop. Verify actual permissions, return navigation, draft resumption and restart persistence on a real phone and computer.

Revert the extractor commit to roll back, or use the exact UI11 extractor in **REFERENCE_ONLY/Workspace_UI12/rollback/deploy/extract_source.py**. Do not reset the persistent project. Preserve any unfinished forms before rollback.

The existing pristine-source recovery helper remains **unapproved for overlaid runtimes**. Do not bypass its verification to force recovery. Overlay-compatible off-host recovery, company isolation, full security acceptance and vessel/cloud synchronisation are separate pending work.

## Validation boundaries

Exact commands, test counts, initial findings, screenshots and final extraction checks accompany the package. Browser checks execute the real shipped scripts/styles with temporary fictional Wavelink services and controlled local transport; persistence is injected in memory. They are not screenshots of your live domain.

The full application suite, Docker image build, live GitHub/Render deployment, durable browser storage, off-host restoration, physical devices and full accessibility acceptance were not tested here. No production-readiness or vessel/cloud-synchronisation claim is made.

## Final selected local results

**512 distinct targeted Python tests and 108 compound browser checks passed**, with no failed, errored or skipped Python cases and no recorded browser errors in the final runs. All 42 JavaScript files passed syntax checks. The original UI10 harness expected pre-UI11 one-page forms; the same failure occurred on unchanged UI11. Its documented adapter uses the current guided navigation while retaining the scenarios. Final tests were repeated after a scoped checkbox CSS correction; earlier runs are retained and not counted twice.

Fresh final-ZIP verification is recorded separately; repeat tests are not additional distinct coverage.
