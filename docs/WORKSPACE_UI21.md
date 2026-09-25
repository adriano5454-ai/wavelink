# Workspace UI21 — daily handover resume and source review

Prepared 25 September 2026. Core 1.34.19; the exact UI20 source on the supplied-UI18
branch plus working G01 is the parent. This update is browser/read-only navigation
and two bounded Help article reviews, not a new backend handover format.

## Saved work first

Your saved daily drafts is populated from the existing authorised handover list,
not from a new store. Only the signed-in author's active, non-archived grouped daily
records in private-draft state appear. A record can also retain a publication. The
panel deliberately spans other days/departments/location labels and is independent
of the lower daily and library filters. It excludes full-hitch/ungrouped and archived
drafts. It does not claim to list another device's unsaved local text.

Continue my draft reads the exact record again and requires that it is still the
current author's editable daily draft. It opens the existing Work & priorities
editor. It does not copy/create/publish it. Empty, loading and unavailable states are
distinct. A failed read removes the old panel rather than preserving stale private
information. The ordinary wider library remains below.

## The selected day is explicit

Previous day and Next day move the selected operational date by one calendar day;
Today uses the device calendar. These are reads, not new shifts. Date/location/
department changes invalidate the visible snapshot immediately. The new projection
requires matching actor/context and well-formed records; an incomplete or mismatched
response is shown unavailable rather than accepted as zero.

A successful response shows its selected date, location label, department and
retrieval time in UTC. Three counts describe only the accessible returned records:
Your private drafts; Records with a publication; Others' publications not
acknowledged by you. A draft with a retained publication contributes to more than
one count. Acknowledgement is not approval/completion. No total, crew roster, number
of planned shifts or live completion status is invented.

## Continue the exact source, not the latest revision timestamp

One own draft offers resume; several offer an explicit draft choice. With no own
draft, one publication can offer its exact next-shift action. Several publications
offer Choose previous shift and focus the source controls. The old use of most
recent publication timestamp is removed: revising an earlier shift does not make it
a later operational shift. Each card labels Read published revision N and Start next
shift from revision N; the source is re-read before continuation. If publication
revision changed or the record was archived, the old selected action is refused.

Read published revision shows the saved publication, even when an author has newer
private draft edits. Draft cards label Draft period and keep retained-publication
status separate. Published notes/dates are not silently replaced by the draft.

The existing UI20 startDaily form and helper still calculate periods from an exact
publication whose actual saved period matches its optional creation schedule.
06:00 gives 06:00–18:00 / 18:00–06:00 next calendar day; 12:00 gives 12:00–00:00 /
00:00–12:00 next day. 3×8,4×6/custom and manual fallback remain. Default board Today
does not shift an older predecessor; a deliberately selected later board date keeps
the existing warning/review. No intervening records are fabricated. No timezone/DST
conversion, crew-wide preference or shared live private draft was added.

## Interrupted reads and existing editors

Generations, actor/token, route, exact workspace/host, editor and unrelated-dialog
checks discard delayed reads that no longer belong to the current action. Opening
an unrelated dialog or another handover editor is not permission to replace it.
The new Handovers help link is the only added navigation-guard exception, opens a
separate tab, and does not save/discard a form. Ordinary existing unsaved-work guards
remain. Real tab opening still requires hosted/browser acceptance; the local test
suppressed navigation after checking the link event was not blocked.

## Scope and preservation

All181 application Python files remain byte-identical. Existing handover writes,
review forms, API payloads, operation IDs, private audience/publication/signature/
acknowledgement rules and storage formats remain unchanged. No new databases,
columns, documents, permissions, environments or dependencies. Existing executable
upload-repository change is only deploy/extract_source.py. G01 gateway/entrypoint,
provisioning, nginx, Docker, dependency pins, vendor source/seed and recovery bytes
remain unchanged. Only the Handovers and Handover continuity article bodies change;
74 others remain exact, apart from shared reader cache URLs outside article bodies.
Two corresponding search-index entries were re-synchronised. The inherited create
article/index discrepancy is recorded separately, not silently rewritten.

There are seven distinct bounded reviewed topics,69 still pending, plus native,
master-PDF, entry-point and accessibility work. This is not a full Help rewrite.

## Validation record

Final selected Python:257 handover/schedule/day/privacy/continuity/transfer/backup/
Help/assets cases plus91 gateway/public-entry/package cases =348. All pass, no errors
or skips. Four old release-only expectations were explicitly deselected after they
failed identically on untouched UI20: two obsolete embedded Help article expectations,
one old fieldwork API checksum and one old store reverse-delta expectation. Their
initial and baseline failures are retained; the complete product suite is not green
or claimed tested.

Final Chromium:13 UI21 day/draft/source checks +12 inherited UI20 shift checks =25,
using actual assets and in-process fictional TestClient API with injected transport
and in-memory persistence. Responsive checks cover1440/1000/768/390/320px. The added
Help action exposed768px heading overflow; wrapping/flex sizing fixed it. The earlier
about:blank fixture's invalid URL was repaired with an inert base URL, not weakened
application guards. Real loopback navigation was blocked by browser policy and is
excluded. 44 new pure projection checks +18 inherited schedule checks pass, also
inside Python coverage. 224 calendar-parity cases are inside one Python test.

50 JavaScript syntax checks,181 Python parses; fresh final-package reconstruction
must match all1650 tracked runtime files before delivery. No real phone/Windows,
durable storage, service-worker lifecycle, hosted HTTPS, full accessibility, security/
isolation/load, Docker or off-host restore acceptance; no live push/deploy/secrets edit.
