# Wavelink UI87 — Visual Reconciliation

## Purpose

UI87 corrects the visual regressions visible after UI86. Two UI86 visual variants were prepared with the same release number, while an older deployment-branding script and separate icon maps remained active. The resulting browser could show Wavelink, Sulmara and a second Sulmara card at once; Profile could display a detached heading and unrelated route shortcuts; Maintenance and Toolbox Talks could retain older icons.

## Final ownership rules

- **Product identity:** Wavelink in the fixed top bar.
- **Company identity:** the current company name once in the left company context.
- **Home/Profile covers:** no embedded company logo or company-name card.
- **User-editable Report Branding:** supported reports and exports only; never the application shell, Home, Profile, sidebar, sign-in or deployment logo.
- **Profile route:** the Profile hero is the page heading. No detached `My profile` title card or generic Account/Team/Home shortcut row is inserted above it.
- **Icons:** sidebar and Workspaces cards use one stroke-line SVG family. Maintenance is a wrench; Toolbox Talks uses a hard-hat/toolbox-talk mark.

## Approved art

UI87 uses local WebP production assets derived from the user-approved offshore visual:

- `app/static/wavelink-approved-offshore-ui87.webp`
- `app/static/wavelink-approved-offshore-profile-ui87.webp`

The production crops contain no company wordmark, company card, UI text or remote asset request.

## Runtime

- Patch ID: `workspace-ui87-visual-reconciliation-2026-10-01`
- Parent: `workspace-ui86-authentic-visual-branding-boundaries-2026-10-01`
- Runtime manifest: 2,055 files
- Runtime including generated manifest: 2,056 files
- UI87 records: 13 (7 modified, 6 new)
- Database migration: none

## Acceptance

At 1440, 390 and 320 CSS pixels, verify that:

1. The top bar contains Wavelink and no visible Sulmara lockup/chip.
2. Sulmara appears once in the left company context.
3. Home contains no duplicate company card, company logo or Profile shortcut.
4. Profile contains no detached heading or shortcut row above its hero.
5. Tasks and other ordinary routes do not receive a stray `My profile` action.
6. Maintenance and Toolbox Talks display the new line icons in both navigation and Workspaces.
7. No document-level horizontal overflow or unexpected browser errors occur.

## Preserved boundaries

UI87 does not change accounts, authority, operational services, data, recognition scoring, badge IDs, report branding scope, C01/G01 separation, device-local unsent work or Mail Startup M01.
