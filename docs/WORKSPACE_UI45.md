# Wavelink UI45 — revisit builders and simplify sign-out

Core **1.34.19** · UI45 · Company C01 and demo G01 retained. Prepared 27 September 2026.
Exact baseline: **UI44 + Company C01** from this conversation. This is a changed-files patch,
not a complete repository, database backup or a deployed service.

## Update using GitHub Desktop

Extract the ZIP. Copy **everything inside UPLOAD_TO_GITHUB into the existing Wavelink application
repository folder**, replacing matching files. Review in GitHub Desktop, commit and Push origin.
Do not replace the repository or delete files absent from this patch. Not Wavelink-Website.
The optional CHECK_UI45_UPDATE.ps1 checks hashes only; it is not an installer or required upload.

The demo and Sulmara can use the same repository. Review each service's existing auto-deploy setting:
a push can deploy both. No live GitHub/Render action was performed here. Preserve backups,
current C01 activation marker/dedicated company disk, G01 settings and all unsent work before updating.
No environment variables, dependencies, APIs, permissions, SQL tables or browser store versions change.
Do not reset/re-import a project, clear site data, copy demo credentials into Sulmara or repeat setup.

## What the review corrected

UI44's Logbooks Create shortcut called a nonexistent local create function. Its toolbox editor still
had an administrator-only front-end gate despite the new saved builder permission. Both paths now
open their actual editors for appropriately permissioned named accounts. The backend still verifies
current authority; no user is automatically granted access.

Each available card separates **Create new · Import existing · View saved** and shows its accessible
saved count. These counts are not proof the whole company is empty or operationally ready. A focused
create/import screen replaces the card grid while working. Saving/importing gives an explicit result
and opens the exact saved definition or inventory, rather than sending you to an unrelated list.
Checklist/maintenance initial creation opens Sections & steps. Toolbox keeps its structured prompts
and questions, and Logbooks keeps its useful structural designer; the wizards are not replaced by
basic text boxes. Original files and People & departments keep their existing authority boundaries.

For unpublished checklist, maintenance and toolbox definitions, initial creation and routine draft
saves have no generic reason or confirmation checkbox. A draft is still unpublished. Published-source
corrections, publication and lifecycle actions retain the applicable explanation/review controls.
Toolbox draft completeness and numeric-reading limits still apply. This is not automatic approval.

## Imports stay deliberate

Select the supported Wavelink package, **Check file**, review what will be copied, then Import.
A failed preview clears old results and can retry the same selected file. A lost committed response
keeps the original operation/file/review for **Retry unchanged request**; fields lock while sending.
Changing account, route or editor blocks a stale save before sending. No import occurs by browsing.

Formats remain .ajcheck, .ajtoolbox, .ajlogs and .ajinventory, up to the existing 12 MB bound.
Checklist/routine/toolbox imports are unpublished. Logbooks import definitions, not operational
entries/media/history. Inventory packages can include item rows, not verification/custody history.
No accounts, passwords, signatures or completed checklist history are imported. PDFs/Office files
remain sources in Original files, not automatic definition conversions. Advanced whole-project,
setup-bundle and workbook transfers remain separate. No new example-download pack is claimed.

## One useful sign-out warning, not a draft blockade

Use **Account → Sign out**, or the **Sign out** control in an open main-workspace dialog.
A clean session signs out directly. With local entries or an open editor, one warning offers
**Stay signed in** or **Keep stored drafts & sign out**. No typed reason and no requirement to open
all drafts first. Cancel leaves the working editor in place. Account tools no longer overwrite it.

Stored local operation forms, log/checklist drafts, new-checklist drafts, queued results, receipts,
snapshots and unknown JSON fields remain. Existing operation-form draft flush is called before
logout. A small optional signedOutWorkOwner marker in the existing main record protects resumption:
**sign back in with the same named account** to continue or use Manage unsaved work. Another account
is refused while protected local work remains; use a separate browser profile/device for that account
or return as the original account to resolve/discard its entries deliberately. This is not a new
multi-account draft vault or secure erasure of browser storage.

**Unsaved text held only in an open editor is not a stored draft.** The warning states that it can be
lost on confirmed sign-out. Stay signed in to save it first. Separate log-window/native/other-device
stores are not cleared or comprehensively counted. Hub-saved private handovers, publications, files
and signatures are not deleted. Sign-out does not finish a handover or cancel an already-sent save.

Already-active saves and file preparation must settle first. New writes/queue delivery pause during
the confirmation. Failed local persistence or a changed write lease refuses completion and keeps the
work for retry. Local auth removal plus the retained-work marker commit in one existing-state-store
transaction; account/token/lease are checked again. An aborted transaction leaves the saved state.

Normal sign-out attempts to revoke the captured hub token, then stays at named login without a new
root navigation/automatic demo login. Offline or gateway-refused local sign-out is allowed, but explicitly reports that
server revocation was not confirmed: the old server session may remain valid until expiry. It does
not promise logout of every device. Embedded Fleet can report active writes and is disposed only
after confirmed main sign-out; standalone Fleet's own sign-out is not redesigned.

## One acceptance session

On fictional data, give a named non-admin the intended builder permission, open its Create action,
save an unpublished definition and reopen it through View saved. Check a normal import using a
reviewed disposable package. Keep one disposable local Task draft. Sign out, cancel the warning once,
then sign out while keeping it and return with that same account. Verify the notes remain. Use a
phone once during the same session. Never use valuable unsent work for discard testing.

## Local verification and limits

**364 selected Python tests** (186 app/authoring/local-work +
71 C01 + 107 demo/gateway/provision/package),
**22 compound Chromium checks**, **72 application JavaScript syntax checks** and **192 Python
parses** completed on the frozen source. The broader selected checklist/toolbox/logbook authoring
suites completed; this is not the entire product suite. Two old blank-reason rejection cases were
intentionally changed to reject a non-string reason instead; new tests explicitly cover allowed blank
unpublished drafts and reasons still required for published work. No unrelated historical failure is
claimed fixed.

Browser tests use actual shipped assets and fictional real TestClient APIs, injected fetch/hash
navigation, paused unrelated periodic jobs and a staged transaction store. **Not real durable
IndexedDB, real navigation, service-worker lifecycle, physical-device, Windows/PowerShell, native
binary, full accessibility/security/load, Docker or accepted off-host recovery validation.**
C01 tests are local; no Sulmara records/credentials or live service were inspected. Earlier failed,
partial and superseded runs are retained separately and excluded from these totals. A modal blocking
the main Account button led to the explicit in-dialog sign-out action. Mobile Originals checks open
the existing collapsed Browse folders panel before looking for its upload control; authority unchanged.

All C01 deployment files, G01 gateway, signing nginx, app schemas, handover/QR/operational writers and
normal permission policies remain unchanged. Three existing application Python adapters changed;
189 others are byte-identical. Six hosted Help articles/outlines and their catalogue were updated;
70 other article bodies, native guides and PDFs were not rewritten. Main app source changes are
listed in the accompanying audit. Do not revert to incompatible pre-C01/pre-UI34 writers. Protect
retained local work before any rollback; older code does not implement this sign-out owner marker.

**Nothing was pushed or deployed from here.**
