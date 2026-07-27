"""Deliver messages about crawled items."""

import json
import os
import urllib.error
import urllib.request

WEBHOOK_ENV = "DISCORD_WEBHOOK_URL"
TIMEOUT = 10


def format_message(items: list[dict]) -> str:
    """Render *items* into a single notification body.

    One line per item, using its ``title``. Returns an empty string when there
    is nothing to report, so callers can skip sending.
    """
    return "\n".join(f"- {item.get('title', '')}" for item in items)


def send(message: str) -> bool:
    """Deliver *message* to the Discord webhook named by DISCORD_WEBHOOK_URL.

    Returns True when the webhook accepts it. A missing URL or a failed
    request reports the problem and returns False rather than raising, so
    the notification step never aborts a pipeline run.
    """
    url = os.environ.get(WEBHOOK_ENV)
    if not url:
        print(f"{WEBHOOK_ENV} is not set; skipping notification")
        return False

    payload = json.dumps({"content": message}).encode("utf-8")
    request = urllib.request.Request(
        url, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return 200 <= response.status < 300
    except urllib.error.URLError as error:
        print(f"notification failed: {error}")
        return False
