 const birthdayHomes = new WeakMap();

 function birthdayCurrent(panel,ticket,session) {
  return panel.isConnected && ticket === epoch && session === owner && session === H.session();
 }

 function birthdayDate(month, day, format) {
  const locale = window.WavelinkI18n?.locale === 'pt-BR' ? 'pt-BR' : 'en-GB';
  return new Intl.DateTimeFormat(locale,{...format,timeZone:'UTC'}).format(new Date(Date.UTC(2000,month-1,day)));
 }

 function mountTeamBirthdays(panel,ticket,session) {
  const t = newsText;
  panel.innerHTML = `<h2 id="wl-birthday-title">${t('Aniversários','Birthdays')}</h2>
   <p class="wl-birthday-period">${t('Nos próximos 30 dias','In the next 30 days')}</p>
   <ul class="wl-birthday-list"></ul><p role="status" class="wl-birthday-status"></p>
   <div class="wl-birthday-actions"><button type="button" data-prev hidden>${t('Anteriores','Previous')}</button>
   <button type="button" data-next hidden>${t('Próximos','Next')}</button>
   <button type="button" data-retry hidden>${t('Tentar novamente','Try again')}</button></div>`;
  const list = panel.querySelector('ul'), status = panel.querySelector('[role=status]');
  const previous = panel.querySelector('[data-prev]'), next = panel.querySelector('[data-next]');
  const retry = panel.querySelector('[data-retry]');
  const limit = 6;
  let offset = 0;

  async function refresh(start) {
   previous.disabled = next.disabled = true;
   retry.hidden = true;
   status.textContent = t('Carregando…','Loading…');
   try {
    const data = await H.api('/api/recognition/birthdays?limit='+limit+'&offset='+start);
    if (!birthdayCurrent(panel,ticket,session)) return;
    if (start && !data.items.length) return refresh(0);
    offset = start;
    list.replaceChildren();
    for (const member of data.items) {
     const item = document.createElement('li');
     const name = document.createElement('span');
     name.textContent = member.name;
     const date = document.createElement('span');
     const label = birthdayDate(member.month,member.day,{day:'numeric',month:'short'});
     date.textContent = member.days_until === 0 ? t('Hoje','Today')+' · '+label : label;
     if (member.days_until === 0) date.classList.add('wl-birthday-today');
     item.append(name,date);
     list.append(item);
    }
    previous.hidden = start === 0;
    next.hidden = start + data.items.length >= data.total;
    status.textContent = data.items.length ? '' : t('Nenhum aniversário compartilhado neste período.','No shared birthdays in this period.');
   } catch (error) {
    if (!birthdayCurrent(panel,ticket,session)) return;
    list.replaceChildren();
    next.hidden = previous.hidden = true;
    if ([401,403].includes(error?.status)) {panel.hidden=true;return;}
    status.textContent = t('Não foi possível carregar os aniversários.','Birthdays could not be loaded.');
    retry.hidden = false;
    retry.onclick = () => refresh(start);
   } finally {
    previous.disabled = next.disabled = false;
   }
  }
  previous.onclick = () => refresh(Math.max(0,offset-limit));
  next.onclick = () => refresh(offset+limit);
  refresh(0);
 }

 function mountBirthdayPreference(panel,ticket,session) {
  const t = newsText;
  const demo = !!window.WavelinkNativeDemo?.active();
  panel.innerHTML = `<h2>${t('Meu aniversário','My birthday')}</h2>
   <p>${t('Compartilhe o dia e o mês com a equipe para aparecer na lista de aniversários.','Share your day and month to appear in Team birthdays.')}</p>
   <form hidden><div class="wl-birthday-fields">
   <label>${t('Dia','Day')}<select name="birth_day" required></select></label>
   <label>${t('Mês','Month')}<select name="birth_month" required></select></label></div>
   <div class="wl-birthday-actions"><button class="btn" data-birthday-save type="submit">${t('Compartilhar aniversário','Share birthday')}</button>
   <button class="btn secondary" data-birthday-remove type="button" hidden>${t('Remover da lista','Remove from birthdays')}</button></div></form>
   <p class="wl-birthday-status" role="status"></p><button type="button" class="btn secondary" data-retry hidden>${t('Tentar novamente','Try again')}</button>`;
  const form = panel.querySelector('form'), status = panel.querySelector('[role=status]');
  const day = form.elements.birth_day, month = form.elements.birth_month;
  const remove = form.querySelector('[data-birthday-remove]'), save = form.querySelector('[data-birthday-save]');
  const retry = panel.querySelector('[data-retry]');
  let version;
  month.add(new Option('—',''));
  for (let m=1; m<=12; m++) month.add(new Option(birthdayDate(m,1,{month:'long'}),String(m)));
  function days() {
   const old = day.value;
   const count = month.value ? new Date(Date.UTC(2000,Number(month.value),0)).getUTCDate() : 31;
   day.replaceChildren(new Option('—',''));
   for (let d=1; d<=count; d++) day.add(new Option(String(d),String(d)));
   if (Number(old)<=count) day.value = old;
  }
  function show(record,message) {
   version = record.version;
   month.value = record.month ? String(record.month) : '';
   days();
   day.value = record.day ? String(record.day) : '';
   remove.hidden = !record.month;
   save.textContent = record.month ? t('Salvar alteração','Save change') : t('Compartilhar aniversário','Share birthday');
   status.textContent = message || (record.month ? t('Visível na lista da equipe.','Shared with the team.') : t('Você ainda não compartilhou seu aniversário.','Your birthday is private.'));
   form.hidden = false;
  }
  async function read(message) {
   retry.hidden = true;
   try {
    const record = await H.api('/api/recognition/birthday');
    if (birthdayCurrent(panel,ticket,session)) show(record,message);
   } catch(error) {
    if (!birthdayCurrent(panel,ticket,session)) return;
    form.hidden = true;
    if ([401,403].includes(error?.status)) {panel.hidden=true;return;}
    retry.hidden = false;
    status.textContent = t('Não foi possível carregar a preferência.','Could not load your preference.');
   }
  }
  async function write(clear) {
   if (save.disabled || demo || !birthdayCurrent(panel,ticket,session)) return;
   const body = {version,day:clear?null:Number(day.value),month:clear?null:Number(month.value)};
   month.disabled = day.disabled = save.disabled = remove.disabled = true;
   try {
    await H.api('/api/recognition/birthday',{method:'POST',body});
    if (birthdayCurrent(panel,ticket,session)) await read(clear ? t('Aniversário removido da lista.','Birthday removed from the list.') : t('Aniversário compartilhado com a equipe.','Birthday shared with the team.'));
   } catch(error) {
    if (!birthdayCurrent(panel,ticket,session)) return;
    if (error?.status===409) await read(t('Sua preferência mudou. Confira os dados atuais.','Your preference changed. Check the current setting.'));
    else status.textContent = H.message(error);
   } finally {
    month.disabled = day.disabled = save.disabled = remove.disabled = false;
   }
  }
  month.onchange = days;
  form.onsubmit = event => {event.preventDefault();if (form.reportValidity()) write(false);};
  remove.onclick = () => write(true);
  retry.onclick = () => read();
  if (demo) status.textContent = t('Preferência disponível em sua conta pessoal. A demonstração é somente leitura.','Available in your personal account. The public demo is read-only.');
  else read();
 }
