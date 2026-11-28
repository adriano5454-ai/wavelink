"""Deliberate external OpenStreetMap navigation, no tiles/requests on render."""
from pathlib import Path
import runpy,sys

def fleet(s):
    anchor=' const ul=make(\'ul\');if(!data.sites.length)box.append'
    assert s.count(anchor)==1
    s=s.replace(anchor," box.append(make('p',fmT('Abrir no OpenStreetMap envia apenas as coordenadas selecionadas ao site externo.','Open in OpenStreetMap sends only the selected coordinates to the external site.')));\n"+anchor)
    anchor="li.append(text);if(p){const x=(p.lon+180)*2,y=(90-p.lat)*2;"
    assert s.count(anchor)==1
    return s.replace(anchor,"""li.append(text);if(p){const open=make('button',fmT('Abrir no OpenStreetMap','Open in OpenStreetMap'));open.type='button';open.className='btn';open.setAttribute('aria-label',open.textContent+' · '+s.name);open.onclick=()=>{const u=new URL('https://www.openstreetmap.org/');u.searchParams.set('mlat',String(p.lat));u.searchParams.set('mlon',String(p.lon));u.hash='map=9/'+p.lat+'/'+p.lon;window.open(u.href,'_blank','noopener,noreferrer');};li.append(open);const x=(p.lon+180)*2,y=(90-p.lat)*2;""")
def transforms():return {'app/static/fleet.js':fleet}
def additions():return {}
if __name__=='__main__':
    runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply'](
        Path(sys.argv[1]),parent='6d9c473b26bb7346d136881d1ca7fc3589fafd851993f12ced792dbb60ddad58',
        overlays=(Path(__file__).name,),previous_cache='ui162-vessel-consumption',cache='ui162-fleet-osm',
        suffix='fleet-osm',scope='Public showcase fictional vessel positions and opt-in external OpenStreetMap links.')
