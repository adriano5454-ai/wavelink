"""Add a worldwide, offline, interactive basemap to the existing Fleet map."""
from hashlib import sha256
from pathlib import Path
import json
import runpy
import sys

HERE = Path(__file__).resolve().parent

def fleet(s):
    geo = (HERE / "fleet_map_land.json").read_bytes()
    data = json.loads(geo)
    js = (HERE / "fleet_map_interactive.js").read_text(encoding="utf-8")
    js = js.replace("__FLEET_LAND__", json.dumps({k:data[k] for k in ("world","rio")},separators=(",",":")))
    at = "async function showFleetPositions(){"
    assert s.count(at) == 1
    s = s.replace(at, js + "\n" + at)
    start = s.index(" const map=addSvg(box,'svg',{viewBox:'-14 -14 748 388'")
    end = s.index(" box.append(make('p',fmT('Abrir no OpenStreetMap", start)
    s = s[:start] + " interactiveFleetMap(box,addSvg,make,data.sites);\n" + s[end:]
    start = s.index("const x=(p.lon+180)*2,y=(90-p.lat)*2;")
    end = s.index("\n if(data.admin)", start)
    s = s[:start] + "}" + s[end:]
    return s

def transforms():
    return {"app/static/fleet.js":fleet}

if __name__ == "__main__":
    runpy.run_path(str(HERE / "apply_editor_exit.py"))["apply"](
        Path(sys.argv[1]), parent="bf38b0e38cef8983e37c522d9d8fc2303ce4a1cf2735e591706f8a7c18d461b0",
        overlays=(Path(__file__).name,), previous_cache="ui162-fleet-reading-ranges",
        cache="ui162-fleet-interactive-map", suffix="fleet-interactive-map",
        scope="Offline worldwide interactive Fleet basemap with a Rio–Macaé detail layer and fictional demo positions.")
