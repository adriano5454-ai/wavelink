"""Reporting positions describe work; only existing membership controls grant access."""
from uuid import uuid4
from . import company_roles, departments, membership_policy
from .accounts import Accounts
from .hr import current
from .store import Problem


def schema(c):
    c.execute("""CREATE TABLE IF NOT EXISTS hr_org_positions(
        id TEXT PRIMARY KEY, department TEXT NOT NULL REFERENCES ops_departments(id),
        role TEXT NOT NULL REFERENCES company_role_presets(id), parent TEXT REFERENCES hr_org_positions(id),
        person TEXT REFERENCES users(id), version INTEGER NOT NULL, UNIQUE(department,person))""")


def snapshot(c, actor, public):
    user, caps = current(c, actor)
    editor = bool(not public and user['role']=='admin' and caps['hr.people_manage'])
    query = """SELECT p.*, d.name AS dept_name, r.name AS role_name, u.name AS person_name
               FROM hr_org_positions p JOIN ops_departments d ON d.id=p.department
               JOIN company_role_presets r ON r.id=p.role LEFT JOIN users u ON u.id=p.person
               WHERE d.active=1"""
    args = ()
    if not caps['hr.people_manage']:
        query += ' AND p.person=?'
        args = (user['id'],)
    rows = [dict(r) for r in c.execute(query+' ORDER BY d.name,r.name,p.id',args)]
    visible = {r['id'] for r in rows}
    for row in rows:
        if row['parent'] not in visible:
            row['parent'] = None
    result = dict(positions=rows, editor=editor)
    if editor:
        result['revision'] = revision(c)
        result['departments'] = [dict(r) for r in c.execute('SELECT id,name FROM ops_departments WHERE active ORDER BY name')]
        result['roles'] = [dict(id=r['id'],name=company_roles.for_display(r)['display_name']) for r in company_roles.list_public(c) if r['active']]
        result['people'] = [dict(id=r['id'],name=r['name'],departments=sorted(departments.membership_ids(c,r['id'],active_only=True)))
                            for r in c.execute('SELECT id,name FROM users WHERE enabled ORDER BY name')]
    return result


def revision(c):
    return c.execute('SELECT COALESCE(sum(version),0) FROM hr_org_positions').fetchone()[0]


def save(store, actor, p, public):
    if public:
        raise Problem(403,'Read-only demo.')
    keys = {'id','revision','department','new_department','role','new_role','parent','person'}
    if not isinstance(p,dict) or set(p)!=keys or type(p['revision']) is not int or any(
            not isinstance(p[k],str) or len(p[k])>200 for k in keys-{'revision'}):
        raise Problem(422,'Invalid position.')
    with store.connection(True) as c:
        user,caps=current(c,actor)
        Accounts._admin(c,actor)
        if not caps['hr.people_manage']:
            raise Problem(403,'HR management required.')
        if revision(c)!=p['revision']:
            raise Problem(409,'Chart changed. Reopen before saving.')
        pos=p['id'] or str(uuid4())
        old=c.execute('SELECT * FROM hr_org_positions WHERE id=?',(pos,)).fetchone()
        if p['id'] and not old:
            raise Problem(404,'Position unavailable.')
        dept,role,parent,person=p['department'],p['role'],p['parent'] or None,p['person'] or None
        if bool(dept)==bool(p['new_department']) or bool(role)==bool(p['new_role']):
            raise Problem(422,'Choose one department and one role.')
        if p['new_department']:
            name=departments.normal_group(p['new_department'])
            if departments.lookup(c,name):
                raise Problem(409,'Department already exists.')
            dept=departments._new(c,name,'',actor)
        if not c.execute('SELECT 1 FROM ops_departments WHERE id=? AND active',(dept,)).fetchone():
            raise Problem(422,'Department unavailable.')
        if old and old['department']!=dept and c.execute('SELECT 1 FROM hr_org_positions WHERE parent=?',(pos,)).fetchone():
            raise Problem(409,'Move subordinate positions first.')
        if person:
            if (not c.execute('SELECT 1 FROM users WHERE id=? AND enabled',(person,)).fetchone()
                    or dept not in departments.membership_ids(c,person,active_only=True)):
                raise Problem(422,'Choose an active department member.')
            if c.execute('SELECT 1 FROM hr_org_positions WHERE department=? AND person=? AND id<>?',(dept,person,pos)).fetchone():
                raise Problem(409,'Person already occupies a position in this department.')
        cursor=parent
        while cursor:
            if cursor==pos:
                raise Problem(422,'A position cannot report to itself or a subordinate.')
            node=c.execute('SELECT parent FROM hr_org_positions WHERE id=? AND department=?',(cursor,dept)).fetchone()
            if not node:
                raise Problem(422,'Choose a position in the same department.')
            cursor=node[0]
        if p['new_role']:
            name=company_roles.normal_name(p['new_role'])
            if any(r['name'].casefold()==name.casefold() for r in company_roles.list_public(c)):
                raise Problem(409,'Role already exists.')
            profile=dict(key='org-'+uuid4().hex,name=name,description='',family='participant',security_role='technician',
                         permissions=[],actions={k:False for k in membership_policy.ACTION_KEYS},
                         delegation_capabilities=[],task_management=False,active=True)
            role=company_roles.save_revision(c,profile,actor_id=user['id'],expected_revision=0)['id']
            membership_policy.audit(c,user['id'],role,'role_profile_saved',{'before_revision':0,'revision':1,'name':name})
        else:
            company_roles.get(c,role,active=True)
        c.execute("""INSERT INTO hr_org_positions VALUES(?,?,?,?,?,1) ON CONFLICT(id) DO UPDATE SET
                     department=excluded.department,role=excluded.role,parent=excluded.parent,
                     person=excluded.person,version=version+1""",(pos,dept,role,parent,person))
        membership_policy.audit(c,user['id'],pos,'org_position_saved',dict(department=dept,role=role,parent=parent,person=person))
        return snapshot(c,actor,False)
