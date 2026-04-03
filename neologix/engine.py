"""
Core naming engine — builds the prompt, calls the provider, parses the table.
"""

from __future__ import annotations
import re
from typing import List, Tuple

from .rules import DEFAULT_RULES, SYSTEM_PROMPT


def _build_user_prompt(description: str, count: int, extra_constraints: list[str]) -> str:
    banned = DEFAULT_RULES["negative"]["banned_words"]
    blocked = DEFAULT_RULES["negative"]["banned_soundalikes"]

    lines = [
        f"PRODUCT DESCRIPTION:\n{description.strip()}",
        f"\nGenerate exactly {count} unique brand names following ALL rules above.",
        f"Exactly 5 of the {count} must be the Color + Land variant.",
        f"Banned words (never use these): {', '.join(banned)}.",
        f"Banned soundalikes (no names that resemble): {', '.join(blocked)}.",
    ]
    if extra_constraints:
        lines.append("ADDITIONAL CONSTRAINTS:\n" + "\n".join(f"- {c}" for c in extra_constraints))

    lines.append(
        "\nReturn ONLY the markdown table — no intro, no outro, no explanations outside the table."
    )
    return "\n".join(lines)


def _parse_table(raw: str) -> List[Tuple[str, str, str]]:
    """Parse a markdown table into a list of (name, origin, feeling) tuples."""
    rows = []
    for line in raw.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        # skip header and separator rows
        if cells[0].lower() in ("name", "") or re.match(r"^[-:]+$", cells[0]):
            continue
        rows.append((cells[0], cells[1], cells[2]))
    return rows


def generate(
    description: str,
    provider,
    count: int = 15,
    extra_constraints: list[str] | None = None,
) -> List[Tuple[str, str, str]]:
    """
    Generate brand names for the given product description.

    Args:
        description: What the product does (free-form text).
        provider:    An instantiated provider object (Gemini, OpenAI, Anthropic, Ollama).
        count:       Total names to generate (default 15, min 5 to allow Color+Land quota).
        extra_constraints: Additional rules appended to the prompt.

    Returns:
        List of (Name, Linguistic Origin, Magic Feeling) tuples.
    """
    if count < 5:
        raise ValueError("count must be >= 5 to satisfy the 5-name Color+Land quota.")

    user_prompt = _build_user_prompt(description, count, extra_constraints or [])
    raw = provider.complete(SYSTEM_PROMPT, user_prompt)
    return _parse_table(raw), raw
