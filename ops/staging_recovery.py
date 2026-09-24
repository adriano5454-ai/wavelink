#!/usr/bin/env python3
"""Independent PRIVATE-STAGING recovery helper for verified Wavelink 1.34.19.

Never deploys, discovers projects, overwrites a project, or contacts a network.
Backup uses SQLite's coherent online-backup API; source sessions are untouched.
The encrypted copy removes sessions/participants. Restore creates a NEW folder.
This is an operator-level full private copy, not an end-user export permission API.
"""
from __future__ import annotations
import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import sqlite3
import stat
import sys
import tempfile
import time
import zipfile
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

VERSION = '1.34.19'
SOURCE_ZIP_SHA256 = '8c1b6a8d731d01b05a1290d3a1dd1a544054147aac9048ca345af7983613cd9e'
MAGIC = b'WAVELINK-STAGING-BACKUP-1\n'
AAD = MAGIC
CHUNK = 1024 * 1024
MAX_DB = 500_000_000   # Conservative pilot limit, not a new Wavelink database limit.
MAX_ENVELOPE = 510_000_000
MAX_JSON = 256_000
MEMBERS = {'manifest.json', 'dives.sqlite3', 'hub.json', 'hosted.json'}

class Refusal(ValueError):
    """Safe operator-facing refusal. Never contains supplied secrets."""

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        while b := f.read(CHUNK): h.update(b)
    return h.hexdigest()

def regular(path: Path) -> None:
    s = path.lstat()
    if not stat.S_ISREG(s.st_mode) or path.is_symlink() or s.st_nlink != 1:
        raise Refusal('A required file is not an independent regular file.')

def safe_path(path: Path) -> Path:
    p = Path(path)
    if not p.is_absolute() or '..' in p.parts or p == Path(p.anchor):
        raise Refusal('Use an explicit absolute subpath without parent traversal.')
    if any(x.is_symlink() for x in (p, *p.parents)):
        raise Refusal('Symbolic links are not accepted.')
    return p

def key_bytes(path: Path) -> bytes:
    path = safe_path(path); regular(path)
    if os.name == 'posix' and path.stat().st_mode & 0o077:
        raise Refusal('Restrict the key file to its owner (mode 0600).')
    k = path.read_bytes()
    if len(k) != 32: raise Refusal('The key file must contain exactly 32 random bytes.')
    return k

def new_key(path: Path) -> None:
    path = safe_path(path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as f:
        f.write(secrets.token_bytes(32)); f.flush(); os.fsync(f.fileno())

def load_source(source: Path):
    source = safe_path(source); regular(source / 'RELEASE_FILES.json')
    m = json.loads((source / 'RELEASE_FILES.json').read_text())
    if m.get('version') != VERSION or m.get('format') != 'aj-release-files-1':
        raise Refusal('Only the verified 1.34.19 source is supported by this helper.')
    # Manifest is additionally pinned below, not merely trusted as supplied.
    if sha(source / 'RELEASE_FILES.json') != PINNED_MANIFEST_SHA256:
        raise Refusal('Release manifest does not match the reviewed source.')
    for name, expected in m['files'].items():
        p = source / name
        if name.startswith('/') or '..' in Path(name).parts:
            raise Refusal('Invalid release path.')
        regular(p)
        if sha(p) != expected: raise Refusal('Source verification failed; no project was changed.')
    sys.path.insert(0, str(source))
    from app.hosted_config import HostedSettings
    from app.hosted_storage import PreparedProject
    from app.projects import FileLease
    return HostedSettings, PreparedProject, FileLease, len(m['files'])

def db_summary(db: Path) -> dict:
    """Integrity plus content hashes. No raw record fields or credentials returned."""
    regular(db)
    with closing(sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)) as c:
        if c.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
            raise Refusal('Snapshot database integrity check failed.')
        if c.execute('PRAGMA foreign_key_check').fetchone() is not None:
            raise Refusal('Snapshot database has a foreign-key violation.')
        names = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        tables = {}; blobs = {}
        for name in names:
            quoted = '"' + name.replace('"','""') + '"'
            columns = c.execute('PRAGMA table_info(' + quoted + ')').fetchall()
            blob_ix = [i for i,r in enumerate(columns) if r[2].upper() == 'BLOB']
            rows = []; blob_hashes = []; bytes_total = 0
            for row in c.execute('SELECT * FROM ' + quoted):
                normal = [ {'bytes_sha256':hashlib.sha256(v).hexdigest(), 'size':len(v)} if isinstance(v,bytes) else v for v in row]
                rows.append(hashlib.sha256(json.dumps(normal,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest())
                for i in blob_ix:
                    v = row[i]
                    if isinstance(v,bytes):
                        bytes_total += len(v); blob_hashes.append(hashlib.sha256(v).hexdigest())
            tables[name] = {'rows':len(rows),'sha256':hashlib.sha256('\n'.join(sorted(rows)).encode()).hexdigest()}
            if blob_ix:
                blobs[name] = {'values':len(blob_hashes),'bytes':bytes_total,'sha256':hashlib.sha256('\n'.join(sorted(blob_hashes)).encode()).hexdigest()}
        return {'integrity_check':'ok','foreign_key_check':'ok','tables':tables,'blob_stores':blobs}

def write_private(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd,'wb') as f:
        f.write(data); f.flush(); os.fsync(f.fileno())

def seal(plain: Path, encrypted: Path, key: bytes) -> None:
    nonce = secrets.token_bytes(12)
    enc = Cipher(algorithms.AES(key),modes.GCM(nonce)).encryptor()
    enc.authenticate_additional_data(AAD)
    with plain.open('rb') as src, encrypted.open('xb') as dst:
        os.chmod(encrypted,0o600)
        dst.write(MAGIC); dst.write(nonce)
        while b := src.read(CHUNK): dst.write(enc.update(b))
        dst.write(enc.finalize()); dst.write(enc.tag); dst.flush(); os.fsync(dst.fileno())

def unseal(encrypted: Path, plain: Path, key: bytes) -> None:
    regular(encrypted); size = encrypted.stat().st_size
    if not len(MAGIC)+28 < size <= MAX_ENVELOPE:
        raise Refusal('Encrypted backup has an invalid or unsupported size.')
    with encrypted.open('rb') as src:
        if src.read(len(MAGIC)) != MAGIC: raise Refusal('Not this staging recovery format.')
        nonce = src.read(12); src.seek(-16,2); tag = src.read(16)
        src.seek(len(MAGIC)+12)
        dec = Cipher(algorithms.AES(key),modes.GCM(nonce,tag)).decryptor(); dec.authenticate_additional_data(AAD)
        left = size-len(MAGIC)-28
        try:
            with plain.open('xb') as dst:
                os.chmod(plain,0o600)
                while left:
                    b = src.read(min(CHUNK,left))
                    if not b: raise Refusal('Truncated encrypted backup.')
                    left -= len(b); dst.write(dec.update(b))
                dst.write(dec.finalize())
        except Exception:
            plain.unlink(missing_ok=True)
            raise Refusal('Backup authentication failed; no restored project was published.') from None

def outside(candidate: Path, directory: Path):
    if candidate == directory or directory in candidate.parents:
        raise Refusal('Keep key, output and scratch storage outside the source project.')

def publish_without_overwrite(temp: Path, destination: Path) -> None:
    # EXCL creates a reservation. A concurrent destination is never overwritten.
    fd = os.open(destination,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    os.close(fd)
    try: os.replace(temp,destination)
    except BaseException:
        destination.unlink(missing_ok=True); raise

def backup(source: Path, config: Path, keyfile: Path, out: Path, scratch: Path, confirm_hub: str) -> dict:
    Settings, Prepared, Lease, count = load_source(source)
    config=safe_path(config); out=safe_path(out); scratch=safe_path(scratch); keyfile=safe_path(keyfile)
    settings=Settings.from_file(config)
    if settings.expected_hub_id != confirm_hub:
        raise Refusal('Confirm the exact prepared hub UUID.')
    prepared=Prepared(settings)
    for p in (out,scratch,keyfile): outside(p,settings.project_dir)
    outside(out,source)
    if out.exists(): raise Refusal('Backup output already exists; no overwrite is supported.')
    if not scratch.is_dir() or not out.parent.is_dir(): raise Refusal('Create protected scratch/output parent directories first.')
    if prepared.path.stat().st_size > MAX_DB: raise Refusal('This staging helper is limited to 500 MB databases.')
    k=key_bytes(keyfile)
    started=time.monotonic()
    with Lease(settings.project_dir/'.staging-backup.lock'):
        with tempfile.TemporaryDirectory(prefix='wavelink-snapshot-',dir=scratch) as temp:
            root=Path(temp); os.chmod(root,0o700); target=root/'dives.sqlite3'
            cfg_raw=config.read_bytes(); hub_raw=prepared.config_path.read_bytes()
            def progress(status,remaining,total):
                if time.monotonic()-started > 600: raise Refusal('Snapshot time budget exceeded; retry during a quieter period.')
                if total * 4096 > MAX_DB * 2: raise Refusal('Snapshot exceeds the conservative pilot budget.')
            with closing(prepared.connect(readonly=True,timeout=15)) as src, closing(sqlite3.connect(target)) as dst:
                src.backup(dst,pages=256,progress=progress,sleep=0.05)
                dst.execute('PRAGMA secure_delete=ON')
                dst.execute('DELETE FROM sessions'); dst.execute('DELETE FROM participants'); dst.commit()
                dst.execute('PRAGMA journal_mode=DELETE'); dst.execute('VACUUM')
            os.chmod(target,0o600)
            prepared.assert_same_files()
            if config.read_bytes()!=cfg_raw or prepared.config_path.read_bytes()!=hub_raw:
                raise Refusal('Configuration changed during snapshot; nothing was published.')
            if target.stat().st_size>MAX_DB: raise Refusal('Snapshot exceeds the 500 MB pilot limit.')
            info=db_summary(target)
            write_private(root/'hub.json',hub_raw); write_private(root/'hosted.json',cfg_raw)
            manifest={'format':'wavelink-private-staging-recovery-1','application_version':VERSION,
                      'source_zip_sha256':SOURCE_ZIP_SHA256,'created_utc':datetime.now(timezone.utc).isoformat(),
                      'hub_id':settings.expected_hub_id,'sessions_removed_from_copy':True,
                      'files':{name:{'bytes':(root/name).stat().st_size,'sha256':sha(root/name)} for name in ['dives.sqlite3','hub.json','hosted.json']},
                      'database_summary':info}
            write_private(root/'manifest.json',(json.dumps(manifest,indent=2)+'\n').encode())
            plain=root/'snapshot.zip'
            with zipfile.ZipFile(plain,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
                for name in sorted(MEMBERS):z.write(root/name,name)
            with tempfile.TemporaryDirectory(prefix='.wavelink-encrypted-',dir=out.parent) as encdir:
                cipher=Path(encdir)/'backup.wlstaging';seal(plain,cipher,k)
                publish_without_overwrite(cipher,out)
    return {'result':'encrypted_snapshot_created','source_manifest_entries':count,'file_bytes':out.stat().st_size,
            'ciphertext_sha256':sha(out),'source_sessions_modified':False,'off_host_copy_performed':False,
            'database_bytes':manifest['files']['dives.sqlite3']['bytes'],'tables':len(info['tables']),
            'blob_values':sum(x['values'] for x in info['blob_stores'].values()),'elapsed_seconds':round(time.monotonic()-started,3)}

def restore(source: Path, encrypted: Path, keyfile: Path, destination: Path, confirm_hub: str) -> dict:
    Settings, Prepared, _, count=load_source(source)
    destination=safe_path(destination); encrypted=safe_path(encrypted)
    if destination.exists():raise Refusal('Restore requires a NEW folder; existing projects are never overwritten.')
    if not destination.parent.is_dir():raise Refusal('Create the protected restore parent first.')
    outside(destination,source)
    k=key_bytes(keyfile)
    started=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='.wavelink-restore-',dir=destination.parent) as td:
        root=Path(td);os.chmod(root,0o700);plain=root/'unverified.zip'
        unseal(encrypted,plain,k)
        staged=root/'project';staged.mkdir(mode=0o700)
        with zipfile.ZipFile(plain) as z:
            members=z.infolist();names=[i.filename for i in members]
            if set(names)!=MEMBERS or len(names)!=len(MEMBERS):raise Refusal('Unexpected or duplicate archive members.')
            if any(i.flag_bits & 1 for i in members):raise Refusal('Nested encrypted archive is not supported.')
            if z.getinfo('dives.sqlite3').file_size>MAX_DB or any(z.getinfo(n).file_size>MAX_JSON for n in MEMBERS-{'dives.sqlite3'}):
                raise Refusal('Restore archive exceeds the conservative pilot limits.')
            manifest=json.loads(z.read('manifest.json'))
            if (manifest.get('format')!='wavelink-private-staging-recovery-1' or manifest.get('application_version')!=VERSION
                    or manifest.get('source_zip_sha256')!=SOURCE_ZIP_SHA256 or manifest.get('hub_id')!=confirm_hub
                    or set(manifest.get('files',{}))!=MEMBERS-{'manifest.json'}):
                raise Refusal('Recovery version, source, identity or members do not match.')
            for name,meta in manifest['files'].items():
                p=staged/name
                with z.open(name) as src,p.open('xb') as dst:shutil.copyfileobj(src,dst,CHUNK)
                os.chmod(p,0o600)
                if p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']:raise Refusal('Restored member checksum mismatch.')
        info=db_summary(staged/'dives.sqlite3')
        if info!=manifest['database_summary']:raise Refusal('Restored tables or attachments do not match the snapshot.')
        if any(info['tables'][n]['rows'] for n in ('sessions','participants')):
            raise Refusal('Snapshot unexpectedly contains active sessions/participants.')
        config=json.loads((staged/'hosted.json').read_text())
        if config['expected_hub_id']!=confirm_hub:raise Refusal('Configuration identity mismatch.')
        config['project_dir']=str(staged)
        config['external_origin']='https://restore-check.example.invalid'
        config['listen_host']='127.0.0.1';config['trusted_proxy_ips']=['127.0.0.1']
        Prepared(Settings.from_dict(config))
        config['project_dir']=str(destination)
        (staged/'hosted.json').write_text(json.dumps(config,indent=2)+'\n');os.chmod(staged/'hosted.json',0o600)
        # Publish only after authentication, all hashes and schema checks succeed.
        destination.mkdir(mode=0o700)   # exclusive; no overwrite
        try:
            for p in staged.iterdir():os.replace(p,destination/p.name)
            Prepared(Settings.from_file(destination/'hosted.json'))
        except BaseException:
            shutil.rmtree(destination);raise
    return {'result':'restored_to_new_folder','source_manifest_entries':count,'application_version':VERSION,
            'integrity_and_content_hashes':'matched','active_sessions_restored':False,
            'restored_origin':'https://restore-check.example.invalid','service_started':False,
            'tables':len(info['tables']),'blob_values':sum(x['values'] for x in info['blob_stores'].values()),
            'elapsed_seconds':round(time.monotonic()-started,3)}

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    key=sub.add_parser('keygen');key.add_argument('--key-file',type=Path,required=True)
    for name in ('backup','restore'):
        q=sub.add_parser(name)
        q.add_argument('--source-dir',type=Path,required=True);q.add_argument('--key-file',type=Path,required=True)
        q.add_argument('--confirm-hub-id',required=True)
        q.add_argument('--acknowledge-private-copy',action='store_true',required=True)
        if name=='backup':
            q.add_argument('--config',type=Path,required=True);q.add_argument('--output',type=Path,required=True)
            q.add_argument('--scratch-dir',type=Path,required=True)
        else:q.add_argument('--backup',type=Path,required=True);q.add_argument('--new-project-dir',type=Path,required=True)
    a=p.parse_args()
    try:
        if a.command=='keygen':
            new_key(a.key_file);result={'result':'key_created','key_printed':False,'escrow_required':True}
        elif a.command=='backup':result=backup(a.source_dir,a.config,a.key_file,a.output,a.scratch_dir,a.confirm_hub_id)
        else:result=restore(a.source_dir,a.backup,a.key_file,a.new_project_dir,a.confirm_hub_id)
        print(json.dumps(result,indent=2));return 0
    except Exception:
        # Do not put database details, passwords or key bytes into hosted logs.
        print('Operation refused or failed. No deployment was performed. Check identities, permissions, versions and the recovery runbook; do not delete project locks or overwrite data.',file=sys.stderr)
        return 2

PINNED_MANIFEST_SHA256 = '5224e380a19546a91c80f4c69f0cf5b3c6b7e7e8075fb3952f7123d08488cfce'
if __name__=='__main__':raise SystemExit(main())
