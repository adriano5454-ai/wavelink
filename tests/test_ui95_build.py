"""Exact UI94 -> UI95 overlay, cumulative build and reject-before-write checks."""
import hashlib,importlib.util,json,os,shutil
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'deploy'/f'apply_{name}.py');out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out);return out
UI93,UI94,UI95=[module(n) for n in ('ui93','ui94','ui95')]
SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE']);BASE=Path(os.environ['WAVELINK_UI94_TEST_SOURCE'])
def identical(path):
    assert (path/'RELEASE_FILES.json').read_bytes()==(SOURCE/'RELEASE_FILES.json').read_bytes()
    for name,digest in json.loads((SOURCE/'RELEASE_FILES.json').read_text())['files'].items():assert hashlib.sha256((path/name).read_bytes()).hexdigest()==digest,name

def test_exact_ui94_replay_and_double_apply_rejected(tmp_path):
    p=tmp_path/'runtime';shutil.copytree(BASE,p);UI95.apply(p);identical(p);before=(p/'RELEASE_FILES.json').read_bytes()
    with pytest.raises(ValueError,match='exact UI94'):UI95.apply(p)
    assert (p/'RELEASE_FILES.json').read_bytes()==before

def test_tampered_parent_rejected_before_any_writes(tmp_path):
    p=tmp_path/'runtime';shutil.copytree(BASE,p);(p/'app/static/fieldwork.js').write_text('tampered');before=(p/'RELEASE_FILES.json').read_bytes()
    with pytest.raises(ValueError,match='parent resource'):UI95.apply(p)
    assert (p/'RELEASE_FILES.json').read_bytes()==before;assert not (p/'app/document_import.py').exists()

def test_cumulative_ui92_build_and_email_art_preserved(tmp_path):
    p=tmp_path/'runtime';shutil.copytree(Path(os.environ['WAVELINK_UI92_TEST_SOURCE']),p);UI93.apply(p);UI94.apply(p);UI95.apply(p);identical(p)
    for n in ['app/email_alerts.py','app/email_alerts_api.py','app/static/visual_system_ui94.css','app/static/experience_shell.js','app/static/wavelink-approved-offshore-ui87.webp']:
        assert (p/n).read_bytes()==(BASE/n).read_bytes()

def test_docker_order_once_and_passive_parser_dependencies():
    s=(ROOT/'Dockerfile').read_text();last=s.index('python extract_source.py')
    for name in ('ui93','ui94','ui95'):
        term='&& python apply_'+name+'.py /opt/wavelink/app';assert s.count(term)==1;index=s.index(term);assert index>last;last=index
    for name in ('poppler-utils','tesseract-ocr','tesseract-ocr-por'):assert name in s
    assert 'pypdf==6.19.0' in (ROOT/'requirements.lock').read_text()
