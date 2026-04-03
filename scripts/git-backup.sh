#!/bin/bash
cd /Users/clawbot/.openclaw/workspace
git add -A
# Only commit if there are changes
if ! git diff --cached --quiet; then
  git commit -m "Auto-backup $(date '+%Y-%m-%d %H:%M')"
  git push
fi
