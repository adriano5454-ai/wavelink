# Wavelink UI30 — support contact update

**Core 1.34.19 · UI30 contact update · UI29 handovers and working G01 unchanged · 26 September 2026.**
Compact update for the exact UI29 + G01 source from this chat, on the supplied-UI18 lineage.
Not a full application, live-project backup or Windows installer.

## New support address

**support@mywavelink.com** replaces the personal address wherever it serves as the
current program support contact: Contact display, Write email and Copy email controls,
clipboard fallback, hosted Help and search catalogue, original all-in-one guide,
native Help footers, checklist authoring previews, guide-generation scripts and
current support/readme material. The native contact window uses the updated branding
constant; a separately installed Windows program still needs its own updated build.
Your author credit and the rest of the contact wording remain unchanged.

Eight bundled PDF guide files are updated, including the master user guide and its
legacy filename alias. Both visible email text and clickable email destinations change.
Pages, bookmarks, reference links, metadata, historical instructions and version labels
are preserved. This is not completion of the wider Help review.

This does **not** change user login emails, passwords, customer/project records,
original uploaded documents, guest settings or the separate website sales contact.
Historical source/test snapshots and original vendor parts remain frozen as evidence.
No email is sent automatically. The mailbox must exist in your email service; this
patch does not create or verify it.

## Apply over matching UI29 + G01

Preserve your approved commit, complete backup and unsent browser/separate-log work.
From the extracted patch folder, run the included read-only checker:

```powershell
.\CHECK_UI30_UPDATE.ps1 -RepositoryPath "C:\path\to\wavelink" -Mode Baseline
```

After it passes, copy the **contents of UPLOAD_TO_GITHUB** into the existing repository,
preserving subfolders. Review, commit and push through your existing workflow.
Do not replace the repository or delete files absent from this small patch.
`-Mode Installed` checks the resulting source. Stop on a mismatch; do not bypass it.
The checker is not executed on Windows here; its hash/CRLF contract is checked locally.

No environment edits or database migrations are needed. Preserve
`DEMO_PUBLIC_ENTRY=YES`, `INITIALISE_FICTIONAL_DEMO=NO`, working credentials,
the separate named administrator, domain, disk and removed initial bootstrap.
Do not reset, re-import the demo or clear browser storage.

After your deployment finishes, use a fresh private browser window to open
**https://demo.mywavelink.com/contact** and confirm the address. Copy email should give
`support@mywavelink.com`; the visible email link should target the same address.
The shell/contact/Help asset cache versions advance; preserve unsent work before
reopening older tabs. Existing handover and other module badges do not all become UI30.

## What was checked

165 selected Python tests, 31 compound Chromium checks, 58 JavaScript syntax checks
and 182 application Python parses passed. The simple handover workflow and G01
regressions are included. Of 182 app Python modules, only branding.py and
checklist_preview.py change, by the exact email substitution; 180 are byte-identical.
All operational services, routes, handover scripts and account/storage formats stay intact.

The eight PDFs contain six unique document contents: every one of their 172 unique
pages was compared for exact text substitution, link preservation and rendered pixels
outside the email-containing line. Inline text following the longer address shifts
within that line; no page reflow. A second Poppler rendering of the contact page and
all unique guide footer crops were visually inspected.

Browser checks use fictional local APIs/in-memory persistence and simulated clipboard,
not real email delivery or full physical-device/durable-storage/service-worker acceptance.
The full product suite was not rerun. Previously documented historical release
assertions remain outside this selected run. Inherited contact styling/version labels
are unchanged; this is not a complete contact-page accessibility refresh.

Nothing was pushed to GitHub or deployed to Render here. Rollback is the approved
UI29 + G01 source commit, not a database reset. Keep current UI29 transfer safeguards.
The pristine-source recovery helper remains unapproved for the overlaid runtime.

**Next:** resume the simplified handover priorities and grouped workflow improvements.
Subtle project presence remains future work; it has not been implemented by UI30.
