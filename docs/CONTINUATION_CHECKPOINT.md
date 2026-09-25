# Full online demo consolidation — core 1.34.19 + UI03

Requested after Inventory UI03: one ZIP of all deployment files, to replace the existing GitHub files together rather than tracking separate snippets/patches.

Sources: supplied initial GitHub deployment ZIP; latest successful entrypoint/Nginx/Docker/gate corrections in this conversation; exact cumulative Inventory UI03 extractor. Live GitHub bytes were not fetched (GitHub connector is not connected). No live service was changed. Later independent edits are not claimed included.

Preserved: seed/marker/hub identities; original five source parts; UI03 cumulative resources and categories; last confirmed normal/guest sign-in flow; /var/data and initialization NO; local vessel/CCVD separation; source and validation history.

Packaging-only small correction: supervisor returns exit status 2 on handled startup failure instead of returning success after printing an error. Normal login/authentication/record behavior is not expanded.

Use the existing service and secrets. Apply demo categories through administrator preview/confirmation, not by reseeding. No new software version/Windows release or live-data approval.

Next priority remains inventory, boxes, manifests and movement/receiving usability. Preserve Original Files folder work as pending. Use the current UI03 README for category export/rollback compatibility.

Validation and exact hashes are in DELIVERY_CHECKS.json / DEPLOYMENT_FILES.json. Historical tests are labelled as historical; local consolidation tests do not substitute for actual Render acceptance.
