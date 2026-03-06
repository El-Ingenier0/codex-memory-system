#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description='Promote selected learnings into MEMORY.md')
    ap.add_argument('--root', default='.')
    ap.add_argument('--contains', action='append', default=[], help='keyword filter (repeatable)')
    ap.add_argument('--max-lines', type=int, default=20)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    learn = root / 'memory' / 'codex_learnings.md'
    mem = root / 'MEMORY.md'
    if not learn.exists() or not mem.exists():
        print('missing files')
        return 2

    lines = [ln.strip() for ln in learn.read_text(encoding='utf-8', errors='replace').splitlines() if ln.strip().startswith('-')]
    if args.contains:
        kws = [k.lower() for k in args.contains]
        lines = [ln for ln in lines if any(k in ln.lower() for k in kws)]
    lines = lines[-args.max_lines:]

    if not lines:
        print('no matches')
        return 0

    with mem.open('a', encoding='utf-8') as f:
        f.write('\n## Promoted learnings\n')
        for ln in lines:
            f.write(f"{ln}\n")
    print(f'promoted {len(lines)} lines')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
