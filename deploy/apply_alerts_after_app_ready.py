"""Register optional alert polls only after the main application has initialized its globals."""
from pathlib import Path
import runpy
import sys


def replace_once(before, after):
    def edit(source):
        if source.count(before) != 1:
            raise ValueError('Unexpected startup anchor: ' + before)
        return source.replace(before, after)
    return edit


def transforms():
    start = """
// These modules load before the application globals used by their pollers.
// Register once per document, outside the retryable workspace-opening flow.
if (window.AJOperations) setInterval(window.AJOperations.refreshAlert, 15000);
if (window.AJAssets) setInterval(window.AJAssets.refreshAlerts, 15000);
openWorkspace();
"""
    loading = '<main id="app"><div class="loading">'
    status = '<main id="app"><div class="loading" role="status">'
    return {
        'app/static/operations.js': replace_once(' setInterval(()=>refreshAlert(),15000);\n', ''),
        'app/static/assets.js': replace_once(' setInterval(refreshAlerts,15000);\n', ''),
        'app/static/app.js': replace_once('\nopenWorkspace();\n', start),
        'app/static/index.html': replace_once(loading, status),
        'app/static/pt-BR/index.html': replace_once(loading, status),
    }


if __name__ == '__main__':
    build = Path(__file__).resolve()
    apply = runpy.run_path(str(build.with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]), parent='1eb0dc2f7030342475744f8c00299a41a408148a83a33de605a55d37a0f39922',
          overlays=(build.name,), cache=None, suffix='alert-startup',
          scope='Start existing alert polls after core initialization and announce workspace loading.')
