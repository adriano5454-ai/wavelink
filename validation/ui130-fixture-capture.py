from pathlib import Path
import json, os, platform, runpy, sys, tempfile, uuid
w=Path(__file__).resolve().parent; r=w/'runtime-ui130'
platform.node=lambda:'isolated-ui130-it-api-flow'
(w/'ui130-it-temp').mkdir(exist_ok=True)
tempfile.tempdir=str(w/'ui130-it-temp')
sys.path[:0]=[str(w/'policy-test-deps'),str(r)]
os.chdir(r)
from fastapi.testclient import TestClient
from app.server import create_app
Company=runpy.run_path(str(r/'tests/test_it_requests_ui130.py'))['Company']
with tempfile.TemporaryDirectory(prefix='api-contract-') as temp:
 app=create_app(Path(temp)/'company')
 with TestClient(app) as client:
  h=Company(app,client); operations=[]; current=None
  def perform(action,payload,key='alice'):
   global current
   before=h.read('requests/'+current['id'],key) if current else None
   request_body=dict(action=action,payload=payload,op_id=str(uuid.uuid4()))
   before_workspace=h.read('workspace?view='+('queue' if key=='desk' else 'mine'),key)
   before_detail_workspace=h.read('workspace?view=mine&limit=1',key)
   response=client.post('/api/it/action',headers=h.headers(key),json=request_body)
   assert response.status_code==200,response.text
   saved=response.json(); current=saved['request']
   assert h.read('requests/'+current['id'],key)==saved
   operations.append(dict(actor='manager' if key=='desk' else 'owner',actor_user_id=h.uid(key),before_detail=before,before_workspace=before_workspace,before_detail_workspace=before_detail_workspace,request_body=request_body,response=saved))
   return saved
  created=perform('create',dict(title='Conexão da estação fictícia',description='Descrição de teste <sem HTML executável>.',priority='normal'))
  assigned=perform('triage',dict(id=current['id'],version=current['version'],priority='high',assignee_id=h.uid('desk')),'desk')
  commented=perform('comment',dict(id=current['id'],version=current['version'],text='Comentário fictício de triagem.'),'desk')
  active=perform('transition',dict(id=current['id'],version=current['version'],status='in_progress',comment='Atendimento iniciado no teste.'),'desk')
  fixture=dict(scope='Synthetic real HTTP API responses from an isolated TestClient company; no production data or messages.',created_detail=created,comment_response=commented,triage_response=assigned,transition_response=active,manager_detail=h.read('requests/'+current['id'],'desk'),owner_detail=h.read('requests/'+current['id']),owner_workspace=h.read('workspace'),manager_workspace=h.read('workspace?view=queue','desk'),history_page=h.read('requests/'+current['id']+'/history?offset=0&limit=2'))
  waiting=perform('transition',dict(id=current['id'],version=current['version'],status='awaiting_requester',comment='Informe o horário do erro fictício.'),'desk')
  reply=perform('comment',dict(id=current['id'],version=current['version'],text='O erro ocorreu às 10h.'),'alice')
  assert reply['request']['status']=='awaiting_requester'
  resumed=perform('transition',dict(id=current['id'],version=current['version'],status='in_progress',comment='Informação recebida no teste.'),'desk')
  resolved=perform('transition',dict(id=current['id'],version=current['version'],status='resolved',comment='Conexão fictícia restabelecida e conferida.'),'desk')
  closed=perform('transition',dict(id=current['id'],version=current['version'],status='closed',comment='Confirmo a solução no teste.'),'alice')
  reopened=perform('transition',dict(id=current['id'],version=current['version'],status='open',comment='A falha voltou no cenário fictício.'),'alice')
  cancelled=perform('transition',dict(id=current['id'],version=current['version'],status='cancelled',comment='Cancelamento do cenário fictício sem apagar o histórico.'),'alice')
  assert len(h.read('requests/'+current['id'])['history'])==len(operations)
  fixture.update(operations=operations,manager_before_triage=operations[1]['before_detail'],manager_before_transition=operations[3]['before_detail'],resolved_response=resolved,closed_response=closed,requester_before_reopen=operations[9]['before_detail'],reopened_response=reopened,cancelled_response=cancelled)
  (w/'ui130-it-api-fixture.json').write_text(json.dumps(fixture,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
  print(json.dumps(dict(passed=True,operations=len(operations),final_status=current['status'],final_version=current['version'],history_count=len(operations),path='work/ui130-it-api-fixture.json')))
