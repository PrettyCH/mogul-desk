#!/usr/bin/env bash
# Fetch AIHOT daily JSON into data/aihot-daily.json then rebuild the page.
# Usage: scripts/fetch-ai-daily.sh [YYYY-MM-DD]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATE="${1:-$(TZ=Asia/Shanghai date +%F)}"
UA="aihot-skill/2.0.0 (+https://aihot.news/aihot-skill/)"
ACTOR_FILE="/home/box/agent-data/workflows/aihot/.aihot-actor-id"
if [[ -f "$ACTOR_FILE" ]]; then
  ACTOR="$(tr -d '[:space:]' < "$ACTOR_FILE")"
  if [[ "$ACTOR" =~ ^[0-9a-fA-F-]{36}$ ]]; then
    UA="$UA aihot-actor/$ACTOR"
  fi
fi
URL="https://aihot.news/api/v1/dailies/$DATE"
TMP="$(mktemp)"
curl -fsSL -A "$UA" "$URL" -o "$TMP"
python3 - "$TMP" "$ROOT/data/aihot-daily.json" "$DATE" <<'PY'
import json, sys
from datetime import datetime, timezone, timedelta
src, dest, date = sys.argv[1], sys.argv[2], sys.argv[3]
raw = json.loads(open(src, encoding='utf-8').read())
# Drop top-level skill notice; keep report for rebuild
out = {
  "schemaVersion": raw.get("schemaVersion", 1),
  "fetchedAt": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
  "source": "https://aihot.news",
  "api": f"https://aihot.news/api/v1/dailies/{date}",
  "report": raw["report"] if "report" in raw else raw,
}
open(dest, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print("saved", dest, "date=", out["report"].get("date"))
PY
rm -f "$TMP"
python3 "$ROOT/scripts/build-ai-daily.py"
