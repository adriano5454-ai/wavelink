# Wavelink UI86 — Authentic Visual Covers

**Prepared:** 1 October 2026  
**Core:** 1.34.19  
**Parent:** exact cumulative UI85 repository  
**Runtime variant:** `workspace-ui86-authentic-visual-covers-2026-10-01`

## Why this release exists

UI85 replaced the contribution badges, but the surrounding application still used a generic cinematic Home illustration and older cover treatments. The Home screenshot showed a large detached greeting card, a dominant white company-logo panel and decorative offshore silhouettes that did not feel like a real survey operations product.

UI86 replaces those surfaces with a restrained, hand-authored technical-chart language. The artwork uses vessel outlines, navigation routes, acoustic geometry, AUV/seabed references and bathymetric contours rather than glossy or photorealistic generated scenes.

## Included

- A new technical survey-chart Home cover.
- An integrated dark Home heading instead of the generic white page-heading card.
- A compact company signature that keeps Sulmara visible without dominating the cover or repeating its name.
- A distinct, quieter Profile survey-chart cover.
- A vessel/AUV/seabed cutaway for sign-in and two-step verification.
- A subtle bathymetric-contour treatment for route-owned page headers and Original Files.
- Revised sign-in copy centred on people, equipment and evidence from shore to vessel.
- Four local SVG artwork masters plus one UI86 presentation stylesheet.
- UI86 service-worker cache replacement for the new artwork and revised application shell assets.

## Artwork method

All four illustrations are local, hand-authored SVG files. They contain no embedded raster images, remote URLs, font files, tracking resources or third-party art. Their paths are:

```text
app/static/art/home-survey-chart-ui86.svg
app/static/art/profile-survey-chart-ui86.svg
app/static/art/login-operations-ui86.svg
app/static/art/module-contours-ui86.svg
```

The artwork is intentionally technical and restrained. It supports the operational interface rather than becoming a decorative background that competes with work.

## Surfaces changed

- Personal Home cover and company signature.
- My Profile cover and displayed-emblem area.
- Standard sign-in and MFA sign-in cover.
- Route-owned page headers, including workspaces such as Tasks.
- Native Original Files header.
- Fleet receives the shared UI86 visual stylesheet for consistent route-owned header treatment.

UI86 does **not** redesign report PDFs, every module icon, every empty-state illustration or the public marketing site. Those remain separate visual-art batches and must not be described as complete because this release exists.

## Deliberately unchanged

- No database migration or reset.
- No operational API, permission or security-role change.
- No recognition, badge, threshold, points or contribution-adapter change.
- No company identity or logo change.
- No environment variable.
- No timer, MutationObserver, post-render decorator or shell re-parenting.
- No remote image request.
- Mail Startup M01 remains byte-identical.
- UI85 authentic badges, UI84 company terminology/Original Files, UI83 account security and UI82 search/action centre remain intact.

## Apply

Apply only over the exact UI85 repository. Copy everything from the release `UPLOAD_TO_GITHUB` folder into the Wavelink application repository, review each path, commit and push. Preserve the current UI85 commit as a rollback point.

UI86 has no schema migration. The cumulative UI83 account-security database boundary still applies: rolling back across UI83 requires the corresponding complete database backup and application commit together.

## Demo acceptance

1. Open Home and confirm the technical survey-chart cover appears immediately without the old white greeting card.
2. Confirm Sulmara appears once in a compact company signature and remains legible at desktop and phone widths.
3. Open My Profile and confirm the profile name, role and selected badge remain readable over the quieter chart cover.
4. Sign out and confirm the sign-in cover shows the vessel/AUV/seabed technical illustration and revised copy.
5. Open Tasks, Administration and Original Files and confirm the subtle contour treatment appears without changing their background hierarchy or control contrast.
6. Check 1440, 390 and 320 CSS-pixel layouts for clipping or document-level horizontal overflow.
7. Confirm no page blinks, re-parents controls or adds a second navigation surface.
8. Confirm badges, roles, permissions, points and company identity are unchanged.
