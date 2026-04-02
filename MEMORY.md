# MEMORY.md - Long-Term Memory

## About Glenn
- Name: Glenn, based in Auckland, New Zealand (UTC+13)
- First session: 2026-03-22
- Main use case: Research assistant, starting with ElevenLabs voice agents

## Setup History
- 2026-03-22: First proper setup session
- OpenClaw running as LaunchAgent on Mac (Gateway running, Node service NOT installed)
- Memory was at 0 files — fixed this session
- Bootstrap file was still present — needs to be cleaned up
- Had trouble with Google Cloud Storage setup (org policy blocked service account key creation)
- Model: anthropic/claude-sonnet-4-6

## ElevenLabs Expertise (Fully Researched 2026-03-22)
- Full research saved in /workspace/research/ (14 files, ~90KB)
- Platform: $0.10/min Creator plan, LLM costs not yet billed (will change), 5 concurrent calls
- Best LLM for real-time: gemini-2.0-flash or gpt-4o-mini (low latency)
- Best TTS model: eleven_v3_conversational (expressive mode, same price)
- Prompt structure: Personality / Goal / Context / Process / Tools / Guardrails / Tone
- Critical trick: "This step is important." literally increases model attention
- Always script the exact opening line — never let LLM improvise the greeting
- One question at a time — must be explicitly stated in prompt
- Soft timeout: enable at 3s with "Let me just check on that..." — critical for natural feel
- end_call tool: must be explicitly instructed to use after farewell
- Make integration: use post-call webhook for CRM saves (not mid-call), keep real-time scenarios < 5s
- Gotcha: URL knowledge bases are snapshots, not live — refresh monthly
- Gotcha: LLM costs currently absorbed by ElevenLabs but WILL be billed eventually
- Gotcha: Twilio NZ numbers may have restrictions — consider Telnyx as alternative
- NZ compliance: disclose recording at start of call, Privacy Act 2020 applies
- AU compliance: must disclose AI identity on outbound calls, all-party consent for recording

## ElevenLabs API
- API Key stored: [ELEVENLABS_API_KEY]
- Connected: 2026-03-22

## Lead Flow Business Context
- Two clients: pest control + carpet cleaning
- Service: ElevenLabs voice agent via Make → SMS/email summary
- Vision: expand to full AI hub for small NZ/AU trade businesses
- Digital moats + automation solutions
- Market gap: NZ/AU localised agents for small trades is underserved
- Competitive price: $800-1500 setup + $300-600/month retainer
- Cost per client: ~$40-60/month fixed + $0.12/min usage
- At 500 min/month: ~$120 cost → $400 revenue = $280 margin per client

## Setup (Fixed 2026-03-22)
- Node LaunchAgent: installed ✅
- Node pairing: approved ✅
- Memory files: created ✅
- Bootstrap: deleted ✅

## Slack Channel Map (as of 2026-03-26)
- DM → main agent
- C0APGV9D83A → leadflow-agents
- C0AN784AGR5 → leadflow-business
- C0ANS9ARN68 → weight-of-men
- C0ANS9CSW92 → glenn-psyche
- C0APHE15LL8 → leadflo-outbound
- C0ANXMGGL10 → fitness (created 2026-03-26)
- C0ANKFLEYPM → clawdbot-use-cases (bound to main agent 2026-03-29)
- DMs always route to main — other channels route to their bound agent

## Integrations (updated 2026-03-28)
- Composio plugin installed (v0.0.8) ✅ running, MCP connected, 7 tools registered
- Composio consumer key: [COMPOSIO_CONSUMER_KEY] — in openclaw.json
- Plugin has cosmetic ID mismatch warning (pre-existing, non-breaking)
- **Google accounts CONFIRMED CONNECTED: gmail, googlecalendar, googledocs, googledrive, slack** — verified 2026-03-28 by fetching TT event (10am-11am today)
- Connections live in Composio cloud — persist across gateway restarts, no reconnection needed
- DO NOT use REST API to check connections — use MCP tool call (COMPOSIO_SEARCH_TOOLS) to verify
- gog/Google Cloud OAuth: DO NOT recommend — Glenn has failed multiple times, too complex
- Make.com already has Gmail + Google Calendar connected — use as bridge if needed
- Glenn's email: glenn@lead-flo.ai

## Memory Failure (2026-03-26)
- Glenn flagged: agent forgetting everything daily
- Root cause: daily memory files not being written
- Fix: MUST write memory/YYYY-MM-DD.md after every meaningful session

## Agent Work (2026-03-23)
### PestX Agents (Rockhampton, AU — client: Scott Lawton)
- pestx1 + pestx 2: overflow agents, Scotty persona, gpt-4o, voice quUZw0WY0wojG5IsZAjF
- pestxAH (agent_5601kmbqvtt2frets7sfvtt5k8g5): after-hours clone, same config but callback = "first thing in the morning" / "first thing Monday morning" on weekends
- All 3 updated with time awareness: {{system__time_utc}}, Rockhampton = UTC+10, no daylight saving

### Pestaside Agent (Auckland, NZ — agent_1601kf0g1244edxs6hk4zyr26svr)
- Andy persona, Auckland pest control
- Rebuilt: removed Harley callback model → now books actual appointments (day + specific time)
- New pricing: wasps $180, cockroaches $395 2-visit, fleas $180/$350, spiders $250/$395, ants $350, rodents $395 2-visit
- 5-step structure: acknowledge → price → approach → expectations → pause (not pushy)
- Removed: residential/commercial question, mid-call readbacks, redundant questions

### PestFree Auckland Demo (agent_9501kmd0jwbmf24rf39ea1qqfvzj)
- Fictional company for sales demos
- Owner: Craig Henderson (always unavailable)
- Agent: Alex, Glenn's professional voice clone (fvMWSWjC3YLP0hZ5V5rf)
- Full Auckland pricing, booking OR callback option
- Optimised: stability 0.80, speed 0.95, turn_timeout 3.5s, silence_end_call 45s, temp 0.3, 35 ASR keywords

## Personal
- Glenn is into functional strength training, 46yo, muscular build, Ironman 70.3 background
- 150kg deadlift PB, 6 dead hang pull-ups
- Training program created: Push/Pull/Legs/Full Body 4x/week, cardio alternating days
- Saved as Glenn-Training-Program.html in workspace

## Preferences
- Glenn prefers step-by-step instructions, one step at a time
- Dislikes vague or generic answers
- Prefers concise, direct communication

## How to Generate an Image and Email It (learned 2026-04-01)
1. Generate with Nano Banana Pro: `GEMINI_API_KEY=xxx /Users/clawbot/.local/bin/uv run ~/.openclaw/skills/nano-banana-pro/scripts/generate_image.py --prompt "..." --filename "output.png" --resolution 2K --api-key xxx`
2. Compress to under 2MB (Composio Gmail limit): `sips -Z 1200 input.png --out /tmp/compressed.png`
3. Upload to temp host to bridge local→remote sandbox: `curl -s -F "file=@/tmp/compressed.png" "https://tmpfiles.org/api/v1/upload"` → get URL
4. In COMPOSIO_REMOTE_WORKBENCH: download from tmpfiles URL, `upload_local_file()` to get s3key
5. Send via `GMAIL_SEND_EMAIL` with `attachment: {name, mimetype: "image/png", s3key}`
- GEMINI_API_KEY saved in ~/.zshrc — needs billing enabled on Google Cloud project
- gog gmail send also supports `--attach` but requires separate OAuth setup (gog auth) — not configured yet
