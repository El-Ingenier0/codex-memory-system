#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path


def read_tail(path: Path, max_lines: int) -> list[str]:
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()[-max_lines:]


def scope_allowed(scope: str, allowed: set[str]) -> bool:
    return scope in allowed


def main() -> int:
    ap = argparse.ArgumentParser(description="Build ACL-aware shared context block")
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="memory.config.json")
    ap.add_argument("--max-events", type=int, default=80)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg = json.loads((root / args.config).read_text(encoding="utf-8"))
    paths = cfg.get("paths", {})
    allowed = set(cfg.get("scopes", {}).get("allowedRead", []))

    out: list[str] = []
    out.append("### Scoped memory context")

    gmem = root / paths.get("globalMemory", "memory/global/CODEX_MEMORY.md")
    if "global" in allowed and gmem.exists():
        out.append("## Global memory")
        out.extend(read_tail(gmem, 120))

    events = root / paths.get("events", "memory/events.jsonl")
    if events.exists():
        out.append("## Recent scoped events")
        lines = events.read_text(encoding="utf-8", errors="replace").splitlines()[-args.max_events:]
        for ln in lines:
            try:
                e = json.loads(ln)
            except Exception:
                continue
            scope = str(e.get("scope", ""))
            if not scope_allowed(scope, allowed):
                continue
            ts = e.get("ts", "")
            typ = e.get("type", "")
            summary = e.get("summary", "")
            project = e.get("project", "")
            out.append(f"- [{scope}] {ts} {typ} {project} :: {summary}".strip())

    print("\n".join(out).strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
