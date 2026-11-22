    let savedChecks = null;
    const panelText = (en, pt) => window.WavelinkUX.text(pt, en);
    const checksPerPage = 8;

    function ownsPreview(request) {
      return savedChecks === request && request.session === ctx.session() && active() &&
        prefs.detail && prefs.selected === request.id &&
        allowed().some(row => row.id === request.id && row.version === request.version);
    }

    async function readChecks(request) {
      try {
        const record = await ctx.readSaved(request.id, () => {
          if (!ownsPreview(request)) throw Error('Checklist selection changed');
        });
        if (!ownsPreview(request)) return;
        if (record?.deleted) throw Object.assign(Error(), {status:410});
        if (record?.id !== request.id || !Number.isSafeInteger(record.version) || record.version < request.version ||
            !Array.isArray(record.template?.sections) || !record.meta || !record.items || !phases(record).length) {
          throw Error('Unexpected saved checklist');
        }
        request.record = record;
        request.phase = nextPhase(record);
        request.state = 'ready';
      } catch (error) {
        if (!ownsPreview(request)) return;
        request.state = [401,403,404,410].includes(error?.status) ? 'unavailable' : 'failed';
      }
      if (ownsPreview(request)) detail(allowed().find(row => row.id === request.id));
    }

    function showList() {
      if (!readyToNavigate()) return;
      const id = prefs.selected;
      prefs.selected = null;
      prefs.detail = false;
      update();
      const trigger = [...root.querySelectorAll('.cw-record-name')].find(button => button.dataset.cwSelect === id);
      trigger?.focus({preventScroll:true});
      root.querySelector('#checklist-results').scrollTop = prefs.listScroll;
      window.scrollTo({top:prefs.pageScroll, behavior:'instant'});
    }

    function checksMarkup(request) {
      if (request.state === 'loading') return `<p role="status" aria-busy="true">${panelText('Loading saved checks…','Carregando itens salvos…')}</p>`;
      if (request.state === 'failed') return `<div role="status"><p>${panelText('Could not load the saved items.','Não foi possível carregar os itens salvos.')}</p><button class="btn secondary" type="button" data-cw-retry>${__wl118.t('Retry')}</button></div>`;
      const record = request.record;
      const stage = request.phase;
      const stages = phases(record);
      const items = ctx.stageItems(record, stage);
      const start = request.page * checksPerPage;
      const rows = items.slice(start, start + checksPerPage).map(item => {
        const status = record.items[stage]?.[item.id]?.status || 'pending';
        return `<li><span class="cw-item-number">${esc(item.number)}</span><span>${esc(item.text)}</span><span class="cw-item-status" data-status="${esc(status)}">${esc(ctx.statusText(status))}</span></li>`;
      }).join('');
      const chooser = stages.length < 2 ? '' : `<label class="cw-preview-phase">${panelText('Stage','Etapa')} <select id="cw-preview-phase">${stages.map(p=>`<option value="${p}" ${p===stage?'selected':''}>${esc(phaseName(record,p))}</option>`).join('')}</select></label>`;
      const pager = items.length <= checksPerPage ? '' : `<nav class="cw-preview-pager" aria-label="${panelText('Checklist item pages','Páginas de itens da lista')}"><button class="btn secondary" type="button" id="cw-items-prev" ${start===0?'disabled':''}>${__wl118.t('Previous')}</button><span role="status">${start+1}–${Math.min(start+checksPerPage,items.length)} / ${items.length}</span><button class="btn secondary" type="button" id="cw-items-next" ${start+checksPerPage>=items.length?'disabled':''}>${__wl118.t('Next')}</button></nav>`;
      return `<div class="cw-preview-heading"><h3>${panelText('Checklist items','Itens da lista de verificação')}</h3>${chooser}</div>${rows?`<ul class="cw-item-list">${rows}</ul>`:`<p>${panelText('This stage has no items.','Esta etapa não tem itens.')}</p>`}${pager}`;
    }

    function detail(r) {
      const box = root.querySelector('#checklist-inspector');
      if (!r || !prefs.detail) {
        savedChecks = null;
        AJViewStability.paint(box, `<div class="cw-placeholder"><h2>${__wl118.t('Select a checklist')}</h2><p>${panelText('Choose a card to see its checks and saved progress.','Selecione um cartão para ver os itens e o andamento salvo.')}</p></div>`);
        return;
      }
      if (!savedChecks || savedChecks.id !== r.id || savedChecks.version !== r.version || savedChecks.session !== session) {
        savedChecks = {id:r.id, version:r.version, session, state:'loading', phase:nextPhase(r), page:0};
        readChecks(savedChecks);
      }
      const request = savedChecks;
      const back = `<button type="button" class="btn secondary cw-panel-back" id="cw-back-list">${panelText('Back to checklist records','Voltar às listas de verificação')}</button>`;
      if (request.state === 'unavailable') {
        AJViewStability.paint(box, `${back}<h2 id="cw-detail-title" tabindex="-1">${panelText('Checklist unavailable','Lista de verificação indisponível')}</h2><p role="status">${panelText('Refresh the list to see the records available to you.','Atualize a lista para ver os registros disponíveis para você.')}</p>`);
      } else {
        const record = request.record || r;
        const stage = request.phase;
        const final = !!record.phases[stage]?.final;
        const primary = final ? __wl118.t('View finalised stage') : __wl118.t('Continue checklist');
        const local = ctx.recordLocal(r.id);
        const facts = [
          [__wl118.t('Project'),record.meta?.project],
          [panelText('Ship or base','Embarcação ou base'),record.work_site?.name||record.meta?.vessel],
          [__wl118.t('Equipment'),record.meta?.vehicle],
          [__wl118.t('Record date'),record.meta?.date],
          [panelText('Created','Criado em'),record.created_at],
          [panelText('Updated','Atualizado em'),record.updated_at],
          [panelText('Saved revision','Revisão salva'),record.version],
          [panelText('Record mode','Modo de registro'),record.live_mode?panelText('Live','Editável'):panelText('Fixed','Fixo')]
        ].filter(([,value])=>value);
        const details = `<details class="cw-record-notes"><summary>${__wl118.t('Record details')}</summary><dl class="cw-facts">${facts.map(([label,value])=>`<div><dt>${esc(label)}</dt><dd>${esc(value)}</dd></div>`).join('')}</dl>${record.meta?.notes?`<p class="cw-notes-text">${esc(record.meta.notes)}</p>`:''}<p class="small">${__wl118.t('Record ID')}: ${esc(record.id)} · ${panelText('Revision','Revisão')} ${esc(record.template?.revision||'—')}</p></details>`;
        const progress = `<details class="cw-record-notes"><summary>${panelText('Stage progress','Andamento das etapas')}</summary>${phases(record).map(p=>stageRow(record,p)).join('')}</details>`;
        const localNotice = local ? `<p class="notice warn">${esc(panelText('Local drafts or queued changes','Rascunhos locais ou alterações na fila'))} (${local})</p>` : '';
        AJViewStability.paint(box, `${back}<header class="cw-panel-heading"><div><h2 id="cw-detail-title" tabindex="-1">${esc(reference(record))}</h2><p>${esc(record.template?.title||__wl118.t('Checklist'))}</p></div><span class="pill">${closed(record)?__wl118.t('Closed'):__wl118.t('Open')}</span></header><p class="small">${esc(summary(record))}</p>${localNotice}<a class="btn" data-cw-open="${esc(r.id)}" href="#dive/${encodeURIComponent(r.id)}/${stage}">${primary}</a><section id="cw-preview-items" aria-label="${panelText('Saved checklist items','Itens salvos da lista de verificação')}">${checksMarkup(request)}</section>${progress}${details}`);
        const stageSelect = box.querySelector('#cw-preview-phase');
        if (stageSelect) stageSelect.onchange = changePhase;
        const previous = box.querySelector('#cw-items-prev');
        const next = box.querySelector('#cw-items-next');
        if (previous) previous.onclick = () => changePage(-1);
        if (next) next.onclick = () => changePage(1);
        const retry = box.querySelector('[data-cw-retry]');
        if (retry) retry.onclick = () => { if(readyToNavigate()&&ownsPreview(request)){savedChecks=null;detail(r);} };
        box.querySelectorAll('[data-cw-open]').forEach(link => { link.onclick = event => {
          if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
          if (!readyToNavigate() || !ownsPreview(request)) {event.preventDefault();return;}
          snapshotPosition(); prefs.opened = r.id;
        }; });
      }
      box.querySelector('#cw-back-list').onclick = showList;
      box.onkeydown = event => {
        if(event.key==='Escape' && !event.defaultPrevented && !event.target.closest('select,input,textarea') && !ctx.busy()) {event.preventDefault();showList();}
      };
      function changePhase(event) {
        if (!readyToNavigate() || !ownsPreview(request)) return;
        request.phase = event.target.value; request.page = 0; detail(r);
      }
      function changePage(delta) {
        if (!readyToNavigate() || !ownsPreview(request)) return;
        request.page += delta; detail(r);
      }
    }
