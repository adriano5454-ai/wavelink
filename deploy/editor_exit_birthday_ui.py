"""Add optional member birthdays to Team and the member's own profile."""
from pathlib import Path


def recognition(source):
    js = Path(__file__).with_suffix('.js').read_text(encoding='utf-8')
    news = '<section id="wl-news" class="card wl-news"></section>'
    language = '<section class="card wl-profile-language" id="profile-language"></section>'
    changes = (
        (' async function openTeam(){', js + '\n async function openTeam(){'),
        ("  const featured=home.querySelector('#wl-news');", """  const birthdays=home.querySelector('#wl-home-birthdays');
  if(birthdays && birthdayHomes.get(birthdays)!==owner){
   birthdayHomes.set(birthdays,owner);
   mountTeamBirthdays(birthdays,epoch,owner);
  }
  const featured=home.querySelector('#wl-news');"""),
        (news, '<div class="wl-team-news-row">' + news +
         '<aside class="card wl-team-birthdays" id="wl-team-birthdays" aria-labelledby="wl-birthday-title"></aside></div>'),
        ('  const refreshMoods=mountTeamMoods(content,ticket,session);',
         "  mountTeamBirthdays(content.querySelector('#wl-team-birthdays'),ticket,session);\n"
         '  const refreshMoods=mountTeamMoods(content,ticket,session);'),
        (language, language + '<section class="card" id="profile-team-birthday"></section>'),
        ('hydrateAvatars(content);if(own){',
         "hydrateAvatars(content);if(own){mountBirthdayPreference(content.querySelector('#profile-team-birthday'),ticket,session);"),
    )
    for old, new in changes:
        if source.count(old) != 1:
            raise ValueError(f'Could not locate Team birthday integration: {old}')
        source = source.replace(old, new)
    return source


def home(source):
    rail = '<aside class="ph-dashboard-rail" aria-label="Profile and Team recognition">'
    if source.count(rail) != 1:
        raise ValueError('Could not locate the Home sidebar')
    return source.replace(rail, rail + '<section id="wl-home-birthdays" class="card wl-team-birthdays" aria-labelledby="wl-birthday-title"></section>')


def transforms():
    css = Path(__file__).with_suffix('.css').read_text(encoding='utf-8')
    return {'app/static/recognition_workspace.js': recognition, 'app/static/personal_home.js': home,
            'app/static/recognition_workspace.css': lambda source: source + '\n' + css}
