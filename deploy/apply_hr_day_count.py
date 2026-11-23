from pathlib import Path
import runpy
import sys


def workspace(source):
    start = source.index('   const events=ws.events.filter(e=>e.date===day);')
    end = source.index('   detail.innerHTML=', start)
    rows = source[start:end]
    source = source[:start] + '   const rows=rowsByDay.get(day);\n' + source[end:]
    anchor = '  const months=new Map();'
    # Both the detail panel and the count use this same filtered list, including
    # ongoing assignments that have no separate event on that date.
    project = """  const rowsByDay=new Map();
  const records=ws.roster.map(person=>[person,window.AJHRPlanning.personRecords(ws,person)]);
  for(const day of dates){
""" + rows.replace('for(const person of ws.roster)', 'for(const [person,assignments] of records)').replace('of window.AJHRPlanning.personRecords(ws,person)', 'of assignments') + """   rowsByDay.set(day,rows);
  }
"""
    source = source.replace(anchor, project + anchor, 1)
    label = "E(format(day,{dateStyle:'full'}))"
    button = source.index('days.map(day=>\'<button')
    source = source[:button] + source[button:].replace(label, "E(format(day,{dateStyle:'full'})+countLabel(day))", 1)
    source = source.replace(anchor, """  function countLabel(day){
   const total=rowsByDay.get(day).length;
   if(!total)return '';
   return ', '+total+' '+(total===1?wtext('compromisso','event'):wtext('compromissos','events'));
  }
""" + anchor, 1)
    old = "Number(day.slice(8))+'</button>'"
    new = "'<b>'+Number(day.slice(8))+'</b>'+(rowsByDay.get(day).length?'<small>'+rowsByDay.get(day).length+'</small>':'')+'</button>'"
    if source.count(old) != 1:
        raise ValueError('Unexpected calendar day markup')
    return source.replace(old,new)


CSS = """
@media(max-width:620px){
 .hr-mobile-days button{display:grid;grid-template-rows:24px 14px;align-content:center;justify-items:center;align-items:center}
 .hr-mobile-days button>b{font-weight:inherit}
 .hr-mobile-days button>small{color:inherit;font-size:.75rem;font-weight:700;line-height:14px}
}
"""


def transforms():
    return {'app/static/hr_workspace.js': workspace, 'app/static/hr_workspace.css': lambda s:s+CSS}


if __name__=='__main__':
    apply=runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]),parent='9bd26a95125a00baca60a302189bcaae23b95404c582d322224c88f52a963e09',overlays=(Path(__file__).name,),previous_cache='ui162-hr-mobile-calendar',cache='ui162-hr-mobile-day-count',suffix='hr-mobile-day-count',scope='Daily commitment counts on the mobile HR calendar.')
