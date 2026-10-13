# UI114 — review mapping across worksheets

Core **1.34.19**. Built from exact verified GitHub UI113 commit `59516b37dcc3a4b3d5e48269872f03d4ce8c1dbf`. Earlier workflows and safeguards remain included.

## Find the worksheets needing attention

Each card under **Worksheets to import** now shows its current mapping state and row choices. The included-worksheet summary names pending mappings that prevent a new check. Apply them, or use **Restore last applied mapping** where available. Missing Name and malformed-choice notices are separate mapping advice. A missing source Name column does not automatically invalidate manually edited rows; compare them with the source and use **Check edited draft** for the authoritative review.

An applied mapping record is shown only when its source-associated record is valid. Clean older drafts without a record remain explicitly unavailable for Restore and are not guessed from corrected rows.

## Filter the cards without changing the import

Use **All worksheets**, **Included** or **Needs mapping**. These filters hide cards in place. The original worksheet choices, locations, row exclusions, corrections, inspected worksheet, completed accepted or blocked check, confirmation and retry request stay intact. Filtering makes no API request. The checkboxes still decide what is imported.

Needs mapping includes excluded worksheets too. An excluded pending mapping does not block checking the selected proposal. Filtering may hide the worksheet currently being inspected; its context and selector still identify it. Use **Inspect mapping and items** on a visible card to inspect that worksheet. Existing Worksheets, Mapping, Items, Boxes, Source and Import overview shortcuts remain available.

Statuses and filter membership update after mapping/header changes, Apply, Restore, inclusion and item-row changes. If the focused card becomes hidden, focus moves to the active filter. Busy or uncertain requests lock filters and inspection. Resolve an uncertain result with **Retry unchanged request**, which keeps its original operation ID and payload. Controls captured from another source, worksheet, import type, repaint or session cannot alter the current form.

## Apply and check once

Copy the **contents of REPOSITORY** from the full package into the Wavelink application repository root, preserving Git metadata, private settings and company data. The compact update supports only the exact verified UI113 parent. Docker applies UI114 after UI113. No reset, re-import, schema/dependency change or browser-storage clearing is required.

Use one representative workbook: check and confirm the proposal, then use each worksheet filter and inspect another worksheet. The check and confirmation should remain. Change an included mapping and find its name under mapping attention; apply or restore it, then check again. Change an excluded sheet's mapping on disposable data and verify it does not block a fresh check of the selected proposal. Preserve genuine unsent work.

The earlier MR07 inventory workbook was read privately: five visible sheets, four classified Data and one Summary. UI113 and UI114 produce a byte-identical initial selected import projection (220 rows); reading preserved the original file and every temporary native SQLite table. This comparison does not approve actual quantities, worksheet intent or saveability. Source rows and the original workbook are excluded from evidence.

Read `UI114_REVIEW_REPORT.json` for executed checks and limits. Browser tests use fictional workbooks and temporary C01 databases. Physical devices, live mail, worker upgrades and production synchronization need their own acceptance. GitHub rejected branch creation with 403; this release was not pushed or deployed.
