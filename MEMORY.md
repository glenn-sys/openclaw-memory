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
- API Key stored: fa72b6c19e8672a3782bac5d5f6c0d01b1024300e6fd10d71124d429de05680f
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

## Preferences
- Glenn prefers step-by-step instructions, one step at a time
- Dislikes vague or generic answers
- Prefers concise, direct communication
