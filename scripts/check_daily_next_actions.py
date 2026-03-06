#!/usr/bin/env python3
from __future__ import annotations
import argparse, re
from datetime import datetime
from pathlib import Path

RE = re.compile(r'(?mi)^##\s+Next\s+Actions\s*$')

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--date')
    ap.add_argument('--file')
    a = ap.parse_args()

    root = Path(a.root).resolve()
    target = Path(a.file).resolve() if a.file else (root / 'memory' / f"{a.date or datetime.now().strftime('%Y-%m-%d')}.md")
    if not target.exists():
        print(f'ERROR: missing daily note: {target}')
        return 2
    txt = target.read_text(encoding='utf-8')
    if RE.search(txt):
        print('OK')
        return 0
    print(f"ERROR: {target} missing '## Next Actions'")
    return 2

if __name__ == '__main__':
    raise SystemExit(main())
