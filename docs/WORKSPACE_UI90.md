# Wavelink UI90 — Navigation Simplification and Route-theme Parity

**Date:** 2 October 2026  
**Core:** 1.34.19  
**Parent:** exact UI89 Core Visual System Refinement  
**Patch ID:** `workspace-ui90-navigation-theme-parity-2026-10-02`

## Purpose

UI90 addresses two specific visual problems reported on the connected test deployment:

1. the top of the left navigation had become cluttered with a duplicate **Company workspace** heading and a second **Find a workspace** search even though Wavelink already has permission-aware global search in the product header; and
2. route-owned workspaces such as Tasks, Maintenance, Inventory and Administration did not yet share the established Home/Profile visual hierarchy.

This release is a visual/navigation correction, not a workflow or data-model release.

## Simplified company navigation

The sidebar now contains one compact company context:

```text
Company
Sulmara                         1 active
```

The redundant sidebar finder is removed. The permanent global search in the top product header remains the single search entry point.

On mobile, the same company context includes the navigation **Close** action. There is no duplicate Company workspace heading and no second search field inside the drawer.

The navigation controller continues to:

- show only permission-owned links;
- hide empty groups;
- preserve desktop collapse and mobile drawer behaviour;
- trap focus correctly while the drawer is modal;
- close after a mobile route selection.

It no longer has local search/filter logic and does not create, move or re-parent navigation links.

## Route-theme parity

Normal route headings now use one restrained dark oceanic cover language that matches the product system established by Home and Profile:

- Tasks
- Maintenance
- Checklists
- Handovers
- Toolbox Talks
- Inventory
- Certificates
- Administration
- corresponding Fleet route headings

The shared treatment covers page category, title, description, Help and route actions. Home and Profile deliberately keep their approved offshore image covers rather than being overwritten by the generic route treatment.

The existing approved module icons remain unchanged.

## Architecture

The active presentation asset is:

```text
app/static/visual_system_ui90.css
```

It contains the retained UI89 visual system and the UI90 navigation/theme additions in the same cascade layer. This avoids the important-layer conflict discovered during acceptance and avoids adding another separately active stylesheet.

UI90 adds no:

- post-render decorator;
- MutationObserver-based restyling;
- route animation;
- new polling timer;
- shell DOM re-parenting;
- database migration;
- operational API;
- permission, role or recognition change.

## Acceptance completed locally

- Exact parent/target repository verification.
- Fresh reconstruction from the pinned source parts.
- Byte-for-byte comparison with the prepared UI90 runtime.
- Static UI90 navigation/theme contracts.
- Chromium checks at 1440, 390 and 320 CSS pixels across Home, Profile, Workspaces, Tasks, Maintenance, Checklists, Handovers, Toolbox Talks, Inventory, Certificates, Original Files and Administration.
- Route-cover contrast and containment checks.
- Compact company context checks.
- Mobile drawer checks without the redundant finder.
- JavaScript syntax validation.
- Mail Startup M01 and repository-package regressions.

These are fictional local checks, not live Render or physical-device acceptance.

## Deliberately unchanged

- Company C01 identity and setup markers.
- Separate demonstration G01 data.
- M01 mail/startup forwarding.
- Existing database and operational records.
- Original Files, signatures and local unsent-work storage.
- Search permissions and result filtering.
- Report Branding boundaries.
- Home/Profile approved artwork and badge artwork.

## Next visual work

The next grouped visual pass should refine dense tables, filters, long forms and record inspectors without changing this shell/navigation baseline. Later passes still need state illustrations, report-cover refinement, physical-device testing, zoom/large-text acceptance and visual-regression locking.
