"""Project the visible HR directory by active department."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).parent


def replace(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected HR source: ' + old)
    return source.replace(old, new)


def backend(source):
    anchor = "    def directory(self, actor):"
    helper = """    @staticmethod
    def _org_units(c, user, caps, people):
        from .departments import membership_ids
        all_people = caps['hr.people_manage']
        show_heads = all_people and user['role'] == 'admin'
        visible = [p for p in people if p['enabled'] and (all_people or p['id'] == user['id'])]
        units = {r['id']: dict(name=r['name'], heads=[], people=[])
                 for r in c.execute('SELECT id,name FROM ops_departments WHERE active=1 ORDER BY name')}
        groups = {}
        heads = set(map(tuple, c.execute('SELECT department_id,user_id FROM department_heads'))) if show_heads else set()
        for p in visible:
            # Read only the job title from the canonical HR person record.
            title = c.execute(\"SELECT json_extract(body,'$.job_title') FROM hr_records WHERE kind='people' AND user_id=? ORDER BY updated_at DESC,id LIMIT 1\", (p['id'],)).fetchone()
            member = dict(name=p['name'], title=(title[0] or '') if title else '')
            for key in membership_ids(c, p['id'], active_only=True) or ['']:
                unit = groups.setdefault(key, units[key] if key else dict(name='', heads=[], people=[]))
                unit['heads' if (key, p['id']) in heads else 'people'].append(member)
        return dict(units=sorted(groups.values(), key=lambda g:(not g['name'],g['name'].casefold())), show_heads=bool(show_heads))

"""
    source = replace(source, anchor, helper + anchor)
    return replace(source, "'users':people,", "'users':people, 'org_chart':self._org_units(c,user,capabilities,people),")


def frontend(s):
    s = replace(s, "function tabs(){return", "const orgText=(pt,en)=>window.WavelinkUX.text(pt,en);\n function tabs(){return")
    s = replace(s, "['people',__hr121.t('Colaboradores')", "['org',orgText('Organograma','Organization chart'),true],['people',__hr121.t('Colaboradores')")
    s = s.replace("['dashboard','calendar','people','reports'", "['dashboard','calendar','org','people','reports'")
    s = replace(s, "E(view==='dashboard'?", "E(view==='org'?orgText('Organograma','Organization chart'):view==='dashboard'?")
    s = replace(s, "hidden=['people','reviews']", "hidden=['org','people','reviews']")
    return replace(s, "function renderRecords(){", (BASE/'hr_org_chart.js').read_text(encoding='utf8') + "\n function renderRecords(){\n  if(current()&&!form&&view==='org'){renderOrg();return;}")


def transforms():
    return {'app/hr.py':backend,'app/static/hr_workspace.js':frontend,
            'app/static/ui132_visual.css':lambda s:s + """
.hr-org-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,18rem),1fr));gap:1rem;align-items:start}
.hr-org-unit{min-width:0;padding:1rem;border:1px solid var(--line);border-radius:.65rem;overflow-wrap:anywhere}
.hr-org-unit h3{margin:0 0 .5rem}.hr-org-unit ul{list-style:none;padding:0;margin:.5rem 0 0}
.hr-org-unit li{padding:.35rem 0}.hr-org-unit small{display:block}.hr-org-unit .hr-org-head{border-inline-start:3px solid var(--accent);padding-inline-start:.65rem}
"""}


if __name__ == '__main__':
    apply = runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply']
    apply(Path(sys.argv[1]),parent='4f8498ef1c29af28dc88a7ce8d4f861e39d45a2827e19781c77859f2d3f1323d',
          overlays=(Path(__file__).name,),previous_cache='ui162-handover-shifts',cache='ui162-hr-org-chart',
          suffix='hr-org-chart',scope='Read-only HR organization chart by department.')
