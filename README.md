# Wavelink — UI105

Choose inventory rows deliberately before import, search the mapped list by item name, serial or part number, and resolve original source-row conflicts while retaining the complete proposal. Sheet locations, combined inventories, native SN/PN fields, prior email/recovery/navigation and structured document workflows remain included. Core remains 1.34.19.

Read docs/WORKSPACE_UI105.md, docs/UI105_REVIEW_REPORT.json and the single docs/CONTINUATION_CHECKPOINT.md. The full repository ZIP contains all five source parts and the complete overlay chain. Copy the contents of REPOSITORY into the checkout root, preserving private settings and data. The compact update verifies exact UI103 or UI104 parent files before copying, then verifies the full UI105 target.

Docker reconstructs the app from vendor/source.part files and deploy/extract_source.py, then applies overlays through UI105 in order. Preserve existing environment settings and persistent data. See docs/COMPANY_C01.md for hosted boundaries. No migration, reset, dependency replacement or mail configuration change is required.
