"""Release the Team news editor when its author leaves or its view is gone."""


def _once(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f"Unexpected Team news editor at {old!r}")
    return source.replace(old, new, 1)


def _recognition(source):
    before = """ function allowNewsNavigation() {
  if (!feedNewsView?.editing() || location.hash === '#team') return true;
  history.replaceState(null, '', '#team');
  getHost().toast(newsText('Publique ou cancele a notícia antes de sair.', 'Publish or cancel the news post before leaving.'));
  return false;
 }"""
    source = _once(source, before, """ function allowNewsNavigation(nextHash = location.hash || '#home') {
  return feedNewsView?.prepareLeave(nextHash) ?? true;
 }""")
    source = _once(source, "if (feedNewsView && !feedNewsView.current()) feedNewsView.dispose();",
                   "if (feedNewsView && !feedNewsView.current() && !feedNewsView.editing()) feedNewsView.dispose();")
    source = _once(source, "  function closeEditor(focus) {", """
  function editing() {
   return Boolean(!disposed && session === H.session() && form?.isConnected && panel.contains(form));
  }

  function prepareLeave(nextHash) {
   if (!form) return true;
   if (!editing()) {
    dispose();
    return true;
   }
   if (nextHash === route) return true;
   if (writing) {
    if (window.AJEditorNavigation?.wait) return window.AJEditorNavigation.wait();
    H.toast(t('Aguarde a publicação da notícia.', 'Wait for the post to finish publishing.'));
    return false;
   }
   const {title, body, site, photo} = form.elements;
   const dirty = title.value || body.value || site.value || photo.files?.length;
   if (dirty && !window.confirm(t('Descartar esta notícia não publicada e sair da página?', 'Discard this unpublished post and leave the page?'))) {
    return false;
   }
   closeEditor(false);
   return true;
  }

  function closeEditor(focus) {""")
    source = _once(source, "   let operation = null;",
                   """   const activeForm = form;
   function beforePublish() {
    beforeSend();
    if (form !== activeForm || !editing()) throw Error('News editor changed');
   }
   let operation = null;""")
    source = _once(source, "   form.querySelector('[data-news-cancel]').onclick = () => closeEditor(true);",
                   "   form.querySelector('[data-news-cancel]').onclick = () => { if (!writing) closeEditor(true); };")
    source = _once(source, "    if (!current() || writing) return;",
                   "    if (!current() || !editing() || form !== activeForm || writing) return;")
    source = _once(source, "     beforeSend();\n     operation ||=", "     beforePublish();\n     operation ||=")
    source = _once(source, "{method:'POST', timeout:60000, beforeSend,",
                   "{method:'POST', timeout:60000, beforeSend:beforePublish,")
    source = _once(source, "refreshHome, editing:() => !!form, saving:() => writing,",
                   "refreshHome, prepareLeave, editing, saving:() => editing() && writing,")
    source = _once(source, "if(!news.allowNavigation())return false;",
                   "if(!news.allowNavigation()){history.replaceState(history.state,'','#team');return false;}")
    return _once(source, "return {init,handles,open,mountHome,refreshHomeNews:",
                 "return {init,handles,open,mountHome,prepareNewsLeave:news.allowNavigation,hasNewsEditor:news.editing,refreshHomeNews:")


def transforms():
    return {"app/static/recognition_workspace.js": _recognition}
