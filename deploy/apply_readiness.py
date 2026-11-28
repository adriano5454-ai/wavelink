"""Add operational readiness as a non-authorising read-only company view."""
from hashlib import sha256
from pathlib import Path
import runpy, sys
BASE=Path(__file__).resolve().parent
PARENT='4cc01f2ea127053bf40e29ed5895958c1a478c133b98ee40dcdae4df3fb0fdb6'
STATIC='app/static/'
def once(s,a,b):
    if s.count(a)!=1:raise ValueError(a)
    return s.replace(a,b,1)
def additions():
    return {'app/readiness.py':(BASE/'readiness_model.py').read_bytes(), **{
        STATIC+name:(BASE/name).read_bytes() for name in ('readiness_workspace.js','readiness_workspace.css')}}
def operations(s):
    return once(s,"    @app.get('/api/attention')", """    @app.get('/api/readiness')
    def readiness(a=Depends(logged)):
        from .readiness import snapshot
        from fastapi.responses import JSONResponse
        return JSONResponse(snapshot(store,a,config['hub_id']), headers={'Cache-Control':'no-store'})
    @app.get('/api/attention')""")
def app(s):
    s=once(s,"if(originalLibrary.handles(hash)){","if(hash==='#readiness'){AJLogs.cleanup();window.AJReadiness.open({root,can:canUse,person:()=>state.auth?.person,api,session:connectionSession,hub:()=>state.hub_id});return;}if(originalLibrary.handles(hash)){")
    return once(s,'|profile|qshe|tasks|','|profile|qshe|readiness|tasks|')
def catalogue(s):
    anchor="  ['qshe','safety',"
    line="""  ['readiness','safety','Operational readiness','#readiness','@readiness','Review authorised findings across crew documents, equipment certificates, maintenance and HSE.','readiness compliance expiry inspection prontidão conformidade pendências'],
"""
    s=once(s,anchor,line+anchor)
    s=once(s,"r.permission==='@fleet'?","r.permission==='@readiness'?window.AJReadiness?.allowed(can,person):r.permission==='@fleet'?")
    return once(s,"get:()=>T(r[index])","get:()=>r[0]==='readiness'&&window.WavelinkI18n?.locale==='pt-BR'?(index===2?'Prontidão operacional':'Confira pendências autorizadas em documentos da equipe, certificados, manutenção e HSE.'):T(r[index])")
def homepage(s):
    anchor='<a href="#workspaces" class="btn">Open Workspaces</a>'
    line="""${window.AJReadiness?.allowed(H.can,H.person())?__wl118.html`<a href="#readiness" class="btn secondary">${E(window.WavelinkUX.text('Prontidão operacional','Operational readiness'))}</a>`:''}"""
    # The global app can() is passed to the Home workspace.
    return once(s,anchor,anchor+line)
def shells(s):
    v=lambda name:sha256((BASE/name).read_bytes()).hexdigest()[:12]
    return once(s,'</head>',
      f'<link rel="stylesheet" href="/static/readiness_workspace.css?v=1.34.61-{v("readiness_workspace.css")}">\n'
      f'<script defer src="/static/readiness_workspace.js?v=1.34.61-{v("readiness_workspace.js")}"></script>\n</head>')
def transforms():
    return {'app/operations_api.py':operations,STATIC+'app.js':app,STATIC+'workspace_catalogue.js':catalogue,
            STATIC+'personal_home.js':homepage,STATIC+'index.html':shells,STATIC+'pt-BR/index.html':shells}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),
        previous_cache='ui162-source-pdf-viewer',cache='ui162-readiness',suffix='readiness',
        scope='Read-only operational readiness from permission-filtered certificates, maintenance, crew documents and HSE.')
