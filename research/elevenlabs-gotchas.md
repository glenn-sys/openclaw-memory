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
