# Wavelink 1.34.61

[Inventário e demonstração pública](docs/WORKSPACE_UI162.md)

A demonstração pública abre a empresa fictícia Maré Alta Surveys com as telas do produto. Na página inicial, experimente o humor do dia ou abra **Áreas de trabalho** para consultar RH, TI, operações, frota e administração. Os registros da empresa são de leitura. A escolha de humor é individual por visita. Use **Português** no rodapé para mudar o idioma.

---

# Wavelink 1.34.60

[Entrada automática na demonstração pública](docs/WORKSPACE_UI161.md)

---

# Wavelink 1.34.59

[Humor do dia no feed da equipe e fotos de perfil no celular](docs/WORKSPACE_UI160.md)

---

# Wavelink 1.34.58

[Escalas por departamento e localização da interface em português](docs/WORKSPACE_UI159.md)

---

# Wavelink 1.34.57

[Ajuda da OpenAI na importação e nos formulários de RH](docs/WORKSPACE_UI158.md)

---

# Wavelink 1.34.56

[Perfil Gestão de RH para convites e acesso](docs/WORKSPACE_UI157.md)

---

# Wavelink 1.34.55

[Convites personalizados, calendário por departamento, atendimento de TI e tipos de tarefa](docs/WORKSPACE_UI156.md)

---

# Wavelink 1.34.54

[Documentos no perfil, pendências e acesso à empresa](docs/WORKSPACE_UI155.md)

---

# Wavelink UI154 candidate

Wavelink 1.34.53. See [Wavelink 1.34.53 release notes](docs/WORKSPACE_UI154.md).

---

# Wavelink UI153 candidate

Wavelink 1.34.52. See [Wavelink 1.34.52 release notes](docs/WORKSPACE_UI153.md).

---

# Wavelink UI152 candidate

Wavelink 1.34.52. See [Wavelink 1.34.52 release notes](docs/WORKSPACE_UI152.md).

---

# Wavelink UI151 candidate

Wavelink 1.34.51. See [Camera capture, Excel exports and workflow help](docs/WORKSPACE_UI151.md).

---

# Wavelink UI150 candidate

Wavelink 1.34.50. See [Edit AI suggestions before applying them](docs/WORKSPACE_UI150.md).

---

# Wavelink UI149 candidate

Wavelink 1.34.49. See [Task and inventory creation with OpenAI and Portuguese interface labels](docs/WORKSPACE_UI149.md).

---

# Wavelink UI148 candidate

Wavelink 1.34.48. See [Responsive builder card actions](docs/WORKSPACE_UI148.md).

---

# Wavelink UI147 candidate

Wavelink 1.34.47. See [QSHE evidence, work orders and builder assistance](docs/WORKSPACE_UI147.md).

---

# Wavelink UI146 candidate

Wavelink 1.34.46. See [form scrolling and verification](docs/WORKSPACE_UI146.md).

---

# Wavelink UI145 candidate

Wavelink 1.34.45. See [editor drafts and verification](docs/WORKSPACE_UI145.md).

---

# Wavelink UI144 candidate

Wavelink 1.34.44. See [document assistance and validation](docs/WORKSPACE_UI144.md).

---

# Wavelink UI143 candidate

Version 1.34.43, prepared on 17 November 2026 from the verified UI142 checkpoint, based on published commit `18c14c5429379932ac8f7880f70e72f17e18d137`.

## Changes

- Adds private attachments to travel, shifts, timesheets and IT requests with current record permissions.
- Makes attachments visible while creating personal documents, expenses and IT requests, with retained per-file retries after partial failures.
- Adds clear employee certificate, medical and course entry points and named course presets using the existing document model.
- Shows authorized attachments in the employee document view; files remain in their private HR/IT storage.
- Aligns page action buttons and Help consistently.
- Adds optional OpenAI assistance for inventory column mapping when the server is configured.
- Sends selected column headers and at most eight sample rows only after explicit confirmation. Original files and complete workbooks are excluded from the API request.
- Keeps suggestions separate from application and saving. Users review mappings and explicitly apply them; assistance never saves inventory automatically. Standard local import remains available.
- Rechecks the current named account, selected project, inventory-builder permission and source identity. Connection tests additionally require an administrator.
- Bounds input and response sizes, validates structured suggestions, and limits use to 100 requests per project per UTC day, 20 per user per UTC day, six per user per minute and two concurrent requests per project.
- Persists operation identifiers so repeating the same request cannot cause another provider call or another quota charge. Cached results may be returned; an expired or interrupted operation requires a new explicit request.
- Uses a server-side API key. The administrator connection test sends fixed synthetic text with a 32-token output limit and shares the usage limits.
- Refreshes changed asset URLs and the offline cache identifier for UI143.

Adds UI143 after UI142 in the existing Docker and source reconstruction chains. The two application services and the marketing website retain their existing resources. Website 3.3.1 accompanies the optional-assistance privacy update.

See [UI143_REVIEW.md](docs/UI143_REVIEW.md) for verification and release status.

---

# Wavelink UI142 candidate

Version 1.34.42, prepared on 17 November 2026 from verified UI141 commit `18c14c5429379932ac8f7880f70e72f17e18d137`.

## Changes

- Adds optional OpenAI assistance for inventory column mapping when the server is configured.
- Sends selected column headers and at most eight sample rows only after explicit confirmation. Original files and complete workbooks are excluded from the API request.
- Keeps suggestions separate from application and saving. Users review mappings and explicitly apply them; assistance never saves inventory automatically. Standard local import remains available.
- Rechecks the current named account, selected project, inventory-builder permission and source identity. Connection tests additionally require an administrator.
- Bounds input and response sizes, validates structured suggestions, and limits use to 100 requests per project per UTC day, 20 per user per UTC day, six per user per minute and two concurrent requests per project.
- Persists operation identifiers so repeating the same request cannot cause another provider call or another quota charge. Cached results may be returned; an expired or interrupted operation requires a new explicit request.
- Uses a server-side API key. The administrator connection test sends fixed synthetic text with a 32-token output limit and shares the usage limits.
- Refreshes changed asset URLs and the offline cache identifier for UI142.

Adds UI142 after UI141 in the existing Docker and source reconstruction chains. The three existing Render application services retain their resources. Website 3.3.1 accompanies the optional-assistance privacy update.

See [UI142_REVIEW.md](docs/UI142_REVIEW.md) for verification and release status.

---

# Wavelink UI141 candidate

Version 1.34.41, prepared on 17 November 2026 from the verified UI140 release.

## Changes

- Incorporates the reviewed UI141 visual changes and local typography.
- Registers local font files in the offline shell.
- Refreshes changed static-asset URLs and the offline cache identifier.
- Updates application version labels, including installation and example pages.
- Adds UI141 after UI140 in the existing Docker and source reconstruction chains.

See [UI141_REVIEW.md](docs/UI141_REVIEW.md) for verification and release status.

---

# Wavelink UI140 candidate

Version 1.34.40, prepared on 17 November 2026 from GitHub main f6d69ded35576b558d1ca4ebd0cb568681afe750.

## Changes

- Home provides distinct empty-state messages for personal work, actions and saved handovers in English and Brazilian Portuguese.
- Clear filters resets the active filters and pagination while retaining the selected Home view.
- Home view tabs use two columns on narrow screens so Portuguese labels remain readable.
- Builder package review, import and inventory creation execute synchronous work through the existing worker thread pool.
- Updated asset URLs and offline shell version identify the changed client files.


See [UI140_REVIEW.md](docs/UI140_REVIEW.md) for validation and pending checks.

---

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
