"""Organization chart reads canonical department designations and self-scoped HR records."""
from test_native_showcase import company


def test_authorized_org_chart(company):
    showcase, _ = company
    store = showcase.core.state.store
    accounts = showcase.core.state.accounts
    from app.departments import Departments
    departments = Departments(store)
    survey = next(d for d in departments.list(showcase.manager) if d['name'] == 'Offshore Survey')
    with store.connection() as c:
        uid = c.execute("SELECT id FROM users WHERE login_id='demo.shift1'").fetchone()[0]
        employee = accounts.session_person_in_connection(c, uid)
    restricted = store.hr.directory(employee)['org_chart']
    assert not restricted['show_heads']
    members = [p for group in restricted['units'] for p in group['people']]
    assert members and {p['name'] for p in members} == {employee['name']}
    assert all(set(p) == {'name','title','profile_id'} for p in members)
    assert all(p['profile_id']==uid for p in members)
    assert all(not group['heads'] for group in restricted['units'])

    def unit():
        return next(g for g in store.hr.directory(showcase.manager)['org_chart']['units']
                    if g['name'] == 'Offshore Survey')

    assert [p['name'] for p in unit()['heads']] == ['Lia Costa']
    departments.set_heads(survey['id'], [], survey['version'], showcase.manager, 'Fictional QA: clear designation')
    assert unit()['heads'] == []
    survey=departments.details(survey['id'],showcase.manager)
    departments.set_heads(survey['id'], [uid], survey['version'], showcase.manager, 'Temporary fictional QA designation')
    assert [p['name'] for p in unit()['heads']] == ['Lia Costa']
    assert all(p['name'] != 'Lia Costa' for p in unit()['people'])
    assert store.hr.directory(employee)['org_chart'] == restricted
