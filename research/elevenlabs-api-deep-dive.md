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
