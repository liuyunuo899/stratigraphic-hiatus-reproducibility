"""Losslessly recover the exact original Sadler-pair table from gzip.

The scientific data are never edited. Existing files are preserved if valid
and rejected if their SHA-256 differs from the archived original.
"""
from pathlib import Path
import hashlib
import gzip
import shutil

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / 'data' / 'processed' / 'sadler_pairs.csv.gz'
CSV = ROOT / 'data' / 'processed' / 'sadler_pairs.csv'
EXPECTED = '20c83d9d720a4f65a1685beff0c957b8020398b5777c2d262287bc385a8a7da6'

def checksum(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    if CSV.exists():
        if checksum(CSV) != EXPECTED:
            raise SystemExit('Existing sadler_pairs.csv differs from the original: not overwriting.')
        print('Already restored and verified:', CSV)
        return
    if not ZIP.is_file():
        raise FileNotFoundError(ZIP)
    temp = CSV.with_suffix('.restore_tmp')
    try:
        with gzip.open(ZIP, 'rb') as inp, temp.open('wb') as out:
            shutil.copyfileobj(inp, out)
        if checksum(temp) != EXPECTED:
            raise RuntimeError('Restored bytes failed SHA-256 verification.')
        temp.replace(CSV)
    finally:
        if temp.exists():
            temp.unlink()
    print('Restored and SHA-256 verified:', CSV)

if __name__ == '__main__':
    main()
