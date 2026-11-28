"""Default to an authorised fleet consumption comparison and preserve vessel detail."""
from hashlib import sha256
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
CSS = 'fleet_consumption_compare.css'


def once(source, before, after):
    if source.count(before) != 1:
        raise ValueError(before)
    return source.replace(before, after, 1)


def api(source):
    source = once(source, "end: str='', a=Depends(logged)):", "end: str='', comparison: bool=False, a=Depends(logged)):")
    return once(source, "False),period,start,end)", "False),period,start,end,comparison)")


def tank(source):
    source = once(source, "period='',start='',end=''):", "period='',start='',end='',comparison=False):")
    return once(source, "        if not sid:return {'sites':sites}", """        if not sid:
            if not comparison:return {'sites':sites}
            from .fleet_reading_range import limits
            lower, upper, _ = limits(period,start,end)
            # Query only IDs already authorised by the same vessel access check as the detail view.
            metrics = {}
            for site in sites:
                sid = site['id']
                rows = c.execute('''SELECT contents, COUNT(*) AS days,
                    SUM(CAST(ROUND(used * 1000) AS INTEGER)) AS milli
                    FROM fleet_consumption
                    WHERE site_id=? AND day BETWEEN ? AND ? AND
                        ((contents='fresh_water' AND unit='m3') OR (contents='diesel' AND unit='L'))
                    GROUP BY contents''', (sid,lower,upper))
                metrics[sid] = {r['contents']:{'days': r['days'], 'total': r['milli']/1000} for r in rows}
            return {'sites':sites,'comparison':metrics,'range':{'from':lower,'to':upper},'practice':bool(readonly)}""")


def fleet(source):
    marker = "async function showTankSection(id=''){"
    source = once(source, "readingRangeConsumption=false,readingRangeProduct=", "readingRangeConsumption=true,readingRangeProduct=")
    source = once(source, "tabs.append(readings,consumption);card.append(tabs);",
                  "tabs.append(consumption,readings);card.append(tabs);")
    source = once(source, "drop.value=id;drop.onchange=()=>{location.hash='waterfuel'",
                  "drop.value=id;drop.onchange=()=>{readingRangeConsumption=true;location.hash='waterfuel'")
    source = once(source, marker, (BASE/'fleet_consumption_compare.js').read_text(encoding='utf-8')+'\n'+marker)
    source = once(source, "'/api/fleet/tank-readings'+(id?'?'+readingRangeQuery(id):'')",
                  "'/api/fleet/tank-readings?'+(id?readingRangeQuery(id):new URLSearchParams({comparison:'true',...readingRange}))")
    source = once(source, "fmT('Selecione uma embarcação','Select a vessel')", "fmT('Todas as embarcações','All vessels')")
    return once(source, """if(!id){if(!result.sites.length)card.append(make('p',fmT('Nenhuma embarcação disponível.','No vessels available.')));return;}""",
                """if(!id){
  if(!result.sites.length){card.append(make('p',fmT('Nenhuma embarcação disponível.','No vessels available.')));return;}
  card.append(readingRangeControls(make,result.range));renderFleetConsumptionComparison(card,result,make);return;
 }""")


def html(source):
    suffix = sha256((BASE/CSS).read_bytes()).hexdigest()[:12]
    return once(source, '</head>', f'<link rel="stylesheet" href="/static/{CSS}?v=1.34.61-{suffix}">\n</head>')


def additions():
    return {'app/static/'+CSS:(BASE/CSS).read_bytes()}


def transforms():
    return {'app/fleet_api.py':api,'app/fleet_tank_readings.py':tank,'app/static/fleet.js':fleet,'app/static/fleet.html':html}


if __name__ == '__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]), parent='fa165657974c64c31e7849016d1db491847642ed01fa5da718ed6264eacf757e',
        overlays=(Path(__file__).name,), previous_cache='ui162-fleet-consumption-charts',
        cache='ui162-fleet-graphs-first', suffix='fleet-consumption-comparison',
        scope='Fleet-wide freshwater and diesel totals for one UTC period; existing per-vessel details and permission boundaries preserved.')
