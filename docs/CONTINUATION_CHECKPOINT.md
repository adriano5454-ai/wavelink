# Wavelink online client demonstration checkpoint
Date: 24 September 2026

User priority: immediate online client demonstration with no running Windows/offline Admin. Render preferred, separate from local vessel Wavelink and CCVD. Domain mywavelink.com purchase is not confirmed. Initial suggested presentation subdomain is demo.mywavelink.com; use the actual provider URL first.

Application baseline remains **1.34.19**, not a new Windows application release. Exact upstream source SHA-256: 8c1b6a8d731d01b05a1290d3a1dd1a544054147aac9048ca345af7983613cd9e. All 1,605 manifest entries were verified. Source is included as five reassemblable, hash-checked parts solely to make browser upload practical.

New separate deployment tooling: Dockerfile; headless fictional-seed provisioning; loopback hosted app plus same-container Nginx gateway; private demo invitation/password cookie gate; controlled startup/shutdown; required persistent mount; named initial administrator; published sample accounts disabled. No application API/schema/permission changes. Gateway presentation substitutions are restricted to the application's own /static/app.js response; original source archive, documents, reports and record JSON are unchanged.

No actual GitHub repository, Render service, provider account, domain/DNS, live vessel project or CCVD service was modified. Docker image build, real Render ingress, storage lifecycle and actual browser navigation remain acceptance checks. This deliverable does not certify production security, MFA, SSO, company isolation, full browser parity or vessel/cloud synchronization.

Local validation: see DELIVERY_CHECKS.json. Full upstream regression/browser suite not rerun. New browser navigation attempt was blocked by environment policy (ERR_BLOCKED_BY_ADMINISTRATOR); do not describe it as a passed browser test or a known Wavelink defect.

Next actions: upload this actual repository package, complete a real container build and private Render deployment, disable the one-time seed switch, verify browser administration and upload/restart persistence, rehearse a client walkthrough, and validate recovery. Continue GUI work and Original files folder organization after this narrow demo deployment; preserve all prior roadmaps.
