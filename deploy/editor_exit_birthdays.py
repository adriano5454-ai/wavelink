"""Add voluntary birthdays to Team without reading private personnel records."""
from pathlib import Path


def replace(source, old, new):
    if source.count(old) != 1:
        raise ValueError(f'Unexpected birthday integration near {old[:64]}')
    return source.replace(old, new)


def routes(source):
    anchor = '    app.state.daily_moods = daily_moods'
    source = replace(source, anchor, anchor + '''
    from .team_birthdays import TeamBirthdays
    birthdays = TeamBirthdays(store, config['hub_id'], brand.get('id'),
                              app.state.document_invitations.shared_login)
    app.state.team_birthdays = birthdays''')
    anchor = 'class MoodSave(Strict):'
    source = replace(source, anchor, '''class BirthdaySave(Strict):
    month: int | None = Field(ge=1, le=12)
    day: int | None = Field(ge=1, le=31)
    version: int = Field(ge=0)


''' + anchor)
    anchor = "    @app.get('/api/recognition/moods')"
    return replace(source, anchor, '''    @app.get('/api/recognition/birthdays')
    def upcoming_birthdays(limit: int = 6, offset: int = 0, a=Depends(logged)):
        return private(birthdays.upcoming(a, limit, offset))

    @app.get('/api/recognition/birthday')
    def my_birthday(a=Depends(logged)):
        return private(birthdays.mine(a))

    @app.post('/api/recognition/birthday')
    def save_my_birthday(p: BirthdaySave, req: Request, a=Depends(logged)):
        if getattr(req.state, 'public_demo_read_only', False):
            raise Problem(403, 'Profile changes are unavailable in the public demo.')
        return private(birthdays.save(a, p.month, p.day, p.version))

''' + anchor)


def transforms():
    return {
        'app/recognition_api.py': routes,
        'app/project_modules.py': lambda s: replace(
            s, "    'feed_news_posts', 'feed_news_images',",
            "    'feed_news_posts', 'feed_news_images', 'team_birthdays',"),
    }


def additions():
    return {'app/team_birthdays.py': Path(__file__).with_name(
        'editor_exit_birthdays_payload.py').read_text(encoding='utf-8')}
