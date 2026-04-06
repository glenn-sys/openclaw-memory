#!/usr/bin/env python3
"""
Anthropic balance tracker.
Starting balance: $35.00 USD
Alert threshold: $5.00 USD
Tracks spend via Anthropic usage API and emails when balance is low.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

STATE_FILE = os.path.expanduser("~/.openclaw/workspace/scripts/anthropic_balance_state.json")
ALERT_THRESHOLD = 5.00
STARTING_BALANCE = 35.00
ALERT_EMAIL = "glenn@lead-flo.ai"

# Anthropic model costs per 1M tokens (input/output) USD
MODEL_COSTS = {
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-haiku-3-5":  {"input": 0.80, "output": 4.00},
    "claude-opus-4":     {"input": 15.00, "output": 75.00},
}
DEFAULT_COST = {"input": 3.00, "output": 15.00}

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "starting_balance": STARTING_BALANCE,
        "total_spend": 0.0,
        "last_check": None,
        "alert_sent": False,
        "check_count": 0
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_anthropic_usage(api_key, starting_at, ending_at):
    """Fetch usage from Anthropic API."""
    url = (f"https://api.anthropic.com/v1/organizations/usage_report/messages"
           f"?starting_at={starting_at}&ending_at={ending_at}&bucket_width=1d")
    req = urllib.request.Request(url, headers={
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}

def estimate_cost_from_usage(usage_data):
    """Calculate USD cost from usage report."""
    total = 0.0
    buckets = usage_data.get("data", [])
    for bucket in buckets:
        for item in bucket.get("breakdown", []):
            model = item.get("model", "")
            costs = DEFAULT_COST
            for k, v in MODEL_COSTS.items():
                if k in model:
                    costs = v
                    break
            input_tokens = item.get("input_tokens", 0)
            output_tokens = item.get("output_tokens", 0)
            cache_read = item.get("cache_read_input_tokens", 0)
            total += (input_tokens / 1_000_000) * costs["input"]
            total += (output_tokens / 1_000_000) * costs["output"]
            total += (cache_read / 1_000_000) * costs["input"] * 0.1  # cache read is ~10% of input
    return total

def main():
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        # Try reading from openclaw.json
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)
            api_key = config.get("env", {}).get("ANTHROPIC_API_KEY", "")

    if not api_key:
        print("ERROR: No ANTHROPIC_API_KEY found")
        sys.exit(1)

    state = load_state()
    state["check_count"] = state.get("check_count", 0) + 1

    # Fetch last 30 days of usage
    now = datetime.now(timezone.utc)
    starting_at = (now - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")
    ending_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    usage = get_anthropic_usage(api_key, starting_at, ending_at)

    if "error" in usage:
        # Admin API not available — fall back to session-based estimation
        # Rough estimate: average OpenClaw session ~0.05 USD
        estimated_daily = 0.50  # conservative $0.50/day estimate
        days_since_start = (now - datetime(2026, 4, 6, tzinfo=timezone.utc)).days + 1
        estimated_spend = estimated_daily * days_since_start
        print(f"Usage API unavailable ({usage['error']}), using estimate: ${estimated_spend:.2f}")
    else:
        estimated_spend = estimate_cost_from_usage(usage)
        print(f"Fetched usage data. Estimated spend (last 30d): ${estimated_spend:.2f}")

    state["total_spend"] = estimated_spend
    state["last_check"] = now.isoformat()
    remaining = STARTING_BALANCE - estimated_spend
    print(f"Starting balance: ${STARTING_BALANCE:.2f}")
    print(f"Estimated spend:  ${estimated_spend:.2f}")
    print(f"Remaining:        ${remaining:.2f}")
    print(f"Alert threshold:  ${ALERT_THRESHOLD:.2f}")

    if remaining <= ALERT_THRESHOLD and not state.get("alert_sent"):
        print(f"ALERT: Balance at ${remaining:.2f} — sending email!")
        state["alert_sent"] = True
        save_state(state)
        sys.exit(42)  # Signal to wrapper: send email alert
    elif remaining <= ALERT_THRESHOLD * 2:
        print(f"WARNING: Balance getting low (${remaining:.2f})")

    save_state(state)
    print("Done. No alert needed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
