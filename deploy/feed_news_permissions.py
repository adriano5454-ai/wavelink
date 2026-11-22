"""Add individual news publishing to the existing account access editor."""


def edit(*changes):
    def apply(source):
        for old, new in changes:
            if source.count(old) != 1:
                raise ValueError(f"Unexpected news permission source near {old[:65]!r}")
            source = source.replace(old, new)
        return source
    return apply


def transforms():
    # Older account editors send their complete previous catalogue. Keep the
    # unseen grant as-is inside the same version-checked transaction.
    access = edit(
        (" ('Project backups',[", " ('Team news',[('news.publish','Publish team news')]),\n ('Project backups',["),
        ("  base['it.manage']=False", "  base['news.publish']=False\n  base['it.manage']=False"),
        ("set(permissions)!=KEYS", "set(permissions) not in (KEYS, KEYS-{'news.publish'})"),
        ("  c.execute('INSERT INTO account_permissions",
         "  if 'news.publish' not in new:\n   new={**new,'news.publish':base_effective(c,uid,user['role'])['news.publish']}\n"
         "  c.execute('INSERT INTO account_permissions"),
    )
    roles = edit(
        ("allow_legacy_administrator: bool = False, preset_id: str = '')",
         "allow_legacy_administrator: bool = False, stored_snapshot: bool = False, preset_id: str = '')"),
        ("        complete = permitted == KEYS",
         "        # The previous complete administrator catalogue remains valid for stored roles\n"
         "        # and invitations. Keep its signed permission list exactly as recorded.\n"
         "        complete = permitted == KEYS or (stored_snapshot and permitted == KEYS - {'news.publish'})"),
        ("allow_legacy_administrator=historical, preset_id=row['id']",
         "allow_legacy_administrator=historical, stored_snapshot=True, preset_id=row['id']"),
        ("        if 'backups.export' in permitted or",
         "        if 'news.publish' in permitted:\n"
         "            raise Problem(422, _rt('Grant news publishing in the individual account permissions.'))\n"
         "        if 'backups.export' in permitted or"),
    )
    return {
        'app/access.py': access,
        'app/membership_policy.py': edit(
            ("return {*ACTION_KEYS, 'backups.export'", "return {*ACTION_KEYS, 'news.publish', 'backups.export'")),
        'app/company_roles.py': roles,
        'app/company_membership.py': edit(
            ("allow_legacy_administrator=historical,preset_id=row['preset_id']",
             "allow_legacy_administrator=historical,stored_snapshot=True,preset_id=row['preset_id']")),
        'tests/ui65_roles_access/test_catalogue_upgrade_ui153.py': edit(
            ("permissions,delegated,initial=replace_catalogue(h,excluded)",
             "permissions,delegated,initial=replace_catalogue(h,excluded | {'news.publish'})")),
        'app/browser_admin.py': edit(
            ("set(p['permissions']) != access.KEYS",
             "set(p['permissions']) not in (access.KEYS, access.KEYS - {'news.publish'})")),
        'app/static/browser_admin.js': edit(
            ("const individualOnly=k=>k.startsWith('members.')", "const individualOnly=k=>k==='news.publish'||k.startsWith('members.')")),
        'app/access_ui.py': edit(
            ("  for k,v in values.items():flags[k].set(v)",
             "  for k,v in values.items():\n   if mode!='all' or k!='news.publish':flags[k].set(v)")),
        'app/static/membership_workspace.js': edit(
            ("new Set(['backups.export','handovers.shifts_all_departments'])",
             "new Set(['backups.export','handovers.shifts_all_departments','news.publish'])")),
        'app/static/permission_labels.js': edit(
            ('  "backups.export":', '  "news.publish": "Publish team news",\n  "backups.export":')),
        'app/static/locale_pt_br.js': edit(
            ('window.WAVELINK_PT_BR=Object.freeze({',
             'window.WAVELINK_PT_BR=Object.freeze({\n'
             '  "Team news": "Notícias da equipe",\n'
             '  "Publish team news": "Publicar notícias da equipe",')),
        'app/report_localization.py': lambda source: source + """

REPORT_MESSAGES_PT_BR.update({
    'Team news': 'Notícias da equipe',
    'Publish team news': 'Publicar notícias da equipe',
    'Grant news publishing in the individual account permissions.':
        'Conceda a permissão para publicar notícias nas permissões individuais da conta.',
})
""",
    }
