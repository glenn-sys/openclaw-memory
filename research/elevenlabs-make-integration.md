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
