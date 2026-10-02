# Wavelink UI89 — Core Visual System Refinement

**Date:** 2 October 2026  
**Core:** 1.34.19  
**Parent:** exact UI88 Mobile-first Visual Hardening  
**Patch ID:** `workspace-ui89-core-visual-system-refinement-2026-10-02`

## Purpose

UI89 is the first of several post-UI88 visual refinement passes. It does not claim that the visual programme is complete. It consolidates the actively loaded UI86, UI87 and UI88 presentation layers into one authoritative stylesheet and establishes a calmer, more consistent hierarchy for the application shell, route headings, Home, Profile and Workspaces.

## Active visual architecture

The main entry document now loads:

```text
app/static/visual_system_ui89.css
```

It no longer loads these three files as separate active cascade layers:

```text
visual_refresh_ui86.css
visual_reconciliation_ui87.css
mobile_foundation_ui88.css
```

Those historical files remain in the cumulative source lineage. Their required rules are retained inside the UI89 system; they are not deleted from history.

UI89 adds no JavaScript decorator, MutationObserver restyling, DOM re-parenting or refresh timer.

## Refined surfaces

- Product header and utility hierarchy.
- Left-aligned company/workspace navigation.
- Shared route heading, action and Help placement.
- Buttons, inputs, cards, notices and tabs.
- Home hero typography and operational overview cards.
- Profile identity, selected emblem and progress surfaces.
- Workspaces directory cards and responsive columns.
- Empty-state treatment.
- Desktop, phone and narrow-phone spacing.

The approved UI87 offshore art, UI85 badge artwork, UI88 mobile containment and existing module icons remain in place.

## Deliberately unchanged

- Database schema and records.
- Operational APIs and workflow states.
- Permissions, roles and company isolation.
- Recognition scoring, tiers and badge IDs.
- Report-branding scope.
- Company identity assets.
- M01 startup/mail forwarding.
- Local unsent-work storage.

## Acceptance completed locally

- Exact parent/target repository verification.
- Fresh source reconstruction from pinned source parts.
- Byte-for-byte comparison with the prepared UI89 runtime.
- UI89 static architecture tests.
- Chromium checks at 1440, 390 and 320 CSS pixels for Home, Profile, Workspaces, Tasks, Maintenance, Toolbox Talks, Inventory, Original Files and Administration.
- No tested document overflow, controls outside the viewport or unexpected JavaScript errors.

These are fictional local checks, not live Render or physical-device acceptance.

## Next visual batches

1. **UI90 — Records and data-density refinement:** tables, filters, master/detail inspectors, forms and Fleet parity.
2. **UI91 — States and visual language:** loading, empty, error, offline, attachment, evidence and report-cover art.
3. **UI92 — Real-device and accessibility polish:** landscape, keyboards, zoom, large text, camera/signature/QR paths and visual-regression locking.

English/Portuguese localisation remains a later functional batch, after the visual baseline is stable.
