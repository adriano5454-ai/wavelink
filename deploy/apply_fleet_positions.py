"""Add permission-scoped, manually reported vessel positions to Fleet."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
PARENT = 'c01fe2b32da02f08bcfcba724bacb1b11bb8bf5139bcae2470ed1c58904dc3e7'

def replace(source, before, after):
    if source.count(before) != 1:
        raise ValueError(before)
    return source.replace(before, after, 1)

def fleet(source):
    source = replace(source, '    access.ensure(c)', '    access.ensure(c)\n    from .fleet_positions import ensure as ensure_positions\n    ensure_positions(c)')
    source = replace(source, "if action not in ('save_site',", "if action not in ('report_position','save_site',")
    source = replace(source, "if action in ('save_site','set_access','allocate'):", "if action in ('report_position','save_site','set_access','allocate'):")
    return replace(source, '    def do_save_site(self,c,p,a):',
        '    def do_report_position(self,c,p,a):\n        from .fleet_positions import save\n        return save(c,p,a)\n\n    def do_save_site(self,c,p,a):')

def api(source):
    return replace(source, "    @app.get('/api/fleet/receiving')", """    @app.get('/api/fleet/positions')
    def positions(request: Request, a=Depends(logged)):
        from .fleet_positions import read
        from fastapi.responses import JSONResponse
        result = read(store.fleet,a)
        if getattr(request.state,'public_demo_read_only',False):
            result['admin'] = False
        return JSONResponse(result, headers={'Cache-Control':'no-store'})

    @app.get('/api/fleet/receiving')""")

def backup(source):
    base = "'fleet_custody','fleet_manifests','fleet_audit','fleet_files'"
    return replace(source, base, base + ",'fleet_position_reports'")

def scripts(source):
    source = replace(source, "if(page==='logbooks')return await showLogbooks();",
        "if(page==='positions')return await showFleetPositions();if(page==='logbooks')return await showLogbooks();")
    link = " const mapLink=document.createElement('a');mapLink.className='btn';mapLink.href='#positions';mapLink.textContent=fmT('Mapa da frota','Fleet map');root.querySelector('.fleet77-workspace')?.prepend(mapLink);"
    source = replace(source, " on('add-site',()=>siteForm());", link+"\n on('add-site',()=>siteForm());")
    return replace(source, 'async function showSites(){',
        (BASE/'fleet_positions_ui.js').read_text(encoding='utf-8-sig')+'\nasync function showSites(){')

def additions():
    return {'app/fleet_positions.py': (BASE/'fleet_positions_model.py').read_bytes()}

def transforms():
    return {'app/fleet.py':fleet,'app/fleet_api.py':api,'app/project_modules.py':backup,'app/static/fleet.js':scripts}

if __name__ == '__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),
        previous_cache='ui162-tank-readings',cache='ui162-fleet-positions',suffix='fleet-positions',
        scope='Private Fleet map of manually reported positions using existing vessel access settings.')
