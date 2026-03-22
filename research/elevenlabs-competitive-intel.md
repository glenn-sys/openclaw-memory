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
