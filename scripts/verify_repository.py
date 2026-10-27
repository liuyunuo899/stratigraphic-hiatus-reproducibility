"""Validate tracked GitHub repository files using the generated SHA-256 list.

Does not execute the scientific simulations or alter outputs.
Can run before restoring the large processed Sadler CSV.
"""
from pathlib import Path
import csv
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'FILE_SHA256.csv'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as inp:
        for b in iter(lambda: inp.read(1048576), b''):
            h.update(b)
    return h.hexdigest()

def main():
    fail = []
    total = 0
    with MANIFEST.open(newline='', encoding='utf-8') as inp:
        for row in csv.DictReader(inp):
            total += 1
            rel = row['path']
            path = ROOT / rel
            if not path.is_file() or digest(path) != row['sha256']:
                fail.append(rel)
    print(f'SHA-256 checked: {total}; passed: {total-len(fail)}; failed: {len(fail)}')
    for f in fail:
        print('FAIL:', f)
    if fail:
        raise SystemExit(1)
    print('All tracked files match the archived manifest.')

if __name__ == '__main__':
    main()
