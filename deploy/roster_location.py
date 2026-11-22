from pathlib import Path


def transform(source):
    def replace(old, new):
        nonlocal source
        if source.count(old) != 1:
            raise ValueError("Unexpected roster integration point: " + old)
        source = source.replace(old, new)

    anchor = " function calendarHtml(){"
    replace(anchor, Path(__file__).with_suffix(".js").read_text(encoding="utf-8") + "\n" + anchor)
    start = "function calendarHtml(){\n  const filtered=window.AJHRInsights.select(workspace,planningQuery,planningFocus);\n  return "
    replace(start, start + "(canSection('shifts') ? locationRosterHtml() : '')+")
    replace("window.AJHRPlanning.mount(body);bindRecordActions(body);",
            "window.AJHRPlanning.mount(body);bindRecordActions(body);bindLocationRoster(el('hr-location-roster'));")
    replace("if(k==='shifts')html+=field('project',__hr121.t('Projeto'),p.project)",
            """if(k==='shifts')html+=field('project',wtext('Número ou nome do projeto (opcional)','Project number or name (optional)'),p.project)+'<datalist id="hr-shift-projects"></datalist>'""")
    hook = " function planningControls(f){"
    replace(hook, hook + """
  const options=f.node?.querySelector('#hr-shift-projects');
  if(options && !options.dataset.bound){options.dataset.bound='1';bindRosterProjects(f.node.elements.project,options,workspace,capture());}""")
    return source


def shift_project(source):
    anchor = "                values=self._values(c,kind,payload,record)\n"
    assert source.count(anchor) == 1
    return source.replace(anchor, anchor + """                if kind == 'shifts' and (not record or values['project'] != record.get('project', '')):
                    # Keep the assignment's text as a historical snapshot. Free text and blank remain valid.
                    label = values['project'].casefold()
                    project = c.execute('SELECT id,body FROM hr_timesheet_projects WHERE name_key=?',
                                        (label,)).fetchone() if label else None
                    values['roster_project_id'] = project['id'] if project and json.loads(project['body'])['active'] else ''
""")


def project_search(source):
    anchor = "        if location or project:\n"
    assert source.count(anchor) == 1
    source = source.replace(anchor, anchor + """            query = project.casefold()
            matching_projects = set()
            if query:
                for entry in c.execute('SELECT id,name_key,body FROM hr_timesheet_projects'):
                    if query in entry['name_key'] and (user['role'] == 'admin' or json.loads(entry['body'])['active']):
                        matching_projects.add(entry['id'])
            def matches_shift(row):
                return ((not location or location.casefold() in row.get('location','').casefold())
                        and (not query or query in row.get('project','').casefold()
                             or row.get('roster_project_id') in matching_projects))
""")
    old = "(not location or location.casefold() in r.get('location','').casefold()) and (not project or project.casefold() in r.get('project','').casefold())"
    assert source.count(old) == 2
    return source.replace(old, "matches_shift(r)")


def transforms():
    return {"app/static/hr_workspace.js": transform, "app/hr.py": shift_project, "app/hr_workspace.py": project_search}
