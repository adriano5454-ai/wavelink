import pytest
from test_native_showcase import company, headers
from app import org_positions
from app.store import Problem


def test_reporting_positions(company):
    showcase, guest = company
    store, admin = showcase.core.state.store, showcase.manager
    with store.connection() as c:
        base=org_positions.snapshot(c,admin,False)
        department=next(d['id'] for d in base['departments'] if d['name']=='Offshore Survey')
        uid=next(p['id'] for p in base['people'] if p['name']=='Mara Brisa')
        employee=showcase.core.state.accounts.session_person_in_connection(c,uid)
        before=tuple(c.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone())
    fields=dict(id='',revision=0,department=department,new_department='',role='',new_role='Fictional position',parent='',person='')
    chart=org_positions.save(store,admin,fields,False)
    top=chart['positions'][0]
    assert not top['person'] and top['role'] in {r['id'] for r in chart['roles']}
    from app import company_roles
    with store.connection() as c:
        role=company_roles.get(c,top['role'])
        assert not role['permissions'] and not any(role['actions'].values()) and not role['delegation_capabilities']
    def save(**changes):
        return org_positions.save(store,admin,dict(fields,**changes),False)
    chart=save(revision=1,new_role='',role=top['role'],parent=top['id'],person=uid)
    child=next(r for r in chart['positions'] if r['person']==uid)
    with pytest.raises(Problem):save(revision=2,id=top['id'],parent=child['id'],role=top['role'],new_role='')
    with pytest.raises(Problem):save(revision=2,new_department='Fictional unit',department='',person=uid,role=top['role'],new_role='')
    with pytest.raises(Problem):save(revision=1)
    with pytest.raises(Problem):org_positions.save(store,employee,fields,False)
    chart=save(revision=2,id=child['id'],role=top['role'],new_role='',person=uid)
    assert not next(r for r in chart['positions'] if r['id']==child['id'])['parent']
    with store.connection() as c:
        assert before==tuple(c.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone())
        own=org_positions.snapshot(c,employee,False)
        assert not own['editor'] and len(own['positions'])==1
    response=guest.get('/api/hr/org-positions',headers=headers(showcase))
    assert response.status_code==200 and not response.json()['editor']
    assert guest.post('/api/hr/org-positions',json=fields,headers=headers(showcase)).status_code==403
