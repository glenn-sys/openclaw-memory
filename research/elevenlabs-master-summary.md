# ElevenLabs Conversational AI — Master Summary

*Comprehensive reference for building voice agents for trade businesses (pest control, carpet cleaning)*
*Research date: March 2026*

---

## What ElevenLabs Conversational AI Is

A complete platform for building AI-powered phone/voice/chat agents. You get:
- **Voice**: 5,000+ voices, 70+ languages, sub-100ms latency
- **Brains**: Any LLM (GPT-4, Claude, Gemini, or custom)
- **Knowledge**: Upload docs, URLs, or text as a knowledge base
- **Actions**: Call webhooks/APIs mid-conversation (book appointments, save leads, etc.)
- **Phone**: Native Twilio integration or SIP trunking for inbound/outbound calls

**For a trade business**: this means 24/7 AI receptionist that answers calls, qualifies leads, captures job details, and fires off automations — all while sounding like a real person.

---

## How It Works (Technical Architecture)

```
Caller speaks → ASR converts to text → LLM generates response (+ RAG lookups)
→ TTS speaks response → Turn-taking model decides when to respond → Repeat
```

Four components:
1. **Speech-to-Text (ASR)** — fine-tuned model, very accurate
2. **LLM** — your choice; Claude/GPT-4 recommended for complex conversations
3. **Text-to-Speech** — ElevenLabs' proprietary, highest quality available
4. **Turn-taking model** — understands "um", "ah", knows when user is done speaking

---

## Platform Pricing (March 2026)

| What | Cost |
|------|------|
| Conversational AI calls | **$0.10/min** (Starter/Creator/Pro), **$0.08/min** (Business annual) |
| LLM costs | Currently absorbed by ElevenLabs (may change) |
| Twilio phone number | ~$1.15/month (extra) |
| Twilio inbound calls | ~$0.0085/min (extra, US rates) |
| Agents you can create | Unlimited on all plans |
| Concurrent calls (Creator plan) | 5 |
| Creator plan price | $22/month ($11 first month) |

**For a small trade business**: Creator plan ($22/month) = 5 concurrent calls, plenty for most scenarios. ~$0.10/min × average 3-min call = $0.30/call.

---

## Setting Up an Agent — Quick Overview

### 1. Create Agent
Dashboard → Agents → Create New → Name your agent

### 2. Configure Core Settings
- **System prompt** — personality, goal, process, guardrails
- **First message** — exact words the agent says when call connects
- **Voice** — choose from 5,000+ voices
- **LLM** — recommend Claude 3 Haiku (fast + affordable) or GPT-4o-mini
- **Language** — or enable auto-detection

### 3. Add Knowledge Base
Upload your services, pricing, FAQ, service areas as text files

### 4. Configure Tools
Add webhooks for: save lead, check availability, etc.

### 5. Connect Phone Number
Link a Twilio number → ElevenLabs auto-configures

### 6. Test & Refine
Use ElevenLabs built-in test widget → review transcripts → adjust prompt

---

## System Prompt Template (Trade Business)

```markdown
# Personality
You are [Name], a friendly receptionist for [Business Name] in [City].
You are warm, efficient, and knowledgeable.

# Goal
Answer calls, handle enquiries, and collect details for bookings or quotes.

# Context
[Business] provides [services] in [service areas].
Hours: [hours]. Pricing starts from [prices].

# Process
1. Answer: "[Business Name], this is [Name], how can I help?"
2. Listen to the caller's need.
3. Collect (one question at a time): name, address/suburb, service needed, 
   preferred time, phone number.
4. Confirm all details back to caller. This step is important.
5. Explain next steps clearly.
6. Close warmly and use end_call.

# Tools
## save_enquiry
Use ONLY after confirming ALL details with caller.
Required: name, phone, service_needed
Optional: address, preferred_time, notes

# Guardrails
Ask ONE question at a time. This step is important.
Do not quote exact prices — say "our team will confirm when they call."
Do not confirm bookings — only "someone will be in touch to confirm."
If you don't know something, say so and offer to pass a message.
Never discuss competitors.

# Tone
Warm, friendly, concise. Natural spoken language. No corporate jargon.
```

---

## Knowledge Base Setup

**What to upload** (as separate text files):
- Services & Pricing (detailed)
- Service Areas (list of suburbs)
- FAQ (common questions + answers)
- What to Expect (process description)

**Rules**:
- Keep each file focused on one topic
- Write in plain language (agent mirrors your writing style)
- Update monthly (URL imports are snapshots, not live)
- Enable RAG for large documents (500+ tokens)
- Small docs (< 3,000 tokens): inject directly, no RAG needed

**Limits**:
- Creator plan: 20 MB for RAG documents
- Non-enterprise: 20 MB total / 300k characters

---

## Tools & Webhooks (The Action Layer)

### Three patterns:

**1. Mid-call tool (real-time)**
Agent calls your webhook, waits for response, uses it in conversation.
- Use for: availability checking, customer lookup
- Keep response time < 5 seconds

**2. Lead capture tool (end of call)**
Agent collects info → calls your webhook → saves data
- Use for: saving leads, creating records
- Most common pattern for trade businesses

**3. Post-call webhook (automatic)**
ElevenLabs sends full call data after call ends.
- Use for: transcript processing, complex CRM updates, analytics
- No time pressure — can run complex workflows

---

## Make Integration (The Automation Layer)

Make connects ElevenLabs to the rest of your business:

**Minimal viable setup** (start here):
```
ElevenLabs agent → calls save_lead webhook → Make scenario:
  1. Add row to Google Sheets (lead log)
  2. Send SMS to caller (confirmation)
  3. Send email to owner (notification)
  4. Return 200 OK to ElevenLabs
```

Total setup time: ~30 minutes. Genuinely useful from Day 1.

**Advanced patterns**:
- Post-call → Parse transcript → Create HubSpot contact → Send follow-up SMS
- Real-time availability check → Google Calendar lookup → Return available slots
- Batch outbound calls → Make triggers → ElevenLabs initiates calls

---

## Key Gotchas (Don't Skip This)

| Issue | Impact | Fix |
|-------|--------|-----|
| LLM costs not in per-minute price | Cost surprise later | Monitor pricing announcements |
| URL knowledge is a snapshot | Outdated info | Re-import monthly |
| Agent asks multiple questions | Unnatural conversation | "Ask ONE question at a time" in prompt |
| No soft timeout configured | Awkward silence | Enable 3s soft timeout |
| Phone numbers come as words | Tool failures | Specify format in parameter descriptions |
| Make scenario timeout = 40s | Mid-call failures | Keep real-time scenarios simple |
| Concurrency limits | Missed calls | Monitor usage; upgrade if needed |
| Agent doesn't hang up | Call lingers | Script closing + end_call tool |

---

## What Makes a Great Agent (vs. Average)

### Average agent
- Generic "How can I assist you today?"
- Asks all questions at once
- Makes up answers when unsure
- Sounds robotic
- No error handling
- Never hangs up cleanly

### Great agent
- Warm branded greeting with agent's name
- One question at a time, natural flow
- Has knowledge base — never guesses
- Sounds human (good voice, soft timeout configured, natural filler phrases)
- Explicit guardrails (never promises, never oversteps)
- Validates and confirms data before saving
- Clean, warm goodbye with clear next steps
- Call ends properly with end_call tool
- Post-call webhook saves full transcript for review

---

## Deployment Checklist for Trade Business

**Before going live:**
- [ ] System prompt tested with 10+ realistic calls
- [ ] Knowledge base has: services, pricing, service areas, FAQ
- [ ] Agent never promises exact prices or confirms bookings
- [ ] Soft timeout configured (3 seconds, natural filler)
- [ ] Turn eagerness set appropriately (Patient when collecting details)
- [ ] Tool tested with real data — check what arrives at your webhook
- [ ] Make scenario handles empty/malformed fields gracefully
- [ ] Confirmation SMS/email working
- [ ] Owner notification working
- [ ] Twilio number properly connected
- [ ] Call recording disclosure (if recording is enabled)
- [ ] Phone number verified and tested (call it yourself first)
- [ ] Concurrency limit appropriate for expected call volume

**Week 1 monitoring:**
- [ ] Review every call transcript daily
- [ ] Check for common unanswered questions → add to knowledge base
- [ ] Check for data format issues in webhook payloads
- [ ] Adjust system prompt based on real call patterns

---

## Further Reading (Official Docs)

- Platform overview: https://elevenlabs.io/docs/eleven-agents/overview
- Prompting guide: https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide
- Knowledge base: https://elevenlabs.io/docs/eleven-agents/customization/knowledge-base
- RAG: https://elevenlabs.io/docs/eleven-agents/customization/knowledge-base/rag
- Conversation flow: https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow
- Twilio integration: https://elevenlabs.io/agents/integrations/twilio
- Make integration: https://elevenlabs.io/agents/integrations/make
- Pricing: https://elevenlabs.io/pricing
- Blog - How to prompt: https://elevenlabs.io/blog/how-to-prompt-a-conversational-ai-system

---

## Files in This Research Package

| File | Contents |
|------|----------|
| `elevenlabs-platform.md` | Full platform overview, capabilities, architecture, pricing |
| `elevenlabs-prompting.md` | System prompt guide, templates, best practices |
| `elevenlabs-knowledge-bases.md` | KB setup, RAG, content best practices |
| `elevenlabs-tools-webhooks.md` | Server tools, system tools, post-call webhooks |
| `elevenlabs-make-integration.md` | Make scenarios, patterns, setup guide |
| `elevenlabs-gotchas.md` | Known issues, limits, things to avoid |
| `elevenlabs-master-summary.md` | This file — concise overview of everything |
