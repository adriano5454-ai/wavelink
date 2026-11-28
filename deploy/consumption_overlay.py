from pathlib import Path
BASE=Path(__file__).resolve().parent

def once(s,a,b):
    if s.count(a)!=1:raise ValueError(a)
    return s.replace(a,b,1)

def fleet(s):
    s=once(s,'    ensure_tanks(c)', '''    ensure_tanks(c)
    from .fleet_consumption import ensure as ensure_consumption
    from .fleet_consumption_access import ensure as ensure_consumption_access
    ensure_consumption(c)
    ensure_consumption_access(c)''')
    s=once(s,"if action not in ('record_tank_reading',","if action not in ('record_consumption','record_tank_reading',")
    s=once(s,"        if action=='record_tank_reading':","""        if action=='record_consumption':
            from .fleet_consumption_access import require
            require(c,a,p.get('site_id'))
        elif action=='record_tank_reading':""")
    s=once(s,"        if kind=='tank_reading':","        if kind=='consumption':\n            from .fleet_consumption import result\n            return result(c,a,eid)\n        if kind=='tank_reading':")
    s=once(s,'    def do_record_tank_reading', '    def do_record_consumption(self,c,p,a):\n        from .fleet_consumption import save\n        return save(c,p,a)\n\n    def do_record_tank_reading')
    query='SELECT site_id,role FROM fleet_site_grants WHERE user_id=?'
    assert s.count(query)==2
    s=s.replace(query,'''SELECT g.site_id,g.role,EXISTS(SELECT 1 FROM fleet_consumption_grants f WHERE f.user_id=g.user_id AND f.site_id=g.site_id) AS consumption FROM fleet_site_grants g WHERE g.user_id=?''')
    s=once(s,"        seen=set();clean=[]", """        previous_consumption={r[0] for r in c.execute('SELECT site_id FROM fleet_consumption_grants WHERE user_id=?',(uid,))}
        seen=set();clean=[]""")
    s=once(s,"            sid=ident(g.get('site_id'));_site(c,sid,active=True)","            sid=ident(g.get('site_id'));site=_site(c,sid,active=True)")
    s=once(s,"            seen.add(sid);clean.append(dict(site_id=sid,role=g['role']))","""            post=g.get('consumption',sid in previous_consumption and site['kind']=='vessel')
            if type(post) is not bool or (post and (site['kind']!='vessel' or mode=='project_user')):
                raise Problem(422,'Consumption posting requires an active vessel grant.')
            seen.add(sid);clean.append(dict(site_id=sid,role=g['role'],consumption=post))""")
    return once(s,"        if c.execute(\"SELECT 1 FROM sqlite_master WHERE name='fleet_log_permissions'\").fetchone():","""        c.execute('DELETE FROM fleet_consumption_grants WHERE user_id=?',(uid,))
        c.executemany('INSERT INTO fleet_consumption_grants VALUES(?,?)',[(uid,g['site_id']) for g in clean if g['consumption']])
        if c.execute("SELECT 1 FROM sqlite_master WHERE name='fleet_log_permissions'").fetchone():""")

def tank(s):
    return once(s,"        return {'sites':sites,'latest':latest",'''        from .fleet_consumption import daily
        from .fleet_consumption_access import allowed
        return {'sites':sites,'consumption':daily(c,sid),'practice':bool(readonly),
                'can_record_consumption':not readonly and allowed(c,a,sid),'latest':latest''')

def backup(s):
    s=once(s,"'fleet_files','fleet_tank_readings'","'fleet_files','fleet_tank_readings','fleet_consumption'")
    return once(s,"'fleet_sites','fleet_site_grants','fleet_account_scope',","'fleet_sites','fleet_site_grants','fleet_consumption_grants','fleet_account_scope',")

def ui(s):
    s=once(s,'const check=(id,label)=>','const check=(id,label,selected=false)=>')
    s=once(s,'type="checkbox" id="${id}"><span>${E(label)}','type="checkbox" id="${id}" ${selected?\'checked\':\'\'}><span>${E(label)}')
    s=once(s,"u.grants.find(g=>g.site_id===s.id)?.role||'')).join('')","""u.grants.find(g=>g.site_id===s.id)?.role||'')+(s.kind==='vessel'?check('usage-grant-'+s.id,fmT('Pode registrar consumo nesta embarcação','Can post consumption for this vessel'),!!u.grants.find(g=>g.site_id===s.id)?.consumption):'')).join('')""")
    s=once(s,"role:val('grant-'+s.id)})),reason:", "role:val('grant-'+s.id),consumption:s.kind==='vessel'&&checked('usage-grant-'+s.id)})),reason:")
    s=once(s," const site=result.sites.find(s=>s.id===id);",""" const site=result.sites.find(s=>s.id===id);
 const tabs=make('div');tabs.style.cssText='display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0';
 const readings=make('button',fmT('Leituras de tanques','Tank readings')), consumption=make('button',fmT('Consumo','Consumption'));
 readings.id='tank-readings-tab';consumption.id='tank-consumption-tab';readings.className=consumption.className='btn';
 tabs.append(readings,consumption);card.append(tabs);
 const body=make('div');card.append(body);
 const activate=show=>{readings.setAttribute('aria-pressed',String(!show));consumption.setAttribute('aria-pressed',String(show));readings.classList.toggle('primary',!show);consumption.classList.toggle('primary',show);body.hidden=show;balance.hidden=!show;};
 const balance=renderConsumption(card,result,site,kinds,make);
 readings.onclick=()=>activate(false);consumption.onclick=()=>activate(true);
 activate(false);""")
    s=once(s,'Leituras manuais por embarcação. As quantidades de tanques não são somadas.','Leituras de tanques e consumo diário por embarcação.')
    s=once(s,'Manual readings by vessel. Tank quantities are not added together.','Tank readings and daily consumption by vessel.')
    a=s.index('async function showTankSection(');b=s.index('async function showSites(){',a)
    seg=s[a:b]
    seg=seg.replace('card.append(b);','body.append(b);').replace("card.append(make('h2',title))","body.append(make('h2',title))").replace("card.append(make('p',fmT('Nenhuma leitura","body.append(make('p',fmT('Nenhuma leitura").replace('card.append(ul)','body.append(ul)').replace('card.append(hd,lbl,pick,plot)','body.append(hd,lbl,pick,plot)').replace("if(result.more)card.append","if(result.more)body.append")
    return s[:a]+(BASE/'consumption_ui.js').read_text(encoding='utf8')+'\n'+seg+s[b:]

def additions():
    return {'app/fleet_consumption.py':(BASE/'consumption_model.py').read_bytes(),
            'app/fleet_consumption_access.py':(BASE/'consumption_access.py').read_bytes()}
def transforms():return {'app/fleet.py':fleet,'app/fleet_tank_readings.py':tank,'app/project_modules.py':backup,'app/static/fleet.js':ui}
