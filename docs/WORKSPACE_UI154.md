# Wavelink 1.34.53

Employees of Corcovado can request access from the sign-in page using an address at `corcovadogeosub.com.br`. The portal sends a verification code to the address. After verifying it, the employee chooses a password and can check the request status and update their display name. The workspace remains closed to the employee until an authorized reviewer approves access in **People and access**.

The hosted company wrapper identifies Corcovado using its installation marker. The company’s configured HTTPS origin and invitation mail service must also match. The demo and other companies keep their existing entry flows. Existing email invitations continue on their original links.

The permissions form includes controls to select or clear the editable permissions in one area. Authorized reviewers can also request suggestions from OpenAI, inspect the proposed permissions, and decide which to keep. Saving the final permissions remains an explicit action.

The release adds temporary SQLite storage for email verification challenges. Registration reuses the company’s configured invitation mail delivery. The optional permissions assistant uses the existing OpenAI integration. Validation uses local company and demo fixtures, an isolated test mailbox, a simulated OpenAI provider, and real Chromium. External delivery of the new verification email and the revised invite templates requires a production check.

The authenticated Chromium flow covered editing a pending profile, approval, suspension and signing in again. Chromium also checked consent, department changes, valid recommendations and rejection of privileged suggestions after the scope fix. Applying suggestions and explicitly saving in that same final end-to-end run remains to be confirmed. Automated review detected an external telemetry attempt in the workstation test execution. Final packaging uses file-based integrity checks and preserves the results of completed product tests separately.
