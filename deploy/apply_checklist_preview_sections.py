"""Show saved section labels beside the existing paged checklist items."""
from pathlib import Path
import runpy
import sys


def replace(source, before, after):
    if source.count(before) != 1:
        raise ValueError("Unexpected checklist preview source: " + before)
    return source.replace(before, after)


def workspace(source):
    source = replace(source, 'const rows = items.slice(start, start + checksPerPage).map(item => {',
                     '''const pageItems = items.slice(start, start + checksPerPage);
      function itemRow(item) {''')
    source = replace(source, """      }).join('');
      const chooser = stages.length""", """      }
      const groups = record.template.sections.map((section, index) => {
        const visible = pageItems.filter(item => item.section === section.id);
        if (!visible.length) return '';
        const title = section.title?.trim() || section.short?.trim();
        const heading = 'cw-preview-section-' + index;
        const label = title ? `<h4 id="${heading}">${esc(title)}</h4>` : '';
        const relationship = title ? ` aria-labelledby="${heading}"` : '';
        return `${label}<ul${relationship}>${visible.map(itemRow).join('')}</ul>`;
      }).join('');
      const chooser = stages.length""")
    return replace(source, '${rows?`<ul class="cw-item-list">${rows}</ul>`',
                   '${groups?`<div class="cw-item-list">${groups}</div>`')


def style(source):
    return replace(source, '.cw-item-list li {', '''.cw-item-list ul { list-style: none; margin: 0; padding: 0; }
.cw-item-list h4 { margin: .75rem 0 .125rem; overflow-wrap: anywhere; }
.cw-item-list li {''')


def transforms():
    return {'app/static/checklist_workspace.js': workspace, 'app/static/ui132_visual.css': style}


if __name__ == '__main__':
    build = Path(__file__).resolve()
    apply = runpy.run_path(str(build.with_name('apply_editor_exit.py')))['apply']
    apply(Path(sys.argv[1]), parent='b7f682701bc6f2ad081a5061f5f92d714ed3377300ef6e4879b7ddc53bf15a3d',
          overlays=(build.name,), previous_cache='ui162-date-filter-context', cache='ui162-checklist-preview-sections',
          suffix='checklist-preview-sections', scope='Show each saved section on the checklist item pages where it appears.')
