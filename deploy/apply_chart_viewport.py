"""Keep the reporting chart in view through explicit navigation and branch changes."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
replace = runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']


def chart(source):
    source = replace(source, 'let filterOwner, chartFilters;', """function reachOrgCard(card){
 if(!card)return;
 // A filtered match may have been folded manually since the last search.
 for(let list=card.closest('ul');list;list=list.parentElement.closest('ul')){
   if(list.hidden)list.parentElement.querySelector(':scope > .org-node > [aria-expanded]').click();
 }
 card.focus({preventScroll:true});
 card.scrollIntoView({block:'center',inline:'center',behavior:'instant'});
}
let filterOwner, chartFilters;""")
    source = replace(source, ' const fields={}, text=orgText;', """ const fields={}, text=orgText;
 const jump=document.createElement('button');jump.type='button';jump.className='btn secondary org-result-jump';
 jump.textContent=text('Ir ao resultado','Go to result');count.after(jump);
 jump.onclick=()=>reachOrgCard(results.querySelector('[data-org-match]'));""")
    source = replace(source, '   clear.disabled=!active;', '   clear.disabled=!active; jump.hidden=!active||!matches.size;')
    source = replace(source, "section.append(el('h3',heading));container.append(section);", """const group=el('div');group.className='org-viewport-group';container.append(group);
   const actions=el('div');actions.className='org-viewport-actions';
   const center=btn(text('Centralizar na raiz','Center on root'),()=>reachOrgCard(section.querySelector('.org-roots > li > .org-node')));
   center.classList.add('org-root-action');actions.append(center);
   if(matches){
     const back=btn(text('Voltar aos filtros','Back to filters'),()=>{
       const input=container.parentElement.querySelector('.org-filter-controls input');
       input?.focus({preventScroll:true});input?.scrollIntoView({block:'center',behavior:'instant'});
     });
     actions.append(back);
   }
   group.append(actions,section);section.append(el('h3',heading));""")
    source = replace(source, "card.className='org-node';item.append(card);", """card.className='org-node';card.tabIndex=-1;card.setAttribute('role','group');
     card.setAttribute('aria-label',[r.role_name,r.person_name||text('Vaga','Vacant')].join(' · '));
     if(matches?.has(r.id))card.dataset.orgMatch='';
     item.append(card);""")
    return replace(source, "if(folds.has(parent))folds.delete(parent);else folds.add(parent);sync()", """const card=item.firstChild,before=card.getBoundingClientRect();
       if(folds.has(parent))folds.delete(parent);else folds.add(parent);
       sync();
       const after=card.getBoundingClientRect();
       section.scrollLeft+=after.left-before.left;
       window.scrollBy({top:after.top-before.top,behavior:'instant'});""")


def transforms():
    return {'app/static/hr_workspace.js':chart,
            'app/static/ui132_visual.css':lambda s:s+"""
.org-viewport-group{position:relative;min-width:0}
.org-viewport-actions{position:sticky;top:4.5rem;z-index:2;display:flex;justify-content:flex-end;gap:.35rem;pointer-events:none}
.org-viewport-actions button{pointer-events:auto}
.org-result-jump{margin-bottom:.5rem}
.org-node:focus-visible{outline:2px solid currentColor;outline-offset:2px}
@media(max-width:640px){.org-viewport-actions .org-root-action{display:none}}
"""}


if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='6ba71726b6d61edbbf2c89a977a4f19e8bc5c7afed27f1bdf75b7d19e619adde',
        overlays=(Path(__file__).name,),previous_cache='ui162-org-chart-avatars',cache='ui162-org-chart-viewport',
        suffix='org-chart-viewport',scope='Anchor chart branch controls and navigate to roots and filtered matches.')
