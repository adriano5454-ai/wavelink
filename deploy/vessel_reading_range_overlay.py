from pathlib import Path

BASE = Path(__file__).resolve().parent


def once(s, a, b):
    if s.count(a) != 1:
        raise ValueError(a)
    return s.replace(a, b, 1)


def tank(s):
    s = once(s, "def read(fleet,a,sid='',readonly=False):",
             "def read(fleet,a,sid='',readonly=False,period='',start='',end=''):")
    s = once(s, "        vessel(c,a,sid)\n        cols=", """        vessel(c,a,sid)
        from .fleet_reading_range import limits
        lower, upper, stop = limits(period,start,end)
        cols=""")
    s = once(s, "WHERE site_id=? ORDER BY {order} LIMIT 101',(sid,))]",
             "WHERE site_id=? AND observed>=? AND observed<? ORDER BY {order} LIMIT 2001',(sid,lower,stop))]")
    s = once(s, "'consumption':daily(c,sid)", "'consumption':daily(c,sid,lower,upper),'range':{'from':lower,'to':upper}")
    return once(s, "'history':history[:100],'more':len(history)>100",
                "'history':history if len(history)<=2000 else [],'more':len(history)>2000")


def api(s):
    s = once(s, "def tank_readings(request: Request, site_id: str='', a=Depends(logged)):",
             "def tank_readings(request: Request, site_id: str='', period: str='', start: str='', end: str='', a=Depends(logged)):")
    return once(s, "read(store.fleet,a,site_id,getattr(request.state,'public_demo_read_only',False))",
                "read(store.fleet,a,site_id,getattr(request.state,'public_demo_read_only',False),period,start,end)")


def consumption(s):
    s = once(s, "def daily(c, sid):", "def daily(c, sid, lower, upper):")
    return once(s, "AND contents=? ORDER BY day DESC LIMIT 30',\n        (sid,kind)",
                "AND contents=? AND day BETWEEN ? AND ? ORDER BY day DESC',\n        (sid,kind,lower,upper)")


def ui(s):
    p = s.index('function renderConsumption(')
    s = s[:p] + (BASE/'vessel_reading_range_ui.js').read_text(encoding='utf8') + '\n' + s[p:]
    s = once(s, "(id?'?site_id='+encodeURIComponent(id):'')", "(id?'?'+readingRangeQuery(id):'')")
    s = once(s, " const tabs=make('div');", " card.append(readingRangeControls(make,result.range));\n const tabs=make('div');")
    s = once(s, "readings.onclick=()=>activate(false);consumption.onclick=()=>activate(true);\n activate(false);",
             "readings.onclick=()=>{readingRangeConsumption=false;activate(false);};consumption.onclick=()=>{readingRangeConsumption=true;activate(true);};\n activate(readingRangeConsumption);")
    s = once(s, ".sort((a,b)=>b.day.localeCompare(a.day)).slice(0,30);",
             ".filter(r=>r.day>=result.range.from&&r.day<=result.range.to).sort((a,b)=>b.day.localeCompare(a.day));")
    s = once(s, "panel.append(label,pick);", "panel.append(label,pick);pick.value=readingRangeProduct;")
    s = once(s, " pick.onchange=draw;draw();return panel;", " pick.onchange=()=>{readingRangeProduct=pick.value;draw();};draw();return panel;")
    s = once(s, "const first=Date.parse(data[0].observed),last=Date.parse(data.at(-1).observed),max=", "const max=")
    s = once(s, "if(related(data.contents).some(r=>r.day===data.day))",
             "if([...(result.consumption[data.contents]||[]),...(result.practice?(usageScratch.get(site.id)||[]).filter(r=>r.contents===data.contents):[])].some(r=>r.day===data.day))")
    s = s.replace("Total dos dias registrados exibidos:", "Total dos dias registrados no período:").replace("Total across displayed recorded days:", "Total for recorded days in range:")
    s = s.replace("Últimos 30 dias registrados","Balanços no período").replace("Last 30 recorded days","Balances in range")
    s = s.replace("Histórico recente","Histórico no período").replace("Recent history","History in range")
    old = "   svg(s,'path',{d:'M60 16V146H588',fill:'none',stroke:'#8c9da4'});"
    begin = s.index(old)
    end = s.index("\n",begin)
    s = s[:begin]+old+s[end:]
    s = once(s, "   if(data.length<2||first===last)", "   if(!data.length)")
    s = once(s, "(Date.parse(r.observed)-first)/(last-first)*528",
             "(Date.parse(r.observed)-Date.parse(result.range.from))/(Date.parse(result.range.to+'T23:59:59Z')-Date.parse(result.range.from))*528")
    s = s.replace("data[0].observed.slice(0,10)", "result.range.from").replace("data.at(-1).observed.slice(0,10)", "result.range.to")
    s = once(s, " render(fmT('Histórico no período','History in range'),result.history);",
             " if(!result.more)render(fmT('Histórico no período','History in range'),result.history);")
    return s.replace("São mostradas as 100 leituras mais recentes.", "Mais de 2.000 leituras no período. Selecione um intervalo menor para ver o histórico e o gráfico.").replace("Shows the 100 most recent readings.", "Over 2,000 readings in range. Select a shorter range to view the complete history and chart.")


def additions():
    return {'app/fleet_reading_range.py':(BASE/'vessel_reading_range_model.py').read_bytes()}


def transforms():
    return {'app/fleet_api.py':api,'app/fleet_tank_readings.py':tank,'app/fleet_consumption.py':consumption,'app/static/fleet.js':ui}

