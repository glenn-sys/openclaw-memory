# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## Google Drive
- Mounted path: ~/Library/CloudStorage/GoogleDrive-glenn@lead-flo.ai
- Access via: Mac node (mike's MacBook Pro)
- Account: glenn@lead-flo.ai


## Web Search
- Use COMPOSIO_SEARCH_WEB (via Composio) for all web search needs
- Do NOT use the native web_search tool or ask about Brave API — it is not configured
- COMPOSIO_SEARCH_WEB uses Exa and is always available via the Composio connection
- For news specifically, use COMPOSIO_SEARCH_NEWS
- For fetching a URL's content, use COMPOSIO_SEARCH_FETCH_URL_CONTENT

