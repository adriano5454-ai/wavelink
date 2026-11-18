# Wavelink 1.34.47

## Safety and quality evidence

Reporters can select photos and documents when creating a safety and quality report. Authorized users can add evidence to an existing open, in-progress or on-hold report. The web and desktop report editors display the saved originals for authorized readers.

The supported formats are JPEG, PNG, PDF, DOCX, XLSX, TXT and CSV. Each report accepts up to six files, up to 5 MB per file and 10 MB combined. The application verifies filenames, contents and sizes before committing the report and evidence together. Report history records the addition. Reading an original requires current access to its report and a successful file integrity check.

## Work orders and builders

Work-order entry opens a maintenance form from the workspace or a linked equipment record when there is a published routine. With no published routine, the application explains what is missing and offers the available routine-builder actions according to the user’s permissions. The builders page offers a direct OpenAI action on each authorized checklist, maintenance, toolbox, logbook and inventory editor when the workspace enables assistance.

## Drafts and completion

Checklist, maintenance routine and toolbox authors can save partially written templates before review. Publication checks still validate the required fields and definitions. In an operational checklist, **Save draft** keeps progress on the current device while readings or required photos are pending. **Complete** checks the required evidence and readings before submitting the completed item.

## Build verification

This release derives from Wavelink 1.34.46 at commit `65d49a65617f538d60977f356cde186bdb62f399`. The build verifies the complete parent manifest before composing the overlay. The deployment manifest records the SHA-256 identity of every bundled resource. Release test results are in `DELIVERY_CHECKS.json`.
