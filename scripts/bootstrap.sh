#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  echo "Usage: $0 /path/to/target-repo" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$TARGET/memory" "$TARGET/.codex-memory/scripts"

[[ -f "$TARGET/CODEX_MEMORY.md" ]] || cp "$ROOT/templates/CODEX_MEMORY.md" "$TARGET/CODEX_MEMORY.md"
[[ -f "$TARGET/memory.config.json" ]] || cp "$ROOT/templates/memory.config.json" "$TARGET/memory.config.json"
[[ -f "$TARGET/memory.policy.json" ]] || cp "$ROOT/templates/memory.policy.json" "$TARGET/memory.policy.json"
cp "$ROOT/scripts/session_state_checkpoint.py" "$TARGET/.codex-memory/scripts/"
cp "$ROOT/scripts/check_daily_next_actions.py" "$TARGET/.codex-memory/scripts/"
cp "$ROOT/scripts/session_recover_tail.py" "$TARGET/.codex-memory/scripts/"
cp "$ROOT/scripts/events_append.py" "$TARGET/.codex-memory/scripts/"
cp "$ROOT/scripts/context_build.py" "$TARGET/.codex-memory/scripts/"
cp "$ROOT/scripts/promote_scoped.py" "$TARGET/.codex-memory/scripts/"
cp "$ROOT/scripts/codex_with_memory.sh" "$TARGET/.codex-memory/scripts/"
chmod +x "$TARGET/.codex-memory/scripts/"*.py "$TARGET/.codex-memory/scripts/"*.sh

TODAY="$(date +%F)"
if [[ ! -f "$TARGET/memory/$TODAY.md" ]]; then
  cat > "$TARGET/memory/$TODAY.md" <<EOF
# $TODAY

## Notes

## Next Actions
- [ ] None (log is complete for now)
EOF
fi

echo "Bootstrapped codex-memory-system into $TARGET"
