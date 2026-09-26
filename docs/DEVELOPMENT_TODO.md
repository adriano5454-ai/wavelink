# Wavelink continuation — UI27 + G01

**Adriano's 25 September priority: HANDOVER FIRST.** UI20 implements daily Start
today, selected shift and automatic periods, default 12 hours, alternatives/custom
24-hour cycle, manual fallback and saved-publication continuation. Core 1.34.19.
UI21 adds fresh saved-draft resume, read-only day navigation and explicit published
source selection with scoped snapshots. No live deployment was made. G01 public
entry was confirmed working by the user;
keep its exact source and non-administrator guest requirement intact.

UI22 adds guided saved publication/personal acknowledgement with fresh exact
review and existing explicit write/retry behaviour. Handovers/Get started Help and
create search-index drift are updated. No new API/storage/G01 behaviour.

UI23 adds visible handover note sections, opened-draft text comparison and an
explicit read-only exact previous-shift reference. No automatic copying or saving.
Draft/publication/acknowledgement action functions and all application Python stay
unchanged. Handovers and continuity Help re-reviewed; same eight distinct topics.

UI24 bundles private-draft review navigation, compact opened/proposed details,
changed/cleared note sections, selected-audience differences, field-return actions
and save-state/reason-only protections. No automatic saves or publication. Existing
UI20–UI23 handover paths were checked together across two named authors.

UI25 bundles the incoming-account workflow: latest active publications across all
dates, independent acknowledgement/type/search filters, complete read-only published
sections, exact pinned refresh, explicit newer-revision navigation and scoped stale
read guards. Existing automatic shifts, draft review and personal acknowledgement
writers are unchanged. No unread tracker, auto-signing or mandatory-signature score.

UI26 bundles publication history and exact two-publication comparison: explicit
visible revisions, last personal-acknowledgement selection, full notes/details and
selected audience ID/label differences, exact reader navigation and scoped async
read guards. Existing save/publication/acknowledgement and automatic shifts unchanged.
No private-draft comparison, automatic save/copy/signature or roster inference.

UI27 bundles author recipient review: current acknowledgement/source/search filters,
full-snapshot counts, unavailable audience selections and retained acknowledgement
evidence, strict projection and scoped refresh/hide. No automatic reminders/signing
or permission changes. Current membership is not historical delivery tracking.

**Release cadence:** Adriano explicitly requests fewer, more substantial grouped
releases. Group related workflow improvements, run integrated regressions, then
address hosted feedback before expanding. Deliver only changed GitHub files with
one current checkpoint; separate bulky evidence. UI27 is locally implemented/tested,
not deployed by this work. Do not infer live version from the latest prepared ZIP.

## Next work

1. Check author recipient filters/exceptions/refresh, history/comparison, incoming/read/exact-revision/acknowledgement and drafting/review/save together on the hosted service with actual shift starts
   (06:00/12:00 or agreed local schedule), night-to-next-day continuity, named
   authors, department audience and real phones. Confirm time basis and that
   published predecessor/acknowledgements do not change. Address feedback before
   unrelated feature additions. No new shared live draft/crew roster is implied.
2. Continue bounded Help wording and entry-point review. Eight distinct topics
   reviewed locally,68pending plus native/master-PDF/accessibility work. UI22 adds
   Get started and re-reviews Handovers. Public-vs-staff instructions now distinguish
   outer gate from named-account login. Create search index now matches its existing
   article; the broader create article wording review remains, not silently counted
   as complete. Keep four historical assertions explicit, not passed.
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

Continue future builds from UI27 + G01's exact source identity/checkpoint. This patch requires the exact UI26 + G01 baseline. This is the supplied UI18 branch, not the other unrecovered UI18 variant. The schema guard must not be bypassed or turned into an unreviewed migration. Verify the source baseline before changing code.

Default deliverables are **changed/new GitHub files only**, short instructions and one current checkpoint. Do not accumulate old screenshots, test logs, old releases, rollback extractors or unchanged source/vendor parts in routine ZIPs. Keep one full GitHub baseline and the approved Git history separately. State required baseline, deletions, migrations and dependencies explicitly. Development evidence stays separate; never claim tests or deployments not actually completed.

Preserve working Gateway G01 and DEMO_PUBLIC_ENTRY=YES, demo.mywavelink.com, all secrets/guest/disk settings, INITIALISE_FICTIONAL_DEMO=NO, removed bootstrap, .git, outside edits and unsent browser/log-window work. No reset, re-import, storage clearing, cloud synchronization or automatic background development.
