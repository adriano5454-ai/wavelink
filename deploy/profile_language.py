"""Personal interface language and the two reviewed Wavelink presentations."""
from typing import Literal

from fastapi import Depends, Request
from pydantic import BaseModel, ConfigDict
from starlette.responses import FileResponse, HTMLResponse

from .localization import MESSAGES_PT_BR, PT_BR, localized_html_path, translate_message
from .store import Problem


def ui_language(value, default):
    return value if value in ('en', PT_BR) else default


# Some older services emit their reviewed Portuguese sentence before building
# the HTTP error. Only translate an exact authored message, never record values.
ENGLISH_ERRORS = {translation: source for source, translation in MESSAGES_PT_BR.items() if source != translation}


def error_message(message, language):
    if language == 'en':
        return ENGLISH_ERRORS.get(message, message)
    return translate_message(message, language)


def page_response(request, static_root, default):
    if request.method not in ('GET', 'HEAD'):
        return None
    choice = ui_language(request.query_params.get('wl_lang'), None)
    portuguese = localized_html_path(request.url.path, static_root, PT_BR if choice else default)
    if portuguese is None:
        return None
    headers = {'Cache-Control': 'no-store', 'Content-Language': choice or default}
    if not choice:
        return FileResponse(portuguese, media_type='text/html', headers=headers)
    # The existing reviewed mapping supplies the path for both packaged siblings.
    page = portuguese if choice == PT_BR else static_root / portuguese.relative_to(static_root / PT_BR)
    if not page.is_file() or page.is_symlink() or not page.resolve().is_relative_to(static_root.resolve()):
        return None
    html = page.read_text(encoding='utf-8').replace('/static/workspace-locale.js"',
                                                    f'/static/workspace-locale.js?wl_lang={choice}"')
    return HTMLResponse(html, headers=headers)


class LanguageChoice(BaseModel):
    model_config = ConfigDict(extra='forbid')
    language: Literal['en', 'pt-BR']


def attach(app, store, config, actor):
    @app.post('/api/me/language')
    def save_language(choice: LanguageChoice, request: Request, person=Depends(actor)):
        if request.headers.getlist('x-aj-hub-id') != [config['hub_id']]:
            raise Problem(409, 'Confirm the selected project before continuing.')
        if not person.get('user_id'):
            raise Problem(403, 'A named account is required.')
        with store.connection(True) as db:
            current = app.state.accounts.session_person_in_connection(
                db, person['user_id'], person['credential_version'])
            db.execute('UPDATE users SET preferred_language=? WHERE id=?', (choice.language, current['user_id']))
        return {'preferred_language': choice.language}
