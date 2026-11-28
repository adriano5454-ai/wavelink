"""UTC period boundaries and complete per-vessel stock-balance selection."""
import datetime
import pathlib
import runpy
import sqlite3
import sys
import types
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
overlay = runpy.run_path(str(ROOT/'deploy/vessel_reading_range_overlay.py'))


def load(name, source, deps):
    module = types.ModuleType('range_fixture.'+name)
    module.__package__ = 'range_fixture'
    package = types.ModuleType('range_fixture')
    with patch.dict(sys.modules, {'range_fixture': package, **{'range_fixture.'+key: value for key, value in deps.items()}}):
        exec(source, module.__dict__)
    return module


class Rejected(Exception):
    pass


class ReadingRanges(unittest.TestCase):
    def test_calendar_clamping_and_validation(self):
        mod = load('limits', (ROOT/'deploy/vessel_reading_range_model.py').read_bytes(),
                   {'store': types.SimpleNamespace(Problem=Rejected)})
        day = datetime.date(2024, 5, 31)
        self.assertEqual(mod.limits('3', today=day), ('2024-02-29','2024-05-31','2024-06-01'))
        self.assertEqual(mod.limits('12', today=day)[0], '2023-05-31')
        self.assertEqual(mod.limits('custom','2024-02-29','2024-02-29',today=day)[2], '2024-03-01')
        for args in [('bogus',), ('1','2024-01-01'), ('custom','2024-02-30','2024-03-01'),
                     ('custom','2024-01-01','2024-06-01'), ('custom','2020-01-01','2024-03-01'),
                     ('custom','2024-03-01','2024-02-29')]:
            with self.assertRaises(Rejected):
                mod.limits(*args,today=day)

    def test_all_selected_days_but_only_vessel_and_product(self):
        source = overlay['consumption']((ROOT/'deploy/consumption_model.py').read_text(encoding='utf8'))
        mod = load('consumption', source, {
            'fieldwork_common':types.SimpleNamespace(base=None,version=None),
            'fleet_tank_readings':types.SimpleNamespace(KINDS={'fresh_water','diesel'}),
            'fleet_consumption_access':types.SimpleNamespace(),
            'store':types.SimpleNamespace(Problem=Rejected),
        })
        with sqlite3.connect(':memory:') as db:
            db.row_factory=sqlite3.Row
            mod.ensure(db)
            day=datetime.date(2024,1,1)
            for i in range(45):
                stamp=(day+datetime.timedelta(days=i*2)).isoformat()
                for sid in ('a','b'):
                    db.execute('INSERT INTO fleet_consumption VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                               (f'{sid}{i}',sid,stamp,'fresh_water','m3',10,5,0,0,0,0,0,5,sid,stamp))
            rows=mod.daily(db,'a','2024-01-01','2024-03-29')
            self.assertEqual(len(rows['fresh_water']),45)
            self.assertEqual(sum(row['used'] for row in rows['fresh_water']),225)
            self.assertEqual(rows['fresh_water'][-1]['day'],'2024-01-01')
            self.assertEqual(rows['fresh_water'][0]['day'],'2024-03-29')
            self.assertEqual(rows['diesel'],[])
            self.assertEqual(mod.daily(db,'a','2024-01-02','2024-01-02')['fresh_water'],[])


if __name__ == '__main__':
    unittest.main()
