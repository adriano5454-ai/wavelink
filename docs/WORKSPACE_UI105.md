# UI105 — choose inventory rows before importing

Core remains 1.34.19. This release follows the verified complete UI104 repository. Current GitHub main was checked again: commit 7e84154f8dbee41a195852ff9f0ad1bc1ef336dc still matches all 303 UI103 files exactly. UI105 includes the intervening UI104 work. Use the full repository ZIP for a complete checkout, or the compact update with its read-only verifier against an exact supported parent.

## Choose the items you want

Open **Setup & builders → Import a document** and read the file as Inventory. Choose the item worksheets and their locations, then select a new inventory or an existing permitted inventory. Open **Choose items** for the worksheet being reviewed. Each row shows its source row, item name, serial number, part number and expected quantity. The separate **Mapped column preview** starts collapsed; open it to inspect every mapped column and Source Notes.

Search and filter the complete mapped proposal, then include or exclude individual rows. Excluded rows remain available to restore. Actions labelled for shown rows affect only the visible page. Searching, filtering and paging do not alter inclusion. The totals distinguish mapped, included and excluded item records; a record total is separate from a physical stock quantity.

A blank expected quantity stays Unknown and a confirmed zero stays zero. Missing serial and part numbers are allowed; check them against the source when those identifiers matter. Repeated PN/SN values on distinct source rows stay distinct. Previous Excel Counted values remain source notes, separate from the current Wavelink verification count.

## Resolve source overlap before saving

Use **Check edited draft** after selecting rows. For an existing inventory, the review identifies previously imported rows from the same original document and worksheet. Compare its source-row references with the chooser, exclude the old rows and keep the new ones you want. Check the changed draft again. The entire batch remains blocked while a duplicate or uncertain-source conflict remains; the application never silently removes rows or merges equipment identities.

The checkbox choices retain the full mapped text and original source references. Editing the full tab-separated text can invalidate original row references and requires checking the source again. Mapping changes keep selections only where confirmed original source rows support the match; otherwise the visible selection must be reviewed again. Missing row references are never fabricated from names or identifiers.

A selected item that explicitly belongs to a box must have that box in the selected set. Review any reported relationship error. A box is not inferred from indentation or appearance, and rows are not silently reparented.

## Check the current proposal

Changing item selection, sheets, locations, mappings or the destination clears import confirmation. Check and confirm the current proposal before Save. If the destination changed elsewhere, use **Refresh inventories** and review its current version. Pending or uncertain saves freeze proposal choices and retain their original retry operation. Existing items, verification progress, task scope, custody, permissions and schema remain in place.

Structured checklist, maintenance, toolbox and logbook imports retain their prior authoring flow. Instructions, tools, typed answers and before/after stages still require comparison against the source. This release improves inventory selection rather than claiming universal document recognition.

## Apply and review

Extract the full ZIP into a new empty folder. Copy the contents of REPOSITORY into your checkout root, including its ignore files, and preserve Git metadata, private settings and local data. Run the outer read-only verifier, review the changes and use the existing commit/deploy workflow. A push may trigger Render's automatic deployment. The full source parts and complete overlay chain are included; an unpacked runtime is not a replacement deployment repository.

The compact update supports exact UI103 and UI104 files, with before/after verification. Read UI105_REVIEW_REPORT.json for the checks actually executed and their limits. No live Render, production SMTP, physical QR device, Windows display, actual service-worker upgrade, WebSocket transport or BFCache acceptance is implied by local tests.
