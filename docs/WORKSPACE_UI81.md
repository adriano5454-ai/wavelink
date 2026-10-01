# Wavelink UI81 — Workflow Foundation Batch

**Date:** 1 October 2026  
**Required parent:** exact UI80 Native Work Execution repository  
**Core:** 1.34.19  
**Runtime variant:** `workspace-ui81-workflow-foundation-batch-2026-10-01`

## Purpose

UI81 deliberately groups several closely related roadmap items into one coherent release instead of issuing a
sequence of tiny patches. It establishes one workflow foundation shared by the main Wavelink application and
Fleet:

- common form structure and validation semantics;
- one native-dialog controller with top-layer behaviour, busy protection and focus restoration;
- a direct account-menu entry for device-local unsaved work;
- the existing selective/batch-discard and recovery-copy workflow surfaced from that entry;
- Original Files presentation ownership consolidated into the final workflow stylesheet;
- mobile action areas, visible focus and reduced-motion support.

This is a presentation and interaction batch. Existing route services, permission checks, record state,
operational evidence, recognition, retry identities and device-local storage remain authoritative.

## Shared form system

`app/static/interface_components.js` now decorates detached route markup before mount with explicit roles:

- `data-wl-form-system="ui81"` on supported forms;
- consistent fieldsets, legends, required-field semantics and invalid states;
- status and error roles;
- common action groups and sticky save areas;
- desktop, phone and high-zoom behaviour.

The component remains explicit: there is no MutationObserver, periodic scan, submission handler, permission
rule or data writer in the form adapter.

## Shared dialog system

`app/static/dialog_system_ui81.js` is used by the main application, Fleet, local-work manager and sign-out path.
It provides:

- native `showModal()` top-layer behaviour;
- one dialog stacking model;
- title-first focus and opener focus restoration where the opener remains visible;
- busy-state protection for in-flight saves;
- no backdrop discard of working forms;
- accessible dialog labelling and status announcements.

It performs no API, storage or polling work.

## Unsaved work

The compact account menu now contains **Unsaved work** with a local count. It opens the existing protected local
work manager, which supports:

- select specific eligible entries;
- select all eligible entries;
- discard selected or all eligible entries after review;
- preserve unsettled/in-flight work;
- export a recovery copy;
- inspect connection/save state and separate log windows.

The count is derived from existing account-scoped local state. It does not count saved company records, other
accounts' private drafts or protected in-flight receipts.

## Original Files

The historical `original_library.css` file remains in cumulative source history but is no longer an active page
or service-worker stylesheet. Its required rules are retained in:

`app/static/workflow_foundation_ui81.css`

The Original Files renderer marks its direct workbench with `data-workflow-workbench="originals"`. No source-file
bytes, permissions, folder operations, revision history or API contracts change.

## Runtime delta

- Modified runtime files: **10**
- New runtime/test files: **5**
- Removed runtime files: **0**
- Embedded UI81 records: **15**
- Parent manifest: **2,017** files
- Target manifest: **2,022** files
- Parent overlay SHA-256: `0b86988da0ec10da579d4571d7cad950bc4aabc228b66e21ec5789b32d7e46d0`
- Target overlay SHA-256: `30bc56415df22bc83576b36924a078cda0305bf3de769dd5dc47ff914f2f9aa1`
- Target release-manifest SHA-256: `9a014c3006a60d537c0161e28b1699b1a670809ee5f4975b0206adfef21ee8b0`

## Data and authority boundary

UI81 adds no database migration, destructive reset, permission key, operational API, recognition rule,
completion adapter, environment variable, new timer, post-render decorator or new storage engine. The existing
local-work manager continues to use the established browser-local state transaction and save-receipt safeguards.

The Mail Startup M01 launcher remains byte-identical:

`2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371`

## Local acceptance

The dedicated browser record covers the main application and Fleet at 1440, 390 and 320 CSS pixels. It checks
native modal top-layer behaviour, required-field semantics, focus restoration, direct Unsaved work access,
selective/batch-discard controls, no document overflow and no unexpected JavaScript error. Retained UI80 route
acceptance was also replayed against UI81.

All browser records use fictional local fixtures. They are not live Render, real-account, physical-device or
independent security acceptance.

## Connected demo acceptance

1. Open the account menu and confirm **Unsaved work** appears without crowding the identity summary.
2. Create fictional local drafts in more than one supported family and confirm the count changes truthfully.
3. Open the manager, discard one selected eligible draft, then discard all remaining eligible drafts.
4. Confirm saved records and protected/in-flight work remain intact.
5. Open representative create/edit forms in Tasks, Maintenance, Checklists, Handovers, Toolbox, Administration,
   Inventory, Certificates, Faults/HSE, Logs and Fleet.
6. Confirm required fields, validation messages, action hierarchy and mobile keyboard behaviour.
7. Open and close dialogs repeatedly; confirm they remain above route content and focus returns to a sensible
   visible control.
8. Open Original Files and exercise browse, upload proposal, revision detail and cancel paths.
9. Repeat the primary paths at phone width and with reduced-motion enabled.

## Next batched development direction

The next batch should combine authorised search, notifications/action-centre foundations and remaining direct
route inspectors only after UI81 connected acceptance. Identity routing, two-step verification, SMTP/DNS inbox
acceptance, recovery drills and deeper operational enhancements remain separate security/production batches.
