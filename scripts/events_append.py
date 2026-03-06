#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    ap = argparse.ArgumentParser(description="Append scoped memory event")
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="memory.config.json")
    ap.add_argument("--scope", required=True, help="private:<user>|team:<team>|global")
    ap.add_argument("--type", required=True, help="decision|learning|runbook|incident|note")
    ap.add_argument("--summary", required=True)
    ap.add_argument("--project", default="")
    ap.add_argument("--evidence", action="append", default=[])
    ap.add_argument("--tag", action="append", default=[])
    ap.add_argument("--field", action="append", default=[], help="extra key=value")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg = json.loads((root / args.config).read_text(encoding="utf-8"))
    allowed = set(cfg.get("scopes", {}).get("allowedWrite", []))
    if args.scope not in allowed:
        print(f"ERROR: scope not allowed for write: {args.scope}")
        return 2

    evt_path = root / cfg.get("paths", {}).get("events", "memory/events.jsonl")
    evt_path.parent.mkdir(parents=True, exist_ok=True)

    inst = cfg.get("instance", {})
    event = {
        "ts": now_iso(),
        "scope": args.scope,
        "type": args.type,
        "summary": args.summary,
        "project": args.project,
        "evidence": args.evidence,
        "tags": args.tag,
        "instanceId": inst.get("instanceId", "unknown"),
        "agentId": inst.get("agentId", "codex"),
        "userId": inst.get("userId", "unknown")
    }

    for kv in args.field:
        if "=" in kv:
            k, v = kv.split("=", 1)
            event[k] = v

    with evt_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(evt_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
