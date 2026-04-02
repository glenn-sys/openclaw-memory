# OpenClaw Reconnect

Open Terminal on the Mac and run:

```
launchctl stop ai.openclaw.gateway && sleep 5 && launchctl start ai.openclaw.gateway
```

Wait 20 seconds. Try Slack again. That's it 99% of the time.

---

**If that doesn't work:**

```
launchctl stop ai.openclaw.gateway
launchctl stop ai.openclaw.node
sleep 5
launchctl start ai.openclaw.node
sleep 5
launchctl start ai.openclaw.gateway
```

---

**If you need to ask Claude.ai or Gemini for help:**

> "I run OpenClaw on a Mac. Gateway LaunchAgent: ai.openclaw.gateway. Node: ai.openclaw.node. Config: /Users/clawbot/.openclaw/openclaw.json. Help me restart it."
