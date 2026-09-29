# Wavelink UI64 + Mail Startup M01

29 September 2026 · core 1.34.19 · Company C01 and demo G01 retained.
A targeted company-launcher repair over the exact UI64 repository. The application
workspace still reports UI64: no application source or UI version is replaced.

## The confirmed fault

The C01 supervisor used minimal_environment() when launching deploy.company_runtime.
That minimal environment intentionally excludes unrelated secrets. UI64's SMTP and
membership feature reads its settings inside that child process, but the supervisor
never forwarded WAVELINK_MEMBERSHIP_MODE, the six MEMBERSHIP_SMTP_* values or the
required company identity/PUBLIC_URL. Therefore even a correctly configured hosting
service started the app with membership OFF and no SMTP credentials.

A fresh Python child launched through the actual original supervisor reproduced
`enabled=false, ready=false, smtp_keys_present=[]`. The corrected supervisor produced
`enabled=true, ready=true` with the same complete fictional operator configuration.
This confirms a defect in the supplied launcher; it does not inspect the user's
live deployment or prove that the configured SMTP password is valid.

The existing admin User ID/password login is authorised to manage invitations. It
is not the cause of this configuration message. Email-first operational sign-in and
verified sulmara.com routing remain the planned next identity stage, not this repair.

## What M01 changes

Only deploy/company_entrypoint.py changes among existing executable repository files.
After normal company/disk/identity validation, the supervisor passes an exact allowlist
of identity and mail settings to the company application. PUBLIC_URL uses the validated
canonical company origin. The SMTP password is copied verbatim, not trimmed or logged.
Missing/invalid settings still fail closed; OFF stays OFF. Credentials are forwarded
only for exact INVITE_ONLY. Nginx validation, Nginx runtime and all demo child environments
remain minimal and do not receive SMTP credentials. Bootstrap/setup secrets and unrelated
operator variables are never copied into the child.

The already-existing operator company-identity reader can now see its intended company
identity too. Its logo selection/configuration code and all artwork stay unchanged.
No security check, SMTP TLS validation, pending state, permission grant, invitation
protocol, database table, account or password is changed. No invitation is automatically
sent by applying the patch. Configuration-ready is not proof of actual inbox delivery.

## Install once using GitHub Desktop

1. Preserve the approved commit, independent edits, existing backup and unsent work.
2. Extract the ZIP. Copy EVERYTHING INSIDE UPLOAD_TO_GITHUB into the existing UI64
   Wavelink application repository. Replace matching files; do not delete other files
   or replace .git. Reconcile any independent edits to deploy/company_entrypoint.py.
3. Review in GitHub Desktop, commit (for example: Fix company membership mail startup),
   and Push origin. No PowerShell or Python script needs to be run to install this.
4. Let the Sulmara service deploy that commit. If automatic deployment is disabled,
   use its normal manual deployment action. Environment saving alone will not fix
   the old launcher; the changed code must be deployed.
5. Once that deployment is healthy, open Invitations & access as the existing named
   admin and press Refresh. No reinstall or browser-storage clearing is required.

Keep the current correct settings:

    WAVELINK_MEMBERSHIP_MODE=INVITE_ONLY
    MEMBERSHIP_SMTP_HOST=smtp.zoho.com
    MEMBERSHIP_SMTP_PORT=465
    MEMBERSHIP_SMTP_TLS=SSL
    MEMBERSHIP_SMTP_USERNAME=contact@mywavelink.com
    MEMBERSHIP_SMTP_FROM=contact@mywavelink.com

Keep the existing MEMBERSHIP_SMTP_PASSWORD private in the hosting environment. These
non-secret sender/host/port values come from the user's selected mailbox and supplied
Zoho screenshot; no live provider lookup or authentication test was performed here.
Leave COMPANY_ID, COMPANY_NAME, COMPANY mode, PUBLIC_URL, persistent disk, activation
marker, INITIALISE_COMPANY=NO and removed bootstrap secrets unchanged. Do not copy
these settings to the demo. Both services may auto-deploy the same branch; review
that setting before pushing. Demo startup code and its environment filtering are unchanged.

This small patch is NOT another full repository and does not include the large extractor.
It applies over UI64, including UI64's deploy/company_runtime.py. It has no additional
schema migration. UI64's existing upgrade still requires UI64-or-later compatible software;
never run older code against the membership database or repeat company setup.

## First check after deployment

The configuration banner should disappear when the full settings are valid in the
running child. Send ONE invitation to an unused test mailbox you control, check inbox
and spam, then request the verification code. A transport failure may now produce a
separate delivery-unconfirmed result: that means credentials, connectivity or provider
acceptance still need investigation, not that another user account is required.

Retain the original request for an uncertain outcome; avoid repeated blind resends.
Verify the new person remains Pending with no operational access until approved.
Do not share passwords, private invitation links, codes or authentication tokens.

## Verification and boundaries

New checks exercise the actual supervisor's process launch and fresh Python children,
not just a mailer with injected ready=True. Hosted child tests obtain settings only
from that environment, sign in as the existing fictional administrator and issue an
invitation through the normal authenticated endpoint. Only the SMTP transport is a stub.
The verification code and pending-member isolation are exercised; OFF mode retains
normal admin login and refuses invitations. Nginx environments exclude every mail key.

The separate verification records exact completed test counts, runtime hashes and
package replay. An early company-test command was interrupted by the tool timeout and
is excluded despite producing a pytest summary; its full retry completed with exit 0.
No browser visual tests were rerun because application/UI bytes are unchanged.
These are selected local checks, not full-suite, live Render/Sulmara, real SMTP/TLS inbox,
Windows/installed Chrome, durable browser storage, Docker/Nginx startup, production-security
or off-host recovery acceptance. Mount/provisioning/readiness/Nginx portions of the
supervisor test are simulated; the Python child environment boundary is real.

Nothing has been pushed, deployed, or emailed from here.
