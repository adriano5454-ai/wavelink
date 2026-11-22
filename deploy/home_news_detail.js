  function syncDialogPhoto(holder) {
   const slot = detailDialog?.querySelector('.wl-home-news-detail-photo');
   if (!slot || slot.dataset.post !== holder.dataset.post) return;
   const photo = holder.querySelector('img');
   if (photo) slot.replaceChildren(photo.cloneNode(false));
   else slot.textContent = holder.textContent;
  }

  function makeHomeNewsCard(article, heading, post) {
   const opener = node('button', post.title, 'wl-home-news-open');
   opener.type = 'button';
   opener.setAttribute('aria-haspopup','dialog');
   heading.replaceChildren(opener);
   const read = node('span', t('Ler notícia','Read post') + ' →', 'wl-home-news-read');
   read.setAttribute('aria-hidden','true');
   article.append(read);

   article.onclick = () => {
    if (!current() || detailDialog?.open) return;
    const dialog = node('dialog', null, 'wl-home-news-dialog');
    detailDialog = dialog;
    const header = node('header', null, 'wl-home-news-detail-header');
    const audience = article.querySelector('.wl-news-audience').cloneNode(true);
    const close = node('button', t('Fechar','Close'), 'btn secondary wl-home-news-close');
    close.type = 'button';
    close.onclick = () => dialog.close();
    header.append(audience, close);
    const title = node('h2', post.title);
    title.id = 'wl-home-news-detail-title';
    title.tabIndex = -1;
    dialog.setAttribute('aria-labelledby', title.id);
    const content = node('div', null, 'wl-home-news-detail-content');
    content.append(title, article.querySelector('.wl-news-credit').cloneNode(true));
    const holder = article.querySelector('.wl-news-photo');
    if (holder) {
     const slot = node('div', null, 'wl-home-news-detail-photo');
     slot.dataset.post = post.id;
     content.append(slot);
    }
    content.append(node('p', post.body, 'wl-home-news-detail-body'));
    dialog.append(header, content);
    panel.append(dialog);
    if (holder) syncDialogPhoto(holder);
    dialog.addEventListener('close', () => {
     if (detailDialog === dialog) detailDialog = null;
     dialog.remove();
     if (current() && opener.isConnected) opener.focus({preventScroll:true});
    }, {once:true});
    opener.focus({preventScroll:true});
    dialog.showModal();
    title.focus({preventScroll:true});
   };
  }
