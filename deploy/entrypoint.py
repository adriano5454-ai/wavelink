"""Single-container supervisor; no desktop GUI, second app worker, or vessel access."""

from __future__ import annotations

import http.client
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

from .provision import DemoError, prepare
from .nginx_config import render


BASE = Path('/opt/wavelink')
MOUNT = Path('/var/data')
DATA = MOUNT / 'wavelink'

APP_PORT = 8765
GATE_PORT = 8766


def mounted(path: Path) -> bool:
    """Check the mount table, not merely whether an ephemeral directory exists."""
    try:
        return any(
            line.split()[4] == str(path)
            for line in Path('/proc/self/mountinfo').read_text().splitlines()
        )
    except (OSError, IndexError):
        return False


def minimal_environment() -> dict:
    return {
        'PATH': os.environ.get(
            'PATH',
            '/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
        ),
        'LANG': 'C.UTF-8',
        'LC_ALL': 'C.UTF-8',
        'HOME': '/tmp',
        'PYTHONDONTWRITEBYTECODE': '1',
        'PYTHONUNBUFFERED': '1',
    }


def wait_ready(
    child,
    port,
    path,
    *,
    host=None,
    accepted=(200,),
    seconds=90,
):
    end = time.monotonic() + seconds

    while time.monotonic() < end:
        if child.poll() is not None:
            raise DemoError(
                'A service stopped during startup. '
                'Review the restricted operator logs.'
            )

        con = None

        try:
            con = http.client.HTTPConnection(
                '127.0.0.1',
                port,
                timeout=1,
            )

            con.request(
                'GET',
                path,
                headers={
                    'Host': host or f'127.0.0.1:{port}',
                },
            )

            response = con.getresponse()
            response.read()

            if response.status in accepted:
                return

        except OSError:
            pass

        finally:
            if con:
                con.close()

        time.sleep(0.25)

    raise DemoError(
        'A service did not become ready. '
        'No public listener was started.'
    )


def run() -> int:
    os.umask(0o077)

    if not mounted(MOUNT):
        raise DemoError(
            'A persistent disk must be mounted at /var/data. '
            'Refusing ephemeral storage.'
        )

    if DATA.is_symlink():
        raise DemoError('Unsafe data root.')

    DATA.mkdir(
        mode=0o700,
        exist_ok=True,
    )

    # The provider mounts the volume before runtime.
    # Drop privilege before any project, authentication
    # or HTTP code handles client requests.
    if os.geteuid() == 0:
        os.chown(DATA, 10001, 10001)
        os.setgroups([])
        os.setgid(10001)
        os.setuid(10001)

    port = int(
        os.environ.get(
            'PORT',
            '10000',
        )
    )

    if (
        not 1024 <= port <= 65535
        or port in (APP_PORT, GATE_PORT)
    ):
        raise DemoError(
            'PORT must be a high port different '
            'from the private application ports.'
        )

    cfg = prepare(
        DATA,
        BASE / 'app',
        BASE / 'vendor/FICTIONAL_DEMO.ajproject',
        dict(os.environ),
    )

    runtime = Path('/tmp/wavelink-gateway')

    runtime.mkdir(
        mode=0o700,
        exist_ok=True,
    )

    nginx_file = runtime / 'nginx.conf'

    nginx_file.write_text(
        render(
            cfg['authority'],
            port,
            runtime,
        )
    )

    # Validate generated Nginx configuration before starting
    # the application or public-facing listener.
    check = subprocess.run(
        [
            'nginx',
            '-t',
            '-c',
            str(nginx_file),
        ],
        env=minimal_environment(),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )

    if check.returncode:
        detail = (check.stderr or '').strip()

        if len(detail) > 1500:
            detail = detail[-1500:]

        raise DemoError(
            'Gateway configuration validation failed. '
            + (
                detail
                if detail
                else 'No Nginx diagnostic was returned.'
            )
        )

    processes = []
    stopping = False

    def stop_signal(_sig, _frame):
        nonlocal stopping
        stopping = True

    signal.signal(
        signal.SIGTERM,
        stop_signal,
    )

    signal.signal(
        signal.SIGINT,
        stop_signal,
    )

    exitcode = 0

    try:
        application = subprocess.Popen(
            [
                sys.executable,
                'run_hosted.py',
                'serve',
                '--config',
                str(cfg['config']),
            ],
            cwd=BASE / 'app',
            env=minimal_environment(),
        )

        processes.append(application)

        wait_ready(
            application,
            APP_PORT,
            '/readyz',
        )

        gate_env = minimal_environment()

        gate_env.update(
            DEMO_GATE_ORIGIN=cfg['origin'],
            DEMO_GATE_KEY_FILE=str(cfg['gate_key']),
            DEMO_ACCESS_PASSWORD=os.environ[
                'DEMO_ACCESS_PASSWORD'
            ],
            DEMO_GATE_PORT=str(GATE_PORT),
        )

        gate = subprocess.Popen(
            [
                sys.executable,
                '-m',
                'deploy.gate',
            ],
            cwd=BASE,
            env=gate_env,
        )

        processes.append(gate)

        wait_ready(
            gate,
            GATE_PORT,
            '/__demo/check',
            accepted=(401,),
        )

        gateway = subprocess.Popen(
            [
                'nginx',
                '-c',
                str(nginx_file),
                '-g',
                'daemon off;',
            ],
            env=minimal_environment(),
        )

        processes.append(gateway)

        print(
            'Wavelink fictional client demo started. '
            'One application worker; browser administration; '
            'no native Admin.',
            flush=True,
        )

        while not stopping:
            if any(
                process.poll() is not None
                for process in processes
            ):
                print(
                    'A demo service exited. '
                    'Stopping all components; '
                    'platform restart is required.',
                    flush=True,
                )

                exitcode = 1
                break

            time.sleep(0.5)

    finally:
        # Stop admitting requests before shutting down
        # the gateway, gate and application.
        for process in reversed(processes):
            if process.poll() is None:
                process.terminate()

        deadline = time.monotonic() + 35

        for process in reversed(processes):
            try:
                process.wait(
                    timeout=max(
                        0.1,
                        deadline - time.monotonic(),
                    )
                )

            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

        print(
            'Demo processes stopped. '
            'Persistent project retained.',
            flush=True,
        )

    return exitcode


if __name__ == '__main__':
    try:
        raise SystemExit(run())

    except DemoError as exc:
        print(
            'Demo startup stopped: ' + str(exc),
            file=sys.stderr,
        )

    except (ValueError, OSError) as exc:
        detail = str(exc).strip()

        if len(detail) > 1200:
            detail = detail[-1200:]

        print(
            f'Demo startup stopped ({type(exc).__name__}): '
            + (
                detail
                if detail
                else 'No diagnostic message was returned.'
            ),
            file=sys.stderr,
        )
