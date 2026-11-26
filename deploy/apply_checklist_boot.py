"""Let native demo Home and Inventory open without unrelated checklist data."""
from pathlib import Path
import runpy
import sys


def script(source):
    def replace(before, after):
        nonlocal source
        if source.count(before) != 1:
            raise ValueError('Unexpected checklist startup anchor: ' + before)
        source = source.replace(before, after)

    # Both the new-record form and the workspace menu use the same selection
    # convention. The menu only needs the brief returned by the catalog.
    replace("""    const wanted=state.formTemplateId||state.template?.id||state.info?.template_id;
    state.templates=types;
    const selected=types.find(t=>t.id===wanted)||(state.formTemplateId?null:types[0]);""",
            """    state.templates=types;
    const selected=selectedChecklistType(types);""")
    replace('async function refreshTemplates(){', """function selectedChecklistType(types) {
    const wanted = state.formTemplateId || state.template?.id || state.info?.template_id;
    return types.find(type => type.id === wanted) || (state.formTemplateId ? null : types[0]);
}

let deferredChecklistSession = null;

async function showDeferredMenuChecklist() {
    const session = deferredChecklistSession;
    if (!session || session !== connectionSession() || !canUse('checklists.view')) return;
    const title = dlg.querySelector('#menu-checklist-title');
    const revision = dlg.querySelector('#menu-checklist-revision');
    if (!title || !revision) return;
    const current = () => title.isConnected && dlg.open && session === connectionSession() && canUse('checklists.view');
    try {
        const types = await api('/api/templates');
        if (!current()) return;
        const selected = selectedChecklistType(types);
        title.textContent = selected?.title || '—';
        revision.textContent = selected?.revision || '—';
    } catch (_) {
        if (!current()) return;
        title.textContent = window.WavelinkUX.text('Indisponível', 'Unavailable');
        revision.textContent = '—';
    }
}

async function refreshTemplates(){""")
    replace('Selected checklist ${esc(state.template?.title||"—")} · Rev ${esc(state.template?.revision||"—")}',
            'Selected checklist <span id="menu-checklist-title">${esc(state.template?.title||"—")}</span>'
            ' · Rev <span id="menu-checklist-revision">${esc(state.template?.revision||"—")}</span>')
    replace("if($('#menu-approvals'))$('#menu-approvals').onclick=approvalInbox;",
            "showDeferredMenuChecklist();if($('#menu-approvals'))$('#menu-approvals').onclick=approvalInbox;")
    replace("async function authenticated(){if(await profileLanguage.restore())return;if(state.auth?.person?.fleet_mode==='vessel_only'){render();return;}try{if(state.info?.capabilities?.fleet)state.info=await api('/api/info');await refreshTemplates();await loadRecords();await persist();}catch(e){if(e.status===401){state.auth=null;await persist();}}connectLive();await route();",
            """async function authenticated(){
    if (await profileLanguage.restore()) return;
    if (state.auth?.person?.fleet_mode === 'vessel_only') { render(); return; }
    deferredChecklistSession = null;
    try {
        if (state.info?.capabilities?.fleet) state.info = await api('/api/info');
        const hash = location.hash || '#home';
        const landing = hash === '#home' || hash === '#inventory' || hash.startsWith('#inventory/');
        if (landing && online && WavelinkNativeDemo.active() && canUse('checklists.view')) {
            // The public catalog and personal Home use their own reads. Checklists
            // fetches summaries on entry; the new-record form fetches definitions.
            deferredChecklistSession = connectionSession();
        } else {
            await refreshTemplates();
            await loadRecords();
        }
        await persist();
    } catch (error) {
        if (error.status === 401) { state.auth = null; await persist(); }
    }
    connectLive();
    await route();
""")
    return source


def transforms():
    return {'app/static/app.js': script}


if __name__ == '__main__':
    build = Path(__file__).resolve()
    apply = runpy.run_path(str(build.with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]), parent='07513f8eda8d9b8bc24e8fcf9a272d82e814958e7e4abee162570e25a17e6ea2',
          overlays=(build.name,), cache=None, suffix='defer-demo-checklists',
          scope='Load checklist data on demand when the public demo starts in Home or Inventory.')
