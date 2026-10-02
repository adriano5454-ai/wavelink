# Wavelink UI91 — Visual Continuity and Route Reliability

**Date:** 2 October 2026  
**Core:** 1.34.19  
**Parent:** exact UI90 Navigation Simplification and Route-theme Parity  
**Patch ID:** `workspace-ui91-visual-continuity-route-reliability-2026-10-02`

## Purpose

UI91 addresses three connected-test observations that remained after UI90:

1. **Team updates** still rendered a small nested heading inside an older recognition wrapper instead of using the same full route cover as Home/Profile-derived operational pages;
2. **Logs** had the same nested-heading problem in its catalogue and selected-logbook surfaces; and
3. selecting **Certificates** could appear to do nothing because hash-only navigation depended on browser/base-URL behaviour and the Certificate workspace did not paint route-owned feedback before the authorised read completed.

This is a visual-continuity and route-activation correction. It does not change operational records, permissions, data models, scoring, company identity or Report Branding.

## Team and Logs route ownership

Team and Logs now emit the final shared heading directly:

- one route category/eyebrow;
- one title;
- one concise description;
- one Help/action area;
- one full-width oceanic route cover.

The shared interface component no longer has to insert a second heading inside those pages. The catalogue and selected Logbook surfaces use the same route-owned structure.

## Certificate activation and feedback

The navigation shell now handles ordinary in-app `#...` links as explicit same-document routes. This prevents a stale `<base>` URL or browser quirk from turning a Certificate, Team or Logs link into a full-page navigation. The guarded Fleet hand-off remains separate.

Certificates now paints an immediate route-owned loading state before waiting for the service response:

- `Opening the certificate register…`; or
- `Checking the selected saved record…`.

The authorised Certificate API, permissions, saved records, version checks, operation receipts, local forms and refresh protections are unchanged.

## Visual architecture

UI91 extends the single active visual asset:

```text
app/static/visual_system_ui91.css
```

It does not load another competing theme and adds no:

- visual decorator;
- `MutationObserver` restyling;
- independent timer;
- shell re-parenting;
- secondary navigation frame.

## Mobile behaviour

Team, Logs and Certificates were checked at 1440, 390 and 320 CSS pixels. Their headings, controls, loading feedback and record surfaces remain inside the document viewport.

## Preserved boundaries

UI91 adds no database migration, operational API, permission key, recognition rule, company-identity change, Report Branding scope change, environment variable or local-storage clear. The M01 company launcher remains byte-identical.

## Acceptance after deployment

1. Open Team and confirm the heading is the same full-width route cover used by the other operational workspaces.
2. Open Logs and a selected Logbook and confirm no small nested banner appears.
3. Select Certificates from the sidebar and confirm immediate loading feedback followed by the register.
4. Repeat those paths at phone width.
5. Confirm Help opens separately and no page navigates to a browser error document.
6. Confirm Certificate create/edit/file actions still obey existing permissions and version/receipt safeguards.
