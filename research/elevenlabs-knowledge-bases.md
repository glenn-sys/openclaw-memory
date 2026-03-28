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
