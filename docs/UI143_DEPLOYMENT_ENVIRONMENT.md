# UI143 application environment

The DEMO and COMPANY supervisors forward `OPENAI_API_KEY` and `OPENAI_IMPORT_MODEL`, when present, only to the application process. The Nginx validation process, Nginx server and DEMO gate keep their existing minimal environments and receive neither setting. Other operator variables are not added to the application allowlist.

COMPANY identity and membership settings retain their existing validation and forwarding rules. An absent API key leaves optional assistance unconfigured. Forwarding a setting does not establish provider access, available credit or successful billing; complete the explicit application connection check described in [UI143_OPENAI_SETUP.md](UI143_OPENAI_SETUP.md).

`tests/test_application_ai_environment_ui143.py` checks both supervisors with fictional configured and absent settings, including isolation from proxy and gate processes. No production credentials or provider requests are used by these tests.
