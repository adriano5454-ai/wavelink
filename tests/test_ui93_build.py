"""Pinned UI92 -> UI93 build, independent of project data and mail credentials."""
import hashlib,importlib.util,json,os,shutil
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ui93build',ROOT/'deploy/apply_ui93.py');overlay=importlib.util.module_from_spec(spec);spec.loader.exec_module(overlay)
BASE=Path(os.environ['WAVELINK_UI92_TEST_SOURCE']) if os.environ.get('WAVELINK_UI92_TEST_SOURCE') else None
CANDIDATE=Path(os.environ.get('WAVELINK_UI93_TEST_SOURCE',os.environ['WAVELINK_TEST_SOURCE']))

@pytest.fixture
def baseline_source():
    if BASE is None:
        pytest.skip('Set WAVELINK_UI92_TEST_SOURCE to the unchanged extracted UI92 runtime for replay checks.')
    return BASE

def test_docker_applies_ui93_exactly_once_and_copies_runner():
    source=(ROOT/'Dockerfile').read_text()
    assert source.count('&& python apply_ui93.py /opt/wavelink/app')==1
    copy=next(line for line in source.splitlines() if line.startswith('COPY deploy/extract_source.py'))
    assert 'deploy/apply_ui93.py' in copy
    assert source.index('python extract_source.py')<source.index('&& python apply_ui93.py')

def test_overlay_replay_is_byte_identical_and_rejects_double_apply(tmp_path,baseline_source):
    shutil.copytree(baseline_source,tmp_path/'runtime');path=tmp_path/'runtime';overlay.apply(path)
    expected=json.loads((CANDIDATE/'RELEASE_FILES.json').read_text())
    assert (path/'RELEASE_FILES.json').read_bytes()==(CANDIDATE/'RELEASE_FILES.json').read_bytes()
    for name,digest in expected['files'].items():assert hashlib.sha256((path/name).read_bytes()).hexdigest()==digest,name
    before=(path/'RELEASE_FILES.json').read_bytes()
    with pytest.raises(ValueError,match='exact UI92'):overlay.apply(path)
    assert (path/'RELEASE_FILES.json').read_bytes()==before

def test_tampered_parent_is_rejected_before_any_overlay_writes(tmp_path,baseline_source):
    shutil.copytree(baseline_source,tmp_path/'runtime');path=tmp_path/'runtime'
    (path/'app/server.py').write_text('tampered fictional source')
    before=(path/'RELEASE_FILES.json').read_bytes()
    with pytest.raises(ValueError,match='parent resource'):overlay.apply(path)
    assert (path/'RELEASE_FILES.json').read_bytes()==before
    assert not (path/'app/email_alerts.py').exists()
