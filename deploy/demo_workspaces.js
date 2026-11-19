/* Public guest destinations backed by the fictional management catalogue. */
const PublicDemoWorkspaces = (() => {
    const samples = {
        hr: ['hr', 'Human resources (HR)', 'Recursos humanos (RH)',
             'Explore employee profiles, certificates, rotations, travel, timesheets and expenses.',
             'Consulte perfis, certificados, escalas, viagens, folhas de ponto e despesas.'],
        it: ['it', 'IT requests', 'Solicitações de TI',
             'Follow support tickets, priorities, replies and attachments.',
             'Consulte chamados de suporte, prioridades, respostas e anexos.'],
        fleet: ['fleet', null, null, 'Explore a vessel, its project and incoming equipment.',
               'Consulte uma embarcação, seu projeto e os equipamentos previstos.'],
        shipments: ['shipments', null, null, 'Trace a sample shipment from the shore base to the vessel.',
                    'Acompanhe uma remessa de exemplo da base até a embarcação.'],
        receiving: ['shipments/mf014', null, null, 'See the contents and receiving instructions for a manifest.',
                    'Consulte o conteúdo e as instruções de recebimento de um manifesto.'],
        members: ['access', null, null, 'View sample access profiles, invitations and approvals.',
                  'Consulte perfis de acesso, convites e aprovações de exemplo.'],
        admin: ['admin', null, null, 'Explore all eight administration sections with read-only access.',
                'Explore as oito seções administrativas com acesso de leitura.']
    };
    function destinations(nativeKeys, portuguese) {
        const result = {};
        for (const [key, [path, en, pt, enNote, ptNote]] of Object.entries(samples)) {
            if (key === 'hr' || key === 'it' || !nativeKeys.includes(key)) {
                result[key] = {href: '#demo/' + path, title: portuguese ? pt : en,
                               description: portuguese ? ptNote : enNote};
            }
        }
        return result;
    }
    function directory(rows, context) {
        if (!context) return rows;
        const native = new Set(rows.map(row => row.key));
        return AJWorkspaceCatalogue.rows.filter(row => native.has(row.key) || context.destinations[row.key]).map(row => {
            const demo = context.destinations[row.key];
            if (!demo) return row;
            return {...row, href: demo.href, title: demo.title || row.title,
                    description: demo.description || row.description, sample: true};
        });
    }
    function navLink(link, context) {
        const sample = context?.destinations[link.dataset.workspace];
        if (sample) {
            if (!link.hasAttribute('data-demo-previous-href')) {
                link.dataset.demoPreviousHref = link.getAttribute('href');
                link.dataset.demoPreviousFleet = String(link.hasAttribute('data-open-fleet'));
            }
            link.hidden = false;
            link.setAttribute('href', sample.href);
            link.removeAttribute('data-open-fleet');
        } else if (link.hasAttribute('data-demo-previous-href')) {
            link.setAttribute('href', link.dataset.demoPreviousHref);
            link.toggleAttribute('data-open-fleet', link.dataset.demoPreviousFleet === 'true');
            delete link.dataset.demoPreviousHref;
            delete link.dataset.demoPreviousFleet;
        }
    }
    function activeKey(hash) {
        const area = hash.split(/[/?]/)[1];
        if (['hr', 'personnel', 'schedule', 'travel', 'time', 'expenses', 'alerts'].includes(area)) return 'hr';
        if (area === 'access') return 'members';
        if (area === 'shipments') return 'fleet';
        return area;
    }
    function open(root, context) {
        const hash = location.hash;
        const [path, search = ''] = hash.slice('#demo/'.length).split('?');
        const [area, record] = path.split('/');
        const params = new URL(context.href, location.origin).searchParams;
        params.set('area', area);
        if (record) params.set('record', record);
        const options = new URLSearchParams(search);
        if (options.has('q')) params.set('q', options.get('q'));
        if (options.get('from') === 'admin') params.set('from', 'admin');
        const key = params.toString();
        if (root.firstElementChild?.dataset.demoRequest === key) return;
        const host = document.createElement('section');
        host.dataset.demoRequest = key;
        const panel = host.attachShadow({mode: 'open'});
        const pt = params.get('lang') === 'pt';
        const status = document.createElement('p');
        status.setAttribute('role', 'status');
        status.textContent = pt ? 'Carregando a área de trabalho…' : 'Loading workspace…';
        panel.append(status);
        root.replaceChildren(host);
        const current = () => host.isConnected && location.hash === hash;
        fetch('/__demo/management/workspace?' + key, {credentials: 'same-origin', cache: 'no-store'})
            .then(async response => {
                if (!response.ok && response.status !== 404) throw Error('Unavailable');
                const html = await response.text();
                if (!current()) return;
                if (!html.startsWith('<style>')) throw Error('Unexpected response');
                panel.innerHTML = html;
                for (const file of panel.querySelectorAll('a[href^="/__demo/management/files/"]')) {
                    file.target = '_blank';
                    file.rel = 'noopener noreferrer';
                }
            }).catch(() => {
                if (!current()) return;
                status.textContent = pt ? 'Não foi possível carregar esta área.' : 'This workspace could not be loaded.';
                const retry = document.createElement('button');
                retry.type = 'button';
                retry.textContent = pt ? 'Tentar novamente' : 'Try again';
                retry.onclick = () => { delete host.dataset.demoRequest; open(root, context); };
                const back = document.createElement('a');
                back.href = '#workspaces';
                back.textContent = pt ? 'Áreas de trabalho' : 'Workspaces';
                panel.append(retry, ' · ', back);
            });
        panel.addEventListener('submit', event => {
            event.preventDefault();
            const data = new FormData(event.target);
            const next = new URLSearchParams();
            if (options.get('from') === 'admin') next.set('from', 'admin');
            const term = String(data.get('q') || '').trim().slice(0, 80);
            if (term) next.set('q', term);
            location.hash = '#demo/' + area + (next.size ? '?' + next : '');
        });
    }
    return {destinations, directory, navLink, activeKey, open};
})();
