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
