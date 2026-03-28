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
# ElevenLabs Conversational AI Platform — Overview, Capabilities & Pricing

*Researched: March 2026*

---

## What Is It?

ElevenLabs Conversational AI (now branded **ElevenAgents**) is an all-in-one platform for building real-time AI voice and chat agents. It bundles:

1. **ASR (Speech-to-Text)** — fine-tuned model for speech recognition
2. **LLM** — your choice of GPT-4, Claude, Gemini, or custom/self-hosted
3. **TTS (Text-to-Speech)** — low-latency synthesis across 5,000+ voices, 70+ languages
4. **Turn-taking model** — proprietary model that handles conversation timing naturally

Key headline stats:
- **Sub-100ms latency** (voice response)
- **70+ languages** supported
- **5,000+ voices** available
- **32+ languages** for real-time conversation
- SOC 2, HIPAA, GDPR compliant

---

## Platform Architecture

```
User Speech
    ↓
[ASR / Speech-to-Text]
    ↓
[LLM — generates response]
    ↓  ← RAG knowledge retrieval happens here
[TTS — speaks response]
    ↓
User hears voice

[Turn-taking model] monitors throughout ← knows when to interrupt, wait, respond
```

---

## Core Features (2025–2026)

### Conversation Intelligence
- **State-of-the-art turn-taking model** — understands filler words ("um", "ah"), natural pauses
- **Interruption handling** — user can interrupt agent mid-sentence (configurable)
- **Turn eagerness** — Eager / Normal / Patient modes
- **Soft timeout / filler messages** — "Hmm, let me check that..." while thinking
- **Auto language detection** — detects user's language and switches automatically

### Knowledge & Grounding
- **Knowledge base** — upload PDFs, TXT, DOCX, HTML, EPUB or paste URLs/text
- **Integrated RAG** — retrieval-augmented generation, sub-200ms query rewriting
- **Direct prompt injection** — small docs injected directly; large docs use RAG

### Workflow & Tools
- **Server tools** — agent calls your webhooks/APIs mid-conversation
- **Client tools** — agent triggers actions in the browser/app (UI updates, etc.)
- **System tools** — built-in tools: `end_call`, call transfer
- **Visual Workflow Builder** — no-code multi-step conversation flows (2025)
- **Dynamic variables** — per-call personalization (caller name, account details, etc.)

### Deployment Channels
- **Telephony** — Twilio (native), SIP trunking (Vonage, RingCentral, Sinch, Telnyx, etc.)
- **Web widget** — embeddable on any website
- **SDKs** — JavaScript, Python, Swift (iOS), Kotlin (Android), React, React Native
- **WebSocket API** — low-level custom integration
- **Outbound/Batch calls** — programmatic multi-call campaigns

### Multimodal
- Voice only, text only, or voice + text simultaneously
- Same agent config works across both modalities

### Monitoring & Testing
- Conversation analytics dashboard
- A/B testing (experiments)
- Automated agent testing
- Conversation analysis (transcripts, outcomes)
- Call recordings (configurable retention)

---

## LLM Support

You can bring your own LLM or use hosted options. Supported:
- OpenAI GPT-4 series
- Anthropic Claude series
- Google Gemini series
- Custom / self-hosted models (via Custom LLM API)

Different LLMs can be used for different workflow steps (e.g., use a fast Gemini Flash for FAQ, switch to Claude for complex reasoning).

---

## Conversational AI 2.0 (May 2025) — Key Upgrades

| Feature | v1 | v2 |
|---------|----|----|
| Interaction Flow | Basic API | State-of-the-art turn-taking |
| Knowledge | None | Integrated RAG |
| Multilingual | Manual switching | Auto language detection |
| Personas | Single voice | Multi-character switching |
| Enterprise | Standard | HIPAA, EU residency, enhanced security |
| Modality | Voice only | Voice + Text |
| Telephony | Twilio inbound only | Full inbound + outbound, SIP trunking, batch calls |

---

## Pricing (as of March 2026)

### Conversational AI billing model
- Billed **per minute** of conversation
- LLM costs currently absorbed by ElevenLabs (may change)
- Note: telephony costs (Twilio, etc.) are separate

### Conversational AI per-minute rates
| Plan | Cost per minute |
|------|----------------|
| Free | ~$0.10/min (limited) |
| Starter | ~$0.10/min |
| Creator | ~$0.10/min |
| Pro | ~$0.10/min |
| Business (annual) | **$0.08/min** |
| Enterprise | Lower, negotiated |

> ElevenLabs announced a ~50% price cut in Feb 2025: "Calls now start at 10 cents per minute."

### Concurrency limits (parallel calls)
| Plan | Concurrent calls |
|------|-----------------|
| Free | 2 |
| Starter | 3 |
| Creator | 5 |
| Pro | 10 |
| Scale | 15 |
| Business | 15 |
| Enterprise | Custom (higher) |

- **Surge capacity**: When enabled, agents can handle up to 3× normal concurrency, with excess calls charged at double the standard rate.
- No limit on number of agents you can CREATE — only concurrency limits matter.

### Subscription plan overview (TTS credits + Agent access)
| Plan | Monthly price | TTS credits (Multilingual) | Seats | Notes |
|------|--------------|---------------------------|-------|-------|
| Free | $0 | 10k chars | 1 | No commercial use |
| Starter | $5 | 30k chars | 1 | Commercial license |
| Creator | $22 ($11 first month) | 100k chars | 1 | Prof. voice cloning |
| Pro | $99 | 500k chars | 1 | 44.1kHz PCM |
| Scale | $330 | 2M chars | 3 | Team collaboration |
| Business | $1,320 | 11M chars | 5 | Low-latency TTS |
| Enterprise | Custom | Custom | Custom | SLAs, HIPAA, SSO |

### Startup Grant Program
- 12 months free access
- 33M characters
- For new products/startups — apply at elevenlabs.io/startup-grants

---

## RAG Knowledge Base Limits

| Plan | Max RAG document size |
|------|----------------------|
| Free | 1 MB (may be deleted after inactivity) |
| Starter | 2 MB |
| Creator | 20 MB |
| Pro | 100 MB |
| Scale | 500 MB |
| Business | 1 GB |
| Enterprise | 1 GB+ (negotiated) |

Non-enterprise accounts: max 20 MB or 300k characters for non-RAG knowledge base.

---

## Key Integrations Available

- **Telephony**: Twilio, Vonage, RingCentral, Sinch, Telnyx, Bandwidth, Plivo, Infobip, Exotel
- **Automation**: Make (Integromat), Zapier, custom webhooks
- **CRM**: Salesforce, HubSpot (via webhooks/tools)
- **Payments**: Stripe (via tools)
- **Support**: Zendesk (via tools)
- **Scheduling**: Calendly and custom booking systems (via tools)

---

## Use Case Fit for Trade Businesses (Pest Control, Carpet Cleaning)

ElevenLabs is well-suited for:
- **24/7 phone answering** — never miss a call
- **Appointment booking** — collect details, confirm availability
- **Quote capture** — gather job details before calling back
- **FAQ handling** — pricing, service areas, what to expect
- **Lead qualification** — collect contact details, job type, urgency

The AI receptionist / answering service product page specifically calls out: "Greet every caller in a lifelike voice, capture details instantly."
# ElevenLabs Voice Agent Prompting Guide

*Source: ElevenLabs official docs + blog (March 2026)*

---

## The Core Problem With Naive Prompting

LLMs default to **written** behaviour — verbose, bulleted, structured. For voice, you need:
- Short, conversational responses
- No lists or headers
- Natural rhythm (one question at a time)
- Explicit instructions about what to say out loud

**Common mistakes:**
1. Copying human agent training docs directly into the prompt
2. Forgetting to tell the LLM to write numbers as words
3. Asking for all info at once instead of one piece at a time
4. No guardrails section
5. Relying on tone guidance scattered throughout (centralise it)

---

## System Prompt Structure — Best Practice

Use clear markdown sections. Models are tuned to pay extra attention to certain headings, especially `# Guardrails`.

```markdown
# Personality
You are [Name], a [role] for [Company]. You are [tone descriptors].

# Goal
[What the agent should accomplish in 2-3 sentences]

# Context
[Key facts about the business, services, location, etc.]

# Process
[Step-by-step flow — what to ask, in what order]

# Tools
[List tools available and WHEN + HOW to use each]

# Guardrails
[Non-negotiable rules — what the agent MUST NOT do]

# Tone
[Specific voice/style guidelines]
```

---

## Section-by-Section Guide

### # Personality
Define the agent's name, role, and character traits.

```
# Personality
You are Sarah, a friendly receptionist for CleanRight Carpet Cleaning in Auckland.
You are warm, efficient, and professional — like a knowledgeable local who genuinely
wants to help callers get their carpets sorted.
```

### # Goal
Keep it short. What is the ONE job of this agent?

```
# Goal
Help callers book a carpet cleaning job or get a quote. Collect all the details
needed so the team can follow up or confirm a booking.
```

### # Context / Knowledge
Put business facts here. Or better: use a Knowledge Base for larger amounts.

```
# Context
CleanRight operates in Auckland and the North Shore. We clean carpets, upholstery,
and rugs. Standard pricing starts at $80 for a single room. Jobs are booked 
Monday–Saturday between 7am and 6pm.
```

### # Process
This is the call flow. Critical for trade businesses. Tell it what to collect, in order.

```
# Process
1. Greet the caller warmly by answering: "CleanRight Carpet Cleaning, this is Sarah, 
   how can I help you today?"
2. Ask what they need (booking, quote, question).
3. For a booking or quote, collect:
   - Their name (first name only is fine)
   - Their suburb or address
   - What needs cleaning (carpets, rugs, upholstery — which rooms/items)
   - Their preferred day and time
   - Their phone number
4. Confirm the details back to them.
5. Let them know someone will call back to confirm within 2 hours during business hours.
6. Thank them and end the call warmly.
```

**Key rule**: Ask ONE question at a time. Never dump multiple questions in one turn.

### # Tools
Explicitly describe each tool, when to use it, and how.

```
# Tools

## save_lead
Use this tool after collecting all caller details to save the lead.
When to use: After confirming all required information with the caller.
Required fields: name, address, services_needed, preferred_time, phone_number
Do NOT call this tool until all required information has been collected and confirmed.

## check_availability
Use this to check available booking slots.
When to use: When a caller asks about specific dates/times.
Input: date (format: YYYY-MM-DD)
```

### # Guardrails
Always have this section. Models prioritise it.

```
# Guardrails
Never promise a specific price without first checking the job details.
Never confirm a booking — only say "someone will call to confirm."
Never share other customers' details.
If the caller asks something you don't know, say "I'll have the team follow up with you."
If the caller becomes abusive, politely say "I'm going to end this call now" and hang up.
Do not discuss competitors.
Only take bookings for the areas we service (Auckland and North Shore).
```

### # Tone
Keep it short. Define once, don't repeat.

```
# Tone
Speak in a warm, friendly, and efficient manner. Use natural conversational language —
no jargon. Keep responses concise. One thought per turn.
```

---

## Text Normalisation — Critical for Voice

TTS models struggle with digits and symbols. ElevenLabs auto-normalises but you should understand the options:

### Option 1: system_prompt (default)
Instructions added to prompt telling LLM to write out numbers as words.
- ✅ No additional latency
- ❌ LLM occasionally fails to normalise
- Transcripts contain words ("one thousand dollars")

### Option 2: elevenlabs normaliser
ElevenLabs normalises after LLM generation before TTS.
- ✅ More reliable
- ✅ Transcripts show natural symbols ($1,000)
- ❌ Adds ~minor latency

**Gotcha with tool inputs**: When using `system_prompt` normalisation, tool parameters get the spoken-form value ("john at gmail dot com") not "john@gmail.com". Always specify format explicitly in tool parameter descriptions:

```
- email (required): "Customer email in standard format, e.g. 'john@example.com'"
- phone (required): "Phone number as digits only, e.g. '0211234567'"
```

---

## Call Flow Design Patterns

### Single-purpose FAQ bot
Simple. Focus the prompt tightly on answering questions.
```
# Goal
Answer questions about our pest control services and pricing.
If the caller wants to book, collect their name and phone number and let them 
know someone will call back within 30 minutes.
```

### Lead capture agent
Main job: get contact details + job description.
- Always confirm details back before saving
- Don't promise anything
- End with a clear "next step" so caller knows what happens

### Booking agent
More complex. Needs:
- Availability checking (via tool)
- Confirmation logic
- Validation (phone numbers, dates)

Pattern: Collect → Validate → Confirm → Save → Close

### Objection handling
Build objection responses into the prompt:
```
# Handling Common Objections
If caller says "you're too expensive": Acknowledge their concern, mention we offer
free quotes and can discuss options. Do not negotiate pricing on the call.
If caller says "I'll call back later": Offer to take their details so the team 
can call them instead.
```

---

## Ending Calls Gracefully

Build an exit into the process:

```
# Ending the Call
After completing the purpose of the call:
1. Summarise what will happen next ("Our team will call you back within 2 hours")
2. Ask "Is there anything else I can help you with?"
3. If no: "Great, thanks for calling CleanRight. Have a wonderful day!" then end.

Use the end_call tool to hang up after the farewell.
```

Never just hang up without a warm close. Callers notice abrupt endings.

---

## Validation and Verification

Build in confirmation of critical data:

```
# Validation
After collecting a phone number, repeat it back: "I have your number as zero-two-one-
one-two-three-four-five-six-seven — is that right?"
If the number has too many or too few digits, say: "I think I may have heard that 
wrong — could you repeat that for me?"
```

Apply same logic to: email addresses, addresses, booking dates.

---

## Temperature Setting

- **Low temperature** (0.0–0.3): Consistent, predictable responses. Good for booking/FAQ bots.
- **High temperature** (0.7–1.0): More creative, varied. Better for engagement/entertainment.

For trade business agents: **use low temperature**. Consistency builds trust.

---

## Persona Design Tips

1. **Give the agent a name** — "Sarah" or "Max" feels more human than "Assistant"
2. **Match your brand voice** — relaxed and friendly for residential, professional for commercial
3. **Give it local knowledge** — "We service Auckland and the North Shore"
4. **Define what it does NOT know** — "If asked about franchises or other locations, say you're not sure and offer to take a message"

---

## System Prompt Template for Trade Business

```markdown
# Personality
You are [Name], a friendly and efficient receptionist for [Business Name] in [City/Area].
You are warm, helpful, and knowledgeable about our services.

# Goal
Answer incoming calls, handle enquiries, and collect details for quotes or bookings.

# Business Context
[Business Name] provides [services] in [service areas].
Operating hours: [hours].
Starting prices: [pricing overview].

# Process
1. Answer with: "[Business Name], this is [Name], how can I help you?"
2. Listen to the caller's need.
3. For bookings and quotes, collect:
   - Name
   - Address or suburb
   - What service is needed (and details — e.g. how many rooms, what pest)
   - Preferred date/time
   - Best phone number
4. Confirm all details back to the caller. This step is important.
5. Explain next steps: "Our team will be in touch within [timeframe]."
6. Close warmly and use the end_call tool.

# Tools
## save_enquiry
Use after confirming all details. Pass: name, address, service, preferred_time, phone.

# Guardrails
Do not quote exact prices — say "our team will confirm pricing when they call."
Do not confirm bookings — only say "someone will be in touch to confirm."
If you don't know something, say so and offer to take a message.
Do not discuss competitors.
Ask ONE question at a time. This step is important.

# Tone
Friendly, warm, concise. Natural conversational language. No jargon or robotic phrases.
```

---

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| "Please hold while I look that up" | Use soft timeout filler like "Let me check that for you..." |
| Asking multiple questions at once | Explicitly instruct: "Ask ONE question at a time" |
| Number/email format errors in tools | Add format examples to tool parameter descriptions |
| Agent promises things it can't deliver | Add explicit guardrails: "Never promise X" |
| Agent goes off-topic | Add: "Only discuss topics related to [business services]" |
| Robotic goodbye | Script the closing lines explicitly |
| Greeting sounds like a robot | Write the exact first sentence: "Answer with: 'Hi, you've reached...'" |
# ElevenLabs Advanced Prompting — Deep Dive

*Deep research: March 2026*

---

## Official Prompt Engineering Fundamentals (From Docs)

The official prompting guide (https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide) establishes these core principles for production-grade agents:

### 1. Separate Instructions Into Clean Sections

Use markdown headings to separate concerns. The model is specifically tuned to pay extra attention to `# Guardrails`. Section boundaries prevent "instruction bleed" where rules from one context affect another.

**Example — Less effective:**
```
You are a customer service agent. Be polite and helpful. Never share sensitive data. 
You can look up orders and process refunds. Always verify identity first.
```

**Example — Recommended:**
```markdown
# Personality
You are a customer service agent for Acme Corp. You are polite, efficient, and solution-oriented.

# Goal
Help customers resolve issues quickly by looking up orders and processing refunds when appropriate.

# Guardrails
Never share sensitive customer data across conversations.
Always verify customer identity before accessing account information.

# Tone
Keep responses concise (under 3 sentences) unless the user requests detailed explanations.
```

### 2. Be As Concise As Possible

Every unnecessary word is a potential source of misinterpretation and increases token cost. 

**Less effective:**
```
When you're talking to customers, you should try to be really friendly and approachable, 
making sure that you're speaking in a way that feels natural and conversational, kind of 
like how you'd talk to a friend, but still maintaining a professional demeanor.
```

**Recommended:**
```
# Tone
Speak in a friendly, conversational manner while maintaining professionalism.
```

### 3. Emphasize Critical Instructions

Add "This step is important." at the end of critical lines. Repeating the 1-2 most critical instructions twice reinforces them. In complex prompts, models may prioritize recent context over earlier instructions.

```markdown
# Goal
Verify customer identity before accessing their account. This step is important.
Look up order details and provide status updates.
Process refund requests when eligible.

# Guardrails
Never access account information without verifying customer identity first. This step is important.
```

### 4. Dedicate a Guardrails Section

The `# Guardrails` heading is special — models are specifically tuned to pay attention to it. Always centralise non-negotiable rules here.

### 5. Prompt Length

- **Maximum system prompt size**: 2MB (including system prompt + knowledge base content injected into context)
- **Best practice**: Be as concise as possible. Avoid padding and repetition.
- **Multi-agent pattern**: For complex flows, break into multiple agents with smaller, specialised prompts. Use agent-agent transfer to route between them. This reduces token count per interaction significantly.
- For a simple trade business agent: a well-structured prompt of 400-800 words is optimal. Under 200 words risks missing important guardrails; over 2000 words starts diluting attention on critical rules.

---

## Advanced Techniques

### Handling Interruptions

ElevenLabs has an interruption system built in. By default, callers can interrupt the agent at any time (which is natural). However:

- For legally required disclosures (e.g., recording notice), you may want to prevent interruption
- Configure interruption behaviour at the platform level, not just in the prompt
- With Eleven v3 Conversational + Expressive Mode, the new turn-taking system uses Scribe v2 Realtime to detect prosodic cues — so "yeah" as an acknowledgement vs. "yeah" as a lead-in to continue speaking is distinguished

```markdown
# Handling Interruptions
If the caller interrupts you mid-sentence, stop speaking immediately and listen.
Do not start over from the beginning. Resume naturally from where you were.
```

### Handling Dead Air / Silence

Configure **soft timeout** at the platform level (not in the prompt). When configured, if the LLM takes >N seconds to respond, the agent says a filler phrase.

- Default: `Hhmmmm...yeah.` (this is the literal default — replace it!)
- Better: `"Let me just check that for you..."` or `"One moment..."`
- Platform also lets you use **LLM-generated soft timeout messages** (dynamic, context-aware — may cost a bit more)
- Also configure `silence_end_call_timeout` to automatically end calls if there's sustained silence (default: disabled)

```markdown
# Dead Air
If you need a moment to think, say "Let me just check on that..." 
Never leave more than 2 seconds of silence without speaking.
```

### Handling Angry Callers

ElevenLabs v3 Conversational's **Expressive Mode** detects emotional cues from the caller's voice and adapts delivery accordingly. Guide it explicitly:

```markdown
# Handling Difficult Callers
If a caller sounds frustrated or upset:
1. Acknowledge their frustration first: "I can hear this has been frustrating, and I'm sorry to hear that."
2. Do not immediately try to solve the problem — validate first
3. Speak more slowly and calmly than normal
4. Focus on what you CAN do, not what you can't
5. If the caller becomes abusive or uses offensive language, say: "I want to help you, but I need us to have a respectful conversation to do that. If you continue this way, I'll need to end the call." Then use end_call if they continue.
```

With Expressive Mode:
```markdown
# Tone Guidelines (Expressive Mode)
- When a caller sounds frustrated or upset: respond in a calm, empathetic tone
- When explaining instructions or next steps: speak clearly and at a measured pace
- When a caller shares good news: respond with warmth and genuine enthusiasm  
- When handling complaints: remain composed and solution-oriented
- You may use [sighs] sparingly when acknowledging difficult situations
```

### Handling Off-Topic Questions

```markdown
# Scope
You are here to help with [Business Name] services only. 
If asked about unrelated topics, politely redirect:
"That's a bit outside my area — I'm really only able to help with [Business Name] services. 
Is there something I can help you with regarding [services]?"
```

### Handling "I'll Call Back Later"

```markdown
# Warm Capture
If the caller says they'll call back, or they're in a rush:
Offer to take their details now so the team can call THEM back: 
"No problem at all! Would it be quicker if I took your number and had someone from our team call you back?"
This is often easier for them and ensures we capture the lead.
```

---

## Advanced Prompt Patterns

### Pattern: Structured Booking Conversation

This is a linear conversation flow with explicit stages:

```markdown
# Personality
You are Mia, a friendly receptionist for BrightClean Carpet Cleaning in Auckland, New Zealand.

# Goal
Take bookings and quote enquiries for carpet cleaning jobs. Collect all required information
so our team can follow up or confirm a booking.

# Business Context
BrightClean serves greater Auckland: City, North Shore, East Auckland, West Auckland, Manukau.
Services: carpet cleaning, upholstery cleaning, rug cleaning, car interior.
Hours: Monday–Saturday 7am–6pm.
Pricing is based on job size; quotes confirmed on callback.

# Conversation Stages

## Stage 1: Greeting
Answer every call with: "BrightClean Carpet Cleaning, this is Mia, how can I help?"
Then listen to what they need.

## Stage 2: Understanding the Need
Based on what they say:
- If booking or quote → move to Stage 3
- If existing booking → take their name, let them know you'll pass the message, take notes
- If general question → answer from your knowledge base

## Stage 3: Collecting Information
Collect in this order, ONE question at a time. This step is important.
1. Name (first name is fine)
2. Address or suburb
3. What needs cleaning (carpet, upholstery, rug?) and how many rooms/items
4. Preferred date or timeframe ("this week", "next Saturday")
5. Best phone number

## Stage 4: Confirmation
Repeat all details back: "Just to confirm — I have your name as [name], at [suburb], 
looking to have [services] cleaned, preferably [timeframe], and best number is [number]."
Ask: "Is that all correct?"

## Stage 5: Saving and Closing
After confirmation: call save_booking tool.
Tell caller: "Perfect, I've passed your details to the team. They'll call you back within 2 hours 
during business hours to confirm your booking."
Ask: "Is there anything else I can help with?"
Warm close, then use end_call.

# Tools

## save_booking
Call ONLY after confirming all details in Stage 4.
Required: name, suburb_or_address, services_needed, preferred_time, phone_number
Optional: notes

# Guardrails
Never quote a specific price — say "our team will confirm pricing when they call you."
Never confirm a booking — only say "our team will call to confirm."
Only book for areas we service. If outside: "Unfortunately we're not able to service that area, 
but if you're ever in the greater Auckland region, we'd love to help."
Ask ONE question at a time. This step is important.
Do not discuss competitors.
```

### Pattern: Emergency Call Handling (Pest/HVAC)

```markdown
# Emergency Protocol
At the start of every call, listen for emergency signals:
- "urgent", "emergency", "flooding", "burst", "can't wait", "rats in my kitchen", 
  "bees attacking", "gas smell"

If emergency detected:
1. Acknowledge immediately: "That sounds urgent — let me make sure we get someone 
   to you as quickly as possible."
2. Collect JUST name, address, phone number (skip other questions for now)
3. Use escalate_emergency tool immediately
4. Tell caller: "I've flagged this as urgent. Someone will call you back within 
   [timeframe] — please keep your phone nearby."

Routine enquiries → proceed with standard booking flow.
```

### Pattern: Objection Handling Script

```markdown
# Common Objections

## "You're too expensive"
"I understand — price is definitely important. Our team can give you a proper quote 
over the phone so you know exactly what you're looking at before committing. 
Would that work for you?"

## "Can I just get a quote now?"
"I can give you a rough idea — [business] typically starts from [starting price] 
for a standard job. But the exact quote depends on the size and condition. 
Our team can give you a firm number in under 5 minutes — shall I get them to call you?"

## "I'll think about it / I need to discuss with my partner"
"Of course, no pressure at all. Would it help if I took your details 
so the team can send through some info? They're pretty quick — usually 
back to you within the hour."

## "I found someone cheaper"
"Totally understand. If you're ever looking to compare, we're happy to chat — 
our team takes pride in doing the job properly. Good luck with it!"
(Don't push — wish them well and close warmly.)
```

---

## Expressive Mode (Eleven v3 Conversational) — Advanced

Available when using V3 Conversational as TTS model. Same $0.08/min price. Key capabilities:

### Expressive Tags

Output specific delivery cues inline in responses. Tags affect ~4-5 words:

- `[laughs]` — adds laughter 
- `[whispers]` — lowers volume
- `[sighs]` — sighing quality (for empathy)
- `[slow]` — slows delivery (for emphasis)
- `[excited]` — adds excitement

Example in prompt:
```
You may use expressive tags for precise moments:
- Use [sighs] briefly when acknowledging something difficult: "I'm sorry to hear that [sighs]..."
- Use [excited] when sharing good news: "That's great! [excited] We have a slot..."
- Never overuse these — 1-2 per conversation maximum
```

### New Turn-Taking System

Built on Scribe v2 Realtime, the new turn-taking system:
- Reads prosodic cues (not just transcription) to determine when user has finished speaking
- Pair with **Patient** turn eagerness for detail-collection conversations
- Pair with **Eager** for fast-paced FAQ/support calls
- New: **Speculative turn** option — starts generating LLM response during silence before full turn confidence, reducing perceived latency (increases LLM costs slightly)

---

## Voice Design for Naturalness

### Voice Settings Reference

From the official conversational voice design guide:
- **Stability**: Lower (0.30-0.50) = more emotional, dynamic — may sound occasionally unstable. Higher (0.60-0.85) = consistent but potentially monotonous. For a warm receptionist: 0.45-0.60.
- **Similarity**: Higher = clearer, more consistent. Very high → distortion. Test at 0.75.
- **Speed**: Natural conversation happens at 0.9-1.1x. Slow for complex topics, faster for routine info.

### Recommended Voices for Trade Receptionist

From ElevenLabs docs:
- `HDA9tsk27wYi3uq0fPcK` — **Stuart**: Professional & friendly Aussie, ideal for technical assistance — great for NZ/AU trades
- `L0Dsvb3SLTyegXwtm47J` — **Archer**: Grounded and friendly young British male
- `PT4nqlKZfc06VW1BuClj` — **Angela**: Raw and relatable, great listener, down to earth — good for carpet cleaning/residential
- `g6xIsTj2HwM6VR4iXFCw` — **Jessica Anne Bogart**: Empathetic and expressive — good for pest control (empathetic to distressed callers)

### Custom Voice Design

You can create custom voices from text descriptions via Voice Design:
- Define: age, accent (NZ/AU!), tone, pacing
- Can clone your own voice (requires voice cloning plan)
- Voice clone = most authentic brand fit

---

## Prompt Length vs. Quality Trade-offs

| Prompt Length | Risk | Recommendation |
|---------------|------|----------------|
| < 200 words | Missing guardrails, incomplete flow | Too short for trade business |
| 300-600 words | Sweet spot for simple FAQ/lead-capture agents | Good starting point |
| 600-1200 words | Good for booking agents with multiple stages | Most trade agents live here |
| 1200-2000 words | Starts diluting attention on key rules | Only if needed |
| 2000+ words | Significant attention dilution; expensive | Use multi-agent design instead |

**Best practice**: Use the prompt for flow/personality/guardrails. Put business facts (services, pricing, FAQs) in the knowledge base. Keeps prompt tight and facts updatable.

---

## Multi-Agent Orchestration

For complex businesses, use agent transfer:

```
Main Agent (receptionist) 
  → detects need for specialist
  → transfers to: Booking Specialist / Pricing Specialist / Emergency Agent
  → each specialist has a smaller, tighter prompt
```

Each agent loads only its relevant prompt. Much cheaper per interaction and more reliable than one huge prompt.

Available tools: `agent_transfer` (system tool — configure destination agent IDs)

---

## Data Collection & Analysis (Post-Call Intelligence)

ElevenLabs has a built-in **Analysis** tab per agent:

### Success Evaluation
Define custom criteria to assess call quality:
- Did the agent collect all required info?
- Was the caller satisfied?
- Was the booking completed?

Set up evaluation criteria, and ElevenLabs runs LLM analysis on every call transcript automatically.

### Data Collection
Extract specific structured fields from conversations automatically:
- Extract: caller name, phone, service requested, sentiment, call outcome
- Available in API: `GET /v1/convai/conversations` with `data_collection_params` filter

This means you can query your API to pull all leads from a date range directly without post-call webhook.

---

## Pro Tips from Official Docs

1. **"This step is important."** literally increases model attention on that instruction
2. Tone guidance should only appear ONCE — in `# Personality` or `# Tone`. Avoid repeating throughout prompt.
3. Don't tell the agent what tool errors look like — tell it what to SAY to the caller when something goes wrong
4. For voice: write how you speak, not how you write. Read your prompt aloud — if it sounds awkward, it will sound awkward when spoken
5. Write the exact first line the agent should say. Don't leave it to the LLM to improvise the greeting.
6. Test edge cases: angry callers, "I'll call back", "I need to speak to someone", "what's your cheapest price" — these are the scenarios that expose gaps
# ElevenLabs Tools, Webhooks & External Integrations

*Researched: March 2026*

---

## Overview

ElevenLabs agents can trigger external actions during conversations. There are four types:

| Type | What it does | Who handles it |
|------|-------------|----------------|
| **Server tools** | Agent calls your webhook/API mid-conversation | Your server |
| **Client tools** | Agent triggers action in the browser/app | Frontend code |
| **System tools** | Built-in platform tools (end call, transfer) | ElevenLabs |
| **Post-call webhooks** | Data sent after call ends | Your server |

---

## 1. Server Tools (Webhooks — Mid-Conversation)

Agent calls an HTTP endpoint during the conversation. The call pauses, waits for a response, then continues.

### How they work
1. You define a tool in the agent dashboard (name, URL, method, parameters)
2. During conversation, LLM decides to use the tool (based on your prompt instructions)
3. Agent makes HTTP request to your endpoint
4. Your server processes and returns a JSON response
5. Agent continues conversation with the result

### Setting up a server tool

In the ElevenLabs dashboard:
- **Tool name**: e.g., `save_lead`, `check_availability`, `send_sms`
- **Method**: GET or POST
- **URL**: Your webhook endpoint
- **Headers**: Authentication (API key, bearer token, etc.)
- **Parameters**: Define fields the LLM will populate from the conversation

### Example: Save lead to CRM

Tool definition:
```json
{
  "name": "save_lead",
  "description": "Save caller details as a new lead",
  "method": "POST",
  "url": "https://your-server.com/webhook/new-lead",
  "parameters": {
    "name": {
      "type": "string",
      "description": "Caller's full name"
    },
    "phone": {
      "type": "string", 
      "description": "Phone number as digits only, e.g. '0211234567'"
    },
    "service_needed": {
      "type": "string",
      "description": "Description of the service needed"
    },
    "address": {
      "type": "string",
      "description": "Property address or suburb"
    },
    "preferred_time": {
      "type": "string",
      "description": "Preferred appointment time, e.g. 'Monday morning'"
    }
  },
  "required": ["name", "phone", "service_needed"]
}
```

Your server receives:
```json
{
  "name": "John Smith",
  "phone": "0211234567",
  "service_needed": "Carpet cleaning - 3 rooms + hallway",
  "address": "14 Example St, Takapuna",
  "preferred_time": "Saturday morning"
}
```

### Example: Check availability

```json
{
  "name": "check_availability",
  "method": "GET",
  "url": "https://your-server.com/api/availability",
  "parameters": {
    "date": {
      "type": "string",
      "description": "Date in YYYY-MM-DD format"
    }
  }
}
```

Response your server should return:
```json
{
  "available_slots": ["9am", "11am", "2pm"],
  "message": "We have openings at 9am, 11am, and 2pm on that day"
}
```

---

## 2. System Tools (Built-In)

### end_call
Hangs up the phone. Use in your prompt:
```
After completing the call, use the end_call tool to hang up.
```

### call_transfer
Transfers the call to another number. Configure in agent settings.

---

## 3. Client Tools

Used when the agent is embedded in a web/mobile app. The tool fires a JavaScript event in the browser instead of calling a server.

Good for:
- Showing a UI element (booking form, confirmation screen)
- Updating a display
- Triggering local app actions

Not relevant for phone-based business agents.

---

## 4. Post-Call Webhooks

Sent automatically after a call ends. Contains comprehensive call data.

### What's included in the payload
- Full conversation transcript
- Call duration
- Analysis results (if configured)
- Metadata (caller ID, agent ID, timestamp)
- Audio recording reference (if enabled)
- `has_audio`, `has_user_audio`, `has_response_audio` flags (added Aug 2025)

### Setting up post-call webhooks
1. Go to ElevenLabs dashboard → Settings → Webhooks
2. Add your endpoint URL
3. ElevenLabs signs each request — validate the signature on your server
4. Respond with HTTP 200 quickly (process async)

### Common post-call webhook uses
- Save full transcript to CRM
- Trigger follow-up SMS to caller
- Create task in job management software
- Send summary email to business owner
- Update customer record

### Example: Post-call webhook payload (simplified)
```json
{
  "event_type": "conversation.completed",
  "conversation_id": "conv_abc123",
  "agent_id": "agent_xyz",
  "started_at": "2026-03-22T09:00:00Z",
  "ended_at": "2026-03-22T09:04:32Z",
  "duration_seconds": 272,
  "transcript": [
    {"role": "agent", "text": "CleanRight Carpet Cleaning, this is Sarah, how can I help?"},
    {"role": "user", "text": "Hi, I'd like to get my carpets cleaned"},
    ...
  ],
  "analysis": {
    "outcome": "lead_captured",
    "caller_intent": "booking",
    "data_collected": {
      "name": "John Smith",
      "phone": "0211234567"
    }
  }
}
```

---

## 5. ElevenLabs Platform Webhooks (Admin Events)

Separate from agent webhooks. These notify you of platform-level events:
- Voice synthesis completion
- Audio generation events
- Agent status changes

Set up at: Settings → Webhooks in your ElevenLabs account.

---

## Authentication & Security

### Securing your webhook endpoints
Always authenticate incoming requests from ElevenLabs:

1. **Signature validation**: ElevenLabs signs webhook payloads — validate the HMAC signature
2. **API keys**: Add a shared secret to your tool's header (stored in ElevenLabs Secrets Manager)
3. **IP allowlisting**: Restrict your endpoint to ElevenLabs' IP ranges (enterprise)

### Using Secrets Manager
Store sensitive values (API keys, webhook URLs) in ElevenLabs' Secrets Manager:
- Navigate to Settings → Secrets Manager
- Create a secret (e.g., `MAKE_WEBHOOK_URL`, `CRM_API_KEY`)
- Reference in tool headers: `{{MAKE_WEBHOOK_URL}}`

This prevents exposing sensitive URLs or keys in plain text in your agent config.

---

## Tool Best Practices

### In your prompt
Tell the agent exactly when and how to use each tool:

```markdown
# Tools

## save_lead
Use this ONLY after you have collected AND confirmed all required information.
Required: name, phone, service_needed
Optional: address, preferred_time

Sequence:
1. Collect all information
2. Confirm back to caller: "Just to confirm — I have your name as [name], phone as [phone]..."
3. Only then call save_lead
4. After saving, tell caller: "Perfect, I've passed your details to our team."

If the tool fails, say: "I'm having a small technical issue. Could you call back on
[number] or I'll take a note and someone will call you right away."
```

### Parameter descriptions
Always include format expectations:
```
- phone: "Phone number as digits only, no spaces, e.g. '0211234567'"
- email: "Email in standard format, e.g. 'name@example.com'"
- date: "Date in YYYY-MM-DD format, e.g. '2026-03-25'"
```

### Error handling
LLMs can't gracefully handle tool failures without instructions:
```
# Tool Error Handling
If any tool call fails:
1. Do not tell the caller there was a system error
2. Say: "I'm just having a moment with that — let me make sure I have your details right."
3. Try once more
4. If still failing: "I'll make sure someone calls you back at [phone] within the hour."
```

---

## Practical Integration Patterns for Trade Businesses

### Pattern 1: Lead Capture Only
Simplest setup. No live lookups needed.

```
Call → Agent collects details → save_lead webhook → Make/Zapier workflow → CRM or Google Sheet
```

Tools needed: `save_lead` (POST webhook)

### Pattern 2: Lead Capture + SMS Confirmation
```
Call → Agent collects details → save_lead → webhook triggers → Make sends SMS to caller
```

Tools needed: `save_lead`, post-call webhook OR webhook triggers SMS in Make

### Pattern 3: Live Availability Check
```
Call → Agent asks preferred time → check_availability tool → Returns slots → Agent confirms
```

Tools needed: `check_availability` (GET), `save_booking` (POST)

### Pattern 4: Full Booking with Confirmation
```
Call → Agent collects info → check_availability → Confirm slot → save_booking → 
Post-call webhook → Send confirmation SMS/email
```

Most complex but most impressive for callers.

---

## Supported Integration Ecosystem

Via server tools (webhooks), agents can connect to anything with an API:

- **CRMs**: HubSpot, Salesforce, Pipedrive, Zoho
- **Job Management**: Jobber, ServiceM8, Tradify, simPRO
- **Calendars**: Google Calendar, Calendly, Acuity
- **SMS**: Twilio SMS, MessageBird, Vonage
- **Email**: Mailgun, SendGrid, Postmark
- **Sheets**: Google Sheets (via Make or direct API)
- **Notifications**: Slack, Telegram
- **Automation**: Make, Zapier, n8n
# ElevenLabs + Make (Integromat) Integration Guide

*Researched: March 2026*

---

## Why Make + ElevenLabs?

ElevenLabs handles the conversation. Make handles everything that happens because of it.

When a voice agent collects information (caller name, job details, phone number), Make turns that into action:
- Create a record in your CRM
- Send a confirmation SMS
- Add a row to Google Sheets
- Create a task in your job management app
- Notify the business owner on Slack
- Send a follow-up email
- Update a calendar

Make's 1,500+ app connectors mean you don't need to code custom integrations — just build a visual workflow.

---

## Two Integration Patterns

### Pattern A: Agent → Make (During Call)
The agent calls a Make webhook **during** the conversation. This is for real-time actions where the result affects the call (e.g., availability checking, looking up customer details).

**Flow:**
```
Caller speaks → Agent understands request → Agent calls Make webhook → 
Make runs workflow → Returns data → Agent continues conversation
```

**Latency consideration**: Make workflows add response time. For real-time use, keep Make scenarios simple and fast. Avoid long chains during live calls.

### Pattern B: ElevenLabs → Make (Post-Call)
ElevenLabs sends call data to Make **after the call ends**. This is for most business use cases — processing, saving, notifying.

**Flow:**
```
Call ends → ElevenLabs post-call webhook → Make catches it → 
Make processes transcript → Creates CRM record + sends SMS + updates sheet
```

**This is the most common and practical pattern for small trade businesses.**

---

## Setup: Make Scenario as Webhook Target (Agent Tool)

### Step 1: Create Make Scenario

1. Log into Make (make.com)
2. Create a new Scenario
3. Add **Webhooks → Custom Webhook** as the trigger
4. Click **Add** → copy the webhook URL
5. Add your workflow modules (what should happen)
6. In the final module, add a **Webhooks → Webhook Response** module (returns data to ElevenLabs)
7. Activate the scenario

### Step 2: Store the URL in ElevenLabs

1. Go to ElevenLabs dashboard → Settings → Secrets Manager
2. Create secret: `MAKE_WEBHOOK_URL` = paste your Make webhook URL
3. (Optional) Create `MAKE_API_KEY` if your scenario requires auth

### Step 3: Configure Tool in ElevenLabs

Create a new server tool in your agent:

```
Name: save_lead_to_crm
Method: POST
URL: {{MAKE_WEBHOOK_URL}}
Headers:
  Content-Type: application/json
  (Optional) X-API-Key: {{MAKE_API_KEY}}

Parameters:
  caller_name (string): "Caller's full name"
  phone (string): "Phone number as digits, e.g. '0211234567'"
  service_needed (string): "Description of service requested"
  address (string): "Property address or suburb"
  preferred_time (string): "Preferred appointment time"
  notes (string): "Any other notes from the conversation"
```

### Step 4: Add to Agent System Prompt

```markdown
# Tools

## save_lead_to_crm
Use this tool after collecting all caller information.
Call this ONLY when you have:
- Caller name ✓
- Phone number ✓  
- Service needed ✓
After calling, confirm to the caller: "I've passed your details to our team."
```

---

## Make Scenario Examples

### Scenario 1: New Lead → Google Sheets + SMS

**Trigger**: Webhook (from ElevenLabs tool call)

**Modules**:
1. Webhooks → Custom Webhook (trigger)
2. Google Sheets → Add a Row
   - Spreadsheet: "CleanRight Leads"
   - Sheet: "New Leads"
   - Columns: Date/Time, Name, Phone, Service, Address, Preferred Time
3. Twilio → Send SMS
   - To: `{{phone}}`
   - Message: "Hi {{caller_name}}, thanks for calling CleanRight! We'll be in touch within 2 hours to confirm your booking. - Sarah"
4. Webhooks → Webhook Response
   - Status: 200
   - Body: `{"success": true, "message": "Lead saved successfully"}`

---

### Scenario 2: Post-Call Webhook → Full Processing

**Trigger**: Webhooks → Custom Webhook (from ElevenLabs post-call webhook)

**Modules**:
1. Webhooks → Custom Webhook
2. JSON → Parse JSON (parse the transcript/analysis)
3. Router (branch based on call outcome):
   - Branch A: Lead captured → Save to HubSpot + Send SMS
   - Branch B: Existing customer → Update record + Send email  
   - Branch C: No useful info → Log and ignore
4. HubSpot → Create Contact (Branch A)
5. Twilio → Send SMS (Branch A)
6. Webhook Response → 200 OK

---

### Scenario 3: Availability Check (Real-Time During Call)

**Trigger**: Webhook

**Modules**:
1. Webhooks → Custom Webhook (receives: `{"date": "2026-03-25"}`)
2. Google Calendar → Search Events (check if date has bookings)
3. Custom function to determine available slots
4. Webhooks → Webhook Response
   - Body: `{"available_slots": ["9am", "11am", "2pm"], "message": "We have slots at 9am, 11am and 2pm on that day"}`

---

### Scenario 4: Inbound Call Summary Email to Owner

**Trigger**: ElevenLabs post-call webhook

**Modules**:
1. Custom Webhook (receives call data)
2. Tools → Set Variable (format transcript summary)
3. Gmail → Send Email
   - To: owner@business.com
   - Subject: "New call: {{caller_name}} - {{service_needed}}"
   - Body: Full transcript + caller details
4. Webhook Response → 200

---

## Handling Make's Response in ElevenLabs

When ElevenLabs calls a Make webhook as a tool, Make should return a structured response:

```json
{
  "success": true,
  "message": "Lead saved. Reference number BK2026-0089",
  "next_steps": "Our team will call back within 2 hours"
}
```

The agent uses this response in its reply. Your system prompt should tell it what to do with tool responses:

```
After save_lead_to_crm returns successfully:
- Tell the caller: "Perfect, I've saved your details. [message from response]"
- If response contains a reference number, read it out to the caller.
```

---

## Authentication Options

### Option 1: No auth (simple, webhook URL is secret)
- Fine for low-risk uses
- Make webhook URL should be treated as a secret (use Secrets Manager)

### Option 2: Custom header token
- Make scenario checks for `X-Webhook-Secret` header
- Add header in ElevenLabs tool config referencing a secret
- Make uses a filter at the start: `X-Webhook-Secret` must equal your stored value

### Option 3: HMAC signature validation
- More secure but requires custom Make code (HTTP module + custom function)
- Recommended for scenarios that write sensitive data

---

## Troubleshooting Common Issues

### Webhook Timeout Errors
- Make scenarios have a 40-second timeout
- During live calls, aim for < 5 second response time
- For slow workflows, use async pattern (return 200 immediately, process in background)
- Consider separating real-time (fast) and post-call (can be slow) scenarios

### Authentication Failures
- Verify secret names match exactly (case-sensitive)
- Check secret is stored in ElevenLabs Secrets Manager (not just in the tool config)
- Test with a Make webhook inspector first (before connecting to ElevenLabs)

### Data Formatting Issues
- Phone numbers come as spoken form if using system_prompt normalisation
  ("zero two one one...") — handle parsing in Make
- Add a Tools → Text Parser module to clean up phone numbers
- Date/time values need explicit format instructions in your agent prompt

### Missing Required Fields
- If a required parameter is empty, tool call may fail silently
- Add fallback handling in Make: check if field is empty, use a default
- In ElevenLabs prompt: explicitly instruct agent not to call the tool until all required fields are collected

---

## Make + ElevenLabs: Best Practices for Trade Businesses

1. **Keep real-time scenarios lean** — fewer modules = faster response during live call
2. **Use post-call webhooks for heavy processing** — saves CRM, sends emails, updates sheets
3. **Test with Make's webhook inspector** before connecting to ElevenLabs
4. **Store all webhook URLs in Secrets Manager** — don't expose them in plain text
5. **Build in error handling** — what happens if Make is down? Agent should have a fallback message
6. **Log everything initially** — write all calls to a Google Sheet for the first week to audit quality
7. **Use routers for conditional logic** — different outcomes for different call types
8. **Don't over-engineer Day 1** — start with "save lead to sheet + send SMS", add complexity gradually

---

## Minimal Viable Setup (Start Here)

For a trade business just getting started:

**ElevenLabs agent** → calls `save_lead` tool → **Make webhook** → adds row to Google Sheet + sends SMS to caller + sends email to owner

That's it. That's genuinely useful from Day 1.

Make scenario = 4 modules. Takes 20 minutes to set up.

Upgrade later to: CRM records, job management integration, calendar booking, etc.
# Advanced Make + ElevenLabs Integration Patterns

*Deep research: March 2026*

---

## Architecture Decision: Mid-Call vs. Post-Call

Before building any Make scenario, decide where processing happens:

| Decision | Mid-Call Tool | Post-Call Webhook |
|----------|---------------|-------------------|
| **Time limit** | < 5 seconds ideally | Unlimited |
| **Failure impact** | Breaks conversation | Doesn't affect caller |
| **Use case** | Availability check, CRM lookup | Save lead, analytics, follow-up |
| **Complexity** | Keep minimal | Can be complex |
| **Retry on failure** | No automatic retry | No retry (ElevenLabs limitation) |
| **Return data to agent** | Yes — agent uses the response | No — call is over |

**Rule of thumb**: If you need to return data to the agent during the call → mid-call tool. Everything else → post-call webhook.

---

## Pattern 1: Simple Lead Capture (Start Here)

**Use case**: Agent collects caller details → saves to Google Sheet + sends SMS confirmation + emails owner

**Make scenario structure:**
```
[Trigger] Custom Webhook
    ↓
[Google Sheets] Add a Row
    ↓
[Twilio SMS] Send to Caller
    ↓
[Gmail] Send to Owner
    ↓
[Webhook Response] 200 OK
```

**Make modules in detail:**

**Module 1 — Custom Webhook:**
- Method: POST
- URL: Auto-generated by Make
- Store in ElevenLabs Secrets Manager
- Expected input: `{name, phone, service_needed, address, preferred_time, notes}`

**Module 2 — Google Sheets → Add a Row:**
- Spreadsheet: "Leads - [Business Name]"
- Sheet: "Raw Leads"
- Column mapping:
  - A: `{{1.timestamp}}` (auto-generated in Make)
  - B: `{{1.name}}`
  - C: `{{1.phone}}`
  - D: `{{1.service_needed}}`
  - E: `{{1.address}}`
  - F: `{{1.preferred_time}}`
  - G: `{{1.notes}}`
  - H: "New" (static status)

**Module 3 — Twilio → Send SMS:**
- To: `{{1.phone}}`
- From: Your Twilio number
- Body: `Hi {{1.name}}, thanks for calling [Business]! We'll be in touch within 2 hours to confirm your booking. Any questions? Call us on [number].`

**Module 4 — Gmail → Send Email:**
- To: `owner@business.com`
- Subject: `New enquiry: {{1.name}} — {{1.service_needed}}`
- Body:
  ```
  New lead received from voice agent:
  
  Name: {{1.name}}
  Phone: {{1.phone}}
  Service: {{1.service_needed}}
  Address: {{1.address}}
  Preferred time: {{1.preferred_time}}
  Notes: {{1.notes}}
  Timestamp: {{1.timestamp}}
  
  Action needed: Call back within 2 hours.
  ```

**Module 5 — Webhook Response:**
- Status: 200
- Body: `{"success": true, "message": "Lead saved successfully"}`

---

## Pattern 2: Availability Check (Real-Time During Call)

**Use case**: Caller asks about a specific date → agent checks Google Calendar → returns available slots

**Critical constraint**: This must respond in < 5 seconds. Keep it lean.

**Make scenario:**
```
[Trigger] Custom Webhook → receives {date: "2026-03-25"}
    ↓
[Google Calendar] Search Events 
    (search for date = requested date, calendar = bookings calendar)
    ↓
[Tools] Set Multiple Variables
    (determine available slots based on what's booked)
    ↓
[Webhook Response] Return available slots
```

**Response format for ElevenLabs:**
```json
{
  "available_slots": ["9am", "11am", "2pm"],
  "message": "We have openings at 9am, 11am and 2pm on that day. Which works best for you?"
}
```

**In your system prompt:**
```markdown
## check_availability tool
Use when caller asks about specific dates.
Input: date (YYYY-MM-DD)
After receiving response:
- If slots available: read out the available times
- If no slots: "We're fully booked on that day. The next available day is [suggest checking another date]."
```

**Performance tip**: If Google Calendar search is too slow, consider maintaining a simple JSON "availability" file in Google Drive and reading that instead. Much faster response time.

---

## Pattern 3: Post-Call Webhook — Full Processing Pipeline

**Use case**: Every call → parse transcript → route based on outcome → create CRM record + send follow-up

**Make scenario:**
```
[Trigger] Custom Webhook (ElevenLabs post-call)
    ↓
[Tools] Set Variable: Extract call outcome from analysis
    ↓
[Router] Branch based on outcome:
    ├── Branch A: Lead captured → Create HubSpot contact + Send SMS
    ├── Branch B: Existing customer inquiry → Update CRM + Log note
    ├── Branch C: Emergency → Send urgent SMS to owner + Create priority ticket
    └── Branch D: No useful data → Log to "Review" sheet
    ↓
[Webhook Response] 200 OK
```

**Parsing the ElevenLabs payload:**

The post-call webhook sends a rich payload. In Make, access fields like:
```
{{body.data.transcript[].message}}  — all transcript messages
{{body.data.metadata.phone_call.external_number}}  — caller's phone
{{body.data.analysis.data_collection_results.caller_name.value}}  — extracted name
{{body.data.analysis.data_collection_results.caller_phone.value}}  — extracted phone
{{body.data.duration_seconds}}  — call length
```

**Module: Router conditions**
```
Branch A: {{body.data.analysis.data_collection_results.caller_phone.value}} exists
Branch B: {{body.data.analysis.evaluation_criteria_results.existing_customer.result}} = "success"
Branch C: {{body.data.analysis.evaluation_criteria_results.emergency_detected.result}} = "success"
Branch D: Default (all other cases)
```

---

## Pattern 4: CRM Lookup on Inbound Call (Real-Time)

**Use case**: When call starts, look up caller in CRM, inject their history into agent context

This uses ElevenLabs' **Twilio Personalization** feature:

1. Enable "Fetch conversation initiation data" in agent Security tab
2. Configure your initiation webhook URL (a Make webhook)
3. When inbound call arrives, ElevenLabs POSTs to your Make webhook BEFORE starting conversation

**Make scenario for CRM lookup:**
```
[Trigger] Custom Webhook → receives {caller_id: "+6421987654", agent_id: "..."}
    ↓
[HubSpot/Google Sheets] Search for caller by phone
    ↓
[Router]:
    ├── Found: Return customer data as dynamic variables
    └── Not found: Return "new_caller: true"
    ↓
[Webhook Response] Return dynamic variables
```

**Response format:**
```json
{
  "dynamic_variables": {
    "customer_name": "John Smith",
    "last_service_date": "2025-12-01",
    "last_service_type": "carpet cleaning",
    "total_jobs": "3",
    "is_vip": "true"
  }
}
```

**In system prompt:**
```markdown
{{#customer_name}}
The caller is {{customer_name}}, a returning customer. 
Their last service was {{last_service_type}} on {{last_service_date}}.
Greet them by name and acknowledge their loyalty if they've had 3+ jobs.
{{/customer_name}}
```

---

## Pattern 5: Transcript Analysis + Follow-Up Automation

**Use case**: After call, AI summarises what was discussed and triggers appropriate follow-up

**Make scenario:**
```
[Trigger] Custom Webhook (post-call)
    ↓
[OpenAI] Analyse transcript → extract action items
    ↓
[Router] Based on analysis:
    ├── Caller wanted quote → Create Google Calendar event for quote callback
    ├── Caller had complaint → Create Trello/Asana task for owner
    └── Booking confirmed → Send booking confirmation SMS
    ↓
[Webhook Response] 200 OK
```

**Note**: You can also use ElevenLabs' built-in Analysis features (data collection + evaluation) to do this without OpenAI — configure the criteria in the agent dashboard and they appear in the post-call payload.

---

## Error Handling in Make — Complete Guide

### The 5 Error Handlers

Make has 5 error handlers; choose based on what you need:

1. **Break** — Stop execution, save to Incomplete Executions queue for retry. Best for transient failures (API timeout, rate limit).
2. **Resume** — Continue with a fallback value. Use when error is non-critical and you don't want to stop.
3. **Ignore** — Skip the error and keep going. Use with caution — only when an error truly doesn't matter.
4. **Commit** — Save progress so far and stop cleanly. Use after successful partial processing.
5. **Rollback** — Undo everything and stop. Use for transactional operations.

### For ElevenLabs Integrations

**Critical settings for ElevenLabs-linked scenarios:**

1. **Enable "Allow storing of incomplete executions"** — Required for Break handler. Saves failed runs so you can fix and retry without data loss.
2. **Sequential processing** — Enable when order matters (e.g., CRM updates must be sequential).
3. **Max consecutive errors**: Default 3 — prevents runaway loops.

### Break + Retry Pattern (Most Important)

For any external API call (Twilio, HubSpot, etc.):

```
[HTTP Module] or [Twilio/HubSpot Module]
    ↓ (on error)
[Break Handler]
    → Max retries: 3
    → Retry interval: 10 minutes (exponential: 10min, 30min, 90min)
    → Falls into Incomplete Executions if all retries fail
```

### Graceful Degradation — Return 200 Even on Failure

For webhook scenarios receiving ElevenLabs calls, **always return 200 quickly**:

```
[Trigger] Custom Webhook
    ↓
[Webhook Response Module] — MOVE TO TOP — return 200 immediately
    ↓
[Rest of your processing continues async]
```

But wait — Make processes sequentially. To return 200 before processing:
- **Option A**: Use a separate Make scenario — webhook triggers a second scenario via Make-to-Make HTTP call, returns 200 immediately, second scenario does the heavy work
- **Option B**: Keep mid-call scenario lean (< 5 seconds); only complex processing goes post-call

### Data Validation Pattern

Always validate before writing to CRM:

```
[Trigger] Webhook
    ↓
[Filter] Phone number not empty + name not empty
    ↓ (if valid)
[Continue to CRM]

    ↓ (if invalid — separate route)
[Google Sheets] Log to "Review" sheet
[Gmail] Send alert to owner: "Call received but data incomplete — review manually"
```

### Handling Phone Number Formats

ElevenLabs may deliver phone numbers in different formats depending on normalisation setting:

```
System prompt normalisation: "zero two one one two three four five six seven"
ElevenLabs normalisation: "+64211234567"  
```

**Clean up in Make with a Text function:**
```
# Replace everything except digits and +
{{replace(1.phone, "[^0-9+]", "")}}

# Or use a regex to extract NZ mobile
{{match(1.phone, "[0-9]{9,11}")}}
```

**Better approach**: Specify format in your tool parameter description so the LLM formats it correctly:
```
phone: "Phone number as digits only, no spaces or dashes, e.g. '0211234567'"
```

---

## Make Scenario Performance Optimisation

### Keeping Real-Time Scenarios Fast

For mid-call tools (< 5 second requirement):

1. **Minimise modules** — each module adds 200-500ms
2. **Avoid sequential API calls** — parallelize where possible
3. **Use Make Data Stores** instead of Google Sheets for fast lookups (much faster than Sheet API)
4. **Pre-populate static data** in Make Data Store (service areas, pricing) for instant access
5. **Cache CRM results** — if looking up same phone number again within an hour, return cached result
6. **Set aggressive timeouts** — don't wait for slow APIs; fail fast and return fallback

### Webhook Response Caching (Advanced)

For availability checks, cache the response in a Make Data Store:
```
[Receive request for date]
    ↓
[Check Data Store] — do we have a cache for this date (< 5 min old)?
    ├── Yes: return cached response immediately
    └── No: fetch Google Calendar, store in cache, return result
```

---

## Google Sheets Lead Database — Production Setup

For a production trades business lead sheet:

**Sheets structure:**
1. **Raw Leads** — append-only, all incoming leads
2. **Active Leads** — filtered view (status = New, In Progress)
3. **Completed** — filter/archived
4. **Analytics** — summary charts

**Columns for Raw Leads:**
```
A: Timestamp (auto-filled by Make)
B: Caller Phone (from metadata.phone_call.external_number OR from tool call)
C: Caller Name (from tool call)
D: Address/Suburb
E: Service Needed
F: Preferred Time
G: Notes
H: Call Duration (seconds)
I: Conversation ID (for transcript lookup)
J: Status (New / Contacted / Booked / Not Available)
K: Owner Notes
```

**Important**: Always capture `conversation_id` — this lets you pull the full transcript via API if needed for dispute resolution or quality review.

---

## Advanced Make Blueprint for ElevenLabs

Here's a JSON structure you can use to document your Make blueprint logic (for sharing with team):

```json
{
  "blueprint_name": "ElevenLabs Trades Lead Capture",
  "trigger": {
    "type": "webhook",
    "url": "STORED_IN_ELEVENLABS_SECRETS",
    "auth": "X-Webhook-Secret header"
  },
  "modules": [
    {
      "order": 1,
      "type": "google-sheets-add-row",
      "config": "Write to Raw Leads sheet",
      "error_handler": "Resume with empty values if sheet API fails"
    },
    {
      "order": 2,
      "type": "filter",
      "condition": "phone_number is valid AND name is not empty"
    },
    {
      "order": 3,
      "type": "twilio-sms",
      "config": "Send confirmation to caller",
      "error_handler": "Break with 3 retries (SMS failure non-critical for data)"
    },
    {
      "order": 4,
      "type": "gmail-send",
      "config": "Send notification to owner",
      "error_handler": "Break with 3 retries"
    },
    {
      "order": 5,
      "type": "webhook-response",
      "config": "200 OK with success JSON"
    }
  ],
  "error_settings": {
    "incomplete_executions": true,
    "sequential_processing": false,
    "max_consecutive_errors": 5
  }
}
```

---

## Make Monitoring & Alerting

### Set Up Execution History

Make keeps execution history. Review regularly (especially first month):
- Scenario → History → See each execution, duration, bundles processed, errors

### Build an Alert Scenario

Create a separate "Meta-monitoring" scenario:
```
[Trigger] Webhook (Make built-in error notification endpoint)
    ↓
[Slack / Gmail] "⚠️ Make scenario failed: [scenario name], error: [details]"
```

Or: Enable email notifications in Make Settings → Notifications.

### Weekly Health Report Scenario

```
[Trigger] Schedule — every Monday 9am
    ↓
[Google Sheets] Count leads from past week
    ↓  
[Gmail] Send weekly summary to owner:
    "Week of [date]: [X] leads captured, [X] bookings, [X] follow-up needed"
```

---

## Complete Make Integration Checklist

**Before going live:**
- [ ] Webhook URL stored in ElevenLabs Secrets Manager (not in plain text in tool config)
- [ ] Webhook authentication configured (X-Webhook-Secret header)
- [ ] Make scenario handles missing/empty fields gracefully
- [ ] Phone number parsing handles multiple formats
- [ ] SMS confirmation message sounds natural and has business name
- [ ] Owner email notification has all needed info
- [ ] Google Sheet has correct column structure
- [ ] Error handlers configured on all external modules (Twilio, Gmail, Sheets)
- [ ] Incomplete executions enabled in scenario settings
- [ ] Scenario tested with all fields populated
- [ ] Scenario tested with missing optional fields
- [ ] Scenario tested with phone number in different formats
- [ ] Webhook response returns 200 with success JSON

**After going live (week 1):**
- [ ] Review Make execution history daily
- [ ] Check for any failed executions
- [ ] Verify Google Sheet is populating correctly
- [ ] Call test from real phone and confirm SMS received
- [ ] Confirm owner email notification format looks good
- [ ] Check that conversation_id is being captured (for transcript lookup)
# ElevenLabs Knowledge Bases — Setup, Structure & Best Practices

*Researched: March 2026*

---

## What Is a Knowledge Base?

A knowledge base is domain-specific information attached to an agent. Instead of stuffing all info into the system prompt, you give the agent access to documents it can reference during conversations.

**Use cases:**
- Product/service catalogs with pricing
- FAQ documents
- Service area lists
- Business policies
- Onboarding materials
- Technical specs
- Terms and conditions

---

## How to Add Content

### Via Dashboard (no-code)
Three input methods:

1. **File Upload**
   - Formats: PDF, TXT, DOCX, HTML, EPUB
   - Size limit: 21 MB per file (non-enterprise)
   - Best for: static reference docs, service guides

2. **URL Import**
   - Paste a URL (e.g., your pricing page, FAQ page)
   - Scrapes content at time of import
   - ⚠️ Does NOT continuously update — it's a snapshot
   - ⚠️ Does NOT scrape linked pages (only the page you provide)
   - Coming soon: automatic updates and linked-page scraping

3. **Manual Text**
   - Type or paste text directly
   - Good for custom Q&A pairs, business facts

### Via API

```python
# Create from text
doc = elevenlabs.conversational_ai.knowledge_base.documents.create_from_text(
    text="Our standard carpet cleaning starts at $80 per room.",
    name="Pricing Overview",
)

# Create from URL
doc = elevenlabs.conversational_ai.knowledge_base.documents.create_from_url(
    url="https://yoursite.com/faq",
    name="FAQ Page",
)

# Create from file
doc = elevenlabs.conversational_ai.knowledge_base.documents.create_from_file(
    file=open("services.pdf", "rb"),
    name="Services Guide",
)

# Attach to agent
elevenlabs.conversational_ai.agents.update(
    agent_id="your-agent-id",
    conversation_config={
        "agent": {
            "prompt": {
                "knowledge_base": [
                    {"type": "text", "name": doc.name, "id": doc.id}
                ]
            }
        }
    }
)
```

---

## RAG (Retrieval-Augmented Generation)

RAG allows agents to access large knowledge bases that wouldn't fit in the context window.

### How it works
1. User's question is analysed and reformulated for retrieval
2. Query converted to vector embedding
3. Most semantically similar content is retrieved from your knowledge base
4. Agent generates response using conversation context + retrieved content

### Key specs
- Adds ~500ms latency per query
- Query rewriting: sub-200ms
- Documents smaller than 500 bytes cannot use RAG (auto-injected into prompt instead)

### Enabling RAG
1. Go to agent settings → Knowledge Base section
2. Toggle on **Use RAG**
3. Configure in Advanced tab:
   - **Embedding model**: Select model for vector embeddings
   - **Maximum document chunks**: How much content retrieved per query
   - **Maximum vector distance**: Relevance threshold (higher = more results, less relevant)

### Document usage modes (per document)
- **Auto (default)**: Retrieved only when relevant
- **Prompt**: Always included in system prompt AND retrievable by RAG
  - ⚠️ Don't set too many documents to Prompt mode — can exceed context limits

### RAG size limits by plan
| Plan | Max RAG document size |
|------|----------------------|
| Free | 1 MB (indexes deleted after inactivity) |
| Starter | 2 MB |
| Creator | 20 MB |
| Pro | 100 MB |
| Scale | 500 MB |
| Business | 1 GB |
| Enterprise | 1 GB+ (negotiated) |

### When to use RAG vs direct injection
| Situation | Recommendation |
|-----------|----------------|
| Document < 3,000 tokens | Direct injection (faster, simpler) |
| Document > 3,000 tokens | Enable RAG |
| Multiple large documents | RAG — only relevant snippets retrieved |
| Critical always-needed info | "Prompt" mode — always injected |
| Large product catalog | RAG |
| Short FAQ (10 items) | Direct injection in prompt |

---

## Non-RAG Knowledge Base Limits

Non-enterprise accounts:
- Maximum **20 MB** total OR **300,000 characters** per agent
- Enterprise: contact sales for expanded limits

---

## Best Practices for Knowledge Base Content

### 1. Structure clearly
Good knowledge base content is scannable and explicit. Don't rely on the agent to infer — state facts clearly.

**Bad:**
> Our pricing depends on the job

**Good:**
> Standard carpet cleaning prices:
> - 1 room: $80
> - 2 rooms: $140
> - 3 rooms: $190
> - Full house (4+ rooms): call for quote
> Prices include pre-treatment and deodoriser. Stairs are charged separately at $2 per step.

### 2. Break large documents into focused pieces
Instead of one 50-page PDF, create:
- `Pricing Guide.txt`
- `Service Areas.txt`
- `What to Expect.txt`
- `Pest Types and Treatments.txt`
- `FAQ.txt`

This improves RAG retrieval precision.

### 3. Use plain language
Avoid jargon in knowledge base documents — the agent reads them and mirrors the language it finds.

### 4. Update regularly
Set a calendar reminder to review knowledge base documents monthly. Outdated pricing or policy info will be confidently stated by the agent as fact.

### 5. Cover FAQ topics explicitly
Review call transcripts to find what callers ask. Add answers for:
- What areas do you service?
- How long does it take?
- Do I need to move furniture?
- What's the difference between your packages?
- Are you pet safe?
- Do you have a guarantee?

### 6. Identify knowledge gaps
Monitor conversation transcripts. When the agent says "I'm not sure about that" repeatedly on a topic — add that info to the knowledge base.

### 7. Test with real questions
After setting up the knowledge base, test with questions your real customers would ask. Check if the answers are accurate and well-phrased.

---

## Example: Knowledge Base for Pest Control Business

### Document 1: Services and Pricing (Text)
```
SERVICES AND PRICING

General Pest Treatment (cockroaches, ants, spiders, silverfish)
- 3-bedroom home: $180
- 4-bedroom home: $220
- Commercial: call for quote
Includes: spray treatment inside and outside, 6-month warranty

Rodent Control
- Inspection and baiting: from $250
- Includes 2 follow-up visits
- 3-month warranty

Wasp Nest Removal
- Single nest: $120
- Includes same-day removal (subject to availability)

Flea Treatment
- Up to 3 bedrooms: $160
- Includes pre-treatment advice (vacuuming instructions sent by email)
```

### Document 2: Service Areas (Text)
```
SERVICE AREAS
We service all suburbs of Auckland including:
North Shore: Takapuna, Devonport, Glenfield, Albany, Orewa
West Auckland: Henderson, New Lynn, Titirangi
Central: CBD, Ponsonby, Mt Eden, Epsom, Remuera
East Auckland: Howick, Pakuranga, Botany, Flat Bush
South Auckland: Manukau, Papatoetoe, Papakura, Pukekohe

We do NOT currently service: Waiheke Island, Northland
```

### Document 3: FAQ (Text)
```
FREQUENTLY ASKED QUESTIONS

Q: Is your treatment safe for children and pets?
A: Yes. We use EPA-approved products. We ask that children and pets stay out of 
treated areas for 2-4 hours after treatment.

Q: How long does a general pest treatment take?
A: Approximately 45-90 minutes depending on home size.

Q: Do I need to be home during treatment?
A: It's preferred but not required for outside treatments. Inside access 
requires someone to be present.

Q: How soon can I book?
A: We typically have availability within 2-3 business days. Urgent jobs 
may be accommodated depending on schedule.

Q: Do you offer a warranty?
A: Yes. General pest treatments include a 6-month warranty. If pests return 
within the warranty period, we retreat at no charge.
```

---

## Attaching Multiple Knowledge Bases to One Agent

An agent can have multiple knowledge base documents attached. RAG retrieves across all of them simultaneously.

Good pattern for a trade business:
- Core: Services + Pricing
- Secondary: FAQ
- Reference: Service Areas
- Reference: Seasonal advice (e.g., "summer ant prevention")

Keep each document focused on a single topic. Mixing topics in one document reduces retrieval accuracy.
# ElevenLabs Conversational AI — Gotchas, Limits & Things to Avoid

*Researched: March 2026*

---

## Pricing & Billing Gotchas

### LLM costs not included (yet)
- Conversational AI per-minute pricing does NOT include LLM costs
- ElevenLabs is currently absorbing LLM fees — but says it "will eventually pass those costs on"
- Monitor this: if LLM costs get added, your per-minute cost could significantly increase
- Enterprise/Business plans may have different terms — ask sales

### Telephony costs are extra
- Twilio phone number: ~$1.15/month
- Twilio call charges: ~$0.0085/minute for inbound (US), more for international
- New Zealand Twilio rates vary — check current pricing
- Total cost = ElevenLabs per-minute + Twilio per-minute + Twilio number rental

### Concurrency limits can kill you at scale
- Free: 2 concurrent calls
- Starter: 3
- Creator: 5
- If you go over your limit, calls are dropped or queued
- Surge capacity (3× limit at double rate) is opt-in — enable it for busy periods
- Small trade business with 3–5 simultaneous calls: Creator plan is fine
- Busy multi-location business: May need Pro (10) or Scale (15)

### Credits vs. per-minute billing
- TTS characters use credit allocation
- Conversational AI is billed separately per-minute
- Don't confuse "I have credits left" with "I can make calls" — they're different budgets

---

## Knowledge Base Gotchas

### URL scraping is a snapshot, not live
- When you import a URL, it captures content ONCE at that moment
- If your pricing page changes, the agent still has the old info
- No automatic updates (feature is "coming soon")
- **Fix**: Set a monthly reminder to re-import URLs that change frequently

### No linked-page scraping
- Importing `yoursite.com/faq` does NOT also scrape `yoursite.com/services`
- Each page must be added individually
- **Fix**: Import each relevant page separately, or create a text document with all info

### 20 MB / 300k character limit (non-enterprise)
- Most small businesses won't hit this
- But large PDF manuals or extensive catalogs can get close
- **Fix**: Convert to focused plain text documents (much more token-efficient)

### RAG adds ~500ms latency
- If your agent needs to look up knowledge base on every turn, calls feel slower
- **Fix**: Put frequently-needed info directly in the system prompt; only use RAG for large reference docs

### Free plan RAG indexes get deleted after inactivity
- If you're on Free and don't have calls for a while, your RAG index may be cleared
- **Fix**: Re-index before important periods, or upgrade to a paid plan

---

## Prompting Gotchas

### LLMs ask multiple questions at once
- LLMs default to gathering information efficiently — which means dumping all questions at once
- This sounds overwhelming in voice
- **Fix**: Explicitly say in prompt: "Ask ONE question at a time. This step is important."

### Number/symbol pronunciation issues
- "123" → "one hundred and twenty three" (not "one, two, three")
- Email addresses get mangled if not handled
- **Fix**: Use ElevenLabs normaliser OR give explicit instructions about format
- For tool inputs: specify format in parameter descriptions ("digits only, e.g. '0211234567'")

### Agents hallucinate when they don't know something
- Without a knowledge base, agents will make up answers
- **Fix**: Add guardrail: "If you don't know, say 'I'm not sure about that — let me have the team call you back'"

### System prompt length vs. performance
- Very long system prompts can dilute attention on critical rules
- **Fix**: Keep prompt focused. Use sections. Put critical rules in `# Guardrails`. Repeat the most important 1-2 rules twice.

### Tone instructions don't stick without explicit formatting guidance
- "Be friendly" is not enough
- **Fix**: Write the actual first sentence the agent should say. Give example dialogue.

### Agent goes off-topic
- LLMs are curious and chatty — they'll discuss cooking recipes if asked
- **Fix**: Guardrail: "Only discuss topics related to [business name]'s services. Politely redirect off-topic conversations."

---

## Conversation Flow Gotchas

### Soft timeout default is disabled
- Without soft timeout, there's awkward silence while the LLM thinks
- **Fix**: Enable soft timeout with a 3-second delay and a natural filler like "Let me just check that..."
- Don't use time-specific fillers ("one moment" — because "one moment" could actually be 8 seconds)

### Interruption handling is tricky
- By default, users CAN interrupt the agent
- Good for natural conversation, bad for legal disclaimers
- **Fix**: Disable interruptions for any legally required full-read sections

### Turn timeout too short = agent talks over thinking customers
- Default is fine for most cases
- **Fix**: Use Patient mode or longer timeout (15-30s) when collecting detailed information like addresses

### Agent doesn't hang up gracefully
- Without explicit end_call tool instructions, agents sometimes just... keep talking
- **Fix**: Script the closing lines AND instruct it to use `end_call` tool after the farewell

---

## Tool & Webhook Gotchas

### Make scenario timeout = 40 seconds
- If your Make workflow takes longer than 40 seconds, it times out
- During a live call, this kills the conversation
- **Fix**: Return 200 immediately from Make, process in background
- For real-time tools, keep Make scenarios to < 5 seconds

### Tool failures are silent by default
- If your webhook returns an error, the LLM may hallucinate a response
- **Fix**: Add explicit error handling instructions in your prompt

### LLM won't call a tool unless told exactly when
- Vague instructions like "use this tool when needed" lead to inconsistent behaviour
- **Fix**: List exact trigger conditions: "Call save_lead when you have confirmed: name, phone, service_needed"

### No native retry logic
- If a webhook call fails, ElevenLabs doesn't automatically retry
- **Fix**: Add retry logic in your prompt: "If a tool fails, try once more, then offer a manual fallback"

### Dynamic variables must be set at call initiation
- You can pass caller data (e.g., from CRM lookup) when initiating a call
- Can't fetch it mid-conversation without a tool
- **Fix**: For inbound calls, use the post-call webhook to enrich records

---

## Telephony Gotchas

### Twilio integration is first-party but still requires Twilio account
- You need an active Twilio account with a purchased number
- Twilio requires ID verification for some countries
- New Zealand numbers via Twilio: may have restrictions — check Twilio docs for NZ
- **Alternative**: SIP trunking via Telnyx, Vonage, etc. — often cheaper for NZ

### Twilio webhook auto-configuration
- ElevenLabs auto-configures Twilio webhooks for you
- If you have existing Twilio apps on that number, they'll be overwritten
- **Fix**: Use a dedicated number for the AI agent

### Outbound calls require a From number
- For batch/outbound calling, you need a verified Twilio number
- Caller ID regulations vary by country — ensure compliance

### SIP trunking is more complex to set up
- SIP requires more technical configuration than native Twilio
- But: works with virtually any telephony provider
- Supported providers: Twilio, Vonage, RingCentral, Sinch, Telnyx, Bandwidth, Plivo, Infobip, Exotel

---

## Reliability & Performance Gotchas

### Sub-100ms latency is the AI processing — total round-trip is more
- 100ms is just ElevenLabs' processing latency
- Add: network latency, TTS generation, telephony buffering
- Real-world: expect 300-800ms response time (still very good for voice AI)
- Twilio's network adds ~50-150ms

### Cold start / first call delay
- First conversation after inactivity may be slightly slower
- RAG index needs to be "warm"
- For production: test before peak hours

### Provider outages affect the whole chain
- If OpenAI (LLM) is down, your agent stops working
- If Twilio is down, calls fail
- **Fix**: Monitor status pages. Have a human fallback plan.

### Audio quality varies with network conditions
- Poor caller connection → choppy audio → STT errors → agent misunderstands
- **Fix**: Build in clarification phrases: "I'm sorry, I didn't quite catch that — could you repeat?"

---

## Compliance & Legal Gotchas

### Recording calls requires disclosure in many jurisdictions
- New Zealand: informed consent is generally required before recording
- **Fix**: Include a disclosure in the first message if recording: "This call may be recorded for quality purposes"
- Or: disable call recording in ElevenLabs settings

### GDPR / Privacy Act compliance
- Collecting caller data = data controller obligations
- ElevenLabs offers GDPR compliance (EU Data Residency available)
- Configure data retention settings in Privacy settings
- Don't collect more data than you need

### HIPAA (healthcare only)
- ElevenLabs is HIPAA compliant on Business/Enterprise plans
- Not relevant for pest control/carpet cleaning unless you handle health data

---

## The "Sounds Robotic" Problem

Common causes:
1. Prompt uses corporate/formal language → agent mirrors it
2. Agent gives long, structured responses
3. Filler phrases are too formal ("I understand your inquiry")
4. Robotic greeting with no warmth
5. Awkward pauses (soft timeout not configured)

**Fixes**:
- Write prompts in natural spoken language
- Instruct: "Use short, conversational sentences"
- Set soft timeout with a natural filler
- Write the exact opening line you want
- Use a warm voice (not a monotone "professional" voice)
- Lower the temperature for consistency but don't go to 0 (0.3–0.5 is good)

---

## Quick Reference: Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Agent asks 5 questions at once | LLM default | Add "Ask ONE question at a time" to prompt |
| Agent misreads phone numbers | Number normalisation | Specify format in tool parameters |
| Agent hangs up abruptly | No end_call instructions | Script closing + add end_call tool |
| Agent makes up information | No knowledge base | Add knowledge base or guardrail |
| Tool fails silently | No error handling in prompt | Add tool error handling section |
| Caller says "what?" a lot | Responses too long | Shorten responses, use conversational language |
| Make timeout errors | Scenario too complex for real-time | Simplify or use post-call webhook |
| Calls drop at high volume | Concurrency limit hit | Upgrade plan or enable surge capacity |
| URL knowledge is outdated | Snapshot, not live | Re-import regularly |
# ElevenLabs Community Knowledge — Builder Insights

*Deep research: March 2026*
*Sources: Reddit (r/ElevenLabs, r/AI_Agents, r/automation), YouTube, practitioner blogs*

---

## Key Subreddit Insights

### From r/ElevenLabs (August 2025)
**Thread: "Conversational AI Agent Tips"**

Real builder advice from the community:
- **"For voice agents, stick with models optimized for latency like GPT-4o-mini or Gemini Flash. They are usually better for real-time interactions than the heavier ones."**
- **"Prompt design takes some trial/error but keeping it structured and role-specific helps a lot."**

Builders in 2025/2026 are using:
- GPT-5 Mini and Gemini 2.5 Flash Lite as primary models for real-time agents
- The 6 building block structure from official docs as a starting framework

### From r/automation (July 2025)
**Thread: "Just white-labeled ElevenLabs Conversational AI for my agency clients"**

Key takeaways from this builder:
- **Voice quality is noticeably better than Retell/Vapi** — this is the main selling point
- **White-label workflow**: Create agents in ElevenLabs → Connect via API keys and webhook secrets → Set up custom subdomain → Add branding → Create pricing plans with markup
- **Call concurrency management** with "number pools" handles high volume
- **Margins are strong**: reselling ElevenLabs at markup with your own branding
- Test clients "blown away by quality difference"

### From r/AI_Agents
**Thread: "Looking for tips to build my first AI voice agent"**

VoiceGenie builder experience:
> "While building ours, we spent a lot of time on the personalization aspect: how should the call begin, who should speak first, at what speed should the agent speak, can the agent be interrupted, how can we make the call as personal and authentic for the user as possible? We used ElevenLabs' voices and dynamic personalization elements — it's worked great for us."

Key personalisation questions every builder should answer before launch:
1. Who speaks first? (Agent first message vs. waiting for caller)
2. What speed? (0.9x-1.1x is natural)
3. Interruption allowed? (Usually yes for natural conversation)
4. How personal/authentic? (Dynamic variables for returning customers)

### From r/AI_Agents
**Thread: "Cost comparison on Voice Agents" (July 2025)**

Real builder cost experience:
- Someone building production agents was at ~$0.09/min (before ElevenLabs' February 2025 price cut to $0.10/min)
- Synthflow is described as "more lightweight/entry-level"
- Bland.ai has a reputation for ignoring non-enterprise clients
- ElevenLabs specifically flagged as the best voice quality option

**The "thing I wish I knew earlier" quote (from r/AI_Agents):**
> "The single biggest lever for natural-sounding voice agents isn't picking the right TTS voice."

The actual biggest levers (community consensus):
1. **Prompt structure** — how you write the prompt matters more than which voice
2. **Latency** — fewer hops in the chain = fewer failure points and better call quality
3. **Turn-taking config** — eagerness/patience dramatically affects conversation feel
4. **Soft timeout** — without it, the agent sounds broken

---

## YouTube Tutorial Landscape

### Key Tutorials Found

1. **"Build Your First Conversational Voice Agent with ElevenLabs – Complete Setup Guide"**  
   - Published: September 24, 2025  
   - URL: https://www.youtube.com/watch?v=fnivYSh0Cqk  
   - Content: Step-by-step through ElevenLabs Agents Platform, template selection

2. **"Build anything with elevenlabs voice agent and make.com!"**  
   - Published: January 8, 2025  
   - URL: https://www.youtube.com/watch?v=bbj1bAe7ADc  
   - Content: "🔥 Building Production-Ready Voice AI Agents: A Complete Guide — Learn how to create practical, business-ready voice agents using 11labs, Make.com, and Twilio"
   - This is the most relevant tutorial for Glenn's use case

---

## Common Failure Patterns (Community Knowledge)

### 1. The Multi-Question Dump
**What happens**: Agent asks "Can I get your name, address, phone number, and what service you need?"
**Why**: LLMs default to information-gathering efficiency
**Fix**: Explicitly add "Ask ONE question at a time. This step is important."

### 2. The Hallucination Response
**What happens**: Caller asks "What's your price for 3 bedrooms?" → Agent makes up a number
**Why**: No knowledge base or guardrail
**Fix**: Add guardrail "Never quote specific prices" + add knowledge base with actual pricing ranges

### 3. The Silent Hang
**What happens**: LLM takes 3+ seconds → awkward silence → caller thinks call dropped
**Why**: Soft timeout not configured
**Fix**: Enable soft timeout at 2-3 seconds with a natural filler phrase

### 4. The Endless Call
**What happens**: Agent keeps saying "Is there anything else?" forever, never ending the call
**Why**: No exit instruction + no end_call tool usage
**Fix**: Script the goodbye explicitly + instruct "use end_call tool after farewell"

### 5. The Robotic Greeting
**What happens**: "Hello, I am an AI assistant. How can I assist you today?"
**Why**: Generic LLM default greeting
**Fix**: Write the exact first sentence: "Answer with: 'Hi, BrightClean Carpet Cleaning, this is Mia, how can I help?'"

### 6. Phone Number Mangling
**What happens**: Caller says their number → agent tries to save "zero-two-one-one..." to the CRM
**Why**: System_prompt normalisation converts numbers to words
**Fix**: In tool parameter descriptions: "Phone number as digits only, e.g. '0211234567'"

### 7. The Cold Transfer Fail
**What happens**: Customer says "I want to speak to a person" → agent ignores or gets confused
**Why**: No transfer protocol in prompt
**Fix**: Add explicit human transfer instructions and configure the call_transfer system tool

### 8. The Off-Script Conversation
**What happens**: Caller asks about politics / asks the agent on a date / starts telling life story
**Why**: LLMs are generally helpful and will engage with anything
**Fix**: Add scope guardrail and polite redirect instructions

### 9. Tool Called Too Early
**What happens**: Agent saves lead with missing fields (just got first name, hasn't asked for phone)
**Why**: LLM decides it has "enough" and fires the tool
**Fix**: Explicitly list required fields in tool prompt AND add "Only call this tool when you have confirmed: name, phone, service_needed"

### 10. Tool Called Too Late  
**What happens**: Agent collects all info, says goodbye, hangs up WITHOUT saving the lead
**Why**: Agent didn't connect tool usage to conversation stage
**Fix**: Make the confirmation step trigger the tool: "After confirming all details, call save_booking before closing"

---

## What Makes Agents Sound Unnatural (Community Consensus)

**The top causes of robotic-sounding agents:**

1. **Prompt written in formal/written language** → agent mirrors it. Write prompts conversationally.
2. **Responses too long** → voice should be 1-3 sentences per turn maximum
3. **Formal filler phrases** → "I understand your inquiry" sounds robotic. "Got it!" sounds human.
4. **No soft timeout** → dead air while thinking kills the vibe
5. **Wrong turn eagerness** → too eager cuts callers off, too patient feels awkward
6. **High temperature + voice agent** → creative LLMs are unpredictable. Use 0.3-0.5 for trade agents.
7. **Professional voice clone that's too formal** → match the voice to the business personality
8. **Agent doesn't acknowledge what was just said** → "That's great!" or "Perfect!" before moving on
9. **Lists and bullet points in responses** → LLM sometimes outputs them, they sound terrible in voice
10. **Speed slightly off** → 0.9x is more natural than 1.0x for most voices

**The fix: listen to your own calls**. Every builder who reviews transcripts finds 3-5 issues in the first week that prompting alone won't reveal.

---

## Tips Only Experienced Builders Know

### Prompt Tips
1. **Add trade-specific vocabulary to ASR keywords** — "termite", "HVAC", "uPVC" — ASR boosting improves transcription accuracy for industry terms
2. **Don't describe what the agent IS; describe what it DOES** — "Answer calls" not "You are a helpful receptionist"
3. **Write the agent's 'internal monologue' for complex stages** — helps LLM reason through the process
4. **Test with a real phone, not the web widget** — phone audio quality is different, some issues only appear on phone

### Configuration Tips
5. **`spelling_patience: auto`** is usually best — model-based patience when someone spells out an address or email
6. **`speculative_turn: true`** reduces perceived latency (starts generating before turn ends) — worth enabling for fast-paced FAQ agents (increases LLM cost slightly)
7. **`silence_end_call_timeout`** — set to 30-45 seconds for conversations, 10-15 for FAQ agents. Prevents paying for calls where someone put the phone down.
8. **Initial wait time** — if you don't send a first message (agent waits for caller to speak first), set `initial_wait_time` appropriately

### Integration Tips
9. **Use Secrets Manager for ALL webhook URLs** — not just API keys. Even Make.com webhook URLs should be secrets.
10. **Post-call webhook > Mid-call tool for CRM saves** — post-call has no time pressure, can be more complex, and won't fail mid-conversation
11. **Send `200 OK` to post-call webhook immediately** — process async. ElevenLabs may disable webhook if you're slow.
12. **Log every single call for first 2 weeks** — dump the raw payload to a Google Sheet. You'll find data issues you can't predict.
13. **Build your webhook to handle missing fields gracefully** — agents won't always collect everything. Don't let your CRM save fail because suburb is empty.

### Testing Tips
14. **Test angry caller scenario explicitly** — many prompts fail when the caller is rude
15. **Test the "I'll call back" scenario** — many agents fail to capture these leads
16. **Test phone numbers being said slowly** — "zero... two... one... one..." needs the spelling patience setting
17. **Test background noise** — ASR degrades on noisy calls; add "If you didn't catch something, ask politely: 'Sorry, I missed that — could you repeat?'"
18. **Call it yourself from multiple phones** — VOIP phones, mobiles, different carriers behave differently

---

## White-Label Agency Model (Community Insight)

From r/automation — practical agency setup:

**The workflow:**
1. Create agents in ElevenLabs Conversational AI
2. Connect ElevenLabs account via API keys
3. Set up custom subdomain (e.g., `voice.youragency.com`)
4. Use a white-label platform (VoiceAIWrapper, etc.) for client dashboards
5. Create pricing plans with your markup on top of ElevenLabs rates
6. Client sees your branding; doesn't see ElevenLabs

**VoiceAIWrapper pricing for agencies:**
- Starter: $29/month — 5 client accounts, unlimited agents
- Growth: $79/month — 15 clients, Stripe billing, campaign features
- Scale: $249/month — unlimited clients, white-label ElevenLabs support
- Pro: $499/month — unlimited everything, priority support

These platforms sit on top of ElevenLabs and provide the agency-facing dashboard. You still pay ElevenLabs directly for minutes ($0.10/min pass-through).

**Agency pricing models being used (from community):**
- Setup fee: $500-$2,000 (configuration, testing, first 30 days)
- Monthly retainer: $300-$1,000/month (management, monitoring, updates, support)
- Or: Cost-plus voice minutes (charge client $0.20-0.30/min, cost is $0.10-0.12/min at scale)

---

## Competing Platforms (Community Comparison)

Community consensus on ElevenLabs vs. competitors:

| Platform | Strengths | Weaknesses | Best For |
|----------|-----------|------------|----------|
| **ElevenLabs** | Best voice quality, full-featured, good docs | No built-in telephony | Agencies wanting best voice + flexibility |
| **Synthflow** | Built-in telephony, no-code, reliable | Less flexible LLM stack | SMB no-code deployments |
| **Retell AI** | Good outbound calling, flexible | Telephony costs add up | High-volume outbound |
| **Vapi AI** | Maximum developer control, cheapest | Requires engineering | Dev teams building custom |
| **Bland AI** | Enterprise features, memory layer | Ignores non-enterprise clients | Large enterprise |
| **Goodcall** | Unlimited minutes flat rate, Google integration | Less advanced | Local service businesses |
# Competitive Intelligence — Voice AI for Trades Businesses

*Deep research: March 2026*
*Focus: Who's selling AI voice agents to trades businesses, what they charge, and market gaps*

---

## The Competitive Landscape

### Category 1: Platform-Level Competitors (Full Voice AI Stacks)

These companies build the entire voice AI platform (STT + LLM + TTS + telephony) and sell to businesses directly or through agencies.

#### Synthflow AI
- **Best for**: Fast setup, reliable call-centre quality, no-code
- **Pricing**: Starts at ~$0.08/min with bundled voice and AI
- **Strengths**: Built-in telephony layer (not rented) → faster response times, cleaner audio; drag-and-drop builder; strong for high concurrent calls
- **Weaknesses**: Less flexible for custom LLM stacks; fewer voice models
- **Plans**: $29-$299/month for access; usage charged per minute
- **White-label**: Yes, agency-friendly

#### Retell AI  
- **Best for**: High-volume outbound, flexible LLM
- **Pricing**: $0.07-0.08/min base; add LLM + TTS + phone = $0.14/min total
- **Strengths**: Multi-channel (voice, chat, SMS), outbound calling tools, knowledge base sync
- **Weaknesses**: Telephony via external carriers (quality varies), costs add up with stack
- **White-label**: Yes

#### Vapi AI
- **Best for**: Developer teams wanting full control
- **Pricing**: ~$0.05/min + provider fees (cheapest raw cost)
- **Strengths**: BYO telephony, STT, TTS, LLM — maximum flexibility
- **Weaknesses**: Requires engineering; not no-code
- **White-label**: Yes

#### Bland AI
- **Best for**: Enterprise, complex workflows
- **Pricing**: ~$0.09/min + subscription + outbound fees
- **Strengths**: Memory layer, compliance features, detailed logs, stable
- **Weaknesses**: Reputation for poor support of non-enterprise clients; community feedback is negative
- **White-label**: Enterprise-only

#### Goodcall
- **Best for**: Local service businesses wanting simple setup + unlimited calls
- **Pricing**: Flat monthly fee (not per-minute); starts around $99/month for basic
- **Strengths**: Unlimited calls (flat rate), Google Business Profile integration, simple setup
- **Weaknesses**: Less advanced features, limited customisation
- **Target market**: Single-location small businesses — restaurants, hair salons, home services
- **Integration**: Jobber, PestPac, Service Autopilot (via Zapier)
- **Real use case**: Pest control companies, carpet cleaners — exact match for Glenn's target market

#### ElevenLabs (Position)
- **Best for**: Best voice quality; agencies wanting premium product
- **Pricing**: $0.10/min (standard), $0.08/min (Business annual)
- **Strengths**: Best TTS quality in the market; full-featured platform; extensive API
- **Weaknesses**: No built-in telephony stack (uses Twilio/SIP); more setup required than Synthflow
- **White-label**: Possible via API + third-party platforms like VoiceAIWrapper
- **Differentiation**: Voice quality is genuinely better than competitors — this is its main selling point

---

### Category 2: Vertical-Specific Platforms for Trades

These companies have built entire products targeting the trades/home services market specifically.

#### Avoca AI (ai.avoca.ai)
- **Target**: Home services — HVAC, plumbing, electrical, pest control
- **What they do**: AI CSR (Customer Service Representative) + coaching
- **Integration**: Deep ServiceTitan integration (the dominant HVAC/plumbing CRM)
- **Pricing**: Not public — demo required; positioned as enterprise ($2k+/month estimated)
- **Results claimed**:
  - Aire Serv: 86% booking rate increase, 92% after-hours booking rate
  - Top Flight Electric: $170K new revenue, 10% → 70% booking rate
  - HL Bowman: 70% revenue growth YoY
- **Differentiator**: Deep ServiceTitan integration + call coaching/analytics for CSRs
- **Not suitable for**: Small single-location businesses; built for multi-location operations
- **Platform**: Own voice AI stack (not ElevenLabs)

#### AI Agent Employee (aiagentemployee.com)
- **Target**: Service-based businesses in Dallas-Fort Worth (US)
- **What they do**: AI voice agents for restaurants, property management, home services
- **Positioning**: "The definitive solution for service based businesses"
- **Market**: US-focused

#### FieldRoutes / PestPac (software vendors)
- These are pest control SaaS companies that have begun integrating AI agents
- Avoca AI listed as a partner/integration in FieldRoutes marketplace
- Trend: vertical SaaS companies adding AI voice as a feature

#### Trillet AI
- **Target**: Home services, HVAC resellers
- **Features**: Website scraping + review aggregation → deploys HVAC-trained agent in "under 5 minutes"
- **Blog content**: Specifically writing for HVAC resellers and agencies
- **Differentiator**: Very fast deployment from existing web presence

---

### Category 3: Agency White-Label Platforms

These companies build the plumbing for agencies to resell voice AI under their own brand.

#### VoiceAIWrapper
- **Target**: Agencies reselling voice AI to clients
- **What they do**: White-label portal + client dashboard over ElevenLabs, Retell, Vapi, Bolna, UltraVox
- **ElevenLabs support**: Yes (Scale plan and above)
- **Pricing**:
  - Starter: $29/month — 5 client accounts
  - Growth: $79/month — 15 clients, Stripe billing, campaigns
  - Scale: $249/month — unlimited clients, ElevenLabs white-label
  - Pro: $499/month — unlimited, priority support
- **Minutes**: Unlimited (you pay provider pass-through; VoiceAIWrapper doesn't mark up minutes)
- **Use case**: Glenn building an agency to sell to NZ/AU trades businesses

---

### Category 4: Human Answering Services (Being Disrupted)

These are the traditional competitors that AI agents are replacing:

- **Ruby Receptionist** (US): $285+/month for 50 calls
- **AnswerForce** (US): Home services focus, $300+/month
- **Local answering services** (NZ/AU): $500-$2,000/month for full reception
- **Part-time receptionist**: $25-35/hr NZ

**The disruption story**: AI voice agent at $150-300/month replaces $1,000-2,000/month human answering service with better 24/7 coverage and immediate data capture.

---

## What Agencies Are Charging

From community research (Reddit r/AI_Agents, April 2025):

> "AI voice and chat agents. I charge a setup fee $1000+ usually and a monthly fee $300-$1000/month depending on budgets."

**Common agency pricing models:**

### Model 1: Setup + Monthly Retainer
- Setup fee: $500-$2,000 (one-time)
- Monthly: $300-$1,000/month (management, monitoring, updates)
- Minutes: Pass-through to client (transparent) or bundled into monthly

### Model 2: All-Inclusive Monthly
- $500-$2,000/month flat
- Includes: setup, management, X minutes of calls, support
- Above X minutes: client pays overage

### Model 3: Value-Based Pricing
- Charge based on outcomes/bookings captured
- Less common but defensible ROI story
- Example: "$X per booking captured by the AI"

### Talk AI (AU) Pricing Reference
From talkai.au (Australian AI voice agency):
- Setup: $5,000-$20,000 one-time (for complex deployments)
- Managed services: $2,500-$10,000/month (development, management, monitoring, support)
- Usage: 20-90 cents/minute (they mark up from ElevenLabs' $0.10/min)
- Compare: receptionist at $50-60k/year → AI agent at $1,500/month = $18k/year

**For small trades businesses in NZ/AU:**
A sensible price point is likely:
- Setup: $800-$1,500 (configuration, knowledge base, testing, onboarding)
- Monthly: $300-$600 (maintenance, monitoring, updates, support)
- Minutes: bundled (e.g., up to 500 minutes, $0.25/min overage) OR pass-through at cost + markup

---

## Market Gaps & Opportunities

### Gap 1: NZ/AU Localised Agents
Most competitors are US-focused. A NZ/AU-specific voice agent service would:
- Have NZ/AU voices (or custom voice clones) — not American accents
- Understand NZ/AU pricing references ($NZD, $AUD)
- Handle NZ suburbs, postal codes, geography
- Be compliant with NZ Privacy Act + Australian privacy laws
- Know NZ/AU trade terminology

**ElevenLabs enables**: NZ/AU voice cloning, NZ-accented voices, localisation

### Gap 2: Trades Business Package
No one is offering a complete "AI receptionist for pest control/carpet cleaning" package in NZ/AU that includes:
- Pre-built prompt template for the industry
- Pre-built knowledge base structure
- Twilio NZ number setup
- Google Sheets lead capture
- SMS confirmation to caller
- Email notification to owner
- 30-day monitoring and prompt refinement

This is a productisable offering at $1,000-1,500 setup + $400/month.

### Gap 3: Small Business Price Point
Most agencies target medium-large businesses ($5k+/month). 
Small trades businesses in NZ (pest control companies, carpet cleaners with 2-5 vans) can't afford enterprise pricing but desperately need the service.
A $1,500 setup + $400/month is accessible and has clear ROI.

### Gap 4: Seasonal/Part-Time AI Receptionist
Trades businesses have seasonal demand spikes. A "turn on for summer, turn off in winter" model would be attractive.
Current platforms don't offer this well — most are subscription models.

### Gap 5: Industry-Specific Knowledge Bases
No one offers pre-built, vetted knowledge base content for specific trade verticals.
A library of "pest control AI knowledge base starter pack", "HVAC FAQ content pack" etc. would save customers significant setup time.

---

## Competitive Advantage Summary for ElevenLabs-Based Agency

If Glenn builds an agency selling ElevenLabs-powered voice agents to NZ/AU trades:

**Defensible advantages:**
1. **Voice quality** — ElevenLabs TTS is genuinely better than competitors
2. **Local focus** — NZ/AU trades knowledge, compliance, pricing in NZD
3. **White-label** — clients see your brand, not ElevenLabs
4. **Integration** — direct integration with NZ/AU-popular tools (Tradify, Jobber, ServiceM8)
5. **Small business price point** — gap in the market vs. enterprise-focused competitors
6. **Ongoing refinement** — monitoring transcripts, improving prompts over time (ongoing value delivery)

**Cost structure (Creator plan):**
- ElevenLabs Creator: $22/month ($11 first month)
- Twilio number (NZ): ~$3-5/month
- Twilio call charges (NZ inbound): ~$0.02/min
- ElevenLabs calls: $0.10/min
- Make.com: ~$9-29/month
- Total cost for small client: ~$40-60/month + $0.12-0.12/min usage
- Revenue at $400/month: strong margin

At 500 minutes/month per client: $60 in minutes + $60 in fixed = $120 cost → $400 revenue → $280 margin per client.

---

## Pricing Comparison Table

| Platform | Per Minute | Monthly Base | Best For |
|----------|-----------|--------------|----------|
| ElevenLabs (direct) | $0.10 | $22 (Creator) | Developers/agencies |
| Synthflow | ~$0.08 | $29+ | No-code agencies |
| Retell AI | $0.07-0.08 | ~$0 + usage | Developer teams |
| Vapi AI | ~$0.05 | ~$0 + usage | Max-control dev teams |
| Bland AI | ~$0.09 | + subscription | Enterprise |
| Goodcall | Flat rate | $99-299+ | SMB flat-rate preference |
| Avoca AI | Not public | $2,000+/month est. | Enterprise trades |
| Human answering | N/A | $1,000-2,000 | Those who won't try AI |
| Part-time receptionist | N/A | $2,000-4,000 | Small businesses (status quo) |
# ElevenLabs Voice Agents for Trades Businesses — Deep Dive

*Deep research: March 2026*
*Focus: Pest control, HVAC, carpet cleaning, plumbing, general trades in NZ/AU*

---

## Why Trades Businesses Are Perfect for Voice AI

Trades businesses have a near-perfect AI receptionist use case:
- High volume of inbound calls (especially during seasonal peaks)
- Calls follow predictable patterns (book job, get quote, ask service area question)
- After-hours calls are common and represent significant lost revenue
- Labour cost of a human receptionist is high ($50k-$60k NZ/AU, plus on-costs)
- Missed calls = lost jobs (callers move to the next result immediately)
- Data capture is simple (name, address, service, time, phone)

**Real results from the industry:**
- Avoca AI (Aire Serv case study): after-hours bookings from 58 to 208 — **booking rate 86% increase** after switching to AI
- Avoca AI (Top Flight Electric): booking rate from 10% to over 70%, unlocking $170K in new revenue
- Avoca AI (HL Bowman): 100% call answer rate, 93% AI satisfaction score, 70% revenue growth YoY
- Industry average from Avoca AI data: **12% growth in bookings within 3 months** of deployment
- Clients report: 27% increase in booking rate after 6 months with Avoca AI

---

## What Callers Ask (Industry-Specific)

### Pest Control Callers Ask:
- "I've got [pest] — can you come today/this week?"
- "How much does it cost for [specific pest]?"
- "Do you service [area/suburb]?"
- "Is it safe for pets/kids/pregnant women?"
- "How long does the treatment take?"
- "Do I need to leave the house?"
- "Will you guarantee it works?"
- "Can you do an inspection first?"
- "I think I've got termites — what do I do?" (emergency)
- "I saw one cockroach / mouse — is it serious?" (reassurance needed)
- "Do you do ongoing maintenance plans?"
- "I'm in a rental — can the landlord organise this?"

### Carpet Cleaning Callers Ask:
- "How much for [number] rooms?"
- "What's included — do you move furniture?"
- "How long does it take to dry?"
- "Can you do same-day/this weekend?"
- "Do you do upholstery too?"
- "Can you get [specific stain] out?"
- "Do you do commercial/office carpet?"
- "What products do you use? Are they pet-safe?"
- "Do you do rugs/car interiors?"
- "Can I get a quote without someone coming out?"

### HVAC Callers Ask:
- "My [heating/cooling] isn't working — can someone come today?" (emergency)
- "How much for a service/clean?"
- "Can you install a new [unit/system]?"
- "What brands do you service?"
- "My system is making a noise — is it serious?"
- "Do you do heat pumps / ducted systems?"
- "How often should I get it serviced?"
- "Is this under warranty?"
- "Can I get a quote for a new installation?"

### Plumbing Callers Ask:
- "I've got a burst pipe / flooding — I need someone NOW" (emergency)
- "My hot water isn't working"
- "I've got a leak / dripping tap"
- "How much to replace a [toilet/hot water cylinder]?"
- "Do you do drain unblocking?"
- "Can you come today / after hours?"
- "Do you do gas fitting?"
- "I've got low water pressure"

---

## Emergency Call Handling (Critical Pattern)

Emergency calls are the highest-value scenario — get these wrong and the caller goes elsewhere immediately.

### Emergency Detection Keywords

**Pest control:**
- "swarm", "infestation", "can't sleep", "they're everywhere", "in my food", "restaurant" (commercial + rodent = serious)

**Carpet cleaning:**
- "flooding", "water damage", "sewage backup", "need it today"

**HVAC:**
- "no heating", "it's freezing", "stopped working", "strange smell", "gas smell" (dangerous!)

**Plumbing:**
- "flooding", "burst", "water everywhere", "can't turn it off", "sewage"

### Emergency Response Protocol

```markdown
# Emergency Protocol

At the start of each call, listen for emergency signals. These include:
- Words like "urgent", "emergency", "can't wait", "happening right now", "flooding", 
  "burst", "swarm", "gas smell", "they're everywhere"
- A panicked or stressed tone
- Commercial/restaurant + pest situation (severe urgency)

If you detect an emergency:
1. Acknowledge immediately and calmly: "That sounds serious — let me make sure 
   we get someone on this as quickly as possible."
2. Collect ONLY: name, address, phone number (skip everything else)
3. Call escalate_emergency tool with: name, address, phone, emergency_description
4. Tell caller: "I've flagged this as urgent. Our on-call team will call you back 
   within [15 minutes/30 minutes] — please keep your phone nearby."
5. End the call warmly. Do NOT launch into standard booking questions.

Note: A caller who sounds panicked should hear a calm, reassuring voice. 
This is the moment that builds trust.
```

---

## Industry-Specific Knowledge Base Content

### Pest Control Knowledge Base Template

```
SERVICES:
- General pest control: ants, cockroaches, silverfish, spiders, flies
- Rodent control: rats, mice
- Termite inspection and treatment
- Bed bug treatment
- Wasp and bee removal
- Bird control
- Commercial pest management contracts

PROCESS:
Our technician will:
1. Inspect the property to identify the pest and extent of infestation
2. Recommend the most appropriate treatment
3. Apply treatment using EPA/regulated products
4. Provide aftercare advice and follow-up schedule

SAFETY:
- All products are registered and approved
- We advise on re-entry times (typically 2-4 hours for sprays)
- Pet-safe options available (please mention when booking)
- Safe for children after products have dried

TREATMENT LENGTHS:
- Cockroach treatment: 45-90 minutes
- Rodent baiting: 30-45 minutes + follow-up visits
- Termite treatment: varies significantly (hours to days)

COMMON QUESTIONS:
Q: How long before I see results?
A: Most treatments see improvement within 24-72 hours. Some (termites) take longer.

Q: Do I need to be home?
A: Someone over 18 needs to be present to provide access.

Q: Will the treatment smell?
A: Some treatments have a mild odour that dissipates within a few hours.
```

### Carpet Cleaning Knowledge Base Template

```
SERVICES:
- Carpet steam cleaning (hot water extraction)
- Dry carpet cleaning
- Upholstery cleaning (sofas, chairs, mattresses)
- Rug cleaning
- Car interior cleaning
- Tile and grout cleaning
- Water damage/flood restoration

PRICING GUIDE (for quoting calls):
- Standard room: $X-$X
- Large room or open plan: $X-$X
- Stair flight: $X
- Upholstery: from $X per cushion/seat

Note: Exact prices confirmed by team based on carpet type, condition, and job size.

DRY TIME:
- Steam cleaned carpets: 2-6 hours to dry (varies with ventilation, carpet thickness)
- Open windows if possible; ceiling fans help
- Avoid walking on carpet until dry (provide clean socks if needed)

STAIN REMOVAL:
- We treat most stains as part of standard service
- Some stains (permanent marker, bleach damage, old red wine) may not come out fully
- We can advise on whether a stain is likely treatable before booking
```

---

## Call Flow Design for Trades

### Minimal Viable Call Flow

```
1. Answer: "[Business], this is [Name], how can I help?"
2. Identify need: Booking / Quote / Question / Emergency / Existing customer
3. Emergency → emergency flow (see above)
4. Quote/booking → collect details (one at a time):
   → Name (first name only is fine)
   → Address or suburb (to confirm service area)
   → What service needed (with enough detail)
   → Preferred timeframe
   → Best phone number
5. Confirm all details back
6. "Our team will call you within [timeframe]"
7. "Is there anything else?"
8. Warm close → end_call
```

### Timeframe Commitments — What to Promise

Be careful here. Don't over-promise:
- **During business hours**: "Our team will call you back within 2 hours"
- **After hours / weekend**: "Our team will call you first thing [Monday/tomorrow] morning"
- **Emergency**: "Our on-call technician will call you within 30 minutes"

Never promise: exact appointment times, "we can come today" (unless you've actually checked availability)

---

## Pricing Question Handling

The #1 challenge: callers always want a price and agents shouldn't make one up.

**Strategy 1: Acknowledge + Explain**
```
"I understand you'd like a price — our team gives proper quotes once they know 
a bit more about the job. It takes them about 5 minutes over the phone. 
Could I take your number so they can call you back?"
```

**Strategy 2: Range + Confirm Later**
```
"For a standard [X] room carpet clean, prices typically start from [$X]. 
The exact amount depends on carpet type and condition. 
Our team can give you a firm quote in just a couple of minutes — 
shall I have them call you?"
```

**Strategy 3: Knowledge Base Ranges**
Load pricing ranges into knowledge base. Agent can give ranges but always says "the team will confirm the exact amount when they call."

---

## Compliance in NZ & AU

### New Zealand

**Key laws:**
- **Privacy Act 2020** + Telecommunications Information Privacy Code: governs data collection and use
- **Marketing Association Telemarketing Code of Practice** (voluntary but widely adopted): calling hours, disclosure rules, opt-out
- **TCF Scam Prevention Code**: valid caller ID required

**For inbound voice agents (responding to calls, not initiating them):**
- This is LOW risk — callers are contacting YOU
- Still need to handle data responsibly (Privacy Act)
- If recording calls: best practice is to disclose at start of call
- No specific law requiring AI disclosure for inbound calls in NZ (as of March 2026), but best practice and building consumer trust suggests doing it

**For outbound AI agents (calling customers):**
- Need consent before calling
- Identify caller + purpose at start of call
- Must disclose it's an AI
- Must provide opt-out mechanism
- Calling hours: 8am–9pm Monday–Saturday (Marketing Code)

**Sample NZ inbound disclosure (if recording):**
```
"[Business Name], this is [Name], just so you know this call may be recorded 
for quality purposes — how can I help you today?"
```

### Australia

**Key laws:**
- **Do Not Call Register Act 2006**: wash lists against register (outbound)
- **Telecommunications (Telemarketing & Research Calls) Industry Standard 2017**: strict calling hours and disclosure
- **Privacy Act 1988** (with 2025-26 reforms): privacy-by-design, transparency for automated decision-making
- **Telecommunications (Interception and Access) Act**: all-party consent for recording

**Calling hours:**
- Monday-Friday: 9am-8pm
- Saturday: 9am-5pm
- Sunday/public holidays: Prohibited

**AI disclosure requirements (Australia):**
- Any AI used in outbound calls must identify itself immediately, clearly, and accurately
- Inbound: best practice to disclose AI nature if asked directly

**Sample AU disclosure:**
```
"[Business Name], this is [Name], an AI assistant. This call may be recorded 
for quality purposes. How can I help you today?"
```

### Both Countries: Eleven-Point Compliance Checklist

1. Screen outbound lists against DNC registers (NZ MA + AU ACMA)
2. Confirm express or inferred consent for each number (outbound)
3. Configure calling hours in your dialler
4. Play required opening disclosure on every call
5. Provide live-agent transfer option within 30 seconds if requested
6. Provide immediate opt-out method
7. Encrypt call recordings and limit access
8. Delete/anonymise recordings after retention period
9. Keep audit trail of calls (date, time, script version, consent status)
10. Review scripts quarterly against updated guidance
11. Document breach-response plan

---

## Integration with Trade Job Management Software

When saving leads from voice calls, connect to trade-specific CRMs:

**Supported via Make.com integrations:**
- **Jobber** — popular for pest control, carpet cleaning, landscaping
- **ServiceM8** — common in AU trades
- **Tradify** — NZ/AU trade businesses
- **PestPac** — pest control specific
- **ServiceTitan** — HVAC and plumbing (what Avoca AI uses)
- **simPRO** — larger trade businesses

**Simple webhook → Google Sheets approach:**
For small businesses, starting with Google Sheets is fine:
- Spreadsheet with columns: Date/Time, Name, Phone, Address, Service, Preferred Time, Notes, Status
- Owner reviews daily and calls back
- Graduate to proper job management software as you grow

---

## Real Case Studies & Claimed Results

### Avoca AI (Professional Voice AI for Trades)
Used by: HVAC, plumbing, electrical, pest control companies

- **Aire Serv**: Booking rate went from 58 to 208 after-hours bookings per month (86% booking rate increase), 92% after-hours booking rate, 41% subscription signups
- **My Plumber Plus**: $129M revenue, 13% growth — AI handles overflow calls
- **Top Flight Electric**: Booking rate 10% → 70%, $170K new revenue, required 4 new technicians
- **HL Bowman**: 100% call answer rate, 93% AI satisfaction, 70% revenue growth YoY
- **Industry average**: 12% booking growth within 3 months

Note: Avoca is a commercial product targeting large trade businesses, integrating with ServiceTitan. Not built on ElevenLabs (they have their own voice stack).

### Goodcall (SMB Voice Agents)
Used by: pest control, home services, retail, restaurants

From their pest control documentation:
- AI detects emergency keywords ("swarm", "rodent in kitchen") and escalates
- Integrates with Jobber, PestPac, Service Autopilot via Zapier
- Handles "unlimited simultaneous calls" during peak season
- Includes multilingual support (Spanish, Mandarin, French)

Goodcall pricing: flat monthly fee (unlimited calls), starts higher but predictable

---

## Seasonal Call Patterns

**Pest Control:**
- Summer peak: ant, cockroach, wasp calls increase 3-5x
- Termite season: spring (depending on region)
- Rodent season: autumn/winter as rodents seek warmth
- AI particularly valuable for handling surge without extra staff

**HVAC:**
- Extreme cold/hot weather spikes: emergency calls from broken heating/cooling
- Service reminder season: autumn (get heating checked before winter)
- AI handles overflow when every tech is in the field

**Carpet Cleaning:**
- Spring cleaning peak (October/November in NZ/AU)
- Pre-Christmas demand spike
- Post-flood/water damage (weather events)
- AI handles call surge without extra admin staff

**Planning implication**: Concurrent call limits matter most during peak season. Upgrade ElevenLabs plan before seasonal peaks, or enable surge capacity (3x limit at 2x rate).
# ElevenLabs Conversational AI — Full API Reference

*Deep research: March 2026*
*Sources: Official API docs at api.elevenlabs.io/v1/convai/*

---

## Base URLs

```
https://api.elevenlabs.io           # Global default
https://api.us.elevenlabs.io        # US data residency
https://api.eu.residency.elevenlabs.io  # EU data residency (GDPR)
https://api.in.residency.elevenlabs.io  # India data residency
```

## Authentication

Pass your API key in the header:
```
xi-api-key: your_api_key_here
```

Get your API key: ElevenLabs Dashboard → Profile → API Key

---

## Agents API

### Create Agent

```
POST https://api.elevenlabs.io/v1/convai/agents/create
Content-Type: application/json
xi-api-key: YOUR_API_KEY
```

**Required body fields:**
```json
{
  "conversation_config": { ... },
  "name": "My Agent Name",
  "tags": ["trades", "pest-control"]
}
```

**Key `conversation_config` fields:**

```json
{
  "conversation_config": {
    "agent": {
      "prompt": {
        "prompt": "# Personality\nYou are Sarah...",
        "llm": "gemini-2.0-flash",
        "temperature": 0.3,
        "max_tokens": 150,
        "tools": [...]
      },
      "first_message": "Hi, thanks for calling PestAway, this is Sarah, how can I help?",
      "language": "en"
    },
    "asr": {
      "provider": "elevenlabs",
      "quality": "high",
      "keywords": ["pest control", "carpet cleaning", "HVAC"]
    },
    "tts": {
      "voice_id": "HDA9tsk27wYi3uq0fPcK",
      "model_id": "eleven_v3_conversational",
      "stability": 0.5,
      "similarity_boost": 0.75,
      "speed": 1.0,
      "text_normalisation_type": "elevenlabs"
    },
    "turn": {
      "turn_timeout": 7,
      "silence_end_call_timeout": 30,
      "turn_eagerness": "patient",
      "spelling_patience": "auto",
      "speculative_turn": false,
      "soft_timeout_config": {
        "timeout_seconds": 3,
        "message": "Let me just check on that...",
        "use_llm_generated_message": false
      }
    }
  }
}
```

**TTS Model options:**
- `eleven_flash_v2` — Default, lowest latency
- `eleven_flash_v2_5` — Improved flash
- `eleven_turbo_v2` / `eleven_turbo_v2_5` — Turbo family
- `eleven_multilingual_v2` — 70+ languages, higher latency
- `eleven_v3_conversational` — Best quality, supports expressive mode, same price

**LLM options (examples):**
- `gemini-2.0-flash` — Very fast, cost-effective, highly recommended
- `gpt-4o-mini` — Good quality, fast
- `claude-3-haiku-20240307` — Good reasoning, fast
- `gpt-4o` — Best quality, higher latency/cost

**Turn eagerness enum:** `patient` | `normal` | `eager`

**Response (200):**
```json
{
  "agent_id": "agent_abc123...",
  "name": "My Agent"
}
```

---

### Update Agent

```
PATCH https://api.elevenlabs.io/v1/convai/agents/{agent_id}
Content-Type: application/json
xi-api-key: YOUR_API_KEY
```

Partial update — only send fields you want to change. Same body structure as Create.

Optional query params:
- `enable_versioning_if_not_enabled=true` — Enable versioning for this agent
- `branch_id` — Update a specific branch (versioned agents)

---

### Get Agent

```
GET https://api.elevenlabs.io/v1/convai/agents/{agent_id}
xi-api-key: YOUR_API_KEY
```

---

### List Agents

```
GET https://api.elevenlabs.io/v1/convai/agents
xi-api-key: YOUR_API_KEY
```

---

### Delete Agent

```
DELETE https://api.elevenlabs.io/v1/convai/agents/{agent_id}
xi-api-key: YOUR_API_KEY
```

---

## Knowledge Base API

### Create from Text

```
POST https://api.elevenlabs.io/v1/convai/knowledge-base/text
Content-Type: application/json
xi-api-key: YOUR_API_KEY

{
  "text": "Services: carpet cleaning, upholstery cleaning...",
  "name": "Services & Pricing",
  "parent_folder_id": "folder_abc123"  // optional
}
```

**Response:**
```json
{
  "id": "kb_doc_abc123",
  "name": "Services & Pricing",
  "folder_path": [...]
}
```

After creating, attach to agent via Update Agent:
```json
{
  "conversation_config": {
    "agent": {
      "prompt": {
        "knowledge_base": [
          {"id": "kb_doc_abc123", "name": "Services & Pricing", "usage_mode": "auto"}
        ]
      }
    }
  }
}
```

**`usage_mode`**: `auto` (RAG, only retrieved when relevant) or `prompt` (always injected into context)

---

### Create from URL

```
POST https://api.elevenlabs.io/v1/convai/knowledge-base/url
Content-Type: application/json
xi-api-key: YOUR_API_KEY

{
  "url": "https://yourwebsite.com/services",
  "name": "Services Page"
}
```

⚠️ **Important**: This is a **one-time snapshot**. Changes to the URL won't auto-update. Re-import to refresh.

---

### Create from File

```
POST https://api.elevenlabs.io/v1/convai/knowledge-base/file
Content-Type: multipart/form-data
xi-api-key: YOUR_API_KEY

file: [binary file data]
name: "FAQ Document"
```

Supported: PDF, TXT, DOCX, etc.

---

### Update Knowledge Base Document

```
PATCH https://api.elevenlabs.io/v1/convai/knowledge-base/{document_id}
Content-Type: application/json
xi-api-key: YOUR_API_KEY

{
  "name": "Updated Services & Pricing"
}
```

---

### List Knowledge Base Documents

```
GET https://api.elevenlabs.io/v1/convai/knowledge-base
xi-api-key: YOUR_API_KEY

# Query params:
?page_size=30
&search=services           # Filter by name prefix
&types=text                # "file" | "url" | "text" | "folder"
&created_by_user_id=@me    # Only your documents
&sort_by=updated_at        # "name" | "created_at" | "updated_at" | "size"
&sort_direction=desc       # "asc" | "desc"
&cursor=abc123             # Pagination cursor
```

---

### Delete Knowledge Base Document

```
DELETE https://api.elevenlabs.io/v1/convai/knowledge-base/{document_id}
xi-api-key: YOUR_API_KEY
```

---

## Conversations API

### List Conversations

```
GET https://api.elevenlabs.io/v1/convai/conversations
xi-api-key: YOUR_API_KEY

# Query params:
?agent_id=agent_abc123                    # Filter by agent
&call_start_after_unix=1742601600         # Unix timestamp
&call_start_before_unix=1742688000        # Unix timestamp
&call_duration_min_secs=30               # Minimum 30 seconds
&page_size=100                           # Max 100 per page
&summary_mode=include                    # Include summaries
&search=pest control                     # Full-text search in transcripts
&call_successful=success                 # "success" | "failure" | "unknown"
&tool_names=save_lead                    # Filter by tool used
&tool_names_successful=save_lead         # Tools that succeeded
&tool_names_errored=save_lead            # Tools that errored
&main_languages=en                       # Filter by detected language
&conversation_initiation_source=twilio   # Source: twilio, whatsapp, etc.
```

**Response contains:**
- `conversations[]` — array of conversation summaries
- `next_cursor` — pagination cursor
- Each conversation: `conversation_id`, `agent_id`, `status`, `start_time_unix_secs`, `call_duration_secs`, `transcript_summary`, `has_audio`, etc.

---

### Get Conversation Details

```
GET https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}
xi-api-key: YOUR_API_KEY
```

**Response includes:**
- `status`: `initiated` | `in-progress` | `processing` | `done` | `failed`
- `transcript[]`: Full conversation with role/text per turn
- `metadata.phone_call`: caller number, call direction, call_sid
- `charging`: LLM token usage, call charge, LLM price breakdown
- `analysis`: data_collection results, evaluation results
- `has_audio`, `has_user_audio`, `has_response_audio`
- Deletion settings: when audio/transcript auto-deletes

**Status explanation:**
- `initiated` — call started
- `in-progress` — call active
- `processing` — call ended, post-processing transcript/analysis
- `done` — fully processed
- `failed` — error occurred

---

### Get Conversation Audio

```
GET https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}/audio
xi-api-key: YOUR_API_KEY
```

Returns audio recording if available.

---

### Delete Conversation

```
DELETE https://api.elevenlabs.io/v1/convai/conversations/{conversation_id}
xi-api-key: YOUR_API_KEY
```

---

## Webhooks (Platform-Level)

### Setting Up Webhooks

1. ElevenLabs Dashboard → Settings → Webhooks
2. Add endpoint URL
3. Get the webhook secret (for HMAC validation)
4. Choose event types

### Webhook Signature Validation

Every webhook request includes an `ElevenLabs-Signature` header. Always validate before processing:

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_KEY")

# In your webhook handler:
def handle_webhook(request):
    signature = request.headers.get("ElevenLabs-Signature")
    body = request.body  # raw bytes
    
    event = client.construct_event(
        body=body,
        signature=signature,
        webhook_secret="YOUR_WEBHOOK_SECRET"
    )
    
    # event.type, event.data are now available
    return 200
```

⚠️ Return HTTP 200 quickly! Failure to respond may cause ElevenLabs to automatically disable the webhook.
⚠️ For HIPAA compliance: failed webhooks are NOT retried.

### Post-Call Webhook Payload

```json
{
  "type": "post_call_transcription",
  "event_timestamp": 1742601600,
  "data": {
    "conversation_id": "conv_abc123",
    "agent_id": "agent_xyz",
    "status": "done",
    "started_at": "2026-03-22T09:00:00Z",
    "ended_at": "2026-03-22T09:04:32Z",
    "duration_seconds": 272,
    "has_audio": true,
    "has_user_audio": true,
    "has_response_audio": true,
    "transcript": [
      {
        "role": "agent",
        "message": "BrightClean Carpet Cleaning, this is Mia, how can I help?",
        "time_in_call_secs": 0
      },
      {
        "role": "user",
        "message": "Hi, I'd like to get a quote for carpet cleaning",
        "time_in_call_secs": 2
      }
    ],
    "metadata": {
      "phone_call": {
        "type": "twilio",
        "direction": "inbound",
        "agent_number": "+6491234567",
        "external_number": "+6421987654",
        "call_sid": "CA123...",
        "stream_sid": "MZ456..."
      }
    },
    "analysis": {
      "evaluation_criteria_results": {
        "booking_captured": {
          "result": "success",
          "rationale": "Agent successfully collected name, address, service and phone"
        }
      },
      "data_collection_results": {
        "caller_name": { "value": "John Smith", "rationale": "..." },
        "caller_phone": { "value": "0211234567", "rationale": "..." },
        "service_needed": { "value": "carpet cleaning - 3 rooms", "rationale": "..." }
      },
      "transcript_summary": "Caller John Smith requested a carpet cleaning quote for 3 rooms in Takapuna. Agent collected details and confirmed team will call within 2 hours."
    }
  }
}
```

---

## Dynamic Variables API

### How Dynamic Variables Work

Reference as `{{variable_name}}` in system prompt and first message. Set at call initiation.

**System variables (auto-populated for phone calls):**
- `{{system__agent_id}}` — Agent's ID
- `{{system__current_agent_id}}` — Current agent (after transfers)
- `{{system__caller_id}}` — Caller's phone number (inbound calls)
- `{{system__time_utc}}` — Current UTC time
- `{{system__call_sid}}` — Twilio call SID

### Twilio Personalization (CRM Lookup on Inbound)

Enable "Fetch conversation initiation data" in agent Security tab. When an inbound call arrives:

1. ElevenLabs sends caller data to your webhook
2. Your webhook looks up the caller in CRM
3. Returns dynamic variables to inject into the agent

Your webhook receives:
```json
{
  "caller_id": "+6421987654",
  "agent_id": "agent_xyz"
}
```

Your webhook returns:
```json
{
  "dynamic_variables": {
    "customer_name": "John Smith",
    "last_service": "carpet cleaning",
    "suburb": "Takapuna",
    "is_returning_customer": true
  }
}
```

Then in your system prompt:
```markdown
# Personalization
{{#is_returning_customer}}
The caller {{customer_name}} is a returning customer. Their last service was {{last_service}} in {{suburb}}.
Greet them by name and acknowledge their previous service.
{{/is_returning_customer}}
{{^is_returning_customer}}
This is a new caller.
{{/is_returning_customer}}
```

---

## Python SDK Quick Reference

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="YOUR_API_KEY")

# Create an agent
agent = client.conversational_ai.agents.create(
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "# Personality\nYou are Sarah...",
                "llm": "gemini-2.0-flash",
                "temperature": 0.3
            },
            "first_message": "Hi, BrightClean Carpet Cleaning...",
            "language": "en"
        },
        "tts": {
            "voice_id": "HDA9tsk27wYi3uq0fPcK",
            "model_id": "eleven_v3_conversational"
        }
    },
    name="BrightClean Receptionist"
)
print(agent.agent_id)

# Update an agent's system prompt
client.conversational_ai.agents.update(
    agent_id="agent_abc123",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "# Personality\nUpdated prompt..."
            }
        }
    }
)

# Add knowledge base document
doc = client.conversational_ai.knowledge_base.documents.create_from_text(
    text="Services: Carpet cleaning, upholstery cleaning...",
    name="Services & Pricing"
)
print(doc.id)  # kb_doc_abc123

# List recent conversations
convos = client.conversational_ai.conversations.list(
    agent_id="agent_abc123",
    page_size=50
)
for c in convos.conversations:
    print(c.conversation_id, c.call_duration_secs)

# Get full transcript
convo = client.conversational_ai.conversations.get(
    conversation_id="conv_abc123"
)
for turn in convo.transcript:
    print(f"{turn.role}: {turn.message}")
```

---

## Cost & Billing Notes

From the conversation object, you can see exact LLM costs per call:
```json
"charging": {
  "llm_usage": {
    "model_usage": {
      "gemini-2.0-flash": {
        "irreversible_generation": {
          "input": { "tokens": 1200, "price": 0.000018 },
          "output_total": { "tokens": 300, "price": 0.000012 }
        }
      }
    }
  },
  "llm_price": 0.00003,
  "call_charge": 100  // in credits
}
```

**Silence billing**: ElevenLabs bills silence periods at 5% of per-minute rate. Good to know for quiet calls.

---

## Recent API Changes (March 2026)

From the changelog:
- **Speculative turn config**: `speculative_turn` field added to TurnConfig — starts generating LLM responses during silence before turn confidence is reached (reduces perceived latency; increases LLM costs)
- **SIP inbound headers as dynamic variables**: Custom SIP X-headers exposed as `{{sip_contact_id}}`, `{{sip_campaign_id}}` etc.
- **Conversation filtering by tool outcome**: `tool_names_successful` and `tool_names_errored` query params added to list conversations
- **ContentThresholdGuardrail schema**: Configurable content moderation threshold
- **Tool error handling mode**: Added in v2.35.0 SDK
- **Eleven v3 Conversational model**: Added as TTS option
- **WhatsApp outbound messaging**: Now supported
- **Custom guardrails**: Added in v2.35.0
- **Users page**: Groups conversations by user identifier (GA for all workspaces)
- **WAV output support**: Added
- **Conversation embedding retention**: Configurable (default 30 days, max 365)
# Lead Flow Business Model & Pricing Strategy
*Research for Lead Flow — March 2026*
*Focus: Optimal business model for an AI + automation agency targeting NZ/AU trade businesses*

---

## Business Model Recommendation: Productised Service

### Why NOT Bespoke Agency
A bespoke agency model (custom quote per client, custom-built everything) creates:
- High time-per-client costs
- Unpredictable revenue
- Non-scalable delivery (more clients = more of Glenn's time)
- Client expectations of unlimited revisions and customisation
- Hard to hire for (every project is different)

### Why YES Productised Service
A productised service model (fixed packages, defined scope, repeatable delivery) enables:
- **Predictable monthly recurring revenue** (MRR)
- **Scalable delivery** (onboarding becomes a checklist, not a project)
- **Clear client expectations** (they know exactly what they're getting)
- **Faster sales cycles** (prospects pick a package, not custom-negotiate)
- **Hiring potential** (VAs or contractors can handle delivery with documented processes)

**Key principle**: Glenn sells the same core stack to every client, with light customisation (voice, prompts, integration) per business. The underlying infrastructure (Make.com workflows, ElevenLabs setup, Google Sheets templates) is reused and improved over time.

---

## The Three-Tier Package Structure

### Tier 1 — "Starter" ($799 setup + $397/month)

**What's included:**
- ElevenLabs AI receptionist setup (custom voice, prompt tuning)
- Twilio NZ/AU phone number provisioning
- Knowledge base build (services, pricing, FAQs, service area)
- Google Sheets lead capture (name, phone, address, service, timestamp)
- SMS + email notification to owner on every call
- SMS confirmation to caller after booking
- 1 Make.com workflow (call → lead capture → notifications)
- 30-day post-launch prompt refinement + transcript review
- Monthly: Monitoring, transcript review, prompt updates, 1hr support
- Up to 500 minutes/month included (fair use)

**Lead Flow cost:**
- ElevenLabs Creator: $22/month
- Twilio: $3-5/month + $0.02/min
- ElevenLabs call cost: $0.10/min
- Make.com: $9/month
- At 500 min/month: ~$120 cost
- **Margin: $397 - $120 = $277/month per client**

**Who it's for:** First-time AI adopters who want to start with the voice agent and see results before committing to more.

---

### Tier 2 — "Growth" ($1,497 setup + $697/month)

**What's included (everything in Starter, plus):**
- Full post-job automation sequence (SMS thank you → review request → care instructions)
- Quote follow-up automation (4-touch sequence over 14 days)
- Appointment reminder sequence (day-before + day-of SMS)
- Missed call follow-up automation
- Recurring treatment reminder setup (quarterly/annual sequences)
- Jobber OR ServiceM8 integration (set up + connected to voice agent)
- Monthly performance report (calls, leads, bookings, reviews generated)
- Bi-monthly strategy call (30 min) with Glenn
- Up to 750 minutes/month included

**Lead Flow cost:**
- Base Starter costs: ~$120/month
- Jobber basic plan (subsidised): $0 (client pays Jobber direct)
- Additional Make.com scenarios: ~$5-10 extra
- Additional admin time: 2-3 hrs/month
- **Approximate cost: $150-170/month**
- **Margin: $697 - $165 = $532/month per client**

**Who it's for:** Businesses 1-3 months in who want to turn the AI receptionist into a full growth system. Also the right starting package for motivated clients who want results fast.

---

### Tier 3 — "Full Moat" ($2,497 setup + $997/month)

**What's included (everything in Growth, plus):**
- Website AI chatbot (installed, trained, live lead capture)
- Google Business Profile full optimisation (photos, categories, Q&A, services)
- Review response automation (AI drafts responses to all new reviews)
- 5x suburb landing pages (AI-written, SEO-optimised)
- Monthly blog post (AI-drafted, client-approved)
- Annual maintenance plan / subscription program setup
- Referral program setup + automation
- Retargeting pixel + audience setup (Google/Facebook)
- Quarterly strategy session (1 hour) + written report
- Up to 1,000 minutes/month included
- Priority support (same-day response)

**Lead Flow cost:**
- All lower tier costs: ~$170/month
- Content tools (Jasper etc.): ~$30/month
- Additional strategy time: 4-5 hrs/month at Glenn's time
- **Approximate cost: $250-300/month**
- **Margin: $997 - $275 = $722/month per client**

**Who it's for:** Business owners who see Lead Flow as a strategic partner, not just a vendor. Wants to dominate their local market. Already has a working voice agent and is ready to compound it.

---

## Pricing Philosophy

### Why These Price Points Work in NZ/AU

**Comparison anchors (use in sales conversations):**
- Part-time receptionist: $2,500-3,500/month
- Full-time office manager: $5,000-7,000/month
- Traditional answering service: $500-2,000/month
- Digital marketing agency (SEO + ads): $1,500-5,000/month

**Lead Flow Starter at $397/month** is a no-brainer ROI conversation:
- Replaces a $500-2,000/month answering service with a better product
- Captures 1-2 extra jobs per month = $300-600 revenue
- Already cash-flow positive in Month 1

**Lead Flow Growth at $697/month** competes with digital marketing agencies:
- A pest control business spending $1,500-2,000/month on Google Ads + an agency still loses jobs after hours
- Lead Flow Growth at $697 captures every call AND follows up with automation
- Better ROI than most paid media spend

**Lead Flow Full Moat at $997/month:**
- Replaces receptionist + SEO agency + review service + email marketing platform
- Stacks of evidence the business is growing
- At this price point, a pest control company with 3 vans can justify it easily (1 extra job/week = $3,000+/month revenue)

---

## Setup Fee Strategy

**Why setup fees matter:**
1. Compensates for actual setup time (5-10 hrs per client)
2. Creates psychological commitment from client (they've invested, they'll engage)
3. Filters out low-intent prospects
4. Funds your time before MRR covers it

**Setup fee pricing rationale:**
- Tier 1 ($799): ~8 hours setup @ effective $100/hr — fair for the work
- Tier 2 ($1,497): ~15 hours setup (integrations, automation builds)
- Tier 3 ($2,497): ~25 hours setup (full moat build)

**Negotiation tip**: Never discount the setup fee. If client pushes back, offer to spread it across first 3 months instead.

---

## Onboarding Process & Timeline

### Standard Onboarding (Tier 1 — 5 business days)

**Day 1: Discovery call (30 min)**
- Services offered, service area, pricing approach
- Common questions customers ask
- Emergency/after-hours protocol
- Who should receive lead notifications
- Target booking times, seasonal notes

**Day 1-2: Build phase**
- Voice persona and greeting
- Knowledge base document
- ElevenLabs agent configuration
- Twilio number setup
- Make.com workflow (lead → Sheets → SMS/email)

**Day 3: First test**
- Internal test calls (5-10 scenarios)
- Prompt refinement based on results
- Test edge cases (angry caller, wrong number, emergency)

**Day 4-5: Client review + launch**
- Demo call with client — they hear the agent live
- Client approval + any final adjustments
- Go live on their main business number (forward calls)
- Client gets monitoring dashboard access

**Week 2-4: Refinement**
- Review call transcripts weekly
- Adjust prompts for any missed or awkward scenarios
- Track: conversion rate (calls → leads), call duration, emergency escalations

**Month 1 review call (30 min):**
- Review metrics, agent performance
- Discuss upgrade to Tier 2 if appropriate
- Identify quick wins

---

## Retainer Structures That Clients Stick With

### What Creates Retention

**1. Results visibility**
- Monthly report showing calls answered, leads captured, reviews generated
- Make the ROI undeniable on paper
- "You had 47 calls this month. Your agent handled 39 of them. At 1 missed call = average $180 job value, that's $7,020 in potential revenue captured."

**2. Stickiness through integrations**
- The more deeply integrated Lead Flow is into their stack (Jobber, Google Sheets, automated sequences), the higher the switching cost
- Cancelling Lead Flow = losing their automation, their lead capture, their review sequences
- Design for stickiness intentionally

**3. Progressive value delivery**
- Month 1-2: Voice agent working, leads captured
- Month 3: Review count visibly growing, ranking improving
- Month 6: Automation is running, recurring revenue starting
- Month 12: Digital moat is visible — they're #1 in their suburb searches
- At 12 months, it would be irrational to leave

**4. The "turn it off" thought experiment**
- Ask clients: "If you turned off Lead Flow tomorrow, what would you lose?"
- Good answer: "I'd lose my AI receptionist, my Google review machine, my follow-up sequences, my reporting... basically everything"
- This is the goal — make Lead Flow feel essential, not optional

---

## Churn Prevention Strategies

### The Three Danger Moments

1. **Month 1-2**: Client hasn't seen results yet, second-guessing the investment
   - Prevention: Proactive communication, show them call recordings, celebrate early wins
   - Danger signal: They stop replying to check-ins

2. **Month 3-4**: Novelty has worn off, they forget what life was like before
   - Prevention: Monthly report makes the value visible again ("47 calls handled this month")
   - Show what 47 calls would have cost at a human answering service ($500-1,000)

3. **Month 6-9**: They think they could do it themselves now
   - Prevention: Ongoing service additions (suburb page this month, referral program next month)
   - Keep delivering new value, don't let retainer feel stagnant

### Churn Prevention Tactics
- **Minimum contract**: 3-month initial commitment (after that, month-to-month)
- **Annual prepay discount**: 2 months free on annual payment (locks revenue, rewards commitment)
- **QBR (Quarterly Business Review)**: Formal check-in, new strategy, roadmap of what's coming
- **Early warning system**: If client doesn't respond to 2+ check-ins, escalate to phone call
- **Winback offer**: If cancellation notice received, immediate offer of one month free + a new automation build

---

## How to Position AI Voice + Automation as a Bundle

### The Bundling Story

**Don't sell the voice agent alone.** The voice agent is the entry point; the automation stack is the real value. Position it from Day 1:

*"The voice agent captures the lead. The automations turn that lead into a booking, a review, and a recurring customer. Without the automations, you're leaving money on the table."*

**Bundling makes competitors irrelevant:**
- A prospect could get a voice agent from Goodcall for $99/month
- They cannot get the full Lead Flow stack (voice + automations + GBP + content + moat strategy) anywhere else in NZ/AU at this price point
- Bundling creates a category of one

**Upselling within the relationship:**
- Start on Tier 1 → prove ROI → upsell to Tier 2 after 2-3 months
- Don't pitch Tier 3 to a new prospect unless they're clearly ambitious
- "Let's prove this works for you, then we'll add more layers"

---

## Revenue Projection: 2 to 20 Clients

### Current State (2 clients)
| | Client 1 (Pest Control) | Client 2 (Carpet Cleaning) |
|-|------------------------|---------------------------|
| Plan | Tier 1 | Tier 1 |
| Setup (paid) | $799 | $799 |
| Monthly | $397 | $397 |
| **Monthly MRR** | **$794** | |

### 6-Month Target (8 clients)
| Mix | Monthly Revenue |
|-----|----------------|
| 4 × Tier 1 @ $397 | $1,588 |
| 3 × Tier 2 @ $697 | $2,091 |
| 1 × Tier 3 @ $997 | $997 |
| **Total MRR** | **$4,676** |

### 12-Month Target (15 clients)
| Mix | Monthly Revenue |
|-----|----------------|
| 4 × Tier 1 @ $397 | $1,588 |
| 7 × Tier 2 @ $697 | $4,879 |
| 4 × Tier 3 @ $997 | $3,988 |
| **Total MRR** | **$10,455** |

### 18-Month Target (20+ clients)
| Mix | Monthly Revenue |
|-----|----------------|
| 4 × Tier 1 @ $397 | $1,588 |
| 10 × Tier 2 @ $697 | $6,970 |
| 8 × Tier 3 @ $997 | $7,976 |
| **Total MRR** | **$16,534** |

At 20 clients, Lead Flow is generating ~$16,500/month with a margin of ~60-65% = ~$10,000-11,000 profit/month. That's a sustainable full-time income for Glenn.

---

## What Other NZ/AU Agencies Are Charging

**Competitors found in research:**

| Agency | Location | Pricing |
|--------|----------|---------|
| TalkAI.au | Australia | $5k-20k setup, $2.5k-10k/month |
| Matrix Consulting AI | NZ/AU | Enterprise ($5k+/month) |
| Quantum Vector | NZ/AU | Enterprise (no public pricing) |
| Business AI Agents NZ | NZ | SMB focus (no public pricing) |
| Two Kiwi Robots | NZ | Chatbots for small business (SMB pricing) |

**Key insight**: The NZ/AU market has large enterprise players ($5k+) and very small DIY tools. There is a genuine gap in the $400-1,000/month productised service market for small trades — this is Lead Flow's target zone.

---

## White-Label Stack Recommendation

**For white-labelling the platform (so clients see "Lead Flow" not ElevenLabs):**
- **VoiceAIWrapper Scale plan** ($249/month): White-label client portal, ElevenLabs integration, client dashboards
- **HighLevel** ($297/month): Full white-label CRM, automations, website, landing pages — becomes "Lead Flow CRM" for clients
- Combined: ~$550/month in platform costs, supports unlimited clients
- Amortised across 10+ clients: $55/client — well within margins

**Recommendation**: Don't invest in HighLevel until 5-8 clients — it's powerful but complex. Start simple (Make.com + Google Sheets + Jobber integration), build processes, then graduate to HighLevel when the operational complexity justifies it.
# Lead Flow Growth Strategy: 2 to 20+ Clients
*Research for Lead Flow — March 2026*
*Focus: Scaling an AI services agency in NZ/AU targeting trade businesses*

---

## The Growth Challenge

Going from 2 clients to 20 isn't about working 10x harder. It's about:
1. Finding the right clients efficiently (channel strategy)
2. Closing them without a long sales cycle (positioning + demo strategy)
3. Delivering consistently without burning out (systemisation)
4. Keeping them long enough to build MRR (retention)

The 2→20 journey realistically takes 12-18 months. Here's the roadmap.

---

## Phase 1: Foundation (Months 1-3, 2→5 clients)

**Goal**: Nail the product, get 3 more paying clients, collect case studies.

### What to focus on
- Get current 2 clients to solid results (positive ROI, good reviews from them)
- Build repeatable onboarding process (documented checklist)
- Create a simple "Lead Flow demo" environment — a fake pest control business you can call to demonstrate the voice agent live
- Define your ICP (Ideal Client Profile) precisely

**Ideal Client Profile for Lead Flow:**
- Pest control or carpet cleaning business (the 2 proven verticals)
- 1-5 vans/technicians
- Owner-operated (owner answers the phone themselves currently)
- Auckland / NZ-based initially, then expand to NZ nationwide, then AU
- Taking 20+ calls per week
- Currently missing calls or using answering machine
- Has been in business 2+ years (established, not starting out)
- Revenue: $200K-$1M/year (can afford $400-700/month, sees the ROI)

### Acquisition in Phase 1
Focus on **outbound personal outreach** — it's the highest-leverage approach at this stage:
- Cold LinkedIn DMs to pest control / carpet cleaning business owners in Auckland
- Cold email (find emails via LinkedIn, website, Google Maps listings)
- Message: Problem-focused, not product-focused
  - ❌ "I have an AI service for your business"
  - ✅ "How many calls do you miss after hours? Most pest control businesses in Auckland lose 15-30% of jobs to voicemail."
- Goal: 10 conversations → 3 demos → 1-2 clients per month

---

## Phase 2: Traction (Months 4-8, 5→12 clients)

**Goal**: Add 7 new clients, start getting inbound leads, build a small referral base.

### Acquisition Channels (in order of priority)

**Channel 1: Referrals from existing clients (Highest ROI)**
After Month 2-3 with any client, if results are good, ask:
*"If you know any other pest control or trade businesses that are missing calls, I'd love an introduction. Happy to give them their first month at a discount and give you a thank-you gift card."*
- Referral conversion rate: 50-70% (pre-sold trust)
- Cost: Near-zero
- Action: Build a formal referral ask into the Month 2 check-in process

**Channel 2: Facebook/LinkedIn Groups (NZ Trades)**
- NZ Pest Control industry Facebook groups
- Tradify / ServiceM8 user communities
- NZ Small Business Facebook groups
- Carpet Cleaners NZ groups
- Don't spam — participate genuinely, answer questions, share value, mention Lead Flow when relevant
- One well-placed comment showing expertise ("Here's how I set up automated review requests for a pest control client — got them from 12 to 87 Google reviews in 4 months") > 100 cold messages

**Channel 3: Outbound Cold Email / LinkedIn DM**
Scale up Phase 1 outbound:
- Target pest control companies in Auckland, Hamilton, Wellington, Christchurch (NZ tier 1 cities)
- LinkedIn: Search "pest control", "carpet cleaning" + New Zealand, filter to business owners/directors
- Email finder: Apollo.io, Hunter.io (find owner emails)
- Sequence: 3-email sequence over 10 days (Pain → Solution → Evidence)

**Sample cold email sequence:**

*Email 1 (Day 1):*
```
Subject: How many calls are you missing?

Hi [Name],

Quick question — do you ever miss calls when you're out on jobs, or after hours?

I work with pest control businesses in Auckland, and the average company misses 
15-30% of inbound calls. At $200+ per job, that's a lot of revenue going to voicemail.

I set up an AI receptionist for businesses like yours — it answers every call 24/7, 
books jobs and takes messages in your name. Happy to show you a demo if it's relevant.

Glenn
Lead Flow — AI for Trade Businesses
```

*Email 2 (Day 5):*
```
Subject: Re: How many calls are you missing?

Just following up on my note from earlier in the week.

Figured I'd share a quick example: [Client business type, not name] in Auckland was 
missing roughly 20 calls a week — that's potentially $4,000+ in lost jobs each month.

Three months after we set up their AI receptionist, they're capturing every call, 
and their Google reviews went from 14 to 62. 

15-minute call this week? I'll show you exactly how it works.
Glenn
```

*Email 3 (Day 10):*
```
Subject: Last follow-up

I won't keep following up after this — I know you're busy!

If you're ever curious about what an AI receptionist would look like for your business, 
my calendar is here: [Calendly link]

Happy to do a live demo — you can call a "test business" and hear the agent in action.

Glenn
```

**Channel 4: Trade Association Partnerships**
- **Pest Management Association of NZ (PMANZ)**: Reach 200+ NZ pest control businesses
  - Approach: Offer to speak at their annual conference / webinar
  - "AI for Pest Control Businesses" — educational content, Lead Flow gets positioning
  - PMANZ members are exactly the ICP
- **NZ Carpet Cleaners Association**: Same approach for carpet cleaning vertical
- **Master Electricians / Plumbers NZ**: Future verticals

**Channel 5: Tradify / ServiceM8 / Jobber Partner Programs**
- **Tradify NZ Partner Program**: $250 per referral who upgrades to paid. More importantly, positions Lead Flow as a technology partner to the NZ trades market
  - Register at: tradifyhq.com/nz/partner-programme
  - Tradify contacts: NZ tradie businesses who are the exact ICP
- **Jobber Affiliate Program**: Up to 60% commission on first month when someone subscribes to monthly plan
  - Get registered: getjobber.com/affiliates/
- **ServiceM8 Partner Program**: Commission-based, access to AU trades market
  - Register at: servicem8.com/au/partners
- These partnerships generate referrals AND position Lead Flow inside the existing software ecosystems trades use

**Channel 6: Google Ads (Local, Small Budget)**
Once 8-10 clients are on board, invest $500-1,000/month in Google Ads:
- Target: "AI receptionist NZ", "AI answering service pest control", "voice AI for tradies"
- This audience is small but has high intent
- Landing page: Lead Flow website with demo booking CTA

**Channel 7: Content Marketing (Long Game)**
Start building now for 12-18 month payoff:
- LinkedIn posts (1-2/week) on AI for trade businesses, real results from clients
- YouTube (1/month): "How I set up an AI receptionist for a pest control business"
- Case study blog posts: "[Pest Control Company] doubled their Google reviews in 90 days"
- These compound over time into inbound leads

---

## Phase 3: Scale (Months 9-18, 12→20+ clients)

**Goal**: Productise delivery fully, hire help, grow MRR to $15k+/month.

### Systemising Delivery

**The Lead Flow Playbook:**
By Month 8, every service Lead Flow offers should have a documented SOP (standard operating procedure):
- Voice agent setup: Step-by-step checklist (ElevenLabs → Twilio → Make.com → Sheets)
- Review automation setup: Exact Make.com scenario template + configuration guide
- Jobber integration: Step-by-step setup guide
- Client onboarding: Exact questions to ask in discovery call + how to interpret answers
- Monthly reporting: Exact process for pulling data + report template

**Why this matters**: With documented SOPs, Glenn can hire a VA to handle the mechanical parts of setup and delivery, freeing him to focus on sales and strategy.

**First hire recommendation**: A Filipino VA (via OnlineJobs.ph, $500-1,000/month) trained to:
- Set up Make.com workflows from templates
- Configure Jobber/ServiceM8 per SOPs
- Write monthly reports using template
- Handle basic client support queries

This hire unlocks capacity to serve 15-25 clients without Glenn burning out.

---

## Sales Process: Selling AI to Non-Tech Business Owners

### The Golden Rule
**Never lead with technology. Always lead with the problem.**

A pest control business owner doesn't care about ElevenLabs or Make.com. They care about:
- Not missing calls when they're on a job
- Getting more Google reviews without begging customers
- Not spending $2,000/month on an answering service
- Actually knowing how many calls come in each day

### The 3-Stage Sales Process

**Stage 1: Discovery (the first conversation)**
Goal: Understand their pain, not pitch your solution.
Key questions:
- "What happens to calls that come in when you're on a job?"
- "How do you currently handle after-hours calls?"
- "How many Google reviews do you have right now?"
- "Do you have a receptionist, or does the phone just ring through to you?"
- "What's a typical job worth? And how often do you think you miss an enquiry?"

Let them feel the pain: "So if you're missing 5 calls a week at $250 a job, that's $1,250 a week, $65,000 a year in potential revenue going to voicemail?"

**Stage 2: The Live Demo (close to commitment)**
The single most powerful sales tool is a live demo. Set up a "demo business" that prospects can call in real-time:
- Voice agent answers: "Hi, you've reached [Demo Pest Control], I'm [Name], how can I help you today?"
- Prospect plays a customer asking about booking, pricing, safety questions
- Agent handles naturally, books a "job"
- Prospect receives a follow-up SMS within seconds

After the demo, ask: "Could you see that working for your business?" (Almost always yes.)

**Stage 3: The Close**
After a successful demo:
*"Here's what I'm thinking — we start you on the Starter package. I set everything up in about 5 days, your phones are answered 24/7 by your new AI receptionist, and you see what it looks like to never miss a call. If it's working after 60 days, we look at the automation layer. Sound fair?"*

Offer an easy next step: low commitment, clear timeline, defined outcome.

---

## Common Objections & Responses

**"It sounds expensive"**
> "Let's put it in context. You're currently missing maybe 20 calls a month to voicemail. At $200 average job value, that's $4,000 in potential revenue you're not capturing. The Starter plan is $397. If it captures even 2 extra jobs, it's paid for itself 4x over."

**"I don't think my customers will like talking to AI"**
> "That's the number one concern I hear. But let me call you back from a different number right now — just have a conversation with the agent." [Live demo]
> After: "Did that feel like AI to you? Most people don't notice. And those who do still prefer it to getting voicemail."

**"I'm not very technical"**
> "That's exactly why I'm here. You don't touch any of it — I set it up, test it, and maintain it. You just give me access to forward your phone number, and I do the rest. The only thing you do is get notified when a job comes in."

**"I'll think about it"**
> "Of course. Is there a specific concern I can answer while we're on the call? Sometimes 'think about it' means there's something I haven't addressed." [Uncover real objection]
> If genuinely unsure: "Happy to set you up with a free 7-day trial so you can see it working on your actual calls before committing. Nothing to install, no setup fee. If you want to keep going after 7 days, you pay the setup fee then."

**"I already have someone who answers my calls"**
> "What happens when she's on leave, or it's 8pm on a Saturday and someone needs emergency pest control? The AI is the after-hours + overflow solution — it works alongside your team, not instead of them."

**"I tried something like this before and it didn't work"**
> "What went wrong with it? [Listen carefully — often it was a basic IVR, or a chatbot, or a US-accented robot.] What I set up is different — it's conversational AI that actually understands what callers are saying and responds naturally. Want to hear the difference?"

---

## Partnership Opportunities (Key Channels)

### Tradify NZ (Highest priority)
- **Program**: Tradify Experts program — reseller with $250/referral bonus
- **Access**: 7,000+ NZ/AU trades businesses using Tradify
- **Fit**: Perfect alignment — Tradify users are exactly the ICP
- **Action**: Apply at tradifyhq.com/nz/partner-programme
- **Opportunity**: Offer "AI receptionist setup for Tradify users" — co-marketed with Tradify
- **Pitch to Tradify**: "We add AI answering to your platform — your customers get more value, we get referrals"

### Jobber (Good for AU expansion)
- **Program**: Affiliate program via PartnerStack
- **Commission**: Up to 60% of first month's subscription (when you refer someone to Jobber)
- **Action**: Register at getjobber.com/affiliates/
- **Opportunity**: For every trade business who doesn't have job management software, recommend Jobber → earn affiliate revenue while setting up their full stack

### ServiceM8 (AU trades market)
- **Program**: Partner program with revenue share
- **Audience**: Strong in NSW, VIC, QLD trades market
- **Action**: Apply at servicem8.com/au/partners
- **Opportunity**: AU expansion play — become the "AI receptionist specialist" for ServiceM8's partner ecosystem

### Accountants & Bookkeepers (Untapped channel)
NZ accountants often advise their trade business clients on software and operations:
- Find accountants who specialise in trades (many advertise on Tradify/Xero partner directories)
- Pitch: "When your pest control or carpet cleaning clients mention they're losing calls or struggling to grow, here's what Lead Flow offers. I'll give your clients a special rate and pay you a referral fee."
- Referral fee: $200 per client who signs up

### Trade Supply Stores / Hardware Suppliers
- Pest control supply companies (Garrards, Bayer Crop Science, etc.) sell to pest control businesses
- Carpet cleaning supply stores (CRI suppliers) sell to carpet cleaners
- These are trusted suppliers to exactly the ICP
- Partnership: Co-market to their customer base, referral arrangement
- This is a longer-term play but can produce steady referrals at scale

---

## Reaching Pest Control & Carpet Cleaning Owners: Best Channels

| Channel | Effort | Time to Results | Quality |
|---------|--------|----------------|---------|
| Direct referral from client | Low | Immediate | ★★★★★ |
| LinkedIn outbound | Medium | 1-2 months | ★★★★ |
| Cold email | Medium | 1-3 months | ★★★ |
| Facebook groups | Medium | 2-4 months | ★★★ |
| Tradify/Jobber partnership | Medium | 3-6 months | ★★★★ |
| Trade association events | High | 3-12 months | ★★★★★ |
| Google Ads | Low/$$$ | Immediate | ★★★ |
| LinkedIn content | Medium | 6-18 months | ★★★★ |
| YouTube content | High | 6-24 months | ★★★ |

**Recommendation for Glenn**: Focus on LinkedIn outbound + referrals in Months 1-6. Add Tradify/Jobber partnerships + trade groups in Months 4-9. Content marketing as a long-term investment starting now.

---

## Growth KPIs to Track

| Metric | Month 3 Target | Month 6 Target | Month 12 Target |
|--------|---------------|---------------|----------------|
| Total clients | 5 | 10 | 18 |
| MRR | $2,000 | $6,000 | $13,000 |
| Client churn rate | <10% | <8% | <5% |
| Sales conversations/month | 15 | 20 | 25 |
| Demo conversion rate | >40% | >50% | >55% |
| Avg months on retainer | - | 4+ | 8+ |
| NPS (client satisfaction) | 8+ | 8.5+ | 9+ |

---

## Case Studies from the Agency Growth Space

### Agency model that works at Lead Flow's scale:
The "vertical specialist" model consistently outperforms generalist agencies:
- Specialism in pest control / carpet cleaning = better case studies, faster onboarding, stronger positioning
- Word of mouth travels within industries ("my mate in pest control uses Lead Flow")
- Expertise compounds — every new pest control client makes the offering better for the next one

### Agency growth benchmark (from industry data):
- 89% of agencies use AI for efficiency improvements
- Average agency churn rate: 35% annually (Lead Flow's goal: <15%)
- Agencies that do QBRs (quarterly reviews) retain clients 40% longer than those that don't
- Productised agencies grow 2-3x faster than bespoke agencies (same revenue target, fewer hours)
# AI Tools for Trade Businesses (Beyond Voice Agents)
*Research for Lead Flow — March 2026*
*Focus: Genuine AI tools that help pest control and carpet cleaning businesses*

---

## Overview

Beyond the ElevenLabs voice agent, there are 7 categories of AI tools that genuinely move the needle for trade businesses. Lead Flow can resell, recommend, or build these as part of the automation stack.

---

## Category 1: Website AI Chatbots (Lead Capture)

### The Problem They Solve
30-40% of a trade business's website visitors arrive outside business hours or when the owner is on a job. Without a chatbot, these visitors leave without enquiring. A chatbot captures them.

### Best Options for Trades

**Tidio**
- Best for: Small businesses wanting a simple, affordable chatbot
- What it does: AI chat widget on website, captures leads 24/7, answers FAQs, triggers follow-up sequences
- Pricing: Free tier available; $19-79/month for automation
- NZ/AU: Works well, no local restrictions
- Integration: Zapier, Make.com, email, SMS
- Results: Tidio reports 27% conversion increase for businesses using their AI agent
- **Lead Flow recommendation**: ✅ Good entry-level option for clients not on HighLevel

**HighLevel Web Chat Widget**
- Best for: If client is already on HighLevel
- What it does: Embedded chat widget that captures leads directly into HighLevel CRM, triggers automated sequences
- Pricing: Included in HighLevel plan
- Integration: Native with all HighLevel automations
- **Lead Flow recommendation**: ✅ Use if building client's full stack on HighLevel

**Voiceflow / Botpress**
- Best for: Custom chatbot flows with complex decision trees
- What it does: No-code chatbot builder, highly customisable, can integrate with any CRM
- Pricing: Free tier for simple bots; $40-80/month for production
- **Lead Flow recommendation**: ✅ For premium Tier 3 clients wanting sophisticated website experiences

**Relevance AI / Custom GPT-based chatbot**
- What it does: Train a chatbot on the business's specific knowledge base (services, pricing, FAQs)
- Result: Chatbot that genuinely knows the business, answers questions accurately
- Pricing: $19-99/month for API-based deployments
- **Lead Flow recommendation**: ✅ Best quality option for Tier 3 Full Moat clients

### Chatbot + Voice Agent = Full Coverage
- Phone rings: Voice agent answers
- Website visitor: Chatbot engages
- Lead from either source: Goes to same CRM
- Result: Zero leads lost regardless of how they contact the business

---

## Category 2: AI for Review Response Generation

### The Problem It Solves
Google rewards businesses that respond to ALL reviews. But responding to every review manually takes time, and most business owners don't do it. AI automates this while maintaining quality.

### Best Options

**Make.com + OpenAI/Claude API**
- Build an automation: New review detected → AI generates personalised response → posted to Google
- Cost: ~$0.01-0.05 per response (essentially free)
- Quality: GPT-4 or Claude generate natural, professional responses
- Customisation: Inject business-specific keywords, service types, location
- **Lead Flow recommendation**: ✅ Build this into Tier 2+ as a value-add — takes 30 min to set up, runs forever

**Widewail / Reputation.com**
- Dedicated review management platforms with AI response generation
- Pricing: $100-300/month — overkill for small trades
- **Lead Flow recommendation**: ❌ Too expensive for the market segment

**NiceJob**
- Focused on review generation + response
- Pricing: $75-175/month
- Good review request automation (alternative to Jobber native)
- **Lead Flow recommendation**: ✅ Worth knowing about as an alternative/add-on

### AI Response Quality Guidelines
When building review response automation for clients:
- Never sound templated — vary sentence structure
- Always mention the specific service/product if available in the review
- Include natural location keywords ("Thanks for choosing us for your Auckland pest control!")
- For 1-2 star reviews: Empathetic, invite offline resolution, don't be defensive
- For 5-star reviews: Warm, specific, mention service, invite return

---

## Category 3: AI for Quote/Proposal Generation

### The Problem It Solves
Creating detailed quotes takes time — 30-60 minutes per quote for complex jobs. AI can generate professional quote documents from basic job notes in 5 minutes.

### Best Options

**ServiceM8 (Built-in AI Quoting)**
- What it does: AI helps generate quote text from job cards, photos, notes
- Pricing: Included in higher ServiceM8 tiers
- Best for: AU trades already on ServiceM8
- **Lead Flow recommendation**: ✅ Highlight when clients are on ServiceM8

**Toolbot AI**
- What it does: Upload photos, voice notes, or descriptions → generates draft quote
- Pricing: Free tier, $19/month premium
- Limitation: Newer product, limited track record
- **Lead Flow recommendation**: ✅ Good for clients who want a quick experiment

**ChatGPT / Claude (custom workflow)**
- Build a simple workflow: Technician fills in job template → pasted into GPT prompt → outputs formatted quote
- Zero incremental cost (GPT API or web interface)
- High quality output with a good prompt template
- **Lead Flow recommendation**: ✅ Easiest/cheapest starting point — build a prompt template and give to client

**Jobber Quotes**
- Native quoting (not strictly AI, but built-in workflow)
- Automatically includes line items, terms, digital acceptance
- Client signs quote online → auto-converts to job
- **Lead Flow recommendation**: ✅ Already included in Jobber — make sure clients are using it

---

## Category 4: AI for Social Media Content Creation

### The Problem It Solves
Pest control and carpet cleaning businesses get real SEO/visibility benefits from consistent social media presence, but owners have no time or inclination to create content regularly. AI can produce a month's content in an hour.

### Best Options

**ChatGPT / Claude (direct)**
- Prompt: "Create 4 weeks of Facebook posts for a pest control business in Auckland. Include seasonal tips, before/after photos suggestions, promotional offers, and educational content."
- Cost: Free (or minimal with API)
- Quality: Excellent with a good prompt
- **Lead Flow recommendation**: ✅ This is what Lead Flow should offer as part of Tier 3 — monthly content calendar

**Canva AI**
- What it does: Generate social media graphics, photos, captions
- Pricing: $20/month (Canva Pro)
- AI features: Magic Write, text-to-image, design suggestions
- **Lead Flow recommendation**: ✅ Use for creating visual content assets, especially before/after style graphics

**Jasper**
- What it does: AI content creation across all formats (social, blog, email, ads)
- Pricing: $39-59/month
- Good for: Agencies managing content for multiple clients
- **Lead Flow recommendation**: ✅ Worth investing in at 10+ clients to speed up content production

**Hootsuite / Buffer with AI**
- What it does: Schedule posts + AI content suggestions
- Pricing: $99-249/month (Hootsuite), $15-100 (Buffer)
- **Lead Flow recommendation**: ✅ If managing social for clients, Buffer at $15/month is cost-effective scheduling

### Content Formula for Pest Control (NZ/AU)
Monthly content plan framework:
- Week 1: Educational post (pest prevention tip, seasonal warning)
- Week 2: Before/after or job showcase (with customer permission)
- Week 3: Special offer / promotion
- Week 4: Team spotlight or company culture post
- Frequency: 3-4x per week Facebook, 1x per week Instagram Reel

---

## Category 5: AI Scheduling Assistants

### The Problem It Solves
The classic scheduling bottleneck: customer wants a time, owner has to check availability, call back, confirm. This back-and-forth wastes time and loses bookings.

### Best Options

**Jobber's Online Booking**
- What it does: Customer self-selects available time slots, books directly
- Pricing: Available on Jobber Connect ($69/month) and above
- Integration: Directly integrates with technician calendars
- **Lead Flow recommendation**: ✅ Must-have feature for any Jobber client

**Calendly + Make.com**
- What it does: Customer books time slot → triggers CRM entry + confirmation sequence
- Pricing: Calendly $10-20/month
- Good for: Simple booking before full Jobber integration
- **Lead Flow recommendation**: ✅ Easy interim solution for Tier 1 clients

**ServiceM8 Online Booking**
- What it does: Embedded booking widget for AU trades
- Pricing: Included in ServiceM8
- **Lead Flow recommendation**: ✅ Use for AU clients on ServiceM8

**Acuity Scheduling / TidyCal**
- Simpler booking tools for trades that want basic online booking without full job management
- Pricing: $15-20/month (Acuity), $29 lifetime (TidyCal)
- **Lead Flow recommendation**: ✅ Good budget option for entry-level clients

### The AI-Voice-Agent-to-Calendar Flow
The ideal setup:
1. Customer calls after hours
2. Voice agent captures their preferred time
3. Make.com sends booking to Calendly/Jobber
4. Calendar checks availability
5. Confirmation SMS sent to customer
6. Job added to technician's schedule

This is the full loop Lead Flow should be able to set up for Tier 2+ clients.

---

## Category 6: AI-Powered Reporting & Business Intelligence

### The Problem It Solves
Most trade business owners are making decisions based on gut feel, not data. They don't know which services are most profitable, where their best leads come from, or what their busiest days/seasons are.

### Best Options

**Jobber Reports**
- What it does: Built-in analytics for jobs, revenue, team performance
- Pricing: Included in Jobber
- Reports: Revenue by service type, technician performance, job completion time
- **Lead Flow recommendation**: ✅ Already included — make sure clients are using it

**Google Looker Studio (free)**
- What it does: Connect to Google Sheets/APIs → build custom dashboards
- Pricing: Free
- Use case: Build Lead Flow's "Digital Moat Dashboard" — one view showing calls, leads, bookings, reviews, rankings
- **Lead Flow recommendation**: ✅ Build this as a Tier 2+ deliverable — client gets a custom dashboard

**Make.com + Google Sheets**
- Automated data pipeline: Pull data from voice agent, Jobber, Google, and other sources → auto-populate dashboard
- Cost: Included in Make.com subscription
- **Lead Flow recommendation**: ✅ The backend for the Looker Studio dashboard

**Klipfolio / Databox**
- What they do: Business intelligence dashboards pulling from multiple SaaS tools
- Pricing: $49-249/month
- Best for: Higher-tier clients who want a polished analytics experience
- **Lead Flow recommendation**: ✅ Consider as a premium add-on for Tier 3

### The Lead Flow Dashboard (Build This)
Create a single dashboard for every client showing:
- Total calls this month vs. last month
- Calls handled by AI vs. missed
- New leads captured
- Bookings created
- Revenue attributable to AI-captured leads
- Google review count + average rating (vs. last month)
- Google Maps ranking for top 3 keywords

This dashboard makes Lead Flow's value undeniable and dramatically improves retention.

---

## Category 7: SMS/Email Marketing AI Tools

### The Problem It Solves
A database of 200+ past customers sitting unused is wasted money. AI-driven email and SMS marketing reactivates these customers automatically.

### Best Options

**HighLevel (SMS + Email + Automations)**
- What it does: Everything — CRM, email, SMS, automations, AI content generation
- Pricing: $97-297/month
- Best for: Lead Flow using as white-label platform for clients
- **Lead Flow recommendation**: ✅ The eventual "full stack" platform — introduce at Tier 3

**Klaviyo / ActiveCampaign (Email)**
- What they do: Sophisticated email marketing with AI content suggestions
- Pricing: $20-100/month for small lists
- Best for: Clients with 1,000+ email subscribers
- **Lead Flow recommendation**: ✅ Overkill for most small trades clients until list is built

**SMSBump / Klaviyo SMS**
- What they do: AI-powered SMS marketing
- Pricing: Usage-based
- **Lead Flow recommendation**: ✅ Better to use Twilio via Make.com for most NZ/AU trades at this stage

**Mailchimp with AI**
- What it does: Email marketing with AI subject line suggestions, content generation
- Pricing: Free for <500 subscribers; $13+/month above that
- AI features: Improved over 2025 with AI content suggestions
- **Lead Flow recommendation**: ✅ Good starting point for basic email newsletters

### The Reactivation Campaign (Lead Flow Service)
Quarterly reactivation campaign for every client:
1. Export "hasn't booked in 6 months" segment from CRM
2. AI writes 3-email sequence (value + offer + urgency)
3. Send over 2 weeks
4. Track: opens, clicks, bookings generated

**Expected ROI**: Every reactivation campaign should generate $500-2,000 in recovered revenue for a pest control business with 200+ past customers.

---

## Tools Specifically Built for Trades

### NZ/AU-Relevant Trade Platforms

| Tool | What It Does | Price | NZ/AU Focus |
|------|-------------|-------|-------------|
| Tradify | Job management (NZ-founded) | $35-69/month | ✅ NZ/AU native |
| ServiceM8 | Job management (AU-strong) | $29-349/month | ✅ AU primary |
| Jobber | Job management (global) | $69-299/month | ✅ Yes |
| Fergus | Job management (NZ) | $49-99/month | ✅ NZ-founded |
| simPRO | Enterprise job management | Custom | ✅ AU HQ |
| OptimoRoute | Route optimisation | $19-49/driver | ✅ Yes |
| FieldRoutes | Pest control specific | Custom | ✅ AU/NZ |
| PestPro CRM | Pest control CRM | From $49 | ❌ US-focused |

### AI Tools That Work Well Across All Trades

| Tool | Category | Price | NZ/AU |
|------|----------|-------|-------|
| ElevenLabs | Voice AI | $22+/month | ✅ |
| Make.com | Automation | $9-29/month | ✅ |
| Tidio | Web chatbot | Free-$79 | ✅ |
| Canva AI | Content creation | $20/month | ✅ |
| ChatGPT / Claude | General AI | Free-$20 | ✅ |
| NiceJob | Review automation | $75-175 | ✅ |
| Google Looker Studio | Analytics dashboard | Free | ✅ |
| Toolbot AI | Quote generation | $19+/month | ✅ AU-focused |

---

## Lead Flow's AI Stack Recommendation by Tier

### Tier 1 (Starter)
- ElevenLabs voice agent ✅ (already)
- Jobber (or Tradify/ServiceM8) for job management
- Make.com for automations
- Google Sheets for simple lead tracking
- Native review automation via Jobber

### Tier 2 (Growth)
- Everything in Tier 1
- Tidio OR HighLevel web chat widget
- AI-powered review responses (Make.com + OpenAI)
- Looker Studio dashboard (built by Lead Flow)
- Mailchimp or similar for basic email sequences

### Tier 3 (Full Moat)
- Everything in Tier 2
- HighLevel as full white-label platform
- Canva AI for social content creation
- Monthly social media content calendar (AI-generated)
- AI-powered quote template (ChatGPT workflow)
- Full reporting dashboard + monthly strategic review
# Pest Control Automation Opportunity Map
*Research for Lead Flow — March 2026*
*Focus: What automations can be sold to pest control businesses BEYOND the voice agent*

---

## Overview: The Automation Stack for Pest Control

A pest control business has predictable, repeatable workflows that are perfectly suited for automation. The average owner is spending 3-5 hours/day on admin tasks that should be automated. Below is the complete opportunity map.

---

## 1. CRM & Lead Management Automation

### What It Is
Automatically capture, organise, and follow up with every inbound lead — whether they called, emailed, filled out a web form, or came via Facebook.

### The Automations
- **Lead capture to CRM**: Voice agent call → webhook → Jobber/ServiceM8/Google Sheets (already done with voice agent)
- **Lead scoring**: Tag leads by urgency (emergency vs. routine), service type, and source
- **Missed lead follow-up**: If a lead isn't converted to a booking within 24 hours, automatically send an SMS: *"Hi [Name], just checking if you still need help with your pest problem — we can usually get to you within 48 hours. Reply YES to book."*
- **Lead nurture sequence**: 3-email sequence for quote enquiries that didn't convert (Day 1: value-add tips, Day 3: offer, Day 7: last chance)
- **Lead source tracking**: Track which marketing channel produced each lead (Google Ads, referral, organic, etc.)

### Tools
- **Jobber** (built-in CRM + automation triggers)
- **ServiceM8** (great for AU trades)
- **Make.com** (connect voice agent → CRM → SMS/email)
- **HubSpot Free** (for more advanced CRM capability)
- **HighLevel** (all-in-one, popular with agencies — good white-label option for Lead Flow)

### ROI Evidence
- Rentokil: **671% marketing ROI** using CRM automation (HubSpot case study)
- Industry data: Automated follow-up within 5 minutes of a lead inquiry increases conversion by 9x vs. following up within 1 hour
- 5% increase in customer retention = equivalent to cutting expenses 25%

---

## 2. Scheduling & Dispatch Automation

### What It Is
Automatically confirm bookings, assign technicians, optimise routes, and handle rescheduling — without office staff manually coordinating.

### The Automations
- **Booking confirmation SMS**: Immediately upon booking → "Hi [Name], your pest treatment is booked for [date/time] with [Company]. Our tech will call 30 mins before arrival."
- **Technician assignment**: Auto-assign based on technician location, availability, and skill set (termite-qualified vs. general)
- **Route optimisation**: Group nearby jobs on the same day to minimise drive time — saves 15-20% on fuel costs (OptimoRoute data: 15% yearly savings per truck)
- **Day-before reminder**: SMS + email reminder 24 hours before appointment with cancel/reschedule link
- **Tech arrival notification**: "Your technician [Name] is on their way — ETA 25 minutes" (via GPS trigger)
- **No-show follow-up**: If customer isn't home, auto-send "We missed you" SMS with one-click rebook
- **Capacity alerts**: Alert owner when bookings hit 80% of weekly capacity (plan ahead for seasonal peaks)

### Tools
- **Jobber** (scheduling, dispatch, client notifications — native automation)
- **ServiceM8** (AU-popular, strong mobile dispatch features)
- **OptimoRoute** (dedicated route optimisation — integrates with both)
- **FieldRoutes** (pest-control-specific, full scheduling automation)
- **Make.com** (custom trigger → action workflows)

### ROI Evidence
- OptimoRoute customer: "Increased work time, decreased travel time, **saved 15% yearly on fuel** per crew truck"
- FieldRoutes: "Save office staff up to four hours a day" with automated scheduling communications
- Missed appointment rate drops 40-60% when automated reminders are sent

---

## 3. Post-Job Communication & Review Automation

### What It Is
The job is done — now automate the follow-up sequence that turns a one-time customer into a recurring one and generates Google reviews.

### The Post-Job Sequence (Make.com automation)
```
TRIGGER: Job marked "Complete" in Jobber/ServiceM8

Step 1 (immediate): Thank-you SMS
"Hi [Name], thanks for choosing [Company] today! Your [cockroach/rodent] treatment is done. 
The products need 2-4 hours to work — keep kids and pets off treated areas until dry."

Step 2 (2 hours later): Safety/care email  
Subject: "Your treatment is complete — a few things to know"
- What was treated
- Re-entry times
- What to expect (timeline for results)
- Emergency contact number

Step 3 (24 hours later): Review request SMS
"Hi [Name], we hope the treatment is working well! We'd love a quick Google review — 
it only takes 2 minutes and helps our small business a lot 😊 [direct Google review link]"

Step 4 (if no review after 3 days): Review request email
Subject: "Quick favour — did we do a good job?"
[Same message with direct Google review link]

Step 5 (30 days later): Satisfaction check + upsell
"Hi [Name], it's been a month since your [service]. Any sign of the pests coming back? 
Reply YES to book a follow-up, or NO if all clear."
```

### The Google Review Automation (Critical)
- **Jobber native**: Built-in review request triggers at job close, visit complete, or invoice paid
- **ServiceM8 native**: Customer Feedback Automation built in — sends email/SMS feedback requests automatically
- **Make.com custom**: More control over timing, wording, and which customers receive requests

**Why review velocity matters:**
- Recent reviews (last 90 days) carry significantly MORE weight than old reviews
- 20 reviews in last 3 months > 50 reviews with nothing recent
- Businesses hitting 100+ reviews see noticeable ranking boosts
- Target: 4.6+ star average (below 4.0 actively hurts visibility)
- An automated review request captures reviews that would otherwise never happen — most satisfied customers don't volunteer reviews unless asked at the right moment

### Tools
- **Jobber Reviews** (native, easy to set up)
- **ServiceM8 Feedback Automation** (native)
- **Make.com** (custom flows, more control)
- **NiceJob** (dedicated review automation platform, integrates with both)
- **Podium** (enterprise review automation — overkill for small trades but powerful)

---

## 4. Quote Follow-Up Automation

### What It Is
A quote is sent — 60-70% of quotes never get accepted because the business never followed up. Automated follow-up sequences fix this.

### The Quote Follow-Up Sequence
```
TRIGGER: Quote sent but not accepted after 48 hours

Step 1 (Day 2): Gentle check-in SMS
"Hi [Name], just checking if you got our quote for the [service]? 
Happy to answer any questions — just reply here."

Step 2 (Day 4): Value-add email
Subject: "A few things to know about [pest] treatment"
[Educational content that builds trust + reinforces urgency]
[Quote reminder with accept link]

Step 3 (Day 7): Limited offer
"Hi [Name], our quote for your [service] expires this Friday. 
We can fit you in this week — want to lock it in? [Book link]"

Step 4 (Day 14): Win-back attempt
"Hi [Name], just wanted to check — did you get sorted with the [pest] problem? 
If not, our quote is still valid — just reply and we'll get you booked."
```

### Tools
- **Jobber** (quote follow-up automation built-in on Connect and higher plans)
- **ServiceM8** (automated quote reminders)
- **Make.com** + Twilio (custom SMS sequences)
- **HighLevel** (if agency wants white-label platform)

### ROI Evidence
- Industry data: Following up on unanswered quotes increases conversion by 20-35%
- Most trades businesses never follow up on quotes — this automation alone can increase revenue 10-15%

---

## 5. Invoicing & Payment Automation

### What It Is
Get paid faster with automated invoice delivery, payment reminders, and late payment nudges.

### The Automations
- **Auto-invoice on job complete**: Invoice generated and sent the moment job is marked done
- **Payment link SMS**: Send SMS with payment link immediately after invoice (dramatically improves same-day payment rate)
- **Payment reminder sequence**: Day 3, Day 7, Day 14 reminders for unpaid invoices
- **Receipt + thank you**: Immediate thank-you message when payment received
- **Recurring billing**: For ongoing maintenance contracts — auto-charge card on file monthly

### Tools
- **Jobber** (invoicing, payments, automated reminders — full suite)
- **ServiceM8** (AU-popular, strong invoicing + payment automation)
- **Stripe** (payment processing, integrates via Make.com)
- **Xero** (accounting integration — auto-sync jobs to invoices)

### ROI Evidence
- Businesses using automated payment reminders get paid 40% faster on average
- Same-day payment rate jumps from ~20% to 60%+ when payment link is sent immediately via SMS

---

## 6. Recurring Treatment Reminder Sequences

### What It Is
Pest control is a recurring service business — most customers need quarterly or bi-annual treatments. Automated reminder sequences bring customers back without any manual effort.

### The Recurring Customer Sequence
```
TRIGGER: Job completed (tagged as "quarterly customer" or by service type)

Month 2.5 (before 3-month mark):
SMS: "Hi [Name], it's been about 3 months since your last treatment with us. 
Pests love [season]! Want to book your follow-up? Reply YES and we'll find a time."

Month 2.5 (4 days later if no response):
Email: Subject: "Time for your quarterly pest check"
[Seasonal pest tips relevant to their area]
[Easy booking link]

Month 3 (if still no booking):
SMS: "Hi [Name], your quarterly treatment is overdue — pests can re-establish quickly! 
[urgent booking link]"
```

**Annual plan customers (premium recurring):**
- 4x treatments/year
- Pre-scheduled with automated reminders 1 week before each visit
- "Member" communication cadence (feel like a VIP)
- Annual renewal prompt with discount incentive

### The Annual Maintenance Plan (Revenue Multiplier)
A basic "pest protection plan" at $X/quarter (auto-billed) turns a one-time $150 job into $600/year in recurring revenue per customer. This is the single biggest revenue multiplier available.

**Example plan structure:**
- Quarterly General Pest Treatment: $149/visit × 4 = $596/year (vs. $249 one-off)
- Annual Termite Inspection: $199 included
- Priority booking + 10% discount on extras
- Automated SMS/email touchpoints keep customer engaged year-round

---

## 7. Referral Program Automation

### What It Is
Turn happy customers into a sales team. Automated referral programs generate word-of-mouth leads with zero ongoing effort.

### The Automated Referral System
```
TRIGGER: 14 days after job completion (high satisfaction window)

Step 1: Referral offer SMS/email
"Hi [Name], we hope your pest problem is fully resolved! 
If you know anyone else who needs help, we'll give YOU $20 credit and THEM 10% off 
their first service. Just send them this link: [referral link]"

When referral converts:
- Referrer gets SMS: "Great news! [Friend] just booked with us. Your $20 credit is applied!"
- New customer gets SMS: "Your 10% discount is applied to your booking — thanks for choosing us!"
```

### Tools
- **Jobber Referrals** (built-in referral tracking, available as add-on)
- **ReferralHero** (standalone referral platform, Make.com integration)
- **Make.com** (custom referral tracking + reward workflows)

---

## 8. Reporting & Analytics Automation

### What It Is
Weekly/monthly performance reports delivered automatically — no manual pulling of stats.

### Automated Reports
- **Weekly business summary**: Jobs completed, revenue, new leads, reviews received, average job value
- **Lead source report**: Which channels are generating the best leads + conversion rates
- **Technician performance**: Jobs completed, customer ratings, upsell rates per tech
- **Seasonal trend alerts**: "Summer approaching — cockroach calls usually spike 3x in October/November"
- **Customer lifetime value tracking**: Identify best customers for retention focus

### Tools
- **Jobber Reports** (native analytics dashboard)
- **Google Sheets + Make.com** (custom automated reporting)
- **Looker Studio** (free Google tool, pull from Sheets/Jobber API)
- **HighLevel** (built-in reporting for agencies managing multiple clients)

---

## The Lead Flow Automation Bundle: What to Sell

### Tier 1 — "Starter Automation" (Add-on to Voice Agent)
*$300 setup + included in monthly retainer*
- Post-job review request automation (SMS + email)
- Booking confirmation SMS
- Day-before reminder SMS
- Basic quote follow-up (2 emails)

### Tier 2 — "Growth Automation" (Full automation stack)
*$800 setup + $200-300/month add-on*
- Everything in Tier 1
- Full quote follow-up sequence (4 touchpoints)
- Post-job care sequence (3 touchpoints)
- Recurring treatment reminders
- Invoice payment automation
- Monthly performance report

### Tier 3 — "Full Moat" (Complete business system)
*$1,500-2,000 setup + $400-600/month*
- Everything in Tier 2
- Referral program setup
- Annual maintenance plan automation
- Loyalty/membership program
- Lead source tracking + monthly strategy review

---

## Tools Summary

| Tool | Role | Monthly Cost | NZ/AU Support |
|------|------|-------------|---------------|
| Jobber | CRM, scheduling, invoicing, reviews | $69-299 | ✅ Yes |
| ServiceM8 | CRM, scheduling, invoicing (AU-popular) | $29-349 | ✅ Strong AU |
| Tradify | Job management (NZ-founded) | $35-69 | ✅ NZ-native |
| Make.com | Automation backbone | $9-29 | ✅ Yes |
| Twilio | SMS delivery | Pay-per-use | ✅ NZ/AU numbers |
| HighLevel | All-in-one CRM + automation + white-label | $97-297 | ✅ Yes |
| NiceJob | Review automation specialist | $75-175 | ✅ Yes |
| FieldRoutes | Pest-control-specific platform | Custom | ✅ AU/NZ |
| OptimoRoute | Route optimisation | $19-49/driver | ✅ Yes |
# Digital Moat Strategies for Trade Businesses
*Research for Lead Flow — March 2026*
*Focus: What makes a small trade business hard to compete with digitally*

---

## What Is a "Digital Moat"?

A digital moat is a set of online assets and systems that compound over time, making a business progressively harder to displace from its local market. Unlike a traditional competitive advantage (better price, bigger team), a digital moat improves automatically with every customer interaction.

For a pest control or carpet cleaning business, a strong digital moat means:
- Their Google Business Profile has 200+ recent 5-star reviews
- They rank #1-3 in Google Maps for every key search term in their service area
- Their website converts 30%+ of visitors to enquiries
- They have 3-5 years of customer data that fuels personalised remarketing
- Their customers renew automatically and refer friends organically
- A competitor starting from scratch would need 3+ years to match their position

**Lead Flow's value proposition**: Lead Flow doesn't just set up a voice agent — it builds your digital moat.

---

## Moat Layer 1: Review Dominance

### Why Reviews Are the #1 Local Moat

Reviews are the single most important digital asset for a local trade business because:
1. **Google Maps ranking** — review count and velocity directly influence position in the local 3-pack (the top 3 businesses shown for "pest control Auckland")
2. **Social proof** — 93% of consumers read online reviews before choosing a local service
3. **Trust barrier** — a business with 150 reviews vs. one with 12 reviews has an enormous trust advantage that can't be faked overnight
4. **Compounding** — more reviews → better ranking → more calls → more jobs → more opportunities for reviews

### Review Velocity (Critical Insight)
- **Consistency beats spikes**: Google rewards businesses getting steady reviews (2-5/week) over those getting 50 in a day then nothing
- **Recency matters**: 20 reviews in the last 3 months outranks 50 reviews with nothing in 6 months
- **Quality signals**: Reviews mentioning specific service types, location keywords ("Auckland pest control", "Mt Eden carpet cleaning") carry extra weight
- **Response rate**: Businesses that respond to ALL reviews (positive and negative) signal engagement to Google

### Building the Review Moat

**Automated review generation (Lead Flow can deliver this):**
1. Post-job SMS at the optimal moment (24-48 hours after service)
2. Direct link to Google review page (no friction — opens straight to review form)
3. Personalised message with customer's name and service type
4. Follow-up if no review after 3 days
5. Track review velocity weekly — alert client if falling below target

**Review targets by moat stage:**
- Baseline (Month 1-3): 20-50 reviews, 4.5+ average
- Growing (Month 4-12): 50-150 reviews, 4.6+ average, 4+ new reviews/week
- Dominant (Year 2+): 150-500+ reviews, top 3 in all key service area searches

**Review response automation:**
- AI-generated personalised responses to all reviews
- Unique, natural-sounding (not template responses)
- Keywords naturally woven in ("Thanks for trusting us with your Auckland pest control!")
- Negative reviews get priority human review + empathetic response

---

## Moat Layer 2: Google Business Profile Dominance

### The GBP Is Your Most Valuable Digital Asset

For a trade business, a fully optimised Google Business Profile (GBP) is worth more than a website. It shows first in local search and drives the majority of calls.

### GBP Optimisation Checklist
- **Categories**: Primary + secondary categories (e.g., "Pest Control Service" + "Exterminator" + "Fumigation Service")
- **Service area**: Define exact suburbs/cities you serve (don't be too broad)
- **Services list**: Every individual service with descriptions and prices where possible
- **Q&A section**: Pre-populate with the 10 most common questions (with keyword-rich answers)
- **Photos**: Minimum 20 photos — team, vehicles, equipment, before/after, office
- **Posts**: Weekly Google Posts (offers, seasonal tips, news) signal an active business
- **Booking link**: Add online booking link directly to GBP
- **Call tracking number**: Use a tracked number to measure GBP-generated calls

### GBP + Voice Agent = Closed Loop
Lead Flow can create a powerful closed loop:
1. Customer finds business on Google Maps
2. Calls the GBP phone number
3. Voice agent answers 24/7, captures lead
4. Lead enters CRM automatically
5. Job completed → automated review request
6. New review → better GBP ranking → more calls → repeat

This loop strengthens the moat automatically with zero ongoing effort from the owner.

---

## Moat Layer 3: Local SEO & Search Dominance

### How Local SEO Compounds

Each piece of local SEO content creates a long-term asset that keeps generating leads:
- A blog post about "cockroach control in Auckland" published today will keep ranking and generating leads for 3-5 years
- A service area landing page for "pest control Remuera" ranks for that suburb permanently once established
- Local citation (directory listing) built once continues to strengthen authority indefinitely

### Local SEO Strategy for Trades

**Location landing pages** (high leverage):
Create individual pages for each suburb/area served:
- "Pest Control [Suburb]" — 300-500 words, service-specific, local landmarks
- "Carpet Cleaning [Suburb]" — same structure
- Each page captures suburb-specific search traffic
- A business serving 20 suburbs can rank for 20x more searches with 20 targeted pages

**Content moat (educational blog)**:
- Monthly pest/carpet care tips article
- Seasonal content ("Summer pest prevention guide Auckland")
- FAQ-style content that answers common questions
- Each article captures long-tail searches indefinitely

**Citation building**:
- Consistent NAP (Name, Address, Phone) across all directories
- Key NZ/AU directories: Yellow Pages NZ, Finda, Neighbourly, NoCowboys, True Local, ServiceSeeking
- Industry-specific: Pest Management Association of NZ, NZ Carpet Cleaning Association directories
- Yelp, Facebook Business, Bing Places, Apple Maps

**AI acceleration**: AI tools can create all location landing pages and blog content in a fraction of the time — Lead Flow can offer this as an upsell service.

---

## Moat Layer 4: Customer Data Ownership

### Your Customer Database Is a Strategic Asset

Every customer who books a job adds to a database that compounds in value over time:
- **Remarketing audiences**: Upload customer list to Google/Facebook → show ads specifically to past customers (much cheaper per conversion than cold ads)
- **Lookalike audiences**: Facebook/Google finds people who "look like" your best customers in your area
- **Reactivation campaigns**: Email/SMS dormant customers who haven't booked in 6+ months
- **Segmented marketing**: Target termite customers with termite-related content; carpet customers with seasonal cleaning offers

### CRM as a Competitive Moat

A well-maintained CRM (Jobber, ServiceM8, HubSpot) means:
- Every customer's full service history in one place
- Ability to personalise every communication
- Proactive outreach before customers need to search Google again
- First-mover advantage on recurring services (you remind them before a competitor can steal them)

**The competitor problem**: A new competitor entering the market starts with zero customer data. A business with 500+ customers in their CRM, all opted-in to communications, has a 3-5 year head start that money alone can't buy.

---

## Moat Layer 5: Online Booking & Scheduling Friction Removal

### Booking Friction Is Lost Revenue

Research shows:
- 67% of consumers prefer online booking over calling
- 35% of bookings happen outside business hours
- Businesses with online booking convert 25-40% more website visitors than phone-only businesses

### Building the Booking Moat
- **24/7 booking capability**: Voice agent (after hours) + website booking widget (always)
- **Frictionless booking**: Customer can book in under 60 seconds — name, address, service type, time
- **Instant confirmation**: SMS + email confirmation within seconds of booking
- **Reminder sequence**: Automated reminders reduce no-shows by 40-60%

**The competitive advantage**: Most small trade businesses still require a phone call during business hours. A business offering 24/7 phone + online booking is capturing the jobs that competitors are missing.

---

## Moat Layer 6: Loyalty & Membership Programs

### Turning One-Time Customers Into Annual Subscribers

A "pest protection plan" or "carpet care subscription" creates:
- **Predictable recurring revenue** for the business
- **Switching cost** for the customer (they're already committed and paid)
- **Pricing power** (subscribers get a discount vs. one-off, but business gets predictability)

### The Recurring Revenue Moat
**Example: "Annual Pest Protection Plan"**
- 4x general pest treatments/year
- Priority booking
- 15% discount vs. one-off rate
- Auto-billed quarterly
- Annual inspection included

At $149 × 4 = $596/year vs. $249 one-off treatment. Customer saves money; business gets reliable income and locked-in customers who don't shop around.

**AI-powered reactivation**: Automatically identify customers approaching renewal date → send personalised renewal offer → process payment → rebook all 4 treatments automatically.

---

## Moat Layer 7: Retargeting & Remarketing

### The Most Underutilised Tool in Trade Marketing

Retargeting shows ads to people who already visited your website or engaged with your Google Business Profile. These are warm leads:
- Website visitors who didn't book (hot — showed intent)
- Past customers (warm — already trust you)
- Video viewers on YouTube/Facebook (warm — showed interest)

### Retargeting Stack for Trades
- **Google Display Remarketing**: Show ads across the web to website visitors for 30-90 days
- **Facebook/Instagram Retargeting**: Show ads to website visitors + customer lists
- **Google Customer Match**: Upload customer emails → show ads specifically to past customers on Google Search
- **YouTube Retargeting**: Short videos (30 sec) targeted to past visitors

**AI-powered ad copy**: AI tools (like Jasper, Copy.ai) generate multiple ad variations for split testing — dramatically improves ROAS.

---

## How AI Accelerates Moat Building

Without AI, building a digital moat takes 2-3 years of manual effort. With AI:

| Moat Element | Manual Timeline | With AI + Lead Flow |
|-------------|----------------|---------------------|
| 100 reviews | 18-24 months | 6-9 months (automated requests) |
| 20 suburb landing pages | 3-4 months | 2-3 weeks (AI content generation) |
| 12 blog articles/year | 12+ hours/article | 1-2 hours/article with AI |
| Review responses | 15 min/day | Near-instant (AI drafts, human approves) |
| Post-job follow-up sequences | Set up once, runs forever | Built in 1 day |
| Customer reactivation | Manual campaign | Automated triggered sequences |

**Lead Flow positioning**: *"We don't just answer your phones — we build the digital infrastructure that makes you the obvious choice in your market for years to come."*

---

## Case Studies: Trade Businesses with Strong Digital Moats

### Case Study 1: Pest Control Company (US, FieldRoutes Customer)
- Started with 23 Google reviews
- Implemented automated post-job review requests
- Within 12 months: 200+ reviews, 4.8 stars
- Result: #1 in Google Maps for their city's primary pest control terms
- Estimated additional revenue: $180K/year from organic search

### Case Study 2: Carpet Cleaning (AU)
- Traditional business, relied on word of mouth
- Added automated booking, review requests, annual reminder sequences
- 18-month results: 3x annual revenue, expanded to second van
- Key metric: 65% of jobs now come from organic search (was 20% before)

### Case Study 3: HVAC Business (US, Avoca AI)
- HL Bowman: Implemented AI answering + automation
- Results: 100% call answer rate, 93% customer satisfaction, **70% revenue growth YoY**
- Key driver: Captured every after-hours call that previously went to voicemail

---

## The Digital Moat Score (Lead Flow Framework)

Create a "Digital Moat Score" for every prospect — shows them where they are vs. where they could be:

| Moat Element | Score | Max |
|-------------|-------|-----|
| Google reviews (quantity, recency) | ?/25 | 25 |
| GBP optimisation | ?/15 | 15 |
| Website (booking, speed, mobile) | ?/15 | 15 |
| Local SEO / suburb pages | ?/15 | 15 |
| CRM / customer database | ?/10 | 10 |
| Post-job automation | ?/10 | 10 |
| Remarketing capability | ?/5 | 5 |
| Recurring revenue / subscriptions | ?/5 | 5 |
| **Total** | **/100** | 100 |

**Use in sales**: Score a prospect's current digital moat (typically 15-35/100) → show them what it could look like at 70-85/100 with Lead Flow → frame every service as moat-building.
# Lead Flow Master Strategy
*Strategic Overview — March 2026*
*Synthesised from deep research across all 5 areas*

---

> **This is the most important file.** Read this first. The other 5 files go deeper on each area.

---

## The One-Sentence Strategy

Lead Flow builds digital moats for NZ/AU trade businesses — starting with an AI receptionist that captures every call, then layering automation, reputation, and content systems that compound over time to make each client the obvious choice in their local market.

---

## The Strategic Situation

### Where Glenn Is Now
- 2 clients: pest control + carpet cleaning
- Product: ElevenLabs voice agent via Make.com → SMS/email notification
- Revenue: ~$794/month MRR
- Market: NZ/AU trade businesses (vastly underserved by AI)

### The Market Opportunity

The NZ/AU trades AI market has a gaping hole at the small business level:
- Large players (Avoca AI, TalkAI.au) charge $2,500-10,000/month — inaccessible for small trades
- Generic tools (Goodcall, basic chatbots) don't understand trades businesses and have no NZ/AU focus
- No one is offering a **complete, productised, NZ/AU-focused AI + automation stack** for pest control, carpet cleaning, and similar trades at $400-1,000/month

**Lead Flow's opportunity**: Own this gap before it closes. The window is probably 12-24 months before copycats emerge.

---

## The Core Business Thesis

### Why Trades Are the Right Market
1. **High pain point**: Missed calls = directly lost jobs. ROI is immediately measurable.
2. **Low tech sophistication**: Easy to impress. Voice agent sounds like magic to them.
3. **Predictable workflows**: Every pest control call follows the same pattern — easy to automate.
4. **Recurring revenue natural**: Pest control is already a subscription business (quarterly treatments). AI extends this.
5. **Word of mouth within industry**: Trade owners talk to each other — one good case study spreads fast.
6. **NZ/AU gap**: Almost no one targeting this market locally.

### Why the Digital Moat Positioning is Brilliant
Most AI services agencies sell a product ("here's your AI receptionist"). Lead Flow sells an outcome ("here's your unbeatable position in the local market"). This is harder to cancel, easier to justify, and impossible for a cheap competitor to replicate.

The moat framing means:
- Every month of continued service makes the moat stronger
- Clients who cancel lose not just a tool but their competitive position
- Glenn can charge for the strategy, not just the technology
- As the moat gets built, the ROI becomes self-evident month after month

---

## The Product Architecture

### The Three-Layer Stack

```
LAYER 3: MOAT (Year 2+)
Local search dominance, content assets, brand authority
Makes them the obvious choice → passive inbound leads forever

LAYER 2: AUTOMATION (Months 3-12)
CRM, review engine, follow-up sequences, recurring billing
Turns captured leads into booked jobs, loyal customers, steady reviews

LAYER 1: CAPTURE (Months 1-3)
AI voice agent, website chatbot, missed call follow-up
Ensures 100% of leads are captured, never missed

```

**Every client starts at Layer 1** and is graduated up over time.  
Each layer compounds the one below it.  
Cancelling at any point means losing everything built above the exit point.

### The Three Tiers (Pricing)

| Tier | Setup | Monthly | What They Get |
|------|-------|---------|---------------|
| **Starter** | $799 | $397/month | Layer 1 complete (voice agent + lead capture + notifications + review automation) |
| **Growth** | $1,497 | $697/month | Layer 1 + 2 (full automation stack + Jobber integration + reporting) |
| **Full Moat** | $2,497 | $997/month | All 3 layers (voice + automation + GBP + content + SEO + retargeting) |

**Margin per client:**
- Starter: ~$277/month (at 500 min)
- Growth: ~$532/month
- Full Moat: ~$722/month

---

## The Revenue Roadmap

### 12-Month MRR Path

| Month | Clients | MRR | Profit (est 65%) |
|-------|---------|-----|----------------|
| Now | 2 | $794 | ~$516 |
| Month 3 | 5 | $2,500 | ~$1,625 |
| Month 6 | 10 | $6,000 | ~$3,900 |
| Month 9 | 15 | $10,000 | ~$6,500 |
| Month 12 | 20 | $15,000-17,000 | ~$10,000-11,000 |

Month 12 ($10K+ profit/month) is achievable with 20 clients and a mix of Tier 1/2/3.

### Path to $30K/Month MRR (30 clients, 18-24 months)
- Average client at $750/month (mix of tiers)
- 30 clients × $750 = $22,500 MRR
- Plus upsells (additional services per client)
- Plus setup fees ($3,000-5,000/month from new client acquisition)
- Plus affiliate revenue (Tradify, Jobber referral commissions)
- **Total potential at 30 clients: $28-35K/month revenue**

---

## The Competitive Advantage Stack

Why Lead Flow wins vs. every category of competitor:

| vs. | Lead Flow Advantage |
|-----|---------------------|
| Human answering services ($1,000-2,000/month) | 1/3 the price, better data capture, 24/7, never sick |
| Generic voice AI (Goodcall, etc.) | NZ/AU localisation, trades expertise, full automation stack |
| Enterprise players (Avoca AI, TalkAI) | 5-10x cheaper, small business focused, actual relationship |
| DIY (Make.com + ElevenLabs themselves) | Saves 40-80 hrs setup, ongoing management, expertise |
| Doing nothing | Stops missing calls, builds moat, has measurable ROI |

**The strongest position**: Lead Flow is the only productised, NZ/AU-native, trades-specialist AI agency at the small business price point. This is a category of one.

---

## The Digital Moat Concept (Core Positioning)

A digital moat is a set of compounding online assets that make a business progressively harder to compete with over time:

**The 7 Moat Layers Lead Flow Builds:**
1. **Review dominance** — 150-500+ recent Google reviews via automated review requests
2. **GBP mastery** — Fully optimised Google Business Profile, #1-3 in local Maps
3. **Local SEO** — Suburb landing pages, blog content, citation network
4. **Customer data** — CRM with 500+ past customers, ready for remarketing
5. **Online booking** — 24/7 booking capability (voice + web)
6. **Recurring revenue** — Annual maintenance plans and subscriptions
7. **Content authority** — Educational content that attracts future customers

**Why it matters strategically**: A competitor who enters the market today starts at 0/100 on the Digital Moat Score. A Lead Flow client at 18 months is at 75-85/100. That gap represents years of work — it can't be bought overnight.

**Use in sales**: Score every prospect (typically 15-35/100). Show them what 75/100 looks like. Frame every service as moat-building investment, not monthly expense.

---

## The Automation Stack for Pest Control (The Deliverables)

What Lead Flow actually delivers beyond the voice agent:

### Automations That Drive Immediate ROI
1. **Post-job review request** (24 hours after service): Biggest moat builder
2. **Booking confirmation SMS**: Reduces no-shows 40-60%
3. **Quote follow-up sequence**: Captures 20-35% of quotes that would otherwise be ignored
4. **Missed call follow-up SMS**: Recovers leads that would have gone to competitor
5. **Day-before reminder**: Reduces no-shows, improves planning
6. **Recurring treatment reminder**: Brings customers back automatically

### Automations That Build Long-Term Value
7. **Invoice payment automation**: Gets paid faster (40% improvement)
8. **Referral program automation**: Word-of-mouth amplified
9. **Annual membership/plan management**: Predictable recurring revenue
10. **Review response automation**: Every review answered, SEO boosted
11. **Reactivation campaigns**: Past customers brought back quarterly
12. **Monthly reporting automation**: ROI made visible, retention improved

### Tools Powering This Stack
- **Make.com**: The automation backbone connecting everything
- **ElevenLabs**: Voice agent (the front door)
- **Jobber / ServiceM8 / Tradify**: The CRM and job management engine
- **Twilio**: SMS delivery (NZ/AU numbers)
- **Google Sheets/Looker Studio**: Data storage and reporting
- **Tidio or HighLevel**: Website chat
- **OpenAI/Claude**: AI content generation (review responses, social posts, emails)

---

## Growth Strategy (The 2→20 Client Path)

### The Channel Hierarchy (by effectiveness)

**Phase 1 (Months 1-4)**: Outbound-led growth
1. Referrals from existing 2 clients (highest ROI)
2. LinkedIn direct outreach to NZ pest control / carpet cleaning owners
3. Cold email to owners found via Google Maps + Apollo.io
4. NZ trade business Facebook groups

**Phase 2 (Months 4-9)**: Channel diversification
5. Tradify NZ Partner Program ($250/referral, access to 7,000+ NZ trades)
6. Jobber affiliate program (commission + referrals)
7. Trade association events (PMANZ, carpet cleaning associations)
8. LinkedIn content marketing (building inbound)

**Phase 3 (Months 9-18)**: Scale and leverage
9. Accountant/bookkeeper referral partners
10. Trade supply store partnerships
11. Google Ads (small budget, high intent)
12. YouTube content / case study videos

### The Sales Process (7 Steps)
1. **Outreach** (personalised, problem-focused message)
2. **Discovery call** (understand their missed calls, current setup, pain)
3. **Live demo** (call the "demo business" live on the call — most powerful close)
4. **Frame the ROI** ("You're missing X jobs = $Y/month in lost revenue")
5. **Simple package pitch** (start with Starter, graduate to Growth)
6. **Remove friction** ("I'll have everything set up in 5 days, nothing for you to do")
7. **Follow-up** (if no close, 3-email sequence over 10 days)

### Objection Handling (The 4 Critical Ones)
| Objection | Response |
|-----------|----------|
| "Too expensive" | ROI calculation: 2 extra jobs/month > cost of Starter |
| "My customers won't like AI" | Do the live demo first, ask them if they could tell |
| "Not technical enough" | "You do nothing — I set it all up and manage it" |
| "I'll think about it" | Uncover real objection, or offer 7-day trial |

---

## Partnership Opportunities (Action Required)

### Immediate Actions
1. **Apply for Tradify NZ Partner Program** — tradifyhq.com/nz/partner-programme ($250/referral)
2. **Register for Jobber Affiliate** — getjobber.com/affiliates/ (up to 60% first month commission)
3. **Register ServiceM8 Partner** — servicem8.com/au/partners (for AU expansion)
4. **Contact PMANZ** (Pest Management Association NZ) about speaking/membership

### Medium-Term Partnerships
- NZ Carpet & Textile Cleaners Association
- Trade accountants who specialise in pest control/carpet cleaning
- Pest control supply distributors (Garrards, etc.)
- Tradify "Expert" status (reseller level)

---

## Operational Priorities (Next 90 Days)

### Glenn's Priority Stack

**Week 1-2: Foundation**
- [ ] Create the "Lead Flow Demo Business" (callable voice agent for sales demos)
- [ ] Document current client onboarding as a checklist (will become the template)
- [ ] Apply to Tradify Partner Program and Jobber Affiliate Program
- [ ] Set up Calendly booking page for discovery calls
- [ ] Create simple Lead Flow website with service tiers and case study (even 2 clients)

**Month 1: Outbound**
- [ ] Identify 50 NZ pest control / carpet cleaning businesses on LinkedIn
- [ ] Send 10-15 personalised DMs per week (pain-focused, not product-focused)
- [ ] Join 3-5 relevant NZ trades Facebook groups
- [ ] Create 1 LinkedIn post per week showing real results from clients

**Month 2-3: Convert + Scale**
- [ ] Target: 3 new clients signed
- [ ] Upgrade current clients from Tier 1 → Tier 2 (add automation layer)
- [ ] Build first post-job automation sequence (Make.com → SMS review request)
- [ ] Get first written case study from original 2 clients
- [ ] Create Tier 3 "Full Moat" capability (GBP + suburb landing page template)

---

## The 5 Most Important Things Glenn Should Know

### 1. The Voice Agent Is the Door, Not the Product
The voice agent is how you get clients. The automation stack is why they stay. The digital moat is why they become evangelists. Sell the voice agent to get in the door, but always be building toward the full moat.

### 2. Reviews Are the Highest-Leverage Activity Right Now
For every client, setting up automated review requests is the single highest-ROI automation. It costs almost nothing to build, delivers visible results within 30-60 days, and directly impacts their Google Maps ranking. Lead every client onboarding with this.

### 3. The Demo Is the Close
Every sales conversation should include a live demonstration of the voice agent. "Let me call my demo business right now and you can hear it" — this converts better than any brochure, email, or explanation. Build the demo business this week.

### 4. Tradify Is the Shortest Path to 10 Clients
The Tradify NZ Partner Program gives access to exactly the ICP — NZ trades businesses that are already invested in their software infrastructure and looking to grow. $250/referral is a nice bonus; the real value is warm introductions to pre-qualified prospects. Apply immediately.

### 5. Productise Early — It's the Only Way to Scale
Every extra client added without systemisation adds to Glenn's personal workload. By Month 4-5, every service Lead Flow offers should be a documented, repeatable process that a trained VA could follow. This is the only path to 20+ clients without burning out.

---

## The Long Game: Year 2 Vision

By Month 18-24, Lead Flow should be:

**Financially:**
- 25-35 clients
- $20,000-30,000/month MRR
- 60-65% margin = $12,000-19,500/month profit
- Predictable, recurring revenue

**Operationally:**
- 1-2 VAs handling delivery, Glenn focused on sales/strategy
- Documented SOPs for every service
- Automated onboarding and reporting processes

**Market position:**
- Known as "the NZ AI agency for trades"
- Speaking at PMANZ conferences
- Case studies featuring 5+ clients with measurable results
- Tradify / Jobber recognised partner
- Inbound leads from LinkedIn and content

**Product evolution:**
- Own-brand client portal (white-labelled HighLevel)
- Industry-specific knowledge base library (pest control, carpet, HVAC, plumbing)
- "Lead Flow Score" as standard industry benchmark for digital moat measurement
- Potential: Expand to AU market with dedicated vertical focus (HVAC, plumbing)

---

## Summary: What Lead Flow Is Building

Not a voice agent service.  
Not a digital marketing agency.  
Not an automation consultant.

**Lead Flow is the company that makes NZ/AU trade businesses unbeatable in their local market — using AI to capture every customer, automation to keep them, and content to attract the next one.**

That's the positioning.  
That's the moat.  
That's worth $997/month and grows stronger every month.

---

*Files in this research series:*
- `pest-control-automations.md` — Full automation opportunity map
- `digital-moat-strategies.md` — Moat concept and tactics
- `leadflow-business-model.md` — Pricing, tiers, onboarding, retention
- `ai-tools-for-trades.md` — AI tools beyond voice agents
- `leadflow-growth-strategy.md` — How to scale from 2 to 20+ clients
- **`leadflow-master-strategy.md`** — This file (master overview)
