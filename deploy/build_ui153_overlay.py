"""Freeze the reviewed UI153 runtime into a deterministic, fail-closed overlay.

Usage: python deploy/build_ui153_overlay.py VERIFIED_UI152 RUNTIME_UI153
No production data or remote resources are read or modified.
"""
from pathlib import Path
import base64
import hashlib
import json
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
PARENT = '6e79d684b8771ffe09055aef158e695ce0475430b477c26448b241983043d351'
VARIANT = 'workspace-ui153-role-catalogue-hotfix-2026-11-18'
SHA = lambda data: hashlib.sha256(data).hexdigest()

def freeze(parent: Path, target: Path):
    raw = (parent/'RELEASE_FILES.json').read_bytes()
    if SHA(raw) != PARENT:
        raise ValueError('Requires the verified UI152 runtime.')
    baseline = json.loads(raw)
    for name, digest in baseline['files'].items():
        if SHA((parent/name).read_bytes()) != digest:
            raise ValueError('Modified UI152 parent: '+name)
        if not (target/name).is_file():
            raise ValueError('A retained resource is missing: '+name)
    names = set(baseline['files']) | {'docs/WORKSPACE_UI153.md', 'tests/ui65_roles_access/test_catalogue_upgrade_ui153.py'}
    metadata = dict(format='wavelink-runtime-overlay-1',date='2026-11-18',patch_id=VARIANT,
                    parent_patch_id=baseline.get('variant'),parent_manifest_sha256=PARENT,
                    scope='Restore the invitation screen when a company has saved administrator profiles from earlier permission catalogues, retaining their exact recorded authority.',
                    boundaries=dict(database_reset=False, data_schema_changed=False, external_ai_behavior_changed=False, email_behavior_changed=False))
    (target/'UI_PATCH.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8',newline='\n')
    derived = dict(baseline)
    derived['variant'] = VARIANT
    derived['files'] = {}
    files = {}
    for name in sorted(names):
        data = (target/name).read_bytes()
        digest = SHA(data)
        derived['files'][name] = digest
        before = baseline['files'].get(name)
        if before != digest:
            files[name] = dict(before=before, after=digest, bytes=len(data),
                               payload=base64.b64encode(zlib.compress(data,9)).decode())
    target_raw = (json.dumps(derived,indent=2)+'\n').encode()
    (target/'RELEASE_FILES.json').write_bytes(target_raw)
    template = '''"""Verified UI153 workspace update overlay."""
from pathlib import Path, PurePosixPath
import base64, hashlib, json, sys, zlib
PARENT_MANIFEST_SHA256 = PARENT_VALUE
TARGET_MANIFEST_SHA256 = TARGET_VALUE
TARGET_VARIANT = VARIANT_VALUE
FILES = FILES_VALUE

def apply(destination: Path):
    destination = Path(destination)
    if destination.is_symlink() or not destination.is_dir():
        raise ValueError('UI153 destination must be an existing directory without a root symlink.')
    destination = destination.resolve()
    manifest_path = destination/'RELEASE_FILES.json'
    if manifest_path.is_symlink() or not manifest_path.is_file():
        raise ValueError('UI153 manifest must be a regular file without a symlink.')

    def resource_path(name):
        relative = PurePosixPath(name)
        if relative.is_absolute() or not relative.parts or '..' in relative.parts or name!=relative.as_posix() or chr(92) in name:
            raise ValueError('Unsafe UI153 resource path.')
        path = destination.joinpath(*relative.parts)
        current = path
        while current != destination:
            if current.is_symlink():
                raise ValueError('Symlink in UI153 resource path: '+name)
            current = current.parent
        return path

    raw = manifest_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PARENT_MANIFEST_SHA256:
        raise ValueError('UI153 requires the exact UI152 manifest. Do not deploy.')
    manifest = json.loads(raw)
    for name,digest in manifest['files'].items():
        path = resource_path(name)
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError('UI153 parent resource mismatch: '+name)
    prepared = {}
    for name,record in FILES.items():
        path = resource_path(name)
        if record['before'] is None:
            if path.exists() or name in manifest['files']:
                raise ValueError('UI153 new resource already exists: '+name)
        elif manifest['files'].get(name)!=record['before']:
            raise ValueError('UI153 parent file mismatch: '+name)
        dec=zlib.decompressobj()
        data=dec.decompress(base64.b64decode(record['payload'],validate=True),record['bytes']+1)
        if dec.unconsumed_tail: raise ValueError('Oversized UI153 payload.')
        data+=dec.flush()
        if not dec.eof or dec.unused_data or len(data)!=record['bytes'] or hashlib.sha256(data).hexdigest()!=record['after']:
            raise ValueError('UI153 payload integrity failure: '+name)
        prepared[name]=data
    # Validate the complete target before the first mutation, including a bad
    # target digest or internally inconsistent generated overlay metadata.
    composed = dict(manifest)
    composed['files'] = dict(manifest['files'])
    for name in prepared:
        composed['files'][name] = FILES[name]['after']
    composed['files'] = dict(sorted(composed['files'].items()))
    composed['variant'] = TARGET_VARIANT
    result=(json.dumps(composed,indent=2)+'\\n').encode()
    if hashlib.sha256(result).hexdigest()!=TARGET_MANIFEST_SHA256:
        raise ValueError('UI153 manifest composition mismatch.')
    for name,data in prepared.items():
        path=resource_path(name)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
    manifest_path.write_bytes(result)
    manifest = composed
    for name,digest in manifest['files'].items():
        if hashlib.sha256((destination/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Derived UI153 resource mismatch: '+name)

if __name__=='__main__':
    apply(Path(sys.argv[1]))
    print('Applied Workspace UI153 update.')
'''
    script = template.replace('PARENT_VALUE',repr(PARENT)).replace('TARGET_VALUE',repr(SHA(target_raw))).replace('VARIANT_VALUE',repr(VARIANT)).replace('FILES_VALUE',repr(files))
    (ROOT/'deploy/apply_ui153.py').write_text(script,encoding='utf-8',newline='\n')
    provenance = dict(metadata,runtime_manifest_sha256=SHA(target_raw),runtime_resources=len(names),
                      overlay_resources=len(files),files=[dict(path=n,before_sha256=v['before'],after_sha256=v['after']) for n,v in files.items()])
    (ROOT/'docs/UI153_SOURCE_PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:provenance[k] for k in ['runtime_manifest_sha256','runtime_resources','overlay_resources']}))

if __name__=='__main__':
    freeze(Path(sys.argv[1]),Path(sys.argv[2]))
