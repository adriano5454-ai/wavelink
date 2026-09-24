"""Extract only the reviewed, pinned upstream archive at image build time."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import sys
import tempfile
import zipfile

SOURCE_SHA256 = '8c1b6a8d731d01b05a1290d3a1dd1a544054147aac9048ca345af7983613cd9e'
ROOT = 'Wavelink_1.34.19'

def extract(archive: Path, destination: Path) -> int:
    if hashlib.sha256(archive.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError('Source archive checksum mismatch. Do not deploy.')
    if destination.exists() and any(destination.iterdir()):
        raise ValueError('Source destination is not empty.')
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        seen = set()
        for info in z.infolist():
            parts = PurePosixPath(info.filename).parts
            if (not parts or parts[0] != ROOT or '..' in parts or '\\' in info.filename
                    or info.filename in seen or ((info.external_attr >> 16) & 0o170000) == 0o120000):
                raise ValueError('Unexpected source archive member.')
            seen.add(info.filename)
            if len(parts) == 1 or info.is_dir():
                continue
            target = destination.joinpath(*parts[1:])
            target.parent.mkdir(parents=True, exist_ok=True)
            with z.open(info) as src, target.open('wb') as dst:
                shutil.copyfileobj(src, dst)
    manifest = json.loads((destination / 'RELEASE_FILES.json').read_text())
    for name, expected in manifest['files'].items():
        if hashlib.sha256((destination / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Extracted source integrity failure.')
    return len(manifest['files'])

def extract_parts(manifest_path: Path, destination: Path) -> int:
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('format') != 'wavelink-source-parts-1' or manifest.get('archive_sha256') != SOURCE_SHA256:
        raise ValueError('Unexpected source-parts manifest.')
    expected_names = [f'source.part{i:03d}' for i in range(1, len(manifest['parts']) + 1)]
    if [p['name'] for p in manifest['parts']] != expected_names:
        raise ValueError('Missing, duplicate or unsafe source part.')
    with tempfile.TemporaryDirectory(prefix='wavelink-source-build-') as td:
        joined = Path(td) / 'source.zip'
        with joined.open('wb') as output:
            for part in manifest['parts']:
                data = (manifest_path.parent / part['name']).read_bytes()
                if len(data) != part['bytes'] or hashlib.sha256(data).hexdigest() != part['sha256']:
                    raise ValueError('Source part integrity failure.')
                output.write(data)
        return extract(joined, destination)


if __name__ == '__main__':
    incoming = Path(sys.argv[1])
    count = (extract_parts if incoming.name == 'source_parts.json' else extract)(incoming, Path(sys.argv[2]))
    print(f'Verified upstream 1.34.19: {count} tracked files.')
