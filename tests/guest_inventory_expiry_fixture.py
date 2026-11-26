"""Run the Inventory expiry browser test against a compiled, fictional local checkout.

python tests/guest_inventory_expiry_fixture.py --runtime RUNTIME --control-dir NEW_DIR \
    --cert LOCAL_TEST_CERT --key LOCAL_TEST_KEY [--port 19485]

The browser test uses playwright-core and WAVELINK_TEST_CHROMIUM. Do not provide
production files. Only the included, digest-checked demo archive is admitted.
"""
import argparse
import asyncio
from pathlib import Path
import secrets
import sys
import tempfile
import time

import uvicorn
from starlette.requests import Request
from starlette.responses import Response


def local_fixture(port, control):
    from deploy.gate import Gate, PUBLIC_COOKIE, TTL
    from deploy.native_showcase import NativeShowcase

    def clock():
        return time.time() + (TTL + 5) * sum(1 for _ in control.glob("advance-*"))

    authority = f"127.0.0.1:{port}"
    gate = Gate(f"https://{authority}", secrets.token_urlsafe(28), secrets.token_bytes(32),
                "qa-fictional", secrets.token_urlsafe(28), public_entry=True, clock=clock)
    repo = Path(__file__).resolve().parents[1]
    gate.showcase = NativeShowcase(gate, repo / "vendor/FICTIONAL_DEMO.ajproject")
    native, core = gate.app(), gate.showcase.core
    short = control / "short-next"

    async def app(scope, receive, send):
        if scope["type"] == "lifespan":
            return await core(scope, receive, send)
        path = scope["path"]
        if scope["type"] == "websocket":
            if path == "/__demo/native/ws":
                return await native(scope, receive, send)
            return await send({"type":"websocket.close", "code":1008})
        req = Request(scope)
        if req.headers.get("host") != authority or req.method not in ("GET", "HEAD"):
            return await Response(status_code=403)(scope, receive, send)

        async def fixture_send(message):
            if message["type"] == "http.response.start":
                headers = [(k, v) for k, v in message["headers"] if k != b"cache-control"]
                if path == "/__demo/public" and short.exists():
                    for i, (key, value) in enumerate(headers):
                        if key == b"set-cookie" and value.startswith((PUBLIC_COOKIE+"=").encode()):
                            assert f"Max-Age={TTL}".encode() in value
                            headers[i] = (key, value.replace(f"Max-Age={TTL}".encode(), b"Max-Age=6"))
                            short.unlink()
                            break
                message = {**message, "headers": headers + [(b"cache-control",b"no-store")]}
            await send(message)

        if path in ("/__demo/public", "/__demo/login") or path.startswith("/__demo/native/"):
            return await native(scope, receive, fixture_send)
        if path.startswith("/__demo/"):
            return await Response(status_code=404)(scope, receive, fixture_send)
        # Like the demo's reverse proxy, present the original URI to the gate.
        uri = scope["raw_path"] + (b"?" + scope["query_string"] if scope["query_string"] else b"")
        headers = [(k,v) for k,v in scope["headers"] if not k.startswith(b"x-demo-original-")]
        checked = Request({**scope, "headers":headers + [(b"x-demo-original-uri",uri),
                                                         (b"x-demo-original-method",req.method.encode())]})
        if (await gate.check(checked)).status_code != 204:
            return await (await gate.required(checked))(scope, receive, fixture_send)
        return await (native if path.startswith("/api/") else core)(scope, receive, fixture_send)

    return app


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--control-dir", type=Path, required=True)
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--key", type=Path, required=True)
    parser.add_argument("--port", type=int, default=19485, choices=range(1024, 65536), metavar="PORT")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    runtime, control = args.runtime.resolve(), args.control_dir.resolve()
    if not (runtime / "RELEASE_FILES.json").is_file():
        parser.error("--runtime must be a materialized app release")
    control.mkdir(exist_ok=False)
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(repo), str(runtime)]
    with tempfile.TemporaryDirectory(prefix="wl-inventory-expiry-server-") as scratch:
        previous_temp = tempfile.tempdir
        tempfile.tempdir = scratch
        try:
            config = uvicorn.Config(local_fixture(args.port, control), host="127.0.0.1", port=args.port,
                                    ssl_certfile=str(args.cert), ssl_keyfile=str(args.key), proxy_headers=False,
                                    access_log=False, log_level="warning", timeout_graceful_shutdown=3)
            server = uvicorn.Server(config)
            serving = asyncio.create_task(server.serve())
            client = None
            try:
                for _ in range(300):
                    if server.started:
                        break
                    if serving.done():
                        await serving
                        raise RuntimeError("Local fixture stopped during startup")
                    await asyncio.sleep(.1)
                else:
                    raise RuntimeError("Local fixture did not start")
                client = await asyncio.create_subprocess_exec(
                    "node", str(repo / "tests/browser_guest_inventory_expiry.cjs"),
                    f"https://127.0.0.1:{args.port}", str(control))
                return await asyncio.wait_for(client.wait(), timeout=240)
            finally:
                if client and client.returncode is None:
                    client.terminate()
                    await client.wait()
                server.should_exit = True
                await serving
        finally:
            tempfile.tempdir = previous_temp


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
