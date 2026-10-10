# UI104 — clear inventory import review

Core remains 1.34.19. This release follows the exact UI103 repository uploaded at GitHub commit 7e84154f8dbee41a195852ff9f0ad1bc1ef336dc. All 303 parent files were independently verified before development. Prior email, recovery, normal-tab navigation, inventory checks and structured document recognition remain included.

## Review each sheet and the destination

Choose **Setup & builders → Import a document**, read the workbook as Inventory, and select the item worksheets and their locations. Use **Check edited draft** after reviewing the mappings. The new overview shows the destination name, the number of item records being imported, and each sheet's location and contribution. Adding to an existing inventory also shows its current and proposed record totals and the locations being added.

These totals count item records, not stock quantities. A row can represent several units. Expand the identifier and quantity details to review missing serial or part numbers and Unknown expected quantities. Missing identifiers are allowed; an Unknown quantity is not zero. The source Excel Counted values remain old evidence, separate from Wavelink's current verification results.

## Catch overlapping source rows before Save

For an existing destination, checking the draft compares original document, worksheet and row references with its imported records. The overview lists the worksheet, original row, reviewed item name and reason for each conflict. Up to fifty row details are shown, alongside the full conflict count. This is a read-only review; nothing is added by checking the draft.

The entire batch remains blocked if source rows already exist, or if the original row evidence is missing for a worksheet that already contributed records. Choose distinct source rows or worksheets, preserve their original row evidence and check the current draft again. Editing a TSV alone may lose row references; do not guess row identities from item names. UI104 does not automatically discard rows or merge equipment by part number, serial number or name. Identical equipment identifiers can belong to distinct original rows.

The final save still rechecks current access and the destination version and retains its atomic conflict guard. A destination change elsewhere requires **Refresh inventories** and another review. Changing a mapping, sheet, location or destination clears confirmation. An uncertain save retains its identical receipt retry; existing items, verified counts, task scope, custody and schema remain in place.

## Continue using structured documents

Checklist and maintenance imports retain separate instructions, warnings, required tools, before/after stages and typed answer fields. Toolbox talks and logs retain their existing authoring flow. Review extracted proposals against the original document; source marks, answers and signatures never complete new work. UI104 improves inventory review rather than promising universal recognition or automatic kit relationships.

## Apply the release

The full repository ZIP includes every deployment file and the prior overlay chain. Extract into an empty folder and copy the contents of REPOSITORY into the Git checkout root, including its ignore files. Preserve .git, private settings and local data. Run the provided read-only verifier and review, commit and deploy through the existing workflow. The optional compact update applies only to the exact UI103 repository and includes a before/after verifier.

There is no SQL migration, data reset, browser-storage clearing, new dependency or mail setting required. The importer assets and shell cache have new versions; all 72 artwork files remain unchanged. Read UI104_REVIEW_REPORT.json for executed checks and limitations. No live deployment, SMTP, physical camera, actual service-worker upgrade, WebSocket or Windows display acceptance is implied by local testing.
