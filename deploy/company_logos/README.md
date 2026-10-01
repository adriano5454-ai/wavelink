# Per-company Wavelink identity assets

Public brand artwork only. Never place passwords, setup files, credentials,
private records or operational evidence in this directory.

Every COMPANY deployment must have a reviewed identity entry in
`deploy/company_identities.json` and a valid local PNG or JPEG in:

```text
deploy/company_logos/<COMPANY_ID>/
```

The identity and logo are selected only by the configured `COMPANY_ID`. Host
headers, browser values and uploaded files never choose deployment branding.
Commit the image and JSON change together before provisioning or restarting a
company service. Company mode now fails closed when its reviewed identity or
logo is missing, invalid or inconsistent with `COMPANY_NAME`.

Sulmara uses:

```text
deploy/company_logos/sulmara/sulmara-primary.png
```

For a new company:

1. Create a directory whose name exactly matches its `COMPANY_ID`.
2. Add the approved primary logo as one PNG or JPEG.
3. Add the exact company name and filename to `company_identities.json`.
4. Run package and company-provisioning checks before deployment.
5. Keep the identity in the shared application repository; do not store it in
   the company database or copy a different company logo between services.

The image must be a single PNG/JPEG, at most 2,000,000 bytes, no more than
4,096 pixels on either side and no more than 8 million pixels in total. Preserve
its aspect ratio and keep it legible in a compact header. Wide wordmarks are
shown as complete artwork; compact marks may be paired with the controlled
company-name field.

Only the selected company's validated logo is served from
`/static/company-identity/logo`; filenames and filesystem paths are never
request parameters. The installer/Chrome icon and database-owned PDF report
profile remain separate identities.

`fictional-company` is a deliberately fictional automated-test identity. It is
not a customer deployment and must not be reused for a real company service.
