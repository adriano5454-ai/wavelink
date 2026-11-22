"""Promote the inventory's registered storage locations into the main search row."""
from pathlib import Path
import runpy
import sys


def fieldwork(source):
    def change(old, new):
        nonlocal source
        if source.count(old) != 1:
            raise ValueError("Unexpected Inventory UI: " + old)
        source = source.replace(old, new)

    start = source.index("${select('location',__wl118.t('Location')")
    end = source.index("${select('source',", start)
    source = source[:start] + source[end:]
    change("  const vessels=b.vessels||[]", """  const locationKey=value=>value && value.trim() ? value : 'Unassigned';
  const physicalLabel=value=>value==='Unassigned'?txt('Sem local','No location'):inventoryLocationLabel(value);
  const itemLocations=new Set(b.items.map(item=>locationKey(item.location)));
  const locations=[...new Set([...b.locations,...itemLocations])].filter(value=>value && (value!=='Unassigned'||itemLocations.has(value)));
  const vessels=b.vessels||[]""")
    change("${inventoryVesselField(vessels)}${select('department'", """${inventoryVesselField(vessels)}${select('location',txt('Local físico','Physical location'),[['',txt('Todos os locais','All locations')],...locations.map(value=>[value,physicalLabel(value)])],inventoryFilter.location)}${select('department'""")
    change("||x.location===inventoryFilter.location", "||locationKey(x.location)===inventoryFilter.location")
    change("const categoryRows=b.items.filter(x=>", "const categoryRows=b.items.filter(x=>(!inventoryFilter.location||locationKey(x.location)===inventoryFilter.location)&&")
    change("labels.push(inventoryLocationLabel(inventoryFilter.location))", "labels.push(txt('Local físico','Physical location')+' · '+physicalLabel(inventoryFilter.location))")
    return source


def transforms():
    return {'app/static/fieldwork.js': fieldwork}


if __name__ == '__main__':
    apply = runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]), parent='c7cf87f275911f7d65b29c77073f8769ff394d0ee99dd66c4067859c029ca89f',
          overlays=(Path(__file__).name,), previous_cache='ui162-inventory-area',
          cache='ui162-inventory-physical-location', suffix='physical-location',
          scope='Filter authorized inventory records by their registered storage location.')
