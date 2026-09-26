"""C01 company TLS/host ingress. No demonstration-password gate or auto-guest."""
from pathlib import Path
import re


def render_company(authority: str, port: int, runtime: Path, *, app_port=8765, bind='0.0.0.0') -> str:
    if (not re.fullmatch(r'[a-z0-9.-]+(?::[0-9]{1,5})?', authority)
            or type(port) is not int or not 1024 <= port <= 65535
            or type(app_port) is not int or not 1024 <= app_port <= 65535 or app_port == port):
        raise ValueError('Invalid company gateway authority or port.')
    if bind not in ('0.0.0.0', '127.0.0.1') or any(c in str(runtime) for c in ' \t\n;{}"'):
        raise ValueError('Invalid company gateway runtime path.')
    runtime.mkdir(parents=True, exist_ok=True)
    for name in ('body','proxy','fastcgi','uwsgi','scgi'):
        (runtime/name).mkdir(parents=True, exist_ok=True, mode=0o700)
    clear='''proxy_set_header Forwarded "";
            proxy_set_header X-Forwarded-Host "";
            proxy_set_header X-Forwarded-Port "";
            proxy_set_header X-Forwarded-Prefix "";
            proxy_set_header X-Real-IP "";'''
    probe=f'''location = /healthz {{
            limit_except GET HEAD {{ deny all; }}
            proxy_pass http://127.0.0.1:{app_port}/readyz;
            proxy_pass_request_headers off;
            proxy_set_header Host 127.0.0.1:{app_port};
            proxy_set_header Origin "";
            proxy_set_header X-Forwarded-For "";
            proxy_set_header X-Forwarded-Proto "";
            {clear}
        }}'''
    common=f'''if ($company_tls_ok = 0) {{ return 400; }}
            if ($http_host != "{authority}") {{ return 421; }}
            proxy_pass http://127.0.0.1:{app_port};
            proxy_http_version 1.1;
            proxy_pass_request_headers off;
            proxy_set_header Content-Type $content_type;
            proxy_set_header Accept $http_accept;
            proxy_set_header Accept-Language $http_accept_language;
            proxy_set_header Origin $http_origin;
            proxy_set_header X-AJ-Hub-ID $http_x_aj_hub_id;
            proxy_set_header If-None-Match $http_if_none_match;
            proxy_set_header If-Modified-Since $http_if_modified_since;
            proxy_set_header Range $http_range;
            proxy_set_header If-Range $http_if_range;
            proxy_set_header Sec-WebSocket-Key $http_sec_websocket_key;
            proxy_set_header Sec-WebSocket-Version $http_sec_websocket_version;
            proxy_set_header Sec-WebSocket-Protocol $http_sec_websocket_protocol;
            proxy_set_header Sec-WebSocket-Extensions $http_sec_websocket_extensions;
            proxy_set_header Host {authority};
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header X-Forwarded-For $remote_addr;
            {clear}
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header Authorization $http_authorization;
            proxy_buffering off;
            proxy_read_timeout 3600s;
            proxy_send_timeout 60s;
            proxy_hide_header Server;'''
    presentation='''proxy_set_header Accept-Encoding "";
            sub_filter_types application/javascript text/javascript;
            sub_filter_once off;
            sub_filter 'ONBOARD HUB' 'COMPANY WORKSPACE';
            sub_filter 'Need access or a password reset? Ask the PC hub administrator.' 'Need access or a password reset? Ask your company administrator.';
            sub_filter 'Keep the Windows hub running and awake. Phones must be able to reach its IP address on the approved local network. No internet is needed during local use.' 'This company workspace runs on its separate hosting service. An internet connection is required.';
            sub_filter 'This address is saved in the PC Admin console.' 'This is the configured company workspace address.';
            sub_filter 'To change it, synchronise work, stop the hub, enter the correct PC IP, Save address and restart.' 'The hosting operator manages the company address. Preserve unsent work before changing domains.';'''
    return f'''worker_processes 1;
pid {runtime}/nginx.pid;
error_log {runtime}/error.log notice;
events {{ worker_connections 512; }}
http {{
    access_log off;
    server_tokens off;
    default_type application/octet-stream;
    client_body_temp_path {runtime}/body;
    proxy_temp_path {runtime}/proxy;
    fastcgi_temp_path {runtime}/fastcgi;
    uwsgi_temp_path {runtime}/uwsgi;
    scgi_temp_path {runtime}/scgi;
    client_max_body_size 25m;
    client_body_timeout 30s;
    keepalive_timeout 30s;
    map $http_upgrade $connection_upgrade {{ default upgrade; '' close; }}
    map $http_x_forwarded_proto $company_tls_ok {{ default 0; https 1; }}
    server {{
        listen {bind}:{port} default_server;
        server_name _;
        {probe}
        location / {{ return 421; }}
    }}
    server {{
        listen {bind}:{port};
        server_name {authority.split(':')[0]};
        add_header X-Content-Type-Options nosniff always;
        add_header Referrer-Policy no-referrer always;
        add_header X-Frame-Options SAMEORIGIN always;
        add_header Cache-Control "no-store" always;
        {probe}
        location ^~ /company-setup/ {{ client_max_body_size 4k; {common} }}
        location = /company-setup {{ {common} }}
        location = /api/login {{ client_max_body_size 4k; {common} }}
        location ^~ /api/document-sign/ {{ client_max_body_size 100k; {common} }}
        location = /static/app.js {{ {common}
            {presentation}
        }}
        location / {{ {common} }}
    }}
}}
'''
