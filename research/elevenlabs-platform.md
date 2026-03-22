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
