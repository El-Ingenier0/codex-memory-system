#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--file', required=True)
    ap.add_argument('--max-lines', type=int, default=400)
    ap.add_argument('--max-total-chars', type=int, default=40000)
    ap.add_argument('--max-line-chars', type=int, default=2000)
    a = ap.parse_args()

    p = Path(a.file)
    if not p.exists():
        print(json.dumps({'ok': False, 'error': f'missing file: {p}'}))
        return 2

    lines = p.read_text(encoding='utf-8', errors='replace').splitlines()[-a.max_lines:]
    out_rev=[]; used=0; trunc=0
    for ln in reversed(lines):
        s=ln
        if len(s) > a.max_line_chars:
            s = s[:a.max_line_chars] + ' [...TRUNCATED]'
            trunc += 1
        if used + len(s) + 1 > a.max_total_chars:
            break
        out_rev.append(s); used += len(s)+1

    out = list(reversed(out_rev))
    print(json.dumps({'ok': True, 'entryCount': len(out), 'truncatedCount': trunc, 'entries': out}, ensure_ascii=False))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
