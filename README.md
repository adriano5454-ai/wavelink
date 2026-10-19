# Wavelink — UI133 integrada localmente

Versão 1.34.33. Base GitHub: c2a38ac189b58f874cf56d70412f94b4b1e12124 (UI132). Toda a base anterior foi preservada. Nenhum commit, deployment, serviço ou dado real foi alterado nesta rodada.

## Alterações

- Checklists no perfil: fotos salvas de evidência, ilustrações do procedimento e arquivos originais em grupos separados. Vínculo pelo identificador salvo do criador; autoria não significa autoria de todas as fotos. Etapas anterior/posterior permanecem identificadas. Fontes preservam a revisão exata e a pasta real.
- Livros de registros: Documentos e fontes reúne páginas extraídas e imagens de referência do livro correto, tanto no projeto quanto na Frota. A liberação permite consultar; não aprova configurações. O Excel completo não é prometido como download.
- Permissões e integridade: leitura apenas, sem nova tabela ou alteração de dados. Downloads conferem o arquivo e o acesso atual. Conta, rota, lista ou janela alteradas invalidam ações antigas.
- Navegação e idioma: fechar e voltar preservam a sessão e o contexto. Textos e ajuda em português brasileiro para Corcovado, com inglês preservado nas demais instalações.

## Validação

51 testes Python distintos e 67 suítes JavaScript aprovados; 2378 recursos reconstruídos da cadeia completa e conferidos por SHA-256. Evidências em DELIVERY_CHECKS.json e validation/. Prévias HTML com dados fictícios em docs/UI133-previas; não são screenshots.
Não houve Chrome, publicação, envio de mensagem, acesso ao banco real ou alteração do admin/usuário temporário.

## Usar o pacote

Extraia em uma pasta nova. Compare com o repositório mais recente antes de aplicar no GitHub Desktop e preserve trabalho posterior. O ZIP mantém o repositório completo de implantação existente. Não crie outro serviço ou disco e não envie bases fictícias para produção.
Para materializar todo o código-fonte em uma pasta nova: python deploy/materialize_runtime.py CAMINHO_NOVO. A cadeia verifica os arquivos antes de aplicar a UI133.

## Backup e reversão

A base local UI132 e seu ZIP anterior foram preservados e conferidos. Nenhum backup de produção foi criado nesta rodada porque o ambiente real não foi acessado. Antes de publicar futuramente, faça backup verificado do banco/disco existente.
A UI133 acrescenta apenas consultas e apresentação, sem migração ou novas escritas de dados. O retorno para a mesma UI132 preservada não exige conversão introduzida por esta etapa; confira a versão efetivamente instalada antes de reverter. Permanecem as proteções anteriores: após salvar contatos da UI131, voltar somente o código para UI130 é bloqueado; código e dados devem continuar compatíveis.
Leia docs/UI133-pendencias.json e docs/UI133_GUIA.html.
