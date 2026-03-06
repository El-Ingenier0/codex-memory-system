# codex-memory-system

A flexible memory layer for Codex CLI focused on code development, with support for:
- multiple instances (different computers)
- multiple users
- scoped memory sharing (private/team/global)

## Core idea
Use **append-only events** as source-of-truth, then promote into curated memories.

This enables cross-user compounding without leaking private context.

## Files installed into your repo
- `CODEX_MEMORY.md` (local curated coding memory)
- `memory.config.json` (identity, scope ACLs, paths, promotion rules)
- `memory/YYYY-MM-DD.md` (daily log)
- `memory/session-state.md` (checkpoint snapshot)
- `memory/events.jsonl` (append-only scoped events)
- `.codex-memory/scripts/*` helpers

## Scope model
Each event has scope:
- `private:<userId>`
- `team:<teamId>`
- `global`

Reads/writes are controlled by `memory.config.json`:
- `scopes.allowedRead`
- `scopes.allowedWrite`

## Install
```bash
git clone https://github.com/El-Ingenier0/codex-memory-system.git
cd codex-memory-system
./scripts/bootstrap.sh /path/to/your/repo
```

Then edit `/path/to/your/repo/memory.config.json`:
- set `instance.instanceId`
- set `instance.userId`
- set team memberships + scope ACLs

## Run Codex with memory
```bash
cd /path/to/your/repo
./.codex-memory/scripts/codex_with_memory.sh "Implement X with tests"
```

Wrapper includes:
- `CODEX_MEMORY.md`
- recent learnings
- ACL-filtered scoped context (from events)

## Key scripts
- `events_append.py` — append scoped events
- `context_build.py` — build ACL-aware shared context block
- `promote_scoped.py` — promote scoped events to curated memory files
- `session_state_checkpoint.py` — write pre-compaction/session checkpoint
- `session_recover_tail.py` — bounded JSONL recovery
- `check_daily_next_actions.py` — enforce daily note hygiene

## Example: cross-user compounding
User A discovers a durable build fix, writes event to `team:platform` with evidence.
User B reads team-scoped context automatically via wrapper.
A promoter run materializes the fix into `memory/teams/platform/CODEX_MEMORY.md`.

## Flexibility-first notes
- schema allows custom fields (`extensions.customFieldsAllowed`)
- path layout is configurable under `paths`
- promotion policy is configurable under `promotion`

## License
MIT
