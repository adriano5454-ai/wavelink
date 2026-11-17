# Wavelink UI142 candidate

Version 1.34.42, prepared on 17 November 2026 from verified UI141 commit `18c14c5429379932ac8f7880f70e72f17e18d137`.

## Changes

- Adds optional OpenAI assistance for inventory column mapping when the server is configured.
- Sends selected column headers and at most eight sample rows only after explicit confirmation. Original files and complete workbooks are excluded from the API request.
- Keeps suggestions separate from application and saving. Users review mappings and explicitly apply them; assistance never saves inventory automatically. Standard local import remains available.
- Rechecks the current named account, selected project, inventory-builder permission and source identity. Connection tests additionally require an administrator.
- Bounds input and response sizes, validates structured suggestions, and limits use to 100 requests per project per UTC day, 20 per user per UTC day, six per user per minute and two concurrent requests per project.
- Persists operation identifiers so repeating the same request cannot cause another provider call or another quota charge. Cached results may be returned; an expired or interrupted operation requires a new explicit request.
- Uses a server-side API key. The administrator connection test sends fixed synthetic text with a 32-token output limit and shares the usage limits.
- Refreshes changed asset URLs and the offline cache identifier for UI142.

Adds UI142 after UI141 in the existing Docker and source reconstruction chains. The three existing Render application services retain their resources. Website 3.3.1 accompanies the optional-assistance privacy update.

## Verification

The complete release chain reproduced all 2464 resources. Their SHA-256 hashes match the candidate runtime. The runtime manifest is `9a37e900fddb020d9e6c58fa338d9e14ae22c346b5069e6e6cf9f9d163abded3`.

`DELIVERY_CHECKS.json` records reconstruction results and any supplied visual or regression results. `validation/UI142_ASSET_KEYS.json` records asset keys and registered fonts. UI141-specific source files retain their original hashes.

## Release status

The package is a local candidate. Publication, post-deployment verification, per-service API configuration and explicit live connection verification remain pending. This record does not claim available OpenAI credit or activation on any service.

Run `python deploy/materialize_runtime.py NEW_DIRECTORY` to reconstruct the complete candidate source.

See [UI142_OPENAI_SETUP.md](UI142_OPENAI_SETUP.md) for configuration, limits and the connection check.
