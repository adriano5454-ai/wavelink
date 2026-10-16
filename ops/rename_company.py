#!/usr/bin/env python3
"""Offline, copy-first rename of an existing C01 installation's current identity.

Dry-run is the default. This tool never contacts hosting or changes a database,
accounts, operational records, historical reports, SMTP settings or DNS. Stop the
whole company service before applying or recovering; all three app leases must
also be free. A full private local backup precedes the two JSON replacements.
"""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import sys
import uuid
from urllib.parse import urlsplit
import warnings

PENDING = 'COMPANY_RENAME_PENDING.json'
FORMAT = 'wavelink-company-rename-1'
FILES = ('project/hub.json', 'COMPANY_DEPLOYMENT.json')  # Marker commits last.
LOCKS = ('.bootstrap.lock', 'project/.admin.lock', 'project/.server.lock')
MARKER_KEYS = {'format', 'company_id', 'company_name', 'hub_id', 'installation_id',
               'admin_id', 'admin_login', 'initial_hash', 'initial_credential_version',
               'setup_key_sha256', 'created_at', 'created_epoch', 'setup_expires_epoch'}


class Refusal(ValueError):
    """Bounded diagnostic: never include file contents or credentials."""


def safe_path(path: Path) -> Path:
    path = Path(path)
    if (not path.is_absolute() or '..' in path.parts or path == Path(path.anchor)
            or any(p.is_symlink() for p in (path, *path.parents))):
        raise Refusal('Use an absolute independent path without links or parent traversal.')
    return path


def regular(path: Path) -> None:
    try:
        info = path.lstat()
    except OSError:
        raise Refusal('A required installation or backup file is unavailable.') from None
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise Refusal('Only independent regular files are accepted; links are refused.')


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_digest(path: Path) -> str:
    regular(path)
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while block := stream.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def read_json(path: Path, limit: int = 1_000_000) -> dict:
    regular(path)
    if path.stat().st_size > limit:
        raise Refusal('A required JSON file is too large.')
    try:
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError('duplicate key')
                result[key] = value
            return result
        def invalid_constant(_):
            raise ValueError('non-finite number')
        result = json.loads(path.read_text('utf-8'), object_pairs_hook=unique,
                            parse_constant=invalid_constant)
    except (ValueError, UnicodeError):
        raise Refusal('A required JSON file is invalid or contains duplicate keys.') from None
    if not isinstance(result, dict):
        raise Refusal('A required JSON file is not an object.')
    return result


def encoded(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def sync_directory(path: Path) -> None:
    if os.name == 'posix':
        fd = os.open(path, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def atomic_write(path: Path, data: bytes) -> None:
    if path.exists():
        regular(path)
    temporary = path.with_name(path.name + '.rename-' + uuid.uuid4().hex)
    try:
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        sync_directory(path.parent)
    finally:
        temporary.unlink(missing_ok=True)


class Lease:
    def __init__(self, path):
        self.path, self.stream = path, None

    def __enter__(self):
        if self.path.is_symlink():
            raise Refusal('An installation lease must not be a link.')
        if self.path.exists():
            regular(self.path)
        fd = os.open(self.path, os.O_RDWR | os.O_CREAT | getattr(os, 'O_NOFOLLOW', 0), 0o600)
        stream = os.fdopen(fd, 'r+b')
        try:
            if os.name == 'nt':
                import msvcrt
                if self.path.stat().st_size == 0:
                    stream.write(b'0'); stream.flush()
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            stream.close()
            raise Refusal('The company service or an Admin process is still using this installation.') from None
        self.stream = stream
        return self

    def __exit__(self, *_):
        if self.stream:
            try:
                if os.name == 'nt':
                    import msvcrt
                    self.stream.seek(0)
                    msvcrt.locking(self.stream.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self.stream.fileno(), fcntl.LOCK_UN)
            finally:
                self.stream.close()


def validate_company(company_id: str, name: str) -> None:
    if not re.fullmatch(r'[a-z][a-z0-9-]{1,39}', company_id):
        raise Refusal('Use a valid 2-40 character COMPANY_ID.')
    if not isinstance(name, str) or not 2 <= len(name) <= 80 or name != name.strip() or any(ord(c) < 32 for c in name):
        raise Refusal('Use a valid 2-80 character COMPANY_NAME.')


def validate_origin(origin: str) -> str:
    try:
        url = urlsplit(origin)
        port = url.port
    except ValueError:
        raise Refusal('Use one exact HTTPS public origin.') from None
    if (url.scheme != 'https' or not url.hostname or url.username or url.password
            or url.path or url.query or url.fragment or port not in (None, 443)
            or not re.fullmatch(r'[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?', url.hostname)
            or origin != 'https://' + url.hostname
            or origin == 'https://demo.mywavelink.com'):
        raise Refusal('Use one canonical HTTPS company origin without a path, port or credentials.')
    return origin


def validate_identity(deploy: Path, company_id: str, name: str) -> None:
    deploy = safe_path(deploy)
    identities = read_json(deploy / 'company_identities.json', 128_000)
    identity = identities.get(company_id)
    if not isinstance(identity, dict) or identity.get('name') != name:
        raise Refusal('The reviewed repository identity does not exactly match the company ID and name.')
    filename = identity.get('logo')
    if not isinstance(filename, str) or not re.fullmatch(r'[A-Za-z0-9_-]+\.(?:png|jpg|jpeg)', filename):
        raise Refusal('The reviewed company identity needs a PNG or JPEG logo.')
    logo = safe_path(deploy / 'company_logos' / company_id / filename)
    regular(logo)
    if not 1 <= logo.stat().st_size <= 2_000_000:
        raise Refusal('The reviewed company logo is unavailable or exceeds its size limit.')
    try:
        from PIL import Image
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(logo.read_bytes())) as image:
                if (image.format not in ('PNG', 'JPEG') or getattr(image, 'n_frames', 1) != 1
                        or max(image.size) > 4096 or image.width * image.height > 8_000_000):
                    raise Refusal('The reviewed company logo is not a supported static image.')
                image.verify()
    except ImportError:
        raise Refusal('Run this tool in the Wavelink runtime with Pillow installed.') from None
    except (OSError, ValueError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise Refusal('The reviewed company logo did not pass decoding validation.') from None


def inventory(root: Path) -> dict[str, str]:
    safe_path(root)
    if not root.is_dir():
        raise Refusal('A complete installation or backup directory is unavailable.')
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        for name in dirs:
            safe_path(Path(directory) / name)
        for name in files:
            path = Path(directory) / name
            relative = path.relative_to(root).as_posix()
            if relative in (*LOCKS, PENDING):
                continue
            result[relative] = file_digest(path)
    return result


def walk_error(_):
    raise Refusal('A directory could not be fully read; no complete backup or snapshot is claimed.')


def require_installation_owner(root: Path) -> None:
    """A root shell must not strand 0600 JSON/leases under the wrong owner."""
    if os.name != 'posix':
        raise Refusal('Applying this hosting transition requires the POSIX company runtime.')
    for path in (root, root / 'project', root / FILES[0], root / FILES[1]):
        info = path.stat()
        if (info.st_uid, info.st_gid) != (os.geteuid(), os.getegid()):
            raise Refusal('Run apply/recovery as the existing installation owner and primary group (normally UID/GID 10001), not a different maintenance user.')


def plan(root: Path, deploy: Path, from_id: str, from_name: str, to_id: str,
         to_name: str, public_url: str) -> tuple[dict, dict[str, bytes]]:
    root = safe_path(root)
    if not root.is_dir() or not (root / 'project').is_dir():
        raise Refusal('Select the existing whole C01 company directory.')
    if (root / PENDING).exists() or (root / PENDING).is_symlink():
        raise Refusal('A company rename is pending. Run --recover before restarting or renaming.')
    validate_company(from_id, from_name)
    validate_company(to_id, to_name)
    if from_id == to_id or from_name == to_name:
        raise Refusal('This procedure requires a different company ID and name.')
    validate_origin(public_url)
    validate_identity(deploy, from_id, from_name)
    validate_identity(deploy, to_id, to_name)
    marker = read_json(root / FILES[1])
    if set(marker) != MARKER_KEYS or marker.get('format') != 'wavelink-company-c01':
        raise Refusal('The existing C01 installation marker is incompatible.')
    already_done = marker.get('company_id') == to_id and marker.get('company_name') == to_name
    if not already_done and (marker.get('company_id') != from_id or marker.get('company_name') != from_name):
        raise Refusal('The existing disk does not match the explicitly selected source company.')
    try:
        for key in ('hub_id', 'installation_id', 'admin_id'):
            if str(uuid.UUID(marker[key])) != marker[key]:
                raise ValueError()
    except (TypeError, ValueError, KeyError, AttributeError):
        raise Refusal('The existing installation identity is invalid.') from None
    hub = read_json(safe_path(root / FILES[0]))
    if hub.get('hub_id') != marker['hub_id'] or not isinstance(hub.get('defaults'), dict):
        raise Refusal('The project configuration does not match the existing company marker.')
    if already_done and (hub.get('project_name') == from_name or
            any(hub['defaults'].get(key) == from_name for key in ('company', 'project', 'client'))):
        raise Refusal('The target marker and current default names disagree. Review the interrupted transition.')
    regular(safe_path(root / 'project/dives.sqlite3'))
    changed = ['COMPANY_DEPLOYMENT.json:company_id', 'COMPANY_DEPLOYMENT.json:company_name']
    retained = []
    new_hub = json.loads(json.dumps(hub))
    if hub.get('project_name') == from_name:
        new_hub['project_name'] = to_name
        changed.append('project/hub.json:project_name')
    else:
        retained.append('project_name')
    for key in ('company', 'project', 'client'):
        if hub['defaults'].get(key) == from_name:
            new_hub['defaults'][key] = to_name
            changed.append('project/hub.json:defaults.' + key)
        else:
            retained.append('defaults.' + key)
    new_marker = {**marker, 'company_id': to_id, 'company_name': to_name}
    proposed = {FILES[0]: encoded(new_hub), FILES[1]: encoded(new_marker)}
    result = dict(status='dry_run', source_company=from_name, destination_company=to_name,
                  changed_fields=changed, retained_custom_fields=retained,
                  environment_after=dict(COMPANY_ID=to_id, COMPANY_NAME=to_name,
                      PUBLIC_URL=public_url, INITIALISE_COMPANY='NO'),
                  preserved=['hub_id', 'installation_id', 'accounts', 'credentials', 'database',
                      'operational records', 'history', 'files', 'SMTP settings'],
                  follow_up=['Change service environment only after this offline migration succeeds.',
                      'Review and save the current PDF report profile through Administration > Company branding.',
                      'Existing exported PDFs and historical evidence retain their original identity.',
                      'Review outstanding invitation/signing links and drafts saved under the previous browser origin.',
                      'Verify DNS, HTTPS, the exact public origin and real email links after restart.'])
    if already_done:
        result.update(status='already_renamed_offline', changed_fields=[])
        proposed = {}
    return result, proposed


def make_backup(root: Path, backup_parent: Path, original: dict[str, str]) -> Path:
    backup_parent = safe_path(backup_parent)
    if backup_parent == root or root in backup_parent.parents or backup_parent in root.parents:
        raise Refusal('Use a backup directory separate from and outside the company directory.')
    backup_parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if os.name == 'posix' and backup_parent.stat().st_mode & 0o077:
        raise Refusal('The backup parent must be private to its owner (mode 0700).')
    required = sum((root / name).stat().st_size for name in original)
    reserve = max(16 * 1024 * 1024, required // 20)
    if shutil.disk_usage(backup_parent).free < required + reserve:
        raise Refusal('Insufficient free space for the complete private backup and a safety margin. No configuration was replaced.')
    backup = backup_parent / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + uuid.uuid4().hex)
    backup.mkdir(mode=0o700)
    snapshot = backup / 'company'
    snapshot.mkdir(mode=0o700)
    # Include empty directories as well as every regular file. The backup parent
    # is already private; every copied directory/file also gets owner-only mode.
    for directory, dirs, _ in os.walk(root, followlinks=False, onerror=walk_error):
        for name in dirs:
            source = safe_path(Path(directory) / name)
            (snapshot / source.relative_to(root)).mkdir(mode=0o700)
    for name, expected in sorted(original.items()):
        source = root / name
        target = snapshot / name
        regular(source)
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with source.open('rb') as src, os.fdopen(fd, 'wb') as dst:
            shutil.copyfileobj(src, dst, 1024 * 1024)
            dst.flush(); os.fsync(dst.fileno())
        if file_digest(source) != expected or file_digest(target) != expected:
            raise Refusal('Installation files changed during backup. No configuration was replaced.')
    if inventory(root) != original or inventory(snapshot) != original:
        raise Refusal('The complete backup does not match the stopped installation.')
    for directory, _, _ in os.walk(snapshot, topdown=False, onerror=walk_error):
        sync_directory(Path(directory))
    atomic_write(backup / 'BACKUP_MANIFEST.json', encoded(dict(format=FORMAT, files=original)))
    sync_directory(backup_parent)
    return backup


def recover(root: Path, *, apply=False, service_stopped=False) -> dict:
    root = safe_path(root)
    journal = read_json(root / PENDING)
    if (journal.get('format') != FORMAT or journal.get('root') != str(root)
            or not isinstance(journal.get('files'), dict) or set(journal['files']) != set(FILES)):
        raise Refusal('The pending rename journal is incompatible; retain all recovery evidence.')
    backup = safe_path(Path(journal.get('backup', '')))
    if backup == root or root in backup.parents or backup in root.parents:
        raise Refusal('The pending backup location is not independent.')
    saved = read_json(backup / 'BACKUP_MANIFEST.json')
    if saved.get('format') != FORMAT or not isinstance(saved.get('files'), dict):
        raise Refusal('The private backup manifest is invalid.')
    # Verify the full private backup before offering or applying recovery.
    if inventory(backup / 'company') != saved['files']:
        raise Refusal('The complete private backup has changed. No automatic recovery is allowed.')
    originals = {}
    for name in FILES:
        item = journal['files'][name]
        if (not isinstance(item, dict) or set(item) != {'before', 'after'}
                or saved['files'].get(name) != item['before']):
            raise Refusal('The pending rename does not match its private backup.')
        current = file_digest(safe_path(root / name))
        if current not in (item['before'], item['after']):
            raise Refusal('A current configuration was edited after interruption. Operator review is required.')
        originals[name] = (backup / 'company' / name).read_bytes()
    result = dict(status='recovery_dry_run', backup=str(backup),
                  action='Restore the two original JSON files; no database or records are replaced.')
    if not apply:
        return result
    if not service_stopped:
        raise Refusal('Applying recovery requires --service-stopped after stopping the whole service.')
    require_installation_owner(root)
    with ExitStack() as stack:
        for name in LOCKS:
            stack.enter_context(Lease(root / name))
        # Recheck the journal, backup and current bytes after acquiring leases.
        checked = recover(root, apply=False)
        if checked['backup'] != str(backup):
            raise Refusal('The recovery journal changed before the leases were acquired.')
        originals = {name: (backup / 'company' / name).read_bytes() for name in FILES}
        if any(digest(originals[name]) != journal['files'][name]['before'] for name in FILES):
            raise Refusal('The original configuration backup changed after recovery validation.')
        before_data = inventory(root)
        for name in reversed(FILES):
            atomic_write(root / name, originals[name])
        after_data = inventory(root)
        if ({k:v for k,v in before_data.items() if k not in FILES}
                != {k:v for k,v in after_data.items() if k not in FILES}):
            raise Refusal('Unrelated installation data changed during recovery; retain the pending journal.')
        atomic_write(backup / 'RENAME_RECEIPT.json', encoded(dict(status='rolled_back', format=FORMAT)))
        (root / PENDING).unlink()
        sync_directory(root)
    return {**result, 'status': 'recovered_original_identity'}


def rename(root: Path, deploy: Path, from_id: str, from_name: str, to_id: str,
           to_name: str, public_url: str, *, apply=False, service_stopped=False,
           backup_parent: Path | None = None) -> dict:
    args = (root, deploy, from_id, from_name, to_id, to_name, public_url)
    result, proposed = plan(*args)
    if not apply or result['status'] == 'already_renamed_offline':
        return result
    if not service_stopped:
        raise Refusal('Applying a rename requires --service-stopped after stopping the whole service.')
    root = safe_path(root)
    require_installation_owner(root)
    with ExitStack() as stack:
        for name in LOCKS:
            stack.enter_context(Lease(root / name))
        result, proposed = plan(*args)
        if result['status'] == 'already_renamed_offline':
            return result
        original = inventory(root)
        backup = make_backup(root, backup_parent or root.parent / (root.name + '-rename-backups'), original)
        journal = dict(format=FORMAT, root=str(root), backup=str(backup), files={
            name: dict(before=original[name], after=digest(proposed[name])) for name in FILES})
        atomic_write(root / PENDING, encoded(journal))
        try:
            for name in FILES:
                if file_digest(root / name) != original[name]:
                    raise Refusal('A configuration changed after backup. The rename was stopped.')
                atomic_write(root / name, proposed[name])
            expected = {**original, **{name: digest(data) for name, data in proposed.items()}}
            if inventory(root) != expected:
                raise Refusal('Unrelated installation files changed during the rename.')
            atomic_write(backup / 'RENAME_RECEIPT.json', encoded(dict(format=FORMAT, status='renamed',
                source_company=from_name, destination_company=to_name,
                files=journal['files'], database_unchanged=True)))
            (root / PENDING).unlink()
            sync_directory(root)
        except Exception:
            # We already own all leases: restore both JSON files directly. A hard
            # interruption leaves the durable journal for explicit --recover.
            try:
                for name in FILES:
                    if file_digest(root / name) not in (original[name], digest(proposed[name])):
                        raise Refusal('A configuration was edited externally; retain the journal for operator review.')
                for name in reversed(FILES):
                    atomic_write(root / name, (backup / 'company' / name).read_bytes())
                atomic_write(backup / 'RENAME_RECEIPT.json', encoded(dict(format=FORMAT, status='rolled_back')))
                (root / PENDING).unlink()
                sync_directory(root)
            except Exception:
                raise Refusal('Rename interrupted and rollback incomplete. Keep the service stopped and use --recover.') from None
            raise Refusal('Rename refused; both original JSON files were restored. Keep the private backup.') from None
    return {**result, 'status': 'renamed_offline', 'backup': str(backup), 'database_unchanged': True}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path, help='Existing whole company directory')
    parser.add_argument('--deploy-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'deploy')
    parser.add_argument('--from-id')
    parser.add_argument('--from-name')
    parser.add_argument('--to-id')
    parser.add_argument('--to-name')
    parser.add_argument('--public-url')
    parser.add_argument('--backup-parent', type=Path)
    parser.add_argument('--recover', action='store_true', help='Review or roll back a pending interrupted rename')
    parser.add_argument('--apply', action='store_true', help='Without this flag, report only')
    parser.add_argument('--service-stopped', action='store_true', help='Confirm the whole company service is stopped')
    args = parser.parse_args(argv)
    try:
        if args.recover:
            result = recover(args.root, apply=args.apply, service_stopped=args.service_stopped)
        else:
            if any(value is None for value in (args.from_id, args.from_name, args.to_id, args.to_name, args.public_url)):
                parser.error('rename requires --from-id, --from-name, --to-id, --to-name and --public-url')
            result = rename(args.root, args.deploy_dir, args.from_id, args.from_name,
                args.to_id, args.to_name, args.public_url, apply=args.apply,
                service_stopped=args.service_stopped, backup_parent=args.backup_parent)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (Refusal, OSError) as exc:
        # OSError may contain private filenames; keep the public message bounded.
        print('REFUSED: ' + (str(exc) if isinstance(exc, Refusal) else 'Filesystem operation failed; retain recovery evidence.'), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
