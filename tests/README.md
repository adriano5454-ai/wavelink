# Local-only validation

## Current UI94 cumulative replay

Use three new, disposable directories. Extract UI92, copy it and apply UI93, then copy UI93 and apply UI94. The companions reject altered parents or a second application. No live project or mail credentials are used.

```bash
python deploy/extract_source.py vendor/source_parts.json /tmp/WAVELINK_UI92_TEST_BASE
cp -a /tmp/WAVELINK_UI92_TEST_BASE /tmp/WAVELINK_UI93_TEST_BASE
python deploy/apply_ui93.py /tmp/WAVELINK_UI93_TEST_BASE
cp -a /tmp/WAVELINK_UI93_TEST_BASE /tmp/WAVELINK_UI94_TEST_SOURCE
python deploy/apply_ui94.py /tmp/WAVELINK_UI94_TEST_SOURCE
WAVELINK_UI92_TEST_SOURCE=/tmp/WAVELINK_UI92_TEST_BASE WAVELINK_UI93_TEST_SOURCE=/tmp/WAVELINK_UI93_TEST_BASE WAVELINK_TEST_SOURCE=/tmp/WAVELINK_UI94_TEST_SOURCE PYTHONPATH=. python -m pytest -q tests/test_ui93_build.py tests/test_ui94_build.py
PYTHONPATH=/tmp/WAVELINK_UI94_TEST_SOURCE python -m pytest -q /tmp/WAVELINK_UI94_TEST_SOURCE/tests/test_email_alerts_ui93.py
```

Real Chromium checks are available in the extracted runtime as tests/browser_shell_ui94.py, tests/browser_email_ui93.py and retained workflow browser scripts. They use fictional in-process APIs; no live inbox or production session is tested. See docs/UI94_REVIEW_REPORT.json for current results.

## Current UI93 replay and mail checks

Use two new, disposable runtime directories. Keep the first as the exact UI92 parent; apply UI93 only to its copy. These checks use fictional projects and mocked mail, never a live mailbox or company project.

```bash
python deploy/extract_source.py vendor/source_parts.json /tmp/WAVELINK_UI92_TEST_BASE
cp -a /tmp/WAVELINK_UI92_TEST_BASE /tmp/WAVELINK_UI93_TEST_SOURCE
python deploy/apply_ui93.py /tmp/WAVELINK_UI93_TEST_SOURCE
WAVELINK_UI92_TEST_SOURCE=/tmp/WAVELINK_UI92_TEST_BASE WAVELINK_TEST_SOURCE=/tmp/WAVELINK_UI93_TEST_SOURCE PYTHONPATH=. python -m pytest -q tests/test_ui93_build.py
PYTHONPATH=/tmp/WAVELINK_UI93_TEST_SOURCE python -m pytest -q /tmp/WAVELINK_UI93_TEST_SOURCE/tests/test_email_alerts_ui93.py
```

The two parent-replay checks skip when the optional UI92 test-source variable is absent. Existing broad suites contain historical source/cache-version assertions; see docs/UI93_REVIEW_REPORT.json for the unchanged-baseline comparison and current validation boundary.

## Retained historical validation instructions

Use a disposable extracted UI03 source and a test environment with pytest/httpx and the shipped runtime dependencies. Never point these probes at the live Render/vessel/CCVD projects.

```
python deploy/extract_source.py vendor/source_parts.json /tmp/NEW_EMPTY_UI03_SOURCE
WAVELINK_TEST_SOURCE=/tmp/NEW_EMPTY_UI03_SOURCE PYTHONPATH=. python -m pytest -q tests
WAVELINK_TEST_SOURCE=/tmp/NEW_EMPTY_UI03_SOURCE python tests/integration_probe.py
```

The integration probe temporarily binds local port 8765; it refuses an occupied port. It prepares fictional data in a temporary directory and exercises normal and guest authentication, browser-admin API, real HTTP/WebSocket routing and an application restart. It does not execute the browser handoff JavaScript.

rootless_nginx_probe.py is an optional isolated-root-container test that drops to UID 10001, validates the generated gateway and exercises a non-root listener. No project is opened.

browser_probe.py is retained as a separate optional full-browser probe with test-only synthetic credentials. It was not rerun for this consolidation. Its original evidence/limitations remain outside the upload tree. Installing Playwright/browsers is a test environment step, not a new application dependency.

Original UI03 category/extractor tests and their environment contracts are preserved under REFERENCE_ONLY/Inventory_UI03/validation/tests. They were repeated using the exact cumulative extractor; see DELIVERY_CHECKS.json for outcomes.
