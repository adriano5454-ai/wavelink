# UI107 — review boxes and contents before importing inventory

Core remains 1.34.19. UI107 follows the complete UI106 repository uploaded at GitHub main commit a7e5d4dfac358744599939b1a861309476a1ccc3. All 321 uploaded Git blobs match the delivered UI106 repository. Earlier document interpretation, instructions/tools/answer choices, inventory row selection, SN/PN, worksheet locations, existing-inventory import and email/recovery/navigation work remain included.

## Read and map the workbook

Open **Setup & builders → Import a document**, choose the source and read it. Review each selected worksheet. Explicit box flags and parent references can identify an inventory table even when it has only a Name column alongside them. Parent and Parent ID remain supported labels; qualified English and Portuguese parent-box labels are recognized too. An unqualified Container ID, Container reference, Box reference or Caixa can mean the row's own identifier or its parent, so review the mapping notice and choose deliberately. Unmapped source columns remain in Notes.

Keep all desired sheets in one inventory with different worksheet locations, or append incoming items to an existing permitted inventory. Source Counted values remain source notes; verification is performed by the app. Unknown expected quantity remains Unknown, and zero remains zero. Repeated serial or part numbers are separate records unless you deliberately change the proposal.

## Correct boxes and their contents

Open the collapsed **Boxes and contents** editor for a worksheet. Search, inspect advisories and page through the rows. Correct the asset/tag reference, whether the row is a box, its parent-box reference or its expected quantity. A parent must be an included row explicitly marked as a box with a unique exact asset/tag reference in the same worksheet. Suggestions follow those requirements. Leading zeros, punctuation and case are significant. Choose no parent to clear a link, or retain a literal unmatched reference while correcting it.

The editor does not infer containers from formatting, names, serial numbers or part numbers. It does not link across worksheets or to an existing destination box. Import the incoming batch first and use the existing movement workflow for later placement where needed.

Self-links, cycles, duplicate box references, excluded or unmarked parents, excessive depth and invalid box quantities require correction before saving. A box accepts Unknown or one expected unit. The native hierarchy allows at most eight ancestor edges. Located messages use proven original Excel rows when available and otherwise identify the mapped row and worksheet.

A contained item inherits the location of its top box. The review and saved result now agree on that effective location. A different mapped location is retained in Notes as **Mapped location before containment**. This describes the current reviewed mapping, which may already have been edited; it is not a claim about an immutable original source. If retained Notes exceed the native limit, correct the draft rather than silently losing text.

Field edits preserve row order, source coordinates, row selection, Notes and other mapped values. An actual edit clears the previous approval and requires checking again. Opening, searching or paging the inspector and identical no-op edits preserve a checked proposal. Applying the mapping again replaces these mapped corrections; changing the full raw table resets provenance and selection with a notice. Wait for a pending or uncertain save before changing its proposal; retries preserve the original operation.

## Check and save

Compare the corrected rows, worksheet locations and effective box locations with the source, check the current proposal and confirm the summary. Appending preserves existing items, verification, task scope and custody. Source files are read-only; keep your copy. The importer records the filename and digest rather than uploading original bytes to Original files.

Checklist, maintenance and toolbox documents retain **Review source interpretation** and their existing editors. Compare instructions, required tools, printed answer choices and before/after stages with the source. For a toolbox talk, deliberately add retained instructions and tools to discussion prompts when needed. Recognition remains a proposal for review, not a guarantee of procedural correctness or universal document recognition.

## Apply the repository

Extract the full ZIP into a fresh folder and copy the contents of **REPOSITORY** into the checkout root. Preserve Git metadata, private settings and company data. Run the outer read-only verifier. The compact update supports only the exact 321-file UI106 parent and verifies the complete UI107 target after copying. All five vendor source parts and the ordered overlay chain are included.

Read **UI107_REVIEW_REPORT.json** for executed checks and limits. Local checks do not establish live Render/SMTP, physical camera, Windows display, actual service-worker upgrades, WebSocket transport or browser back/forward cache acceptance. No schema migration, data reset, dependency replacement or new mail configuration is required.
