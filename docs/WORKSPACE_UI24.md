# Wavelink UI24 — handover drafting and review bundle

**Core 1.34.19 · UI24 · working G01 unchanged · 25 September 2026.**
A grouped update for the exact **UI23 + G01** repository from this chat. This is
an incremental patch, not the full source repository or a live-project backup.

## One workflow, several related improvements

In **Handovers → Continue my draft** (or **Edit private draft**), use **Review &
save draft** to open the Review tab. **Back to writing** returns to your last note
section. Neither button submits or discards anything.

The review combines **Draft when opened** and **Proposed on this device**:
complete title/type/location/period/time-basis details in a compact table;
seven note sections with changed sections expanded and cleared text identified;
and additions/removals of selected account and department IDs. The left side is
the saved draft loaded when you opened the editor—not a fresh hub read. Names use
the already-loaded directory; selected departments are not a live recipient roster.

**Details · Notes · Audience · Save controls** jump within the review. The Edit
buttons return to the exact fields/section without losing your wording or reason.
Expand/collapse only changes the view. The layout stacks on narrow screens.

The status strip distinguishes local edits, a reason entered but not sent,
a pending save, an uncertain response and a conflicting saved record. Counts
are editing indicators, not completed work. Reason-only edits also trigger the
existing discard warning. Keep an uncertain request open for **Retry unchanged
request**; the existing operation ID, payload and server conflict checks stay intact.

**Saving remains explicit:** give a reason, confirm and choose **Save private hub
draft**. It does not publish, acknowledge or change the previous-shift reference.
Unsent notes/reason are **in-tab only**, not durable offline drafts or autosaved text.

UI20 automatic shifts, UI21 saved-draft continuation, UI22 publication/acknowledgement
reviews and UI23 exact previous-publication reading remain included. These paths
were exercised together in a two-named-author day/night workflow. Full-hitch drafts
use the same draft review without inventing a schedule or predecessor.

## Apply over matching UI23 + G01

Preserve your approved commit, complete project backup, outside edits and all
unsent browser/separate-log work. In the extracted patch folder, run:

```powershell
.\CHECK_UI24_UPDATE.ps1 -RepositoryPath "C:\path\to\wavelink" -Mode Baseline
```

After a passing check, copy the **contents of UPLOAD_TO_GITHUB into the existing
repository**, preserving subfolders. Review the diff, commit and push using your
normal workflow. Do not replace the repository or delete files absent from the
patch. `-Mode Installed` verifies the copied target. Stop and reconcile a mismatch.

Nine changed/new repository files; the only changed existing executable upload
file is `deploy/extract_source.py`. No required deletions, database migrations,
dependencies or new environment variables. All 181 application Python modules,
G01 gateway, entrypoint, vendor source parts and startup rules remain unchanged.
Keep **DEMO_PUBLIC_ENTRY=YES**, **INITIALISE_FICTIONAL_DEMO=NO**, existing domain,
non-admin guest credentials, named administrator, disk and removed bootstrap.
No reset, demo re-import or browser-storage clearing.

## Validation and current status

**392 selected Python tests, 77 compound Chromium checks and 53 JavaScript syntax
checks passed** on the frozen extracted runtime. That includes a complete fictional
two-person day/night create/write/save/publish/acknowledge/next-shift path. 1,665
tracked runtime files are verified. Four historical assertions also fail on
untouched UI23 and remain excluded, not passed. Handovers/continuity Help and their
outlines/search are updated; 74 other article bodies are unchanged.

Tests use fictional data and controlled browser transport/storage. No full-suite,
physical-device, durable-storage, service-worker, live HTTPS, security/isolation,
Windows/PowerShell, Docker or off-host recovery acceptance is claimed. Nothing was
pushed to GitHub or deployed to Render here. Test evidence is a separate download.

Rollback using the approved UI23 + G01 source commit—not an older full archive or
data rollback. The pristine-source recovery helper remains unapproved for overlays.

**Next:** hosted handover feedback first. Group related improvements into fewer
substantial workflow releases, with integrated checks, before unrelated features.
See `docs/CONTINUATION_CHECKPOINT.md` and `docs/DEVELOPMENT_TODO.md` for the retained
roadmap and the implemented/tested/deployed distinction.
