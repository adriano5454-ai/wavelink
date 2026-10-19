# Wavelink — UI139 integrada localmente

Versão 1.34.39. Base local UI138; base GitHub UI138: d7e8614d946708b80f8bc8217a6a60d0dd117a78. Repositório completo, com cadeia anterior preservada. Esta rodada não publica nem acessa dados reais.

## Alterações

- Remessas, recebimento e custódia: Busca e estados em português, datas legíveis, filtros corretos para itens avariados, preservação de contexto e proteção contra respostas de arquivos após sair da tela.
- RH: despesas, viagens e afastamentos planejados: Busca encontra o projeto da despesa e a situação planejada; formulário distingue afastamento, folga e trabalho; detalhes e reenvio após correção mais claros.
- Controles compartilhados: Nomes com acento e estados em português funcionam nas buscas; opções de logística removidas ou bloqueadas não podem ser escolhidas por controles antigos. Navegação e conferência do seletor de equipamentos em português.

## Validação

75 testes Python distintos, 113 suítes JavaScript e 114 arquivos JavaScript com sintaxe aprovada. Os 2453 recursos reconstruídos pela cadeia completa coincidem por SHA-256 com a versão final. DELIVERY_CHECKS.json e validation/ registram resultados, limitações e identidade da versão.

docs/UI139-previas contém exemplos reais de componentes com dados fictícios, incluindo comparação dos filtros de itens avariados e datas de transporte entre UI138 e UI139. São HTML portáteis, não screenshots. Os testes de transporte e DOM simulados não comprovam layout, SMTP ou produção.

## Usar o pacote

Extraia em uma pasta nova. Compare com o GitHub mais recente antes de aplicar, preservando trabalho posterior. Não crie outro serviço ou disco e não leve bases de teste para produção. O pacote não contém banco real, .env ou credenciais de produção.
Para reconstruir todo o código-fonte em uma pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. A cadeia verifica cada etapa e recusa base incompatível.

## Backup e reversão

A base local UI138 e o ZIP anterior foram preservados e conferidos. Não foi criado backup de produção, que não foi acessada. Antes de publicação futura, conferir a versão instalada e fazer backup verificado do banco/disco existentes.
Esta etapa altera controles e textos da interface, sem introduzir tabela, migração ou contrato novo de gravação. Reverter para a UI138 correspondente não exige conversão de dados introduzida pela UI139, mas reintroduz os problemas de interface corrigidos nesta rodada. Permanecem as restrições anteriores: após salvar contatos na UI131, voltar só o código para UI130 é bloqueado; código e dados precisam ser compatíveis.

Admin, usuário temporário, permissões e dados reais não foram alterados. Leia docs/UI139_GUIA.html, docs/UI139-cobertura.json e docs/UI139-pendencias.json para distinguir implementação, validação local e pendências.
