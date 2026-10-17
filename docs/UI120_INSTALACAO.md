# Instalação e revisão — UI120 / Wavelink 1.34.20

## Estado desta entrega
Pacote completo preparado a partir de adriano5454-ai/wavelink, main c435332618811aa29ac59e856a5ed922513f4e5e (UI119), que inclui UI118. UI120 foi testada localmente com contas fictícias. Este trabalho não publica código nem muda Render, DNS, domínio, banco ou usuários da Corcovado. O pacote não contém banco de produção, senhas de usuários nem documentos reais.

O repositório conserva seu formato: fonte original em vendor/source.part*, seguida das atualizações verificadas deploy/apply_ui*.py. O Dockerfile inclui UI120 ao final. Não é um ZIP somente de alterações. Para obter a árvore completa e legível do aplicativo, execute:

    python deploy/materialize_runtime.py ./runtime-ui120

O destino deve ser novo. A ferramenta valida cada etapa, todos os recursos finais e não inicia o aplicativo. Consulte docs/UI120_SOURCE_PROVENANCE.json e DEPLOYMENT_FILES.json para os hashes. Não edite um overlay antigo para contornar divergências de versão.

## Instalar uma atualização de um serviço existente
1. Compare o main atual com o commit-base acima. Caso haja trabalho posterior, integre-o em uma cópia separada e refaça os testes; o instalador recusa uma base diferente. Preserve especialmente UI118, UI119 e a migração Corcovado.
2. Faça backup verificado do diretório completo da empresa com os processos gravadores parados de fato, como o proprietário dos arquivos. Confira integridade do SQLite e possibilidade de restauração. Uma tela de manutenção não substitui a parada dos processos. Não use um backup antigo como se fosse o ponto de recuperação desta atualização.
3. Construa e valide primeiro em homologação: docker build -t wavelink:ui120 . O build de imagem Linux/Render ainda precisa ser executado no ambiente de publicação; a reconstrução do aplicativo e os testes Python/JavaScript foram realizados localmente.
4. Na publicação autorizada, use o mesmo serviço, disco, modo COMPANY e diretório persistente. Preserve COMPANY_ID, COMPANY_NAME, PUBLIC_URL, segredos de e-mail/autenticação e todos os demais parâmetros existentes. INITIALISE_COMPANY deve continuar NO. Não importe FICTIONAL_DEMO.ajproject; ele é um recurso anterior preservado no repositório, não a inicialização da Corcovado.
5. Não execute rename_company.py nem qualquer limpeza/reset novamente. A mudança de identidade e o reset anterior são independentes desta versão.
6. Após publicar, valide login, Recursos Humanos, permissões de cada conta, leitura dos registros existentes, anexos privados, rascunhos, filtros, exportações e retorno a Operações. Teste notificações conforme as preferências reais antes de habilitar novos envios.

## Onde encontrar
Pessoas → Recursos Humanos abre uma área própria: Visão geral; Calendário e escalas; Colaboradores; Relatórios; Documentos pessoais; Escalas e viagens; Apontamento de horas; Despesas e reembolso; Aprovações pendentes. “Voltar a Operações” abre o início operacional.

O calendário oferece agenda diária e tabela de equipe, com filtros de período (até 93 dias), colaborador, embarcação/local, projeto e lotação/departamento. Em telas estreitas, vira uma agenda vertical. Sobreposição é um alerta para revisão, inclusive na troca de turma no mesmo dia; não há decisão automática sobre aptidão.

Em Calendário e escalas, cadastre uma necessidade de equipe e vincule escalas a ela. A cobertura por dia conta pessoas distintas com programação confirmada; não soma a mesma pessoa duas vezes. A referência do ciclo de trabalho/folga não gera automaticamente novas escalas. Cadastre a folga ou afastamento em um registro próprio para refletir a programação real.

Em Colaboradores, reutilize contas e lotações existentes. A criação de conta continua em Administração → Usuários e acesso (ou pelo fluxo existente de convite). Não existe uma segunda lista independente de identidades de RH.

## Permissões
A administração escolhe deliberadamente quais capacidades cada conta recebe. As permissões de gestão/revisão existentes têm abrangência da empresa; o filtro de departamento é de consulta, não uma restrição de segurança por departamento.

| Perfil de uso | Capacidades |
|---|---|
| Colaborador | hr.view_own e, conforme a função, hr.documents_submit, hr.timesheets_submit, hr.expenses_submit. Contatos próprios editáveis; dados profissionais mantidos pelo RH. |
| RH de cadastro | Nova hr.people_manage, para contatos/dados profissionais privados de outros colaboradores. Não é habilitada automaticamente para não administradores. |
| RH documental | hr.documents_manage. Conferência por pessoa diferente do titular e de quem alterou a evidência. |
| Planejamento / viagens | hr.shifts_manage para escalas, necessidades e cobertura; hr.travel_manage para viagens. Não concedem acesso a passaportes ou dados médicos de terceiros. |
| Supervisor / revisor | hr.timesheets_review e/ou hr.expenses_review. Autoaprovação bloqueada, inclusive para administrador. |

Perfil público, Equipe, busca geral e páginas operacionais não passam a expor os contatos ou documentos privados. Relatórios usam somente registros retornados para a conta autorizada. A exportação completa de backup continua restrita por sua política anterior.

## Dados e reversão
A alteração é aditiva, utilizando as tabelas privadas existentes de RH: registros, anexos, auditoria e recibos de operação. Não muda IDs de contas, senhas, equipamentos, departamentos, inventário nem documentos históricos. Pessoas e necessidades são novos tipos; a conferência é registrada separadamente da validade. Arquivos retirados permanecem no histórico conforme a política existente. Não há substituição indiscriminada de textos no banco.

Registros anteriores sem conferência explícita aparecem como “Aguardando conferência”; não ganham aprovação fictícia. Escalas antigas recebem valores de leitura conservadores, sem fabricar necessidade de equipe, disponibilidade ou documentos exigidos. Edição por clientes antigos conserva campos novos omitidos quando aplicável; evite manter clientes antigos gravando durante a troca.

Para reversão após gravações UI120, pare os gravadores e prefira correção para frente. Restauração do backup pré-publicação precisa preservar/reconciliar o trabalho posterior. Não foi validada operação de UI119 sobre dados novos UI120; não faça downgrade cego nem apague os novos tipos para fazê-lo funcionar.

## Limites e validações restantes
- Cobertura exige necessidade cadastrada e vínculo explícito; não comprova presença, habilitação documental ou aptidão médica. Confirmações concluídas historicamente contam como programação registrada, não como ponto realizado.
- Consulta limitada a 3.000 registros acessíveis e 500 necessidades. O limite é sinalizado; cobertura incompleta não é apresentada como cálculo confiável. Documentos são consultados pelo acervo ativo, não apenas por data de emissão.
- Filtro por local/projeto seleciona escalas e seus colaboradores; documentos/horas/despesas dessas pessoas não são atribuídos automaticamente ao mesmo projeto. Cobertura de necessidades considera a equipe inteira, mesmo com filtro de pessoa/departamento, conforme a ajuda exibida.
- Não há folha de pagamento, banco de horas, registro eletrônico de ponto, execução de pagamento/reembolso, compra de passagem, validação externa de certificados ou integração eSocial.
- Relatórios são tabelas e CSV, incluindo cobertura. CSV neutraliza fórmulas e separa programação, conferência e aprovação; não é um demonstrativo de pagamento.
- Histórico, limites de upload, proteção de anexos e revisão independente permanecem. Prévia de imagens foi validada no Chrome; prévia de PDF depende do visualizador do navegador e oferece download autenticado como alternativa.
- Testes de e-mail deste pacote usam infraestrutura simulada; não foram enviados e-mails ou mensagens a terceiros. Publicação, imagem Linux, desempenho em grande volume e aceite dos fluxos com a equipe real ainda precisam de validação.

Consulte UI120_VALIDACAO.json para a evidência executada e UI120_GLOSSARIO_FONTES.md para o vocabulário pesquisado.

## Reproduzir os testes selecionados
Use Python 3.12 (versão utilizada nesta validação) e Node.js em uma cópia local isolada, com as dependências de produção e as dependências adicionais de teste instaladas. Os testes criam empresas e contas fictícias temporárias. Não aponte variáveis de dados para a empresa real.

    python -m pip install -r requirements.lock -r tests/requirements-ui120.txt
    python deploy/materialize_runtime.py ./runtime-ui120
    python tests/run_ui120_checks.py ./runtime-ui120 --junitxml=ui120-resultados.xml
    node runtime-ui120/tests/test_hr_forms_ui120.cjs

O relatório entregue contém 187 aprovações na primeira execução Python e três verificações estáticas antigas corrigidas e aprovadas na repetição (190 casos únicos no total). Não representa uma única execução integral sem falhas. As três expectativas antigas se referiam a versões de recursos e caminho/hash do inicializador, não a falhas de fluxo de RH. O comando acima seleciona os mesmos 190 casos na versão final. O teste JavaScript executa 16 verificações de comportamento dos formulários e exportação.
