# Research Complete ✅

**Topic**: ElevenLabs Conversational AI Voice Agents
**Completed**: March 22, 2026
**Scope**: Platform capabilities, prompting, knowledge bases, tools/webhooks, Make integration, gotchas, pricing

---

## Files Saved

| File | Status | Notes |
|------|--------|-------|
| `elevenlabs-platform.md` | ✅ Complete | Full platform overview, architecture, pricing tables, concurrency limits, deployment options |
| `elevenlabs-prompting.md` | ✅ Complete | Prompt structure, templates, call flow patterns, text normalisation, validation, temperature |
| `elevenlabs-knowledge-bases.md` | ✅ Complete | RAG guide, upload methods, size limits by plan, example KB content for trade businesses |
| `elevenlabs-tools-webhooks.md` | ✅ Complete | Server tools, client tools, system tools, post-call webhooks, auth, integration patterns |
| `elevenlabs-make-integration.md` | ✅ Complete | Full Make setup guide, 4 scenario examples, troubleshooting, MVS patterns |
| `elevenlabs-gotchas.md` | ✅ Complete | 40+ specific gotchas across pricing, KB, prompting, telephony, compliance |
| `elevenlabs-master-summary.md` | ✅ Complete | Concise synthesis of everything, deployment checklist, quick-start guidance |

---

## Key Findings

- **Pricing**: $0.10/min (Creator plan), $0.08/min (Business annual). LLM costs currently absorbed but may change.
- **Concurrency**: Creator plan = 5 concurrent calls. Free = 2. Business = 15.
- **Make integration**: Official native integration. ElevenLabs provides a dedicated setup guide at elevenlabs.io/agents/integrations/make
- **Architecture**: ASR → LLM → TTS + proprietary turn-taking model. All four components work together.
- **RAG**: Built in, sub-200ms. Creator plan gets 20MB of indexed documents.
- **Phone**: Native Twilio integration (10-15 min setup) + SIP trunking for other providers.
- **Biggest gotchas**: URL KB is snapshot only; LLM costs not yet in per-minute price; Make scenarios need to stay < 5s for real-time calls.

---

## Sources Used

- elevenlabs.io/docs (official documentation)
- elevenlabs.io/blog (product announcements)
- elevenlabs.io/conversational-ai (product page)
- elevenlabs.io/agents/integrations/make (Make integration page)
- elevenlabs.io/agents/integrations/twilio (Twilio integration page)
- elevenlabs.io/pricing (pricing page)
- flexprice.io/blog/elevenlabs-pricing-breakdown (third-party pricing analysis)
- elevenlabs.io/blog/we-cut-our-pricing-for-conversational-ai (pricing announcement)
- elevenlabs.io/blog/conversational-ai-2-0 (v2 feature announcement)
