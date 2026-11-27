"""Exercise the real project-transfer archive on disposable fictional data."""
from contextlib import closing
import sqlite3
import uuid

import pytest

from app import company_roles, departments, membership_policy, org_positions
from app.export_policy import has_hr, require_backup
from app.hub_manager import HubManager
from app.project_modules import describe, export_workspaces, import_workspaces, preview_import, prune_snapshot
from app.project_transfer import inspect_project
from app.store import Problem
from tests.test_hr_backup_ui117 import PASSWORD, company


def seed_chart(manager, admin, supervisor):
    head, child = str(uuid.uuid4()), str(uuid.uuid4())
    with manager.store.connection(True) as c:
        from app.hr import ensure
        ensure(c)
        org_positions.schema(c)
        company_roles.seed(c)
        department = departments._new(c, 'Fictional chart export department', '', admin)
        if isinstance(department, dict):
            department = department['id']
        role = c.execute("SELECT id FROM company_role_presets WHERE role_key='administrator'").fetchone()[0]
        c.execute('INSERT INTO hr_org_positions VALUES(?,?,?,?,?,1)', (head, department, role, None, admin['user_id']))
        c.execute('INSERT INTO hr_org_positions VALUES(?,?,?,?,?,1)', (child, department, role, head, supervisor['user_id']))
        for pos, parent, who in ((head, None, admin['user_id']), (child, head, supervisor['user_id'])):
            membership_policy.audit(c, admin['user_id'], pos, 'org_position_saved', dict(parent=parent,person=who))
        membership_policy.audit(c, admin['user_id'], admin['user_id'], 'fictional_core_audit', {'marker':'normal membership history'})
    return head, child


def contents(c):
    return (
        [tuple(r) for r in c.execute('SELECT * FROM hr_org_positions ORDER BY id')],
        [tuple(r) for r in c.execute("SELECT target_id,detail FROM company_access_audit WHERE action='org_position_saved' ORDER BY target_id")],
    )


@pytest.mark.parametrize('mode', ['without', 'with', 'complete'])
def test_org_transfer_round_trip(company, tmp_path, mode):
    manager, token, creator, supervisor_token, viewer = company
    head, child = seed_chart(manager, creator, viewer)
    with manager.store.connection() as c:
        expected = contents(c)
        assert describe(c)['known_tables'] and has_hr(c)
    with pytest.raises(Problem) as non_admin:
        require_backup(manager.store, viewer)
    assert non_admin.value.code == 403
    with pytest.raises(Problem) as select_non_admin:
        export_workspaces(manager, supervisor_token, tmp_path/'denied.ajproject', ['toolbox'])
    assert select_non_admin.value.code == 403
    package = tmp_path/'chart.ajproject'
    complete = mode=='complete'
    export_workspaces(manager, token, package, None if complete else ['toolbox'] if mode=='without' else ['hr'], complete=complete)
    preview = preview_import(package)
    selected = preview['manifest']['selected_modules']
    assert ('hr' in selected) == (mode!='without')
    _, files = inspect_project(package)
    (_, hr) = (preview['summary']['known_tables'], next(x for x in preview['summary']['modules'] if x['key']=='hr'))
    assert preview['summary']['known_tables'] and hr['counts']['hr_org_positions']==(0 if mode=='without' else 2)
    if mode=='without':
        for secret in (head, child):
            assert secret.encode() not in files['database.sqlite3']
    target=tmp_path/'fictional-restored'
    import_workspaces(package,target,'Fictional chart restored',complete=True,expected_hash=preview['file_hash'])
    restored=HubManager(target)
    _, actor=restored.accounts.login('backup.admin',PASSWORD,'fictional-restored-chart-admin')
    assert actor['role']=='admin' and restored.config['hub_id']!=manager.config['hub_id']
    with restored.store.connection() as c:
        assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        assert not c.execute('PRAGMA foreign_key_check').fetchall()
        assert contents(c) == (expected if mode!='without' else ([],[]))
        assert c.execute("SELECT count(*) FROM company_access_audit WHERE action='fictional_core_audit'").fetchone()[0]==1
        if mode!='without':
            assert has_hr(c)
        assert c.execute('SELECT parent FROM hr_org_positions WHERE id=?',(child,)).fetchone() is None if mode=='without' else (
            c.execute('SELECT parent FROM hr_org_positions WHERE id=?',(child,)).fetchone()[0]==head)
    with manager.store.connection() as c:
        assert contents(c)==expected


def test_unknown_org_schema_fails_before_editing_copy(company,tmp_path):
    manager, _, admin, _, supervisor = company
    seed_chart(manager,admin,supervisor)
    p=tmp_path/'fictional-future.sqlite3'
    manager.store.backup(p)
    with closing(sqlite3.connect(p)) as c:
        c.execute('ALTER TABLE hr_org_positions ADD COLUMN future TEXT')
        c.commit()
    before=p.read_bytes()
    with pytest.raises(Problem) as denied:
        prune_snapshot(p,['toolbox'])
    assert denied.value.code==409 and p.read_bytes()==before


def test_audit_alone_remains_private(company):
    manager, _, admin, _, supervisor = company
    _, child=seed_chart(manager,admin,supervisor)
    with manager.store.connection(True) as c:
        c.execute('UPDATE hr_org_positions SET parent=NULL WHERE id=?',(child,))
        c.execute('DELETE FROM hr_org_positions')
        assert has_hr(c)
    with pytest.raises(Problem) as denied:
        require_backup(manager.store,supervisor)
    assert denied.value.code==403
