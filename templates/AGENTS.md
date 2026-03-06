# AGENTS.md

## Startup
1. Read `SOUL.md`
2. Read `TOOLS.md`
3. Read today + yesterday `memory/YYYY-MM-DD.md`
4. Read `MEMORY.md`

## Long-term learning loops

### Durable logging
- After every durable change, append bullets to `memory/YYYY-MM-DD.md`.
- Every daily note must end with `## Next Actions`.

### Pre-compaction checkpoint (mandatory)
Before compaction/session end:
- Overwrite `memory/session-state.md`
- Append one checkpoint bullet to today’s daily note.

`memory/session-state.md` must include:
1) active task/waiting reason
2) last 3-5 exchanges
3) pending proposals/questions
4) decisions in flight
5) conversational tone
6) brief timeline
7) files/resources in play

### Recovery ladder
1. `memory/session-state.md`
2. latest `memory/YYYY-MM-DD.md`
3. JSONL tail recovery via `.codex-memory/scripts/session_recover_tail.py`

### Regression policy
- Convert meaningful failures into explicit “don’t repeat” rules in `MEMORY.md`.

### Friction policy
- Log instruction conflicts in `FRICTION.md` with source files + resolution.

### Prediction calibration
- Log predictions + outcomes in `PREDICTIONS.md`.
