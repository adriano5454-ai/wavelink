# Wavelink UI88 — Mobile-first visual hardening

## Purpose

UI88 is a focused responsive-layout release built after the UI87 visual reconciliation. It addresses the user-reported mobile failure where top-bar utilities, route actions, Profile content and Fleet controls could exist outside the visible viewport or behind clipped horizontal rows.

## Mobile ownership rules

- **Main top bar:** two rows below 760 CSS pixels. Product identity and essential utility icons stay in row one; Search receives a full-width row two.
- **Route actions:** route-owned actions become bounded grids. No invisible horizontal action rail is used for Tasks, Maintenance, Checklists, Handovers, Toolbox Talks, Inventory, Certificates, Fault/HSE or other covered headings.
- **Profile:** the identity and selected-emblem surfaces remain inside the cover; all three profile tabs stay visible at 320 CSS pixels.
- **Original Files:** its native dark heading remains readable and the workspace stays inside the normal application route.
- **Fleet:** status and account controls are compact, Fleet actions are bounded, tables scroll inside their own cards, and dialogs remain inside the visual viewport.
- **Safe areas:** top and bottom device safe-area insets are respected.

## Runtime

- Patch ID: `workspace-ui88-mobile-first-visual-hardening-2026-10-02`
- Parent: `workspace-ui87-visual-reconciliation-2026-10-01`
- Runtime manifest: 2,060 files
- Runtime including generated manifest: 2,061 files
- UI88 records: 8 (3 modified, 5 new)
- Database migration: none

## Acceptance

Main-application acceptance covers Home, Profile, Workspaces, Tasks, Maintenance, Checklists, Handovers, Toolbox Talks, Inventory, Certificates, Original Files and Administration at 430, 390, 360 and 320 CSS pixels. It checks every visible top utility, route action and ordinary interactive control for horizontal containment, plus the navigation drawer, account menu and Search dialog.

Fleet acceptance covers Sites, Manifests, Receiving, Assets, asset detail, item journey and Logbooks at 390 and 320 CSS pixels, including the navigation drawer and account surface.

## Preserved boundaries

UI88 adds no database migration, operational API, permission, recognition rule, environment variable, refresh timer, MutationObserver restyling, post-render decorator, shell DOM movement or browser-storage clearing. Report Branding remains report/export only. M01, company/demo isolation, saved records, signatures and local unsent work remain unchanged.
