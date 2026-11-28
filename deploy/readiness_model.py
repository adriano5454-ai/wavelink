"""Operational readiness findings from source records the account can already read."""
from datetime import date, datetime, timedelta, timezone
import json

from .certificates import date_status
from .fieldwork_common import rows, member
from .hr import current as hr_current, expiry_status
from .personal_home import identity, finish_check
from .qshe_reports import allowed as qshe_allowed
from .store import Problem

RULES = {'certificates':'certificates.view','maintenance':'maintenance.view',
         'crew':'hr.view_own','qshe':'qshe.view'}
SEVERITY = {'urgent':0,'review':1,'upcoming':2}
LIMIT=500

def snapshot(store, actor, hub_id, *, now=None):
    now=now or datetime.now(timezone.utc)
    today=now.date()
    out=[]
    sources={}
    def issue(kind, row, severity, reason, due='', label=None, href=''):
        out.append(dict(kind=kind, id=row['id'], title=label if label is not None else row['title'],
                        severity=severity, reason=reason, due=due or '', href=href))
    with store.connection() as c:
        user,flags=identity(c,actor)
        if not any(flags.get(key) for key in RULES.values()):
            raise Problem(403,'No readiness source is available to this account.')
        if flags.get(RULES['certificates']):
            member(c,actor,RULES['certificates'])
            bucket=sources['certificates']=dict(records=0, scope='company')
            for r in rows(c,'asset_certificates'):
                if r.get('status')!='active' or r.get('archived') or r.get('superseded_by'): continue
                bucket['records']+=1
                state=date_status(r,today)
                match={'expired':('urgent','certificate_expired','expires_on'),
                       'due_soon':('upcoming','certificate_due','expires_on'),
                       'not_yet_valid':('review','certificate_not_yet_valid','valid_from'),
                       'expiry_not_recorded':('review','certificate_unknown','expires_on')}.get(state)
                if match:
                    level,reason,field=match
                    issue('certificates',r,level,reason,r.get(field),href='#certificates/'+r['id'])
        if flags.get(RULES['maintenance']):
            member(c,actor,RULES['maintenance'])
            bucket=sources['maintenance']=dict(records=0,scope='company')
            for r in rows(c,'maintenance_jobs'):
                blocked=r.get('status')=='completed' and (r.get('follow_up') or {}).get('state')=='blocked'
                if not blocked and r.get('status')!='open': continue
                bucket['records']+=1
                href='#maintenance/'+r['id']; title=r['name']; due=r.get('due_at','')
                if blocked:
                    issue('maintenance',r,'review','maintenance_follow_up',r['follow_up'].get('due_at'),title,href)
                elif not due:
                    issue('maintenance',r,'review','maintenance_undated','',title,href)
                else:
                    dt=datetime.fromisoformat(due.replace('Z','+00:00')).astimezone(timezone.utc)
                    if dt<now: issue('maintenance',r,'urgent','maintenance_overdue',due,title,href)
                    elif dt<=now+timedelta(days=7): issue('maintenance',r,'upcoming','maintenance_due',due,title,href)
        if flags.get(RULES['crew']) and not actor.get('guest'):
            hu,hf=hr_current(c,actor)
            manage=hf.get('hr.documents_manage',False)
            bucket=sources['crew']=dict(records=0,scope='company' if manage else 'own')
            query="SELECT body FROM hr_records WHERE kind='documents'"+('' if manage else ' AND user_id=?')
            for raw in c.execute(query,() if manage else (hu['id'],)):
                r=json.loads(raw[0])
                if not store.hr._read_allowed(r,hu,hf) or r.get('archived'): continue
                bucket['records']+=1
                state=expiry_status(r,today)
                match={'expired':('urgent','crew_expired'),'due_soon':('upcoming','crew_due'),
                       'unknown':('review','crew_unknown')}.get(state)
                if match:
                    level,reason=match
                    href='#hr/staff/'+r['user_id']+'/documents' if r['user_id']!=hu['id'] else '#hr/me/documents'
                    issue('crew',r,level,reason,r.get('expires_on'),r['title']+' · '+r['user_name'],href)
        if flags.get(RULES['qshe']):
            member(c,actor,RULES['qshe'])
            bucket=sources['qshe']=dict(records=0,scope='authorised')
            for raw in c.execute('SELECT body FROM qshe_reports'):
                r=json.loads(raw[0])
                if r.get('archived') or r['status'] in ('closed','cancelled') or not qshe_allowed(c,r,actor): continue
                bucket['records']+=1
                due=min([value for value in (r.get('due_on'),r.get('review_on')) if value] or [''])
                if r.get('priority')=='critical': level,reason='urgent','qshe_critical'
                elif due and date.fromisoformat(due)<today: level,reason='urgent','qshe_overdue'
                else: level,reason='review','qshe_open'
                issue('qshe',r,level,reason,due,href='#qshe/'+r['id'])
    finish_check(store,actor,user,flags)
    out.sort(key=lambda x:(SEVERITY[x['severity']], x['due'] or '~', x['kind'], x['id']))
    counts={key:sum(x['severity']==key for x in out) for key in SEVERITY}
    return dict(hub_id=hub_id,user_id=user['id'],as_of=now.isoformat(),sources=sources,
                counts=counts,items=out[:LIMIT],total=len(out))
