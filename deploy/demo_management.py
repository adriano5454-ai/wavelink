"""Read-only management tour. Its only data source is the bundled fictional catalogue."""
from html import escape
from hashlib import sha256
from pathlib import Path
import unicodedata
from urllib.parse import urlencode
from uuid import UUID

from .demo_management_data import ADMIN_SECTIONS, AREAS, BY_AREA, BY_RECORD, GROUPS
from .demo_management_files import SAMPLE_FILES


BASE = '/__demo/management'
CSS = Path(__file__).with_name('demo_management.css').read_text(encoding='utf-8')
STYLE_PATH = BASE + '/workspace.css'
STYLE_VERSION = sha256(CSS.encode('utf-8')).hexdigest()[:12]
STYLESHEET = f'<link rel="stylesheet" href="{STYLE_PATH}?v={STYLE_VERSION}">'
HR_AREAS = ('personnel', 'schedule', 'travel', 'time', 'expenses', 'alerts')
# Each link enters the existing workspace using the visitor's normal permissions.
NATIVE = {
    'inventory': ('#inventory', 'Open inventory', 'Abrir inventário'),
    'tasks': ('#tasks', 'Open tasks', 'Abrir tarefas'),
    'handovers': ('#handovers', 'Open handovers', 'Abrir passagens de turno'),
    'hr': ('#hr', 'Open HR', 'Abrir RH'),
    'it': ('#it', 'Open IT requests', 'Abrir solicitações de TI'),
    'logs': ('#logs', 'Open logs', 'Abrir livros de registro'),
    'calendar': ('#calendar', 'Open calendar', 'Abrir calendário'),
    'checklists': ('#checklists', 'Open checklists', 'Abrir checklists'),
    'certificates': ('#certificates', 'Open equipment certificates', 'Abrir certificados de equipamentos'),
    'fleet': ('#fleet', 'Open fleet', 'Abrir frota'),
    'shipments': ('#fleet/manifests', 'Open manifests', 'Abrir manifestos'),
    'receiving': ('#fleet/receiving', 'Open receiving', 'Abrir recebimento'),
    'maintenance': ('#maintenance', 'Open maintenance', 'Abrir manutenção'),
    'faults': ('#faults', 'Open fault reports', 'Abrir relatórios de falhas'),
    'qshe': ('#qshe', 'Open safety and quality', 'Abrir segurança e qualidade'),
    'toolbox': ('#toolbox', 'Open toolbox talks', 'Abrir diálogos de segurança'),
    'originals': ('#original-files', 'Open original files', 'Abrir arquivos originais'),
    'builders': ('#builders', 'Open builders', 'Abrir editores'),
    'members': ('#admin/users', 'Open people and access', 'Abrir pessoas e acesso'),
    'team': ('#team', 'Open team feed', 'Abrir feed da equipe'),
}
ALSO_NATIVE = {'safety': ('toolbox',), 'maintenance': ('faults',), 'logs': ('calendar',),
               'shipments': ('receiving',)}


def select_language(choice, accept_language):
    if choice in ('en', 'pt'):
        return choice
    preferences = []
    for item in accept_language[:300].lower().split(','):
        tag, _, quality = item.strip().partition(';')
        lang = tag.split('-')[0]
        if lang in ('en', 'pt'):
            try:
                weight = 1 if not quality else float(quality.strip().removeprefix('q='))
            except ValueError:
                continue
            if 0 < weight <= 1:
                preferences.append((weight, lang))
    return max(preferences, key=lambda pair: pair[0])[1] if preferences else 'en'


def guest_workspace(value):
    try:
        uid = UUID(value)
    except (ValueError, AttributeError, TypeError):
        return ''
    return value if uid.version == 4 and str(uid) == value else ''


def norm(value):
    return ''.join(char for char in unicodedata.normalize('NFKD', value.casefold())
                   if not unicodedata.combining(char))


def management_page(query, accept_language='', active_guest=False, embedded=False):
    language = select_language(query.get('lang'), accept_language)
    pt = language == 'pt'
    language_index = int(pt)
    namespace = guest_workspace(query.get('workspace')) if active_guest else ''
    visible = set(query.get('open', '')[:350].split(',')).intersection(NATIVE) if namespace else set()
    context = {'lang': language}
    if namespace:
        context.update(workspace=namespace, open=','.join(sorted(visible)))
    area_key = query.get('area', '')
    record_key = query.get('record', '')
    admin_index = area_key == 'admin' and not record_key
    hr_index = area_key == 'hr' and not record_key
    from_admin = query.get('from') == 'admin'
    if from_admin and area_key and not admin_index:
        context['from'] = 'admin'
    area = BY_AREA.get(area_key)
    record = BY_RECORD.get((area_key, record_key))
    term = query.get('q', '')[:80].strip()

    def tr(en, br):
        return br if pt else en

    def tx(value):
        return escape(value[language_index])

    def url(section='', selection='', **extra):
        if embedded:
            if not section:
                return '#workspaces'
            path = '#demo/' + section + ('/' + selection if selection else '')
            options = {key: value for key, value in extra.items() if key in ('q', 'from') and value}
            if from_admin and section != 'admin':
                options.setdefault('from', 'admin')
            return path + ('?' + urlencode(options) if options else '')
        values = dict(context)
        if not section or section == 'admin':
            values.pop('from', None)
        if section:
            values['area'] = section
        if selection:
            values['record'] = selection
        values.update({key: value for key, value in extra.items() if value})
        return BASE + '?' + urlencode(values)

    def native_url(fragment='#home'):
        if embedded:
            return fragment
        if not namespace:
            return '/__demo/public'
        return '/?' + urlencode({'browser_workspace': namespace, 'public_demo': '1'}) + fragment

    def anchor(destination, label, css=''):
        attr = f' class="{css}"' if css else ''
        return f'<a{attr} href="{escape(destination, quote=True)}">{label}</a>'

    def breadcrumb(*items):
        divider = ' <span class="path-separator" aria-hidden="true">/</span> '
        label = tr('Breadcrumb', 'Caminho de navegação')
        return f'<nav class="path" aria-label="{label}">' + divider.join(items) + '</nav>'

    title = tr('Management preview', 'Visão de gestão')
    directory = tr('Workspaces', 'Áreas de trabalho') if embedded else title
    hr_title = tr('Human resources (HR)', 'Recursos humanos (RH)')
    admin_title = tr('Administration', 'Administração')
    readonly = tr('Read-only · Fictional company', 'Somente leitura · Empresa fictícia')
    back = tr('Guest workspace', 'Área do visitante')
    switch = anchor(url(area_key, record_key, q=term, lang='en' if pt else 'pt'),
                    'English' if pt else 'Português')
    header = ('<header><div class="bar">' + anchor(url(), 'Wavelink', 'brand')
              + '<nav aria-label="' + tr('Demo navigation', 'Navegação da demonstração') + '">'
              + anchor(url('admin'), admin_title) + switch + anchor(native_url(), back) + '</nav></div></header>')

    def hero(name, description='', buttons=''):
        return ('<section class="hero"><div class="context">' + readonly + '</div><h1>' + name + '</h1>'
                + (f'<p>{description}</p>' if description else '')
                + (f'<div class="actions">{buttons}</div>' if buttons else '') + '</section>')

    def entry(destination, label, note=''):
        content = '<span class="entry-title">' + label + '</span>'
        if note:
            content += ' <small>' + note + '</small>'
        return '<li>' + anchor(destination, content) + '</li>'

    status = 200
    if hr_index:
        body = breadcrumb(anchor(url(), directory), '<span aria-current="page">' + hr_title + '</span>')
        body += hero(hr_title, tr('Explore the offshore crew’s documents, rotations, travel and claims.',
                                  'Consulte documentos, escalas, viagens e despesas da equipe offshore.'))
        body += '<section class="hr-directory" aria-labelledby="hr-sections"><h2 id="hr-sections">' + tr('HR sections', 'Áreas de RH') + '</h2><ul class="links section-grid">'
        for key in HR_AREAS:
            item = BY_AREA[key]
            body += entry(url(key), tx(item.title), tx(item.description))
        body += '</ul></section>'
    elif admin_index:
        body = breadcrumb(anchor(url(), directory), '<span aria-current="page">' + admin_title + '</span>')
        body += hero(admin_title, tr('Explore the administration sections used by Maré Alta Surveys. Open a section to inspect its records and settings.',
                                     'Explore as seções de administração da Maré Alta Surveys. Abra uma seção para consultar os registros e as configurações.'))
        body += '<div class="details"><section class="card"><h2>' + tr('Admin sections', 'Seções administrativas') + '</h2><ul class="links">'
        for _, label, section, item in ADMIN_SECTIONS:
            body += entry(url(section, item, **{'from': 'admin'}), tx(label))
        body += '</ul></section><section class="card"><h2>' + tr('Manager follow-up', 'Acompanhamento da gestão') + '</h2><ul class="links">'
        for section, item in (('access', 'request'), ('expenses', 'taxi'), ('it', 'ticket-018')):
            example = BY_RECORD[(section, item)]
            body += entry(url(section, item, **{'from': 'admin'}), tx(example.title), tx(example.status))
        body += '</ul></section></div>'
    elif (area_key and not area) or (record_key and not record):
        status = 404
        body = hero(tr('Example not found', 'Exemplo não encontrado'),
                    buttons=anchor(url(), tr('All areas', 'Todas as áreas'), 'button'))
    elif not area:
        journeys = (
            (('Follow an employee', 'Acompanhar uma colaboradora'), 'personnel', 'lia'),
            (('Trace an inventory item', 'Localizar um item de inventário'), 'inventory', 'base'),
            (('Review an IT ticket', 'Consultar um chamado de TI'), 'it', 'ticket-018'),
        )
        body = hero(title, tr('Explore Maré Alta Surveys through the records a manager reviews. Open a person, project or item to follow its related work.',
                              'Conheça a Maré Alta Surveys pelos registros que a gestão acompanha. Abra uma pessoa, um projeto ou um item para ver o trabalho relacionado.'),
                    anchor(url('admin'), tr('Explore administration', 'Explorar a administração'), 'button'))
        body += '<div class="journeys">'
        for label, section, item in journeys:
            source = BY_RECORD[(section, item)]
            body += anchor(url(section, item), '<strong>' + tx(label) + '</strong><small>' + tx(source.title) + '</small>')
        body += '</div><div class="grid">'
        for group, group_title in GROUPS.items():
            body += '<section class="card"><h2>' + tx(group_title) + '</h2><ul class="links">'
            body += ''.join(entry(url(a.key), tx(a.title)) for a in AREAS if a.group == group)
            body += '</ul></section>'
        body += '</div>'
    else:
        path = [anchor(url(), directory)]
        if from_admin:
            path.append(anchor(url('admin'), admin_title))
        elif area.key in HR_AREAS:
            path.append(anchor(url('hr'), hr_title))
        if record:
            path.extend([anchor(url(area.key), tx(area.title)), '<span aria-current="page">' + tx(record.title) + '</span>'])
        else:
            path.append('<span aria-current="page">' + tx(area.title) + '</span>')
        body = breadcrumb(*path)
        native_keys = (area.native,) + ALSO_NATIVE.get(area.key, ())
        buttons = ''.join(anchor(native_url(NATIVE[key][0]), NATIVE[key][1 + language_index], 'button subtle')
                          for key in native_keys if key in visible)
        if record:
            body += hero(tx(record.title), tx(record.status))
            body += '<div class="details"><section class="card"><h2>' + tr('Record details', 'Detalhes do registro') + '</h2><dl>'
            for label, value in record.fields:
                field_value = tx(value)
                sample = SAMPLE_FILES.get(value[0])
                if sample and value[0] == value[1]:
                    field_value = anchor(BASE + '/files/' + sample + '?lang=' + language, field_value)
                body += '<div><dt>' + tx(label) + '</dt><dd>' + field_value + '</dd></div>'
            body += '</dl></section>'
            if record.related:
                body += '<section class="card"><h2>' + tr('Related records', 'Registros relacionados') + '</h2><ul class="links">'
                for section, item in record.related:
                    related = BY_RECORD[(section, item)]
                    body += entry(url(section, item), tx(related.title), tx(BY_AREA[section].title))
                body += '</ul></section>'
            body += '</div>'
            if buttons:
                body += '<div class="actions">' + buttons + '</div>'
        else:
            body += hero(tx(area.title), tx(area.description), buttons)
            if len(area.records) > 1 or term:
                inputs = ''.join(f'<input type="hidden" name="{key}" value="{escape(value,quote=True)}">'
                                 for key, value in {**context, 'area': area.key}.items())
                body += ('<form class="filter" method="get" action="' + BASE + '">' + inputs
                         + '<label for="find">' + tr('Find a record in this area', 'Localizar um registro nesta área')
                         + '</label><div><input id="find" type="search" name="q" maxlength="80" value="' + escape(term, quote=True)
                         + '"><button class="button" type="submit">' + tr('Search', 'Buscar') + '</button>'
                         + (anchor(url(area.key), tr('Clear search', 'Limpar busca')) if term else '') + '</div></form>')
            words = norm(term).split()
            def matches(row):
                labels = [row.title, row.status, *(value for _, value in row.fields)]
                text = norm(' '.join(label[language_index] for label in labels))
                return all(word in text for word in words)
            entries = ''.join(entry(url(area.key, row.key), tx(row.title), tx(row.status)) for row in area.records if matches(row))
            body += '<section class="card"><h2>' + tr('Example records', 'Registros de exemplo') + '</h2>'
            body += ('<ul class="links">' + entries + '</ul>') if entries else '<p>' + tr('No matching records.', 'Nenhum registro encontrado.') + '</p>'
            body += '</section>'
    if embedded:
        return STYLESHEET + '<section data-demo-workspace lang="' + tr('en', 'pt-BR') + '">' + body + '</section>', status, 'pt-BR' if pt else 'en'
    full_title = hr_title if hr_index else admin_title if admin_index else tx(record.title) if record else tx(area.title) if area else title
    document = ('<!doctype html><html lang="' + tr('en','pt-BR') + '"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1"><title>' + full_title
                + ' · Wavelink</title>' + STYLESHEET + '</head><body>' + header
                + '<main>' + body + '</main></body></html>')
    return document, status, 'pt-BR' if pt else 'en'
