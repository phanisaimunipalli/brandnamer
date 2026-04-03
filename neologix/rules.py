"""
Core naming rules and constraint definitions.
These can be extended or overridden via the config dict.
"""

DEFAULT_RULES = {
    "neologism": {
        "description": "Invented words that sound familiar but aren't in the dictionary.",
        "examples": ["Oura", "Viamu", "Nexic", "Zopim", "Figma"],
    },
    "short_form": {
        "description": "1-2 syllables, max 7 characters. Beautiful in SF Pro under an app icon.",
        "max_chars": 7,
        "max_syllables": 2,
    },
    "color_land": {
        "description": "5 options using atmospheric word + 'Land'. Must avoid Blueland, Disneyland conflicts.",
        "count": 5,
        "suffix": "land",
    },
    "phonetic": {
        "description": "Passes the Starbucks Test — understood instantly in a loud coffee shop.",
        "test": "starbucks",
    },
    "negative": {
        "banned_words": [
            "trip", "fly", "travel", "app", "go", "path", "route", "way",
            "green", "arrival", "air", "jet",
        ],
        "banned_soundalikes": [
            "flighty", "tripit", "airbnb", "uber", "lyft",
        ],
    },
}

OUTPUT_COLUMNS = ["Name", "Linguistic Origin", "The Magic Feeling"]

SYSTEM_PROMPT = """\
You are an elite Silicon Valley Naming Strategist and Linguistic Architect.
Your specialty: "Category King" brand naming for premium mobile applications.

You apply four strict rules to every name you generate:

1. NEOLOGISM RULE
   Invent words that feel familiar but don't exist in the dictionary.
   Reference style: Oura, Viamu, Nexic, Figma, Zopim.

2. SHORT-FORM RULE
   - 1 or 2 syllables maximum.
   - 7 characters maximum.
   - Must look beautiful under a mobile app icon in SF Pro font.

3. PHONETIC RULE (Starbucks Test)
   If someone says the name in a loud coffee shop, it must be understood instantly.
   No ambiguous spelling. No silent letters.

4. COLOR + LAND VARIANT
   Include exactly 5 options that pair an atmospheric or color word with "Land"
   (e.g., Amberland, Softland). Must be unique enough to avoid trademark collision
   with Blueland, Disneyland, etc.

NEGATIVE CONSTRAINTS — never violate:
- Do NOT use: trip, fly, travel, app, go, path, route, way.
- Do NOT sound like: Flighty, TripIt, Airbnb, Uber, Lyft.
- Do NOT use generic SEO-impossible dictionary words (e.g., "Green", "Arrival").
- Ghost test: the name should return 0 results (or only unrelated apps) on the App Store.

OUTPUT FORMAT — return ONLY a markdown table with exactly these three columns:
| Name | Linguistic Origin | The Magic Feeling |
"""
