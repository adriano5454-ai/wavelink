# Wavelink UI21 — find drafts and continue the correct shift

**Core 1.34.19 · Workspace UI21 · Gateway G01 retained · 25 September 2026.**
Small changed-files GitHub patch for the **exact UI20 + G01** repository from this
conversation (supplied-UI18 lineage). It is not a complete repository or backup.

## What changed

Open **Handovers**. **Your saved daily drafts** shows your own active saved daily
shift drafts across dates, above the filters. **Continue my draft** re-reads the
exact record and opens Work & priorities without making another handover.
Unsaved browser-only text, archived entries, full-hitch drafts and colleagues'
private drafts are not part of this panel.

**Your department's day** now has Previous day / Today / Next day, a dated,
permission-scoped snapshot, and separate counts for your private drafts, records
with a publication and others' publications not acknowledged by you. These counts
overlap; they are not a total, a complete crew roster or a live completion report.
Changing context or a failed read clears the old snapshot rather than showing zero.

When several published shifts are available, **Choose previous shift** lets you
select **Start next shift from revision N** on the exact card. The page no longer
picks a source by latest publication time. A revised earlier shift is not necessarily
the next shift. The selected publication is read again; a changed revision must be
reviewed again, not silently substituted. Published views keep saved published dates
separate from the author's newer private draft dates.

UI20's automatic 12-hour/default, 8/6-hour/custom shifts, Start today, explicit time
basis and manual fallback remain included. No schedule or operational record is
created merely by browsing. A direct **Handovers help** link keeps an open editor.
Details and limits are in `docs/WORKSPACE_UI21.md`.

## Apply over the matching UI20 + G01 only

Preserve your approved commit, complete project backup, outside edits and unfinished
browser/separate-log work. From the extracted patch folder run:

```powershell
.\CHECK_UI21_UPDATE.ps1 -RepositoryPath "C:\path\to\wavelink" -Mode Baseline
```

The helper only reads expected file hashes. A mismatch means stop and reconcile.
It accepts explicitly listed UTF-8 CRLF-only differences, not modified code/binaries.
The PowerShell script has not been run on Windows here; equivalent exact/CRLF/tamper
reference cases are checked locally.

After the check passes, copy the **contents of UPLOAD_TO_GITHUB into the existing
repository**, keeping subfolders. Do not replace the repository, delete absent
files or copy the enclosing folder as a subfolder. Review, commit and push normally.
Use `-Mode Installed` to check the resulting target before deployment.

No new variables, dependencies, tables, migrations or deletions. Preserve:

```text
PUBLIC_URL=https://demo.mywavelink.com
DEMO_PUBLIC_ENTRY=YES
INITIALISE_FICTIONAL_DEMO=NO
```

Keep required access password, matching non-admin guest credentials, removed initial
admin bootstrap and persistent disk. **No reset, demo re-import or storage clearing.**
G01 root guest entry and normal staff entry are unchanged. Nothing was deployed here.

## Local validation and rollback

348 selected Python tests, 25 compound Chromium checks, 62 pure Node checks and
50 JavaScript syntax checks passed. Node cases overlap Python coverage; they are not
added to the Python total. All181 application Python files are unchanged and parse.
Four historical release assertions fail on untouched UI20 too; they are explicitly
excluded from the final selection, not passed. The create Help search-index mismatch
also predates this patch and remains a follow-up. Detailed evidence is separate.

Not full-suite, real-device, durable-storage, service-worker, hosted HTTPS, security,
accessibility, Docker or off-host recovery acceptance. Browser checks used injected
transport/storage; the actual separate Help-tab navigation was not accepted here.

For source rollback use your exact approved UI20 + G01 commit. Do not reset data or
restore an older full archive's gateway. The pristine-source recovery helper remains
unapproved for the overlaid runtime. Handovers shows UI21; Home remains UI13 and
Original Files UI19. Continue with hosted handover feedback before unrelated modules.
