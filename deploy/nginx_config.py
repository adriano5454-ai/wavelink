from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse


def _escape_nginx(value: str) -> str:
    return (
        value.replace('\\', '\\\\')
        .replace('"', '\\"')
        .replace('$', '\\$')
    )


def render(authority: str, public_port: int, runtime: Path) -> str:
    parsed = urlparse(authority)

    if parsed.scheme != 'https':
        raise ValueError('Hosted demo authority must use https.')

    host = parsed.hostname

    if not host:
        raise ValueError('Hosted demo authority has no hostname.')

    runtime = Path(runtime)

    client_temp = runtime / 'client_body'
    proxy_temp = runtime / 'proxy'
    fastcgi_temp = runtime / 'fastcgi'
    uwsgi_temp = runtime / 'uwsgi'
    scgi_temp = runtime / 'scgi'

    for path in (
        client_temp,
        proxy_temp,
        fastcgi_temp,
        uwsgi_temp,
        scgi_temp,
    ):
        path.mkdir(
            mode=0o700,
            parents=True,
            exist_ok=True,
        )

    host_q = _escape_nginx(host)

    return f'''
worker_processes  1;

pid {runtime / "nginx.pid"};

error_log stderr notice;

events {{
    worker_connections 1024;
}}

http {{
    access_log off;

    client_body_temp_path {client_temp};
    proxy_temp_path {proxy_temp};
    fastcgi_temp_path {fastcgi_temp};
    uwsgi_temp_path {uwsgi_temp};
    scgi_temp_path {scgi_temp};

    client_max_body_size 64m;

    map $http_upgrade $connection_upgrade {{
        default upgrade;
        ''      close;
    }}

    server {{
        listen 0.0.0.0:{public_port};

        server_name {host_q};

        location = /healthz {{
            proxy_pass http://127.0.0.1:8766/__demo/healthz;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-Host $host;
        }}

        location / {{
            proxy_pass http://127.0.0.1:8766;
            proxy_http_version 1.1;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-Host $host;

            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;

            proxy_read_timeout 300s;
            proxy_send_timeout 300s;
        }}
    }}
}}
'''.strip() + '\n'
