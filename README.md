# Wavelink — UI134 integrada localmente

Versão 1.34.34. Base GitHub UI133: d44a6167a4155d22ee664203cb3232d12b1c8582. O repositório completo mantém a cadeia existente de implantação e todas as versões anteriores. Esta rodada não publica nem acessa dados reais.

## Alterações

- RH e perfis: Calendário usa o dia local; viagem sem retorno informa a ausência. Apontamento semanal mantém foco após limpar linha, indica seleção por texto e distingue consulta de edição. Perfil usa Documentos relacionados.
- Documentos e checklists: Fontes dos livros têm busca em toda a extração, páginas de até 100 células e falha de imagem junto ao conteúdo. Biblioteca preserva pasta e foco. Resumo e pendências do checklist encaminham o foco ao destino.
- Solicitações de TI: Próximo passo explícito, triagem separada do acompanhamento e cancelamento em seção própria. Filtros aplicados e intervalo da lista visíveis; prioridades explicadas e homônimos identificados pelo ID já disponível.
- Navegação e apresentação: Busca com rótulo visível, ícones próprios de RH/TI e seleção identificada além da cor. Conta sem acesso tem mensagem específica. Menu móvel e atalho de conteúdo mantêm foco na área ativa, inclusive na Frota.

## Validação

49 testes Python distintos, 73 suítes JavaScript e 113 verificações de sintaxe JavaScript aprovados. Todos os 2388 recursos reconstruídos da cadeia completa coincidem por SHA-256. A jornada local cobre qualquer responsável designado, devolução justificada, correção e reenvio, sem autoaprovação nem leitura de registros de outra pessoa.

DELIVERY_CHECKS.json e validation/ contêm evidências. docs/UI134-previas contém seis exemplos de componentes reais com dados fictícios, incluindo comparações antes/depois de TI e navegação. São HTML, não screenshots. Não houve Chrome, produção, alteração de usuários ou mensagem externa.

## Usar o pacote

Extraia em uma pasta nova. Compare com o repositório mais recente antes de aplicar no GitHub Desktop, preservando trabalho posterior. Não crie outro serviço ou disco, nem leve bases de teste para produção. O ZIP não contém banco real, arquivo .env ou credenciais de produção.
Para materializar todo o código-fonte em uma pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. O processo verifica cada etapa e recusa uma base incompatível.

## Backup e reversão

A base local UI133 e seu ZIP anterior foram preservados e conferidos. Não foi criado backup de produção, pois ela não foi acessada. Antes de uma futura publicação, faça backup verificado do banco/disco existentes e confira a versão instalada.
Esta etapa altera apresentação e handlers, sem nova tabela, migração ou contrato de gravação. Reverter para a UI133 correspondente não exige conversão de dados introduzida pela UI134. Permanecem as restrições anteriores: após salvar contatos da UI131, voltar somente o código para UI130 é bloqueado; código e dados precisam permanecer compatíveis.

Leia docs/UI134_GUIA.html, docs/UI134-cobertura.json e docs/UI134-pendencias.json. As vistas apenas inspecionadas ou não retestadas não contam como fluxos validados.
