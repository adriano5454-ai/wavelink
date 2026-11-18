# Wavelink 1.34.52

## Cadastro de colaboradores

Em **Pessoas e acesso**, a equipe pode consultar o diretório, enviar convites e acompanhar aprovações pendentes. Cada colaborador escolhe a própria senha. A concessão de acesso respeita os departamentos e permissões de quem envia o convite ou revisa a solicitação.

O administrador pode iniciar um convite pendente com apenas o e-mail e definir o departamento na revisão. Quando a pessoa que convida pode conceder acesso antecipadamente, ela escolhe o departamento e os acessos que o colaborador receberá ao concluir o cadastro.

A interface indica quando o envio de e-mail está indisponível. O convite continua usando a configuração SMTP da empresa e um link com prazo de validade.

## Testes da versão

A montagem parte do commit `bda9c912e8600c600e8f8643b91a6b6c13008330` da 1.34.51. Os testes usam empresas fictícias e caixas de e-mail locais. A entrega de uma mensagem pela conta SMTP real da empresa precisa ser verificada em produção. O registro de testes está em `DELIVERY_CHECKS.json`.
