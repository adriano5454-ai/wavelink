# Wavelink UI44 — Setup & builders for clean companies

**Core 1.34.19 · UI44 · Company C01 compatible · working G01 preserved · 26 September 2026.**

UI44 adds one permission-scoped browser workspace for creating or importing the reusable definitions a clean company needs. It is designed for empty COMPANY installations such as Sulmara, while remaining available in DEMO mode where the same permissions allow it.

## Setup & builders

Open **Setup & builders** from the main navigation or Home. The workspace shows only capabilities granted to the signed-in named account:

- Checklist templates — create from blank or import `.ajcheck`.
- Maintenance routines — create from blank or import `.ajcheck` as an unpublished routine.
- Toolbox-talk forms — create from blank or import `.ajtoolbox` as an unpublished form.
- Logbooks — design from blank or import `.ajlogs` definitions into a new logbook. Operational entries/history/media are not imported through this browser route.
- Inventory structure — create a new list/locations from blank or import a separate `.ajinventory`. Verification/custody history is not imported.
- Original files — opens the existing Original Files library when the account can view it.
- People & departments — remains an administrator action; it is shown as an onboarding shortcut for admins.

Every builder has a clear **Create new** and **Import** choice where supported. Imports are previewed before any save and use an idempotent operation receipt for retry safety.

## Permission model

Builder authority is **not administrator-only**. Five explicit permissions are added to the existing per-account permission policy:

- `builders.checklists`
- `builders.maintenance`
- `builders.toolbox`
- `builders.logbooks`
- `builders.inventory`

Existing non-admin accounts receive all five as **false** until an administrator deliberately grants them. Administrators retain full access. Each builder also requires its underlying viewing/editing dependency. A permissioned Technician or Supervisor can author/import the corresponding reusable definition without becoming an administrator or gaining access to Administration/Fleet.

Original Files keeps its existing permissions and administrator-only upload/folder controls; UI44 does not silently broaden those authorities.

## Clean-company boundary

Browser imports create new reusable definitions or separate clean structures. They do **not** import users, passwords, completed checklist records, signatures, inventory-verification history or log entries. Whole-project transfers, reusable setup bundles and operations workbooks remain advanced transfer/native workflows until separately reviewed for browser import.

A new company therefore does not need demo data. An administrator can create departments/accounts, grant builder permissions, and let the responsible people build their own operational definitions.

## Compatibility

UI43 handovers/day journal/PDF, UI34+ signing evidence, the C01 company startup/first-sign-in boundary, G01 demo entry, attachments, Tasks, Maintenance, Certificates, Toolbox Talks, Original Files, presence and support branding are retained. No new database tables, dependencies or environment variables are introduced.

Keep C01-compatible startup for company installations and UI34-or-later evidence writers. Do not reset/re-import a project to obtain builders.
