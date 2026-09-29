# Per-company application header logos

Public brand artwork only. Never put passwords, setup files, credentials or original reports here.

The existing COMPANY_ID in COMPANY mode selects the entry in deploy/company_identities.json.
For Sulmara, add the actual approved logo at deploy/company_logos/sulmara/logo.png and set
its entry's "logo" to "logo.png". Until artwork is supplied, null intentionally renders the
company name; no substitute logo is included. Commit both the logo and JSON change.

For another company, create its own directory and JSON entry with that company's COMPANY_ID.
The same shared repository can serve every company. DEMO mode does not display these identities.
The installer/Chrome icon and database-owned PDF report branding are separate and are not changed.

Accepts a single PNG/JPEG, <=2,000,000 bytes, <=4,096 pixels on either side and <=8 million pixels.
Keep transparent/white-background artwork legible in a compact header. Aspect ratio is preserved.
Only the selected company's validated logo is served by /static/company-identity/logo; filenames
and directory paths are not request parameters. Missing/invalid artwork falls back to the name.
The display configuration is code-owned and takes effect on process restart/deploy; no database
reset, Company C01 initialisation or browser-data clearing is needed.
