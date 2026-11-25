"""Apply the scoped navigation and visit-language fixes to the verified #82 runtime."""
from pathlib import Path
import runpy
import sys


if __name__ == '__main__':
    apply = runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(
        Path(sys.argv[1]),
        parent='495ffb677ed4a9cd1597878a29c0f30546a28c68baf8a63e8e2ea943507780e4',
        overlays=(
            'apply_asset_certificate_return.py',
            'apply_calendar_home_team_context.py',
            'apply_qshe_history_return.py',
            'apply_visit_footer_language.py',
        ),
        previous_cache='ui162-journal-history-return',
        cache='ui162-record-navigation-context',
        suffix='record-navigation-context',
        scope='Restore equipment certificate, Team, Home news and QSHE context and keep the language chosen for the current visit.',
    )
