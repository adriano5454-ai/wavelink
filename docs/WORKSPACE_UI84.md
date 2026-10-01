# Wavelink UI84 - Company Workspace, Branding and Original Files

**Date:** 1 October 2026  
**Core:** 1.34.19  
**Exact parent:** UI83 Account Security and Sessions Batch  
**Runtime variant:** `workspace-ui84-company-workspace-branding-original-files-2026-10-01`

## Purpose

UI84 aligns the hosted application with Wavelink's deployment model: one isolated
service, disk and database per company. The active hosted interface now describes
that boundary as the **company** or **company workspace**, rather than presenting
the selected company installation as a user-facing project.

Internal database keys, transfer formats and compatibility APIs that still use
`project` remain unchanged. Operational fields such as **Project / job** and
**Project number** also remain because they describe real survey or client work
inside the company, not the deployment boundary.

## Company deployment identity

Every COMPANY deployment must now have a reviewed repository-owned identity:

- exact `COMPANY_ID`;
- exact `COMPANY_NAME`;
- one bounded local PNG or JPEG;
- matching entry in `deploy/company_identities.json`.

Company provisioning and repeat startup fail closed when that identity is
missing, invalid or inconsistent. Browser values, Host headers and uploaded
records cannot select a deployment logo.

Sulmara is configured with:

```text
deploy/company_logos/sulmara/sulmara-primary.png
```

A separate deliberately fictional identity remains only for automated C01
provisioning tests.

The Wavelink product logo, installed-app icon and company report profile remain
separate identities. Adding a company logo does not rename records, grant access
or change report evidence.

When a configured company logo is available, the company site displays it once in
the shared header. A full wordmark replaces the fallback company-name text there,
so the header does not repeat the company name beside the artwork.

## Company-first interface copy

The active hosted shell now uses **Current company**, **Company workspace** and
company-scoped explanations across the main application and Fleet. This includes
account/session safeguards, saved-work warnings, administration, action summaries,
record registers and company-level imports.

Operational job/project fields are intentionally retained where they represent a
real job, contract or survey project. Internal variable and schema names are not
mass-renamed because doing so would create unnecessary migration risk.

## Original Files is now a normal page

**Original files** now owns the `#original-files` route and renders directly inside
the normal Wavelink shell. It no longer opens as a dialog or pop-out surface.

The page retains:

- exact source revisions;
- folders and history;
- permitted usage references;
- upload and revision flows;
- archive/restore safeguards;
- unsaved/busy exit protection;
- Help opening in a separate tab.

No new API, permission or database migration was added for this route change.

## PDF company report branding

UI84 corrects duplicate company names when an uploaded logo is already a complete
wordmark.

- Wide artwork (aspect ratio at least 3:1) is treated as a full wordmark.
- The PDF renderer displays that artwork once and does not print the controlled
  company-name text again beside or above it.
- Compact/square marks remain paired with the controlled company name.
- Aspect ratio is preserved on cover, header and continuation pages.
- Previewing remains unsaved and does not change company settings.

This is a layout rule only. Branding does not change the original record, author,
approval, restriction, signature or access control.

## No migration or authority change

UI84 adds no:

- database schema or data reset;
- permission or security-role change;
- operational API;
- recognition or contribution rule;
- completion adapter;
- environment variable;
- polling loop, MutationObserver decorator or second shell;
- automatic company creation or cross-company copy.

The UI83 account-security schema remains the newest database boundary. Databases
opened by UI83 or later must stay paired with UI83-or-later application software.

## Apply and accept

1. Preserve the current UI83 commit and complete database backup.
2. Copy the UI84 `UPLOAD_TO_GITHUB` contents over the Wavelink application repository.
3. Review every change, especially company identities and `company_provision.py`.
4. Commit and push normally.
5. After the intended company/demo service reports healthy, reload one tab once.
6. Confirm the sidebar says **Current company** and no deployment-level **Current project** remains.
7. Open Original files and confirm it is a normal page, not a dialog.
8. Preview a wide wordmark and a compact mark in Company branding.
9. Confirm the wide wordmark appears once while the compact mark retains the company name.
10. Provisioning tests for a new company must include a reviewed logo before first startup.

Do not clear browser storage, reset the company, re-import data or repeat company
setup merely to load UI84.
