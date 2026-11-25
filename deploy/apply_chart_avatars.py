"""Decorate chart identities using the existing authorized profile image route."""
from pathlib import Path
import sys
import runpy

BASE = Path(__file__).resolve().parent
replace = runpy.run_path(str(BASE / 'apply_org_chart_filters.py'))['replace_once']


def directory(source):
    anchor = '        for p in visible:\n            # Read only the job title'
    source = replace(source, anchor, """        import json
        images = set()
        if profiles and visible:
            images = {r[0] for r in c.execute(
                "SELECT user_id FROM member_profiles WHERE avatar_sha256 != '' "
                "AND user_id IN (SELECT value FROM json_each(?))",
                (json.dumps([p['id'] for p in visible]),))}
""" + anchor)
    return replace(source, "                member['profile_id'] = p['id']",
                   "                member['profile_id'] = p['id']\n                if p['id'] in images: member['has_avatar'] = True")


def chart(source):
    source = replace(source, 'function paintOrgTree(', (BASE/'org_chart_avatar.js').read_text('utf8')+'\nfunction paintOrgTree(')
    source = replace(source, " const persons=new Set(directory.org_chart.units.flatMap(u=>[...u.people,...u.heads]).map(p=>p.profile_id).filter(Boolean));",
                     " const persons=new Map(directory.org_chart.units.flatMap(u=>[...u.people,...u.heads]).filter(p=>p.profile_id).map(p=>[p.profile_id,p]));")
    return replace(source, '     card.append(link);', """     if(r.person){
       const person=el('div');person.className='org-person';person.append(chartAvatar(r.person_name,persons.get(r.person)),link);card.append(person);
     }else{link.className='org-vacancy';card.append(link)}""")


def transforms():
    return {'app/hr.py':directory,'app/static/hr_workspace.js':chart,
            'app/static/ui132_visual.css':lambda s:s+"""
.org-person{display:flex;align-items:center;gap:.4rem;max-width:100%;min-width:0}
.org-person>a,.org-person>span:last-child{min-width:0;overflow-wrap:anywhere}
.org-person .org-avatar{display:inline-grid;place-items:center;flex:none;width:1.8rem;height:1.8rem;border-radius:50%;overflow:hidden;background:var(--line);font-weight:600;font-size:.72rem}
.org-avatar img{width:100%;height:100%;object-fit:cover}
.org-vacancy{border:1px dashed var(--line);border-radius:.4rem;padding:.08rem .4rem}
@media(max-width:640px){.org-person>a{display:inline-flex;align-items:center;min-height:44px}}
"""}


if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='60c8d27b6889fdab36e2528c4a5145b48c82bf83577915b64a3b3350c00260c4',
        overlays=(Path(__file__).name,),previous_cache='ui162-demo-chart-locales',cache='ui162-org-chart-avatars',
        suffix='org-chart-avatars',scope='Display authorized profile images or initials for filled chart positions.')
