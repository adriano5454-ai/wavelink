"""One explicitly authorised, fictional-only server-side project preparation.

This module never uses the desktop GUI or a local project catalogue. It cannot
load a user-provided dataset. Existing deployment identity/files are checked
before startup; a missing initialized project is NEVER silently reseeded.
"""
from __future__ import annotations
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import secrets
import sqlite3
import sys
import uuid

SEED_SHA256 = '6a406262adb2fc593cdc6dbc620f591bb79eca28d93f3735f58b66a0a03aa702'
DEPLOYMENT_ID = 'wavelink-client-demo-2026-09-24-r1'
ADMIN_LOGIN = 'adriano.admin'
MARKER = 'DEPLOYMENT.json'

class DemoError(ValueError):
    """Bounded operator-safe error; never include secrets or input values."""


def private_json(path: Path, value: dict) -> None:
    raw = json.dumps(value, indent=2).encode()
    temporary = path.with_name(path.name + '.new-' + uuid.uuid4().hex)
    try:
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def secret_value(value: str, label: str) -> str:
    if not isinstance(value, str) or not 20 <= len(value) <= 128 or value != value.strip() or any(ord(x) < 32 for x in value):
        raise DemoError(f'{label} must be a new 20-128 character secret without outer spaces or control characters.')
    return value


def settings_dict(root: Path, hub_id: str, origin: str, app_port: int) -> dict:
    return dict(format='wavelink-hosted-runtime-1', mode='private_staging',
                project_dir=str(root / 'project'), expected_hub_id=hub_id,
                external_origin=origin, listen_host='127.0.0.1', listen_port=app_port,
                trusted_proxy_ips=['127.0.0.1'], acknowledge_private_staging=True)


def prepare(root: Path, source: Path, seed: Path, environ: dict, *, app_port=8765) -> dict:
    """Prepare or verify ONLY this deployment's explicit directory.

    Filesystem mount verification happens before this method in entrypoint.py.
    Paths are injectable here solely to permit disposable local acceptance tests.
    """
    if source.resolve() not in map(Path, sys.path):
        sys.path.insert(0, str(source.resolve()))
    from app.hosted_config import canonical_origin, HostedSettings
    from app.hosted_storage import PreparedProject
    from app.projects import FileLease

    raw_origin = environ.get('PUBLIC_URL', '') or environ.get('RENDER_EXTERNAL_URL', '')
    if not raw_origin and environ.get('RENDER_EXTERNAL_HOSTNAME'):
        raw_origin = 'https://' + environ['RENDER_EXTERNAL_HOSTNAME']
    if not raw_origin:
        raise DemoError('Set PUBLIC_URL to the exact assigned HTTPS address. No address was guessed.')
    origin = canonical_origin(raw_origin)
    gate_password = secret_value(environ.get('DEMO_ACCESS_PASSWORD', ''), 'DEMO_ACCESS_PASSWORD')
    if root.is_symlink() or root.resolve() != root or root == Path('/'):
        raise DemoError('The demo data root must be a separate absolute directory, without symbolic links.')
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    marker = root / MARKER
    # Do not follow a substituted lock target.
    if (root / '.bootstrap.lock').is_symlink():
        raise DemoError('Unsafe bootstrap lease.')
    with FileLease(root / '.bootstrap.lock'):
        if not marker.exists():
            if any(p.name != '.bootstrap.lock' for p in root.iterdir()):
                raise DemoError('Incomplete or unknown data directory. No files were overwritten or reseeded.')
            if environ.get('INITIALISE_FICTIONAL_DEMO') != 'YES_FIRST_DEPLOY_ONLY':
                raise DemoError('No initialized demo exists. Explicit first-deploy authorisation is required; do not reseed a lost disk.')
            admin_password = secret_value(environ.get('INITIAL_ADMIN_PASSWORD', ''), 'INITIAL_ADMIN_PASSWORD')
            if secrets.compare_digest(gate_password.encode(), admin_password.encode()):
                raise DemoError('Use different administrator and demonstration-access passwords.')
            if hashlib.sha256(seed.read_bytes()).hexdigest() != SEED_SHA256:
                raise DemoError('The fictional seed checksum does not match the reviewed seed.')
            from app.project_transfer import import_project
            from app.accounts import password_hash
            from app.projects import atomic_json
            import_project(seed, root / 'project', 'Wavelink | FICTIONAL CLIENT DEMONSTRATION')
            hub_file = root / 'project/hub.json'
            config = json.loads(hub_file.read_text())
            # Readiness checks use this independent identity. No source/vessel UUID is reused.
            config['allow_legacy_codes'] = False
            config['project_name'] = 'Wavelink | FICTIONAL CLIENT DEMONSTRATION'
            atomic_json(hub_file, config)
            with closing(sqlite3.connect(root / 'project/dives.sqlite3')) as con:
                admin = con.execute("SELECT id FROM users WHERE login_id='demo.admin' AND role='admin'").fetchone()
                if admin is None:
                    raise DemoError('Expected fictional administrator identity is missing. No service was started.')
                con.execute('UPDATE users SET enabled=0, credential_version=credential_version+1, password_hash=?, failures=0, locked_until=0',
                            (password_hash(secrets.token_urlsafe(48)),))
                con.execute("UPDATE users SET login_id=?, name='Adriano - demo administrator', enabled=1, password_hash=? WHERE id=?",
                            (ADMIN_LOGIN, password_hash(admin_password), admin[0]))
                con.execute('DELETE FROM sessions')
                con.execute('DELETE FROM participants')
                from app.store import utcnow
                con.execute('INSERT INTO user_audit(at,actor_id,target_id,action,detail) VALUES(?,?,?,?,?)',
                            (utcnow(), admin[0], admin[0], 'client_demo_first_provision',
                             json.dumps({'fictional_only': True, 'published_demo_accounts_disabled': True})))
                con.commit()
                if con.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                    raise DemoError('Initial fictional database integrity check failed.')
            operator = root / 'operator'
            operator.mkdir(mode=0o700)
            key = operator / 'gate.key'
            fd = os.open(key, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(secrets.token_bytes(32))
            record = dict(deployment=DEPLOYMENT_ID, fictional_only=True, hub_id=config['hub_id'],
                          upstream_version='1.34.19', seed_sha256=SEED_SHA256)
            # The marker is written LAST. An interrupted bootstrap never opens the partially prepared database.
            private_json(marker, record)
            print('Fictional demo prepared. Published sample logins are disabled. Remove first-deploy variables now.', flush=True)
        if marker.is_symlink() or not marker.is_file():
            raise DemoError('Deployment identity file is unavailable.')
        record = json.loads(marker.read_text())
        if record.get('deployment') != DEPLOYMENT_ID or record.get('fictional_only') is not True:
            raise DemoError('This is not the separately prepared fictional demo project.')
        operator = root / 'operator'
        key = operator / 'gate.key'
        if key.is_symlink() or not key.is_file() or len(key.read_bytes()) != 32:
            raise DemoError('The persistent access-session key is unavailable. Operator recovery is required.')
        if environ.get('INITIALISE_FICTIONAL_DEMO') == 'YES_FIRST_DEPLOY_ONLY':
            print('ACTION REQUIRED: set INITIALISE_FICTIONAL_DEMO=NO before sharing this demo; never permit reseeding after disk loss.', flush=True)
        proposed = settings_dict(root, record['hub_id'], origin, app_port)
        settings = HostedSettings.from_dict(proposed, environ={})
        PreparedProject(settings)
        config_file = operator / 'hosted.json'
        if not config_file.exists() or json.loads(config_file.read_text()) != proposed:
            private_json(config_file, proposed)
        for folder in ('recovery-work', 'backup-spool'):
            (root / folder).mkdir(exist_ok=True, mode=0o700)
        return dict(root=root, origin=origin, authority=settings.authority,
                    config=config_file, gate_key=key, hub_id=record['hub_id'])
