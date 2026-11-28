from pathlib import Path
BASE=Path(__file__).resolve().parent
def once(s,a,b):
    if s.count(a)!=1:raise ValueError(a)
    return s.replace(a,b,1)
def fleet(s):
    s=once(s,'    access.ensure(c)','    access.ensure(c)\n    from .fleet_tank_readings import ensure as ensure_tanks\n    ensure_tanks(c)')
    s=once(s,"if action not in ('report_position',","if action not in ('record_tank_reading','report_position',")
    s=once(s,"        if action in ('report_position',","        if action=='record_tank_reading':\n            from .fleet_tank_readings import vessel\n            vessel(c,a,p.get('site_id'),'prepare')\n        elif action in ('report_position',")
    s=once(s,'    def do_save_site(self,c,p,a):','    def do_record_tank_reading(self,c,p,a):\n        from .fleet_tank_readings import save\n        return save(c,p,a)\n\n    def do_save_site(self,c,p,a):')
    return once(s,"        if kind=='site':","        if kind=='tank_reading':\n            from .fleet_tank_readings import result\n            return result(c,a,eid)\n        if kind=='site':")
def api(s):
    return once(s,"    @app.get('/api/fleet/receiving')",'''    @app.get('/api/fleet/tank-readings')
    def tank_readings(request: Request, site_id: str='', a=Depends(logged)):
        from .fleet_tank_readings import read
        from fastapi.responses import JSONResponse
        return JSONResponse(read(store.fleet,a,site_id,getattr(request.state,'public_demo_read_only',False)),headers={'Cache-Control':'no-store'})

    @app.get('/api/fleet/receiving')''')
def backup(s):
    anchor="'fleet_audit','fleet_files'"
    return once(s,anchor,anchor+",'fleet_tank_readings'")
def scripts(s):
    s=once(s,"if(page==='logbooks')return await showLogbooks();","if(page==='waterfuel')return await showTankSection(id);if(page==='logbooks')return await showLogbooks();")
    mark=" on('add-site',()=>siteForm());"
    link=""" const tankLink=document.createElement('a');tankLink.id='fleet-waterfuel';tankLink.className='btn';tankLink.href='#waterfuel';tankLink.textContent=fmT('Água e combustível','Water & fuel');root.querySelector('.fleet77-workspace')?.prepend(tankLink);"""
    s=once(s,mark,link+"\n"+mark)
    return once(s,'async function showSites(){',(BASE/'tank_section_ui.js').read_text(encoding='utf-8-sig')+'\nasync function showSites(){')
def page(s):
    s=once(s,'<p class="shell-group">Vessel logs</p>','''<a href="#waterfuel" data-workspace="waterfuel"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12 2c4 5 7 9 7 13a7 7 0 0 1-14 0c0-4 3-8 7-13Z"/></svg><span>Water &amp; fuel</span></a>
<p class="shell-group">Vessel logs</p>''')
    return s
def additions():return {'app/fleet_tank_readings.py':(BASE/'tank_section_model.py').read_bytes()}
def page_pt(s):
    anchor='<p class="shell-group">Registros da embarcação</p>'
    return page(once(s,anchor,'<p class="shell-group">Vessel logs</p>')).replace('Water &amp; fuel','Água e combustível').replace('<p class="shell-group">Vessel logs</p>',anchor)
def transforms():return {'app/fleet.py':fleet,'app/fleet_api.py':api,'app/project_modules.py':backup,'app/static/fleet.js':scripts,'app/static/fleet.html':page,'app/static/pt-BR/fleet.html':page_pt}
