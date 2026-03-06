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
MEMORY="$ROOT/MEMORY.md"
LEARNINGS="$ROOT/memory/codex_learnings.md"

mkdir -p "$ROOT/memory"
[[ -f "$LEARNINGS" ]] || echo "# Codex Learnings (append-only)" > "$LEARNINGS"
[[ -f "$DAILY" ]] || cat > "$DAILY" <<EOF
# $TODAY

## Notes

## Next Actions
- [ ] None (log is complete for now)
EOF

CTX_FILE="$(mktemp)"
{
  echo "### Curated memory";
  [[ -f "$MEMORY" ]] && tail -n 120 "$MEMORY" || echo "(missing MEMORY.md)";
  echo;
  echo "### Recent learnings";
  tail -n 80 "$LEARNINGS";
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

rm -f "$CTX_FILE"
