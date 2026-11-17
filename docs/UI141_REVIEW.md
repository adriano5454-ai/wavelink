# Wavelink UI141 candidate

Version 1.34.41, prepared on 17 November 2026 from the verified UI140 release.

## Changes

- Incorporates the reviewed UI141 visual changes and local typography.
- Registers local font files in the offline shell.
- Refreshes changed static-asset URLs and the offline cache identifier.
- Updates application version labels, including installation and example pages.
- Adds UI141 after UI140 in the existing Docker and source reconstruction chains.

## Verification

The complete release chain reproduced all 2457 resources. Their SHA-256 hashes match the candidate runtime. The runtime manifest is `4c219eb1bbf0ff0b6d3bf2e8c5b0a0a2f1dac664babb0bbd1d4b4b20563c4a1a`.

`DELIVERY_CHECKS.json` records reconstruction results and any supplied visual or regression results. `validation/UI141_ASSET_KEYS.json` records asset keys and registered fonts. UI140-specific source files retain their original hashes.

## Release status

The package is a local candidate. Publication, post-deployment verification and the application API integration remain pending.

Run `python deploy/materialize_runtime.py NEW_DIRECTORY` to reconstruct the complete candidate source.
