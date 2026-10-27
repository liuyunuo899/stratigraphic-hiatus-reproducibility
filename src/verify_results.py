"""Check reproducibility of numeric output files; this does not validate scientific assumptions."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
from project_guard import verify_project_inputs
verify_project_inputs()
checks = []

def check(label, value, expected, tol=0):
    passed = abs(value-expected) <= tol
    checks.append(passed)
    print(f"{'PASS' if passed else 'FAIL'}  {label}: observed={value}, expected={expected}, tol={tol}")

proc = ROOT / 'data' / 'processed'
syn = ROOT / 'data' / 'synthetic'
check('column count', len(pd.read_csv(proc/'columns_summary.csv')), 948)
check('hiatus count', len(pd.read_csv(proc/'hiatuses.csv')), 6281)
check('Sadler pairs', len(pd.read_csv(proc/'sadler_pairs.csv')), 683120)
fits = pd.read_csv(proc/'hiatus_powerlaw_fits.csv').set_index('setting')
for setting, expected in [('Appalachian orogen',1.434468), ('Cordilleran & Alaska orogen',1.821525),('Cratonic platform',5.272),('Foreland (Rocky Mtn.)',1.547),('Passive margin & coastal plain',1.607),('Shield & Arctic',2.792)]:
    check(f'alpha: {setting}', fits.loc[setting,'alpha'], expected, 0.005)
r = pd.read_csv(syn/'ensemble_runs.csv')
check('ensemble runs',len(r),600)
for setting,expected in [('F1',0.017),('F2',0.089),('F3',0.386)]:
    check(f'P median {setting}',r.loc[r.kind==setting,'P'].median(),expected,0.001)
inv = pd.read_csv(syn/'inversion_ensemble.csv')
check('inversion Monte Carlo runs',len(inv),5000)
check('inversion M_gross median',inv.M_gross.median(),104.8,0.1)
check('inversion P median',inv.P.median(),0.718,0.001)
if not all(checks):
    raise SystemExit('Mismatch: inspect files/parameters for differences.')
print('All numeric-output checks passed; scientific model validity is a separate question.')
