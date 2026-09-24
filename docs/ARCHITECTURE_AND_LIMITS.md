# Architecture and trust boundary — fictional client demo

```
Tester browser -> provider TLS endpoint -> Nginx on 0.0.0.0:$PORT
                                      -> independent demo cookie gate on 127.0.0.1:8766
                                      -> Wavelink on 127.0.0.1:8765 (one worker)
                                      -> one SQLite-WAL project at /var/data/wavelink/project
```

The launcher checks a real `/var/data` mount using Linux mount metadata; a directory with that name is not enough. It prepares only its supplied fictional seed, once under explicit first-deploy authorization. Initialized project files and hub identity must remain present. A missing initialized database or key does not trigger replacement. A completely empty replacement disk can only be distinguished from first use once the one-time environment switch has been disabled: this is a required post-bootstrap step.

After mount ownership setup, the supervisor drops to UID/GID 10001 before any project or HTTP handling. It starts the existing hosted CLI without secret/local/multiworker environment overrides, then the gate, then the public gateway. All components stop when one exits; no replica/writer scaling is supported. Source and dependencies are inside the image, not the data disk. The root entrypoint, Docker build and real provider mount ownership still require platform testing.

Nginx requires the canonical Host and exactly `X-Forwarded-Proto: https`. It whitelists supported application HTTP/WebSocket headers and replaces forwarding metadata rather than trusting client-supplied forwarding chains. The IP supplied to Wavelink is the ingress TCP peer, NOT a certified original end-user address. Application login throttling may consequently share that peer bucket among testers. Gateway admission uses a conservative global attempt budget for this small demonstration.

The gate protects static assets, APIs, downloads and new WebSocket upgrades, except its own login/logout pages and minimal health status. Gate authentication never replaces the Wavelink Bearer token. It uses a generated persistent HMAC key, a password-specific cookie epoch, explicit expiry, same-origin/CSRF form checks and Secure/HttpOnly/SameSite cookies. It is deliberately not a production identity provider or MFA implementation. Wavelink retains named account authorization; its existing password, session and role semantics are not silently rewritten.

A gate session is checked at requests/new upgrades, not continuously within an existing WebSocket. Restart the service to close existing connections when withdrawing access. Do not claim that removing access recalls downloads or already saved browser data.

The encrypted inherited recovery helper covers its prepared-project format only. This wrapper's deployment marker and cookie key require additional encrypted operator preservation/reconstruction. Provider off-site backup, automatic retention/alerts, complete wrapper restoration and remote browser parity remain unresolved real-data gates. Client demonstration data should be considered disposable until those checks pass.

No PostgreSQL adapter, Redis coordination, distributed session/live-update service, independent replicas, multi-company tenancy or vessel/cloud synchronization is implemented. One isolated fictional company/project per service. Do not convert this seeded demonstration into a production project by uploading real records.

Image base and apt package versions are not digest-pinned. Python package versions match the installed local test environment; package availability, registry pulls and dependency vulnerability status were not verified online. Render compatibility and account access were not available for live testing.
