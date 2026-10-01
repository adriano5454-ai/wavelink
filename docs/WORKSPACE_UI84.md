# Wavelink UI84 — Company Workspace Identity and Native Original Files

**Prepared:** 1 October 2026  
**Core:** 1.34.19  
**Parent:** exact cumulative UI83 repository  
**Runtime variant:** `workspace-ui84-company-workspace-identity-native-originals-2026-10-01`

## Why this release exists

Wavelink is deployed as a separate company service. User-facing tenant context therefore uses **Company** and **Company workspace**, rather than presenting Sulmara itself as a project. Internal IDs and operational fields such as **Project / job** and **Project number** remain unchanged because those can describe real customer work inside the company.

UI84 also makes company identity a required part of provisioning and converts Original Files from a popup into a first-class route.

## Included

- Company workspace terminology in the permanent shell, Home, Fleet and active operational/admin surfaces.
- Existing internal `project_name`, hub IDs, storage paths and API contracts retained for compatibility.
- Exact cleaned Sulmara PNG committed at `deploy/company_logos/sulmara/logo.png`.
- `deploy/company_identities.json` selects the code-owned identity by exact `COMPANY_ID`.
- COMPANY startup fails closed when its identity is absent, its name differs from `COMPANY_NAME`, or its logo is invalid/unavailable.
- The validated logo appears in the existing header identity surface and the Home cover; loading failure falls back to the company name.
- Original Files opens at `#original-files` as a normal native workspace page with a normal Back to workspaces action.
- Existing Original Files permissions, APIs, receipts, revisions, upload proposals and provenance remain unchanged.

## Deliberately unchanged

- No database migration or reset.
- No account, permission, role or recognition change.
- No operational API or completion-adapter change.
- No new timer, MutationObserver, decorator or shell DOM re-parenting.
- No public company-domain discovery or cross-company synchronisation.
- No change to operational Project / job or Project number fields.
- Mail Startup M01 remains byte-identical.

## Add another company

1. Add `deploy/company_logos/<company-id>/logo.png` (or approved JPEG).
2. Add the exact ID, company name and filename to `deploy/company_identities.json`.
3. Ensure `COMPANY_ID` and `COMPANY_NAME` match the entry exactly.
4. Run package and company-provisioning tests.
5. Deploy the separate company service with its own persistent disk and database.

Do not store customer data, passwords, setup keys or private originals in the branding directory.

## Apply

Apply only over exact UI83. Copy all files from the release `UPLOAD_TO_GITHUB` folder into the Wavelink application repository, review every changed path, commit and push. Preserve the current commit and a complete database backup as rollback points.

UI84 has no schema change, but the cumulative UI83 account-security database boundary still applies: databases opened by UI83 must stay paired with UI83-or-later software unless the corresponding earlier database backup is restored.

## Demo acceptance

- Sulmara is labelled as the company, not as a project, in the sidebar and Fleet context.
- The Sulmara logo appears in the header and Home cover and remains legible on desktop and phone.
- An unknown company identity refuses COMPANY startup before creating/resetting data.
- Original Files opens as a normal page; no dialog is open and browser Back/route navigation behaves normally.
- Existing upload, folder, revision and permission behaviour remains intact.
- Operational Project / job fields still exist where they describe actual work.
- No blinking, layout jump or horizontal document overflow appears at 1440, 390 or 320 CSS pixels.
