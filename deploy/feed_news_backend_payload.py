"""Company news, visible to the company or a current vessel/base audience."""
from __future__ import annotations

import hashlib
import json
import os
import unicodedata
import uuid

from fastapi import Depends, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, ConfigDict, Field

from . import access, feed_news_media as media, fleet_access
from .fieldwork_common import ident
from .store import Problem, pack, utcnow


class NewsDraft(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    op_id: str = Field(min_length=36, max_length=36)
    title: str = Field(min_length=1, max_length=140)
    body: str = Field(min_length=1, max_length=3000)
    site_id: str | None = Field(default=None, min_length=36, max_length=36)
    image: str | None = Field(default=None, max_length=media.MAX_DATA_URL_LENGTH)


def ensure(c):
    c.execute('''CREATE TABLE IF NOT EXISTS feed_news_posts(
        seq INTEGER PRIMARY KEY, id TEXT NOT NULL UNIQUE, op_id TEXT NOT NULL,
        fingerprint TEXT NOT NULL, author_id TEXT NOT NULL REFERENCES users(id),
        author_name TEXT NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL,
        site_id TEXT, site_name TEXT, created_at TEXT NOT NULL,
        has_image INTEGER NOT NULL CHECK(has_image IN (0,1)),
        UNIQUE(author_id,op_id))''')
    c.execute('CREATE INDEX IF NOT EXISTS feed_news_site_page ON feed_news_posts(site_id,seq DESC)')
    media.ensure(c)


def _member(store, c, actor, *, fleet=False):
    user = store.recognition._person(c, actor)
    guest = os.environ.get('DEMO_GUEST_LOGIN', 'guest.demo').strip().casefold()
    if user['login_id'].casefold() == guest:
        raise Problem(403, 'Use a personal account with access to the team.')
    if fleet:
        if user['role'] != 'admin' and not fleet_access.logistics_enabled(c, user['id']):
            raise Problem(403, 'Your account needs Fleet access to view vessel or base news here.')
        return user, False
    flags = access.effective(c, user['id'], user['role'])
    if fleet_access.restricted(c, user['id']) or not any(flags.values()):
        raise Problem(403, 'Use a personal account with access to the team.')
    return user, bool(flags['news.publish'])


def _sites(c, user, *, fleet=False):
    query = "SELECT id,body FROM fleet_sites WHERE json_extract(body,'$.active')=1"
    params = []
    if user['role'] != 'admin':
        # A published location label, task assignment, or visible directory entry
        # does not establish a person's current location audience.
        uid = user['id']
        query += ''' AND id IN (
            SELECT site_id FROM fleet_site_grants
            WHERE user_id=? AND role IN ('viewer','operator','manager') AND ?'''
        params = [uid, fleet_access.logistics_enabled(c, uid)]
        if not fleet:
            today = utcnow()[:10]
            query += ''' UNION SELECT json_extract(body,'$.work_site.id') FROM hr_records
                WHERE kind='shifts' AND user_id=? AND json_extract(body,'$.status')='confirmed'
                AND json_extract(body,'$.assignment_type') IN ('offshore','onshore')
                AND json_extract(body,'$.start_on')<=? AND json_extract(body,'$.end_on')>=?'''
            params.extend([uid, today, today])
        query += ')'
    sites = {}
    for row in c.execute(query, params):
        site = json.loads(row['body'])
        sites[row['id']] = dict(id=row['id'], name=site['name'], kind=site['kind'])
    return sites


FIELDS = ('id', 'title', 'body', 'author_id', 'author_name', 'created_at', 'site_id', 'site_name')


def _public(row):
    return {**{key: row[key] for key in FIELDS}, 'has_image': bool(row['has_image'])}


def _read_scope(store, c, actor, fleet, site_id=''):
    user, can_publish = _member(store, c, actor, fleet=fleet)
    sites = _sites(c, user, fleet=fleet)
    if site_id:
        if site_id not in sites:
            raise Problem(404, 'This vessel or base is unavailable to your account.')
        sites = {site_id: sites[site_id]}
    audience = 'site_id IN (SELECT value FROM json_each(?))'
    if not fleet:
        audience = 'site_id IS NULL OR ' + audience
    return 'SELECT * FROM feed_news_posts WHERE (' + audience + ')', [pack(list(sites))], sites, can_publish


def list_news(store, actor, limit, before, *, fleet=False, site_id=''):
    if type(limit) is not int or not 1 <= limit <= 50:
        raise Problem(422, 'Choose between 1 and 50 news posts.')
    with store.connection() as c:
        query, params, sites, can_publish = _read_scope(store, c, actor, fleet, site_id)
        if before:
            cursor = c.execute(query + ' AND id=?', [*params, ident(before)]).fetchone()
            if cursor is None:
                raise Problem(422, 'Refresh the news feed to continue.')
            query += ' AND seq<?'
            params.append(cursor['seq'])
        rows = c.execute(query + ' ORDER BY seq DESC LIMIT ?', [*params, limit + 1]).fetchall()
        choices = sorted(sites.values(), key=lambda s: (s['name'].casefold(), s['id'])) if can_publish else []
        return dict(posts=[_public(row) for row in rows[:limit]],
                    next_cursor=rows[limit - 1]['id'] if len(rows) > limit else None,
                    can_publish=can_publish, sites=choices)


def _publish_scope(store, c, actor, site_id):
    user, _ = _member(store, c, actor)
    access.require(c, actor, 'news.publish')
    if site_id is None:
        return user, None
    site = _sites(c, user).get(site_id)
    if site is None:
        raise Problem(422, 'Choose an active vessel or base available to you.')
    return user, site['name']


def _text(value, allowed_controls):
    value = value.strip()
    if not value or any(unicodedata.category(ch) in ('Cc', 'Cs') and ch not in allowed_controls
                        for ch in value):
        raise Problem(422, 'Enter a title and message using readable text.')
    return value


def publish(store, actor, draft):
    if not isinstance(draft, NewsDraft):
        draft = NewsDraft.model_validate(draft)
    op_id = ident(draft.op_id)
    site_id = ident(draft.site_id) if draft.site_id is not None else None
    title = _text(draft.title, '')
    body = _text(draft.body, '\r\n\t')
    # Authorize before decoding an upload; check again inside the atomic write.
    with store.connection() as c:
        _publish_scope(store, c, actor, site_id)
    prepared = media.prepare_image(draft.image)
    image_hash = hashlib.sha256(prepared[1]).hexdigest() if prepared else None
    fingerprint = hashlib.sha256(pack([title, body, site_id, image_hash]).encode()).hexdigest()
    with store.connection(True) as c:
        user, site_name = _publish_scope(store, c, actor, site_id)
        prior = c.execute('SELECT * FROM feed_news_posts WHERE author_id=? AND op_id=?',
                          (user['id'], op_id)).fetchone()
        if prior is not None:
            if prior['fingerprint'] != fingerprint:
                raise Problem(409, 'This publication reference was already used for different news.')
            return {'post': _public(prior)}
        post_id = str(uuid.uuid4())
        c.execute('''INSERT INTO feed_news_posts(
            id,op_id,fingerprint,author_id,author_name,title,body,site_id,site_name,created_at,has_image)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
            (post_id, op_id, fingerprint, user['id'], user['name'], title, body, site_id,
             site_name, utcnow(), int(prepared is not None)))
        if prepared:
            media.store_image(c, post_id, prepared)
        return {'post': _public(c.execute('SELECT * FROM feed_news_posts WHERE id=?', (post_id,)).fetchone())}


def get_image(store, actor, post_id, *, fleet=False):
    with store.connection() as c:
        query, params, _, _ = _read_scope(store, c, actor, fleet)
        post = c.execute(query + ' AND id=? AND has_image=1', [*params, post_id]).fetchone()
        image = media.load_image(c, post_id) if post else None
        if image is None:
            raise Problem(404, 'This news image is unavailable.')
        return image


def attach(app, store, config, actor):
    with store.connection(True) as c:
        ensure(c)

    def reader(req: Request, a=Depends(actor)):
        if req.headers.getlist('x-aj-hub-id') != [config['hub_id']]:
            raise Problem(409, 'Confirm the selected project before continuing.',
                          hub_changed=True, hub_id=config['hub_id'])
        return a

    private = {'Cache-Control': 'private, no-store', 'X-Content-Type-Options': 'nosniff'}

    @app.get('/api/recognition/news')
    def feed(req: Request, limit: int = 10, before: str = '', a=Depends(reader)):
        result = list_news(store, a, limit, before)
        if getattr(req.state, 'public_demo_read_only', False) is True:
            result.update(can_publish=False, sites=[])
        return JSONResponse(result, headers=private)

    @app.post('/api/recognition/news')
    def post_news(draft: NewsDraft, a=Depends(reader)):
        return JSONResponse(publish(store, a, draft), headers=private)

    @app.get('/api/fleet/news')
    def fleet_feed(limit: int = 10, before: str = '', site_id: str = '', a=Depends(reader)):
        return JSONResponse(list_news(store, a, limit, before, fleet=True, site_id=site_id), headers=private)

    def inline(image):
        mime, content = image
        return Response(content, media_type=mime, headers={**private, 'Content-Disposition': 'inline'})

    @app.get('/api/recognition/news/{post_id}/image')
    def image(post_id: str, a=Depends(reader)):
        return inline(get_image(store, a, post_id))

    @app.get('/api/fleet/news/{post_id}/image')
    def fleet_image(post_id: str, a=Depends(reader)):
        return inline(get_image(store, a, post_id, fleet=True))
