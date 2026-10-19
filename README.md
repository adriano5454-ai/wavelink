# Wavelink — UI138 integrada localmente

Versão 1.34.38. Base local UI137; base GitHub UI137: 39afca26a8410581c17768ce712126597391563b. Repositório completo, com cadeia anterior preservada. Esta rodada não publica nem acessa dados reais.

## Alterações

- Perfis e equipe: Recuperação de salvamento após perda da resposta, busca de pessoas e identificação de estados de perfil, histórico e alertas.
- Participação documental: Entrada por convite com controle de respostas atrasadas, expiração/revogação e recuperação do recibo de uma operação incerta.
- Manutenção: Intervalos por dia, semana ou mês com os mesmos limites do servidor, explicação das ações sobre a recorrência e proteção ao fechar/reabrir janelas.
- Logística: Pesquisar preserva o destino escolhido, que permanece visível e identificado em texto. Opções bloqueadas e navegação por teclado respeitam o campo original. Cabeçalhos em PT-BR.

## Validação

66 testes Python distintos, 106 suítes JavaScript e 114 arquivos JavaScript com sintaxe aprovada. Os 2441 recursos reconstruídos pela cadeia completa coincidem por SHA-256 com a versão final. DELIVERY_CHECKS.json e validation/ registram resultados, limitações e identidade da versão.

docs/UI138-previas contém exemplos reais de componentes com dados fictícios, incluindo comparação do seletor de destino da logística entre UI137 e UI138. São HTML portáteis, não screenshots. Os testes de transporte, fotos e DOM simulados não comprovam layout, SMTP ou produção.

## Usar o pacote

Extraia em uma pasta nova. Compare com o GitHub mais recente antes de aplicar, preservando trabalho posterior. Não crie outro serviço ou disco e não leve bases de teste para produção. O pacote não contém banco real, .env ou credenciais de produção.
Para reconstruir todo o código-fonte em uma pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. A cadeia verifica cada etapa e recusa base incompatível.

## Backup e reversão

A base local UI137 e o ZIP anterior foram preservados e conferidos. Não foi criado backup de produção, que não foi acessada. Antes de publicação futura, conferir a versão instalada e fazer backup verificado do banco/disco existentes.
Esta etapa altera controles e textos da interface, sem introduzir tabela, migração ou contrato novo de gravação. Reverter para a UI137 correspondente não exige conversão de dados introduzida pela UI138, mas reintroduz os problemas de interface corrigidos nesta rodada. Permanecem as restrições anteriores: após salvar contatos na UI131, voltar só o código para UI130 é bloqueado; código e dados precisam ser compatíveis.

Admin, usuário temporário, permissões e dados reais não foram alterados. Leia docs/UI138_GUIA.html, docs/UI138-cobertura.json e docs/UI138-pendencias.json para distinguir implementação, validação local e pendências.
