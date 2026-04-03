import os
import urllib.request
import json


class OpenAIProvider:
    """OpenAI — GPT-4o / GPT-4-turbo etc."""

    DEFAULT_MODEL = "gpt-4o-mini"
    API_BASE = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not set. Pass api_key= or export OPENAI_API_KEY.")
        self.model = model or self.DEFAULT_MODEL

    def complete(self, system: str, user: str) -> str:
        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.9,
            "max_tokens": 2048,
        }).encode()
        req = urllib.request.Request(
            self.API_BASE,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        return data["choices"][0]["message"]["content"]
