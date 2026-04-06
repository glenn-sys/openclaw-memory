# Workspace Cleanup Checklist

## 1. Agent Consolidation
Audit all current agents and keep only what's needed. Target structure below.

### ✅ Agents to Keep (Target State)

**Client Agents**
- [ ] Agent: **Scott / PestX** — all PestX client ops (Rockhampton, AU)
- [ ] Agent: **Pestaside** — Auckland pest control client ops
- [ ] Agent: **PestFree Demo** — sales demo agent (keep for now)
- [ ] Agent: *(next client)* — create when onboarded

**Lead-Flo Business**
- [ ] Agent: **Lead-Flo Ops** — day-to-day business operations, admin, finances
- [ ] Agent: **Lead-Flo Research** — market research, competitor intel, opportunities
- [ ] Agent: **Marketing & Brand** — marketing strategy, brand assets, content
- [ ] Agent: **Marketing Opps** — specific campaign ideas and pipeline

**Personal**
- [ ] Agent: **Psyche** — personal psychology, mindset, journaling
- [ ] Agent: **Physical** — training, fitness coaching, programming
- [ ] Agent: **Novel** — creative writing and story development

**Main**
- [ ] Agent: **Main** — general assistant, catch-all

### ❌ Agents to Remove / Archive
- [ ] Review full agent list and identify stale/duplicate agents
- [ ] Archive unused workspaces (don't delete — just disable)
- [ ] Remove stale Discord channel bindings

---

## 2. Channels & Routing
- [ ] Confirm Discord is the only external channel (done — Slack/Telegram/WhatsApp removed ✅)
- [ ] Bind each agent to its own dedicated Discord channel
- [ ] Confirm webchat works as fallback for all agents
- [ ] Remove any stale channel bindings from old agents

---

## 3. Workspaces
- [ ] Check each agent workspace dir — remove empty/stale ones
- [ ] Ensure each active agent has: SOUL.md, USER.md, AGENTS.md
- [ ] Consolidate research files — move to relevant agent workspace
- [ ] Clean up main workspace root (archive old files to `/archive/`)

---

## 4. Memory & Context
- [ ] Review MEMORY.md — remove outdated entries
- [ ] Ensure each agent workspace has up-to-date context
- [ ] Delete bootstrap files from any agents that still have them

---

## 5. Integrations & Keys
- [ ] Confirm Anthropic key is working ✅ (done today)
- [ ] Store ElevenLabs API key securely
- [ ] Confirm Gmail + Google Drive connections active ✅
- [ ] Review any other API keys and store centrally

---

## 6. Once Clean — Next Steps
- [ ] Growth planning session — targets, timeline, next clients
- [ ] Marketing strategy build-out
- [ ] Content calendar and lead gen plan
