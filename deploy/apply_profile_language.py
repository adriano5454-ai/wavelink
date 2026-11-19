"""Apply the verified personal interface language change to the packaged runtime."""
from hashlib import sha256
import json
from pathlib import Path
import re
import sys


PARENT = 'a8676218bfc5cd49ac8d49db3a187e911ae0e761b3a8a2382fd9a79d84e48dc4'
HERE = Path(__file__).resolve().parent
ASSETS = 'app/static/'


def once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected language patch context: ' + old[:90])
    return source.replace(old, new)


def accounts(source):
    source = once(source, '            ensure_user_lifecycle(c)', '''            ensure_user_lifecycle(c)
            if not any(row[1] == 'preferred_language' for row in c.execute('PRAGMA table_info(users)')):
                c.execute("ALTER TABLE users ADD COLUMN preferred_language TEXT CHECK (preferred_language IN ('en','pt-BR'))")''')
    return once(source, "                    credential_version=r['credential_version'])",
                "                    preferred_language=r['preferred_language'], credential_version=r['credential_version'])")


def server(source):
    source = once(source, 'from .localization import company_locale,', 'from . import profile_language\nfrom .localization import company_locale,')
    source = once(source, 'translate_message(exc.message, ui_locale)',
                  "profile_language.error_message(exc.message, getattr(req.state, 'ui_language', ui_locale))")
    source = once(source, """        localized_page = localized_html_path(req.url.path, BASE / 'static', ui_locale) if req.method in ('GET', 'HEAD') else None
        resp = FileResponse(localized_page, media_type='text/html', headers={'Cache-Control': 'no-store'}) if localized_page is not None else await call_next(req)""",
                  """        presentation = profile_language.page_response(req, BASE / 'static', ui_locale)
        resp = presentation if presentation is not None else await call_next(req)""")
    source = once(source, '    from .original_folders_api import attach', '    profile_language.attach(app, store, config, actor)\n    from .original_folders_api import attach')
    source = once(source, '    def workspace_locale():', "    def workspace_locale(wl_lang: str = ''):")
    source = once(source, 'Response(locale_bootstrap(ui_locale),', 'Response(locale_bootstrap(profile_language.ui_language(wl_lang, ui_locale)),')
    source = once(source, '    def user_manual():', "    def user_manual(wl_lang: str = ''):")
    return once(source, "if ui_locale == 'pt-BR' and portuguese_manual", "if profile_language.ui_language(wl_lang, ui_locale) == 'pt-BR' and portuguese_manual")


def client(source):
    source = once(source, 'function publicDemoManagement() {', '''const profileLanguage = AJProfileLanguage.create({
    state:()=>state, demo:()=>WavelinkNativeDemo.active(), session:connectionSession, api, persist,
    editing:()=>Boolean(window.AJRecognition?.hasForm?.() || window.AJWorkspaceShell?.hasForm?.())
});
function publicDemoManagement() {''')
    source = once(source, 'AJRecognition.init({root,', 'AJRecognition.init({language:profileLanguage,root,')
    source = once(source, 'async function authenticated(){', 'async function authenticated(){if(profileLanguage.restore())return;')
    source = once(source, 'function loginView(){', 'function loginView(){\n    if(profileLanguage.signedOut())return;')
    source = once(source, "const session=connectionSession(),headers={};", "const session=connectionSession(),headers={'Accept-Language':window.WavelinkI18n.locale};")
    source = once(source, "&&path!=='/api/recognition/moods')window.AJActionCenter", "&&path!=='/api/recognition/moods'&&path!=='/api/me/language')window.AJActionCenter")
    # Vessel-only members retain the original Fleet access boundary. Their home
    # can show their own language preference without opening the team directory.
    source = once(source, "const parts=location.hash.slice(1).split('/');if(parts[0]==='asset'",
                  """const ownLanguage=document.createElement('section');ownLanguage.className='card wl-profile-language';root.append(ownLanguage);profileLanguage.mount(ownLanguage);const parts=location.hash.slice(1).split('/');if(parts[0]==='asset'""")
    return source


def profile(source):
    source = once(source, '<a href="#profile-professional-contacts">',
                  '''${own?'<a href="#profile-language">'+(window.WavelinkI18n.locale==='pt-BR'?'Idioma':'Language')+'</a>':''}<a href="#profile-professional-contacts">''')
    source = once(source, '<div class="wl-profile-overview" id="wl-profile-overview">',
                  '''${own?'<section class="card wl-profile-language" id="profile-language"></section>':''}
    <div class="wl-profile-overview" id="wl-profile-overview">''')
    return once(source, "   window.AJProfessionalContacts?.mount(", "   if(own)H.language?.mount(content.querySelector('#profile-language'));\n   window.AJProfessionalContacts?.mount(")


def help_links(source):
    return once(source, "a.target='_blank';", """const locale=global.WavelinkI18n?.locale;
 if(locale){const u=new URL(a.getAttribute('href'),document.baseURI);if(u.searchParams.get('wl_lang')!==locale){u.searchParams.set('wl_lang',locale);a.setAttribute('href',u.pathname+u.search+u.hash);}}
 a.target='_blank';""")


CSS = '''
.wl-profile-language{display:grid;gap:.65rem;margin-block:1rem;padding:1.1rem 1.4rem}
.wl-profile-language h2,.wl-profile-language p{margin:0}
.wl-profile-language form{display:flex;align-items:flex-end;flex-wrap:wrap;gap:.65rem}
.wl-language-field{display:grid;gap:.3rem;max-width:100%}
.wl-language-field label{font-weight:600}
.wl-language-field select{width:15rem;max-width:100%;min-height:2.65rem}
.wl-profile-language button{min-height:2.65rem}
'''

ERRORS = {
    'A need must be recorded under the account of the person submitting it.': 'A necessidade deve ser registrada na conta de quem a cadastra.',
    'Choose a recipient and review the optional invitation permissions.': 'Escolha um destinatário e revise as permissões opcionais do convite.',
    'Completed or cancelled records are read-only. Reopen the record before changing attachments.': 'Registros concluídos ou cancelados são somente para leitura. Reabra o registro antes de alterar os anexos.',
    'Enter a valid full name and sign-in details.': 'Informe um nome completo válido e os dados de acesso.',
    'Enter your company email address.': 'Informe seu e-mail corporativo.',
    'Enter 0 to 365 days for the planned cycle.': 'Informe de 0 a 365 dias para o ciclo previsto.',
    'Pre-approving permissions requires current invitation, review and access-management authority.': 'Para pré-aprovar permissões, você precisa ter autorização vigente para convidar, revisar e gerenciar acessos.',
    'Review the documents required for this shift.': 'Revise os documentos exigidos para esta escala.',
    'Only authorized HR staff can change professional details.': 'Somente o RH autorizado pode alterar os dados profissionais.',
    'This company uses an incomplete HR project snapshot. Preserve its database.': 'Esta empresa usa uma cópia incompleta do projeto de RH. Preserve o banco de dados.',
    'This invitation permission selection could not be verified.': 'Não foi possível verificar as permissões selecionadas para este convite.',
    'This timesheet project is inactive.': 'Este projeto está inativo para apontamento de horas.',
    'Link an active need only to offshore or onshore work.': 'Vincule uma necessidade ativa somente a trabalho embarcado ou em terra.',
    'You can remove only attachments you uploaded. Ask the responsible manager to remove another attachment.': 'Você pode remover apenas os anexos que enviou. Peça ao gestor responsável para remover outro anexo.',
}


def error_translations(source):
    terms = {**ERRORS, **{pt:pt for pt in ERRORS.values()}}
    return source + '\nMESSAGES_PT_BR.update(' + json.dumps(terms, ensure_ascii=False, indent=2) + ')\n'


def apply(root):
    receipt = root / 'RELEASE_FILES.json'
    if sha256(receipt.read_bytes()).hexdigest() != PARENT:
        raise ValueError('Unexpected parent for profile language')
    manifest = json.loads(receipt.read_bytes())
    changes = {}

    def read(name):
        data = (root / name).read_bytes()
        if sha256(data).hexdigest() != manifest['files'][name]:
            raise ValueError('Unexpected source: ' + name)
        return data

    def edit(name, transform):
        old = changes[name] if name in changes else read(name)
        crlf = b'\r\n' in old
        source = old.decode('utf-8').replace('\r\n', '\n')
        result = transform(source)
        if result != source:
            changes[name] = (result.replace('\n', '\r\n') if crlf else result).encode()

    for name, transform in [
        ('app/accounts.py', accounts),
        ('app/store.py', lambda s: once(s, "person.update(name=user['name'],", "person.update(preferred_language=user['preferred_language'], name=user['name'],")),
        ('app/server.py', server),
        ('app/localization.py', error_translations),
        ('app/fleet_access.py', lambda s: once(s, "path in ('/api/me', '/api/logout'", "path in ('/api/me', '/api/me/language', '/api/logout'")),
        (ASSETS+'app.js', client),
        (ASSETS+'recognition_workspace.js', profile),
        (ASSETS+'recognition_workspace.css', lambda s: s+CSS),
        (ASSETS+'help_links.js', help_links),
        (ASSETS+'i18n_pt_br.js', lambda s: once(s, "const locale=global.WAVELINK_LOCALE==='pt-BR'", "const locale=(global.WAVELINK_LOCALE||global.document?.documentElement?.lang)==='pt-BR'")),
        (ASSETS+'workspace_continuity.js', lambda s: once(s, "+'?embedded=1'+hash;", "+'?embedded=1&wl_lang='+encodeURIComponent(window.WavelinkI18n.locale)+hash;")),
        (ASSETS+'fleet.js', lambda s: once(s, 'const headers={...(opts.headers||{})},session=saveSession()',
                                            "const headers={'Accept-Language':window.WavelinkI18n.locale,...(opts.headers||{})},session=saveSession()")),
    ]:
        edit(name, transform)

    for src, dest in [('profile_language.js', ASSETS+'profile_language.js'), ('profile_language.py', 'app/profile_language.py')]:
        if dest in manifest['files'] or (root / dest).exists():
            raise ValueError('Language resource already exists: ' + dest)
        changes[dest] = (HERE / src).read_bytes().replace(b'\r\n', b'\n')
    tag = '/static/profile_language.js?v=1.34.61-' + sha256(changes[ASSETS+'profile_language.js']).hexdigest()[:12]
    for name in ('index.html', 'pt-BR/index.html'):
        edit(ASSETS+name, lambda s: once(s, '<script src="/static/workspace-locale.js"></script>',
            '<script src="/static/workspace-locale.js"></script>\n<script src="'+tag+'"></script>'))
    asset_keys = {name[len(ASSETS):]: sha256(data).hexdigest()[:12] for name,data in changes.items()
                  if name.startswith(ASSETS) and name.endswith(('.js','.css'))}
    pattern = re.compile(r'(/static/('+'|'.join(re.escape(name) for name in asset_keys)+r')\?v=[\d.]+-)[a-f0-9]{12}')
    def versions(s):
        return pattern.sub(lambda m: m[1]+asset_keys[m[2]], s)
    for name in manifest['files']:
        if name.startswith(ASSETS) and (name.endswith('.html') or name == ASSETS+'sw.js'):
            edit(name, versions)
    def worker(source):
        source = once(source, "ui162-20261119-native-corcovado-mood';", "ui162-20261119-native-corcovado-mood-language';")
        source = once(source, "if(e.request.mode==='navigate'){", """if(e.request.mode==='navigate' && u.pathname==='/' && !u.searchParams.has('public_demo') && ['en','pt-BR'].includes(u.searchParams.get('wl_lang'))){
 const language=u.searchParams.get('wl_lang'), key='/?wl_lang='+language;
 e.respondWith((async()=>{const cache=await caches.open(CACHE);try{const page=await fetch(e.request);
  if(page.ok&&!page.redirected&&page.headers.get('Content-Language')===language&&page.headers.get('Content-Type')?.startsWith('text/html'))await cache.put(key,page.clone());
  return page;}catch(error){return await cache.match(key)||await cache.match('/')||Response.error();}})());return;
}
if(e.request.mode==='navigate'){""")
        return once(source, 'const ASSETS=[', 'const ASSETS=['+json.dumps(tag)+',')
    edit(ASSETS+'sw.js', worker)
    variant = manifest['variant']+'-profile-language'
    info = json.loads(read('UI_PATCH.json'))
    info.update(patch_id=variant,parent_patch_id=manifest['variant'],parent_manifest_sha256=PARENT,
                scope='Account language on company profiles and an isolated choice for each English-first demo visit.')
    info['boundaries']['data_schema_changed'] = True
    changes['UI_PATCH.json'] = (json.dumps(info, indent=2)+'\n').encode()
    for name,data in changes.items():
        (root / name).write_bytes(data)
        manifest['files'][name] = sha256(data).hexdigest()
    manifest['variant'] = variant
    data = (json.dumps(manifest, indent=2)+'\n').encode()
    receipt.write_bytes(data)
    print(variant, sha256(data).hexdigest())


if __name__ == '__main__':
    apply(Path(sys.argv[1]))
