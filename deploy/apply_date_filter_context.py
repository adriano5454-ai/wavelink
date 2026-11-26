"""Keep the selected dates when changing filters in HR, Handovers and Operations."""
from pathlib import Path
import runpy
import sys


if __name__ == '__main__':
    apply = runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(
        Path(sys.argv[1]),
        parent='e5b3a215ce8780d1d1844d3e48e524812398543f40ac4018db267357f555bcce',
        overlays=(
            'apply_roster_filter_dates.py',
            'apply_handover_filter_dates.py',
            'apply_ops_calendar_filter_day.py',
        ),
        previous_cache='ui162-record-navigation-context',
        cache='ui162-date-filter-context',
        suffix='date-filter-context',
        scope='Retain HR roster and handover periods and the Operations Calendar day when a filter changes.',
    )
