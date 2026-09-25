# Wavelink checkpoint — Workspace UI08

Prepared 25 September 2026. Core **1.34.19**, cumulative **UI01–UI08**. Implemented and tested locally; not deployed to GitHub or Render. The live repository was not fetched.

Parent UI07 archive SHA-256 **c68220c0d93634d43e5dd24aa1190bea6f47947880c93728672ccf2adfad969a**; all **1,069 parent package entries** verified. Original five-part source stays pinned to **8c1b6a8d731d01b05a1290d3a1dd1a544054147aac9048ca345af7983613cd9e**. Final extractor SHA-256 **8e1e227c1b8b92dc515433183035adf021a6f4d7571d040cc1f8802cf8d940c9**.

UI08: standalone Checklist catalogue with saved-state filters, type/sort search, desktop summary beside list, phone detail/Back, separate local-work indication, contextual return and account/request-scoped refreshed reads. Selecting a summary is read-only; opening a stage uses its unchanged participant and synchronisation workflow. Individual working editors, item checking, evidence, approvals, readiness and finalisation retain existing services and payloads. Task-owned checklists remain in Tasks.

Two Help articles (`daily`, `records`) now reflect the current browser controls and distinguish retained records from native deletion labels. The other 74 instructional articles are unchanged. Shared Help viewer IDs/styles remain compatible; cache URLs update. Full Help wording, native/PDF, special entry points and accessibility remain partly reviewed or pending.

**84 incremental browser resources; 106 cumulative resources; 1,615 derived tracked files.** Existing app Python code is byte-identical to UI07. Against the supplied upload repository, only **deploy/extract_source.py** changes among existing executable files. Hosting/login/gateway/startup/Docker/dependencies/vendor/seed/recovery remain unchanged. No automatic data changes, reseed, category reset or source-file movement.

**464 distinct targeted Python tests and 95 compound browser checks passed; no failures/errors/skips in the Python results and no recorded browser errors. All 38 JavaScript files passed syntax checks.** A 21-check repeat waited for the real toast to dismiss for screenshots; it is not added as extra coverage. Final source remained unchanged. Initial findings and pre-polish runs are retained separately.

No full product regression suite, Docker build, live deploy, physical phone/Windows, real HTTPS navigation, durable browser-storage, off-host recovery or full accessibility acceptance is claimed. The pristine-source recovery helper is still unapproved for overlaid runtime; do not bypass its checks.

Use the complete ZIP's UPLOAD_TO_GITHUB contents in the existing Wavelink checkout. Preserve .git, outside edits, disk, credentials and **INITIALISE_FICTIONAL_DEMO=NO**. Preserve unsent work before deployment; never clear site data or re-import the demo. Exact UI07 extractor rollback included. Existing category assignments remain stored.

Next: remaining checklist working forms, maintenance interface, HELP-04–HELP-10; inventory/box/manifest/receiving feedback remains first. Original Files logical folders and wider hosted security/isolation/recovery remain pending. No vessel/cloud synchronisation or background automation is implemented by this increment.
