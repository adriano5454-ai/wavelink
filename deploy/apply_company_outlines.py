"""Use stronger neutral edges for signed-in company accounts, in each component's original cascade."""
from pathlib import Path
import re
import runpy
import sys

BASE = Path(__file__).resolve().parent
PARENT = "e1d08c1b3dc94bbaa581b603b329f025c1cb1f51d8f22f689e8a6e69dc3122fa"

TOKENS = """
@media screen and (forced-colors: none) {
  .wl-company-account #app {
    --wl-company-control-edge: #788f9b;
    --wl-company-panel-edge: #9cb1bc;
    --wl-company-divider: #aebfc9;
  }
  .wl-company-account #app :where(:disabled, [aria-disabled=true], [aria-invalid=true]) {
    --wl-company-control-edge: initial;
  }
}
"""


def company_class(source):
    start = "function workspaceNav(){\n"
    if source.count(start) != 1:
        raise ValueError("Unexpected workspace navigation initializer")
    # workspace_brand comes from the server's operator-selected COMPANY identity.
    # Hub IDs bind it to the current named account, including after a workspace switch.
    return source.replace(start, start + """    const companyAccount = Boolean(workspaceReady && !workspaceIssue && !mismatch && !storageFailed && !disposed
        && state.info?.workspace_brand?.id && state.auth?.person?.user_id && state.auth.token && !state.publicDemoUserId
        && state.hub_id && state.hub_id === state.info.hub_id && state.hub_id === state.auth.hub_id);
    document.body?.classList?.toggle('wl-company-account', companyAccount);
""")


def borders(*rules, tokens=False):
    def edit(source):
        for selector, declaration, color, token in rules:
            # Replace only the neutral declaration. Existing state and responsive
            # selectors keep their specificity, priority, widths and other colors.
            pattern = re.escape(selector) + r'\s*\{[^{}]*?' + re.escape(declaration + color)
            matches = list(re.finditer(pattern, source))
            if len(matches) != 1:
                raise ValueError(f"Unexpected border in {selector}: {declaration}{color}")
            end = matches[0].end()
            source = source[:end - len(color)] + f"var(--wl-company-{token},{color})" + source[end:]
        return source + TOKENS if tokens else source
    return edit


def transforms():
    app = 'body.wl-ui124 #app '
    home = 'body.wl-ui124 #personal-home '
    table = app + ':is(table:not(.calendar),.hr-data-table) '
    return {
        'app/static/app.js': company_class,
        'app/static/visual_ui124.css': borders(
            (app + ':is(.btn.secondary,.btn.ghost,.wl-secondary)', 'border:1px solid ', '#bbcdd5', 'control-edge'),
            (app + ':is(.wl-field-control,input:not([type=checkbox]):not([type=radio]):not([type=hidden]),select,textarea)',
             'border:1px solid ', '#b5c7d0', 'control-edge'),
            (app + ':is(.card,.hr-panel,.ph-content,.ph-profile-quick,.wl-home-team,.mw-selected,.mw-controls,.inv-panel)',
             'border:1px solid ', '#dce4e8', 'panel-edge'),
            (app + ':is(.home-destination,.tw110-register,.tw110-detail,.cw-record,.hwd-day,.hwd-record,.sb-card,.fr-row,.qs-row,.of-folders)',
             'border-color:', '#dce4e8', 'panel-edge'),
            (app + ':is(.home-group-filters button,.wl-filter-chip)', 'border:1px solid ', '#dce4e8', 'control-edge'),
            (home + '.ph-metric', 'border:1px solid ', '#dce4e8', 'panel-edge'),
            (home + '.ux-workspace-shortcuts a', 'border:1px solid ', '#dce4e8', 'panel-edge'),
            (home + '.ph-row', 'border-bottom:1px solid ', '#dce4e8', 'divider'),
            (table + 'th', 'border-bottom:1px solid ', '#cbdbe2', 'panel-edge'),
            (table + 'td', 'border-bottom:1px solid ', '#e3ebef', 'divider'),
            tokens=True),
        'app/static/experience_ui123.css': borders(
            ('body.wl-ui121 #app #hr-workspace .hr-panel', 'border:1px solid ', '#ccdae1', 'panel-edge')),
        'app/static/documentos_context.css': borders(
            ('.wl-context-document', 'border:1px solid ', '#b8cdd7', 'panel-edge')),
        'app/static/ui131_visual.css': borders(
            ('.wl-context-documents>header', 'border-bottom:1px solid ', 'var(--wl131-border)', 'divider'),
            ('.wl-context-documents .wl-context-document-details', 'border-block:1px solid ', 'var(--wl131-border)', 'divider')),
    }


if __name__ == '__main__':
    apply = runpy.run_path(str(BASE / 'apply_editor_exit.py'))['apply']
    apply(Path(sys.argv[1]), parent=PARENT, overlays=(Path(__file__).name,),
          previous_cache='ui162-company-toolbox-navigation', cache='ui162-company-outlines-toolbox', suffix='company-outlines',
          scope='Distinguish neutral controls, panel edges and dividers for signed-in company accounts.')
