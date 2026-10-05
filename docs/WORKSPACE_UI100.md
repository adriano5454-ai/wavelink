# UI100 — source-aware document imports

The old importer flattened descriptions and instructions into checks, ignored PDF form fields, and selected the first inferred PDF table. In the supplied four-page checklist this meant a date/time metadata fragment was suggested as a logbook and most of the document disappeared.

The new proposal reads document-wide evidence first. PDF checkbox/text/choice widgets are associated with positioned source rows, without their selected values; Word paragraphs and tables retain their source order. Text and table fallbacks identify purpose, instructions, warnings, tools, sections, check markers, explicit answer headings and before/after stages. Ambiguous prose is retained as information with a review note. Continued sections and grouped subchecks keep their context.

## Review and save

1. Open Setup & builders → Import a document and select your file or pasted text.
2. Review the destination. A checklist/maintenance PDF uses the whole document; Excel shows its real visible worksheets individually. Inventory/logbook sources can select a source table.
3. Review description, tools, instructions/warnings and workflow labels. Check each section and item. Open its details for group, source reference, guidance and answer fields.
4. Correct classification: move prose into instructions/warnings or move an answerable instruction into checks. Edit per-check stage, answer labels, units and choices. Add missing blocks or fields.
5. Check the edited draft, inspect the summary and explicitly confirm. Save the unpublished definition, then use the existing editor/publication workflow.

A checkbox confirms a check. Yes/No, Yes/No/N/A and custom options are actual reading choices; blank means unanswered. Choices do not assert completion. Text/numeric readings remain separate, and numeric minimum/maximum are optional. Limits are not inferred from units. Tools and instructions remain visible during work; Checklist/Maintenance reports include tools. Existing records retain their frozen source templates and answers.

The supplied PDF acceptance finds 3 sections with 22 + 27 + 7 checks, 6 tools, two stages, one post-only parent confirmation, battery percentage, Channel/Power fields and preserved group/manual wording. Recognition uses source labels and geometry, not a hardcoded document code or bundled template. Filled ticks, text answers, signatures and completed history are not loaded into the new definition.

## Update and acceptance

The cumulative ZIP accepts an exact UI98 checkout (GitHub main 80e9090500c33e80c97bcf2296c84d4772870e19) or exact prepared UI99. Run its before verifier, copy COPY_TO_REPOSITORY contents into the checkout, then run its after verifier. Review, commit, push and redeploy normally. Docker applies the pinned overlay chain through UI99 and UI100 once. No database migration/reset, access change, mail setting, fixture import or browser-storage clearing is required. UI98 hosted recovery and UI99 tabs are retained.

After deployment, import your original PDF and another representative source, review classifications/answer fields, save a draft and inspect it before publication. Check worksheet switching, your real report branding and installed browser worker update. See UI100_REVIEW_REPORT.json for exact executed checks and limitations.

Recognition is deterministic and local, with bounded extraction and OCR. Handwriting, damaged scans, rotated/irregular forms, merged tables and unusual section layouts still need manual correction. Approximate PDF text geometry is not an exact layout recreation. Empty response cells are preserved as definitions; unrecognized source material stays available in the complete extracted text. Original file bytes are not automatically stored in Original files. Native Tk changes parse but physical/native display acceptance remains pending; the test environment has no Xvfb. Browser tests suppress actual worker registration/WebSockets, so those lifecycle checks remain deployment acceptance.

Prepared and tested locally; no remote commit, pull request or deployment. Earlier GitHub integration writes returned 403. Detailed evidence is separate from the compact source update.
