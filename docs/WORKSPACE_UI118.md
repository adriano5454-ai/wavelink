# UI118 - Corcovado em português e Recursos Humanos

Atualização preparada em 17/10/2026. Produto Wavelink, AJ Offshore Solutions; core 1.34.19.

A main do GitHub observada no início deste trabalho continha UI116, commit
`8b5f0c51d40481fc8d5cdf03fd19d0a7ee7cc056`. O RH da UI117 estava preparado,
mas não tinha sido publicado. Esta entrega integra UI117 e acrescenta a
localização da Corcovado. Consulte o relatório de verificação para distinguir
preparação, publicação e aceitação real.

## Onde encontrar o RH

- Menu Pessoas -> Recursos Humanos.
- Meu perfil -> Meus registros de RH.
- Documentos pessoais: certificados, atestados, passaporte, caderneta marítima,
  vistos e respectivos arquivos, datas e alertas de vencimento.
- Escalas e viagens: embarcação/local, período, turnos, deslocamento e hospedagem.
- Folhas de horas e despesas: rascunho, envio, devolução e aprovação independente;
  despesas podem ter comprovantes. As moedas permanecem separadas.

O administrador configura os direitos em Administração -> Pessoas e acesso ->
Permissões da empresa. Contas com uma política explícita antiga não recebem
permissões novas automaticamente: conceda `hr.view_own` para o acesso pessoal
e apenas os direitos adicionais necessários. Gerenciamento de documentos,
viagens, escalas e revisão de horas/despesas são autorizações distintas. Não
conceda acesso de RH a toda a empresa para tornar um menu visível.

Certificados do inventário continuam separados dos documentos pessoais.
Não há pagamento, folha salarial ou reserva de viagens automática. Escalas de RH
não substituem silenciosamente os ciclos operacionais de passagem de turno.

## Idioma e preservação

O português brasileiro é fixado pela identidade de implantação verificada:
`WAVELINK_DEPLOYMENT_MODE=COMPANY` e `COMPANY_ID=corcovado`. A demo e outras
empresas mantêm o inglês. Cabeçalhos do navegador, parâmetros da URL e campos
preenchidos pelo visitante não escolhem a identidade da empresa ou seu idioma.

A tradução é aplicada a textos de interface escritos no código, antes de inserir
valores dos registros. Nomes, observações, documentos importados, evidências,
conteúdo assinado e relatórios históricos permanecem no idioma original. Chaves
de API, códigos de estado e formatos compatíveis de CSV/JSON/XLSX são preservados.
Datas e números apresentados em português não alteram os valores canônicos.

Inclui autenticação, mensagens comuns e de RH, menus e formulários, rótulos de
relatórios novos, modelos de e-mail e os 77 tópicos da ajuda. A pesquisa da ajuda
usa conteúdo português. Blocos técnicos de código e comandos são preservados.
O envio real de e-mails não foi executado durante o desenvolvimento. O manual PDF completo contém os 77 capítulos, com sumário e marcadores clicáveis.

## Instalação e migração em paralelo

Use somente o repositório do aplicativo `adriano5454-ai/wavelink`. Não copie este
conteúdo para Wavelink-Website. Preserve alterações válidas mais recentes e
trabalho ainda não enviado. O pacote não altera DNS, plano, serviço ou disco.

Docker reconstrói a origem fixada e aplica UI117 e UI118. Nenhum pacote ZIP ou
commit executa por si só a troca dos dados persistidos de Sulmara para Corcovado.
A migração offline continua em `docs/CORCOVADO_TRANSITION.md`; preserve o mesmo
disco, IDs internos e usuários. Não altere COMPANY_ID/NAME antes de compatibilizar
o marcador persistido. Não reinicialize a empresa para instalar uma atualização.
Mantenha `INITIALISE_COMPANY=NO` e os demais valores seguros já definidos para
essa implantação; não substitua segredos ou a configuração da demo por exemplos.

Confirme que a construção termina em `Applied Workspace UI118`, que o deployment
usa o commit correto e que a conta possui os direitos previstos. Valide o endereço
novo somente após a conclusão de DNS, HTTPS e migração pelo responsável por essa
frente. Salve formulários e preserve rascunhos antes de recarregar a aplicação.

## Limites de aceitação

Os testes usam empresas e contas fictícias, APIs nativas e Chromium isolado.
Não houve alteração no banco de produção, envio real de e-mail, execução do
Docker/Render, aceitação em aparelho físico ou confirmação da troca de DNS.
O relatório de testes descreve também as verificações de inglês preservado,
acesso privado, valores de API, revisão independente e reconstrução integral.
