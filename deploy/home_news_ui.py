"""Feature the most recent visible news on Home and open it in place."""
from pathlib import Path


def _once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f"Unexpected Home news source at {old!r}")
    return source.replace(old, new, 1)


def _home(source):
    start = "${shortcuts(management)}${(H.brand?.()?.id==='corcovado' || window.WavelinkNativeDemo?.active())?"
    source = _once(source, start,
                   '<section id="wl-news" class="card wl-news wl-news-compact"></section>'
                   + start.removeprefix("${shortcuts(management)}"))
    source = _once(source, '''<div id="ph-home-moods"></div>':''}<div id="ph-local">''',
                   '''<div id="ph-home-moods"></div>':''}${shortcuts(management)}<div id="ph-local">''')
    source = _once(source, "host.querySelector('#ph-refresh').onclick=guard(()=>refresh(true));",
                   "host.querySelector('#ph-refresh').onclick=guard(()=>{refresh(true);window.AJRecognition?.refreshHomeNews();});")
    return _once(source, "document.addEventListener('close',()=>{closing++;},true);",
                 "document.addEventListener('close',e=>{if(!e.target.matches?.('.wl-home-news-dialog'))closing++;},true);")


def _recognition(source):
    detail = Path(__file__).with_name("home_news_detail.js").read_text(encoding="utf-8")
    substitutions = [
        ('<section id="wl-news" class="wl-news wl-news-compact"></section>', ''),
        ("   news.mount(panel.querySelector('#wl-news'),true)();", ""),
        ("<p>${E(newsText('Notícias e conquistas recentes da equipe.', 'News and recent team accomplishments.'))}</p>",
         "<p>Recent accomplishments you may currently see.</p>"),
        ("  const profileNode=home.querySelector", """  const featured=home.querySelector('#wl-news');
  if(featured) news.mount(featured,true)();
  const profileNode=home.querySelector"""),
        ("return {init,handles,open,mountHome,syncSession,",
         "return {init,handles,open,mountHome,refreshHomeNews:()=>news.refreshHome(),syncSession,"),
        (" function mountNews(panel, compact) {", """ function mountNews(panel, compact) {
  if(compact && feedNewsView?.panel===panel && feedNewsView.current()) return feedNewsView.refreshHome;"""),
        ("  const imageUrls = new Set();", """  let detailDialog = null, lastHomeRead = null, homeRead = null;
  let homePage = 0, retryPage = 0;
  const homeCursors = [null];
  const imageUrls = new Set();"""),
        ('  panel.setAttribute(\'aria-labelledby\', \'wl-news-title\');',
         """  panel.hidden = false;
  panel.setAttribute('aria-labelledby', 'wl-news-title');"""),
        ("<h${compact?'3':'2'} id=\"wl-news-title\">${heading}</h${compact?'3':'2'}>",
         """<h2 id="wl-news-title">${heading}</h2>
   ${compact?`<a class="wl-home-news-all" href="#team">${t('Ver todas as notícias','View all news')}</a>`:''}"""),
        ('<button type="button" class="btn secondary" id="wl-news-more"', """
   ${compact?`<nav class="wl-home-news-pages" aria-label="${t('Navegar pelas notícias','Browse news')}" hidden>
    <button type="button" class="btn secondary" id="wl-home-news-newer">${t('Notícia mais recente','Newer post')}</button>
    <button type="button" class="btn secondary" id="wl-home-news-older">${t('Notícia anterior','Older post')}</button>
   </nav>`:''}
   <button type="button" class="btn secondary" id="wl-news-more" """.rstrip()),
        ("  if (!compact) {", """  const homePager = find('.wl-home-news-pages');
  function paintHomePager(busy = false) {
   if (!homePager) return;
   homePager.hidden = homeCursors.length === 1;
   find('#wl-home-news-newer').disabled = busy || homePage === 0;
   find('#wl-home-news-older').disabled = busy || homePage + 1 >= homeCursors.length;
  }
  if (!compact) {"""),
        ("   disposed = true;", """   disposed = true;
   if(detailDialog?.open) detailDialog.close();"""),
        ("  function appendPost(post) {", detail + "\n  function appendPost(post) {"),
        ("const heading = node(compact ? 'h4' : 'h3', post.title);", "const heading = node('h3', post.title);"),
        ("   list.append(article);",
         """   if (compact) makeHomeNewsCard(article, heading, post);
   list.append(article);"""),
        ("    holder.replaceChildren(photo);", """    holder.replaceChildren(photo);
    if (compact) syncDialogPhoto(holder);"""),
        ("    if (current() && holder.isConnected) holder.textContent = t('Foto indisponível.', 'Photo unavailable.');",
         """    if (current() && holder.isConnected) {
     holder.textContent = t('Foto indisponível.', 'Photo unavailable.');
     if (compact) syncDialogPhoto(holder);
    }"""),
        ("    if (imageObserver) imageObserver.observe(holder);",
         "    if (!compact && imageObserver) imageObserver.observe(holder);"),
        ("  async function refresh(older = false, notice = '') {",
         "  async function refresh(older = false, notice = '', page = homePage) {"),
        ("   const token = ++request;", "   const token = ++request;\n   if (compact) paintHomePager(true);"),
        ("   status.textContent = t('Carregando notícias…', 'Loading news…');",
         """   if (!compact || !list.firstElementChild) status.textContent = t('Carregando notícias…', 'Loading news…');"""),
        ("    const result = await H.api(base + '?limit=' + (compact ? 1 : 6) + (older ? '&before=' + encodeURIComponent(cursor) : ''), {beforeSend});",
         """    const before = compact ? homeCursors[page] : older && cursor;
    const result = await H.api(base + '?limit=' + (compact ? 1 : 6) + (before ? '&before=' + encodeURIComponent(before) : ''), {beforeSend});"""),
        ("    if (!Array.isArray(result.posts))", """    if (compact && (detailDialog?.open || (page === homePage && list.contains(document.activeElement)))) return;
    if (!Array.isArray(result.posts))"""),
        ("    if (compact && !list.firstElementChild) panel.hidden = true;", """    if (compact) {
     if (page > 0 && !result.posts.length) return refresh(false,'',0);
     const changed = homePage !== page;
     homePage = page;
     homeCursors.splice(page + 1);
     if (result.next_cursor) homeCursors.push(result.next_cursor);
     if (changed && current()) list.querySelector('.wl-home-news-open')?.focus({preventScroll:true});
    }"""),
        ("    retryOlder = older;", """    if (compact && page > 0 && Number(error?.status) === 422) {
     homePage = 0;
     homeCursors.splice(1);
     releaseImages();
     list.replaceChildren();
     return refresh(false,'',0);
    }
    retryPage = page;
    retryOlder = older;"""),
        ("    if (token === request && current()) more.disabled = false;",
         """    if (token === request && current()) {
     more.disabled = false;
     if (compact) paintHomePager();
    }"""),
        ("  retry.onclick = () => refresh(retryOlder);",
         """  retry.onclick = () => compact ? refreshHome(true,retryPage) : refresh(retryOlder);
  if (homePager) {
   find('#wl-home-news-newer').onclick = () => refreshHome(true,homePage - 1);
   find('#wl-home-news-older').onclick = () => refreshHome(true,homePage + 1);
  }"""),
        ("  feedNewsView = {current, dispose,",
         """  function refreshHome(force = false, page = homePage) {
   if (!compact || !current() || detailDialog?.open || (!force && list.contains(document.activeElement))) return;
   if (page < 0 || page >= homeCursors.length) return;
   if (homeRead) return homeRead;
   if (!force && lastHomeRead !== null && Date.now() - lastHomeRead < 30000) return;
   lastHomeRead = Date.now();
   homeRead = refresh(false,'',page).finally(() => { homeRead = null; });
   return homeRead;
  }
  feedNewsView = {panel, current, dispose, refreshHome,"""),
        ("  return refresh;\n }\n return {mount:mountNews",
         "  return compact ? refreshHome : refresh;\n }\n return {refreshHome:() => feedNewsView?.refreshHome(true), mount:mountNews"),
    ]
    for old, new in substitutions:
        source = _once(source, old, new)
    return source


def transforms():
    styles = Path(__file__).with_name("home_news_ui.css").read_text(encoding="utf-8")
    return {"app/static/personal_home.js": _home,
            "app/static/recognition_workspace.js": _recognition,
            "app/static/recognition_workspace.css": lambda source: source + "\n" + styles}
