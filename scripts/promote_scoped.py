#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description="Promote scoped events into scoped curated memories")
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="memory.config.json")
    ap.add_argument("--policy", default="memory.policy.json")
    ap.add_argument("--scope", required=True, help="private:<user>|team:<team>|global")
    ap.add_argument("--max-items", type=int, default=50)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg = json.loads((root / args.config).read_text(encoding="utf-8"))
    policy = {}
    pol_path = root / args.policy
    if pol_path.exists():
        policy = json.loads(pol_path.read_text(encoding="utf-8"))
    p = cfg.get("paths", {})
    events = root / p.get("events", "memory/events.jsonl")
    if not events.exists():
        print("no events")
        return 0

    def policy_for_scope(scope: str) -> dict:
        if scope == "global":
            return policy.get("global", {}).get("promotion", {})
        if scope.startswith("team:"):
            team = scope.split(":", 1)[1]
            teams = policy.get("teams", {})
            return teams.get(team, teams.get("default", {})).get("promotion", {})
        return {}

    pol = policy_for_scope(args.scope)
    req_evidence = bool(pol.get("requireEvidence", False))
    req_confirmer = bool(pol.get("requireConfirmer", False))

    lines = events.read_text(encoding="utf-8", errors="replace").splitlines()
    selected = []
    for ln in reversed(lines):
        try:
            e = json.loads(ln)
        except Exception:
            continue
        if e.get("scope") != args.scope:
            continue
        if not pol and args.scope == "global" and cfg.get("promotion", {}).get("toGlobalRequiresEvidence", True):
            req_evidence = True

        if req_evidence and not e.get("evidence"):
            continue
        if req_confirmer and not e.get("confirmer"):
            continue
        selected.append(e)
        if len(selected) >= args.max_items:
            break
    selected.reverse()

    if args.scope == "global":
        dest = root / p.get("globalMemory", "memory/global/CODEX_MEMORY.md")
    elif args.scope.startswith("team:"):
        team = args.scope.split(":", 1)[1]
        dest = root / p.get("teamRoot", "memory/teams") / team / "CODEX_MEMORY.md"
    elif args.scope.startswith("private:"):
        user = args.scope.split(":", 1)[1]
        dest = root / p.get("userRoot", "memory/users") / user / "CODEX_MEMORY.md"
    else:
        print("invalid scope")
        return 2

    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        dest.write_text(f"# Scoped Memory ({args.scope})\n\n", encoding="utf-8")

    with dest.open("a", encoding="utf-8") as f:
        f.write("\n## Promoted events\n")
        for e in selected:
            conf = e.get('confirmer', '')
            suffix = f" (confirmer={conf})" if conf else ""
            f.write(f"- {e.get('ts','')} {e.get('type','')} {e.get('project','')} :: {e.get('summary','')}{suffix}\n")

    print(f"promoted {len(selected)} -> {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
