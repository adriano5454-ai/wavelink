# Sulmara / Wavelink C01 — separate company installation

**Application UI43, core 1.34.19. Optional hosting update C01. Prepared 26 September 2026.**
This is a code/configuration package and locally verified provisioning process, not an already
created Render service, domain or live company database. Render and GitHub were not connected.
The exact approved UI43 application/extractor stays unchanged. No UI44 is claimed.

## What you will have

One maintained Wavelink application GitHub repository, with two separate running services:

| | Existing demo | New company |
|---|---|---|
| Name | Existing demonstration | Sulmara |
| Address | Existing demo.mywavelink.com | Proposed sulmara.mywavelink.com |
| Mode | DEMO (default) | COMPANY (explicit) |
| Storage | Existing demo disk/project | A NEW dedicated persistent disk/project |
| Entry | Existing G01 guest/staff flow | Normal named Wavelink login after first setup |
| Data/accounts | Existing demo unchanged | One initial admin; no demo records or accounts |

The domain in this document is a proposal until configured and verified. A database and
accounts for the live service are created on that NEW service's first approved start.
A separate local empty Sulmara database was created and checked; do not upload that database
or an old demonstration project into the live company installation.

## 1. Update the SAME application repository

Extract the small patch. Copy everything **inside UPLOAD_TO_GITHUB into the existing UI43
Wavelink application repository folder**, replace matching files, review in GitHub Desktop,
commit and Push origin. Not the Wavelink-Website repository. Do not delete files missing from
this patch or replace the whole repository. CHECK_C01_UPDATE.ps1 is optional read-only checking,
not an installer; it has not been executed on Windows here.

Existing demo: leave its environment, public URL, guest, disk and initialization settings alone.
Missing WAVELINK_DEPLOYMENT_MODE means DEMO, preserving the current default. The entrypoint adds
an explicit company branch and refuses company-marked storage in demo mode; G01 gate.py and
the existing demonstration/signing Nginx configuration are unchanged. Only the new company mode
uses the new company ingress and first-sign-in boundary.

Test approved changes on the demo first, then deliberately deploy the same approved commit to
the company service. Do not assume pushing experimental updates must deploy both simultaneously.
Review your hosting service's automatic-deployment setting; no deployment setting was changed here.

## 2. Create a NEW company service and persistent disk

Use your existing hosting account and the SAME application GitHub repository/approved branch.
Choose a new Docker web service, for example `wavelink-sulmara`, using the repository root and
existing Dockerfile. Use its standard container command; no extra build/start command is needed.
The hosting configuration must support an always-retained persistent disk; pricing and current
hosting-dashboard button labels were not checked here. Do not clone the demonstration's data
or attach its disk/environment group. Review any additional service/disk cost before creation.

Attach a NEW persistent disk at **/var/data**. C01 keeps company storage at
**/var/data/wavelink-company**, with the current project at its **project** subdirectory.
It refuses ephemeral storage, an existing demonstration directory and unknown/partial company
storage instead of recreating a project. Company ID/name are pinned to the installation marker.

Configure the health-check path as **/healthz**. This is available while first sign-in is pending.
The public port is supplied by the existing hosting PORT setting (default 10000); the app itself
runs on loopback 8765. Keep one worker/instance for this current SQLite/presence design.

## 3. Add the PRIVATE environment settings to the NEW service

Use the separately supplied **Sulmara_C01_PRIVATE_Setup.txt**. It contains the requested
initial `admin` account credentials and a fresh private first-sign-in key/link.
**Never put that file or its values into GitHub, a screenshot, an issue, support logs or the demo.**
The ignore rules in this update reduce accidental inclusion; they are not permission to store
secrets inside a repository or a guarantee against a forced Git add.

Public, non-secret settings are:

```text
WAVELINK_DEPLOYMENT_MODE=COMPANY
COMPANY_ID=sulmara
COMPANY_NAME=Sulmara
PUBLIC_URL=https://sulmara.mywavelink.com
INITIALISE_COMPANY=YES_FIRST_DEPLOY_ONLY
COMPANY_ADMIN_LOGIN=admin
INITIALISE_FICTIONAL_DEMO=NO
DEMO_PUBLIC_ENTRY=NO
```

Add COMPANY_INITIAL_PASSWORD and COMPANY_SETUP_KEY from the PRIVATE file. Do not reuse any
DEMO_ACCESS_PASSWORD, DEMO_GUEST_LOGIN, DEMO_GUEST_PASSWORD or INITIAL_ADMIN_PASSWORD setting.
Company mode rejects those copied demo credentials instead of silently using them. Empty/invalid
company settings fail closed. Initial password values are not hard-coded in the program.

## 4. Configure the new address and HTTPS

Add **sulmara.mywavelink.com** to the NEW service's custom-domain configuration. At your DNS
provider, use the NEW service's assigned hostname as the CNAME target for `sulmara` (or the exact
DNS instruction the hosting provider supplies). Do not point it at demo.mywavelink.com or reuse
the demo service's target. Complete provider verification and TLS issuance.

The host/HTTPS boundary accepts only the PUBLIC_URL origin. Opening an unrelated generated
service hostname can deliberately return a host error, rather than opening another company.
The health check does not depend on the custom-domain Host. No DNS record, certificate or live
hostname was created by this package. Do not disable host/TLS checks to get around a DNS problem.

## 5. First sign-in: change the initial password before opening the workspace

Open the private `/company-setup#setup=...` address in the PRIVATE file after the new service
and HTTPS domain are healthy. Enter `admin`, the requested temporary password and a different
permanent passphrase twice. Use **at least 14 characters and six distinct characters**, with
no outer spaces. Choose a unique passphrase, not the private link key.

This is a one-time setup step. The known temporary password alone cannot open the company
workspace: every ordinary app/API/QR route is locked until the password change commits.
The separate private setup key is unguessable and valid for **24 hours after initial database
creation**. It is placed in the browser fragment, not the server URL query, and removed from the
address bar by the page. Do not share it; server-side hashing does not protect a publicly shared key.

Completion updates the password and activation evidence atomically, clears any initial sessions
and takes no normal session token. Then choose **Open normal sign-in** and use `admin` with your
NEW password at the root address. Ordinary daily access is just that normal Wavelink login—no
shared demonstration gate, automatic guest or company selector.

If a response is lost, keep the setup page open for **Retry unchanged request** or **Check saved
outcome**. Neither issues a session or restores old-password access. Reloading a completed setup
shows normal sign-in. Closing an uncertain setup does not roll back a successful password change.

After a successful first sign-in, on the NEW service:

- Set **INITIALISE_COMPANY=NO**.
- Remove **COMPANY_INITIAL_PASSWORD** and **COMPANY_SETUP_KEY**.
- Keep COMPANY mode, COMPANY_ID, COMPANY_NAME, PUBLIC_URL and the dedicated disk unchanged.

Apply/restart with those settings. Repeated startup verifies the same installation and does not
reseed accounts, reset passwords or delete records. This initial-passphrase requirement is not
an app-wide MFA/password-policy overhaul; subsequent account management retains the current
application's policies. Create individual named staff accounts, departments and permissions.
Import only reviewed reusable forms/templates; the new company has no fictional template library.

## Retained application and data boundaries

The unchanged UI43 app includes current handovers/day/PDF, files, Tasks, inventory, maintenance,
certificates, toolbox talks, signing reports, Help/new-tab links, local-work manager, icons and
support@mywavelink.com. Private drafts and exact published-revision permissions stay in force.
Existing account API endpoints require a valid named company session. Anonymous join/shared-code
entry is disabled. The public pre-login info response contains no project records or join codes.

The isolated QR signing page keeps its existing exact-document invitation/grant checks. It does
not automatically create project membership or use the demonstration guest. C01 was tested for
invalid grants and route preservation, not accepted as a new complete QR security review.

No application/extractor file, dependency, permission schema or existing project table changes.
The new local company installation uses existing schema/audit tables, plus a private deployment
marker and runtime configuration outside GitHub. The known sample checklist's supported purged
state prevents its automatic adoption into the NEW empty company; no existing project is purged.

## Backup, recovery and operator limits

Back up the **whole company directory**, including COMPANY_DEPLOYMENT.json, the project and
operator settings; a copied database alone is not a complete company deployment. Keep activation
evidence and marker together. A restored initial password with completed activation is refused.
Missing files/unknown storage is refused, not replaced with an empty database. Protect backups
as sensitive company data. Local stopped-instance backup/restore checks passed; actual off-host
recovery, schedules, retention and service ownership still need operator validation. The older
pristine-source recovery helper is NOT approved for this overlaid/company deployment.

If the first 24-hour window expires BEFORE activation, the operator can renew only that pending
setup: stop the company app, generate a DIFFERENT random COMPANY_SETUP_KEY (e.g. in a password
manager), set COMPANY_RENEW_SETUP=YES and start with the SAME company disk. Project leases must
be free. The pending key gets a new 24-hour window; users/passwords/records are not reset.
Remove COMPANY_RENEW_SETUP immediately afterwards and use the new private fragment link. It is
refused for an activated company. No public account-reset/recovery endpoint has been added.
Never delete the marker/tables, enable demo initialization, wipe the disk or clear browser storage.
A source rollback to pre-C01 lacks company support: keep C01-compatible startup on this company.

## Verification and what remains to do live

**301 selected Python checks** (71 C01 + 107 existing demo/gateway/package + 123 existing hosted
runtime), **19 compound Chromium checks** and **22 actual local Nginx→company boundary→UI43
checks** passed. The latter simulated a trusted HTTPS ingress header, not actual TLS. Browser
checks used shipped assets, real fictional TestClient APIs and controlled in-memory transport/
storage, set_content and hash fixtures. The private requested Sulmara setup was separately
checked locally for one locked admin and zero operational records. No private database is shipped.

All 190 application Python modules and 70 application JavaScript files are unchanged; the new
setup script also passed syntax checking. Fresh final-ZIP replay and exact runtime comparison
are in Wavelink_Company_C01_Verification.json. Counts are selected checks, not a full app-suite run.
Initial table-name/browser-executable fixture mistakes and superseded runs are excluded and
retained in separate evidence. Windows/PowerShell, native installers, live Render/DNS/TLS, real
phones, durable IndexedDB/service-worker lifecycle, full security/accessibility/load/Docker and
accepted off-host recovery have NOT been completed. No production-readiness certification.

After deployment: verify first sign-in, remove bootstrap secrets, sign in from a second clean
browser, create a fictional department/person/handovers, check cross-account file/QR permissions,
restart without losing data, and test a complete backup/restore before operational company use.
Keep the demonstration independent during this work. No remote account/data/credential actions
were performed here. The Render/GitHub connection cards are optional; code delivery is not proof
of a live service. Current provider UI labels and prices were not verified by this package.

## UI44 clean-company onboarding

After the company administrator is activated, UI44 adds **Setup & builders** to the browser. Administrators can grant the five builder permissions to named Technician/Supervisor accounts so the people responsible for checklists, maintenance, toolbox forms, logbooks or inventory can create/import those definitions without administrator access. Existing non-admin accounts receive no builder permissions automatically. This avoids importing fictional demo data just to obtain templates. Whole-project/history-bearing transfers remain separate advanced workflows.
