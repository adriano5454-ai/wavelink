# Wavelink continuation — UI21 + G01

**Adriano's 25 September priority: HANDOVER FIRST.** UI20 implements daily Start
today, selected shift and automatic periods, default 12 hours, alternatives/custom
24-hour cycle, manual fallback and saved-publication continuation. Core 1.34.19.
UI21 adds fresh saved-draft resume, read-only day navigation and explicit published
source selection with scoped snapshots. No live deployment was made. G01 public
entry was confirmed working by the user;
keep its exact source and non-administrator guest requirement intact.

## Next work

1. Check the new handover flow on the hosted service with actual shift starts
   (06:00/12:00 or agreed local schedule), night-to-next-day continuity, named
   authors, department audience and real phones. Confirm time basis and that
   published predecessor/acknowledgements do not change. Address feedback before
   unrelated feature additions. No new shared live draft/crew roster is implied.
2. Continue bounded Help wording and entry-point review. Seven distinct topics
   reviewed locally, 69 still pending, plus native/master-PDF/accessibility work.
   UI21 includes Handovers and Handover continuity; other related articles remain.
   Review create Help article/search-index mismatch (reproduced on UI20, unchanged),
   public-vs-staff sign-in guidance and entrypoints; preserve browser/hosted/native
   distinctions. Do not treat the four inherited release-test failures as passes.
3. Address actual Home/inventory/boxes/logistics/maintenance/checklist/Originals
   feedback and refine remaining forms/navigation. Native folder authoring,
   attachment formats and richer import mapping remain separately scoped.
4. Complete durable local-work, multiple-device/account, service-worker,
   interrupted-network and production/security acceptance. In-memory local
   browser checks are not these operational acceptance steps.
5. Prove overlay-compatible off-host recovery; pristine helper remains unapproved.
   Keep complete project backups and browser-local work independently. Selective
   transfers are not interrupted-request continuations.

## Retained larger roadmap (not silently removed by compact packaging)

Task/evidence extensions and recurring reminders; running-hour maintenance; configurable approval chains; further daily handover/vessel identity; guided fault/HSE connections; richer imports and controlled transfers; customer/report layouts; record lifecycle controls; offline/signing installer work; production security/isolation and operational ownership remain separate increments. Basic Tasks, Fault Reports, HSE/QSHE, handovers and the earlier checklist/maintenance guides already exist; do not reintroduce them as new modules. Vessel/cloud synchronization and local phone-network diagnosis remain parked. Native vessel and CCVD are outside this hosted increment.

## Source and delivery rules

Continue from UI21 + G01's exact source identity/checkpoint. This is the supplied UI18 branch, not the other unrecovered UI18 variant. The schema guard must not be bypassed or turned into an unreviewed migration. Verify the source baseline before changing code.

Default deliverables are **changed/new GitHub files only**, short instructions and one current checkpoint. Do not accumulate old screenshots, test logs, old releases, rollback extractors or unchanged source/vendor parts in routine ZIPs. Keep one full GitHub baseline and the approved Git history separately. State required baseline, deletions, migrations and dependencies explicitly. Development evidence stays separate; never claim tests or deployments not actually completed.

Preserve working Gateway G01 and DEMO_PUBLIC_ENTRY=YES, demo.mywavelink.com, all secrets/guest/disk settings, INITIALISE_FICTIONAL_DEMO=NO, removed bootstrap, .git, outside edits and unsent browser/log-window work. No reset, re-import, storage clearing, cloud synchronization or automatic background development.
