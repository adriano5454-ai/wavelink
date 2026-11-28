"""Add bounded UTC range controls to the verified Demo Fleet map release."""
from pathlib import Path
import runpy, sys
BASE = Path(__file__).resolve().parent
if __name__ == '__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent='9bbff29ccd83c55253405d19a5ed7018ad190f38181b5600a4fc15e3a3e00b63',
        overlays=('vessel_reading_range_overlay.py',),
        previous_cache='ui162-fleet-osm',cache='ui162-fleet-reading-ranges',
        suffix='fleet-reading-ranges',
        scope='Fleet map with all-vessel fictional examples and localized Water & Fuel UTC date ranges.')
