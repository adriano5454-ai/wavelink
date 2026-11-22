 const newsText = (pt, en) => window.WavelinkI18n?.locale === 'pt-BR' ? pt : en;
 function createNewsFeed(getHost, fmt, fleet = false) {
 let feedNewsView = null;

 function syncNewsSession() {
  if (feedNewsView && !feedNewsView.current()) feedNewsView.dispose();
 }

 function allowNewsNavigation() {
  if (!feedNewsView?.editing() || location.hash === '#team') return true;
  history.replaceState(null, '', '#team');
  getHost().toast(newsText('Publique ou cancele a notícia antes de sair.', 'Publish or cancel the news post before leaving.'));
  return false;
 }

 function mountNews(panel, compact) {
  feedNewsView?.dispose();
  const H = getHost();
  const route = location.hash || '#home';
  const session = H.session();
  const base = fleet ? '/api/fleet/news' : '/api/recognition/news';
  const t = newsText;
  let disposed = false, writing = false, request = 0, cursor = null, paged = false;
  let form = null, sites = [], retryOlder = false, previewUrl = '';
  const imageUrls = new Set();
  const current = () => !disposed && panel.isConnected && session === H.session() && route === (location.hash || '#home');
  const beforeSend = () => {
   if (!current()) throw Error('News view changed');
  };
  panel.setAttribute('aria-labelledby', 'wl-news-title');
  const heading = fleet ? t('Notícias dos seus locais', 'News from your locations') : t('Notícias da equipe','Team news');
  panel.innerHTML = `<header class="wl-news-header"><h${compact?'3':'2'} id="wl-news-title">${heading}</h${compact?'3':'2'}>
   <button type="button" class="btn secondary" id="wl-news-compose" aria-expanded="false" aria-controls="wl-news-editor" hidden>${t('Escrever notícia','Write a post')}</button></header>
   <div id="wl-news-editor"></div><p class="wl-news-status small" role="status"></p>
   <div class="wl-news-list" aria-labelledby="wl-news-title"></div>
   <button type="button" class="btn secondary" id="wl-news-more" hidden>${t('Ver notícias anteriores','Show older posts')}</button>
   <button type="button" class="btn secondary" id="wl-news-retry" hidden>${t('Tentar novamente','Try again')}</button>`;
  const find = selector => panel.querySelector(selector);
  const compose = find('#wl-news-compose'), editor = find('#wl-news-editor');
  const status = find('.wl-news-status'), list = find('.wl-news-list');
  const more = find('#wl-news-more'), retry = find('#wl-news-retry');
  if (!compact) {
   list.setAttribute('role','region');
   list.tabIndex = 0;
  }

  function releaseImages() {
   for (const url of imageUrls) URL.revokeObjectURL(url);
   imageUrls.clear();
  }

  function dispose() {
   disposed = true;
   imageObserver?.disconnect();
   releaseImages();
   clearPreview();
   form = null;
   panel.replaceChildren();
   if (feedNewsView?.dispose === dispose) feedNewsView = null;
  }

  function clearPreview() {
   if (previewUrl) URL.revokeObjectURL(previewUrl);
   previewUrl = '';
  }

  function node(tag, text, className) {
   const el = document.createElement(tag);
   if (text !== null) el.textContent = text;
   if (className) el.className = className;
   return el;
  }

  async function loadPhoto(holder) {
   if (!current() || !holder.isConnected) return;
   try {
    const blob = await H.api(base + '/' + encodeURIComponent(holder.dataset.post) + '/image', {blob:true, beforeSend});
    if (!current() || !holder.isConnected) return;
    const url = URL.createObjectURL(blob);
    imageUrls.add(url);
    const photo = document.createElement('img');
    photo.alt = holder.dataset.caption;
    photo.decoding = 'async';
    photo.src = url;
    holder.replaceChildren(photo);
   } catch {
    if (current() && holder.isConnected) holder.textContent = t('Foto indisponível.', 'Photo unavailable.');
   }
  }
  const imageObserver = typeof IntersectionObserver === 'function' ? new IntersectionObserver(entries => {
   for (const entry of entries) if (entry.isIntersecting) {
    imageObserver.unobserve(entry.target);
    loadPhoto(entry.target);
   }
  }, {rootMargin:'160px'}) : null;

  function appendPost(post) {
   const article = node('article', null, 'wl-news-post');
   const heading = node(compact ? 'h4' : 'h3', post.title);
   const audience = node('span', post.site_id ? post.site_name : t('Toda a empresa','Company-wide'), 'wl-news-audience');
   const timestamp = node('time', fmt(post.created_at));
   timestamp.dateTime = post.created_at;
   const credit = node('p', null, 'wl-news-credit');
   credit.append(node('span', post.author_name), timestamp);
   const copy = node('p', post.body, 'wl-news-copy');
   article.append(audience, heading, credit, copy);
   list.append(article);
   if (post.has_image) {
    const holder = node('div', t('Carregando foto…','Loading photo…'), 'wl-news-photo');
    holder.dataset.post = post.id;
    holder.dataset.caption = t('Foto da notícia','Photo for') + ' “' + post.title + '”';
    article.append(holder);
    if (imageObserver) imageObserver.observe(holder);
    else loadPhoto(holder);
   }
  }

  function closeEditor(focus) {
   form = null;
   clearPreview();
   editor.replaceChildren();
   compose.setAttribute('aria-expanded', 'false');
   if (focus && !compose.hidden) compose.focus();
  }

  function openEditor() {
   if (fleet || !current() || form || compose.hidden) return;
   editor.innerHTML = `<form class="wl-news-form"><fieldset>
    <legend>${t('Nova notícia','New post')}</legend>
    <label>${t('Título','Headline')}<input name="title" required maxlength="140"></label>
    <label>${t('Mensagem','Message')}<textarea name="body" required maxlength="3000" rows="4"></textarea></label>
    <label>${t('Público','Audience')}<select name="site" required></select></label>
    <label>${t('Foto (opcional)','Photo (optional)')}<input type="file" name="photo" accept="image/jpeg,image/png,image/webp" aria-describedby="wl-news-photo-help"></label>
    <small id="wl-news-photo-help">${t('JPEG, PNG ou WebP de até 5 MB.','JPEG, PNG or WebP up to 5 MB.')}</small>
    <div class="wl-news-photo" data-news-preview hidden></div>
    <div class="wl-news-actions"><button type="submit" class="btn">${t('Publicar','Publish')}</button>
    <button type="button" class="btn secondary" data-news-cancel>${t('Cancelar','Cancel')}</button></div>
    </fieldset><p class="wl-news-status small" role="status"></p></form>`;
   form = editor.querySelector('form');
   const {title, body, site, photo} = form.elements;
   const formStatus = form.querySelector('[role="status"]');
   const fieldset = form.querySelector('fieldset');
   const preview = form.querySelector('[data-news-preview]');
   const validPhoto = f => f.size > 0 && f.size <= 5*1024*1024 && ['image/jpeg','image/png','image/webp'].includes(f.type);
   photo.onchange = () => {
    clearPreview();
    preview.replaceChildren();
    const file = photo.files[0];
    preview.hidden = !file || !validPhoto(file);
    if (!preview.hidden) {
     const img = document.createElement('img');
     img.alt = t('Prévia da foto selecionada','Selected photo preview');
     img.src = previewUrl = URL.createObjectURL(file);
     preview.append(img);
    }
   };
   site.append(new Option(t('Selecione o público','Choose an audience'), ''), new Option(t('Toda a empresa','Everyone in the company'), 'all'));
   const kindNames = {vessel:t('Embarcação','Vessel'), shore_base:t('Base','Base'),
    warehouse:t('Armazém','Warehouse'), workshop:t('Oficina','Workshop')};
   for (const place of sites) {
    const kind = kindNames[place.kind];
    site.append(new Option(kind ? place.name + ' · ' + kind : place.name, place.id));
   }
   let operation = null;
   form.oninput = () => {
    for (const input of [title, body, photo]) input.setCustomValidity('');
    operation = null;
    formStatus.textContent = '';
   };
   form.querySelector('[data-news-cancel]').onclick = () => closeEditor(true);
   compose.setAttribute('aria-expanded', 'true');
   title.focus();
   form.onsubmit = async event => {
    event.preventDefault();
    if (!current() || writing) return;
    const file = photo.files[0];
    const required = t('Preencha este campo.','Fill in this field.');
    title.setCustomValidity(title.value.trim() ? '' : required);
    body.setCustomValidity(body.value.trim() ? '' : required);
    photo.setCustomValidity(file && !validPhoto(file)
     ? t('Escolha uma foto JPEG, PNG ou WebP de até 5 MB.','Choose a JPEG, PNG or WebP photo up to 5 MB.') : '');
    if (!form.reportValidity()) return;
    writing = true;
    fieldset.disabled = true;
    formStatus.textContent = t('Publicando…','Publishing…');
    try {
     const image = file ? await new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject(Error(t('Não foi possível ler a foto.','The photo could not be read.')));
      reader.readAsDataURL(file);
     }) : null;
     beforeSend();
     operation ||= H.uid();
     await H.api(base, {method:'POST', timeout:60000, beforeSend,
      body:{op_id:operation, title:title.value.trim(), body:body.value.trim(), site_id:site.value === 'all' ? null : site.value, image}});
     if (!current()) return;
     closeEditor(true);
     await refresh(false, t('Notícia publicada.','Post published.'));
    } catch (error) {
     if (current() && form) {
      formStatus.textContent = t('Não foi possível confirmar a publicação.','Publication could not be confirmed.') + ' ' + H.message(error);
     }
    } finally {
     writing = false;
     fieldset.disabled = false;
    }
   };
  }

  async function refresh(older = false, notice = '') {
   if (!current() || (older && !cursor)) return;
   const token = ++request;
   status.textContent = t('Carregando notícias…', 'Loading news…');
   more.disabled = true;
   retry.hidden = true;
   try {
    const result = await H.api(base + '?limit=' + (compact ? 1 : 6) + (older ? '&before=' + encodeURIComponent(cursor) : ''), {beforeSend});
    if (token !== request || !current()) return;
    if (!Array.isArray(result.posts)) throw Error('Invalid news response');
    if (!older) {
     imageObserver?.disconnect();
     releaseImages();
     list.replaceChildren();
     list.scrollTop = 0;
    }
    for (const post of result.posts) appendPost(post);
    cursor = result.next_cursor;
    paged = older;
    more.hidden = compact || !cursor;
    sites = result.sites || [];
    compose.hidden = fleet || compact || !result.can_publish || !!window.WavelinkNativeDemo?.active();
    if (compose.hidden && form) closeEditor(false);
    status.textContent = notice || (list.firstElementChild ? '' : t('Nenhuma notícia para você por enquanto.','No news for you yet.'));
    if (compact && !list.firstElementChild) panel.hidden = true;
   } catch (error) {
    if (token !== request || !current()) return;
    if ([401,403].includes(Number(error?.status))) {panel.hidden = true; dispose(); return;}
    retryOlder = older;
    retry.hidden = false;
    status.textContent = [notice, t('Não foi possível carregar as notícias.', 'News could not be loaded.')].filter(Boolean).join(' ');
   } finally {
    if (token === request && current()) more.disabled = false;
   }
  }
  compose.onclick = () => { if (form) form.elements.title.focus(); else openEditor(); };
  more.onclick = () => refresh(true);
  retry.onclick = () => refresh(retryOlder);
  feedNewsView = {current, dispose, editing:() => !!form, saving:() => writing,
   keepOpen:() => current() && !compact && (form || writing || paged || list.scrollTop > 0 || panel.contains(document.activeElement))};
  return refresh;
 }
 return {mount:mountNews, sync:syncNewsSession, allowNavigation:allowNewsNavigation,
  dispose:() => feedNewsView?.dispose(), editing:() => !!feedNewsView?.editing(),
  saving:() => !!feedNewsView?.saving(), keepOpen:() => !!feedNewsView?.keepOpen()};
 }
