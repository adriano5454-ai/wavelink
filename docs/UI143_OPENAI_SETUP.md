# UI143 optional OpenAI connection

The integration is optional. Standard local document extraction and reviewed import remain available without an API connection.

## Server configuration

Set `OPENAI_API_KEY` as a secret environment variable on each intended Render application service. Keep it out of source control, browser code, screenshots and release evidence. `OPENAI_IMPORT_MODEL` is optional and defaults to `gpt-4.1-mini`; the configured account must have access to the selected model. Configuration alone does not prove API access, available credits or successful billing.

The two application services and the marketing website keep their current plans and resources; application disks and databases remain unchanged. This release requests no resource changes. Configure only the deployments intended to offer assistance; the marketing website needs no API key. Website release 3.3.1 documents the optional data transfer.

## Connection check

Sign in with a current named administrator account, select the intended project and open inventory Setup & builders. The account also needs `builders.inventory`. Use the connection-test control and explicitly confirm the request. This invokes `POST /api/builders/ai/test` with a fresh operation identifier and `confirmed: true`. The server enforces the named session and selected-project headers. The test sends fixed synthetic text, no document content, and requests at most 32 output tokens. It counts against the same quotas as suggestions. Record only the success/error category and model; never copy authentication headers or the API key into evidence.

`GET /api/builders/ai/status` reports configuration and remaining local allowances without a provider request. A configured status is not a successful live connection test. A rejected or failed test leaves normal import available.

For an offline regression check from the reconstructed runtime, run:

```sh
python -m pytest tests/test_openai_import_assist_ui142.py tests/test_ai_import_api_ui142.py
```

These tests use synthetic inputs and a replaced provider transport. They do not verify production credentials or available credit.

## Data and usage boundaries

Before requesting suggestions, review the selected headers and up to eight sample rows. Exclude sensitive values that do not belong in an external request. The assistant sends the confirmed sample and mapping context, not the original file or entire workbook. The server bounds columns, cell lengths, request bytes and response bytes and asks for structured output with response storage disabled. This request setting is not a claim about the provider's retention policy.

The local limits are 100 requests per project per UTC day, 20 per named user per UTC day, six per user per minute and two concurrent requests per project. Connection tests share these limits. Persistent operation identifiers prevent duplicate provider calls and duplicate local quota charges. Do not create a new identifier to retry an uncertain request automatically; a fresh request requires another explicit user action.

Review returned suggestions before applying them, then review the import before saving. No suggestion or connection test writes inventory automatically. Record actual deployment and live connection results separately from local regression results.
