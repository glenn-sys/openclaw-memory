---
name: generate-and-email-image
description: Generate an image with Nano Banana Pro (Gemini) and email it to someone. Use when asked to "generate an image and email it", "create an image and send it", or similar.
---

# Generate and Email an Image

Use this skill whenever the user asks to generate an image AND send/email it to someone.

## Prerequisites
- GEMINI_API_KEY must be set (stored in ~/.zshrc — source it or pass via --api-key)
- Nano Banana Pro script: `~/.openclaw/skills/nano-banana-pro/scripts/generate_image.py`
- uv: `/Users/clawbot/.local/bin/uv`

## Step-by-step workflow

### 1. Generate the image (local Mac)
```bash
GEMINI_API_KEY="AIza..." /Users/clawbot/.local/bin/uv run ~/.openclaw/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "your prompt here" \
  --filename "/Users/clawbot/.openclaw/workspace/YYYY-MM-DD-HH-MM-descriptive-name.png" \
  --resolution 2K \
  --api-key "AIza..."
```
- Use 2K for most requests, 4K only for final high-res
- Timestamp filename: `date +%Y-%m-%d-%H-%M`

### 2. Compress to under 2MB (Composio Gmail limit is ~2MB)
```bash
sips -Z 1200 /path/to/original.png --out /tmp/image-compressed.png
ls -lh /tmp/image-compressed.png  # confirm < 2MB
```

### 3. Upload compressed file to temp host (bridges local → Composio remote sandbox)
```bash
curl -s -F "file=@/tmp/image-compressed.png" "https://tmpfiles.org/api/v1/upload"
# Returns: {"status":"success","data":{"url":"http://tmpfiles.org/XXXXXXXX/filename.png"}}
# Direct download URL: https://tmpfiles.org/dl/XXXXXXXX/filename.png
```

### 4. In COMPOSIO_REMOTE_WORKBENCH — download and upload to get s3key
```python
import requests
r = requests.get("https://tmpfiles.org/dl/XXXXXXXX/filename.png", timeout=60)
r.raise_for_status()
with open('/tmp/img.png', 'wb') as f:
    f.write(r.content)

result, error = upload_local_file('/tmp/img.png')
s3key = result.get("s3key")
print("s3key:", s3key)
```

### 5. Send email with attachment via GMAIL_SEND_EMAIL
```python
send_result, send_error = run_composio_tool("GMAIL_SEND_EMAIL", {
    "recipient_email": "recipient@example.com",
    "subject": "Your image",
    "body": "Here's your image!",
    "user_id": "me",
    "attachment": {
        "name": "image.png",
        "mimetype": "image/png",
        "s3key": s3key
    }
})
print("Sent:", send_result.get("data", {}).get("labelIds"))
```

## Common failures
- **429 quota**: GEMINI_API_KEY project doesn't have billing enabled — ask Glenn to enable billing
- **413 payload too large**: Image > 2MB — compress harder: `sips -Z 800 ...`
- **gog gmail send**: Also supports `--attach /path/to/file` but requires `gog auth` OAuth setup (not configured yet)

## Notes
- tmpfiles.org links expire after 1 hour — do the full workflow in one session
- Glenn's email: glenn@lead-flo.ai
- Default resolution: 2K (good quality, manageable size)
