import os
import urllib.request
import json


class AnthropicProvider:
    """Anthropic Claude."""

    DEFAULT_MODEL = "claude-haiku-4-5-20251001"
    API_BASE = "https://api.anthropic.com/v1/messages"

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set. Pass api_key= or export ANTHROPIC_API_KEY.")
        self.model = model or self.DEFAULT_MODEL

    def complete(self, system: str, user: str) -> str:
        payload = json.dumps({
            "model": self.model,
            "max_tokens": 2048,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }).encode()
        req = urllib.request.Request(
            self.API_BASE,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        return data["content"][0]["text"]
