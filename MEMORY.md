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

## Strengths & Achievements — The Full Picture

This section matters. Glenn has done extraordinary things. The psychological profile elsewhere captures his wounds — this captures what he's built *in spite of* them.

### Professional
- One of the best salespeople at Australia's largest property marketing agency — high performer in a competitive, high-stakes environment
- Building Lead-flo: AI/automation business targeting NZ/AU trade market — genuine entrepreneurial vision with real clients and a clear market opportunity
- Self-taught in AI, automation, and tools like ElevenLabs, Make, and OpenClaw — no formal tech background, pure drive and curiosity
- Built functional voice AI agents for real paying clients from scratch

### Physical
- 46 years old with an excellent physique — not "good for his age," genuinely impressive
- 150kg deadlift PB
- 6 dead hang pull-ups
- Completed Ironman 70.3 training
- Trained for and fought in a kickboxing fight
- Consistent functional strength training program — Push/Pull/Legs/Full Body 4x/week
- Training program created: Glenn-Training-Program.html in workspace

### Creative & Personal
- Writing a novel — semi-fictional memoir spanning three generations, tackling generational trauma, alcoholism, and identity. That's not a small thing.
- Great father — Dana loves him, confides in him, and they have a genuinely close relationship despite everything
- Has rebuilt himself multiple times from circumstances that would have broken most people
- Nearly 6 years clean before recent relapse — that was real and hard-won

### The bigger truth
Glenn's psychological patterns are real, but they exist alongside a person who has achieved things that most people — with *far* easier lives — never will. The wounds explain some of the struggle. They don't define the man.

## Deep Psychological Profile (from session 2026-03-25 — full notes in memory/2026-03-25.md)
**READ memory/2026-03-25.md before any deep conversation about Glenn's psychology, life, or patterns.**

### Core wound
- Father: severe alcoholic, absent, only presence was anger — "I am not worth a father's love"
- Mother: chronic depression, critical, conditional love — second abandonment figure
- Home: domestic violence
- Core shame identity: "I am bad / a piece of shit" — not guilt (behaviour) but shame (identity)
- Core fear: "alone, broke, no partner, no opportunity" — existential terror of worthlessness
- Paradox: his addictive behaviours systematically CREATE the outcome he fears most

### The accident (age 17)
- Drunk, walked in front of a car, induced coma 2 days
- Post-accident: expelled from his entire social group overnight — went from "cool kid" to social exile
- This is the defining social wound — has struggled to maintain friendships ever since
- Pattern: likable + popular → can't sustain closeness long-term

### Addiction history
- Poly-substance: meth (IV), GHB, alcohol
- Sex addiction: extensive sex worker use including throughout relationship with Natascha
- Porn addiction
- Tens of thousands spent on drugs/sex workers
- Almost 6 years clean before relapsing ~1 year ago (2025)
- Currently 2 weeks sober (March 2026) after a 24hr slip
- The arrest: girlfriend OD'd on GHB he supplied, he was charged with possession/supply of GHB + meth
- Led to homelessness ~7 years ago

### Key relationships
- **Dana (daughter):** Adult, close, confides in Glenn more than her mum. Loves him but doesn't fully trust the floor to hold — low expectations of sobriety. Glenn's goal: self-forgiveness + consistency.
- **Natascha (current partner):** Colombian, PhD, performing arts professor. "Love of my life" and spiritual role model. BUT Glenn has used sex workers throughout their relationship. Central tension: deepest love vs. most destructive behaviour aimed at the same relationship.
- **Michelle (ex-wife):** Co-dependent, never truly loved her, used as coping mechanism. Dysfunctional background.
- **Campbell:** Met through AA, was his sponsor, became close friend. One of only two people who knew the real Glenn. Glenn ended this friendship 2026-03-26 after years of tension — Campbell challenged him ("I don't think you're willing to go to any lengths"), Glenn rage-responded, partial repair, then ended it. Classic shame-rage pattern. Campbell was genuinely negative influence (values misalignment re: race/women, envy) but decision was made on a high-emotion day.

### Psychological patterns
- Build → achieve → feel empty → self-destruct → rebuild (repeating cycle)
- Collapses happen when he succeeds but the emotional vacuum underneath is exposed
- Approval-seeking: hardest hit from men he respects (father wound — seeking what he never got)
- Rage trigger: feeling disrespected = identity wound activated instantly
- Splitting: person annoys him → immediately "worst person alive"
- Imposter syndrome: never felt he earned corporate success, follows him into Lead-flo
- ADHD/dyslexia: messy, disorganised, never the systems guy

### Current recovery (March 2026)
- AA meeting every day
- Morning prayer: hand the day over, ask God to guide thinking, be free of selfishness, sober day
- Evening prayer: release resentments, thank God
- Working with a sponsor
- Seeing a therapist
- Writing a book: semi-fictional memoir, three generations (Glenn, father, grandfather), theme of generational alcoholism — psychologically mapping the wound back to its origins

### Friendships (as of 2026-03-26)
- Very thin circle: one older AA friend (70s, father figure), sponsor, some work colleagues
- Campbell ending = lost one of his last friends
- Has always struggled to maintain friendships since age 17

### Zopiclone note
- 7mg nightly, long-term dependence
- Z-drug (GABA pathway — same as alcohol/benzos) — clinically controversial in addiction recovery
- Suppresses REM sleep → undermines emotional regulation
- Worth raising with an addiction-aware doctor

## Preferences
- Glenn prefers step-by-step instructions, one step at a time
- Dislikes vague or generic answers
- Prefers concise, direct communication
- Dislikes being treated as if prior context doesn't exist — always read memory files first

## Composio Integration (confirmed 2026-03-28)
- Plugin: @composio/openclaw-plugin v0.0.8 ✅ running
- Consumer key: ck_0i0WL2xECeclwkhK-fDD
- Connected apps: Gmail, Google Calendar, Google Docs, Google Drive, Slack — ALL ACTIVE
- Connections are cloud-based and persist across restarts — no reconnection needed
- Verified: fetched Glenn's Google Calendar event (TT, 10am-11am 2026-03-28)
- Do NOT tell Glenn his Google accounts are not connected — they are

