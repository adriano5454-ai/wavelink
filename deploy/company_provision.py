"""C01: new, isolated company project; never import/reseed the fictional demo.

Secrets are runtime inputs only. A weak initial password is usable only with an
independent setup secret, before normal API access is enabled. No public reset.
"""
from __future__ import annotations
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time
import uuid

from .provision import DemoError, private_json, secret_value, settings_dict

FORMAT = 'wavelink-company-c01'
MARKER = 'COMPANY_DEPLOYMENT.json'
ACTIVATION = 'company_first_password_change'


def digest(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def validate_environment(env: dict) -> tuple[str, str, str]:
    from app.hosted_config import canonical_origin
    slug, name = env.get('COMPANY_ID', ''), env.get('COMPANY_NAME', '')
    if not re.fullmatch(r'[a-z][a-z0-9-]{1,39}', slug):
        raise DemoError('COMPANY_ID must be 2-40 lowercase letters, digits or hyphens, beginning with a letter.')
    if not isinstance(name, str) or not 2 <= len(name) <= 80 or name != name.strip() or any(ord(c) < 32 for c in name):
        raise DemoError('COMPANY_NAME must be 2-80 printable characters, without outer spaces.')
    if env.get('DEMO_PUBLIC_ENTRY', 'NO') != 'NO' or env.get('INITIALISE_FICTIONAL_DEMO', 'NO') != 'NO':
        raise DemoError('Company mode cannot enable demo entry or fictional initialization.')
    if any(env.get(k) for k in ('DEMO_ACCESS_PASSWORD', 'DEMO_GUEST_LOGIN', 'DEMO_GUEST_PASSWORD', 'INITIAL_ADMIN_PASSWORD')):
        raise DemoError('Use a new service with company settings, not copied demonstration credentials.')
    initial = env.get('INITIALISE_COMPANY', 'NO')
    if env.get('COMPANY_RENEW_SETUP', 'NO') not in ('NO', 'YES'):
        raise DemoError('COMPANY_RENEW_SETUP must be NO or YES.')
    if initial not in ('NO', 'YES_FIRST_DEPLOY_ONLY'):
        raise DemoError('INITIALISE_COMPANY must be NO or YES_FIRST_DEPLOY_ONLY.')
    origin = canonical_origin(env.get('PUBLIC_URL', ''))
    if origin == 'https://demo.mywavelink.com':
        raise DemoError('The demonstration address cannot be used for the company installation.')
    return slug, name, origin


def read_marker(root: Path) -> dict:
    from app.hosted_config import read_object
    record = read_object(root / MARKER)
    keys = {'format', 'company_id', 'company_name', 'hub_id', 'installation_id',
            'admin_id', 'admin_login', 'initial_hash', 'initial_credential_version',
            'setup_key_sha256', 'created_at', 'created_epoch', 'setup_expires_epoch'}
    if set(record) != keys or record.get('format') != FORMAT:
        raise DemoError('Company installation marker is missing, incomplete or incompatible. No project was created.')
    for key in ('hub_id', 'installation_id', 'admin_id'):
        if str(uuid.UUID(record[key])) != record[key]:
            raise DemoError('Company installation identity is invalid.')
    if not re.fullmatch(r'[a-f0-9]{64}', record['setup_key_sha256']) or not record['initial_hash'].startswith('pbkdf2_sha256$'):
        raise DemoError('Company bootstrap verification is unavailable.')
    if type(record['initial_credential_version']) is not int or record['initial_credential_version'] < 1:
        raise DemoError('Invalid initial company credential version.')
    if any(type(record[k]) not in (int, float) for k in ('created_epoch', 'setup_expires_epoch')):
        raise DemoError('Invalid company activation window.')
    return record


def activation(con, record: dict) -> dict | None:
    """Authoritative SQL state, not a writable boolean in browser/config data."""
    rows = con.execute('SELECT detail FROM user_audit WHERE action=? AND target_id=?',
                       (ACTIVATION, record['admin_id'])).fetchall()
    matches = []
    for row in rows:
        detail = json.loads(row[0])
        if detail.get('installation_id') == record['installation_id']:
            if detail.get('hub_id') != record['hub_id'] or not re.fullmatch(r'[a-f0-9]{64}', detail.get('request_fingerprint', '')):
                raise DemoError('Company activation evidence is inconsistent. Operator review is required.')
            matches.append(detail)
    if len(matches) > 1:
        raise DemoError('Duplicate company activation evidence. Operator review is required.')
    return matches[0] if matches else None


def verify_activation(con, record: dict) -> bool:
    done = activation(con, record)
    row = con.execute('SELECT * FROM users WHERE id=?', (record['admin_id'],)).fetchone()
    if done:
        # Later ordinary account lifecycle actions are allowed; never open the
        # original temporary credential again after a partial restore.
        if row and (row['password_hash'] == record['initial_hash'] or row['credential_version'] <= record['initial_credential_version']):
            raise DemoError('Initial company credentials conflict with saved activation evidence.')
        return True
    if (not row or row['login_id'] != record['admin_login'] or row['role'] != 'admin' or not row['enabled']
            or row['password_hash'] != record['initial_hash'] or row['credential_version'] != record['initial_credential_version']):
        raise DemoError('Pending administrator no longer matches this setup. No automatic reset is permitted.')
    return False


def prepare_company(root: Path, source: Path, env: dict, *, app_port: int = 8765) -> dict:
    """Fresh empty directory or exact existing marker only. No seed parameter."""
    source = source.resolve()
    if str(source) not in sys.path:
        sys.path.insert(0, str(source))
    from app.projects import FileLease
    from app.hosted_config import HostedSettings
    from app.hosted_storage import PreparedProject
    from app.server import create_app, load_config
    from app.store import utcnow, pack
    from app.accounts import normal_login

    slug, name, origin = validate_environment(env)
    if not root.is_absolute() or root == Path('/') or root.resolve() != root or any(p.is_symlink() for p in (root, *root.parents)):
        raise DemoError('Company storage must be a separate absolute directory without links.')
    if root.exists() and not root.is_dir():
        raise DemoError('Company storage is not a directory.')
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    if (root / '.bootstrap.lock').is_symlink():
        raise DemoError('Unsafe company preparation lease.')
    with FileLease(root / '.bootstrap.lock'):
        marker = root / MARKER
        if not marker.exists():
            if env.get('COMPANY_RENEW_SETUP') == 'YES':
                raise DemoError('Setup renewal requires an existing pending company, not a new disk.')
            if any(p.name != '.bootstrap.lock' for p in root.iterdir()):
                raise DemoError('Unknown or incomplete company storage. No files overwritten or reseeded.')
            if env.get('INITIALISE_COMPANY') != 'YES_FIRST_DEPLOY_ONLY':
                raise DemoError('No initialized company exists. Explicit first-deploy authorization is required.')
            login = normal_login(env.get('COMPANY_ADMIN_LOGIN', ''))
            password = env.get('COMPANY_INITIAL_PASSWORD', '')
            if not isinstance(password, str) or not 6 <= len(password) <= 128 or any(ord(c) < 32 for c in password):
                raise DemoError('COMPANY_INITIAL_PASSWORD must contain 6-128 printable characters.')
            key = secret_value(env.get('COMPANY_SETUP_KEY', ''), 'COMPANY_SETUP_KEY')
            if len(key) < 32 or key == password:
                raise DemoError('Use a separate randomly generated COMPANY_SETUP_KEY of at least 32 characters.')
            project = root / 'project'
            cfg = load_config(project)
            cfg.update(label='Wavelink', project_name=name, allow_legacy_codes=False,
                       defaults={'company': name, 'project': name, 'client': name, 'vessel': '', 'vehicle': ''})
            private_json(project / 'hub.json', cfg)
            core = create_app(project, prepared_config=cfg)
            person = core.state.accounts.create(login, login, password, 'admin')
            with core.state.store.connection(True) as con:
                # Deliberately empty operational library. The supported lifecycle
                # tombstone stops the bundled sample from reappearing on restart.
                core.state.store.checklists._set_original_state(con, 'purged',
                    {'login_id': 'company-initialization'}, 'Fresh company: bundled sample not adopted.')
                core.state.store.checklists._purge_original(con)
                row = con.execute('SELECT * FROM users WHERE id=?', (person['id'],)).fetchone()
                now = time.time()
                record = dict(format=FORMAT, company_id=slug, company_name=name, hub_id=cfg['hub_id'],
                              installation_id=str(uuid.uuid4()), admin_id=person['id'], admin_login=login,
                              initial_hash=row['password_hash'], initial_credential_version=row['credential_version'],
                              setup_key_sha256=digest(key), created_at=utcnow(), created_epoch=now,
                              setup_expires_epoch=now + 24 * 3600)
                con.execute('INSERT INTO user_audit(at,actor_id,target_id,action,detail) VALUES(?,?,?,?,?)',
                    (utcnow(), person['id'], person['id'], 'company_initialization',
                     pack({'company_id': slug, 'installation_id': record['installation_id'], 'empty_project': True,
                           'normal_access_locked_until_password_change': True})))
            del core
            (root / 'operator').mkdir(mode=0o700)
            # Marker last; interrupted preparation must be reviewed, never retried
            # as a destructive reset. No seed, operational records or sample users.
            private_json(marker, record)
        record = read_marker(root)
        if record['company_id'] != slug or record['company_name'] != name:
            raise DemoError('Company ID/name do not match the existing disk. No company was renamed or recreated.')
        proposed = settings_dict(root, record['hub_id'], origin, app_port)
        settings = HostedSettings.from_dict(proposed, environ={})
        prepared = PreparedProject(settings)
        with closing(prepared.connect(readonly=True)) as con:
            active = verify_activation(con, record)
            if not active and con.execute('SELECT count(*) FROM users').fetchone()[0] != 1:
                raise DemoError('Unexpected users in a pending installation. Activation stopped.')
        if env.get('COMPANY_RENEW_SETUP') == 'YES':
            if active:
                raise DemoError('Completed company setup cannot be renewed or reset.')
            key = secret_value(env.get('COMPANY_SETUP_KEY', ''), 'COMPANY_SETUP_KEY')
            if len(key) < 32 or digest(key) == record['setup_key_sha256']:
                raise DemoError('Setup renewal requires a DIFFERENT random key of at least 32 characters.')
            from app.hosted_runtime import project_leases
            with project_leases(settings):
                with closing(prepared.connect(readonly=True)) as con:
                    if verify_activation(con, record):
                        raise DemoError('Setup completed before renewal. No account was changed.')
                record = {**record, 'setup_key_sha256': digest(key), 'setup_expires_epoch': time.time()+24*3600}
                private_json(marker, record)
            print('Pending first-sign-in key renewed; account and records unchanged. Remove COMPANY_RENEW_SETUP before the next restart.', flush=True)
        operator = root / 'operator'
        if operator.is_symlink() or not operator.is_dir():
            raise DemoError('Company operator directory is unavailable.')
        config_file = operator / 'hosted.json'
        if config_file.is_symlink():
            raise DemoError('Unsafe company runtime configuration.')
        if not config_file.exists() or json.loads(config_file.read_text()) != proposed:
            private_json(config_file, proposed)
        for folder in ('recovery-work', 'backup-spool'):
            path = root / folder
            if path.is_symlink():
                raise DemoError('Unsafe company backup directory.')
            path.mkdir(exist_ok=True, mode=0o700)
        if env.get('INITIALISE_COMPANY') == 'YES_FIRST_DEPLOY_ONLY':
            print('Company disk initialized/verified. Set INITIALISE_COMPANY=NO and remove initial password/setup key settings after first sign-in.', flush=True)
        return dict(root=root, origin=origin, authority=settings.authority, config=config_file,
                    hub_id=record['hub_id'], active=active)
