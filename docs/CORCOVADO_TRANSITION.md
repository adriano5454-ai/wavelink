# Transição da empresa Sulmara para Corcovado

Preparação de 16/10/2026, sobre o aplicativo UI116/core 1.34.19,
commit-base `1f1f75401f9c404cb5859de3b1a3742af2e60010`.
Status: preparação local; nenhuma alteração de produção ou DNS foi aplicada.

## Resultado pretendido

| Configuração | Atual | Destino |
| --- | --- | --- |
| Nome exibido | Sulmara | Corcovado |
| Identidade de implantação | sulmara | corcovado |
| Serviço Render | wavelink-sulmara | wavelink-corcovado |
| Endereço público | https://sulmara.mywavelink.com | https://corcovado.mywavelink.com |
| Serviço persistente | srv-das4ujojo6nc73a7u53g | O mesmo serviço |
| Disco persistente | dsk-das52bjbc2fs739c03n0 | O mesmo disco |
| Diretório da empresa | /var/data/wavelink-company | O mesmo diretório |

Não criar outra empresa, disco ou banco de dados para efetuar esta troca.
Preservar `hub_id`, `installation_id`, administrador, credenciais, documentos,
registros operacionais, permissões, backups e histórico. A demonstração pública
é outro serviço e não recebe os valores de ambiente da Corcovado.

O PNG fornecido é uma identificação textual neutra com a palavra CORCOVADO,
sem reutilizar a arte da Sulmara. Não é uma afirmação de logotipo oficial.
As identidades antigas permanecem no repositório durante a transição para que
o primeiro deploy de preparação ainda possa iniciar com a configuração atual.

## Motivo para usar uma migração explícita

`deploy/company_provision.py` recusa inicializar uma empresa existente quando
`COMPANY_ID` ou `COMPANY_NAME` divergem de `COMPANY_DEPLOYMENT.json` no disco.
Mudar somente as variáveis do Render pode impedir a inicialização do serviço.
O utilitário offline prepara/verifica o plano, cria uma cópia privada completa
da empresa com hashes e aplica a troca com proteção contra estado parcial.

Não fazer substituição global de texto em SQLite, relatórios ou documentos.
Registros e revisões anteriores devem manter sua proveniência original.

## Ordem de execução

1. Conferir a versão remota. Esta preparação usa UI116 e não inclui a UI117/RH
   ainda não publicada. Se o remoto avançar, reaplicar estas alterações sobre a
   versão nova; não substituir o repositório inteiro por esta cópia.
2. Publicar somente a preparação de migração/identidade, mantendo inicialmente
   as variáveis Sulmara existentes. Conferir que o serviço atual ainda inicia.
3. Criar `corcovado.mywavelink.com` como domínio personalizado do mesmo serviço.
   No DNS criar CNAME `corcovado` para o destino `onrender.com` que o Render
   realmente informar. O destino observado nesta preparação é
   `wavelink-sulmara.onrender.com`. Não presumir que renomear o serviço altera
   seu hostname; confirmar o hostname após qualquer mudança e ajustar o CNAME.
4. Verificar o domínio e o certificado HTTPS. Não divulgar o endereço como
   disponível antes da verificação. Mudar o nome do serviço para
   `wavelink-corcovado` preservando seu ID e seu disco.
5. Fazer backup completo autorizado da empresa e interromper o aplicativo e
   seus escritores antes de aplicar a migração offline. Modo de manutenção
   HTTP, sozinho, não prova que todos os processos de escrita foram parados.
   Não enviar backups privados ao GitHub ou a pacotes públicos.
6. Executar primeiro a simulação do utilitário `ops.rename_company` no ambiente
   de operação. Aplicar apenas depois de revisar o plano e confirmar o serviço
   parado. O utilitário cria um backup completo local verificado; manter também
   o backup independente habitual. No Render, executar em uma sessão/container
   de manutenção com o mesmo volume, antes de iniciar o aplicativo normal.
   Não executar `--apply` contra um processo normal ainda em execução.
7. Atualizar por merge somente as variáveis de `deploy/corcovado.env.example`.
   Manter credenciais SMTP, demais segredos e configurações particulares
   existentes. Não habilitar inicialização de empresa ou dados fictícios.
8. Reiniciar e verificar as mesmas identidades internas, usuários e contagens
   operacionais. Conferir login, marca da Corcovado, convites, recuperação de
   senha e novos links de alertas no endereço novo. Testar e-mail sem enviar
   mensagens a terceiros sem autorização própria.
9. Em Administração → Company report profile, exportar/revisar o perfil atual
   e salvar uma revisão com Corcovado, identificação textual/logotipo, contato,
   cabeçalho e rodapé corretos. O perfil PDF fica no banco e não é substituído
   pelo logotipo de implantação. Usar a edição administrativa versionada;
   preservar auditoria e relatórios anteriores. Endereços, e-mails e nomes
   jurídicos da Corcovado não fornecidos precisam ser confirmados, não inventados.
10. Após aceitar o endereço novo, retirar o domínio antigo do serviço e do DNS.
    Não simplesmente redirecionar requisições de API autenticadas entre origens.
    Os usuários devem entrar no endereço novo; credenciais continuam iguais,
    mas sessão e trabalho não salvo no navegador antigo não são transferidos
    automaticamente. Salvar o trabalho antes da troca.

## Comandos de operação

Na raiz do código, usando o Python do ambiente Wavelink e o mesmo
usuário/grupo que possui a instalação (no container atual, UID/GID 10001).
O utilitário recusa aplicar/recuperar se o usuário ou grupo não corresponderem
aos proprietários da instalação e dos JSON. Não executar a aplicação como root.

Preparar antes, como operador root, o
diretório privado de backup no volume persistente:

```bash
install -d -m 0700 -o 10001 -g 10001 /var/data/wavelink-company-rename-backups
```

Depois assumir UID/GID 10001 para executar a migração. Conferir o proprietário
do backup sem alterar o proprietário dos dados existentes em massa.
Simulação da transição:

```bash
python -m ops.rename_company \
  --root /var/data/wavelink-company \
  --from-id sulmara --from-name Sulmara \
  --to-id corcovado --to-name Corcovado \
  --public-url https://corcovado.mywavelink.com
```

Esse comando apenas mostra o plano. A execução autorizada acrescenta
`--apply --service-stopped` ao mesmo comando. O argumento é uma confirmação
operacional; não para automaticamente o serviço. O utilitário também exige
que as três leases de escrita estejam livres.

## Recuperação

Se houver journal de migração pendente, o provisionamento recusa iniciar.
Usar a recuperação explícita do utilitário com o serviço parado, revisar as
cópias privadas e restaurar em conjunto as variáveis do ambiente correspondentes.
Não apagar o journal para contornar o bloqueio nem inicializar uma empresa nova.

```bash
python -m ops.rename_company --root /var/data/wavelink-company --recover
```

A recuperação acima também é apenas uma simulação; acrescentar
`--apply --service-stopped` somente para recuperar uma interrupção confirmada.
Ela restaura os dois JSON originais e não substitui o banco operacional.

## Dependências externas restantes

A integração Render disponível consulta serviços e altera variáveis, mas não
renomeia serviços, não cadastra domínios personalizados e não edita DNS.
Essas etapas exigem acesso autorizado ao navegador/painéis correspondentes.
Na consulta pública de 16/10, `sulmara.mywavelink.com` apontava para
`wavelink-sulmara.onrender.com`, e `corcovado.mywavelink.com` não existia.
Configuração final e aceitação em produção continuam pendentes.
