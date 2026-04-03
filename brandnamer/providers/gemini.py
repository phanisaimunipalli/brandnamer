import os
import urllib.request
import json


class GeminiProvider:
    """Google Gemini — free tier works well for this use case."""

    DEFAULT_MODEL = "gemini-2.0-flash"
    API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set. Pass api_key= or export GEMINI_API_KEY.")
        self.model = model or self.DEFAULT_MODEL

    def complete(self, system: str, user: str) -> str:
        url = f"{self.API_BASE}/{self.model}:generateContent?key={self.api_key}"
        payload = json.dumps({
            "contents": [{"role": "user", "parts": [{"text": f"{system}\n\n{user}"}]}],
            "generationConfig": {"temperature": 0.9, "maxOutputTokens": 2048},
        }).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
        return data["candidates"][0]["content"]["parts"][0]["text"]
