"""Same-container gateway config. Hosted application stays loopback-only."""
from pathlib import Path
import re

def render(authority: str, port: int, runtime: Path, *, app_port=8765, gate_port=8766, bind='0.0.0.0') -> str:
    if not re.fullmatch(r'[a-z0-9.-]+(?::[0-9]{1,5})?', authority) or not 1024 <= port <= 65535:
        raise ValueError('Invalid gateway authority or port.')
    if bind not in ('0.0.0.0', '127.0.0.1') or any(c in str(runtime) for c in ' \t\n;{}"'):
        raise ValueError('Invalid gateway runtime path.')
    runtime.mkdir(parents=True, exist_ok=True)
    for name in ('body', 'proxy'):
        (runtime / name).mkdir(exist_ok=True)
    # Never append/trust a browser-supplied XFF chain. The logged client address
    # supplied to Wavelink is the ingress TCP peer, not a claimed end-user IP.
    clear = '''proxy_set_header Forwarded "";
            proxy_set_header X-Forwarded-Host "";
            proxy_set_header X-Forwarded-Port "";
            proxy_set_header X-Forwarded-Prefix "";
            proxy_set_header X-Real-IP "";'''
    probe = f'''location = /healthz {{
            limit_except GET HEAD {{ deny all; }}
            proxy_pass http://127.0.0.1:{app_port}/readyz;
            proxy_pass_request_headers off;
            proxy_set_header Host 127.0.0.1:{app_port};
            proxy_set_header Origin "";
            proxy_set_header X-Forwarded-For "";
            proxy_set_header X-Forwarded-Proto "";
            {clear}
        }}'''
    config = f'''worker_processes 1;
pid {runtime}/nginx.pid;
error_log /dev/stderr crit;
events {{ worker_connections 512; }}
http {{
    access_log off;
    server_tokens off;
    default_type application/octet-stream;
    client_body_temp_path {runtime}/body;
    proxy_temp_path {runtime}/proxy;
    client_max_body_size 25m;
    client_body_timeout 30s;
    keepalive_timeout 30s;
    map $http_upgrade $connection_upgrade {{ default upgrade; '' close; }}
    # Platform ingress must attest TLS. Ambiguous values fail closed.
    map $http_x_forwarded_proto $demo_tls_ok {{ default 0; https 1; }}
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
        location = /_demo_verify {{
            internal;
            proxy_pass http://127.0.0.1:{gate_port}/__demo/check;
            proxy_pass_request_body off;
            proxy_set_header Content-Length "";
            proxy_set_header Host {authority};
        }}
        location = /__demo/check {{ return 404; }}
        location = /__demo/required {{ return 404; }}
        location ^~ /__demo/ {{
            if ($demo_tls_ok = 0) {{ return 400; }}
            if ($http_host != "{authority}") {{ return 421; }}
            client_max_body_size 4k;
            proxy_pass http://127.0.0.1:{gate_port};
            proxy_set_header Host {authority};
        }}
        location @demo_denied {{
            proxy_pass http://127.0.0.1:{gate_port};
            rewrite ^ /__demo/required break;
            proxy_pass_request_body off;
            proxy_set_header Content-Length "";
            proxy_set_header Host {authority};
            proxy_set_header X-Demo-Original-URI $request_uri;
            proxy_set_header X-Demo-Original-Method $request_method;
        }}
        location / {{
            if ($demo_tls_ok = 0) {{ return 400; }}
            if ($http_host != "{authority}") {{ return 421; }}
            auth_request /_demo_verify;
            error_page 401 = @demo_denied;
            proxy_pass http://127.0.0.1:{app_port};
            proxy_http_version 1.1;
            # Whitelist the exact browser/HTTP/WS headers required by 1.34.19.
            # Ingress-specific or forged X-Forwarded-* values cannot reach it.
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
            proxy_hide_header Server;

        }}
    }}
}}
'''
    # Restrict presentation changes to the application's own JavaScript file.
    # Original documents, JSON, generated reports and attachments never pass
    # through this substitution location.
    start = config.index('        location / {\n            if ($demo_tls_ok')
    end = config.index('\n        }\n', start) + len('\n        }\n')
    common = config[start:end]
    presentation = common.replace('location / {', 'location = /static/app.js {', 1)
    substitutions = '            # Demo-only PRESENTATION substitutions; vendored source is untouched.\n            # Do not substitute JSON, downloads, evidence or identifiers.\n            proxy_set_header Accept-Encoding "";\n            sub_filter_types application/javascript text/javascript;\n            sub_filter_once off;\n            sub_filter \'ONBOARD HUB\' \'PRIVATE ONLINE DEMO\';\n            sub_filter \'Need access or a password reset? Ask the PC hub administrator.\' \'Need access or a password reset? Ask your online project administrator.\';\n            sub_filter \'Keep the Windows hub running and awake. Phones must be able to reach its IP address on the approved local network. No internet is needed during local use.\' \'This demonstration runs on the hosting server. No Windows Admin or laptop needs to stay open. An internet connection is required for this separate online demo.\';\n            sub_filter \'This address is saved in the PC Admin console.\' \'This is the configured online demonstration address.\';\n            sub_filter \'To change it, synchronise work, stop the hub, enter the correct PC IP, Save address and restart.\' \'The hosting operator manages the online address. Preserve unsent work before changing domains.\';\n'
    presentation = presentation.replace('            proxy_hide_header Server;\n',
                                        '            proxy_hide_header Server;\n' + substitutions)
    return config[:start] + presentation + config[start:]
