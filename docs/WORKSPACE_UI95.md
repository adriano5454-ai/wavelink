# UI95 — document imports and reliable Toolbox navigation

This update builds on the exact GitHub UI94 main commit c3fcc81eac8a8e67cbb608efd91e734797136b89. UI93 optional email and UI94 header/account/art fixes remain included in the build chain. Core stays 1.34.19.

Toolbox Talks now paints when its screen is no longer mounted, even when the response is unchanged. Existing account/route/dialog guards still reject late reads, and unchanged background polls preserve a mounted view. The duplicate Assigned to me sidebar button is removed; Home, My actions and the existing assignment-opening helper remain available.

Setup & builders now has Import a document. Its existing Import existing cards accept source documents as well as their existing Wavelink packages. PDF, DOCX, XLSX/XLSM, CSV/TSV, TXT, Markdown and single-page PNG/JPEG/TIFF/WebP are supported within published limits. Copied document text can be used directly. This is deterministic extraction and editable mapping, not an AI service or a promise to decipher every layout.

The source is read locally in a bounded subprocess. PDFs use pypdf 6.19.0; scans use Tesseract and Poppler. Docker installs English and Portuguese OCR data. Desktop/server installations outside Docker need those OCR programs separately; other document formats work without them. Current local OCR acceptance covers English images and scanned PDFs. Portuguese OCR data installation is configured in Docker, not claimed as locally tested here. No source is sent to an external document service. One extraction runs at a time, with time, memory, expanded-ZIP, XML and output bounds; Office formulas, macros, queries, links and objects never execute.

Each visible worksheet/table is named separately with its source-row count and suggested content type. Choose one per import; sheets with different purposes become separate imports. Hidden worksheets are named in notes and skipped. Inventory maps headers to name, reference, serial, model, type/subtype, quantity, unit, location, notes, explicit box flag and parent box reference. Review the mapped table and edit the full rows if needed. Changing column choices requires applying the mapping before review. Unknown quantities stay unknown; invalid box references/cycles/depth or invalid row values are rejected before any list is created.

Checklist/routine proposals use editable section-and-check outlines. Toolbox forms require reviewed prompts, understanding questions and an acknowledgement declaration. Logbooks use editable fields, without source operational entries. Source filename/hash and selected worksheet are retained as provenance. Original source bytes are temporary and are not saved to Original files automatically; keep/upload that source separately if needed and permitted.

Check edited draft validates the exact fields. Any edit invalidates the review and confirmation. Saving requires explicit confirmation and a current named destination permission. Source/draft receipts are scoped to the hub/account/credential version. A retry with the same operation returns the saved result; changed contents with an old review/operation are rejected. Lost-response inputs are frozen for Retry unchanged request. Existing records, permissions, publications, signatures, verification and Fleet custody are not merged, signed or inferred by this flow.

## Applying the update

Use the compact UI94_to_UI95 ZIP. Run its verifier in before mode against your checkout, copy the contents of COPY_TO_REPOSITORY into that checkout, and run after verification. Commit/push through your usual GitHub workflow. Do not import fixtures, reset the project, clear browser data or repeat setup. Docker retains the original UI92 extractor and runs UI93, UI94, then UI95 once each. requirements.lock adds only pypdf; OCR programs are installed in the Linux image. Existing private email settings stay out of GitHub.

## One acceptance session after deployment

1. Sign in with the intended builder permissions. Visit Toolbox Talks, Home, Profile, Tasks and Logs, returning to Toolbox Talks each time. Confirm its list opens without needing Refresh. Keep an open local form intact.
2. Confirm Assigned to me is absent from the sidebar and assigned issues still appear in Home/My actions.
3. Import a non-sensitive workbook with two inventory sheets and one log sheet. Check sheet names/counts/types; map the inventory header, choose one sheet, correct rows, and review/confirm. Open the saved separate inventory; confirm other sheets and existing lists were not merged. Import the log sheet separately as empty definitions if desired.
4. Import one ordinary Word checklist, one searchable PDF and one clear scan. Compare all extracted wording/numbers/units against their originals. Correct the proposal and save only the intended reusable draft. Check its separate publication controls.
5. Repeat the import view at desktop/tablet/phone widths. Close or save the proposal before navigating. Use a fictional lost-response test in a separate test workspace if needed; never repeat an uncertain production save with changed inputs.

Current evidence and explicit limits are in UI95_REVIEW_REPORT.json and the separate evidence ZIP. Linux headless viewport checks do not establish physical-device, Windows GUI, real service-worker lifecycle, production WebSocket, actual Docker/Render deployment or live email delivery acceptance. The earlier historical full-suite assertion failures remain documented in UI93/UI94 reports; this release does not claim a green full historical suite.
