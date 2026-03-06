# codex-memory-system

A **simple memory layer for Codex CLI focused on code development**.

## Design goals
- Minimal setup
- Better coding continuity across long sessions
- Fast capture of durable engineering lessons

## What this gives you
- `CODEX_MEMORY.md` (curated coding memory)
- `memory/YYYY-MM-DD.md` (daily dev log)
- `memory/session-state.md` (current checkpoint)
- `.codex-memory/scripts/codex_with_memory.sh` (run Codex with memory context)
- `.codex-memory/scripts/check_daily_next_actions.py` (daily log hygiene)
- `.codex-memory/scripts/session_state_checkpoint.py` (quick checkpoint writer)

## Install into a repo

```bash
git clone https://github.com/El-Ingenier0/codex-memory-system.git
cd codex-memory-system
./scripts/bootstrap.sh /path/to/your/repo
```

## Use it during coding

```bash
cd /path/to/your/repo
./.codex-memory/scripts/codex_with_memory.sh "Implement feature X with tests"
```

The wrapper prepends:
- `CODEX_MEMORY.md`
- today’s daily note tail
- recent learnings tail

and asks Codex to end with `LEARNINGS:` bullets. Those bullets are appended to `memory/codex_learnings.md`.

## Recommended workflow
1. Run task through wrapper
2. Verify tests/build
3. Append durable note to daily file
4. Keep `## Next Actions` updated
5. Update `CODEX_MEMORY.md` when a learning repeats

## Keep it simple
This repo intentionally avoids heavy orchestration. It is a lightweight coding memory scaffold, not an agent platform.

## License
MIT
