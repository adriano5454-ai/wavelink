"""Generate public display labels from the existing access.GROUPS definition.
No user permissions, credentials, database or network access is read.
"""
from pathlib import Path
import ast,json,sys

def generate(runtime):
    runtime=Path(runtime)
    tree=ast.parse((runtime/'app/access.py').read_text(encoding='utf8'))
    assignment=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='GROUPS' for t in n.targets))
    groups=ast.literal_eval(assignment.value)
    labels={key:label for _,rows in groups for key,label in rows}
    source='/* Generated from app/access.py GROUPS; display metadata only. */\nwindow.AJPermissionLabels=(()=>{\n const labels=Object.freeze('+json.dumps(labels,ensure_ascii=False,indent=2)+');\n function label(key){const source=Object.hasOwn(labels,key)?labels[key]:String(key||\'\');return window.WavelinkI18n?.t(source)||source;}\n return Object.freeze({label});\n})();\n'
    (runtime/'app/static/permission_labels.js').write_text(source,encoding='utf8',newline='\n')
    print('Generated '+str(len(labels))+' existing permission labels')
if __name__=='__main__':generate(sys.argv[1])
