# Verificação UI118

Use WAVELINK_UI117_TEST_SOURCE para o runtime UI117 íntegro e WAVELINK_TEST_SOURCE para o runtime final UI118. PYTHONPATH deve conter o runtime alvo e depois o repositório. Dependências de desenvolvimento: requirements.lock, pytest, httpx, playwright, beautifulsoup4 e PyMuPDF.

Testes novos: test_corcovado_locale.py, test_help_locale_ui118.py, test_ui118_build.py, test_locale_ui118.cjs e test_hr_locale_ui118.cjs. O runtime inclui test_corcovado_report_locale_ui118.py e os testes nativos RH UI117. Consulte DELIVERY_CHECKS.json e docs/UI118_REVIEW_REPORT.json para resultados finais.

browser_corcovado_pt_hr_ui118.py exercita APIs nativas e Chromium em português e inglês, documentos privados, horas/despesas, aprovação independente, direitos, preservação de dados e telas estreitas. Dados inteiramente fictícios e SQLite descartável. WebSockets e service workers são suprimidos nesse ensaio; não é aceitação do ambiente publicado.

As suítes JavaScript anteriores são preservadas. Dezoito suítes em inglês foram verificadas; em português, 17 passaram e uma asserção antiga do Toolbox depende literalmente de “Loading”, já traduzido. Essa asserção não foi reescrita para ocultar a diferença. A verificação do pacote reproduz cada recurso e recusa pai alterado ou reaplicação.

Sem alegação de publicação, e-mail real, folha de pagamento, pagamentos, reservas, dispositivos físicos, Windows ou atualização de service worker.
