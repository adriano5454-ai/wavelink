# UI84 continuation checkpoint - Company Workspace, Branding and Original Files

**Date:** 1 October 2026  
**Core:** 1.34.19  
**Runtime variant:** `workspace-ui84-company-workspace-branding-original-files-2026-10-01`

UI84 is the current prepared baseline.

Completed:

- company-first deployment terminology in the active hosted interface;
- reviewed repository identity and local logo required for every COMPANY service;
- Sulmara primary transparent wordmark configured in the repository;
- full-wordmark-aware PDF cover/header rendering without duplicated company name;
- compact mark + controlled company-name behaviour retained;
- Original Files converted from a pop-out/dialog to the normal `#original-files` page;
- UI83 account security, UI82 search/actions and the M01 launcher preserved.

Important distinction:

- **Company/company workspace** is the hosted tenant and deployment boundary.
- **Project / job / project number** may still appear as operational record fields
  because a company can perform many survey or client projects.
- Internal `project_*` schema/API names remain for compatibility and are not a
  reason to expose the company service as a project in the GUI.

Connected acceptance before the next batch:

1. Confirm all company-level shell labels and warnings use company terminology.
2. Open Original files repeatedly at desktop and phone widths; confirm no dialog,
   duplicate shell or blinking appears.
3. Upload/preview a wide wordmark and verify the company name is not duplicated.
4. Preview a compact mark and verify the controlled company name remains present.
5. Confirm the Sulmara deployment header logo is legible at desktop and phone widths.
6. Confirm a company service with missing or mismatched identity/logo refuses startup.
7. Confirm UI83 MFA/session paths still work after the visual/copy update.

Next batched work should return to operational depth, offline/recovery and
real-device acceptance. Do not reintroduce a second shell, post-render decorator or
project-level tenant wording.
