from pathlib import Path
import json
import hashlib
import os
import sys
import pytest
from deploy.extract_source import extract_parts, SOURCE_SHA256
from deploy.nginx_config import render

ROOT=Path(__file__).resolve().parents[1]
SOURCE_ROOT=Path(os.environ.get('WAVELINK_TEST_SOURCE','')).resolve()
if SOURCE_ROOT.is_dir() and str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0,str(SOURCE_ROOT))

def test_reassembled_source_is_exact(tmp_path):
    count=extract_parts(ROOT/'vendor/source_parts.json',tmp_path/'source')
    assert count==1605
    source=Path(os.environ['WAVELINK_TEST_SOURCE'])
    manifest=json.loads((source/'RELEASE_FILES.json').read_text())
    assert all((tmp_path/'source'/name).read_bytes()==(source/name).read_bytes() for name in manifest['files'])

def test_parts_are_small_and_hash_checked():
    manifest=json.loads((ROOT/'vendor/source_parts.json').read_text())
    assert len(manifest['parts'])==5 and manifest['archive_sha256']==SOURCE_SHA256
    assert all(p['bytes']<=8*1024*1024 for p in manifest['parts'])

def test_presentation_rules_only_apply_to_application_script(tmp_path):
    cfg=render('demo.example.test',19085,tmp_path/'nginx')
    scripted=cfg.split('location = /static/app.js {',1)[1].split('\n        }',1)[0]
    general=cfg.rsplit('location / {',1)[1]
    assert 'sub_filter ' in scripted
    assert 'sub_filter ' not in general
    assert 'auth_request /_demo_verify' in scripted

def test_forwarded_headers_whitelisted(tmp_path):
    cfg=render('demo.example.test',19085,tmp_path/'nginx')
    assert 'proxy_pass_request_headers off' in cfg
    assert 'proxy_set_header Authorization $http_authorization' in cfg
    assert 'proxy_set_header X-AJ-Hub-ID $http_x_aj_hub_id' in cfg
    assert 'proxy_set_header X-Forwarded-For $remote_addr' in cfg

@pytest.mark.parametrize('bad',['demo.example;bad','demo.example\nother','demo.example/abc','*.example.test'])
def test_gateway_authority_injection_refused(tmp_path,bad):
    with pytest.raises(ValueError):render(bad,19085,tmp_path/'nginx')

def test_no_real_project_or_secret_files_packaged():
    names=[p.name for p in ROOT.rglob('*') if p.is_file()]
    assert 'dives.sqlite3' not in names and 'hub.json' not in names and 'gate.key' not in names


def test_ui90_overlay_navigation_theme_and_m01_launcher_are_exact():
    from deploy.extract_source import (
        UI_PATCH_ID,
        UI66_PATCH_ID,
        UI67_PATCH_ID,
        UI68_PATCH_ID,
        UI69_PATCH_ID,
        UI70_PATCH_ID,
        UI71_PATCH_ID,
        UI72_PATCH_ID,
        UI73_PATCH_ID,
        UI74_PATCH_ID,
        UI75_PATCH_ID,
        UI76_PATCH_ID,
        UI77_PATCH_ID,
        UI78_PATCH_ID,
        UI79_PATCH_ID,
        UI80_PATCH_ID,
        UI81_PATCH_ID,
        UI82_PATCH_ID,
        UI83_PATCH_ID,
        UI84_PATCH_ID,
        UI85_PATCH_ID,
        UI86_PATCH_ID,
        UI87_PATCH_ID,
        UI88_PATCH_ID,
        UI89_PATCH_ID,
        UI90_PATCH_ID,
        _UI66_FILES,
        _UI67_FILES,
        _UI68_FILES,
        _UI69_FILES,
        _UI70_FILES,
        _UI71_FILES,
        _UI72_FILES,
        _UI73_FILES,
        _UI74_FILES,
        _UI75_FILES,
        _UI76_FILES,
        _UI77_FILES,
        _UI78_FILES,
        _UI79_FILES,
        _UI80_FILES,
        _UI81_FILES,
        _UI82_FILES,
        _UI83_FILES,
        _UI84_FILES,
        _UI85_FILES,
        _UI86_FILES,
        _UI87_FILES,
        _UI88_FILES,
        _UI89_FILES,
        _UI90_FILES,
    )
    assert UI_PATCH_ID == 'workspace-ui65-role-ready-invitations-2026-09-29'
    assert UI66_PATCH_ID == 'workspace-ui66-profiles-recognition-2026-09-29'
    assert UI67_PATCH_ID == 'workspace-ui67-experience-foundation-2026-09-30'
    assert UI68_PATCH_ID == 'workspace-ui68-data-grounded-home-profile-2026-09-30'
    assert UI69_PATCH_ID == 'workspace-ui69-work-execution-experience-2026-09-30'
    assert UI70_PATCH_ID == 'workspace-ui70-equipment-logistics-experience-2026-09-30'
    assert UI71_PATCH_ID == 'workspace-ui71-single-gui-cutover-2026-09-30'
    assert UI72_PATCH_ID == 'workspace-ui72-native-workspaces-cutover-2026-09-30'
    assert UI73_PATCH_ID == 'workspace-ui73-integrated-shell-context-2026-09-30'
    assert UI74_PATCH_ID == 'workspace-ui74-gui-recovery-baseline-2026-09-30'
    assert UI75_PATCH_ID == 'workspace-ui75-native-administration-2026-09-30'
    assert UI76_PATCH_ID == 'workspace-ui76-native-operational-records-2026-09-30'
    assert UI77_PATCH_ID == 'workspace-ui77-native-fleet-vessel-logs-2026-09-30'
    assert UI78_PATCH_ID == 'workspace-ui78-native-fleet-logistics-2026-09-30'
    assert UI79_PATCH_ID == 'workspace-ui79-native-equipment-records-2026-10-01'
    assert UI80_PATCH_ID == 'workspace-ui80-native-work-execution-2026-10-01'
    assert UI81_PATCH_ID == 'workspace-ui81-workflow-foundation-batch-2026-10-01'
    assert UI82_PATCH_ID == 'workspace-ui82-authorised-search-action-centre-batch-2026-10-01'
    assert UI83_PATCH_ID == 'workspace-ui83-account-security-sessions-batch-2026-10-01'
    assert UI84_PATCH_ID == 'workspace-ui84-company-workspace-identity-native-originals-2026-10-01'
    assert UI85_PATCH_ID == 'workspace-ui85-authentic-contribution-badges-2026-10-01'
    assert UI86_PATCH_ID == 'workspace-ui86-authentic-visual-branding-boundaries-2026-10-01'
    assert UI87_PATCH_ID == 'workspace-ui87-visual-reconciliation-2026-10-01'
    assert UI88_PATCH_ID == 'workspace-ui88-mobile-first-visual-hardening-2026-10-02'
    assert UI89_PATCH_ID == 'workspace-ui89-core-visual-system-refinement-2026-10-02'
    assert UI90_PATCH_ID == 'workspace-ui90-navigation-theme-parity-2026-10-02'
    assert len(_UI66_FILES) == 33
    assert len(_UI67_FILES) == 41
    assert len(_UI68_FILES) == 11
    assert len(_UI69_FILES) == 9
    assert len(_UI70_FILES) == 8
    assert len(_UI71_FILES) == 11
    assert len(_UI72_FILES) == 12
    assert len(_UI73_FILES) == 12
    assert len(_UI74_FILES) == 9
    assert len(_UI75_FILES) == 12
    assert len(_UI76_FILES) == 12
    assert len(_UI77_FILES) == 7
    assert len(_UI78_FILES) == 7
    assert len(_UI79_FILES) == 10
    assert len(_UI80_FILES) == 12
    assert len(_UI81_FILES) == 15
    assert len(_UI82_FILES) == 13
    assert len(_UI83_FILES) == 14
    assert len(_UI84_FILES) == 50
    assert len(_UI85_FILES) == 39
    assert len(_UI86_FILES) == 21
    assert len(_UI87_FILES) == 13
    assert len(_UI88_FILES) == 8
    assert len(_UI89_FILES) == 6
    assert len(_UI90_FILES) == 8
    assert len([name for name in _UI85_FILES if name.startswith('app/static/badges/')]) == 30
    assert len([name for name in _UI67_FILES if name.startswith('app/static/badges/')]) == 30
    assert hashlib.sha256((ROOT/'deploy/company_entrypoint.py').read_bytes()).hexdigest() == '2f117d85c439c16ab78908bf5728056cc837e5d1f948a77040ef1d509c04c371'
    assert (ROOT/'docs/WORKSPACE_UI65.md').is_file()
    assert (ROOT/'docs/UI65_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI66.md').is_file()
    assert (ROOT/'docs/UI66_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI67.md').is_file()
    assert (ROOT/'docs/UI67_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI68.md').is_file()
    assert (ROOT/'docs/UI68_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI69.md').is_file()
    assert (ROOT/'docs/UI69_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI70.md').is_file()
    assert (ROOT/'docs/UI70_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI71.md').is_file()
    assert (ROOT/'docs/UI71_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI72.md').is_file()
    assert (ROOT/'docs/UI72_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI73.md').is_file()
    assert (ROOT/'docs/UI73_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI74.md').is_file()
    assert (ROOT/'docs/UI74_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI75.md').is_file()
    assert (ROOT/'docs/UI75_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI76.md').is_file()
    assert (ROOT/'docs/UI76_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI77.md').is_file()
    assert (ROOT/'docs/UI77_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI78.md').is_file()
    assert (ROOT/'docs/UI78_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI79.md').is_file()
    assert (ROOT/'docs/UI79_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI80.md').is_file()
    assert (ROOT/'docs/UI80_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI81.md').is_file()
    assert (ROOT/'docs/UI81_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI82.md').is_file()
    assert (ROOT/'docs/UI82_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI83.md').is_file()
    assert (ROOT/'docs/UI83_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI84.md').is_file()
    assert (ROOT/'docs/UI84_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI85.md').is_file()
    assert (ROOT/'docs/UI85_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI86.md').is_file()
    assert (ROOT/'docs/UI86_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI87.md').is_file()
    assert (ROOT/'docs/UI87_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI88.md').is_file()
    assert (ROOT/'docs/UI88_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI89.md').is_file()
    assert (ROOT/'docs/UI89_SOURCE_PROVENANCE.json').is_file()
    assert (ROOT/'docs/WORKSPACE_UI90.md').is_file()
    assert (ROOT/'docs/UI90_SOURCE_PROVENANCE.json').is_file()



def test_ui84_sulmara_company_identity_is_code_owned_and_valid(tmp_path):
    from PIL import Image
    from app.deployment_branding import read_identity
    from deploy.company_provision import validate_company_branding
    from deploy.provision import DemoError
    source=Path(os.environ['WAVELINK_TEST_SOURCE'])

    descriptor=json.loads((ROOT/'deploy/company_identities.json').read_text())
    assert descriptor == {'sulmara': {'name': 'Sulmara', 'logo': 'logo.png'}}
    logo=ROOT/'deploy/company_logos/sulmara/logo.png'
    assert logo.is_file() and 0 < logo.stat().st_size <= 2_000_000
    with Image.open(logo) as image:
        assert image.format == 'PNG' and image.width == 1496 and image.height == 412
        assert getattr(image, 'n_frames', 1) == 1
    env={'WAVELINK_DEPLOYMENT_MODE':'COMPANY','COMPANY_ID':'sulmara','COMPANY_NAME':'Sulmara'}
    identity, asset=read_identity(env, ROOT/'deploy')
    assert identity['logo_status'] == 'ready' and identity['name'] == 'Sulmara'
    assert identity['logo_url'].startswith('/static/company-identity/logo?v=')
    assert asset['content'] == logo.read_bytes() and asset['mime'] == 'image/png'
    assert validate_company_branding(source, env, deploy_root=ROOT/'deploy') == identity

    empty=tmp_path/'deploy'; (empty/'company_logos').mkdir(parents=True)
    (empty/'company_identities.json').write_text('{}\n')
    with pytest.raises(DemoError, match='not configured|valid company logo'):
        validate_company_branding(source, env, deploy_root=empty)


def test_ui84_keeps_operational_project_job_fields_and_native_originals():
    source=Path(os.environ['WAVELINK_TEST_SOURCE'])
    app=(source/'app/static/app.js').read_text()
    originals=(source/'app/static/original_library.js').read_text()
    assert 'Project / job' in app  # operational reference remains valid
    assert "location.hash='#original-files'" in originals
    assert 'showModal(' not in originals
    assert 'Current project' not in (source/'app/static/index.html').read_text()


def test_ui85_badge_assets_keep_stable_ids_and_cosmetic_boundaries():
    from PIL import Image
    from app.recognition import BADGE_CATALOG, TIERS, badges_for
    source=Path(os.environ['WAVELINK_TEST_SOURCE'])
    paths=sorted((source/'app/static/badges').glob('*.webp'))
    expected={f'{tier}-{family}' for tier, _label, _threshold in TIERS
              for family in ('compass','survey-wave','sonar')}
    assert {path.stem for path in paths} == expected
    assert set(BADGE_CATALOG) == expected
    assert len({BADGE_CATALOG[key][0] for key in BADGE_CATALOG}) == 30
    assert len(paths) == 30
    for path in paths:
        with Image.open(path) as image:
            assert image.format == 'WEBP' and image.size == (300,300)
            assert image.convert('RGBA').getchannel('A').getextrema() == (0,255)
    badges=badges_for(1000)
    assert len(badges) == 30 and all(row['unlocked'] for row in badges)
    patch=json.loads((source/'UI_PATCH.json').read_text())
    ui85=json.loads((ROOT/'docs/UI85_SOURCE_PROVENANCE.json').read_text())
    assert patch['patch_id'] == 'workspace-ui90-navigation-theme-parity-2026-10-02'
    assert patch['parent_patch_id'] == 'workspace-ui89-core-visual-system-refinement-2026-10-02'
    assert patch['boundaries']['recognition_rule_change'] is False
    assert ui85['boundaries']['badge_id_change'] is False
    assert ui85['boundaries']['recognition_scoring_change'] is False



def test_ui86_visual_art_and_report_branding_boundaries_are_explicit():
    source=Path(os.environ['WAVELINK_TEST_SOURCE'])
    patch=json.loads((source/'UI_PATCH.json').read_text())
    assert patch['patch_id'] == 'workspace-ui90-navigation-theme-parity-2026-10-02'
    assert patch['parent_patch_id'] == 'workspace-ui89-core-visual-system-refinement-2026-10-02'
    assert patch['boundaries']['report_branding_changes_app_identity'] is False
    ui86=json.loads((ROOT/'docs/UI86_SOURCE_PROVENANCE.json').read_text())
    assert ui86['localisation_roadmap']['implemented'] is False
    assert (source/'app/static/wavelink-home-cover-ui86.svg').is_file()
    assert (source/'app/static/wavelink-profile-cover-ui86.svg').is_file()
    index=(source/'app/static/index.html').read_text()
    assert 'visual_system_ui90.css?v=1.34.19-ui90' in index
    assert 'visual_refresh_ui86.css' not in index
    assert 'visual_reconciliation_ui87.css' not in index
    assert 'mobile_foundation_ui88.css' not in index
    assert 'pxgeo-dive-check-shell-1.34.19-ui90' in (source/'app/static/sw.js').read_text()
    deployment=(source/'app/static/deployment_branding.js').read_text()
    report=(source/'app/static/company_branding.js').read_text()
    assert '/api/admin/company-branding' not in deployment
    assert 'Reports and exports only' in report
    assert 'never alter the application header' in report
    visual=(source/'app/static/visual_system_ui90.css').read_text()
    assert 'wavelink-approved-offshore-ui87.webp' in visual
    assert 'wavelink-approved-offshore-profile-ui87.webp' in visual


def test_ui65_release_keeps_operator_secret_examples_blank():
    values = {}
    for line in (ROOT/'deploy/membership.env.example').read_text().splitlines():
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            values[key] = value
    assert values.get('MEMBERSHIP_SMTP_PASSWORD') == ''
    assert not any((ROOT/name).exists() for name in ('hub.json','gate.key','.env','secrets.json'))
