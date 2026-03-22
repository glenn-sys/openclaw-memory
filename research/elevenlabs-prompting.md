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
