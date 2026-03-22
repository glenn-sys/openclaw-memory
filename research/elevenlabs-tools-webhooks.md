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
