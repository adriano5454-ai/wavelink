# Original Files organisation — UI18 status

## User request

Organise Original files into a clearer folder structure without losing documents or breaking references. The implementation must preserve immutable bytes, exact revision identity, saved links, permissions and audit. UI17's existing browser library was a flat authorised download list; upload/revision management lived in established native tools.

## Implemented in UI18

Project-shared nested folder metadata and per-exact-revision locations; searchable full paths; all-files/root/folder scopes; archived filter; exact details/download; named-administrator create/rename/reparent/empty-remove and multi-select moves; explicit reason, preview and fresh confirmation; database transaction, catalogue snapshot and idempotent action history; unchanged source bytes/IDs/references; complete/selected documents-module transfer preservation. No automatic categorisation of existing or newly imported originals. Five modules changed/added; three additive tables, rather than a new physical filesystem tree.

## Deliberately not marked complete

Browser Add original/Add revision and destination choice during upload; native folder authoring; automatic family-wide organisation; organisation of every certificate/log/maintenance attachment; folder-specific access controls; universal cross-module source-link picker changes; bulk file deletion; cloud/vessel synchronisation; accepted off-host restoration. The old reusable setup export format does not include project folder metadata. Existing native imports create originals in the root, after which the browser administrator can organise them.

## Local verification and pending operator acceptance

Final folder and upgrade tests verify immutable originals, frozen checklist references, named-administrator scope, stale snapshot refusal, atomic moves, duplicate-operation replay, archived contents, audit and transfers. Local browser tests exercise actual scripts against TestClient-backed fictional projects, error/retry paths and small viewports. An actual UI17-created project is opened with UI18; a separate restart test verifies saved locations. No live service or real-device acceptance is implied.

Operator acceptance remains: intended users and permissions, deployment/restart with the real persistent project, actual document downloads, service-worker/tab transitions with unsent work, real phone/Windows review, multi-device conflicts and accepted transfer/recovery procedures. Keep the existing domain and data; no reset or re-import is required.
