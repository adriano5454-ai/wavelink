"""Add audience-aware news to Team and the existing Home updates panel."""
from pathlib import Path


def _once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f"Unexpected recognition workspace at {old!r}")
    return source.replace(old, new, 1)


def _recognition(source):
    script = Path(__file__).with_suffix(".js").read_text(encoding="utf-8")
    substitutions = [
        (" function syncSession(){", script + "\n const news = createNewsFeed(() => H, fmt);\n function syncSession(){news.sync();"),
        ("if(teamMoodPanel?.keepOpen()) return;",
         "if(teamMoodPanel?.keepOpen() || news.keepOpen()) return;"),
        ("function hasForm(){return ", "function hasForm(){return news.editing()||"),
        ("function exitBusy(){return ", "function exitBusy(){return news.saving()||"),
        ("function guardRoute(){", "function guardRoute(){if(!news.allowNavigation())return false;"),
        ("__wl118.t('TEAM / RECENT ACCOMPLISHMENTS')", "__wl118.t('TEAM')"),
        ("__wl118.t('Shareable accomplishments and colleagues that your current access allows you to see.')",
         "newsText('Notícias, conquistas e pessoas da sua equipe.', 'News, accomplishments and people on your team.')"),
        ("${moodPanel()}<section", '${moodPanel()}<section id="wl-news" class="card wl-news"></section><section'),
        ("  const refreshMoods=mountTeamMoods",
         "  const refreshNews=news.mount(content.querySelector('#wl-news'),false);\n  const refreshMoods=mountTeamMoods"),
        ("[refresh(),refreshMoods()]", "[refresh(),refreshMoods(),refreshNews()]"),
        ("[refresh(),refreshMoods(),mountPeopleDirectory", "[refresh(),refreshMoods(),refreshNews(),mountPeopleDirectory"),
        ("<p>Recent accomplishments you may currently see.</p>",
         "<p>${E(newsText('Notícias e conquistas recentes da equipe.', 'News and recent team accomplishments.'))}</p>"),
        ('</header><div class="wl-feed-list"></div>',
         '</header><section id="wl-news" class="wl-news wl-news-compact"></section><div class="wl-feed-list"></div>'),
        ("   panel.querySelector('#wl-home-refresh').onclick=",
         "   news.mount(panel.querySelector('#wl-news'),true)();\n   panel.querySelector('#wl-home-refresh').onclick="),
    ]
    for old, new in substitutions:
        source = _once(source, old, new)
    return source


def _fleet(source):
    script = Path(__file__).with_suffix(".js").read_text(encoding="utf-8")
    host = """
const fleetNews = createNewsFeed(() => ({
 session:saveSession,
 api:async (path, {blob, beforeSend}) => {
  beforeSend();
  const result = await api(path,{binary:!!blob});
  return blob ? result.blob() : result;
 }
}), journeyTime, true);
"""
    source = _once(source, "function beginPage(key){", script + host + "function beginPage(key){fleetNews.dispose();")
    source = _once(source, "async function loginPage(){", "async function loginPage(){fleetNews.dispose();")
    source = _once(source, '<div class="grid fleet77-site-grid">',
                   """${auth?.person?.fleet_mode==='vessel_only'?'<section id="wl-news" class="card fleet77-card wl-news"></section>':''}<div class="grid fleet77-site-grid">""")
    return _once(source, " on('add-site',()=>siteForm());",
                 " if($('wl-news')) fleetNews.mount($('wl-news'),false)();\n on('add-site',()=>siteForm());")


def transforms():
    styles = Path(__file__).with_suffix(".css").read_text(encoding="utf-8")
    return {
        "app/static/recognition_workspace.js": _recognition,
        "app/static/recognition_workspace.css": lambda source: source + "\n" + styles,
        "app/static/fleet.js": _fleet,
        "app/static/fleet_workspace_ui78.css": lambda source: source + "\n" + styles,
    }
