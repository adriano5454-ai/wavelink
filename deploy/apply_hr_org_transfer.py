"""Keep organogram data and its audit inside the selected HR boundary."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
PARENT = '7be54d43230951033ad64565e5e7204e40dc8e49c68c5a62221bb06a1b52b497'

def once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected HR export anchor: '+repr(old))
    return source.replace(old, new, 1)

def modules(s):
    s = once(s, "    'hr': ('Private HR records and evidence',\n           'All staff documents, travel, shifts, timesheets, expenses, original evidence files, history and saved receipts; not filtered to the importing person',\n           ('hr_records', 'hr_files')),",
             "    'hr': ('Private HR records and evidence',\n           'Staff documents, travel, shifts, timesheets, expenses, original evidence, reporting positions and hierarchy history; not recipient-filtered',\n           ('hr_records', 'hr_files', 'hr_org_positions')),")
    s = once(s, 'HR_TABLES = LEGACY_HR_TABLES | HR_PROJECT_TABLES',
             "HR_ORG_TABLES = {'hr_org_positions'}  # Optional in older snapshots.\nHR_TABLES = LEGACY_HR_TABLES | HR_PROJECT_TABLES | HR_ORG_TABLES")
    s = once(s, '        # Never erase or re-label an unknown future fault format, even when',
             """        if 'hr_org_positions' in names:
            columns = {row['name'] for row in c.execute('PRAGMA table_info(hr_org_positions)')}
            refs = {(row['from'], row['table'], row['to'])
                    for row in c.execute('PRAGMA foreign_key_list(hr_org_positions)')}
            if (columns != {'id', 'department', 'role', 'parent', 'person', 'version'}
                    or refs != {('department', 'ops_departments', 'id'),
                                ('role', 'company_role_presets', 'id'),
                                ('parent', 'hr_org_positions', 'id'),
                                ('person', 'users', 'id')}):
                raise Problem(409, 'Unrecognised organisation chart schema. Use the matching application.')
        # Never erase or re-label an unknown future fault format, even when""")
    s = once(s, "        if 'hr' not in chosen and 'hr_meta' in names:",
             """        if 'hr' not in chosen and 'company_access_audit' in names:
            # This audit carries explicit position-to-person and reporting links.
            # Keep unrelated membership and permission history in the core copy.
            c.execute("DELETE FROM company_access_audit WHERE action='org_position_saved'")
        if 'hr' not in chosen and 'hr_meta' in names:""")
    s = once(s, 'timesheets, project approvers, expense receipts, history and saved operation receipts when selected',
             'timesheets, project approvers, expense receipts, reporting positions and their audit,\nother history and saved operation receipts when selected')
    s = once(s, 'despesas, comprovantes, históricos e recibos de operações quando selecionado',
             'despesas, comprovantes, cargos do organograma, relações de reporte e seu histórico, e recibos de operações quando selecionado')
    return s

def policy(s):
    s = once(s, 'travel, shifts, timesheets, expenses and receipts, including retained history.',
             'travel, shifts, timesheets, expenses, receipts and reporting positions, including retained history.')
    s = once(s, "    for name in names:\n        if not name.startswith('hr_'):",
             """    if 'company_access_audit' in names and c.execute(
            "SELECT 1 FROM company_access_audit WHERE action='org_position_saved' LIMIT 1").fetchone():
        return True
    for name in names:
        if not name.startswith('hr_'):""")
    return s

def tests(s):
    s = once(s, "            for table in sorted(HR_TABLES)}",
             "            for table in sorted(HR_TABLES) if c.execute('SELECT 1 FROM sqlite_master WHERE type=? AND name=?', ('table', table)).fetchone()}")
    s = once(s, "assert hr['counts'] == {'hr_records': 1, 'hr_files': 1}",
             "assert hr['counts'] == {'hr_records': 1, 'hr_files': 1, 'hr_org_positions': 0}")
    s = once(s, "                assert c.execute('SELECT count(*) FROM ' + table).fetchone()[0] == 0",
             "                if c.execute('SELECT 1 FROM sqlite_master WHERE type=? AND name=?', ('table', table)).fetchone():\n                    assert c.execute('SELECT count(*) FROM ' + table).fetchone()[0] == 0")
    s = once(s, "        ensure(c)\n    assert require_backup(manager.store, supervisor)['kind']",
             "        ensure(c)\n        c.execute(\"DELETE FROM hr_meta WHERE key='expiry_reminders_started_on'\")\n    assert require_backup(manager.store, supervisor)['kind']")
    s = once(s, "    assert require_backup(manager.store, supervisor)\n    copied = tmp_path",
             "    with manager.store.connection(True) as c:\n        c.execute(\"DELETE FROM hr_meta WHERE key='expiry_reminders_started_on'\")\n    assert require_backup(manager.store, supervisor)\n    copied = tmp_path")
    s = once(s, "    with imported.store.connection() as c:\n        assert not has_hr(c)",
             "    with imported.store.connection() as c:\n        assert all(not value for k, value in rows(c).items() if k != 'hr_meta')\n        assert {r[0] for r in c.execute('SELECT key FROM hr_meta')} <= {'format', 'expiry_reminders_started_on'}")
    return s

def eol(transform):
    def run(s):
        if '\r\n' not in s:
            return transform(s)
        return transform(s.replace('\r\n','\n')).replace('\n','\r\n')
    return run

def transforms():
    return {'app/project_modules.py': eol(modules), 'app/export_policy.py': eol(policy),
            'tests/test_hr_backup_ui117.py': eol(tests)}

def additions():
    name='test_hr_org_transfer.py'
    return {'tests/'+name: (BASE/name).read_bytes()}

if __name__ == '__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]), parent=PARENT, overlays=(Path(__file__).name,),
        cache=None, suffix='hr-org-transfer', scope='Keep organisation chart positions and their audit inside the private HR export module.')
