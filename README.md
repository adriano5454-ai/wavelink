# Wavelink — UI131 integrada localmente

Versão 1.34.31. Base GitHub: b8e5a7aad47df0874672b1a6406a742b68374b29 (UI130). Esta entrega não fez commit, publicação ou alteração de infraestrutura. O repositório mantém a estrutura completa de implantação existente.

## Implementado

- Contatos profissionais: e-mail, WhatsApp e Teams opcionais, visibilidade explícita, conferência de acesso ao abrir o atalho, sem envio automático.
- Documentos: certificados e fontes exatas de manutenção no item; documentos privados RH no perfil; pastas dos originais e retorno com contexto.
- Visual: campos móveis de 16px, botões de 44px nos componentes revisados, foco, navegação selecionada, hierarquia e leitura de tabelas e cartões.
- Ajuda: novos guias em português brasileiro e inglês e catálogo alinhado em 80 tópicos.

## Validação e limites

198 testes Python e 59 suítes JavaScript aprovados na versão final; 2353 recursos reconstruídos e conferidos por SHA-256. Detalhes em DELIVERY_CHECKS.json e validation/.
Sem Chrome, publicação, teste de produção, mensagens externas ou alteração dos usuários e dados da Corcovado. As prévias em docs/UI131-previas são HTML de componentes reais com dados fictícios, não screenshots.

## Usar o pacote

Extraia em uma nova pasta. Compare com a versão mais recente do seu repositório antes de aplicar pelo GitHub Desktop; preserve trabalho novo. Não copie bancos ou arquivos de dados dos testes para a empresa. Não crie outro serviço ou disco.
O Dockerfile mantém a cadeia de reconstrução do aplicativo. Para obter o código-fonte completo numa pasta nova, use: python deploy/materialize_runtime.py CAMINHO_NOVO. Nenhum dado de empresa é necessário para isso.

## Backup e reversão

A UI130 local foi mantida intacta; esta rodada não criou nem alterou um backup do banco de produção. Antes de uma publicação futura, faça e confira o backup do banco/disco existente.
Os contatos usam tabelas adicionais. No primeiro salvamento de contatos, um marcador impede que versões antigas leiam a empresa sem aplicar a proteção de privacidade. Depois disso, reverter somente o código para UI130 é bloqueado. Uma reversão completa exige código compatível e restauração coordenada de um backup anterior verificado, com processos de escrita parados; isso perderia alterações posteriores ao backup. Preferir correção para frente para manter dados novos.
Não houve reset, renomeação de serviço, concessão de permissão a usuário real ou limpeza do usuário temporário.
