# codex-memory-system

A drop-in long-term learning framework for **Codex CLI**.

This ports the same architecture we use in OpenClaw:
- curated memory + daily logs
- pre-compaction/session checkpointing
- regressions/friction/predictions loops
- bounded JSONL tail recovery
- lightweight prompt-eval scaffolding

## What you get

- `templates/` baseline files (`AGENTS.md`, `SOUL.md`, `MEMORY.md`, `TOOLS.md`, `SECURITY.md`)
- `scripts/session_state_checkpoint.py` (writes `memory/session-state.md`)
- `scripts/session_recover_tail.py` (bounded JSONL recovery)
- `scripts/check_daily_next_actions.py` (enforces `## Next Actions`)
- `scripts/codex_with_memory.sh` (wrap Codex with memory context)
- `scripts/promote_learnings.py` (promote durable lessons into curated memory)

## Quick start

```bash
git clone https://github.com/El-Ingenier0/codex-memory-system.git
cd codex-memory-system
./scripts/bootstrap.sh /path/to/your/repo
```

Then run Codex through the wrapper:

```bash
cd /path/to/your/repo
./.codex-memory/scripts/codex_with_memory.sh "Implement X and include LEARNINGS section"
```

## Memory model

Inside your target repo:

- `memory/YYYY-MM-DD.md` → daily operational log
- `memory/session-state.md` → overwrite snapshot for continuity
- `MEMORY.md` → curated long-term memory
- `FRICTION.md` → instruction conflicts
- `PREDICTIONS.md` → calibration log
- `.codex-memory/state.json` → tool state

## Guardrails

- Never claim completion from proxy signals alone.
- Log durable changes immediately.
- Add `## Next Actions` to daily notes.
- If uncertain, explicitly say confidence + what remains unknown.

## License

MIT
