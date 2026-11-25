from pathlib import Path
import runpy
import sys

BASE = Path(__file__).resolve().parent
one = runpy.run_path(str(BASE/'apply_org_chart_filters.py'))['replace_once']


def workspace(source):
    source = one(source, "    function stageRow(r,p) {", """    function guestStage(stage) {
      return `<button class="btn secondary" type="button" data-cw-read-stage="${esc(stage)}">${panelText('Read saved stage','Ler etapa salva')}</button>`;
    }
    function stageRow(r,p) {""")
    start = source.index('<a class="btn secondary" data-cw-open')
    end = source.index('</a>', start) + 4
    source = source[:start] + "${ctx.publicVisitor?.()?guestStage(p):__wl118.html`" + source[start:end] + "`}" + source[end:]
    source = one(source, "closed(r)?__wl118.t('View finalised checklist')", "ctx.publicVisitor?.()?panelText('Read checklist','Ler lista de verificação'):closed(r)?__wl118.t('View finalised checklist')")
    source = one(source,"if(!r)return;snapshotPosition();prefs.opened=r.id;","if(!r)return;if(ctx.publicVisitor?.()){select(r.id);return;}snapshotPosition();prefs.opened=r.id;")
    start = source.index('<a class="btn" data-cw-open')
    end = source.index('</a>', start) + 4
    source = source[:start] + "${ctx.publicVisitor?.()?guestStage(stage):`" + source[start:end] + "`}" + source[end:]
    source = one(source,'        const stageSelect =',"""        box.querySelectorAll('[data-cw-read-stage]').forEach(button=>{button.onclick=()=>{
          if(!readyToNavigate()||!ownsPreview(request)||request.state!=='ready')return;
          const phase=button.dataset.cwReadStage;
          if(!phases(request.record).includes(phase))return;
          request.phase=phase;request.page=0;detail(r);
          const items=box.querySelector('#cw-preview-items');items.tabIndex=-1;items.focus();
        };});
        const stageSelect =""")
    return source


def transforms():
    return {'app/static/checklist_workspace.js':workspace,
            'app/static/app.js':lambda s:one(s,'const checklistWorkspace = AJChecklistWorkspace.create({',
                'const checklistWorkspace = AJChecklistWorkspace.create({\n    publicVisitor:()=>WavelinkNativeDemo.active(),')}


if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),
        parent='5268be83dc9eb6e46db07e1b01b5c6d5c17a4dd1ed144f2ed7ebf06ae6b6ddd4',
        overlays=(Path(__file__).name,),previous_cache='ui162-placement-locations',
        cache='ui162-checklist-guest-reader',suffix='checklist-guest-reader',scope='Open saved checklist items in the public visitor reader.')
