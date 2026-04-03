#!/bin/bash
# OpenClaw backup script - runs hourly via OpenClaw cron

# 1. Run native openclaw backup to ~/Desktop/openclaw-backups/
BACKUP_DIR=~/Desktop/openclaw-backups
mkdir -p "$BACKUP_DIR"

# Keep only last 5 full backups
ls -t "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -n +6 | xargs rm -f 2>/dev/null

/Users/clawbot/.openclaw/tools/node-v22.22.0/bin/node \
  /Users/clawbot/.openclaw/lib/node_modules/openclaw/dist/entry.js \
  backup create --output "$BACKUP_DIR/" >> /tmp/openclaw-backup.log 2>&1

# 2. Git backup of workspace (memory, research, config snapshot)
cd /Users/clawbot/.openclaw/workspace

# Snapshot openclaw.json (scrubbed)
python3 -c "
import json, re
with open('/Users/clawbot/.openclaw/openclaw.json') as f:
    content = f.read()
d = json.loads(content)
def scrub(obj):
    if isinstance(obj, dict):
        return {k: ('REDACTED' if any(x in k.lower() for x in ['token','key','secret','pass']) else scrub(v)) for k,v in obj.items()}
    elif isinstance(obj, list):
        return [scrub(i) for i in obj]
    return obj
with open('/Users/clawbot/.openclaw/workspace/openclaw.json.backup', 'w') as f:
    json.dump(scrub(d), f, indent=2)
" 2>/dev/null

git add -A
if ! git diff --cached --quiet; then
  git commit -m "Auto-backup $(date '+%Y-%m-%d %H:%M')"
  git push
fi
