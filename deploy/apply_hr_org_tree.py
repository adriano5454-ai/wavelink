from pathlib import Path
import runpy
import sys

BASE=Path(__file__).parent

def one(s,a,b):
    if s.count(a)!=1:raise ValueError(a)
    return s.replace(a,b)

def backend(s):
    s=one(s,"def _org_units(c, user, caps, people):","def _org_units(c, user, caps, people, actor):")
    s=one(s,"self._org_units(c,user,capabilities,people)","self._org_units(c,user,capabilities,people,actor)")
    s=one(s,"        for p in visible:", """        from .recognition import Recognition
        try:
            Recognition._person(c, actor)
            profiles = True
        except Problem as exc:
            if exc.code not in (401,403): raise
            profiles = False
        for p in visible:""")
    return one(s,"            for key in membership_ids(c, p['id']", """            if profiles and Recognition._eligible(c, p['id']):
                member['profile_id'] = p['id']
            for key in membership_ids(c, p['id']""")

def frontend(s):
    s=one(s,'async function mountPositions(container){',(BASE/'hr_org_tree.js').read_text(encoding='utf8')+'\nasync function mountPositions(container){')
    s=one(s,'let data, busy=false;', 'let data, busy=false, editing=false;')
    s=one(s,'if(!data.positions.length&&!data.editor)return;',"""if(!editing){drawOrgTree(body,data,()=>{editing=true;draw()});return}
   body.append(button(text('View chart','Ver organograma'),()=>{editing=false;draw()}));""")
    s=one(s,"const row=person=>'<li><strong>'+E(person.name)+'</strong>'","const row=person=>'<li><strong>'+(person.profile_id?'<a href=\"#profile/'+E(person.profile_id)+'\" data-org-member=\"'+E(person.profile_id)+'\">'+E(person.name)+'</a>':E(person.name))+'</strong>'")
    return one(s,'records.prepend(positions);mountPositions(positions);',"""records.prepend(positions);
  const title=document.createElement('h2');title.textContent=orgText('Diretório por departamento','Department directory');positions.after(title);
  records.querySelectorAll('[data-org-member]').forEach(a=>{a.onclick=()=>{treeOwner=identity();returnLink={member:a.dataset.orgMember}}});
  if(treeOwner===identity()&&returnLink?.member){const a=records.querySelector('[data-org-member="'+CSS.escape(returnLink.member)+'"]');if(a)a.focus();returnLink=null}
  mountPositions(positions);""")

def transforms():
    return {'app/hr.py':backend,'app/static/hr_workspace.js':frontend,'app/static/ui132_visual.css':lambda s:s+"""
.org-tree{overflow:auto;max-width:100%;padding:.5rem}
.org-tree ul{padding:0;margin:0;list-style:none;display:flex;justify-content:center;width:max-content;min-width:100%}
.org-tree ul[hidden]{display:none}.org-tree li{position:relative;display:flex;flex-direction:column;align-items:center;padding:1rem .25rem 0}
.org-tree li:before,.org-tree li:after{content:'';position:absolute;top:0;width:50%;height:1rem;border-top:1px solid currentColor;opacity:.45}
.org-tree li:before{right:50%;border-right:1px solid}.org-tree li:after{left:50%}
.org-tree li:first-child:before,.org-tree li:last-child:after{border-top:0}.org-tree li:only-child:after{display:none}
.org-tree .org-roots>li:before,.org-tree .org-roots>li:after{display:none}
.org-tree li>ul:not([hidden]){position:relative;margin-top:1rem}.org-tree li>ul:before{content:'';position:absolute;bottom:100%;height:1rem;left:50%;border-left:1px solid;opacity:.45}
.org-node{display:grid;justify-items:center;gap:.3rem;padding:.65rem;border:1px solid var(--line);border-radius:.55rem;max-width:13rem;overflow-wrap:anywhere;text-align:center}
@media(max-width:640px){.org-tree ul{display:block;width:auto;min-width:0}.org-tree li{display:block;padding:.4rem 0}.org-tree li:before,.org-tree li:after,.org-tree li>ul:before{display:none}.org-tree li>ul:not([hidden]){margin:.25rem 0 0 .5rem;padding-left:.65rem;border-left:1px solid var(--line)}.org-node{max-width:none;justify-items:start;text-align:start}}
"""}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='1067e346d0e621a89e213fd7b3f59d054e34a9f7d4522f690c4e397734055233',overlays=(Path(__file__).name,),previous_cache='ui162-hr-positions',cache='ui162-hr-org-tree',suffix='hr-org-tree',scope='Collapsible reporting tree with authorized profile navigation.')
