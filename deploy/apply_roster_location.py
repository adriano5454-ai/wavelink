from pathlib import Path
import runpy
import sys


def apply(root):
    previous = runpy.run_path(str(Path(__file__).with_name("apply_editor_exit.py")))
    previous["apply"](root, parent="f8f0189c2b862511d28628be5e254e238c1739aafe9e38b82deaf815d18b125d",
                      overlays=("roster_location.py",), previous_cache=previous["CACHE"],
                      cache="ui162-roster-location", suffix="roster-location",
                      scope="Read-only daily roster grouped by scheduled work location and project.")


if __name__ == "__main__":
    apply(Path(sys.argv[1]))
