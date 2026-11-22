"""Install the local vessel filter in the main application and Fleet workspace."""
from pathlib import Path


def transforms():
    script = Path(__file__).with_name('page_vessel_filter.js').read_text(encoding='utf-8')
    css = '''
.wl-page-vessel {display:grid; align-content:start; gap:.25rem; min-width:0; max-width:100%;}
.wl-page-vessel>label {display:grid; gap:.25rem; min-width:0; margin:0;}
.wl-page-vessel>label>span {font-size:.875rem; font-weight:650;}
.wl-page-vessel select {width:100%; min-width:0; max-width:100%; min-height:40px;}
.wl-page-vessel-status {font-size:.8rem; color:var(--muted,#465d67);}
.wl-page-vessel [hidden] {display:none!important;}
.wl-page-vessel-retry {justify-self:start;}
'''
    return {'app/static/action_center_ui82.js': lambda source: script + '\n' + source,
            'app/static/fleet.js': lambda source: script + '\n' + source,
            'app/static/ui132_visual.css': lambda source: source + '\n' + css}
