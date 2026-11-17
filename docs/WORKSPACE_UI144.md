# Wavelink 1.34.44 — revisão com OpenAI

O Wavelink pode sugerir campos para conferência antes de salvar um registro ou modelo. O usuário escolhe o formulário, confere o trecho que será enviado e solicita as sugestões.

| Onde usar | O que pode ser sugerido |
| --- | --- |
| Importação de checklists e rotinas de manutenção | Título, código, sistema e etapas identificadas no documento |
| Importação de diálogos de segurança e modelos de livros de registros | Perguntas e instruções do formulário ou campos em branco do modelo |
| Criação de modelos e de inventários | Primeira proposta editável a partir da descrição fornecida pelo autor |
| Passagem de turno | Resumo, trabalho concluído, condição dos equipamentos, pendências e prioridades que constam nas anotações |
| Viagens, documentos pessoais e despesas | Campos disponíveis no cadastro, com base no trecho conferido da passagem, certificado ou comprovante |
| Importação de inventário | Associação das colunas usando a amostra de cabeçalhos e linhas da planilha, disponível desde a versão 1.34.43 |

O preenchimento dos formulários mantém as permissões da área correspondente. Para conferir as sugestões, compare cada valor com o documento, especialmente datas, unidades, identificadores e textos de segurança. A aplicação das sugestões e o salvamento do registro são ações separadas. Campos individuais de um formulário dependem de sua configuração e do conteúdo legível da fonte.

O serviço usa a chave da OpenAI configurada no servidor, com controle de acesso e limites de uso. O texto confirmado para a solicitação é enviado à OpenAI. O teste de conexão do administrador continua acessível na importação de inventário. A confirmação de conexão e o saldo da conta são informações distintas.

Este pacote é uma versão candidata baseada no commit `cd6903b7fe1985fa93f84a6dc3c2c3de6f3a5276`. As verificações de reconstrução e os resultados dos testes fornecidos acompanham o pacote em `DELIVERY_CHECKS.json`.
