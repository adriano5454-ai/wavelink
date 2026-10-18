# Wavelink — UI130 local integrada

Versão **1.34.30**, baseada no commit 45f07468056e1240e7df9d51a9d53ce9c815a657 (UI129). **Integrada e testada localmente; não publicada.** Não há commit ou deployment UI130.

- TI: chamados próprios, fila autorizada, prioridade, responsável, comentários, justificativas, resolução, encerramento, reabertura e histórico.
- Pessoas: paginação, busca sem acentos e preservação de contexto.
- Documentos originais: caminho clicável por pastas/subpastas.
- Perfil: cancelar edição avisa antes de descartar mudanças.
- Permissões e cópias seletivas protegem dados privados de TI. Avisos de backup em português para Corcovado; inglês preservado nas outras instalações.

Passaram 153 testes Python, 53 suítes JavaScript, 110 verificações de sintaxe JavaScript e 228 de sintaxe Python. A reconstrução completa reproduziu os 2330 recursos do manifesto 4a815e6be23196cbaf5097fa449998178f63b6a832e96a073e21c42403797835.

[Relatório e prévias](docs/UI130_GUIA.html) · [Validação](validation/ui130-validation.json) · [Pendências](validation/ui130-pendencias-consolidadas.json)

## Código completo

Mantida a estrutura existente: fonte-base verificada em vendor/ e cadeia de alterações em deploy/. Para materializar todo o código em pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. Isso não abre dados da empresa. O Dockerfile acrescenta UI130 à mesma cadeia; a imagem Linux não foi construída nesta rodada.

## Preservação e reversão

Nenhum serviço, domínio, disco, banco, conta real, senha ou registro foi alterado. Admin e usuário temporário preservados. Nenhuma mensagem a terceiros. Permissões explícitas existentes não recebem novos direitos automaticamente; gestão global de TI não pode ser delegada por departamento.

A base UI129 foi preservada separadamente. Antes de futura publicação: conferir novamente a versão remota, fazer backup verificado dos dados, publicar no serviço existente e validar a versão servida. Depois de criar chamados reais, reversão deve preservar as novas tabelas, históricos e acessos. Não reinicializar ou restaurar backup antigo sobre gravações novas. Nenhuma reversão foi executada.

## Limites

Sem Chrome, produção, capturas novas ou validação visual móvel. Testes DOM/API não substituem essas verificações. Contatos profissionais com visibilidade própria, percurso universal de documentos por item/perfil/pasta e aceite formal de tarefas continuam pendentes. A revisão integral das 193 vistas não está concluída. Relatórios anteriores são históricos e não representam o status da UI130.
