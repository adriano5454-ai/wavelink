/* WaveLink read-only PDF preview. Never hands document bytes to a remote service. */
(() => {
  'use strict';
  const base = '/static/wl-pdfjs-6.5.438/';
  let active, engine;
  const t = (en, pt) => /^(pt)(-|$)/i.test(document.documentElement.lang) ? pt : en;
  const el = (name, text) => { const e = document.createElement(name); if (text) e.textContent = text; return e; };
  function loadEngine() {
    if (!engine) engine = import(base + 'pdf.min.mjs').then(lib => {
      lib.GlobalWorkerOptions.workerSrc = base + 'pdf.worker.min.mjs';
      return lib;
    }).catch(error => { engine = null; throw error; });
    return engine;
  }
  function open(blob, { name = 'document.pdf', trigger = document.activeElement, allowed = () => true } = {}) {
    if (!(blob instanceof Blob) || typeof allowed !== 'function') return false;
    const valid = () => { try { return allowed() === true; } catch { return false; } };
    if (!valid()) return false;
    active?.dispose(false);

    const dialog = el('dialog'), header = el('header'), title = el('h2', name);
    const toolbar = el('nav'), body = el('div'), status = el('p'), canvas = el('canvas');
    const number = el('span');
    let raw = blob, doc, task, drawing, page = 1, zoom = 1, seq = 0, timer, resize, ended = false;
    const origin = location.href;
    dialog.className = 'wl-pdf-dialog';
    dialog.setAttribute('aria-label', t('PDF preview','Visualização do PDF') + ': ' + name);
    toolbar.setAttribute('aria-label', t('PDF controls','Controles do PDF'));
    body.className = 'wl-pdf-body'; body.tabIndex = 0;
    body.setAttribute('aria-label', t('Document page','Página do documento'));
    status.className = 'wl-pdf-status'; status.setAttribute('role', 'status');
    number.setAttribute('aria-live','polite');
    canvas.hidden = true;
    const button = (en, pt, run) => {
      const b = el('button',t(en,pt)); b.type = 'button'; b.className = 'btn secondary';
      b.addEventListener('click', run); return b;
    };
    const close = button('Close','Fechar',() => dispose(true)); close.autofocus = true;
    const save = button('Download','Baixar',() => {
      if (!usable() || !raw) return;
      const url = URL.createObjectURL(raw), a = el('a');
      a.href = url; a.download = name; document.body.append(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 30000);
    });
    const prev = button('Previous page','Página anterior',() => { if (page > 1) { page--; render(); } });
    const next = button('Next page','Próxima página',() => { if (page < doc?.numPages) { page++; render(); } });
    const less = button('Zoom out','Reduzir zoom',() => { zoom = Math.max(.67, zoom / 1.25); render(); });
    const more = button('Zoom in','Aumentar zoom',() => { zoom = Math.min(3, zoom * 1.25); render(); });
    const fit = button('Fit width','Ajustar à largura',() => { zoom = 1; render(); });
    function controls() {
      prev.disabled = !doc || page <= 1; next.disabled = !doc || page >= doc.numPages;
      less.disabled = !doc || zoom <= .67; more.disabled = !doc || zoom >= 3;
      fit.disabled = !doc || zoom === 1;
      number.textContent = doc ? page + ' / ' + doc.numPages : '';
    }
    function dispose(restore) {
      if (ended) return;
      ended = true; seq++; clearInterval(timer); clearTimeout(resize);
      window.removeEventListener('hashchange', boundary);
      window.removeEventListener('popstate', boundary);
      window.removeEventListener('pagehide', leave);
      window.removeEventListener('resize', reflow);
      drawing?.cancel(); Promise.resolve(task?.destroy()).catch(() => {});
      canvas.width = canvas.height = 0; raw = null;
      if (dialog.open) dialog.close(); dialog.remove();
      if (active?.dispose === dispose) active = null;
      if (restore && valid() && trigger?.isConnected && typeof trigger.focus === 'function') trigger.focus({preventScroll:true});
    }
    function usable() {
      if (ended || active?.dispose !== dispose) return false;
      if (origin !== location.href || !valid()) { dispose(false); return false; }
      return true;
    }
    function boundary() { usable(); }
    function leave() { dispose(false); }
    function reflow() { clearTimeout(resize); resize = setTimeout(() => render(), 120); }
    function problem() {
      canvas.hidden = true;
      status.textContent = t('This PDF could not be previewed. You can still download it.', 'Não foi possível visualizar este PDF. Você ainda pode baixá-lo.');
    }
    async function render() {
      if (!usable() || !doc) return;
      const id = ++seq;
      const previous = drawing; previous?.cancel();
      status.textContent = t('Rendering page…','Preparando página…'); controls();
      try {
        if (previous) await previous.promise.catch(() => {});
        const pdfPage = await doc.getPage(page);
        if (!usable() || seq !== id) return;
        const width = Math.max(100, body.clientWidth - 28);
        const unit = pdfPage.getViewport({scale: 1});
        const viewport = pdfPage.getViewport({scale: (width / unit.width) * zoom});
        const ratio = Math.min(devicePixelRatio || 1, 2, 4096 / Math.max(viewport.width, viewport.height),
          Math.sqrt(12000000 / (viewport.width * viewport.height)));
        if (!Number.isFinite(ratio) || ratio <= 0) throw Error('Invalid page dimensions');
        canvas.width = Math.max(1, Math.floor(viewport.width * ratio));
        canvas.height = Math.max(1, Math.floor(viewport.height * ratio));
        canvas.style.width = Math.round(viewport.width) + 'px';
        canvas.style.height = Math.round(viewport.height) + 'px';
        canvas.setAttribute('aria-label', t('PDF page ','Página do PDF ') + page);
        const current = pdfPage.render({canvas, viewport, transform: [ratio,0,0,ratio,0,0], annotationMode: 1});
        drawing = current; await current.promise;
        if (!usable() || seq !== id) return;
        canvas.hidden = false; body.scrollTop = body.scrollLeft = 0; status.textContent = '';
      } catch { if (usable() && seq === id) problem(); }
    }
    title.title = name; header.append(title, save, close);
    toolbar.append(prev, number, next, less, fit, more); body.append(status, canvas);
    dialog.append(header, toolbar, body); document.body.append(dialog); active = {dispose};
    try { dialog.showModal(); } catch { dispose(false); return false; }
    controls(); status.textContent = t('Opening PDF…','Abrindo PDF…');
    dialog.addEventListener('cancel', event => { event.preventDefault(); dispose(true); });
    dialog.addEventListener('close', () => dispose(true));
    window.addEventListener('hashchange', boundary);
    window.addEventListener('popstate', boundary);
    window.addEventListener('pagehide', leave);
    window.addEventListener('resize', reflow);
    timer = setInterval(boundary, 350);
    (async () => {
      try {
        const signature = new TextDecoder().decode(await raw.slice(0,1024).arrayBuffer());
        if (!usable()) return;
        if (!signature.includes('%PDF-')) throw Error('Not a PDF');
        const lib = await loadEngine();
        if (!usable()) return;
        const data = new Uint8Array(await raw.arrayBuffer());
        if (!usable()) return;
        task = lib.getDocument({data, cMapUrl:base+'cmaps/', cMapPacked:true, standardFontDataUrl:base+'standard_fonts/',
          iccUrl:base+'iccs/', wasmUrl:base+'wasm/', isEvalSupported:false, enableXfa:false, useSystemFonts:true,
          maxImageSize:18000000});
        doc = await task.promise;
        if (usable()) render();
      } catch { if (usable()) problem(); }
    })();
    return true;
  }
  window.WLPdfViewer = Object.freeze({open});
})();
