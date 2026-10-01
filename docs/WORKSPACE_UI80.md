# Wavelink UI80 — Native Work Execution

**Date:** 1 October 2026  
**Required parent:** exact UI79 Native Equipment Records repository  
**Core:** 1.34.19  
**Runtime variant:** `workspace-ui80-native-work-execution-2026-10-01`

## Purpose

UI80 gives the five daily work-execution families one authoritative, route-owned presentation system:

- Tasks
- Maintenance
- Checklists
- Handovers
- Toolbox Talks

The change addresses the remaining mixed-generation styling in these routes without reviving the earlier
post-render decorator architecture. Existing services, permissions, record lifecycles, evidence, approval,
publication, acknowledgement, recognition and unsent-work behaviour remain authoritative.

## Architecture

The active application now loads one final work-execution stylesheet:

`app/static/work_execution_ui80.css`

Seventeen historical module styles are no longer linked by the active entry document or cached by the service
worker. Their required functional rules are retained under a legacy cascade layer inside the final asset, while
an unlayered UI80 section owns the final visual hierarchy. This avoids stylesheet-order fights without deleting
historical source from the reconstructed runtime.

Each route renderer marks its own final workspace directly with `data-work-execution`:

| Route family | Ownership marker |
|---|---|
| Tasks | `tasks` |
| Maintenance | `maintenance` |
| Checklists and checklist stage | `checklists` |
| Handovers | `handovers` |
| Toolbox Talks | `toolbox` |

There is no UI80 JavaScript decorator, shell replacement, MutationObserver-driven restyling, route animation,
new polling loop or DOM re-parenting layer.

## Active-style cutover

The following presentation files remain in source history but are retired from the active page/cache:

- `app/static/maintenance_workspace.css`
- `app/static/browser_toolbox.css`
- `app/static/handovers.css`
- `app/static/shift_workspace.css`
- `app/static/handover_workspace.css`
- `app/static/checklist_workspace.css`
- `app/static/checklist_forms.css`
- `app/static/checklist_review.css`
- `app/static/task_checklists.css`
- `app/static/toolbox_form.css`
- `app/static/task_create.css`
- `app/static/general_tasks.css`
- `app/static/task_workspace.css`
- `app/static/checklist_stage.css`
- `app/static/maintenance_forms.css`
- `app/static/maintenance_management.css`
- `app/static/maintenance_evidence.css`

## Runtime delta

- Modified runtime files: **8**
- New runtime/test files: **4**
- Removed runtime files: **0**
- Embedded UI80 records: **12**
- Parent manifest: **2,013** files
- Target manifest: **2,017** files
- Parent overlay SHA-256: `085d7d358ebdfdc4103e62c9a0a2eeb48112d54c0ee205dfcd7ada7e344a7468`
- Target overlay SHA-256: `0b86988da0ec10da579d4571d7cad950bc4aabc228b66e21ec5789b32d7e46d0`
- Target release-manifest SHA-256: `ef9e548efe548d0c93db5b74a8157bdff2848d3843c278f6a87c4fe015866419`

## Data and authority boundary

UI80 adds no database migration, destructive reset, account conversion, permission key, operational API,
recognition rule, source-completion adapter, environment variable or browser-storage writer. Opening, filtering
or refreshing a work route does not complete, approve, publish, acknowledge, assign or score work.

The Mail Startup M01 launcher remains byte-identical:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

## Local acceptance performed

The curated UI80 runtime was checked at 1440, 390 and 320 CSS pixels for all five route families. The browser
record reports 16 scenarios, no retired active stylesheet, left-aligned navigation, no document-level horizontal
overflow and no unexpected JavaScript error. A real-timer Tasks route remained open for more than 9.2 seconds
after settlement with zero workspace mutations.

The final repository/extractor package must additionally pass the included before/after verifier and a fresh
source reconstruction before release. Browser checks use fictional local data and are not live Render or
physical-device acceptance.

## Demo acceptance after deployment

1. Open Tasks, Maintenance, Checklists, Handovers and Toolbox Talks on desktop.
2. Confirm each route immediately appears in the current interface without briefly revealing an older layout.
3. Leave Tasks and Maintenance open for at least 15 seconds and confirm there is no route rebuild or flash.
4. Exercise one permitted and one denied action in every family.
5. Confirm draft, unsaved-work, approval, publication, acknowledgement and privacy safeguards remain effective.
6. Repeat the primary screens at 390 and 320 CSS pixels.
7. Confirm the sidebar remains left aligned and account/dialog layers stay above the workspace.

## Next development direction

The next release should complete the remaining native route/form cutover and shared editor/dialog system before
adding large new product features. The delivery includes a separate master future-improvements roadmap that
separates already requested work from recommendations and production-hardening gates.
