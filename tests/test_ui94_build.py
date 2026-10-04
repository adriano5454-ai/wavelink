"""UI94 overlay replay and cumulative UI92 -> UI93 -> UI94 build checks."""
import hashlib,importlib.util,json,os,shutil
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'deploy'/f'apply_{name}.py')
    value=importlib.util.module_from_spec(spec);spec.loader.exec_module(value);return value
UI93=module('ui93');UI94=module('ui94')
CANDIDATE=Path(os.environ.get('WAVELINK_UI94_TEST_SOURCE',os.environ['WAVELINK_TEST_SOURCE']))

@pytest.fixture
def sources():
    if not os.environ.get('WAVELINK_UI93_TEST_SOURCE') or not os.environ.get('WAVELINK_UI92_TEST_SOURCE'):
        pytest.skip('Set exact UI92 and UI93 parent runtime directories to verify cumulative replay.')
    return Path(os.environ['WAVELINK_UI92_TEST_SOURCE']),Path(os.environ['WAVELINK_UI93_TEST_SOURCE'])

def identical(path):
    assert (path/'RELEASE_FILES.json').read_bytes()==(CANDIDATE/'RELEASE_FILES.json').read_bytes()
    for name,digest in json.loads((CANDIDATE/'RELEASE_FILES.json').read_text())['files'].items():
        assert hashlib.sha256((path/name).read_bytes()).hexdigest()==digest,name

def test_docker_copies_both_companions_and_runs_each_once_in_order():
    text=(ROOT/'Dockerfile').read_text()
    assert text.count('&& python apply_ui93.py /opt/wavelink/app')==1
    assert text.count('&& python apply_ui94.py /opt/wavelink/app')==1
    assert text.index('python extract_source.py')<text.index('python apply_ui93.py')<text.index('python apply_ui94.py')
    copy=next(line for line in text.splitlines() if line.startswith('COPY deploy/extract_source.py'))
    assert 'deploy/apply_ui93.py' in copy and 'deploy/apply_ui94.py' in copy

def test_ui93_replay_matches_final_runtime_and_double_apply_is_rejected(tmp_path,sources):
    shutil.copytree(sources[1],tmp_path/'runtime');path=tmp_path/'runtime';UI94.apply(path);identical(path)
    before=(path/'RELEASE_FILES.json').read_bytes()
    with pytest.raises(ValueError,match='exact UI93'):UI94.apply(path)
    assert (path/'RELEASE_FILES.json').read_bytes()==before

def test_tampered_ui93_is_rejected_before_any_writes(tmp_path,sources):
    shutil.copytree(sources[1],tmp_path/'runtime');path=tmp_path/'runtime'
    (path/'app/static/index.html').write_text('tampered fictional shell')
    before=(path/'RELEASE_FILES.json').read_bytes()
    with pytest.raises(ValueError,match='parent resource'):UI94.apply(path)
    assert (path/'RELEASE_FILES.json').read_bytes()==before
    assert not (path/'app/static/visual_system_ui94.css').exists()

def test_ui92_cumulative_replay_retains_email_and_matches_final_runtime(tmp_path,sources):
    shutil.copytree(sources[0],tmp_path/'runtime');path=tmp_path/'runtime'
    UI93.apply(path);UI94.apply(path);identical(path)
    assert (path/'app/email_alerts.py').read_bytes()==(sources[1]/'app/email_alerts.py').read_bytes()
    assert (path/'app/email_alerts_api.py').read_bytes()==(sources[1]/'app/email_alerts_api.py').read_bytes()
