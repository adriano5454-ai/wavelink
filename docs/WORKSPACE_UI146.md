# Wavelink 1.34.46

The QSHE and Faults report editors use the page scrollbar for the complete form. Opening a report moves focus to its heading, and users can reach the final fields and action buttons with the wheel, touch or keyboard. Closing a report returns to its workspace.

This release derives from Wavelink 1.34.45 at commit `12d7bd7569fd0ab74b7397b63a93fd5eb9ff7804`. The deployment build validates the full parent manifest and verifies every resource in the resulting application. The release checks include QSHE and Faults form behavior, report persistence and access, and the browser scroll regression.

## Reproduce the browser check

From the materialized application root, run `node tests/ui40_reports/scroll_browser_ui146.cjs` with Playwright and its Chromium browser installed. To use an existing Chromium or Chrome executable, set `WAVELINK_TEST_CHROMIUM` to its full path. Set `NODE_PATH` to the package directory when using an externally supplied Playwright installation. The test exercises normal QSHE and Faults report entry at four viewport sizes with fictional, intercepted API responses.
