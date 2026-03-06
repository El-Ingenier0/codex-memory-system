#!/usr/bin/env python3
from __future__ import annotations
import argparse
from datetime import datetime
from pathlib import Path

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--active-task', required=True)
    ap.add_argument('--exchange', action='append', default=[])
    ap.add_argument('--pending', action='append', default=[])
    ap.add_argument('--decision', action='append', default=[])
    ap.add_argument('--tone', action='append', default=[])
    ap.add_argument('--timeline', action='append', default=[])
    ap.add_argument('--resource', action='append', default=[])
    args = ap.parse_args()

    root = Path(args.root).resolve()
    p = root / 'memory' / 'session-state.md'
    p.parent.mkdir(parents=True, exist_ok=True)

    def sec(title, xs):
      out=[f'## {title}']
      out += [f'- {x}' for x in xs] if xs else ['- ']
      return '\n'.join(out)

    text='\n\n'.join([
      '# session-state.md',
      f'Last updated: {datetime.now().isoformat(timespec="minutes")}',
      sec('Active Task', [args.active_task]),
      sec('Last 3–5 Exchanges (Paraphrased)', args.exchange),
      sec('Pending Proposals / Questions', args.pending),
      sec('Decisions In Flight', args.decision),
      sec('Conversational Tone / Context', args.tone),
      sec('Session Timeline (brief)', args.timeline),
      sec('Files / Resources In Play', args.resource),
    ]) + '\n'
    p.write_text(text, encoding='utf-8')
    print(p)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
