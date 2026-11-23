from pathlib import Path
import runpy
import sys

MOBILE_JS = ''' let mobileDay='';
 function mountMobileCalendar(board,ws){
  if(!board)return;
  const dates=window.AJHRPlanning.days(ws.start_on,ws.end_on);
  if(!dates.length)return;
  const locale=window.WavelinkI18n?.locale==='pt-BR'?'pt-BR':'en-GB';
  const format=(day,options)=>new Intl.DateTimeFormat(locale,{...options,timeZone:'UTC'}).format(new Date(day+'T12:00:00Z'));
  const months=new Map();
  for(const day of dates){
   const month=day.slice(0,7);
   if(!months.has(month))months.set(month,[]);
   months.get(month).push(day);
  }
  const weekdays=Array.from({length:7},(_,i)=>'<span>'+E(format('2024-01-0'+(i+1),{weekday:'short'}))+'</span>').join('');
  board.innerHTML=Array.from(months.values(),days=>{
   const offset=(new Date(days[0]+'T12:00:00Z').getUTCDay()+6)%7;
   return '<h3>'+E(format(days[0],{month:'long',year:'numeric'}))+'</h3><div class="hr-mobile-days">'+weekdays+'<i aria-hidden="true"></i>'.repeat(offset)+days.map(day=>'<button type="button" data-hr-day="'+day+'" aria-label="'+E(format(day,{dateStyle:'full'}))+'"'+(day===localDay()?' aria-current="date"':'')+'>'+Number(day.slice(8))+'</button>').join('')+'</div>';
  }).join('')+'<section class="hr-mobile-detail" aria-live="polite"></section>';
  const detail=board.querySelector('.hr-mobile-detail');
  const buttons=Array.from(board.querySelectorAll('[data-hr-day]'));
  function selectDay(day){
   mobileDay=day;
   buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.hrDay===day)));
   const events=ws.events.filter(e=>e.date===day);
   const rows=events.map(e=>'<li>'+recordLink(e,[e.label,e.user_name,e.title].filter(Boolean).join(' · '))+'</li>');
   for(const person of ws.roster){
    for(const r of window.AJHRPlanning.personRecords(ws,person)){
     if(r.start_on<=day && day<=r.end_on && !events.some(e=>e.kind===r.kind&&e.id===r.id))
      rows.push('<li>'+recordLink(r,[window.AJHRPlanning.kindLabel(r.assignment_type),person.name,r.location].filter(Boolean).join(' · '))+'</li>');
    }
   }
   detail.innerHTML='<h3>'+E(format(day,{dateStyle:'full'}))+'</h3>'+(rows.length?'<ul>'+rows.join('')+'</ul>':'<p>'+E(wtext('Nenhum compromisso neste dia.','No events on this day.'))+'</p>');
   bindRecordActions(detail);
  }
  buttons.forEach(b=>b.onclick=()=>selectDay(b.dataset.hrDay));
  selectDay(dates.includes(mobileDay)?mobileDay:dates.includes(localDay())?localDay():dates[0]);
 }
'''
MOBILE_CSS = '''
.hr-mobile-calendar{display:none}
@media(max-width:620px){
 #hr-planning-results:has(.hr-mobile-calendar) .ux-timeline-mobile,
 #hr-planning-results:has(.hr-mobile-calendar) .ux-timeline-desktop,
 #hr-planning-results:has(.hr-mobile-calendar) .ux123-planning-key{display:none}
 .hr-mobile-calendar{display:block;min-width:0}
 .hr-mobile-days{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:2px;text-align:center}
 .hr-mobile-days span{font-size:.75rem;color:#456170}
 .hr-mobile-days button{min-width:0;min-height:44px;padding:0;border:1px solid #c6d9dd;border-radius:6px;background:#fff;color:#123b44;font:inherit}
 .hr-mobile-days button[aria-current=date]{border-color:#087983}
 .hr-mobile-days button[aria-pressed=true]{background:#075e67;color:white}
 .hr-mobile-detail{margin-block:1rem;overflow-wrap:anywhere}
 .hr-mobile-detail ul{padding-inline-start:1.2rem}
}
'''

def workspace(source):
    def change(old, new):
        nonlocal source
        if source.count(old) != 1:
            raise ValueError('Unexpected HR calendar source: ' + old)
        source = source.replace(old, new)
    change(' function calendarHtml(){', MOBILE_JS + ' function calendarHtml(){')
    change('window.AJHRPlanning.render(filtered,planningView)', "(planningView==='timeline'?'<section class=\"hr-mobile-calendar\"></section>':'')+window.AJHRPlanning.render(filtered,planningView)")
    change('  window.AJHRPlanning.mount(body);', """  const mobileBoard=body.querySelector('.hr-mobile-calendar');
  if(mobileBoard)mountMobileCalendar(mobileBoard,window.AJHRInsights.select(workspace,planningQuery,planningFocus));
  window.AJHRPlanning.mount(body);""")
    return source

def transforms():
    return {'app/static/hr_workspace.js': workspace, 'app/static/hr_workspace.css': lambda s:s+MOBILE_CSS}

if __name__=='__main__':
    apply=runpy.run_path(str(Path(__file__).with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]),parent='9a3b5f42c37c8bb2f1467f77ab137c0eba187e7749268092909e4821cd53e2a1',overlays=(Path(__file__).name,),previous_cache='ui162-inventory-physical-location',cache='ui162-hr-mobile-calendar',suffix='hr-mobile-calendar',scope='Compact mobile HR calendar with selected-day records.')
