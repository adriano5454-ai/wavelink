# Wavelink — UI110

Tasks now uses a compact list beside a current authorised summary, with an explicit action to open the full saved work. Maintenance titles select the summary; Continue work opens the exact work order. Phone Back controls preserve filters and selection. Core remains 1.34.19, and all UI109 import, email, inventory, recovery and navigation work remains included.

Read `docs/WORKSPACE_UI110.md`, `docs/UI110_REVIEW_REPORT.json` and `docs/CONTINUATION_CHECKPOINT.md`. The full ZIP includes all five source parts and the complete overlay chain. Copy the **contents of REPOSITORY** into the checkout root, retaining Git metadata, private settings and company data. The compact update supports the exact verified UI109 repository.

Docker reconstructs the app from `vendor/source.part*` and `deploy/extract_source.py`, then applies the ordered overlays through UI110. Keep the existing environment settings and persistent data. No migration, reset, new mail configuration or browser-storage clearing is required.
