# Recovery helper — source-pin limitation in this cumulative bundle

The original **ops/staging_recovery.py** is retained unchanged and its SHA-256 is recorded. It accepts only the pristine 1.34.19 source manifest. **It does not accept the cumulative UI03 application directory /opt/wavelink/app**; a source-manifest rejection is expected there, not a reason to override the check.

This consolidation did not update, certify or run that helper against the live UI03 project. No recovery key, live project, backup or off-host scheduler is supplied. The complete original instructions/evidence are preserved in the outer REFERENCE_ONLY/initial_deployment folder and describe the original reviewed source, not a UI03 restore acceptance.

Keep a current, coherent full-project backup through the established operator workflow before deployment; this source ZIP is not that backup. Preserve current source version, category metadata, original uploads and identity/signing material. Do not replace a live SQLite database with a sample, copy only an in-use main SQLite file while omitting its WAL state, or change INITIALISE_FICTIONAL_DEMO back to YES_FIRST_DEPLOY_ONLY.

A future checked recovery update needs an explicit UI03 manifest policy and a complete restore exercise, not silent loosening of the existing pin. Recovery handling must remain separate from vessel/CCVD data.
