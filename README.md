# Wavelink — UI136 integrada localmente

Versão 1.34.36. Base GitHub UI135: 9af487ff83b38f8d1efba050cb3e4179197279c2. Repositório completo, com cadeia anterior preservada. Esta rodada não publica nem acessa dados reais.

## Alterações

- RH: pessoas, escalas e despesas: Seletores distinguem homônimos com identificadores já autorizados, preservando o ID do cadastro. Histórico mostra carregamento, erro e vazio e ignora respostas de outro contexto. Fluxos de escala e correção de despesa foram confrontados com respostas reais do servidor local.
- Certificados e perfil do equipamento: Contagem de revisões atuais corresponde ao filtro, sem confundir revisão atual no cadastro com validade. Cadastro de certificados de equipamentos fica distinto de documentos RH. Ajuda associada aos campos, foco controlado e falhas exibidas junto ao anexo; perfil exibe datas e situações conhecidas em português.
- Tarefas e manutenção: Buscas aceitam texto sem acentos e identificadores existentes. Retorno e limpeza de filtros preservam contexto e foco. Retomar tarefa tem rótulo próprio; limite de justificativa de cancelamento coincide com o servidor. Leituras tardias do diretório não abrem assistente em outra tela.
- Busca global e central de ações: Filtros e respostas pertencem à consulta e conta que os iniciaram. Busca parcial é identificada; limites de 40 resultados e 75 ações são explicados. Preferências em edição sobrevivem à atualização, possuem recarga explícita e repetição exata após falha. Ação pendente pode ser repetida mesmo fora da lista.

## Validação

48 testes Python distintos, 93 suítes JavaScript e 114 arquivos JavaScript com sintaxe aprovada. Os 2418 recursos reconstruídos pela cadeia completa coincidem por SHA-256 com a versão final. DELIVERY_CHECKS.json e validation/ registram resultados, limitações e identidade da versão.

docs/UI136-previas contém exemplos reais de componentes com dados fictícios, incluindo comparação da central de ações entre UI135 e UI136. São HTML portáteis, não screenshots. Os testes de transporte, fotos e DOM simulados não comprovam layout, SMTP ou produção.

## Usar o pacote

Extraia em uma pasta nova. Compare com o GitHub mais recente antes de aplicar, preservando trabalho posterior. Não crie outro serviço ou disco e não leve bases de teste para produção. O pacote não contém banco real, .env ou credenciais de produção.
Para reconstruir todo o código-fonte em uma pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. A cadeia verifica cada etapa e recusa base incompatível.

## Backup e reversão

A base local UI135 e o ZIP anterior foram preservados e conferidos. Não foi criado backup de produção, que não foi acessada. Antes de publicação futura, conferir a versão instalada e fazer backup verificado do banco/disco existentes.
Esta etapa não introduz tabela, migração ou contrato novo de gravação. Reverter para a UI135 correspondente não exige conversão de dados introduzida pela UI136. Permanecem as restrições anteriores: após salvar contatos na UI131, voltar só o código para UI130 é bloqueado; código e dados precisam ser compatíveis.

Admin, usuário temporário, permissões e dados reais não foram alterados. Leia docs/UI136_GUIA.html, docs/UI136-cobertura.json e docs/UI136-pendencias.json para distinguir implementação, validação local e pendências.
