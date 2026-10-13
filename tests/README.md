# UI110 selected acceptance

Set WAVELINK_TEST_SOURCE and WAVELINK_UI110_TEST_SOURCE to the frozen UI110 runtime, and WAVELINK_UI109_TEST_SOURCE to the verified UI109 parent. Set WAVELINK_CHROMIUM_EXECUTABLE to a local Chromium executable. Browser fixtures create disposable fictional companies; they do not use production data.

`test_ui110_build.py` verifies exact-parent replay, refusal before writes, asset/cache consistency and retained backend/art resources. `browser_work_browsing_ui110.py` uses genuine C01 APIs, IndexedDB and SQLite to test no-write summaries and existing full-record actions. `browser_task_inspector_ui110.mjs` uses controlled delayed GET responses in Chromium to exercise account, scope, filter, modal and request races; install Playwright or set CODEX_PRIMARY_RUNTIME_NODE_MODULES. Runtime tests/ui110_maintenance/browser_checks.py exercises the shipped style bundle and saved-record/draft/navigation guards.

The 92 selected retained backend checks cover general Task behavior, Maintenance cycles and saved rules. Together with 6 new build checks they form 98 distinct pytest. Three browser suites are reported separately. Local service-worker registration and WebSockets are suppressed. No live deployment, SMTP, real device or worker lifecycle acceptance is claimed. See docs/UI110_REVIEW_REPORT.json for exact results and diagnostics.
