# OpenClaw Reconnect Guide
**For when the AI assistant is offline, confused, or not responding**
**Mac login: clawbot | Machine: Mike's MacBook Pro**

---

## 🟢 FASTEST FIX — Try This First (30 seconds)

Open **Terminal** on the Mac and run:

```
launchctl stop ai.openclaw.gateway && sleep 3 && launchctl start ai.openclaw.gateway
```

Then wait 15 seconds and try messaging on Slack again.

---

## 🔵 If That Didn't Work — Full Restart

```
launchctl stop ai.openclaw.gateway
launchctl stop ai.openclaw.node
sleep 5
launchctl start ai.openclaw.node
sleep 5
launchctl start ai.openclaw.gateway
```

Wait 20 seconds, then try Slack again.

---

## 🔴 If Still Not Working — Check Status

```
launchctl list | grep openclaw
```

You should see two entries: `ai.openclaw.gateway` and `ai.openclaw.node`
If either is missing, run its start command above.

Check the log for errors:
```
tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
```

---

## 🟡 Slack Not Responding But Gateway Running

The Slack socket may have dropped. Run:
```
launchctl stop ai.openclaw.gateway && sleep 5 && launchctl start ai.openclaw.gateway
```

If Slack still doesn't respond after 30s, check if a pairing approval is needed:
```
/Users/clawbot/.openclaw/tools/node-v22.22.0/bin/node /Users/clawbot/.openclaw/lib/node_modules/openclaw/dist/cli.js sessions list
```

---

## 🔁 If You Need to Re-pair Slack

Run this in Terminal:
```
/Users/clawbot/.openclaw/tools/node-v22.22.0/bin/node /Users/clawbot/.openclaw/lib/node_modules/openclaw/dist/cli.js pairing list
```

If there's a pending code, approve it:
```
/Users/clawbot/.openclaw/tools/node-v22.22.0/bin/node /Users/clawbot/.openclaw/lib/node_modules/openclaw/dist/cli.js pairing approve slack <CODE>
```

---

## ⚡ Model Got Changed and Now It's Broken?

Reset the model back to Sonnet (the safe default):

```bash
python3 -c "
import json
with open('/Users/clawbot/.openclaw/openclaw.json') as f:
    d = json.load(f)
d['agents']['defaults']['model']['primary'] = 'anthropic/claude-sonnet-4-6'
with open('/Users/clawbot/.openclaw/openclaw.json', 'w') as f:
    json.dump(d, f, indent=2)
print('Done - model reset to Sonnet')
"
```

Then restart the gateway (see top of this doc).

---

## 📋 Quick Reference

| Service | Start | Stop |
|---------|-------|------|
| Gateway | `launchctl start ai.openclaw.gateway` | `launchctl stop ai.openclaw.gateway` |
| Node | `launchctl start ai.openclaw.node` | `launchctl stop ai.openclaw.node` |

**Config file:** `/Users/clawbot/.openclaw/openclaw.json`
**Log file:** `/tmp/openclaw/openclaw-YYYY-MM-DD.log`
**Workspace:** `/Users/clawbot/.openclaw/workspace`

---

## 💬 What to Tell Claude.ai / Gemini If You Need Help

> "I'm running OpenClaw on a Mac. The gateway runs as a LaunchAgent called ai.openclaw.gateway. The node service is ai.openclaw.node. Config is at /Users/clawbot/.openclaw/openclaw.json. Help me restart it."

---

*Last updated: 2026-04-03*
