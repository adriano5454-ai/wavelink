"""Offer recorded final locations from the already authorised site inventory."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
one = runpy.run_path(str(BASE / 'apply_org_chart_filters.py'))['replace_once']


def placement(source):
    start = source.index('async function placementForm(entry)')
    end = source.index('async function ', start + 6)
    body = source[start:end]
    body = one(body, ' const send=operation', """ const label=(pt,en)=>document.documentElement.lang.toLowerCase().startsWith('pt')?pt:en;
 const manualLabel=label('Informar outro local','Enter another location');
 const known=[...new Set(all.filter(item=>!own.has(item.id)&&item.list_id===rootItem.list_id&&item.custody?.state==='available'&&(!item.custody.site_id||item.custody.site_id===entry.site_id))
  .map(item=>(item.location||'').trim()).filter(name=>name&&name.toLowerCase()!=='in transit'&&name.toLowerCase()!==entry.location.trim().toLowerCase()))].sort((a,b)=>a.localeCompare(b));
 const locationValue=()=>val('place-kind')==='manual'?val('place-location'):val('place-known');
 const send=operation""")
    body = one(body,"['box',__wl118.t('Existing box at this site')]", "['box',__wl118.t('Existing box at this site')],['manual',manualLabel]")
    body = one(body,'<div id="place-location-fields">','''<div id="place-known-fields">${select('place-known',__wl118.t('Final location / area'),[['',''],...known.map(name=>[name,name])])}<p>${E(known.length?manualLabel:label('Nenhum local final registrado para esta lista neste local. Use “Informar outro local”.','No recorded final locations for this list at this site. Choose “Enter another location”.'))}</p></div><div id="place-location-fields">''')
    body = one(body,"location:box?box.location:val('place-location')","location:box?box.location:locationValue()")
    body = one(body,"to:[box?box.path:val('place-location')]","to:[box?box.path:locationValue()]")
    body = one(body,"$('place-location-fields').hidden=inBox;", """const manual=val('place-kind')==='manual',knownMode=!inBox&&!manual;
 $('place-known-fields').hidden=!knownMode;$('place-known').disabled=!knownMode;$('place-known').required=knownMode;
 $('place-location-fields').hidden=!manual;""")
    body = one(body,"$('place-location').required=!inBox;$('place-location').disabled=inBox;", "$('place-location').required=manual;$('place-location').disabled=!manual;")
    body = one(body,"$('place-kind').onchange=update;", """$('place-known').addEventListener('change',()=>{$('place-confirm').checked=false;});
 AJLogisticsUI.picker($('place-known'),known.map(name=>({id:name,name,path:'',detail:'',reference:'',department:''})),{title:__wl118.t('Final location / area')});
 $('place-kind').onchange=update;""")
    return source[:start] + body + source[end:]


def transforms():
    return {'app/static/fleet.js': placement}


if __name__ == '__main__':
    runpy.run_path(str(BASE / 'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]), parent='dd7a0919776faa2a668b505e7ee762ae8202ba8b97dfed33e70116661d75cf06',
        overlays=(Path(__file__).name,), previous_cache='ui162-roster-receiving-context',
        cache='ui162-placement-locations', suffix='placement-locations',
        scope='Choose a recorded final location at the receiving site.')
