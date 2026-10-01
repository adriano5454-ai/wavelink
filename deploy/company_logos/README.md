# Per-company Wavelink identity artwork

Every hosted **COMPANY** service must have one approved, code-owned company logo before it starts. Public brand artwork only belongs here. Never put passwords, setup keys, credentials, customer records or original reports in this directory.

## Add a new company site

1. Choose the exact `COMPANY_ID` used by the service, for example `sulmara`.
2. Create `deploy/company_logos/<COMPANY_ID>/`.
3. Add one approved PNG or JPEG, normally named `logo.png`.
4. Add the matching entry to `deploy/company_identities.json`:

   ```json
   {
     "example-company": {
       "name": "Example Company",
       "logo": "logo.png"
     }
   }
   ```

5. Confirm the JSON name exactly matches `COMPANY_NAME`, commit the logo and configuration together, then deploy.

Actual COMPANY startup now fails closed when the identity entry is missing, the configured name differs, or the logo is unavailable/invalid. This prevents a newly provisioned customer service from launching with a generic or incorrect company identity. Direct development/test preparation without `WAVELINK_DEPLOYMENT_MODE=COMPANY` retains its existing name-only behaviour.

The shared repository can contain separate entries for multiple companies; only the exact runtime `COMPANY_ID` is selected. DEMO mode does not display a company identity.

## Accepted artwork

- One PNG or JPEG.
- Maximum 2,000,000 bytes.
- Maximum 4,096 pixels on either side.
- Maximum 8 million pixels total.
- Transparent or white-background artwork should remain legible in a compact header and on the Home cover card.
- Aspect ratio is preserved.

Only the selected company’s validated asset is served through `/static/company-identity/logo`; filenames and directory paths are never request parameters. The installer/Chrome icon and database-owned PDF report branding are separate systems.

Changing this code-owned display identity takes effect after process restart/deployment. It does not reset the database, repeat Company C01 initialization or require browser-data clearing.
