# MEMORY.md - Long-Term Memory

## About Glenn
- Auckland, NZ (UTC+13) | email: glenn@lead-flo.ai | Discord: Mraeson089 (1438301281394364527)
- Preferences: step-by-step, concise, direct. No vague answers.
- Personal: 46yo, functional strength training, 150kg deadlift PB, 6 pull-ups, Ironman 70.3 background

## Lead-Flo Business
- Clients: pest control (PestX/Pestaside) + carpet cleaning
- Service: ElevenLabs voice agents via Make → SMS/email summary
- Pricing: $800-1500 setup + $300-600/month | Cost ~$40-60/month + $0.12/min usage
- Vision: AI hub for NZ/AU trade businesses (underserved market)

## ElevenLabs (researched 2026-03-22, files in /workspace/research/)
- Plan: $0.10/min Creator, 5 concurrent calls
- Best LLM: gemini-2.0-flash or gpt-4o-mini | Best TTS: eleven_v3_conversational
- Key rules: script opening line, one question at a time, soft timeout 3s, explicit end_call instruction
- Make: use post-call webhook (not mid-call) | URL knowledge bases are snapshots — refresh monthly
- NZ: disclose recording | AU: disclose AI identity on outbound, all-party consent recording

## Agent Work
### PestX (Rockhampton AU — Scott Lawton: scott.lawton@pestx.com.au | (07) 49362093)
- Jan Lawton (jan.lawton@pestx.com.au / jan.lawton001@gmail.com) — weekly reports
- Agents: pestx1/pestx2 (overflow, Scotty persona, gpt-4o, voice quUZw0WY0wojG5IsZAjF)
- pestxAH (agent_5601kmbqvtt2frets7sfvtt5k8g5): after-hours clone, UTC+10
- Reports: leadflow-pestx-report.netlify.app + leadflow-pestx-updates.netlify.app (NEVER auto-publish)
- Netlify token: nfp_XJ69L6H5wNVzpeygVVL9seCXLJDTihkSeaa9
- Netlify sites: updates=dad6626e-dfc8-4f0f-bdc3-51fbbc5acfe4, report=56e31501-8226-4c87-9678-7af5f645f19e
- Make scenarios: PestX Scotty (4365414), Webhooks (4010409), Webhooks+OpenAI+ServiceM8 (4048652)
- ServiceM8 integration in progress: post-call webhook → Make → find contact by phone → create job

### Pestaside (Auckland NZ — agent_1601kf0g1244edxs6hk4zyr26svr)
- Andy persona | Books appointments (day + time)
- Pricing: wasps $180, cockroaches $395 2-visit, fleas $180/$350, spiders $250/$395, ants $350, rodents $395 2-visit
- Style: acknowledge → price → approach → expectations → pause (not pushy)

### PestFree Auckland Demo (agent_9501kmd0jwbmf24rf39ea1qqfvzj)
- Alex persona, Glenn's voice clone (fvMWSWjC3YLP0hZ5V5rf)
- Settings: stability 0.80, speed 0.95, turn_timeout 3.5s, silence_end_call 45s

## Make.com
- Token: 1dafa2f8-36a0-466b-a1eb-7bc9954098da | us2.make.com | Org 5878007 | Team 1632137
- Pestaside scenario: 3937873

## Integrations
- Composio v0.0.8 ✅ | Connected: gmail, googlecalendar, googledocs, googledrive, slack
- Connections persist across gateway restarts — use COMPOSIO_SEARCH_TOOLS to verify (not REST API)
- DO NOT use gog/Google Cloud OAuth — Glenn has failed multiple times

## Channel → Agent Map
**Discord:** 1489546949982949490→main | 1490166576559951992→main | 1490191869890531500→marketing-opps | 1490547008853770442→pestx | 1490547070455517314→pestaside | 1490801706261282967→agent-builder | 1490913485155074189→psyche-research | 1490913540897505432→business-research
**Slack:** DM→main | C0APGV9D83A→leadflow-agents | C0AN784AGR5→leadflow-business | C0ANS9ARN68→weight-of-men | C0ANS9CSW92→glenn-psyche | C0APHE15LL8→leadflo-outbound | C0ANXMGGL10→fitness | C0ANKFLEYPM→clawdbot-use-cases

## Agent Models (updated 2026-04-08)
- main: Sonnet | pestx: Sonnet | agent-builder: Sonnet (default haiku, main overrides to sonnet)
- pestaside: Haiku | marketing-opps: Flash | psyche-research: Haiku | business-research: Haiku
- Haiku model ID: anthropic/claude-haiku-4-5 (NOT 3-5)
- Heartbeat: 55m (keeps 1h cache warm — cheaper than 30m or 2h)
- bootstrapMaxChars: 12000 (reduce context load)

## Generate Image → Email Workflow
1. `GEMINI_API_KEY=xxx uv run ~/.openclaw/skills/nano-banana-pro/scripts/generate_image.py --prompt "..." --resolution 2K`
2. `sips -Z 1200 input.png --out /tmp/compressed.png` (under 2MB)
3. Upload to tmpfiles.org → pass URL to COMPOSIO_REMOTE_WORKBENCH → upload_local_file() → s3key
4. `GMAIL_SEND_EMAIL` with `attachment: {name, mimetype: "image/png", s3key}`
- GEMINI_API_KEY in ~/.zshrc

## Cost Optimisation (2026-04-08)
- Weekly spend Apr 1-7: NZ$217/week — 95% was Sonnet cache writes/reads
- Changes made: cacheRetention→long for all models, heartbeat 30m→55m, bootstrapMaxChars 12000, trimmed MEMORY.md
- Expected savings: ~NZ$50-80/week from reduced cache writes + fewer heartbeat cycles
- Opus appearing in usage — investigate if fallback or accidental /model use
