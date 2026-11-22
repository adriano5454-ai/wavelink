"""Exercise the read-only preview against fictional users and retained revisions."""
from tests.browser_admin.test_admin import dump, h
from tests.handovers.test_handovers import change, create, publish
from tests.ui33_usability.test_files import action, create_files, file, reopened


def preview(h, ident, *, revision=None, token=None):
    return h.client.get('/api/handovers/'+ident+'/preview',headers=h.headers(token),
                        params={'revision':revision} if revision is not None else {})


def test_preview_is_private_revision_specific_and_read_only(h):
    first=publish(h,create(h))
    corrected=change(h,first,'start_revision')
    correction=dict(corrected['draft'],summary='Private notes for the next issue.')
    corrected=change(h,corrected,'save_draft',edit=correction)
    before=dump(h)
    own=preview(h,first['id'])
    assert own.status_code==200 and own.json()['edit']['summary']==correction['summary']
    assert own.json()['can_edit'] and own.json()['revision'] is None
    assert preview(h,first['id'],token=h.wt).status_code==404
    for token in [None,h.wt]:
        shown=preview(h,first['id'],revision=1,token=token)
        assert shown.status_code==200 and shown.headers['cache-control']=='no-store'
        assert shown.json()['edit']['summary']==first['publication']['edit']['summary']
        assert shown.json()['revision']==1 and not shown.json()['can_edit']
        assert 'recipient_user_ids' not in shown.json()['edit'] and 'draft' not in shown.json()
    assert preview(h,first['id'],revision=2,token=h.wt).status_code==404
    assert dump(h)==before
    published=publish(h,corrected)
    assert published['published_revision']==2
    assert preview(h,first['id'],revision=1,token=h.wt).json()['edit']['summary']!=correction['summary']
    assert preview(h,first['id'],revision=2,token=h.wt).json()['edit']['summary']==correction['summary']


def test_preview_shows_only_attachments_from_its_version(h):
    _,draft,_,original=create_files(h)
    ident=draft['id']
    assert [f['filename'] for f in preview(h,ident).json()['files']]==[f['filename'] for f in original]
    assert preview(h,ident,token=h.wt).status_code==404
    revised=[file('issued-evidence.txt')]
    issued,_=action(h,reopened(h,ident),revised,'finish')
    assert issued.status_code==200,issued.text
    before=dump(h)
    assert [f['filename'] for f in preview(h,ident,revision=1,token=h.wt).json()['files']]==['issued-evidence.txt']
    assert preview(h,ident).status_code==404
    assert dump(h)==before
