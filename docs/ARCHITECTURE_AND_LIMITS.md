# Current consolidated demo architecture

One persistent fictional project, SQLite WAL, one hosted application worker at loopback port 8765, an invitation/guest gate at loopback port 8766, and Nginx at the platform PORT. The same-process gateway enforces the canonical host and requires the platform TLS indicator; the Wavelink API retains its separate bearer-token permissions. Nginx never makes the loopback-only app a directly public listener.

This is the architecture last supplied and reported working in the conversation. No live hosting configuration was fetched during consolidation. The complete original design/review is preserved under the outer REFERENCE_ONLY directory.

UI03 changes optional inventory-list classification metadata and scoped UI/API actions, not the database schema or physical movement rules. The exact checked extractor is carried over unchanged from UI03.

The shared guest URL grants the configured guest account to anyone holding the link. It is not company isolation, individual attribution or MFA. The gate's signed cookie/form checks and browser storage handoff retain the limitations of the last supplied demo implementation. A separate browser profile/private window avoids mixing the guest handoff with administrator work. This consolidation does not claim a new security review or reimplement account switching.

Normal account administration is in the browser. Some legacy imports/recovery still require operator tools. Tk is installed only to satisfy an existing Help-module import; no desktop Admin is launched. Data must remain fictional pending the separate authentication/isolation/persistence/recovery acceptance plan. Vessel/cloud synchronisation and Original Files folder organisation remain pending.
