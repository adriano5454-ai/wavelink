"""Materialize the complete application from the bundled, verified release chain."""
from pathlib import Path
import hashlib,json,runpy,sys
ROOT=Path(__file__).resolve().parents[1]
STAGES=[93,94,95,96,97,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123]

def main(destination):
    dest=Path(destination).absolute()
    if dest.exists() or dest.is_symlink(): raise SystemExit('Use a new destination; existing files will not be overwritten.')
    original=Path.write_text
    # Earlier verified builders were authored on Linux. Preserve their exact LF
    # bytes when materializing on Windows as well, without changing the overlays.
    def write_lf(self,data,encoding=None,errors=None,newline=None):
        return original(self,data,encoding=encoding or 'utf-8',errors=errors,newline='\n')
    Path.write_text=write_lf
    try:
        sys.argv=['extract_source.py',str(ROOT/'vendor/source_parts.json'),str(dest)]
        runpy.run_path(str(ROOT/'deploy/extract_source.py'),run_name='__main__')
        for stage in STAGES:
            sys.argv=['apply_ui'+str(stage)+'.py',str(dest)]
            runpy.run_path(str(ROOT/'deploy'/sys.argv[0]),run_name='__main__')
        manifest=json.loads((dest/'RELEASE_FILES.json').read_bytes())
        for name,digest in manifest['files'].items():
            if hashlib.sha256((dest/name).read_bytes()).hexdigest()!=digest: raise ValueError('Resource mismatch: '+name)
        print(json.dumps({'variant':manifest['variant'],'resources':len(manifest['files']),'manifest_sha256':hashlib.sha256((dest/'RELEASE_FILES.json').read_bytes()).hexdigest()}))
    finally: Path.write_text=original

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: python deploy/materialize_runtime.py NEW_DIRECTORY')
    main(sys.argv[1])
