# UI115 selected acceptance

Set `WAVELINK_UI114_TEST_SOURCE` and `WAVELINK_UI115_TEST_SOURCE` to verified parent and frozen target. `test_ui115_build.py` checks exact replay, refusal before writes, corrupt payload/new-resource collisions, cache/chain completeness and byte preservation of every unrelated resource. Retained runtime Help and signed-boundary suites pass separately.

Thirteen Node suites pass 344 cases. New overlap cases cover literal identifiers, included scope, source availability, locations, escaping, bounded/focused pagination, cache invalidation, safe inspection and ownership locks. The retained UI108 mock now models native connected/disconnected nodes rather than omitting `isConnected`.

`browser_inventory_overlap_ui115.py` uses fictional XLSX and a disposable native C01 API/SQLite company. Set `WAVELINK_TEST_SOURCE` and `WAVELINK_CHROMIUM_EXECUTABLE`. Its 15 grouped checks cover accepted/blocked browsing, exact item/source focus, four widths and genuine lost-response retry. Retained UI114 worksheet and UI111 save/retry browser harnesses pass 22 and 28 grouped checks. This environment used Chromium Headless Shell 141.0.7390.37 with `--no-sandbox --no-zygote --single-process`; retained harnesses used an execution-only launch shim without source edits.

Selected pytest total: 48 (14 final build + 23 Help + 11 signed boundary). Service workers/WebSockets were suppressed. No production, email, physical device, Windows desktop or worker-upgrade claim. Text evidence excludes screenshots, user-source content and temporary databases. Read `docs/UI115_REVIEW_REPORT.json`.
