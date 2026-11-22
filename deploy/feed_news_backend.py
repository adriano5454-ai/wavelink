"""Install the news API, request limits and selective transfer behavior."""
from pathlib import Path


def replace_once(source, old, new):
    if source.count(old) != 1:
        raise ValueError('Unexpected feed news integration near ' + old)
    return source.replace(old, new)


def server(source):
    anchor = '    attach_recognition(app,store,config,actor)'
    source = replace_once(source, anchor, anchor + '''
    from .feed_news_backend import attach as attach_feed_news
    attach_feed_news(app,store,config,actor)''')
    anchor = '        default_limit = RECOGNITION_BODY_LIMIT if profile_save else 100_000'
    source = replace_once(source, anchor, anchor + '''
        news_save = req.method == 'POST' and req.url.path == '/api/recognition/news'
        if news_save:
            from .feed_news_media import MAX_DATA_URL_LENGTH
            default_limit = MAX_DATA_URL_LENGTH + 65_536''')
    anchor = "else RECOGNITION_BODY_LIMIT if req.url.path.startswith('/api/recognition/')"
    return replace_once(source, anchor, 'else default_limit if news_save ' + anchor)


def transforms():
    return {'app/server.py': server,
            'app/project_modules.py': lambda source: replace_once(
                source, 'RECOGNITION_TRANSFER_CACHE = {',
                "RECOGNITION_TRANSFER_CACHE = {\n    'feed_news_posts', 'feed_news_images',")}


def additions():
    return {'app/feed_news_backend.py': Path(__file__).with_name(
        'feed_news_backend_payload.py').read_text(encoding='utf-8')}
