# Deep Research Complete

**Completed**: March 2026
**Research depth**: Level 2 (advanced, practitioner-level)

## Files Created

1. **`elevenlabs-advanced-prompting.md`** — Advanced prompting with real examples, emotional handling, v3 expressive mode, multi-agent patterns, data collection/analysis, prompt length guidance
2. **`elevenlabs-api-deep-dive.md`** — Full API reference (create/update/delete agents, knowledge base API, conversations API, post-call webhook payload structure, dynamic variables, Python SDK examples)
3. **`elevenlabs-community-knowledge.md`** — Community insights from Reddit (r/ElevenLabs, r/AI_Agents, r/automation), YouTube tutorials found, common failure patterns, what makes agents sound unnatural, 18 practitioner tips
4. **`elevenlabs-trade-business.md`** — Trade-specific knowledge (what callers ask, emergency protocols, industry FAQ content templates, real case study results, NZ/AU compliance, seasonal call patterns)
5. **`elevenlabs-competitive-intel.md`** — Competitive landscape (Synthflow, Retell, Vapi, Bland, Goodcall, Avoca AI), market gaps, agency pricing models, NZ/AU market opportunities
6. **`elevenlabs-make-advanced.md`** — Advanced Make patterns (5 integration patterns, error handling, incomplete executions, data validation, performance optimisation, production checklist)
7. **`elevenlabs-master-summary-v2.md`** — Updated master summary incorporating all V1 + V2 research

## Key Discoveries

### Platform
- Eleven v3 Conversational model (same price $0.08/min) adds expressive mode — emotional delivery adaptation
- Speculative turn config reduces latency (new Feb 2026)
- Silence billed at 5% of per-minute rate
- Max system prompt: 2MB
- Conversation API has powerful filtering (by tool success/error, language, duration, full-text search)

### API
- Full CRUD for agents, knowledge base, conversations
- Twilio personalization enables CRM lookup before call starts
- Post-call webhook payload includes LLM token costs, full transcript, analysis results
- Dynamic variables (preferred over overrides): inject runtime data with `{{variable_name}}`

### Community
- Voice quality is ElevenLabs' #1 differentiator (community consensus)
- Biggest lever for natural sound: prompt structure, not voice selection
- YouTube tutorial: "Build anything with elevenlabs voice agent and make.com!" (Jan 2025) — directly relevant
- Common failure: tool called too early (before data collected) or too late (after goodbye)

### Trades/NZ/AU
- Real results: 10-86% booking rate increase from AI agents (Avoca AI case studies)
- Emergency call protocol is the highest-value feature for trades
- NZ compliance: Privacy Act 2020 + Marketing Association Code
- AU compliance: Telecommunications Act + Do Not Call Register + strict calling hours
- Gap: No one servicing small NZ/AU trades at accessible price points

### Competitive
- Agency pricing: $500-2,000 setup + $300-1,000/month
- VoiceAIWrapper = white-label platform ($29-499/month) for agencies
- Market gap: NZ/AU localised, small-business-priced AI receptionist for trades

### Make
- 5 error handlers: Break, Resume, Ignore, Commit, Rollback
- Break + incomplete executions = safe retry pattern
- Always return 200 quickly; process async for post-call
- Data Store (not Sheets) for real-time availability checks — much faster
