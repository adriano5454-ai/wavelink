from pathlib import Path
import runpy
import sys


def apply(root):
    previous = runpy.run_path(str(Path(__file__).with_name("apply_editor_exit.py")))
    previous["apply"](root, parent="71ac97fdf8433be3c26416095edfd4090f2a490ade4b4219258dfbbbe98baa4c",
                      overlays=("inventory_area.py",), previous_cache="ui162-roster-location",
                      cache="ui162-inventory-area", suffix="inventory-area",
                      scope="Filter inventory records by owning department in list and box views.")


if __name__ == "__main__":
    apply(Path(sys.argv[1]))
