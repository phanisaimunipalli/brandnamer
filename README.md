# neologix

**Category King brand name generator — Neologism + Short-Form + Phonetic rules.**

The same naming framework used by elite Silicon Valley naming studios, now as a CLI tool and Python library. Describe your product in plain English, pick your LLM, get a table of ghost-clean, App Store-ready names in seconds.

```
$ neologix "Premium iOS travel orchestrator that eliminates flight-to-hotel friction"

┌──────────────┬────────────────────────────────┬──────────────────────────────────────┐
│ Name         │ Linguistic Origin              │ The Magic Feeling                    │
├──────────────┼────────────────────────────────┼──────────────────────────────────────┤
│ Luvio        │ Latin lux + -vio motion suffix │ Light, forward motion, effortless    │
│ Dryst        │ Compressed "drift" + "rest"    │ The moment you stop moving and arrive│
│ Tivn         │ Invented — crisp Nordic sound  │ Invisible precision                  │
│ Softland     │ "soft" + "land" atmospheric    │ The gentlest possible arrival        │
│ …            │ …                              │ …                                    │
└──────────────┴────────────────────────────────┴──────────────────────────────────────┘
```

---

## The Rules

Every name neologix generates must pass four gates:

| Rule | What it means |
|------|--------------|
| **Neologism** | Invented word that _sounds_ familiar but isn't in the dictionary. Reference: Oura, Figma, Zopim. |
| **Short-Form** | ≤ 7 characters, 1-2 syllables. Beautiful under an app icon in SF Pro. |
| **Phonetic (Starbucks Test)** | If shouted in a loud coffee shop, it would be understood instantly. No ambiguous spelling. |
| **Color + Land** | 5 of the generated names pair an atmospheric word with "Land" (e.g., Amberland, Softland). Trademark-safe variants only. |

**Negative constraints** — automatically enforced:
- Banned words: `trip`, `fly`, `travel`, `app`, `go`, `path`, `route`, `way`
- Banned soundalikes: Flighty, TripIt, Airbnb, Uber, Lyft
- No generic SEO-impossible dictionary words

**Ghost test** — each name is prompted to be App Store-ghost: 0 results or only unrelated apps.

---

## Install

```bash
# From PyPI (once published)
pip install neologix

# With pretty table output (recommended)
pip install "neologix[pretty]"

# From source
git clone https://github.com/phanisaimunipalli/neologix
cd neologix
pip install -e ".[pretty]"
```

---

## Quick Start

### CLI

```bash
# Gemini (free tier — default)
export GEMINI_API_KEY=your_key
neologix "B2B SaaS for real-time supply chain visibility"

# OpenAI
export OPENAI_API_KEY=your_key
neologix "Mindfulness app for founders" --provider openai

# Anthropic Claude
export ANTHROPIC_API_KEY=your_key
neologix "Gen-Z savings app with gamification" --provider anthropic --model claude-haiku-4-5-20251001

# Local Ollama (no API key)
neologix "Fitness tracker for remote workers" --provider ollama --model qwen2.5:14b

# From a JSON config file
neologix --file examples/travel_app.json

# 20 names, extra constraint, raw markdown output
neologix "Luxury skincare subscription" -n 20 -c "avoid ocean metaphors" --raw
```

### Python API

```python
from neologix.engine import generate
from neologix.providers import get_provider

provider = get_provider("gemini", api_key="your_key")

rows, raw_markdown = generate(
    description="Premium iOS travel orchestrator that eliminates flight-to-hotel friction.",
    provider=provider,
    count=15,
    extra_constraints=["evoke effortlessness", "premium — not budget travel"],
)

for name, origin, feeling in rows:
    print(f"{name:12}  {origin}")
```

---

## JSON Config Files

Create a config file to save your product brief and reuse it:

```json
{
  "description": "A high-end iOS travel orchestrator...",
  "constraints": [
    "Evoke effortlessness and invisible orchestration",
    "Must work as a single-word app icon label"
  ]
}
```

```bash
neologix --file examples/travel_app.json --provider anthropic
```

See [`examples/`](examples/) for ready-made configs.

---

## Providers

| Provider | Flag | Env var | Default model | Free tier |
|----------|------|---------|---------------|-----------|
| Gemini | `--provider gemini` | `GEMINI_API_KEY` | `gemini-2.0-flash` | Yes |
| OpenAI | `--provider openai` | `OPENAI_API_KEY` | `gpt-4o-mini` | No |
| Anthropic | `--provider anthropic` | `ANTHROPIC_API_KEY` | `claude-haiku-4-5-20251001` | No |
| Ollama (local) | `--provider ollama` | — | `qwen2.5:14b` | Always free |

Override the model with `--model`:

```bash
neologix "..." --provider openai --model gpt-4o
neologix "..." --provider ollama --model llama3.2
```

---

## CLI Reference

```
neologix [description] [options]

Arguments:
  description          Product description in plain English (wrap in quotes)

Options:
  -f, --file PATH      JSON config file (description + constraints)
  -p, --provider       gemini | openai | anthropic | ollama  (default: gemini)
  -m, --model          Override the default model
  -n, --count INT      Number of names to generate (default: 15, min: 5)
  -k, --api-key        API key (overrides environment variable)
  -c, --constraint     Extra constraint, repeatable
      --raw            Print raw LLM output instead of the table
  -v, --version        Show version
```

---

## Extending neologix

### Add a new provider

Create `neologix/providers/myprovider.py`:

```python
class MyProvider:
    def __init__(self, api_key: str, model: str = "my-model", **kwargs):
        self.api_key = api_key
        self.model = model

    def complete(self, system: str, user: str) -> str:
        # call your API, return raw text
        ...
```

Register it in `neologix/providers/__init__.py`:

```python
from .myprovider import MyProvider
PROVIDERS["myprovider"] = MyProvider
```

### Customize the naming rules

Import and modify `DEFAULT_RULES` before calling `generate()`:

```python
from neologix.rules import DEFAULT_RULES

DEFAULT_RULES["negative"]["banned_words"].append("zen")
DEFAULT_RULES["short_form"]["max_chars"] = 6
```

---

## Contributing

PRs welcome. Keep zero hard dependencies (stdlib only). Optional extras go in `[project.optional-dependencies]`.

1. Fork → branch → PR
2. Run `pytest` before submitting
3. One feature per PR

---

## License

MIT — [LICENSE](LICENSE)

---

Built by [Phani Sai Ram Munipalli](https://github.com/phanisaimunipalli)
