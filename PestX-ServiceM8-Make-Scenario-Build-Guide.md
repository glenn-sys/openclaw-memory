# PestX ServiceM8 Integration — Make.com Scenario Build Guide

## Overview
This scenario connects ElevenLabs post-call webhooks → Make → ServiceM8 contact search/create → job ticket creation.

**Time estimate:** 25–30 minutes  
**Complexity:** Medium (6 modules, 1 conditional router, phone normalisation)

---

## Step 1: Create New Scenario

1. Log into **make.com**
2. Go to **Scenarios**
3. Click **Create a new scenario**
4. Name it: `PestX ServiceM8 Integration - Voice Agent → Job Tickets`
5. Set team to: `My Team` (ID: 1632137)
6. **Save**

---

## Step 2: Add Webhook Trigger

1. Click the **+** to add the first module
2. Search for **Webhooks** → select **Webhooks > Custom Webhook**
3. Click **Add**
4. A webhook URL will be generated. **Copy this URL** — you'll give it to ElevenLabs
   - Format: `https://hook.make.com/webhooks/xxx/yyy/zzz`
5. In the webhook settings:
   - **IP whitelist:** Leave blank (allow all)
   - **Data structure:** Leave auto-detect
6. **Save** the module

---

## Step 3: Extract & Normalise Phone Number

1. Add a new module: **Tools > Set multiple variables** (or **Tools > Text aggregator**)
   - This will parse the incoming webhook and normalise the phone number

**Module settings:**
```
Variable 1: caller_phone_raw
Value: {{1.caller_phone}}

Variable 2: caller_phone_normalised
Value: (use regex to convert E.164 → +61 format)
```

**Phone normalisation logic:**
- Input: `+61412345678` (already in correct format)
- Input: `0412345678` (local AU format, needs +61 prefix)
- Regex formula: `{{regex(1.caller_phone; "/^0/"; "+61"; "g")}}`
  - This replaces leading `0` with `+61`
- If already has `+61`, it passes through unchanged

**Alternative:** Use **Tools > JavaScript** for more control:
```javascript
let phone = data.caller_phone;
if (phone.startsWith("0")) {
  phone = "+61" + phone.slice(1);
}
output = phone;
```

2. Set other variables:
```
Variable 3: pest_type
Value: {{1.variables.pest_type}}

Variable 4: call_notes
Value: {{1.transcript}}

Variable 5: caller_name
Value: {{1.variables.name}}

Variable 6: call_timestamp
Value: {{1.call_timestamp}}
```

3. **Save**

---

## Step 4: Search ServiceM8 for Existing Contact

1. Add new module: **HTTP > Make a request**
2. **Module name:** "Search ServiceM8 Contact by Phone"

**Settings:**
```
URL: https://api.servicem8.com/api_contacts.html
Method: GET
Headers:
  Authorization: Bearer [SERVICEM8_API_KEY_HERE]
  Content-Type: application/json

Query parameters:
  phone: {{3.caller_phone_normalised}}
  limit: 1
```

3. **Advanced settings:**
   - **Parse response:** ON
   - **Store response headers:** ON

4. **Save**

This returns contact(s) matching the phone number. The response structure will be:
```json
{
  "data": [
    {
      "id": "contact_id_123",
      "name": "John Doe",
      "phone": "+61412345678"
    }
  ]
}
```

---

## Step 5: Router — Conditional Branch (Contact Found vs Not Found)

1. Add a **Router** module (Tools > Router)
2. Configure **two routes:**

**Route 1: Contact Found**
- Condition: `{{length(4.data) > 0}}`
- Meaning: If ServiceM8 returned at least 1 contact

**Route 2: Contact Not Found**
- Condition: `{{length(4.data) == 0}}`
- Meaning: If ServiceM8 returned no contacts

---

## Step 6a: Contact FOUND Path — Create Job Only

**Coming off Route 1 of the Router:**

1. Add new module: **HTTP > Make a request**
2. **Module name:** "Create ServiceM8 Job (Existing Contact)"

**Settings:**
```
URL: https://api.servicem8.com/api_jobs.html
Method: POST
Headers:
  Authorization: Bearer [SERVICEM8_API_KEY_HERE]
  Content-Type: application/json

Body (JSON):
{
  "contact_id": "{{4.data[0].id}}",
  "job_type": "{{3.pest_type}}",
  "notes": "Inbound call summary:\nCaller: {{3.caller_name}}\nPhone: {{3.caller_phone_normalised}}\n\nCall notes:\n{{3.call_notes}}\n\nCall time: {{3.call_timestamp}}",
  "date": "{{formatDate(now; "YYYY-MM-DD")}}",
  "status": "pending"
}
```

3. **Save**

---

## Step 6b: Contact NOT FOUND Path — Create Contact Then Job

**Coming off Route 2 of the Router:**

### Step 6b.1: Create New Contact

1. Add new module: **HTTP > Make a request**
2. **Module name:** "Create ServiceM8 Contact"

**Settings:**
```
URL: https://api.servicem8.com/api_contacts.html
Method: POST
Headers:
  Authorization: Bearer [SERVICEM8_API_KEY_HERE]
  Content-Type: application/json

Body (JSON):
{
  "first_name": "{{split(3.caller_name; " ")[0]}}",
  "last_name": "{{split(3.caller_name; " ")[1]}}",
  "phone": "{{3.caller_phone_normalised}}",
  "email": "",
  "source": "voice_agent_inbound"
}
```

3. **Save**

The response will include the new `contact_id`:
```json
{
  "id": "new_contact_id_456",
  "phone": "+61412345678"
}
```

### Step 6b.2: Create Job with New Contact

1. Add new module: **HTTP > Make a request**
2. **Module name:** "Create ServiceM8 Job (New Contact)"

**Settings:**
```
URL: https://api.servicem8.com/api_jobs.html
Method: POST
Headers:
  Authorization: Bearer [SERVICEM8_API_KEY_HERE]
  Content-Type: application/json

Body (JSON):
{
  "contact_id": "{{5.id}}",
  "job_type": "{{3.pest_type}}",
  "notes": "Inbound call summary:\nCaller: {{3.caller_name}}\nPhone: {{3.caller_phone_normalised}}\n\nCall notes:\n{{3.call_notes}}\n\nCall time: {{3.call_timestamp}}",
  "date": "{{formatDate(now; "YYYY-MM-DD")}}",
  "status": "pending"
}
```

3. **Save**

---

## Step 7: Error Handling (Optional but Recommended)

Add error handling to both HTTP request modules:

1. Click on each HTTP module
2. Go to **Error handling**
3. Set:
   - **Throw error on HTTP error status:** ON
   - **Ignore all errors:** OFF

This way if ServiceM8 API fails, the scenario will log it clearly.

---

## Final Setup

1. **Save the scenario**
2. Click the **clock icon** to enable the scenario
3. Set to **Running**

---

## Give ElevenLabs the Webhook URL

Copy the webhook URL from **Step 2** and configure it in ElevenLabs agent settings:

**Post-call webhook URL:**
```
https://hook.make.com/webhooks/[unique-id]/[unique-id]/[unique-id]
```

**Webhook payload format (ElevenLabs sends this):**
```json
{
  "call_id": "call_123",
  "call_status": "completed",
  "call_timestamp": "2026-04-07T22:15:00Z",
  "caller_phone": "+61412345678",
  "duration": 180,
  "transcript": "Customer said they have wasps in the roof...",
  "variables": {
    "name": "John Smith",
    "pest_type": "wasps",
    "location": "roof area"
  }
}
```

---

## ServiceM8 API Fields Reference

**When you have the API key**, replace `[SERVICEM8_API_KEY_HERE]` in all HTTP modules.

### Contact Search Response
```json
{
  "data": [
    {
      "id": "contact_id",
      "name": "Full Name",
      "phone": "+61412345678",
      "email": "email@domain.com"
    }
  ]
}
```

### Job Creation Response
```json
{
  "id": "job_id_789",
  "contact_id": "contact_id",
  "job_type": "wasps",
  "status": "pending",
  "created_at": "2026-04-07T22:15:00Z"
}
```

---

## Testing

1. **Trigger a test call** via ElevenLabs agent
2. Check **Make scenario execution history** (click the scenario → **Execution history**)
3. Look for:
   - ✅ Webhook received (Step 2)
   - ✅ Phone normalised correctly (Step 3)
   - ✅ ServiceM8 search result (Step 4)
   - ✅ Router condition evaluated (Step 5)
   - ✅ Contact found OR contact + job created (Step 6)

If any step fails, click that module in the history to see the error.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Webhook not triggering | Check ElevenLabs webhook URL is exact copy. Test by calling the agent. |
| Phone search returns nothing but contact exists | Check phone format in ServiceM8 (may need different normalisation regex). |
| 401 error on ServiceM8 API calls | API key is wrong or expired. Verify in ServiceM8 settings. |
| Contact created but job not created | Check contact_id is being passed correctly from Step 6b.1 → Step 6b.2. |

---

## Next Steps

- Once tested and working, give this scenario to Scott Lawton at PestX as a demo
- Monitor the first week of calls to catch any data formatting issues
- Once stable, consider adding SMS confirmation to the customer after job creation

