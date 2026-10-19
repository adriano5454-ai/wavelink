# Wavelink — UI137 integrada localmente

Versão 1.34.37. Base GitHub UI136: 421f8d3252a73ed0fbd8c8bc088158d9973bee7e. Repositório completo, com cadeia anterior preservada. Esta rodada não publica nem acessa dados reais.

## Alterações

- RH: calendário, agenda, relatórios e cadastro: Respostas antigas não substituem consultas atuais. A exportação fica indisponível durante o carregamento e usa os filtros dos dados efetivamente carregados. Calendário e agenda distinguem pessoas com nomes iguais; a busca também aceita o identificador de acesso autorizado.
- Documentos: conferência, convites e participação: Convites oferecem nova tentativa após falha de carregamento e aviso antes de fechar um envio sem confirmação. Resultados tardios respeitam a conta e a janela atuais. Participação identifica a revisão, diferencia ciência de assinatura e melhora as descrições acessíveis e mensagens em português.
- Manutenção: execução e aprovadores: A publicação e o catálogo de revisores agora usam a permissão de aprovação da manutenção, corrigindo a exigência indevida de aprovação de checklists. O formulário mostra o motivo salvo da devolução, identifica o revisor e apresenta limites numéricos em português. Nenhuma política de acesso ou conta foi alterada.
- Solicitações de TI: Busca de responsáveis por nome sem acentos ou identificador mantém a seleção e o rascunho. Voltar para a lista devolve o foco ao chamado. Falhas de acesso ao histórico retiram detalhes anteriores e permitem recarregar a consulta. Ajuda e apresentação foram alinhadas ao comportamento.

## Validação

55 testes Python distintos, 99 suítes JavaScript e 114 arquivos JavaScript com sintaxe aprovada. Os 2430 recursos reconstruídos pela cadeia completa coincidem por SHA-256 com a versão final. DELIVERY_CHECKS.json e validation/ registram resultados, limitações e identidade da versão.

docs/UI137-previas contém exemplos reais de componentes com dados fictícios, incluindo comparação de seleção de responsáveis em TI entre UI136 e UI137. São HTML portáteis, não screenshots. Os testes de transporte, fotos e DOM simulados não comprovam layout, SMTP ou produção.

## Usar o pacote

Extraia em uma pasta nova. Compare com o GitHub mais recente antes de aplicar, preservando trabalho posterior. Não crie outro serviço ou disco e não leve bases de teste para produção. O pacote não contém banco real, .env ou credenciais de produção.
Para reconstruir todo o código-fonte em uma pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. A cadeia verifica cada etapa e recusa base incompatível.

## Backup e reversão

A base local UI136 e o ZIP anterior foram preservados e conferidos. Não foi criado backup de produção, que não foi acessada. Antes de publicação futura, conferir a versão instalada e fazer backup verificado do banco/disco existentes.
Esta etapa corrige a validação dos aprovadores de manutenção, sem introduzir tabela, migração ou contrato novo de gravação. Reverter para a UI136 correspondente não exige conversão de dados introduzida pela UI137, mas reintroduz a validação incorreta dos revisores de manutenção. Permanecem as restrições anteriores: após salvar contatos na UI131, voltar só o código para UI130 é bloqueado; código e dados precisam ser compatíveis.

Admin, usuário temporário, permissões e dados reais não foram alterados. Leia docs/UI137_GUIA.html, docs/UI137-cobertura.json e docs/UI137-pendencias.json para distinguir implementação, validação local e pendências.
