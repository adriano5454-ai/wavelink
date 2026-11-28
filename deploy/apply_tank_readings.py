"""Add optional vessel reading starters without altering any existing logbook."""
from pathlib import Path
import runpy,sys
BASE=Path(__file__).resolve().parent
PARENT='46b798bb54cc22d3067846f289d9e82d9259bbc7d32ee571b29de0b2b2895e4a'
def once(s,a,b):
    if s.count(a)!=1:raise ValueError(a)
    return s.replace(a,b,1)
def schema(s):
    s=once(s,"QUICK_EVENTS=",'''TANK_READINGS = dict(id='vessel_tank_reading',name='Tank readings',fields=[
 field('tank','Tank name or ID',required=True),
 field('contents','Tank contents','select',required=True,choices=['Fresh water','Diesel / MGO','Fuel oil','Other fuel']),
 field('remaining','Measured remaining quantity','number',required=True),
 field('unit','Measurement unit','select',required=True,choices=['L','m3','kg','t']),
 field('method','Measurement method','select',required=True,choices=['Sounding','Gauge reading','Other manual measurement']),
 field('notes','Notes'),
])

QUICK_EVENTS=''')
    return once(s,"        out[f['id']]=v\n    return out",'''        out[f['id']]=v
    if section == TANK_READINGS:
        if float(out['remaining']) < 0:
            raise Problem(422,'Measured remaining quantity cannot be negative.')
        if out['contents']=='Fresh water' and out['unit'] not in ('L','m3'):
            raise Problem(422,'Use a volume unit for fresh water: L or m3.')
    return out''')
def browser(s):
    s=once(s,'BUILTINS, clean_text','BUILTINS, TANK_READINGS, clean_text')
    s=once(s,"    ('blank', 'Blank custom logbook', []),","    ('tank-readings','Tank readings',['vessel_tank_reading']),\n    ('blank', 'Blank custom logbook', []),")
    return once(s,'sections = copy.deepcopy(BUILTINS)','sections = copy.deepcopy([*BUILTINS,TANK_READINGS])')
def locale(s):
    anchor='  "Vessel operations":'
    j='''  "Tank readings": "Leituras de tanques",
  "Tank name or ID": "Nome ou código do tanque",
  "Tank contents": "Conteúdo do tanque",
  "Fresh water": "Água doce",
  "Diesel / MGO": "Diesel / MGO",
  "Fuel oil": "Óleo combustível",
  "Other fuel": "Outro combustível",
  "Measured remaining quantity": "Quantidade restante medida",
  "Measurement unit": "Unidade de medida",
  "Measurement method": "Método de medição",
  "Sounding": "Sondagem",
  "Gauge reading": "Leitura do indicador",
  "Other manual measurement": "Outra medição manual",
'''
    return once(s,anchor,j+anchor)
def transforms():
    return {'app/log_schema.py':schema,'app/browser_logs.py':browser,'app/static/locale_pt_br.js':locale}
if __name__=='__main__':
    runpy.run_path(str(BASE/'apply_editor_exit.py'))['apply'](
        Path(sys.argv[1]),parent=PARENT,overlays=(Path(__file__).name,),
        previous_cache='ui162-readiness',cache='ui162-tank-readings',suffix='tank-readings',
        scope='Optional manual freshwater and fuel tank readings using the existing permissioned logbook workflow.')
