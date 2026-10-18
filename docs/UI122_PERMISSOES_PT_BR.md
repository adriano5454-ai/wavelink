# UI122 — Permissões em português brasileiro

Corrige o editor de permissões da Corcovado: os rótulos vindos do servidor agora passam explicitamente pela tradução de interface, sem traduzir nomes de pessoas, dados digitados, identificadores ou valores de acesso. Os 79 rótulos e 18 grupos têm apresentação em português, com avisos de escopo e confirmação de backup.

A análise de despesas apresentadas continua separada de pagamento de reembolso. As regras de autoria, concessão e confirmação não foram alteradas. Outros idiomas permanecem preservados pela seleção de idioma existente.

Base: d103ed68a7cd1849405d5e3f05a8a14c5290d553.

Validação local: 12 testes do editor (incluindo gravação simulada com valores idênticos, isolamento de idioma e confirmação do backup) e 30 regressões de localização/UI121. A falha original foi reproduzida no mesmo teste antes da correção.

Não publicado ainda. A verificação no Chrome e os testes de devolução/rejeição em produção dependem da liberação de acesso ao domínio nas permissões de sites do aplicativo.

Reconstrução completa aprovada: 2.269 recursos, manifesto SHA-256 `974b21cf4267564f46bc504908daed03365fdbd221c1747321f3a4688820a3ae`. Este resultado confirma o pacote local; não comprova publicação nem comportamento no serviço ativo.
