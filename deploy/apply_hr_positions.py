from pathlib import Path
import runpy
import sys

BASE=Path(__file__).parent

def api(s):
    anchor="    @app.get('/api/hr/directory')"
    assert s.count(anchor)==1
    return s.replace(anchor,"""    from . import org_positions
    with store.connection(True) as c:
        org_positions.schema(c)

    @app.get('/api/hr/org-positions')
    def org_read(request:Request, person=Depends(logged)):
        with store.connection() as c:
            return response(org_positions.snapshot(c,person,getattr(request.state,'public_demo_read_only',False)))

    @app.post('/api/hr/org-positions')
    async def org_save(request:Request, person=Depends(logged)):
        raw=bytearray()
        async for part in request.stream():
            if len(raw)+len(part)>4096:
                raise Problem(413,'Position request too large.')
            raw.extend(part)
        try:
            payload=json.loads(raw)
        except (ValueError,UnicodeError):
            raise Problem(422,'Invalid position.')
        return response(await asyncio.to_thread(org_positions.save,store,person,payload,getattr(request.state,'public_demo_read_only',False)))

"""+anchor)

def ui(s):
    anchor="function renderOrg(){"
    assert s.count(anchor)==1
    s=s.replace(anchor,(BASE/'hr_position_editor.js').read_text(encoding='utf8')+'\n'+anchor)
    anchor="E(orgText('Nenhuma pessoa visível.','No visible people.'))+'</p>');"
    assert s.count(anchor)==1
    return s.replace(anchor,anchor+"\n  const positions=document.createElement('section');records.prepend(positions);mountPositions(positions);")

def additions():
    return {'app/org_positions.py':(BASE/'org_positions.py').read_bytes()}

def transforms():
    return {'app/hr_api.py':api,'app/static/hr_workspace.js':ui,'app/static/ui132_visual.css':lambda s:s+"""
.hr-position-row{display:grid;gap:.25rem;border-inline-start:2px solid var(--line);padding:.65rem;overflow-wrap:anywhere}
.hr-position-row button{justify-self:start}.hr-position-form{display:grid;gap:.65rem;max-width:32rem}
.hr-position-form label:not([hidden]){display:grid;gap:.2rem}.hr-position-form select,.hr-position-form input{min-width:0;width:100%}
"""}

if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](Path(sys.argv[1]),parent='65708dc6c1148df46291f768ed7188e61f8a8060c7fe873b21dcd44d67e97544',
        overlays=(Path(__file__).name,),previous_cache='ui162-hr-org-chart',cache='ui162-hr-positions',suffix='hr-positions',scope='Company reporting positions, separate from authentication.')
