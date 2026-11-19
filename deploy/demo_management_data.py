"""Public, hand-authored examples for the fictional Maré Alta Surveys company."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    key: str
    title: tuple
    status: tuple
    fields: tuple
    related: tuple = ()


@dataclass(frozen=True)
class Area:
    key: str
    group: str
    title: tuple
    description: tuple
    native: str
    records: tuple


def name(text):
    return (text, text)


GROUPS = {
    'company': ('Company administration', 'Administração da empresa'),
    'people': ('People & HR', 'Equipe e RH'),
    'work': ('Daily operations', 'Operações do dia a dia'),
    'equipment': ('Equipment & logistics', 'Equipamentos e logística'),
    'safety': ('Safety & documents', 'Segurança e documentos'),
}
DEPARTMENT = ('Department', 'Departamento')
PERSON = ('Employee', 'Colaborador')
LOCATION = ('Location', 'Localização')
PROJECT = ('Project', 'Projeto')
PERIOD = ('Period', 'Período')
ASSIGNED = ('Assigned to', 'Responsável')
NEXT = ('Next step', 'Próxima etapa')
EVIDENCE = ('Attachment', 'Anexo')
STATUS = ('Status', 'Situação')
SURVEY = ('Survey', 'Levantamento')
HR = ('Human resources', 'Recursos humanos')
IT = ('Information technology', 'Tecnologia da informação')
FIELD = ('Field operations', 'Operações de campo')
VESSEL = name('MV Aurora')
PROJECT_NAME = ('OCN-001 · Aurora survey', 'OCN-001 · Levantamento Aurora')
EQUIPMENT = ('SV-204 · Sound velocity probe', 'SV-204 · Sonda de velocidade do som')
FOLDER = ('Transport case 04', 'Maleta de transporte 04')
SHIPMENT = ('MF-014 · Mobilisation', 'MF-014 · Mobilização')
LIA = name('Lia Prado')
NILO = name('Nilo Reis')
DORA = name('Dora Luz')
APPROVED = ('Approved', 'Aprovado')
CONFIRMED = ('Confirmed', 'Confirmado')
ACTIVE = ('Active', 'Ativo')
PLANNED = ('Planned', 'Planejado')
SAVED = ('Saved', 'Salvo')
PENDING = ('Awaiting review', 'Aguardando análise')
PEOPLE = Area('access', 'company', ('People & access', 'Pessoas e acesso'),
    ('Review invitation decisions, security profiles and department scope.',
     'Consulte convites, perfis de acesso e permissões por departamento.'), 'members', (
    Record('lia', LIA, ('Access approved', 'Acesso aprovado'), (
        (DEPARTMENT, SURVEY), (('Job', 'Função'), ('Survey technician', 'Técnica de levantamento')),
        (('Access profile', 'Perfil de acesso'), ('Field team member', 'Colaboradora de campo')),
        (('Selected permissions', 'Permissões selecionadas'),
         ('View inventory, record checks and submit her own timesheets.',
          'Consultar o inventário, registrar verificações e apresentar a própria folha de ponto.')),
        (('Invitation', 'Convite'), ('Accepted and approved by the department lead.', 'Aceito e aprovado pela chefia do departamento.'))),
        (('personnel','lia'),('time','lia-week'),('projects','aurora'))),
    Record('dora', DORA, ('Access approved', 'Acesso aprovado'), (
        (DEPARTMENT, HR), (('Access profile', 'Perfil de acesso'), ('HR supervisor', 'Supervisora de RH')),
        (('Selected permissions', 'Permissões selecionadas'), ('Review crew travel, documents and timesheets.',
          'Analisar viagens, documentos e folhas de ponto da equipe.'))),
        (('departments','hr'),('travel','lia-flight'))),
    Record('invite', ('Processing team invitation', 'Convite da equipe de processamento'), ('Awaiting acceptance', 'Aguardando aceite'), (
        (('Recipient', 'Destinatário'), name('training@example.invalid')),
        (('Planned access', 'Acesso previsto'), ('Profile only until a manager reviews the request.',
          'Apenas o próprio perfil até a análise da gestão.')),
        (('Delivery', 'Envio'), ('Fictional invitation history', 'Histórico fictício de convite')))),
    Record('request', ('Access request · Iara Monteiro', 'Solicitação de acesso · Iara Monteiro'), PENDING, (
        (DEPARTMENT, SURVEY),
        (('Requested role', 'Função solicitada'), ('Survey trainee', 'Estagiária de levantamento')),
        (('Suggested access', 'Acesso sugerido'), ('Read the assigned project inventory and complete assigned checklists.',
                                                  'Consultar o inventário do projeto e preencher os checklists atribuídos.')),
        (('Current access', 'Acesso atual'), ('Own profile only', 'Somente o próprio perfil')),
        (('Reviewer', 'Responsável pela análise'), ('Survey department manager', 'Gerência do departamento de levantamento')),
    ), (('access', 'invite'), ('projects', 'aurora'), ('departments', 'management'))),
))

AREAS = (
    PEOPLE,
    Area('departments','company',('Departments & responsibilities','Departamentos e responsabilidades'),
         ('See who receives requests and who can review them.','Veja quem recebe solicitações e quem pode analisá-las.'),'',(
        Record('management',('Management','Gerência'),ACTIVE,(
            (('Responsibility','Responsabilidade'),('Project approvals and department delegation.','Aprovações de projetos e delegação por departamento.')),
            (('Review scope','Escopo de análise'),('Assigned departments and authorised decisions.','Departamentos designados e decisões autorizadas.'))),
            (('projects','aurora'),('access','lia'))),
        Record('hr',HR,ACTIVE,((ASSIGNED,DORA),(('Notifications','Avisos'),('Personnel documents, timesheets and expenses.','Documentos pessoais, folhas de ponto e despesas.'))),
            (('personnel','lia'),('expenses','taxi'))),
        Record('it',IT,ACTIVE,((ASSIGNED,NILO),(('Notifications','Avisos'),('New IT tickets and replies from the requesting team.','Novos chamados de TI e respostas da equipe solicitante.'))),
            (('it','ticket-018'),)),
    )),
    Area('projects','company',('Projects','Projetos'),('Follow project responsibilities, assignments and equipment.','Acompanhe os responsáveis, as alocações e os equipamentos de cada projeto.'),'',(
        Record('aurora',PROJECT_NAME,ACTIVE,((('Client','Cliente'),name('Atlântica Pesquisa')),
            (LOCATION,('Training survey area A','Área de treinamento A')),(('Vessel','Embarcação'),VESSEL),
            (('Scope','Escopo'),('Survey equipment mobilisation and readiness checks.','Mobilização e verificação de equipamentos de levantamento.'))),
            (('schedule','aurora'),('inventory','sv204'),('shipments','mf014'))),
        Record('horizon',('OCN-002 · Horizon readiness','OCN-002 · Preparação Horizonte'),PLANNED,(
            (('Client','Cliente'),name('Farol Estudos')),(DEPARTMENT,FIELD),(NEXT,('Confirm vessel and crew dates.','Confirmar a embarcação e as datas da equipe.')))),
    )),
    Area('personnel','people',('Employee profiles & certificates','Perfis e certificados pessoais'),
         ('Open an employee profile and follow their document, trip and timesheet.','Abra o perfil de uma pessoa e consulte seu documento, sua viagem e sua folha de ponto.'),'hr',(
        Record('lia',LIA,('Scheduled offshore','Em escala de embarque'),((DEPARTMENT,SURVEY),
            (('Role','Função'),('Survey technician','Técnica de levantamento')),(PROJECT,PROJECT_NAME),
            (('Personal document','Documento pessoal'),('Offshore survival training, renewed for the next mobilisation.','Curso de sobrevivência offshore renovado para a próxima mobilização.'))),
            (('access','lia'),('personnel','survival'),('travel','lia-flight'),('time','lia-week'),('expenses','taxi'))),
        Record('survival',('Offshore survival training','Curso de sobrevivência offshore'),('Valid','Vigente'),(
            (PERSON,LIA),(('Expiry date','Vencimento'),name('27/08/2027')),
            (('Reminder','Lembrete'),('First reminder 90 days before expiry.','Primeiro lembrete 90 dias antes do vencimento.')),
            (EVIDENCE,name('TREINAMENTO-EXEMPLO.pdf'))),(('personnel','lia'),)),
    )),
    Area('schedule','people',('Crew schedule','Escalas da equipe'),('See shifts, project allocations and their department.','Consulte turnos, alocações em projetos e departamentos.'),'hr',(
        Record('aurora',('Aurora day shift','Turno diurno Aurora'),CONFIRMED,(
            (PERSON,LIA),(DEPARTMENT,SURVEY),(PERIOD,name('16–29/11/2026')),(LOCATION,VESSEL),
            (('Shift','Turno'),name('06:00–18:00 UTC'))),(('personnel','lia'),('projects','aurora'),('handovers','day'))),
    )),
    Area('travel','people',('Travel & tickets','Viagens e passagens'),('Review an itinerary and the documents shared with its traveller.','Veja o itinerário e os documentos compartilhados com a pessoa que vai viajar.'),'hr',(
        Record('lia-flight',('Mobilisation flight · Lia Prado','Voo de mobilização · Lia Prado'),CONFIRMED,(
            (PERSON,LIA),(('Itinerary','Itinerário'),name('Rio de Janeiro → Vitória')),(('Departure','Partida'),name('15/11/2026 · 09:40 BRT')),
            (EVIDENCE,name('BILHETE-EXEMPLO.pdf'))),(('personnel','lia'),('schedule','aurora'))),
    )),
    Area('time','people',('Timesheets & overtime','Folhas de ponto e horas extras'),('Read a submitted timesheet and the manager’s decision.','Consulte uma folha apresentada e a decisão da chefia.'),'hr',(
        Record('lia-week',('Timesheet · Lia Prado','Folha de ponto · Lia Prado'),APPROVED,((PERSON,LIA),(PROJECT,PROJECT_NAME),
            (PERIOD,name('09–13/11/2026')),(('Recorded hours','Horas registradas'),('40 regular hours + 2 overtime hours','40 horas regulares + 2 horas extras')),
            (('Review','Análise'),('Approved by the designated supervisor.','Aprovada pela supervisão designada.'))),
            (('personnel','lia'),('time','overtime'),('projects','aurora'))),
        Record('overtime',('Overtime · mobilisation','Horas extras · mobilização'),APPROVED,((PERSON,LIA),
            (('Time','Horário'),name('13/11/2026 · 17:00–19:00')),(('Reason','Motivo'),('Equipment handover at the shore base.','Entrega de equipamentos na base.'))),
            (('time','lia-week'),)),
    )),
    Area('expenses','people',('Expenses & receipts','Despesas e recibos'),('Review an expense, its receipt and its approval.','Veja uma despesa, seu recibo e a aprovação.'),'hr',(
        Record('taxi',('Airport transfer · Lia Prado','Traslado ao aeroporto · Lia Prado'),PENDING,(
            (PERSON,LIA),(('Amount','Valor'),name('R$ 86,50')),(('Category','Categoria'),('Ground transport','Transporte terrestre')),
            (EVIDENCE,name('RECIBO-EXEMPLO.pdf'))),(('travel','lia-flight'),('personnel','lia'))),
    )),
    Area('team','people',('Team feed','Feed da equipe'),('See recognition and an optional daily mood.','Veja reconhecimentos e o registro opcional de humor do dia.'),'team',(
        Record('thanks',('Thanks for the mobilisation','Agradecimento pela mobilização'),('Shared','Compartilhado'),(
            (('From','De'),NILO),(('To','Para'),LIA),(('Message','Mensagem'),('The cases were labelled before the vessel arrived.','As maletas já estavam identificadas quando a embarcação chegou.')))),
        Record('mood',('Daily mood · Lia Prado','Humor do dia · Lia Prado'),('Shared with the team','Compartilhado com a equipe'),(
            (('Mood','Humor'),('😊 Feeling good','😊 Estou bem')),(('Visibility','Visibilidade'),('Visible to the team until the end of that day.','Visível à equipe até o fim daquele dia.')))),
    )),
    Area('it','work',('IT requests','Solicitações de TI'),('Follow a support request from the employee to the IT team.','Acompanhe um chamado desde a abertura até o atendimento da equipe de TI.'),'it',(
        Record('ticket-018',('IT-018 · Workstation network dropouts','TI-018 · Quedas de rede na estação'),('In progress','Em atendimento'),(
            (('Requested by','Solicitante'),LIA),(ASSIGNED,NILO),(('Priority','Prioridade'),('High','Alta')),
            (('Latest reply','Última resposta'),('IT replaced the patch cable and is monitoring the connection.','A TI trocou o cabo de rede e está acompanhando a conexão.')),
            (EVIDENCE,name('PORTA-REDE-EXEMPLO.pdf'))),(('departments','it'),('personnel','lia'),('projects','aurora'))),
    )),
    Area('tasks','work',('Operational tasks','Tarefas operacionais'),('Check the assignment, instructions and expected outcome.','Consulte o responsável, as instruções e o resultado esperado.'),'tasks',(
        Record('pack',('Reconcile case 04','Conferir a maleta 04'),('In progress','Em andamento'),(
            (ASSIGNED,LIA),(PROJECT,PROJECT_NAME),(('Instructions','Instruções'),('Check the probe serial number against the manifest.','Conferir o número de série da sonda com o manifesto.'))),
            (('inventory','sv204'),('shipments','mf014'))),
    )),
    Area('handovers','work',('Shift handovers','Passagens de turno'),('Read a handover and outstanding work for the next shift.','Consulte a passagem e o trabalho pendente para o próximo turno.'),'handovers',(
        Record('day',('Aurora · day to night shift','Aurora · turno diurno para noturno'),('Published','Publicada'),(
            (DEPARTMENT,SURVEY),(LOCATION,VESSEL),(('Shift note','Observação'),('Case 04 has arrived on deck. The receiving check is pending.','A maleta 04 chegou ao convés. Falta a conferência do recebimento.'))),
            (('schedule','aurora'),('shipments','mf014'))),
    )),
    Area('checklists','work',('Checklists','Listas de verificação'),('Review a completed stage and its equipment evidence.','Consulte uma etapa concluída e a evidência do equipamento.'),'checklists',(
        Record('deck',('Survey equipment mobilisation','Mobilização de equipamentos de levantamento'),('In progress','Em andamento'),(
            (ASSIGNED,LIA),(('Stage 1','Etapa 1'),('Case label matches the manifest.','A etiqueta da maleta corresponde ao manifesto.')),
            (NEXT,('Record the probe serial number.','Registrar o número de série da sonda.'))),(('inventory','sv204'),('tasks','pack'))),
    )),
    Area('logs','work',('Logbooks & calendar','Livros de registro e calendário'),('Read a log entry and follow its associated activity.','Leia um registro e acompanhe sua atividade associada.'),'logs',(
        Record('deck',('Deck log · case arrival','Diário de convés · chegada da maleta'),SAVED,(
            (LOCATION,VESSEL),(('Logged at','Registrado em'),name('16/11/2026 · 10:20 UTC')),
            (('Entry','Registro'),('Transport case 04 received on deck.','Maleta de transporte 04 recebida no convés.'))),(('shipments','mf014'),('schedule','aurora'))),
    )),
    Area('inventory','equipment',('Inventory & boxes','Inventário e caixas'),('Follow the storage path down to an individual item.','Percorra as pastas até encontrar um item e sua localização.'),'inventory',(
        Record('base',('Shore base','Base em terra'),('Location','Local'),((('Contents','Conteúdo'),('Survey store → transport case 04','Almoxarifado de levantamento → maleta de transporte 04')),),(('inventory','store'),)),
        Record('store',('Survey store','Almoxarifado de levantamento'),('Folder','Pasta'),((LOCATION,('Shore base','Base em terra')),(('Contents','Conteúdo'),FOLDER)),(('inventory','base'),('inventory','case04'))),
        Record('case04',FOLDER,('Box','Caixa'),((LOCATION,('Shore base / Survey store','Base em terra / Almoxarifado de levantamento')),
            (('Item in the case','Item na maleta'),EQUIPMENT)),(('inventory','store'),('inventory','sv204'))),
        Record('sv204',EQUIPMENT,('Ready','Pronto para uso'),((('Serial number','Número de série'),name('FIC-SV-0204')),
            (LOCATION,('Shore base / Survey store / Transport case 04','Base em terra / Almoxarifado de levantamento / Maleta de transporte 04')),
            (('Quantity','Quantidade'),name('1')),(PROJECT,PROJECT_NAME)),(('inventory','case04'),('certificates','cal204'),('shipments','mf014'))),
    )),
    Area('certificates','equipment',('Equipment certificates','Certificados de equipamentos'),('Trace a calibration certificate to its inventory item.','Consulte o certificado de calibração e o item de inventário correspondente.'),'certificates',(
        Record('cal204',('CAL-204 · Probe calibration','CAL-204 · Calibração da sonda'),('Valid','Vigente'),(
            (('Equipment','Equipamento'),EQUIPMENT),(('Expiry date','Vencimento'),name('14/09/2027')),(EVIDENCE,name('CAL-204-EXEMPLO.pdf'))),(('inventory','sv204'),)),
    )),
    Area('fleet','equipment',('Fleet & vessels','Frota e embarcações'),('Review a vessel, its project and its incoming shipment.','Consulte a embarcação, seu projeto e a remessa prevista.'),'fleet',(
        Record('aurora',VESSEL,('Mobilising','Em mobilização'),((PROJECT,PROJECT_NAME),(('Destination','Destino'),('Training survey area A','Área de treinamento A')),
            (('Receiving area','Área de recebimento'),('Aft deck','Convés de popa'))),(('projects','aurora'),('shipments','mf014'))),
    )),
    Area('shipments','equipment',('Manifests & receiving','Manifestos e recebimento'),('Trace a shipment, its contents and the receiving decision.','Acompanhe uma remessa, seu conteúdo e a conferência no destino.'),'shipments',(
        Record('mf014',SHIPMENT,('At receiving','Em recebimento'),((('Origin','Origem'),('Shore base','Base em terra')),
            (('Destination','Destino'),VESSEL),(('Contents','Conteúdo'),FOLDER),(NEXT,('Verify the serial number before placement.','Conferir o número de série antes de confirmar a localização.'))),
            (('inventory','case04'),('inventory','sv204'),('fleet','aurora'))),
    )),
    Area('maintenance','equipment',('Maintenance & faults','Manutenção e falhas'),('Follow a work order and the issue that triggered it.','Acompanhe a ordem de serviço e a falha que a originou.'),'maintenance',(
        Record('os17',('WO-017 · Inspect transit case','OS-017 · Inspeção da maleta'),PLANNED,(
            (ASSIGNED,LIA),(('Reported fault','Falha registrada'),('Loose latch on an empty spare case.','Trava solta em uma maleta reserva vazia.')),
            (NEXT,('Check the replacement latch before release.','Verificar a nova trava antes da liberação.'))),(('projects','aurora'),)),
    )),
    Area('safety','safety',('Safety, quality & toolbox talks','Segurança, qualidade e diálogos de segurança'),('Review a safety observation, evidence and the follow-up briefing.','Consulte uma observação, a evidência e o diálogo de segurança relacionado.'),'qshe',(
        Record('route',('Clear deck access route','Liberar o acesso no convés'),('Action assigned','Ação atribuída'),(
            (LOCATION,VESSEL),(ASSIGNED,LIA),(('Observation','Observação'),('An empty transit case was moved from the marked walkway.','Uma maleta vazia foi retirada da passagem demarcada.')),
            (EVIDENCE,name('CONVES-EXEMPLO.pdf'))),(('safety','briefing'),)),
        Record('briefing',('Toolbox talk · deck access','Diálogo de segurança · acesso ao convés'),('Completed','Concluído'),(
            (('Topic','Tema'),('Keep the marked walkway clear during mobilisation.','Manter a passagem demarcada livre durante a mobilização.')),
            (('Attendance','Presença'),('Five training participants','Cinco participantes fictícios'))),(('safety','route'),)),
    )),
    Area('documents','safety',('Original files & revisions','Arquivos originais e revisões'),('Inspect document ownership, revision and linked equipment.','Consulte o responsável pelo documento, a revisão e o equipamento vinculado.'),'originals',(
        Record('manifest',('Mobilisation manifest · revision 2','Manifesto de mobilização · revisão 2'),('Current revision','Revisão vigente'),(
            (('Folder','Pasta'),('Logistics / Mobilisation','Logística / Mobilização')),(('File','Arquivo'),name('MF-014-EXEMPLO.xlsx')),
            (('Change','Alteração'),('Added the probe serial number.','Inclusão do número de série da sonda.'))),(('shipments','mf014'),('inventory','sv204'))),
    )),
    Area('builders','safety',('Builders & assisted import','Editores e importação com IA'),('Inspect a template and an example of editable suggestions.','Consulte um modelo e um exemplo de sugestões que a equipe pode editar.'),'builders',(
        Record('map',('Manifest column mapping','Mapeamento das colunas do manifesto'),('Example suggestion','Sugestão de exemplo'),(
            (('Source file','Arquivo de origem'),name('MF-014-EXEMPLO.xlsx')),(('Source columns','Colunas de origem'),name('Descrição | N.º de série | Quantidade | Caixa')),
            (('Mapped fields','Campos identificados'),('Item name, serial number, quantity and box.','Nome do item, número de série, quantidade e caixa.')),
            (NEXT,('The editor can correct each suggested field before importing.','A pessoa pode corrigir cada campo sugerido antes de importar.'))),
            (('documents','manifest'),('inventory','sv204'),('builders','checklist'))),
        Record('checklist',('Mobilisation checklist template','Modelo de checklist de mobilização'),SAVED,(
            (('Stage','Etapa'),('Inspect equipment labels.','Inspecionar as etiquetas dos equipamentos.')),
            (('Field type','Tipo de campo'),('Pass/fail check with an optional photo.','Verificação de conformidade com foto opcional.'))),(('checklists','deck'),)),
    )),
    Area('records', 'company', ('Record management', 'Gestão de registros'),
         ('Review a record’s current version and its change history.',
          'Consulte a versão vigente de um registro e o histórico de alterações.'), '', (
        Record('revision', ('Manifest revision history', 'Histórico de revisões do manifesto'),
               ('Revision 2 is current', 'Revisão 2 vigente'), (
                   (('Record', 'Registro'), SHIPMENT),
                   (('Revision 1', 'Revisão 1'), ('Case 04 listed at the shore base.', 'Maleta 04 registrada na base em terra.')),
                   (('Revision 2', 'Revisão 2'), ('The team added serial FIC-SV-0204 at dispatch.',
                                                'A equipe adicionou a série FIC-SV-0204 na expedição.')),
               ), (('documents', 'manifest'), ('inventory', 'sv204'))),
    )),
    Area('branding', 'company', ('Report branding', 'Identidade visual dos relatórios'),
         ('Open a report sample with the company name, project and revision.',
          'Abra um exemplo de relatório com o nome da empresa, o projeto e a revisão.'), '', (
        Record('cover', ('Mobilisation report cover', 'Capa do relatório de mobilização'), SAVED, (
            (('Company', 'Empresa'), name('Maré Alta Surveys')),
            (PROJECT, PROJECT_NAME), (('Revision', 'Revisão'), name('02')),
            (('Footer', 'Rodapé'), ('Training copy · Operations', 'Exemplar de treinamento · Operações')),
            (EVIDENCE, name('OCN-001-EXEMPLO.pdf')),
        ), (('projects', 'aurora'), ('documents', 'manifest'))),
    )),
    Area('log-design', 'company', ('Logbook designer', 'Editor de livros de registro'),
         ('See how a log template defines the fields filled in on deck.',
          'Veja como o modelo define os campos preenchidos no convés.'), '', (
        Record('deck', ('Deck log template', 'Modelo de diário de convés'), ACTIVE, (
            (('Text field', 'Campo de texto'), ('Activity description', 'Descrição da atividade')),
            (('Time field', 'Campo de hora'), ('Event time in UTC', 'Horário do evento em UTC')),
            (('Choice field', 'Campo de seleção'), ('Arrival, inspection or dispatch', 'Chegada, inspeção ou expedição')),
        ), (('logs', 'deck'), ('handovers', 'day'))),
    )),
    Area('site-access', 'company', ('Fleet & site access', 'Acesso à frota e às bases'),
         ('Inspect the locations and responsibilities assigned to a crew member.',
          'Consulte os locais e as responsabilidades atribuídos a uma pessoa da equipe.'), '', (
        Record('aurora', ('Aurora receiving team', 'Equipe de recebimento do Aurora'), ACTIVE, (
            (('Vessel', 'Embarcação'), VESSEL), (PERSON, LIA),
            (('Site', 'Base'), ('Aurora aft deck', 'Convés de popa do Aurora')),
            (('Scope', 'Escopo'), ('View incoming manifests and confirm receipt at the assigned site.',
                                  'Consultar manifestos de entrada e confirmar o recebimento no local atribuído.')),
        ), (('fleet', 'aurora'), ('shipments', 'mf014'), ('access', 'lia'))),
    )),
    Area('alerts', 'people', ('Alerts & reminders', 'Avisos e lembretes'),
         ('See what an employee and their reviewer are asked to follow up.',
          'Veja quais pendências são apresentadas à equipe e à pessoa responsável pela análise.'), '', (
        Record('expiry', ('Personal document reminder', 'Lembrete de documento pessoal'),
               ('Scheduled', 'Programado'), (
                   (PERSON, LIA), (DEPARTMENT, HR),
                   (('Trigger', 'Gatilho'), ('90 days before the certificate expires.', '90 dias antes do vencimento do certificado.')),
               ), (('personnel', 'survival'), ('personnel', 'lia'))),
        Record('expense', ('Expense awaiting review', 'Despesa aguardando análise'), PENDING, (
            (PERSON, LIA), (ASSIGNED, DORA), (('Amount', 'Valor'), name('R$ 86,50')),
        ), (('expenses', 'taxi'), ('departments', 'hr'))),
    )),
)
BY_AREA = {area.key: area for area in AREAS}
BY_RECORD = {(area.key, record.key): record for area in AREAS for record in area.records}

# Match the eight sections of the company browser's Administration menu. Two
# sections lead into different examples in the shared builders workspace.
ADMIN_SECTIONS = (
    ('users', ('People & access', 'Pessoas e acesso'), 'access', ''),
    ('departments', ('Departments', 'Departamentos'), 'departments', ''),
    ('records', ('Record management', 'Gestão de registros'), 'records', ''),
    ('imports', ('Imports & examples', 'Importações e exemplos'), 'builders', 'map'),
    ('company', ('Report branding', 'Identidade visual dos relatórios'), 'branding', ''),
    ('templates', ('Templates & routines', 'Modelos e rotinas'), 'builders', 'checklist'),
    ('logbooks', ('Logbook designer', 'Editor de livros de registro'), 'log-design', ''),
    ('fleet', ('Fleet & site access', 'Acesso à frota e às bases'), 'site-access', ''),
)
