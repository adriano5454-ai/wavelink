# Wavelink — UI118

Corcovado em português, com a frente privada de Recursos Humanos da UI117 integrada. Core 1.34.19. Interface, 77 tópicos de ajuda, manual PDF, relatórios e mensagens do sistema em português quando o serviço está configurado como COMPANY e COMPANY_ID=corcovado. Demo e outras empresas mantêm o inglês.

O módulo **Recursos Humanos** fica na navegação principal; o perfil oferece acesso aos próprios registros privados. Inclui documentos/certificados pessoais, viagens/escalas, folhas de horas, despesas e revisão independente. Certificados de equipamentos continuam no Inventário. Permissões existentes não são ampliadas automaticamente.

Leia [o escopo e os limites](docs/WORKSPACE_UI118.md), [as verificações](docs/UI118_REVIEW_REPORT.json) e [o ponto de continuação](docs/CONTINUATION_CHECKPOINT.md). Docker reconstrói a fonte fixada e aplica os overlays até UI118. Preserve dados, configurações privadas e ambiente.

A [transição Sulmara → Corcovado](docs/CORCOVADO_TRANSITION.md) permanece uma operação separada, no disco existente. Este pacote não executa migração, DNS ou publicação. Código preparado e testado localmente; publicação ainda pendente.
