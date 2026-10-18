# UI127 — Auditoria de RH e Operações

Wavelink **1.34.27**, sobre `736c9c9c82e9b0a0f93f41d59d063c1ade13da27`. Corrige viagens e foco no calendário, navegação, listas de verificação, originais, inventário e validação em português. A revisão complementar corrige também contadores de rascunhos e detalhes de conferência de estoque. Preserva registros, permissões, idiomas e usuário temporário.

- [Cobertura por área, testes, capturas e limites](docs/UI127_GUIA.html)
- [193 telas/funções inventariadas](docs/UI127_COVERAGE.json)
- [Validação e falhas ainda abertas](validation/ui127-validation.json)
- [Proveniência](docs/UI127_SOURCE_PROVENANCE.json)

**Auditoria integral parcial:** 130 itens com evidência detalhada (não equivale a aprovação integral); demais fluxos pendentes e produção autenticada bloqueada. Bateria histórica completa não verde. 27 suítes JavaScript e nove testes Python focados passaram; reconstrução de 2.281 recursos verificada. Reconstruir em pasta nova: `python deploy/materialize_runtime.py ./runtime-ui127`. Não importar cenários fictícios em produção. Documentação anterior preservada abaixo.

# UI126 — Importações e conferência de originais em português

Wavelink **1.34.26**, sobre `d6bc5959c4eb8aa44c238dbc0c1cc53fef88c70f`.

Conclui textos de importações avançadas, comparação com o original, biblioteca e erros. Mantém conteúdo dos documentos, evidências, identificadores, permissões, dados e idiomas das demais empresas.

- [Guia, capturas e limites da validação](docs/UI126_GUIA.html)
- [Resultados dos testes](validation/ui126-validation.json)
- [Proveniência do runtime](docs/UI126_SOURCE_PROVENANCE.json)

Reconstrução: `python deploy/materialize_runtime.py ./runtime-ui126` em uma pasta nova. O cenário fictício de teste não deve ser importado em produção. Validação autenticada na Corcovado permanece bloqueada pela ferramenta do navegador; publicação e integridade de código são verificadas separadamente.

As entregas abaixo são históricas.

---

# UI125 — Português e decisões claras

Wavelink **1.34.25**, sobre `19d16b367143ec6e8d81b4bb5a8d98c4df2168e2`.

Amplia vocabulário brasileiro e distingue salvar, enviar, conferir e aprovar. O formulário de conferência documental mostra metadados e anexos privados junto da decisão. Mantém a UI124, os dados, permissões e idiomas das demais empresas.

- [Guia, capturas, glossário, fontes e pendências](docs/UI125_GUIA.html)
- [162 verificações automatizadas e jornadas locais](validation/ui125-validation.json)
- [Proveniência do runtime](docs/UI125_SOURCE_PROVENANCE.json)

A validação autenticada na Corcovado está bloqueada pela ferramenta do navegador. A cobertura de inglês em caminhos avançados ainda não é integral. Publicação e integridade do código são comprovadas separadamente; não substituem testes funcionais ao vivo.

Reconstrução: `python deploy/materialize_runtime.py ./runtime-ui125` em uma pasta nova. Não importar o cenário fictício em produção.

As entregas abaixo são históricas.

---

# UI124 — Aparência unificada de RH e Operações

Wavelink **1.34.24**, sobre a UI123 `85d79a84b1c9c3393a2a1f8bae720af704dbfa76`.
Reorganiza navegação, cabeçalho, cartões, tabelas, perfis e formulário do colaborador; corrige alternância móvel e foco; amplia rótulos em português sem traduzir dados dos usuários.

- [Guia visual e comparações reais antes/depois](docs/UI124_GUIA_VISUAL.html)
- [Validação local e limites](validation/ui124-validation.json)
- [Proveniência dos recursos](docs/UI124_SOURCE_PROVENANCE.json)

73 verificações automatizadas aprovadas; jornadas locais no Chrome com quatro perfis e dados fictícios. Os testes locais não comprovam a interface de produção, que permanece bloqueada pela ferramenta do navegador. Publicação é registrada separadamente.

Reconstrução completa: `python deploy/materialize_runtime.py ./runtime-ui124` (diretório novo).
Não copiar dados de teste para produção. Mesmas permissões, dados, idiomas e marca preservados.
Os documentos abaixo são entregas históricas e mantêm seus estados originais.

---

# UI123 — Navegação, escalas e acompanhamento do trabalho

Wavelink **1.34.23**, preparado sobre o commit UI122 `28e0dcff4e79c5720aaa322d4bf70170f6ce9653`. Melhora a consulta de equipes, o retorno ao calendário e aos registros, o envio de solicitações e o uso no celular. Preserva dados, permissões, anexos, rascunhos, identidade e idiomas configurados.

- [Guia visual, comparações, glossário e fontes oficiais](docs/UI123_GUIA_VISUAL.html)
- [Validação local e limites](validation/ui123-validation.json)
- [Proveniência dos recursos](docs/UI123_SOURCE_PROVENANCE.json)

**153 verificações automatizadas passaram** e as jornadas foram exercitadas no Chrome com dados fictícios. Os resultados locais não comprovam comportamento em produção; consulte o deployment ativo no Render. A UI122 foi confirmada publicada antes desta revisão. Os documentos abaixo registram entregas anteriores e podem conter seus estados históricos.

Reconstrução completa em diretório novo: `python deploy/materialize_runtime.py ./runtime-ui123`.
Teste dos novos filtros: `node runtime-ui123/tests/test_ux_ui123.cjs`.

---

# UI122 — Permissões em português brasileiro

Wavelink **1.34.22**, preparado sobre o commit d103ed68a7cd1849405d5e3f05a8a14c5290d553 (UI121). Corrige 79 rótulos e 18 grupos do editor de permissões, os avisos de escopo e os títulos de conta. Os identificadores, valores de autorização, nomes de pessoas e registros salvos são preservados; outros deployments continuam no idioma configurado.

**Ainda não publicado.** Verificações locais e publicação em produção são etapas distintas.

- [Escopo e validação](docs/UI122_PERMISSOES_PT_BR.md)
- [Proveniência dos arquivos](docs/UI122_SOURCE_PROVENANCE.json)
- [Verificações locais](validation/ui122-permissions.json)

Fonte completa: `python deploy/materialize_runtime.py ./runtime-ui122` (diretório novo).

---

# UI121 — RH e Operações com navegação mais clara

Wavelink **1.34.21**, preparado e testado localmente sobre main c435332618811aa29ac59e856a5ed922513f4e5e. Inclui UI120. Publicação autorizada para o serviço existente da Corcovado. Os relatórios incluídos registram a validação local; a validação do deployment deve ser conferida separadamente.

- [Guia visual, comparações, glossário e fontes](docs/UI121_GUIA_VISUAL.html)
- [Instalação, permissões e reversão](docs/UI121_INSTALACAO.md)
- [Validação](docs/UI121_VALIDACAO.json)
- [Proveniência](docs/UI121_SOURCE_PROVENANCE.json)

Fonte completa: python deploy/materialize_runtime.py ./runtime-ui121 (diretório novo). Documentação abaixo preservada como histórico da versão indicada.

---

# UI120 — Recursos Humanos em português brasileiro

Versão preparada **1.34.20**, baseada em `c435332618811aa29ac59e856a5ed922513f4e5e` (UI119, com UI118). Esta entrega não foi publicada.

- [Instalação, permissões e reversão](docs/UI120_INSTALACAO.md)
- [Glossário e fontes brasileiras](docs/UI120_GLOSSARIO_FONTES.md)
- [Validação executada](docs/UI120_VALIDACAO.json)
- [Proveniência](docs/UI120_SOURCE_PROVENANCE.json)

Fonte completa: `python deploy/materialize_runtime.py ./runtime-ui120` (diretório novo). O pacote inclui todo o repositório, a fonte em vendor e todas as atualizações.

---

## Documentação anterior preservada

# Wavelink — UI118

Corcovado em português, com a frente privada de Recursos Humanos da UI117 integrada. Core 1.34.19. Interface, 77 tópicos de ajuda, manual PDF, relatórios e mensagens do sistema em português quando o serviço está configurado como COMPANY e COMPANY_ID=corcovado. Demo e outras empresas mantêm o inglês.

O módulo **Recursos Humanos** fica na navegação principal; o perfil oferece acesso aos próprios registros privados. Inclui documentos/certificados pessoais, viagens/escalas, folhas de horas, despesas e revisão independente. Certificados de equipamentos continuam no Inventário. Permissões existentes não são ampliadas automaticamente.

Leia [o escopo e os limites](docs/WORKSPACE_UI118.md), [as verificações](docs/UI118_REVIEW_REPORT.json) e [o ponto de continuação](docs/CONTINUATION_CHECKPOINT.md). Docker reconstrói a fonte fixada e aplica os overlays até UI118. Preserve dados, configurações privadas e ambiente.

A [transição Sulmara → Corcovado](docs/CORCOVADO_TRANSITION.md) permanece uma operação separada, no disco existente. Este pacote não executa migração, DNS ou publicação. Código preparado e testado localmente; publicação ainda pendente.
