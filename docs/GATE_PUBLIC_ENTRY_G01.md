# Wavelink G01 — optional public guest entry

Prepared 25 September 2026. Small GitHub patch on **UI19, supplied-UI18 branch**. Core stays **1.34.19**; workspace UI stays **UI19**. This is a gateway change, not UI20 or a new database release. Nothing has been pushed to GitHub or deployed to Render.

## What to do

Apply this patch to the matching existing **UI19** repository first. Then set the following environment variable on your existing service:

```text
DEMO_PUBLIC_ENTRY=YES
```

Keep **DEMO_ACCESS_PASSWORD** present and non-empty. Keep **DEMO_GUEST_LOGIN** and **DEMO_GUEST_PASSWORD** configured; the latter must match that guest's actual password in Wavelink. Keep `PUBLIC_URL=https://demo.mywavelink.com` and `INITIALISE_FICTIONAL_DEMO=NO`. Keep the initial administrator bootstrap removed. Do not change the domain, disk, project or other secrets as part of this update.

Save/apply the environment change and deploy/restart the service with the patched commit. The exact hosting-dashboard button labels have not been verified here. Merely adding the variable to an old, unpatched build will not enable this feature.

After the deployment is healthy, open **https://demo.mywavelink.com/** in a new private/incognito window. A fresh browser goes through the short “Opening Wavelink…” page into the existing fictional demo guest account without typing the gate password or the guest password. No password is put in the URL or page. JavaScript and browser storage must be available.

For normal staff entry, use **https://demo.mywavelink.com/__demo/login**. The separate Wavelink named-account login and API permissions remain in force. To turn public entry off, set `DEMO_PUBLIC_ENTRY=NO` and redeploy/restart. Omitting the variable also means NO. Only exact YES or NO is accepted; an invalid non-empty value stops startup rather than opening access accidentally.

## Why deleting the password did not work

This conclusion comes from the supplied repository, not a live Render inspection:

- Original `deploy/entrypoint.py`, lines 73–76: `required_env` contains DEMO_ACCESS_PASSWORD, DEMO_GUEST_LOGIN and DEMO_GUEST_PASSWORD; missing values raise “Missing required hosted-demo setting(s)”.
- Original `deploy/provision.py`, line 72: DEMO_ACCESS_PASSWORD is also checked with `secret_value(...)`.
- Original `deploy/gate.py`, lines 52–53: the access password must contain 20–128 characters.
- The original gateway has no public-entry configuration. Its normal root navigation redirects to `/__demo/login`; its existing quick link is a different, password-bearing URL mechanism.

Deleting the variable therefore supplies an invalid startup configuration, not a request for anonymous access. The actual live failure log was not inspected, so no particular failed deployment is asserted here.

G01 deliberately keeps the access password for private entry and the existing gate-cookie epoch. It adds an explicit public-entry mode rather than silently treating an absent secret as permission to open the service.

## Access and data implications

With public entry ON, **anyone who can reach the URL can use the configured guest account and everything that account is permitted to access or change**. This is not automatically read-only. Visitors share the same guest identity and project; actions are not attributable to distinct named visitors. Use fictional demonstration records only.

G01 does not create a guest, enable a disabled account, change a password, reduce or expand permissions, reset a project, import the fictional seed, or touch uploaded original files. The configured guest must already exist with a **technician or supervisor** role. A missing/disabled guest, password mismatch, unexpected identity, malformed login result, or administrator guest is refused with “Guest demonstration unavailable”; an administrator token is not returned by public entry.

Passwords remain server-side. A guest **session token**, as required by the existing app, is delivered to the visitor. Public entry does not remove normal authentication from application API requests and does not grant administrator privileges.

Public openings have a separate global budget of 20 per five minutes, preserving the old private-login budget. This is a simple demo safeguard, not production-scale rate limiting, a multi-tenant boundary or a security acceptance result.

## Existing browsers and unfinished work

An automatic public visit is not permission to switch an existing user's account.

The new handoff reads the existing main record and lease, and only installs a guest when there is **no saved main record and no active lease**. Both reads and the possible creation share one IndexedDB readwrite transaction. It never overwrites an existing main record, including unknown future draft fields.

A saved same-project signed-in session is left intact and returned to Home; it is not silently replaced by the guest. Its token is not revalidated or renewed by this handoff. The ordinary Wavelink session-expiry/sign-in behaviour handles a stale token.

A signed-out saved workspace, another project's record, an unrecognised saved record, or an active lease without a main record is left untouched, with directions to normal sign-in or a private/incognito window. Do not clear browser storage to make the demo open.

Existing service workers/tabs may continue their cached app route; use a new private window to test the experience of a genuinely new visitor. No app service-worker or local-store format is changed here. The older password-bearing quick-link handoff remains byte-identical, with its previous limitations.

## Small-patch installation

1. Preserve the approved commit, established project backup, outside edits and all unfinished browser/separate-log work. Apply UI19 first when the checkout is still on UI18.
2. Extract the ZIP. Run the included **read-only** checker against the existing repository root:

   ```powershell
   .\CHECK_G01_UPDATE.ps1 -RepositoryPath "C:\path\to\wavelink"
   ```

   It checks all expected UI19 files, not just a version label. It accepts only explicitly listed UTF-8 text differences caused by CRLF line endings. It does not copy, delete, reset, make network calls or inspect live data. A mismatch means stop and reconcile, not overwrite.
3. Copy the **contents of UPLOAD_TO_GITHUB** into the existing checkout, preserving subfolders. Do not replace the repository or delete files absent from this patch. Review the diff, commit and push through your normal GitHub workflow.
4. The checker also supports `-Mode Installed` after copying. Then enable `DEMO_PUBLIC_ENTRY=YES` on the service and deploy the patched commit. Keep DEMO_ACCESS_PASSWORD present, all guest credentials matching, existing persistent storage, and initialization OFF.
5. Test fresh guest entry in a private window and normal staff entry in a separate browser context. Check that the visitor has only the intended guest permissions.

Only two existing executable deployment files change: **deploy/gate.py** and **deploy/entrypoint.py**. Documentation, verification metadata and a small regression test are also included. **deploy/extract_source.py, nginx_config.py, provision.py, Dockerfile, dependencies, vendor files, recovery tools and all application assets are unchanged.** No deletions or database migrations are required.

## Rollback and secrets

The simplest switch back is `DEMO_PUBLIC_ENTRY=NO` and a service redeploy/restart. Public-only gate cookies are then rejected; private-password gate cookies keep their separate validation. This does not revoke already-issued Wavelink user tokens or change guest credentials. Disable the guest or rotate its real account credentials deliberately when ending public access, as appropriate for the demonstration.

Reverting the G01 commit restores the original gateway; UI19's application remains unchanged. Preserve data and unsent work. Never re-enable initialization, clear site data, delete tables or reset the persistent disk to undo this gateway change.

The screenshot showed credential values. Rotate exposed credentials deliberately, without copying them into GitHub or support documents. For DEMO_GUEST_PASSWORD, update the **Wavelink guest account and the hosting environment to the same new value**; changing just the environment value breaks automatic sign-in. This patch contains no values from that screenshot.

## Local checks and limitations

Completed: **82 selected gate tests** (inherited and new), **8 selected unchanged deployment/configuration tests**, **13 handoff-JavaScript checks** using controlled in-memory IndexedDB/DOM/navigation fixtures, and **13 local Nginx/Gate checks** using a fictional stand-in for the core application. The new JavaScript passes `node --check`; changed Python modules parse. No failed or skipped cases in the completed Python selection; one unrelated source-reassembly case was deliberately deselected.

The intended real-Chromium/IndexedDB run was blocked at local navigation with **ERR_BLOCKED_BY_ADMINISTRATOR**, before its assertions, and is not counted as a pass. Browser policy was not weakened. An initial Nginx test harness assumed case-sensitive response-header names; the harness was corrected and the final proxy checks passed without an application-code change. The environment also emitted an unrelated spreadsheet warm-up warning during Python startup; pytest reported the completed results above.

This is not a full-suite, production-security, load, accessibility, physical-device, durable browser-storage, service-worker lifecycle, Docker-build, live Render or live GitHub acceptance result. The PowerShell checker was not executed on Windows here. No live deployment or credential change was made.

## Exact source identity

- UI19 extractor, unchanged: `ac61f992b3f9f7b4a122b70a7b0dec59c55b5466ebce3d0bb4c92e3c0f6831fa`.
- Original gate: `e237e77a03ef23d914d9e47ae0e68c19fca97ee23cd02cbd23ca45e2b71ef719`.
- G01 gate: `9dc4ab6f7b7fb324ea06c305a09af8336b0bd10e7be6bef5296af1fd32d2e701`.
- Original entrypoint: `690fd5bf5b53f1494714c3cd387ecfbfd9bad871d8c7c859f07710c673febda5`.
- G01 entrypoint: `a2bbac57635ac6e0b12400bbcbfc7382416ed3d5c7525e4218b7e38c2e7a633f`.

The complete baseline/target checksums are in UPDATE_MANIFEST.json. Future UI updates must retain G01's gateway files and the explicit public-entry setting; do not overwrite them with the unchanged gateway copied from an older full archive.
