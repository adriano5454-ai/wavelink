# Wavelink — private online demonstration

**Core 1.34.19 with cumulative Workspace UI01–UI08.** This update improves the standalone Checklist catalogue and reviews two related browser Help articles. Inventory, categories, Record management and shipments remain included.

Read [Workspace UI08 instructions](docs/WORKSPACE_UI08.md) and the [Help review checklist](docs/HELP_STANDARDISATION_REVIEW.md).

For the existing fictional project, keep the persistent disk, passwords, guest gate and **INITIALISE_FICTIONAL_DEMO=NO**. No reseed, inventory upload, category reset or project replacement is part of this update. The initial-administrator bootstrap variable stays removed.

The Docker build reconstructs the pinned original source from five parts, verifies it, and applies the checked cumulative overlay. Building never opens the persistent project. Do not bypass hash checks.

Against the supplied UI07 upload repository, only `deploy/extract_source.py` changes among existing executable files. The live repository was not fetched; review and reconcile outside edits before replacing files. Native Windows Admin is not updated by this browser package.

Runtime passwords, the current project database and current users are not shipped. Shared guest links remain fictional-demo access, not production SSO or company isolation. The pristine recovery helper remains unapproved for overlay recovery; do not disable its source checks.
