from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parent
one = runpy.run_path(str(BASE / 'apply_org_chart_filters.py'))['replace_once']


def recognition(source):
    anchor = ' function createNewsFeed(getHost, fmt, fleet = false) {'
    source = one(source, anchor, """ // The session owns the visit. Browser history carries only an opaque key,
 // never a news cursor, article or account identifier.
 const teamVisits = new Map();
 let pendingTeamVisit = null;
 function sameTabClick(event) {
  return event.button === 0 && !event.defaultPrevented && !event.ctrlKey && !event.metaKey && !event.shiftKey && !event.altKey;
 }
 function rememberTeamVisit(details) {
  const key = H.uid();
  const visit = {...details, key, route:location.hash || '#home', session:H.session()};
  teamVisits.set(key, visit);
  if (teamVisits.size > 20) teamVisits.delete(teamVisits.keys().next().value);
  pendingTeamVisit = visit;
  history.replaceState({...history.state, wlTeamSource:key}, '');
 }
 function teamOrigin(route) {
  const visit = teamVisits.get(history.state?.wlTeamSource);
  return visit && H && visit.session === H.session() && visit.route === route ? visit : null;
 }
 function teamArrival() {
  const visit = pendingTeamVisit || teamVisits.get(history.state?.wlTeamDestination);
  if (!visit || visit.session !== H.session() || location.hash !== '#team') return null;
  pendingTeamVisit = null;
  visit.awaitingReturn = true;
  history.replaceState({...history.state, wlTeamDestination:visit.key}, '');
  return visit;
 }
 document.addEventListener('click', event => {
  if (location.hash !== '#calendar' || !H || !sameTabClick(event) ||
      !event.target.closest?.('a[data-workspace="team"][href="#team"]')) return;
  const title = document.getElementById('calendar-agenda-title');
  if (title) rememberTeamVisit({day:document.querySelector('.calendar-day[aria-pressed=true]')?.dataset.calendarDay || '',
    calendarTop:title.getBoundingClientRect().top});
 }, true);
 window.addEventListener('hashchange', () => {
  if (location.hash !== '#team') pendingTeamVisit = null;
 });
 function positionTeamHeading(heading) {
  heading.tabIndex = -1;
  heading.focus({preventScroll:true});
  heading.style.scrollMarginTop = '80px';
  heading.scrollIntoView({block:'start', behavior:'instant'});
 }
 function restoreCalendarTeamReturn(day, panel) {
  const visit = teamOrigin('#calendar');
  if (!visit?.awaitingReturn || visit.day !== day) return false;
  const title = panel.querySelector('#calendar-agenda-title');
  requestAnimationFrame(() => {
   if (!title?.isConnected || location.hash !== '#calendar' || teamOrigin('#calendar') !== visit) return;
   visit.awaitingReturn = false;
   title.focus({preventScroll:true});
   window.scrollTo({top:window.scrollY + title.getBoundingClientRect().top - visit.calendarTop, behavior:'instant'});
  });
  return true;
 }
""" + anchor)
    source = one(source, 'owner=next;epoch++;homeEpoch++;directoryView=', 'owner=next;teamVisits.clear();pendingTeamVisit=null;epoch++;homeEpoch++;directoryView=')
    source = one(source, 'return {prepareProfileLeave:target', 'return {restoreCalendarTeamReturn,prepareProfileLeave:target')
    source = one(source, '  let homePage = 0, retryPage = 0;\n  const homeCursors = [null];', """  let homeReturn = compact && !fleet && route === '#home' && teamOrigin(route);
  let homePage = homeReturn ? homeReturn.page : 0, retryPage = 0, visiblePost = '';
  const homeCursors = homeReturn ? [...homeReturn.cursors] : [null];""")
    anchor = "  const homePager = find('.wl-home-news-pages');"
    source = one(source, anchor, anchor + """
  const allNews = find('.wl-home-news-all');
  if (allNews && !fleet) allNews.addEventListener('click', event => {
   if (current() && sameTabClick(event)) rememberTeamVisit({page:homePage, cursors:homeCursors.slice(0, homePage + 1),
     post:visiblePost, top:allNews.getBoundingClientRect().top});
  });""")
    anchor = '     homePage = page;'
    source = one(source, anchor, anchor + """
     visiblePost = String(result.posts[0]?.id || '');
     const returning = homeReturn;
     homeReturn = null;
     if (returning && returning.post === visiblePost) requestAnimationFrame(() => {
      if (!current() || teamOrigin(route) !== returning || !allNews?.isConnected) return;
      allNews.focus({preventScroll:true});
      window.scrollTo({top:window.scrollY + allNews.getBoundingClientRect().top - returning.top, behavior:'instant'});
     });""")
    anchor = "  const refreshNews=news.mount(content.querySelector('#wl-news'),false);"
    source = one(source, anchor, anchor + """
  const arrival = teamArrival();
  const target = arrival && (arrival.route === '#home' ? content.querySelector('#wl-news-title') : H.root.querySelector('.wl-rec-heading h1'));
  if (target) positionTeamHeading(target);
  const arrivalScroll = window.scrollY;""")
    anchor = "  await Promise.all([refresh(),refreshMoods(),refreshNews(),mountPeopleDirectory(content,ticket,session)]);"
    return one(source, anchor, anchor + """
  // The mood/feed sections above the news can grow during the first read.
  if (target?.isConnected && document.activeElement === target && location.hash === '#team' && ticket === epoch &&
      Math.abs(window.scrollY - arrivalScroll) < 2) positionTeamHeading(target);""")


def calendar(source):
    anchor = "paint();notice('');restore(anchor&&anchor.key===reqKey?{...anchor,key:key()}:null);"
    return one(source, anchor, """paint();notice('');
   if (background || !window.AJRecognition?.restoreCalendarTeamReturn?.(prefs.day,node))
    restore(anchor&&anchor.key===reqKey?{...anchor,key:key()}:null);""")


def transforms():
    return {'app/static/recognition_workspace.js': recognition, 'app/static/project_calendar.js': calendar}
