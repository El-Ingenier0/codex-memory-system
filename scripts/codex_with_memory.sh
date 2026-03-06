#!/usr/bin/env bash
set -euo pipefail

PROMPT="${1:-}"
if [[ -z "$PROMPT" ]]; then
  echo "Usage: $0 \"prompt\"" >&2
  exit 2
fi

ROOT="$(pwd)"
TODAY="$(date +%F)"
DAILY="$ROOT/memory/$TODAY.md"
MEMORY="$ROOT/CODEX_MEMORY.md"
LEARNINGS="$ROOT/memory/codex_learnings.md"
CFG="$ROOT/memory.config.json"

mkdir -p "$ROOT/memory"
[[ -f "$LEARNINGS" ]] || echo "# Codex Learnings (append-only)" > "$LEARNINGS"
[[ -f "$DAILY" ]] || cat > "$DAILY" <<EOF
# $TODAY

## Notes

## Next Actions
- [ ] None (log is complete for now)
EOF

CTX_FILE="$(mktemp)"
SCOPED_CTX=""
if [[ -f "$CFG" ]]; then
  SCOPED_CTX="$(python3 ./.codex-memory/scripts/context_build.py --root "$ROOT" --config "$CFG" 2>/dev/null || true)"
fi
{
  echo "### Curated memory";
  [[ -f "$MEMORY" ]] && tail -n 120 "$MEMORY" || echo "(missing CODEX_MEMORY.md)";
  echo;
  echo "### Recent learnings";
  tail -n 80 "$LEARNINGS";
  echo;
  [[ -n "$SCOPED_CTX" ]] && echo "$SCOPED_CTX";
  echo;
  echo "### Task";
  echo "$PROMPT";
  echo;
  echo "### Output requirements";
  echo "- Keep diff small and scoped.";
  echo "- Include verification commands and outcomes.";
  echo "- End with LEARNINGS: bullet list (or 'LEARNINGS: none').";
} > "$CTX_FILE"

OUT="$(codex exec "$(cat "$CTX_FILE")")"
echo "$OUT"

# Append LEARNINGS block to append-only learnings log
if echo "$OUT" | rg -q "LEARNINGS:"; then
  {
    echo;
    echo "## $(date -Is)";
    echo "$OUT" | sed -n '/LEARNINGS:/,$p';
  } >> "$LEARNINGS"
fi

{
  echo "- $(date '+%Y-%m-%d %H:%M %Z') — Codex task run via memory wrapper.";
} >> "$DAILY"

# Optional scoped event write (requires memory.config.json)
if [[ -f "$CFG" ]]; then
  SCOPE="$(python3 - <<'PY'
import json, pathlib
p=pathlib.Path('memory.config.json')
try:
 c=json.loads(p.read_text())
 print((c.get('scopes',{}).get('allowedWrite') or ['global'])[0])
except Exception:
 print('global')
PY
)"
  python3 ./.codex-memory/scripts/events_append.py --root "$ROOT" --config "$CFG" \
    --scope "$SCOPE" --type note --summary "Codex wrapper task executed" --project "$(basename "$ROOT")" >/dev/null 2>&1 || true
fi

rm -f "$CTX_FILE"
