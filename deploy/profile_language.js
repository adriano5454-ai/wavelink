/* The company setting belongs to the signed-in employee. Public visitors keep
   their selection in the same isolated browser workspace as the rest of their visit. */
window.AJProfileLanguage = (() => {
    'use strict';
    const supported = value => value === 'en' || value === 'pt-BR';
    const current = () => window.WavelinkI18n.locale;
    const text = (en, pt) => current() === 'pt-BR' ? pt : en;
    function create({state, demo, session, api, persist, editing}) {
        const defaultLanguage = () => demo() ? 'en' : (state().info?.ui_locale === 'pt-BR' ? 'pt-BR' : 'en');
        function selected() {
            const value = demo() ? state().demoLanguage : state().auth?.person?.preferred_language;
            return supported(value) ? value : defaultLanguage();
        }
        function apply(language) {
            if (language === current()) return false;
            const next = new URL(location.href);
            if (demo()) {
                next.pathname = language === 'pt-BR' ? '/__demo/native/pt' : '/';
                next.searchParams.delete('wl_lang');
            } else if (language === defaultLanguage()) {
                next.searchParams.delete('wl_lang');
            } else {
                next.searchParams.set('wl_lang', language);
            }
            // An offline fallback may serve the default shell at the requested URL.
            if (next.href === location.href) return false;
            location.replace(next.href);
            return true;
        }
        function mount(host) {
            if (!host) return;
            const owner = session();
            const heading = text('Language', 'Idioma');
            const label = demo() ? text('Language for this visit', 'Idioma desta visita') :
                                   text('Preferred language', 'Idioma de preferência');
            const help = demo() ? text('Every new demo visit starts in English.', 'Cada nova visita à demonstração começa em inglês.') :
                                  text('Used when you sign in on any device.', 'Usado quando você entra na sua conta em qualquer dispositivo.');
            host.innerHTML = '<h2>' + heading + '</h2><form><div class="wl-language-field"><label for="wl-language-select">' +
                label + '</label><select id="wl-language-select" aria-describedby="wl-language-help"><option value="en" lang="en">English</option>' +
                '<option value="pt-BR" lang="pt-BR">Português (Brasil)</option></select></div><button class="btn secondary" type="submit">' +
                (demo() ? text('Apply to this visit', 'Aplicar nesta visita') : text('Save language', 'Salvar idioma')) +
                '</button></form><p class="small muted" id="wl-language-help">' + help +
                '</p><p class="small" role="status" aria-live="polite" hidden></p>';
            const form = host.querySelector('form'), select = host.querySelector('select');
            const button = host.querySelector('button'), status = host.querySelector('[role=status]');
            let busy = false;
            select.value = selected();
            function controls() { select.disabled = busy; button.disabled = busy || select.value === selected(); }
            function note(message) { status.textContent = message; status.hidden = false; }
            select.onchange = () => { status.hidden = true; controls(); };
            form.onsubmit = async event => {
                event.preventDefault();
                const choice = select.value;
                if (busy || session() !== owner || !supported(choice) || choice === selected()) return;
                if (editing()) {
                    note(text('Save or close your open edit first.', 'Salve ou feche a edição em andamento primeiro.'));
                    return;
                }
                busy = true;
                controls();
                const visit = demo(), workspace = state(), previous = workspace.demoLanguage, route = location.hash;
                try {
                    if (!visit) {
                        const saved = await api('/api/me/language', {method:'POST', body:{language:choice}});
                        if (session() !== owner || state() !== workspace || saved.preferred_language !== choice) return;
                        workspace.auth.person.preferred_language = choice;
                    } else {
                        workspace.demoLanguage = choice;
                    }
                    try { await persist(); }
                    catch (error) {
                        if (visit) { workspace.demoLanguage = previous; throw error; }
                        if (session() === owner && host.isConnected) note(text('Language saved to your account. Reload when this device is ready.', 'Idioma salvo na conta. Atualize a página quando este dispositivo estiver pronto.'));
                        return;
                    }
                    if (session() !== owner || state() !== workspace || location.hash !== route || !host.isConnected) return;
                    if (!apply(choice)) note(text('Language applied.', 'Idioma aplicado.'));
                } catch (error) {
                    if (session() === owner && host.isConnected) note(error.message || text('Please try again.', 'Tente novamente.'));
                } finally { busy = false; if (host.isConnected) controls(); }
            };
            controls();
        }
        return {
            mount,
            restore: () => apply(selected()),
            signedOut: () => Boolean(state().info && !state().publicDemoUserId && new URLSearchParams(location.search).has('wl_lang') && apply(defaultLanguage()))
        };
    }
    return {create};
})();
