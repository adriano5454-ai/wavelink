# Wavelink — UI135 integrada localmente

Versão 1.34.35. Base GitHub UI134: 3aaf822ea05661f9f2baa1d24bcf0bbef53c4a52. Repositório completo, com cadeia anterior preservada. Esta rodada não publica nem acessa dados reais.

## Alterações

- RH: formulários e relatórios: Cancelar compara o conteúdo real: restaurar os valores originais deixa de provocar aviso desnecessário. A justificativa de devolução/rejeição é identificada e recebe foco quando falta. Relatórios exibem período, abrangência e critério real de cobertura; CSV e mensagens mantêm português e inglês separados.
- Checklists e documentos originais: Leitura numérica 0 e revisão 0 continuam visíveis na edição. Campos indicam obrigatoriedade e limites de forma acessível. Revisão traduz situações e distingue conferir, devolver e finalizar. Envio de original anuncia resultado e mantém foco sem interromper outra ação.
- Conta, perfil, equipe e alertas: Telas e ações conferem a sessão antes do envio e após respostas. Permissões usam os nomes do catálogo em português. Preferências de e-mail preservam rascunho apenas na mesma conta/empresa; envio incerto mantém a tentativa original. Histórico e feed explicam seus limites existentes.
- Início e navegação administrativa: Datas inválidas recebem mensagem junto ao campo. Período UTC aplicado, carregamento e erro ficam explícitos. Página vazia retorna ao começo mantendo filtros. Foco acompanha navegação solicitada e respeita outra ação do usuário. Abas e seções selecionadas usam indicação além da cor.

## Validação

31 testes Python distintos, 84 suítes JavaScript e 114 arquivos JavaScript com sintaxe aprovada. Os 2404 recursos reconstruídos pela cadeia completa coincidem por SHA-256 com a versão final. DELIVERY_CHECKS.json e validation/ registram resultados, limitações e identidade da versão.

docs/UI135-previas contém exemplos reais de componentes com dados fictícios, incluindo comparação do Início entre UI134 e UI135. São HTML portáteis, não screenshots. Os testes de transporte, fotos e DOM simulados não comprovam layout, SMTP ou produção.

## Usar o pacote

Extraia em uma pasta nova. Compare com o GitHub mais recente antes de aplicar, preservando trabalho posterior. Não crie outro serviço ou disco e não leve bases de teste para produção. O pacote não contém banco real, .env ou credenciais de produção.
Para reconstruir todo o código-fonte em uma pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. A cadeia verifica cada etapa e recusa base incompatível.

## Backup e reversão

A base local UI134 e o ZIP anterior foram preservados e conferidos. Não foi criado backup de produção, que não foi acessada. Antes de publicação futura, conferir a versão instalada e fazer backup verificado do banco/disco existentes.
Esta etapa não introduz tabela, migração ou contrato novo de gravação. Reverter para a UI134 correspondente não exige conversão de dados introduzida pela UI135. Permanecem as restrições anteriores: após salvar contatos na UI131, voltar só o código para UI130 é bloqueado; código e dados precisam ser compatíveis.

Admin, usuário temporário, permissões e dados reais não foram alterados. Leia docs/UI135_GUIA.html, docs/UI135-cobertura.json e docs/UI135-pendencias.json para distinguir implementação, validação local e pendências.
