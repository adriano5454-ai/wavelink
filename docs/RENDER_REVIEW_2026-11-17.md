# Wavelink hosting review

Reviewed on 17 November 2026 in Adriano's workspace. Metrics cover approximately 11:06 on 16 November to 11:06 on 17 November, Brazil time.

## Availability

| Service | Render state | Live source |
| --- | --- | --- |
| Wavelink website | Active, latest deployment live | Website commit 8b7cb8bd75a9e96275688574cf57362f0769f426 |
| Wavelink client demo | Active, latest deployment live | App commit f6d69ded35576b558d1ca4ebd0cb568681afe750 |
| Wavelink Corcovado | Active, latest deployment live | App commit f6d69ded35576b558d1ca4ebd0cb568681afe750 |

Both public application health endpoints returned `{"status":"ready"}` through the browser.

- https://demo.mywavelink.com/healthz
- https://corcovado.mywavelink.com/healthz

## Observed capacity

Values below use Render's returned 15-minute samples across the review window. CPU is expressed as a percentage of allocated CPU. Memory values are rounded.

| Service | Average CPU use | Highest sampled memory | Memory allocation | Memory used |
| --- | --- | --- | --- | --- |
| Corcovado | 0.36% | 140 MiB | 512 MiB | 27.3% |
| Demo | 0.41% | 158 MiB | 2,048 MiB | 7.7% |

Each application had one instance throughout the sampled window. These observations describe the current traffic. Load capacity under concurrent document imports still needs application-level testing.

## Requests and observability

- The returned request metrics contained no HTTP 5xx series for either application.
- Corcovado recorded 613 HTTP 200 responses and one HTTP 404 response.
- Demo recorded 2,517 HTTP 200, eight HTTP 303, 256 HTTP 401, 120 HTTP 404 and two status-0 entries.
- The logs API returned no entries, including an unfiltered recent query. The cause of individual 401, 404 and status-0 entries remains unverified.
- Latency queries at 15-minute and one-minute resolution returned no samples. A p95 response-time claim cannot be made from this data.
- The current gateway source disables Nginx access logging and writes its error log to a runtime file. That limits stdout-based gateway diagnostics.

## Deployment findings

Both app services currently have an empty Render HTTP health-check path. Their existing `/healthz` endpoints are working. Configuring Render to use those endpoints is the next hosting improvement, after checking the intended deployment window.

Both app services follow the same repository's main branch with automatic deployment on commit. A release to that branch targets both demo and Corcovado. Each app has a 10 GB persistent disk. Render documents that disk-backed services have a deployment interruption.

The review was read-only in Render. The UI140 and website 3.2.0 candidates remain pending publication and the backend integration checks described in UI140_REVIEW.md.

## References

- https://render.com/docs/health-checks
- https://render.com/docs/deploys
- https://dashboard.render.com/web/srv-daqas5k9v7es73cgjhp0
- https://dashboard.render.com/web/srv-das4ujojo6nc73a7u53g
- https://dashboard.render.com/static/srv-darf4ep42hec73ag632g
