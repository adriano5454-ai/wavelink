# Operator recovery helper — not a deployment launcher

This standalone, network-free tool belongs to the preparation pack, not Wavelink's application source. It is pinned to the exact supplied **1.34.19 source manifest**. It refuses other versions, missing storage, incorrect identity, unsafe paths, invalid keys and overwrite requests. Requires that source and its existing Python/cryptography runtime.

It handles full private project data as an authorised server operator. It is NOT an end-user export API, an app-permission filter, a replacement for Render access controls, or a certified production backup system. Never run it against the vessel or CCVD project as part of this staging task.

## Files and limits

The new `.wlstaging` format is an authenticated AES-256-GCM envelope containing a ZIP with `dives.sqlite3`, `hub.json`, `hosted.json` and a checksum/content manifest. Standard Wavelink Restore does not read this new operator format. Use this helper to restore into a new folder, then use the supported hosted check. This does not replace the existing `.ajproject` transfer format.

**500,000,000-byte database limit**, also bounded encrypted/expanded input and metadata sizes. This is a conservative helper guard, not proof that every workload near that size fits the proposed memory. Scratch space briefly holds plaintext in private directories. Files are cleaned on handled completion/failure; abrupt process/host termination may leave temporary data. Restrict and encrypt the storage, inspect abandoned temporary directories, and never claim cleanup is forensic secure erasure.

Backup uses a coherent SQLite online snapshot, verifies the unchanged config and file identity, removes live sessions and participants IN THE COPY, and preserves other table contents/signing state. The original live sessions stay valid. The new `.staging-backup.lock` only serialises these helper jobs; it is not a replacement for the app's process locks or a distributed lock.

Restore authenticates the encrypted file before using its contents, validates member hashes, database integrity, schema, table-content and BLOB digests, and creates only a NEW folder. It preserves the hub identity for recovery but uses `https://restore-check.example.invalid` in the restored hosted config by default. It does not start the server or change the original config. After a protected restore rehearsal, an operator must deliberately configure the intended URL and stop the old writer before cutover.

## Example operator commands

Paths below are explicit **examples**, not existing Render paths or credentials. First create protected output/scratch directories, obtain the verified source and select only the separate fictional project's real UUID. The helper's Python environment needs Wavelink's runtime dependencies.

Create an independent recovery key on the operator's trusted system. Never print it, email it, put it in Git or upload it beside the backup. Escrow it separately and provide a protected runtime key file through the reviewed secret-injection mechanism.

```sh
python /srv/recovery/staging_recovery.py keygen \
  --key-file /secure/wavelink-staging.key
```

Create the coherent encrypted snapshot (one command; no network transfer):

```sh
python /srv/recovery/staging_recovery.py backup \
  --source-dir /opt/wavelink/app \
  --config /var/data/wavelink/operator/hosted.json \
  --key-file /secure/wavelink-staging.key \
  --scratch-dir /var/data/wavelink/recovery-work \
  --output /var/data/wavelink/backup-spool/UNIQUE-TIMESTAMP.wlstaging \
  --confirm-hub-id EXACT-FICTIONAL-STAGING-UUID \
  --acknowledge-private-copy
```

The key must be 32 raw bytes, not a typed password or a pasted base64 string, and mode 0600 on POSIX. The tool generates this format. There is no environment-variable fallback, default project or secret in command arguments other than a FILE PATH. A runtime failure produces a safe generic diagnostic, not account data. Resolve failures rather than deleting locks or forcing source versions.

Copy the encrypted output to an independent protected store and verify its SHA-256 after retrieving it. This step, retention, scheduling and alerts are **NOT implemented by the helper**. Do not assume another Render job can mount the web service's disk.

Restore a retrieved encrypted copy (no overwrite; no service start):

```sh
python /srv/recovery/staging_recovery.py restore \
  --source-dir /opt/wavelink/app \
  --backup /secure/retrieved/UNIQUE-TIMESTAMP.wlstaging \
  --key-file /secure/wavelink-staging.key \
  --new-project-dir /var/data/wavelink/restore-drill-UNIQUE \
  --confirm-hub-id EXACT-FICTIONAL-STAGING-UUID \
  --acknowledge-private-copy
```

Then validate with the same source:

```sh
cd /opt/wavelink/app
python run_hosted.py check \
  --config /var/data/wavelink/restore-drill-UNIQUE/hosted.json
```

Do not run that restored project publicly next to the existing writer or reuse its UUID as a separate company. For real recovery, stop the old application and follow the main runbook's identity/browser-work reconciliation and protected cutover. Copying data does not synchronise it.

## Repeat the tests

From an environment with pytest and the Wavelink runtime installed:

```sh
WAVELINK_REVIEW_SOURCE=/absolute/verified/Wavelink_1.34.19 \
PYTHONDONTWRITEBYTECODE=1 \
python -m pytest -q /absolute/preparation-pack/05_Tests/test_recovery.py
```

Tests create disposable fictional projects and keys. The all-family BLOB test uses synthetic database fixtures; it is a recovery/storage test, NOT a certification of the corresponding upload interfaces. The separate supplied demo drill used actual stored fictional original/certificate/asset/manifest files. Neither exercise deployed to Render, used real TLS, retrieved off-host objects or proved physical-phone usability.
