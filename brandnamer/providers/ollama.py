import urllib.request
import json


class OllamaProvider:
    """Local Ollama — no API key required."""

    DEFAULT_MODEL = "qwen2.5:14b"
    DEFAULT_HOST = "http://localhost:11434"

    def __init__(self, model: str = None, host: str = None, **kwargs):
        self.model = model or self.DEFAULT_MODEL
        self.host = host or self.DEFAULT_HOST

    def complete(self, system: str, user: str) -> str:
        payload = json.dumps({
            "model": self.model,
            "prompt": f"{system}\n\n{user}",
            "stream": False,
            "options": {"temperature": 0.9},
        }).encode()
        req = urllib.request.Request(
            f"{self.host}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        return data["response"]
