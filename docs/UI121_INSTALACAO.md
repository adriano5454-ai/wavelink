# UI121 — RH e Operações / Wavelink 1.34.21

Entrega preparada e testada localmente, sobre main c435332618811aa29ac59e856a5ed922513f4e5e (UI119 com UI118). Inclui a UI120 de RH brasileiro. Nenhum commit/deployment foi publicado; Render, DNS, domínio, usuários e dados reais não foram modificados.

## Repositório completo

O formato original é preservado: vendor/source.part* contém a fonte original e deploy/apply_ui*.py aplica as atualizações verificadas. O Dockerfile inclui UI121 ao final. Para obter todos os arquivos legíveis:

    python deploy/materialize_runtime.py ./runtime-ui121

Use um diretório novo. A ferramenta confere as etapas e todos os 2268 arquivos finais, sem iniciar o aplicativo. Manifesto final: 06a5e6b85ca3b1e925976405f2f6ea473578501f002d358f155241db7ef81584. UI121_RUNTIME_DIFF.patch mostra as alterações legíveis; UI121_SOURCE_PROVENANCE.json lista seus hashes. O instalador recusa uma base modificada antes de escrever.

## Publicação posterior

Compare o main com o commit-base e preserve trabalho posterior. Faça backup recente verificado da empresa, com todos os processos gravadores realmente parados e com o proprietário dos arquivos, antes da publicação da cadeia UI120/UI121. O pacote não inclui nem substitui esse backup.

Construa primeiro em homologação: docker build -t wavelink:ui121 . A imagem Linux/Render ainda precisa ser validada. Na publicação autorizada, preserve o mesmo serviço, disco, COMPANY_ID, COMPANY_NAME, PUBLIC_URL, segredos e diretório persistente. INITIALISE_COMPANY permanece NO. Não execute limpeza, reset, rename_company.py nem importação da demo.

Valide login, dados e anexos existentes, rascunhos, permissões, idioma, escalas, revisões, exportações e Operações. Não habilite envio real de e-mails apenas para testar.

## Navegação e permissões

Pessoas → Recursos Humanos oferece Visão geral, Calendário e escalas, Colaboradores, Relatórios e Aprovações pendentes. Registros e solicitações reúne documentos, escalas/viagens, apontamentos e despesas. Retomar Operações reabre a última rota da sessão; trocar de identidade reinicia esse contexto sem apagar rascunhos.

O calendário tem linha do tempo, lista e equipe no período, além de cartões no celular. Local, projeto e lotação ficam nos filtros expansíveis. Escala é programação prevista; ausência de escala não comprova disponibilidade. O cadastro usa as identidades existentes e separa contatos privados do perfil público.

UI121 não amplia permissões. A UI120 inclui hr.people_manage, concedida deliberadamente ao responsável pelo cadastro. As capacidades existentes são hr.view_own, hr.documents_submit/manage, hr.shifts_manage, hr.travel_manage, hr.timesheets_submit/review e hr.expenses_submit/review. Filtro de departamento não é fronteira de autorização. Consulte UI120_INSTALACAO.md para detalhes.

## Reproduzir testes

Instale requirements.lock e tests/requirements-ui120.txt em ambiente próprio. Com a árvore reconstruída:

    python tests/run_ui121_checks.py ./runtime-ui121 --junitxml ./ui121-results.xml
    node ./runtime-ui121/tests/test_ui121_experience.cjs
    node ./runtime-ui121/tests/test_hr_forms_ui120.cjs

Os testes usam contas fictícias. UI121_VALIDACAO.json separa testes automatizados, Chrome e pendências. A execução registrada combina a rodada principal e verificações posteriores; não é apresentada como uma única rodada completa sem falhas.

## Reversão e limites

Guarde o pacote anterior e backup recente. UI121 não altera esquema, identificadores ou permissões em relação à UI120; é possível voltar à UI120 sem converter dados. Voltar à UI119 retira funcionalidades de RH da UI120 e exige revisão de compatibilidade/backup. Nunca restaure automaticamente backup antigo sobre registros novos.

Não há folha de pagamento, ponto regulamentado, pagamento de reembolso, reserva de viagem ou decisão de aptidão. Cobertura exige necessidade e escalas confirmadas vinculadas. Consultas mantêm limites de 93 dias, 3000 registros e 500 necessidades. Desempenho com grande volume e aceitação pela equipe real precisam de homologação.
