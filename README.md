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
