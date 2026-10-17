"""Portuguese Help remains complete, linked and isolated from operational data."""
import json
import os
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from test_corcovado_locale import company, client_for
from deploy.company_provision import read_marker
from deploy.company_runtime import ActivationService
from app.hosted_storage import PreparedProject
import uuid

SOURCE=Path(os.environ['WAVELINK_TEST_SOURCE'])
STATIC=SOURCE/'app/static'

def functional(soup):
    result=[]
    for tag in soup.find_all(True):
        attrs={k:v for k,v in tag.attrs.items() if k in {'id','href','src','name','data-topic','data-topic-row','data-index-topic'}}
        for k in ('href','src'):
            if k in attrs and str(attrs[k]).startswith('/static/'):
                attrs[k]=urlsplit(attrs[k]).path
        result.append((tag.name,attrs))
    return result

def test_all_portuguese_articles_keep_links_ids_and_code():
    files=list((STATIC/'help_topics').glob('*.html'))
    assert len(files)==77
    for original in files:
        a=BeautifulSoup(original.read_text(),'html.parser')
        b=BeautifulSoup((STATIC/'pt-BR/help_topics'/original.name).read_text(),'html.parser')
        assert b.html.get('lang')=='pt-BR',original.name
        assert functional(a)==functional(b),original.name
        assert [x.get_text() for x in a.find_all(['pre','code'])]==[x.get_text() for x in b.find_all(['pre','code'])],original.name
        assert a.find('article').get_text()!=b.find('article').get_text(),original.name

def test_help_search_uses_all_portuguese_topics():
    source=json.loads((STATIC/'help_catalogue.json').read_text())
    pt=json.loads((STATIC/'pt-BR/help_catalogue.json').read_text())
    assert [x['id'] for x in source['topics']]==[x['id'] for x in pt['topics']]
    assert pt['format']==source['format']
    assert all(x['heading'] and x['text'] for x in pt['topics'])
    assert any('passaporte' in x['text'].lower() for x in pt['topics'])
    script=(STATIC/'help_workspace.js').read_text()
    assert "locale==='pt-BR'" in script and '/static/pt-BR/help_catalogue.json' in script

def test_all_77_topics_are_actually_served_in_portuguese(company):
    root,cfg,settings,env=company
    ActivationService(PreparedProject(settings),read_marker(root)).complete(env['COMPANY_SETUP_KEY'],dict(request_id=str(uuid.uuid4()),login_id='admin',temporary_password=env['COMPANY_INITIAL_PASSWORD'],new_password='Fictional permanent password 012345.',confirm_password='Fictional permanent password 012345.'))
    with client_for(company) as client:
        for p in (STATIC/'help_topics').glob('*.html'):
            response=client.get('/help/topics/'+p.stem)
            assert response.status_code==200,p.name
            assert response.content==(STATIC/'pt-BR/help_topics'/p.name).read_bytes(),p.name
        catalogue=client.get('/static/pt-BR/help_catalogue.json')
        assert catalogue.status_code==200 and len(catalogue.json()['topics'])==77
        manual=client.get('/help/manual.pdf')
        assert manual.status_code==200
        assert manual.headers['content-language']=='pt-BR'
        assert manual.headers['cache-control']=='no-store'
        assert manual.content==(STATIC/'pt-BR/Wavelink_Guia_Usuario.pdf').read_bytes()
        import fitz
        with fitz.open(stream=manual.content,filetype='pdf') as document:
            assert document.page_count>=77
            assert len(document.get_toc())==77
            assert 'Recursos Humanos' in ''.join(page.get_text() for page in document)
        assert (SOURCE/'docs/user/Wavelink_User_Guide.pdf').read_bytes()==(Path(os.environ['WAVELINK_UI117_TEST_SOURCE'])/'docs/user/Wavelink_User_Guide.pdf').read_bytes()
