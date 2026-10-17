"""Run the selected UI120 checks against a separately reconstructed runtime."""
from pathlib import Path
import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runtime', type=Path, help='Runtime created by deploy/materialize_runtime.py')
    parser.add_argument('--collect-only', action='store_true')
    parser.add_argument('--junitxml', type=Path)
    args = parser.parse_args()
    source = args.runtime.resolve()
    repository = Path(__file__).resolve().parents[1]
    if not (source / 'app/hr_workspace.py').is_file():
        parser.error('Expected a reconstructed UI120 runtime, not the deployment repository.')
    sys.path[:0] = [str(source), str(repository), str(repository / 'tests')]
    os.environ['WAVELINK_TEST_SOURCE'] = str(source)
    os.environ['WAVELINK_TEST_REPO'] = str(repository)
    os.environ['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    sys.dont_write_bytecode = True
    import pytest
    runtime_tests = [
        'tests/test_hr_ui117.py',
        'tests/test_hr_integration_ui117.py',
        'tests/test_hr_ui120.py',
        'tests/test_hr_backup_ui117.py',
        'tests/ui82_search_actions/test_search_actions.py',
        'tests/ui65_roles_access/test_roles_access.py',
        'tests/ui58_shift_permissions/test_permissions.py',
    ]
    selected = [str(source / name) for name in runtime_tests]
    selected.append(str(repository / 'tests/test_password_policy_ui119.py'))
    selected += ['-q', '-p', 'no:cacheprovider']
    if args.collect_only:
        selected.append('--collect-only')
    if args.junitxml:
        selected.append('--junitxml=' + str(args.junitxml.resolve()))
    return pytest.main(selected)


if __name__ == '__main__':
    raise SystemExit(main())
