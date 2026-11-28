"""Use normal Fleet and main-shell navigation for the new operating views."""
from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
PARENT = '3e5101dc3b757689512fb5c5e1ba79e12559834cc3835c4da022a3617b56e479'
if __name__ == '__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,
        overlays=('readiness_navigation_overlay.py','tank_section.py'),
        previous_cache='ui162-fleet-positions',cache='ui162-operations-views',
        suffix='operations-views',
        scope='Safety & quality readiness tab with source charts; separate site-scoped Water & fuel workspace.')

