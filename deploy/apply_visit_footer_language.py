"""Preserve the guest's explicit Home-footer language choice across navigation."""
from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parent
once = runpy.run_path(str(BASE / 'apply_org_chart_filters.py'))['replace_once']


def home(source):
    # Keep the anchor usable with normal navigation, keyboard and a new tab.
    old = "E((location.pathname==='/__demo/native/pt'?'/':'/__demo/native/pt')+location.search+'#home')"
    return once(source, old, 'E(visitLanguageLink())').replace(
        "   host=H.root.querySelector('#personal-home');",
        """   function visitLanguageLink(){
    const url=new URL(location.href);
    const pt=url.pathname!=='/__demo/native/pt';
    url.pathname=pt?'/__demo/native/pt':'/';
    url.searchParams.set('visit_language',pt?'pt-BR':'en');
    url.hash='home';
    return url.href;
   }
   host=H.root.querySelector('#personal-home');""", 1)


def language(source):
    return once(source, '            restore: () => apply(selected()),', """            async restore() {
                const url = new URL(location.href);
                const requested = url.searchParams.get('visit_language');
                if (demo() && supported(requested) && requested === current() &&
                    url.searchParams.get('public_demo') === '1' &&
                    url.pathname === (requested === 'pt-BR' ? '/__demo/native/pt' : '/')) {
                    const workspace = state(), owner = session();
                    const previous = workspace.demoLanguage;
                    if (previous !== requested) {
                        workspace.demoLanguage = requested;
                        try { await persist(); }
                        catch (error) { workspace.demoLanguage = previous; throw error; }
                    }
                    if (session() !== owner || state() !== workspace) return true;
                    const here = new URL(location.href);
                    here.searchParams.delete('visit_language');
                    history.replaceState(history.state, '', here.href);
                }
                return apply(selected());
            },""")


def transforms():
    return {'app/static/personal_home.js': home, 'app/static/profile_language.js': language,
            'app/static/app.js': lambda s: once(s, 'if(profileLanguage.restore())return;',
                                               'if(await profileLanguage.restore())return;')}
