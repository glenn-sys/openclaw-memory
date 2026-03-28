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
