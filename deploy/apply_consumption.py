"""Apply the isolated vessel consumption overlay to the verified release."""
from pathlib import Path
import runpy, sys
BASE = Path(__file__).resolve().parent
if __name__ == '__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='38b0b770bd3a9b2fbb294a60148bdab173c22c71ae0a36ea9a6b296f2d4b69db',
        overlays=('consumption_overlay.py',),previous_cache='ui162-operations-views',cache='ui162-vessel-consumption',
        suffix='vessel-consumption',scope='Daily vessel stock-balance consumption and fictional public practice entries.')
