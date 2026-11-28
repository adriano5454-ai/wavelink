"""Improve the Fleet map without network-dependent imagery or new provider credentials."""
from hashlib import sha256
from pathlib import Path
import runpy, sys

BASE=Path(__file__).resolve().parent
FILES=("fleet-satellite-world.jpg","fleet-satellite-rio.jpg")
def additions():
    return {"app/static/"+n:(BASE/n).read_bytes() for n in FILES}

def fleet(source):
    js=(BASE/"fleet_map_atlas.js").read_text(encoding="utf-8")
    for n,key in zip(FILES,("__WORLD_IMAGE__","__RIO_IMAGE__")):
        js=js.replace(key, f"/static/{n}?v=1.34.61-{sha256((BASE/n).read_bytes()).hexdigest()[:12]}")
    start=source.index("function interactiveFleetMap(")
    stop=source.index("async function showFleetPositions(){",start)
    prior=source[start:stop]
    assert "const gestures" not in prior and "const gesture=" in prior
    pointer_start=prior.index(" const pointers=new Map();")
    pointer_end=prior.index(" draw();\n const resize=",pointer_start)
    pointer=prior[pointer_start:pointer_end]
    pointer=pointer.replace("if(e.button!==0||pointers.size===2)return;", "if(e.button!==0||pointers.size===2||e.target.closest('[data-vessel-pin]'))return;")
    return source[:start]+js.replace("__POINTER_CONTROLS__",pointer)+source[stop:]

def transforms():
    return {"app/static/fleet.js":fleet}

if __name__=="__main__":
    runpy.run_path(str(BASE/"apply_editor_exit.py"))["apply"](
        Path(sys.argv[1]),parent="773facd200930d5fd95167f6d182ed8ad78af9980d452a982ecae9a998dc3b76",
        overlays=(Path(__file__).name,),previous_cache="ui162-fleet-interactive-map",cache="ui162-fleet-atlas",
        suffix="fleet-atlas",scope="Fleet coastline and NASA imagery layers, active vessel selection and detailed map views.")
