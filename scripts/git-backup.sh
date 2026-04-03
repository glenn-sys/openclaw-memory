#!/bin/bash
cd /Users/clawbot/.openclaw/workspace

# Also backup openclaw.json config (strip sensitive tokens before committing)
python3 -c "
import json, re, sys

with open('/Users/clawbot/.openclaw/openclaw.json') as f:
    content = f.read()

# Scrub tokens/keys but keep structure
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
# Only commit if there are changes
if ! git diff --cached --quiet; then
  git commit -m "Auto-backup $(date '+%Y-%m-%d %H:%M')"
  git push
fi
