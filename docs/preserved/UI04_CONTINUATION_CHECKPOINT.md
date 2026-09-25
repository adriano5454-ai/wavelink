# Wavelink checkpoint — Workspace UI04

Prepared 25 September 2026. Core 1.34.19; cumulative UI01/UI02/UI03/UI04. This session changes local package files only, not GitHub or Render.

Current priority: cleaner inventory navigation and improved Record management, followed by the existing agreed UI roadmap. UI04 removes the separate Up row, supplies named box breadcrumbs and view-aware Back within inventory, collapses categories beside Search, and separates single-click names from checkbox work selection. Record management now has grouped types, list/detail presentation, action-effect cards and the same guarded typed confirmation. Mobile uses a named return from detail to list.

Seven existing browser resources change relative to UI03. A scoped optional primary-name click flag is added to row_selection.js with its other consumers unchanged. Server lifecycle/category/movement/custody/permission services and data formats are unchanged. Original source parts, seed, hosting/gateway/guest authentication, environment and persistent disk handling are preserved. Categories remain explicit preview/apply, not automatic reseeding.

Full ZIP includes upload-ready repository files, readable source and diffs, exact UI03 extractor rollback, historical records and current validation. Against supplied full UI03, the only changed existing executable repository file is deploy/extract_source.py. No current live repository was fetched. Review the GitHub diff for any outside edits before copying.

Pending: actual Render/phone/browser storage and restart acceptance; cross-workspace return paths; remaining long inventory/movement forms; checklist/maintenance consistency; Original Files logical folders; broader hosted security/isolation/recovery; vessel/cloud synchronization. None is claimed complete here. No automatic schedule or background development task has been created.

Use README_FIRST and DELIVERY_CHECKS for installation and exact test evidence. Prior UI03/full-package checkpoints remain under REFERENCE_ONLY and docs/preserved; never reset the project to install UI04.
