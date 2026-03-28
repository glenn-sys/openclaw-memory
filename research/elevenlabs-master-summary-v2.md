# ElevenLabs Voice Agent — Master Summary v2

*Comprehensive reference for building voice agents for trade businesses*
*V1 research: March 2026 | V2 deep research: March 2026*

---

## What This Document Is

This is the definitive knowledge base for building ElevenLabs-powered voice agents for NZ/AU trades businesses (pest control, carpet cleaning, HVAC, plumbing). It combines foundational knowledge from V1 with advanced practitioner insights from V2 deep research.

**Files in this research package:**
| File | Contents |
|------|----------|
| `elevenlabs-platform.md` | Platform overview, capabilities, pricing (V1) |
| `elevenlabs-prompting.md` | Prompting guide, templates (V1) |
| `elevenlabs-knowledge-bases.md` | Knowledge base setup, RAG (V1) |
| `elevenlabs-tools-webhooks.md` | Webhooks, tools, patterns (V1) |
| `elevenlabs-make-integration.md` | Make scenarios, setup guide (V1) |
| `elevenlabs-gotchas.md` | Known issues, limits (V1) |
| `elevenlabs-advanced-prompting.md` | Advanced prompting, emotional handling, v3 (V2) |
| `elevenlabs-api-deep-dive.md` | Full API reference, code examples (V2) |
| `elevenlabs-community-knowledge.md` | Community insights, failure patterns (V2) |
| `elevenlabs-trade-business.md` | Trade-specific knowledge, NZ/AU compliance (V2) |
| `elevenlabs-competitive-intel.md` | Competitive landscape, agency pricing (V2) |
| `elevenlabs-make-advanced.md` | Advanced Make patterns, error handling (V2) |
| `elevenlabs-master-summary-v2.md` | This file |

---

## Platform Summary (Updated March 2026)

### Core Capabilities
- Voice quality: Best in market (ElevenLabs TTS)
- Pricing: **$0.10/min** (Creator/Pro), **$0.08/min** (Business annual)
- LLM: Any LLM (GPT-4o-mini, Gemini Flash, Claude recommended)
- TTS models: eleven_flash_v2 (default), eleven_v3_conversational (best quality + expressive mode)
- Phone: Twilio native integration or SIP trunking
- Concurrent calls: Creator (5), Pro (10), Scale (15)
- Silence billing: **5% of per-minute rate** during silent periods

### New in 2026 (V2 Research)
- **Eleven v3 Conversational model**: Context-aware delivery, emotional expressiveness, 70+ languages — same price as other models
- **Expressive Mode**: Automatic emotional delivery adjustment based on caller's tone
- **Expressive tags** in responses: `[laughs]`, `[sighs]`, `[excited]`, `[whispers]`, `[slow]`
- **Speculative turn**: Start generating LLM response during silence before turn ends (reduces perceived latency)
- **SIP inbound headers as dynamic variables**: `{{sip_contact_id}}`, etc.
- **WhatsApp outbound**: Now supported
- **Custom guardrails**: Platform-level content moderation thresholds
- **Users page**: Groups conversations by caller identifier
- **Conversation filtering by tool outcome**: Filter API for tool success/error

---

## API Quick Reference (V2)

### Authentication
```
Header: xi-api-key: YOUR_API_KEY
```

### Key Endpoints
```
POST   /v1/convai/agents/create          # Create agent
PATCH  /v1/convai/agents/{id}            # Update agent
GET    /v1/convai/agents/{id}            # Get agent

POST   /v1/convai/knowledge-base/text    # Add text document
POST   /v1/convai/knowledge-base/url     # Import URL (snapshot)
POST   /v1/convai/knowledge-base/file    # Upload file

GET    /v1/convai/conversations          # List conversations (filterable)
GET    /v1/convai/conversations/{id}     # Get transcript + analysis

# Base: https://api.elevenlabs.io
```

### Conversation Transcript Access
```python
from elevenlabs import ElevenLabs
client = ElevenLabs(api_key="YOUR_KEY")

# List recent calls
convos = client.conversational_ai.conversations.list(
    agent_id="agent_abc",
    page_size=50
)

# Get full transcript
convo = client.conversational_ai.conversations.get("conv_abc")
for turn in convo.transcript:
    print(f"{turn.role}: {turn.message}")
```

---

## System Prompt Template v2 (Production-Ready)

```markdown
# Personality
You are [Name], a [friendly/professional] [role] for [Business Name] in [City/Area], New Zealand.
You are warm, efficient, and knowledgeable about our services.

# Goal
Answer inbound calls, handle enquiries, and collect details for bookings or quotes.
Your job is complete when you've collected all needed details or answered the caller's question.

# Business Context
[Business Name] provides [services] across [service areas].
Business hours: [hours].
After hours calls: We still take messages and call back.

# Emergency Protocol
Listen for: "urgent", "emergency", "flooding", "burst", "swarm", "can't wait"
If emergency detected:
1. Acknowledge: "That sounds urgent — let me make sure we get someone on this."
2. Collect ONLY name, address, phone
3. Use escalate_emergency tool
4. Promise callback within 30 minutes
Do NOT proceed with standard booking questions for emergencies.

# Process — Standard Calls
1. Answer: "[Business Name], this is [Name], how can I help?"
2. Listen to need, identify: booking / quote / question / existing customer
3. For bookings/quotes, collect ONE AT A TIME (this step is important):
   a. Name (first name fine)
   b. Address or suburb (to confirm service area)
   c. Service needed (with enough detail)
   d. Preferred timeframe
   e. Best phone number
4. Confirm all details back: "Just to confirm — I have [name] at [address], needing [service]..."
5. Save with save_enquiry tool AFTER confirmation
6. Explain next step: "Our team will call you within 2 hours during business hours."
7. "Is there anything else I can help with?"
8. Warm close, then end_call.

# Tools

## save_enquiry
Call ONLY after confirming ALL details with caller.
Required: name, phone (digits only, e.g. "0211234567"), service_needed
Optional: address, preferred_time, notes
Do NOT call this tool until you've confirmed the details are correct.

# Guardrails
Ask ONE question at a time. This step is important.
Never quote specific prices — say "our team will confirm pricing when they call."
Never confirm bookings — only "our team will call to confirm."
Do not discuss competitors.
If caller is abusive: "I want to help, but I need a respectful conversation. If this continues, I'll need to end the call." Use end_call if it continues.
Only discuss [Business Name] services. Redirect off-topic questions.

# Tone Guidelines (Expressive Mode)
When caller sounds frustrated: respond in a calm, empathetic tone
When caller shares good news: respond with warmth and genuine enthusiasm
When explaining next steps: speak clearly and measured
When handling complaints: remain composed and solution-oriented

# Common Objections
"Too expensive": "Our team can give you a proper quote so you know exactly what you're looking at — would you like them to call you?"
"I'll call back later": "Of course! Would it actually be quicker if our team called you? I can take your number right now."
```

---

## Voice Configuration (V2 Recommendations)

| Setting | Value | Why |
|---------|-------|-----|
| TTS Model | `eleven_v3_conversational` | Best quality + expressive mode (same price) |
| Stability | 0.45-0.55 | Warm and dynamic but consistent |
| Speed | 0.95 | Slightly slower = more natural |
| Turn eagerness | `patient` | Collecting addresses/details = patient |
| Soft timeout | 2-3 seconds | Natural filler during LLM processing |
| Soft timeout message | "Let me just check on that..." | Natural filler |
| Spelling patience | `auto` | Better for phone numbers/addresses |
| Silence end call | 30-45 seconds | End calls if caller disappears |
| Speculative turn | false (start) | Enable later to reduce latency once stable |

**Recommended voices for NZ/AU trades:**
- `HDA9tsk27wYi3uq0fPcK` — Stuart (Professional & friendly Aussie)
- `PT4nqlKZfc06VW1BuClj` — Angela (Warm, relatable, great listener)
- Custom voice clone — if business owner has a good voice, clone it

---

## Make Integration — Minimal Viable Setup (V2)

```
[ElevenLabs agent]
    → save_enquiry tool
    → [Make Webhook]
        → Google Sheets (add row)
        → Twilio SMS (to caller)
        → Gmail (to owner)
        → Webhook Response (200 OK)
```

**Time to build**: 20-30 minutes  
**Cost**: Make free tier handles low volume; $9/month for Starter beyond that

**Error handling (V2 best practice):**
- Enable "Allow storing incomplete executions" in Make scenario settings
- Add Break handler with 3 retries to all external API modules
- Return 200 OK even if processing fails (don't break the agent's conversation)
- Log all failures to a "Review" sheet for manual follow-up

---

## Compliance (NZ/AU) — V2 Research

### New Zealand (Inbound Calls)
- Privacy Act 2020: collect only what you need, store securely
- **Recording disclosure**: "This call may be recorded for quality purposes"
- AI disclosure (inbound): No specific law yet, but best practice for transparency
- After-hours: Calling hours are 8am-9pm Mon-Sat (Marketing Association Code)

### Australia (Inbound Calls)
- Telecommunications (Interception and Access) Act: all-party consent for recording
- **Standard disclosure**: Add to first message if recording enabled
- Privacy Act 1988 (+ 2025-26 reforms): AI decision-making transparency becoming mandatory

### Practical Disclosure (Both Countries)
```
First message with recording disclosure:
"[Business], this is [Name]. Just so you know, this call may be recorded 
for quality purposes. How can I help you today?"
```

### Outbound AI Calls (Both Countries)
- Must identify as AI immediately
- Must provide opt-out mechanism
- AU: must screen against Do Not Call Register
- AU: Calling hours strict (9am-8pm M-F, 9am-5pm Sat, no Sunday)
- NZ: 8am-9pm Mon-Sat

---

## Competitive Position (V2 Research)

### Why ElevenLabs Wins
1. **Voice quality** — genuinely better than Retell, Vapi, Synthflow (community consensus)
2. **Full-featured API** — create/manage agents, conversations, knowledge base programmatically
3. **Expressive mode** — emotional intelligence that competitors don't have
4. **Flexibility** — any LLM, any telephony (Twilio or SIP)

### The Gap in the Market
No one in NZ/AU is offering a productised "AI receptionist for trades businesses" at small-business price points:
- Setup: $1,000-1,500 (builds agent, tests, monitors for 30 days)
- Monthly: $350-$600 (management, monitoring, prompt updates, support)
- Cost structure: ElevenLabs $22 + Twilio ~$5 + Make $9 + minutes @ $0.12 = ~$60-80/month base

At 500 min/month = $60 extra = ~$140 total cost vs. $400 revenue = strong margin.

### Who You're Competing With
- Human answering services: $1,000-2,000/month (expensive, no 24/7)
- Doing nothing: Missed calls, lost revenue
- Goodcall: ~$99-299/month (limited, US-focused, no NZ presence)
- Avoca AI: Enterprise pricing ($2k+/month), too expensive for small trades

---

## Known Gotchas (V1 + V2 Combined)

| Issue | Impact | Fix |
|-------|--------|-----|
| LLM costs not in per-minute price | Cost surprise | Monitor, especially with GPT-4o |
| URL KB is a snapshot | Stale info | Re-import monthly |
| Agent asks multiple questions | Unnatural | "Ask ONE question at a time. This step is important." |
| No soft timeout | Awkward silence | Enable 3-second soft timeout |
| Phone numbers as words | Tool failures | Specify format in parameter descriptions |
| Make timeout = 40s | Mid-call failures | Keep real-time scenarios < 5 modules |
| Tool called too early | Missing data | Explicit list of required fields + "only when confirmed" |
| Tool called too late | Lost lead | Link tool call to confirmation step explicitly |
| Expressive tags overused | Sounds odd | Max 1-2 per conversation; don't overdo `[sighs]` |
| Voice clone not preserved in v3 | Doesn't sound like clone | Use standard voices for v3 Conversational |
| ElevenLabs webhook not retried | Lost post-call data | Return 200 immediately; process async in Make |
| Speculative turn increases cost | Budget surprise | Test before enabling in production |

---

## The Production Deployment Checklist (V2 Updated)

**Configuration:**
- [ ] TTS model: eleven_v3_conversational
- [ ] Expressive mode enabled (default with v3)
- [ ] Tone guidelines in system prompt for emotional delivery
- [ ] Soft timeout: 3s, custom filler phrase
- [ ] Turn eagerness: patient (for detail collection)
- [ ] Spelling patience: auto
- [ ] Silence end call timeout: 30-45 seconds
- [ ] Knowledge base: services, pricing ranges, FAQ, service areas
- [ ] ASR keywords: trade-specific terms boosted

**Prompting:**
- [ ] Exact first message written out ("Answer with: '...'")
- [ ] Emergency protocol defined
- [ ] One-question-at-a-time rule explicit
- [ ] Tool trigger conditions listed precisely
- [ ] Error handling for tool failures
- [ ] Objection handling scripted
- [ ] Guardrails section dedicated and comprehensive
- [ ] Tone guidelines for expressive mode

**Make Integration:**
- [ ] Webhook URL in Secrets Manager
- [ ] Authentication header configured
- [ ] Error handlers on all external modules
- [ ] Incomplete executions enabled
- [ ] Phone number parsing handles all formats
- [ ] Missing field handling (don't fail if optional fields empty)
- [ ] 200 OK returned
- [ ] Tested with real data

**Compliance:**
- [ ] Recording disclosure in first message (if recording enabled)
- [ ] AI disclosure considered (best practice)
- [ ] Data retention configured (ElevenLabs Privacy settings)
- [ ] GDPR/Privacy Act compliant data storage

**Testing:**
- [ ] Test with real phone (not just web widget)
- [ ] Test 10 realistic call scenarios
- [ ] Test angry caller
- [ ] Test "I'll call back"
- [ ] Test "I want to talk to a human"
- [ ] Test off-topic questions
- [ ] Test emergency call
- [ ] Test partial information (caller only gives name, hangs up)
- [ ] Verify data arrives correctly at webhook
- [ ] Verify SMS/email confirmation sent

**Week 1 Monitoring:**
- [ ] Review every call transcript
- [ ] Check Make execution history daily
- [ ] Log common questions not in KB → add to KB
- [ ] Note any prompt failures → fix prompt
- [ ] Note any data format issues → fix tool parameters

---

## Further Reading

**Official ElevenLabs Docs:**
- Overview: https://elevenlabs.io/docs/eleven-agents/overview
- Prompting guide: https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide
- Expressive mode: https://elevenlabs.io/docs/eleven-agents/customization/voice/expressive-mode
- Voice design: https://elevenlabs.io/docs/eleven-agents/customization/voice/best-practices/conversational-voice-design
- Dynamic variables: https://elevenlabs.io/docs/agents-platform/customization/personalization/dynamic-variables
- LLM optimization: https://elevenlabs.io/docs/eleven-agents/customization/llm/optimizing-costs
- API reference: https://elevenlabs.io/docs/api-reference/introduction
- Plumbing/trades landing page: https://elevenlabs.io/agents/plumbing-answering-service

**Compliance:**
- NZ/AU compliance guide: https://envokeai.co.nz/blog/regulatory-compliance-for-ai-voice-calls-in-nz-au
- AU call recording laws: https://telnyx.com/resources/phone-recording-law-australia

**YouTube:**
- Make.com + ElevenLabs full tutorial: https://www.youtube.com/watch?v=bbj1bAe7ADc
- First voice agent setup: https://www.youtube.com/watch?v=fnivYSh0Cqk

**Competitive:**
- VoiceAIWrapper (agency platform): https://voiceaiwrapper.com
- Avoca AI (trades-specific): https://www.avoca.ai
