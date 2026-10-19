# Wavelink — UI132 integrada localmente

Versão 1.34.32. Base GitHub: f26f38da92cd0ee8dfbc29dfa007a0eb7ea5d86c (UI131); inclui toda a UI131 preservada e a UI132. Nenhum commit, deployment ou serviço foi alterado nesta rodada.

## Alterações

- Documentos relacionados: comprovantes de despesas no perfil, fotos de manutenção no item, anexos de passagens no perfil do autor e arquivos de manifestos vinculados ao item. Cada família usa sua autorização e download próprios. Mantém certificados, fontes exatas e pastas dos Originais da UI131.
- Tarefas: cada responsável pode registrar seu aceite explícito. Ler o alerta, executar e aprovar são ações distintas. Mudança de responsáveis/reabertura pede novo aceite; evidências anteriores ficam no histórico. Os relatórios novos incluem o aceite separado do andamento.
- Visual: hierarquia, metadados legíveis, controles e foco visíveis, seleção textual e apresentação em telas pequenas nas áreas operacionais. Matriz de 193 vistas, com 163 fontes restantes inspecionadas; isso não significa 193 jornadas testadas em navegador.
- Ajuda e linguagem: português brasileiro para Corcovado e inglês preservado nas outras instalações.

## Validação

59 testes Python distintos e 64 suítes JavaScript aprovados; 2369 recursos reconstruídos da cadeia completa e conferidos por SHA-256. Evidências em DELIVERY_CHECKS.json e validation/. Os testes usam dados fictícios. Prévias HTML em docs/UI132-previas; não são screenshots.
Não houve Chrome, publicação, envio de mensagem, acesso ao banco real ou alteração de admin/usuário temporário.

## Usar o pacote

Extraia em uma pasta nova. Compare com o repositório mais recente antes de aplicar no GitHub Desktop e preserve trabalho posterior. O ZIP mantém a estrutura completa do repositório de implantação existente; não copie bancos de teste nem crie outro serviço/disco.
Para materializar todo o código-fonte em uma pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. O processo verifica a cadeia de recursos antes de aplicar a UI132.

## Backup e reversão

A base UI131 local foi mantida intacta. Não foi criado nem alterado backup de produção, pois esta rodada não a acessou. Antes de uma publicação futura, faça backup verificado do banco/disco existente.
O aceite acrescenta metadados ao corpo da tarefa e eventos à auditoria existente. Backups completos e cópias seletivas com tarefas preservam sua origem. A UI132 invalida um aceite quando encontra reatribuição/reabertura posterior, inclusive alterações de um escritor UI131. Versões antigas não exibem esse aceite.
A proteção de contatos da UI131 continua valendo: após o primeiro salvamento de contatos, retornar somente o código para UI130 é bloqueado. Uma reversão completa exige código compatível e backup anterior verificado, com gravações paradas; pode perder mudanças posteriores. Prefira corrigir para frente.
Leia docs/UI132-pendencias.json e docs/UI132_GUIA.html antes de publicar.
