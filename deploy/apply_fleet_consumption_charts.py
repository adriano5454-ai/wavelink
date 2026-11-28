"""Add dual consumption charts without changing calculations, permissions or storage."""
from hashlib import sha256
from pathlib import Path
import runpy
import sys
BASE = Path(__file__).resolve().parent
def additions():
    return {'app/static/fleet_consumption_charts.css': (BASE/'fleet_consumption_charts.css').read_bytes()}
def fleet(source):
    marker='function renderConsumption(card,result,site,kinds,make){'
    assert source.count(marker)==1
    before, suffix=source.split(marker,1)
    stop=suffix.index('async function showTankSection')
    body, rest=suffix[:stop], suffix[stop:]
    a=' panel.append(label,pick);pick.value=readingRangeProduct;'
    assert body.count(a)==1
    body=body.replace(a," const overview=make('div');overview.className='wl-usage-overview';panel.append(overview);\n"+a)
    a="  chart.replaceChildren();const k=pick.value,u=symbol(k),rows=related(k);"
    assert body.count(a)==1
    body=body.replace(a,"  fleetConsumptionOverview(overview,related,fmt,make);\n"+a)
    start=body.index("   const track=make('div');")
    end=body.index("   const detail=make('details');",start)
    body=body[:start]+body[end:]
    body=body.replace('  const max=Math.max(1,...rows.map(r=>r.used)), list=', '  const list=').replace('li.append(row,track,detail);','li.append(row,detail);')
    return before+(BASE/'fleet_consumption_charts.js').read_text(encoding='utf-8')+'\n'+marker+body+rest
def html(source):
    assert source.count('</head>')==1
    path='fleet_consumption_charts.css'
    suffix=sha256((BASE/path).read_bytes()).hexdigest()[:12]
    return source.replace('</head>',f'<link rel="stylesheet" href="/static/{path}?v=1.34.61-{suffix}">\n</head>')
def transforms():
    return {'app/static/fleet.js': fleet, 'app/static/fleet.html': html}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='e9f0aeab92468f6d44ebf777f432b3bebe01917f7a4cc9e41bcb306c0066ec31',
        overlays=(Path(__file__).name,),previous_cache='ui162-fleet-atlas',cache='ui162-fleet-consumption-charts',
        suffix='fleet-consumption-charts',scope='Freshwater and diesel consumption overview with dated charts, recorded-day totals and preserved balance detail.')
