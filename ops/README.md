# Retained operator tools

staging_recovery.py is the unmodified, original-source-pinned helper. Read ../docs/RECOVERY_HELPER.md: the UI03 /opt/wavelink/app manifest is intentionally not accepted by that old helper. Do not bypass its source check. No keys, live backups, scheduler or off-host transfer is included.

`rename_company.py` is a separate offline, dry-run-by-default company identity
transition. Read `../docs/CORCOVADO_TRANSITION.md`. Apply/recover requires the
whole service stopped, all native leases free, a private verified backup and
matching source/target identities. It does not change DNS, hosting or PDF profile
history. Never use the old staging recovery helper for this transition.
