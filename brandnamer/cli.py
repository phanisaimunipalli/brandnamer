#!/usr/bin/env python3
"""
brandnamer CLI

Usage examples:
  brandnamer "Premium iOS travel orchestrator that eliminates friction between landing, rental, and hotel"
  brandnamer "B2B SaaS for supply chain visibility" --provider openai --count 20
  brandnamer "Mindfulness app for founders" --provider ollama --model llama3.2
  brandnamer --file examples/travel_app.json
"""

import argparse
import json
import os
import sys

from .engine import generate
from .providers import get_provider


def _print_table(rows, raw_fallback: str):
    try:
        from rich.table import Table
        from rich.console import Console

        console = Console()
        table = Table(
            title="brandnamer — generated names",
            show_header=True,
            header_style="bold magenta",
            border_style="dim",
            min_width=80,
        )
        table.add_column("Name", style="bold cyan", no_wrap=True, min_width=12)
        table.add_column("Linguistic Origin", style="white", min_width=28)
        table.add_column("The Magic Feeling", style="italic yellow", min_width=32)

        for name, origin, feeling in rows:
            table.add_row(name, origin, feeling)

        console.print(table)
    except ImportError:
        # rich not installed — fall back to raw markdown
        print(raw_fallback)


def main():
    parser = argparse.ArgumentParser(
        prog="brandnamer",
        description="Category King brand name generator — Neologism + Short-Form + Phonetic rules.",
    )
    parser.add_argument(
        "description",
        nargs="?",
        help="Product description (free-form text). Wrap in quotes.",
    )
    parser.add_argument(
        "--file", "-f",
        help="JSON config file (see examples/travel_app.json).",
    )
    parser.add_argument(
        "--provider", "-p",
        default="gemini",
        choices=["gemini", "openai", "anthropic", "ollama"],
        help="LLM provider (default: gemini).",
    )
    parser.add_argument(
        "--model", "-m",
        help="Override the default model for the chosen provider.",
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=15,
        help="Number of names to generate (default: 15, min: 5).",
    )
    parser.add_argument(
        "--api-key", "-k",
        help="API key (overrides environment variable).",
    )
    parser.add_argument(
        "--constraint", "-c",
        action="append",
        dest="constraints",
        help="Extra constraint (repeatable). E.g. -c 'avoid ocean metaphors'.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Print raw LLM output instead of the formatted table.",
    )
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Show version and exit.",
    )

    args = parser.parse_args()

    if args.version:
        from . import __version__
        print(f"brandnamer {__version__}")
        sys.exit(0)

    # Resolve description and constraints from --file or CLI arg
    description = args.description
    constraints = args.constraints or []

    if args.file:
        with open(args.file) as f:
            cfg = json.load(f)
        description = cfg.get("description", description)
        constraints = cfg.get("constraints", []) + constraints
        if not args.model and "model" in cfg:
            args.model = cfg["model"]
        if not args.api_key and "api_key" in cfg:
            args.api_key = cfg["api_key"]

    if not description:
        parser.error("Provide a product description as an argument or via --file.")

    # Build provider kwargs
    provider_kwargs = {}
    if args.model:
        provider_kwargs["model"] = args.model
    if args.api_key:
        provider_kwargs["api_key"] = args.api_key

    try:
        provider = get_provider(args.provider, **provider_kwargs)
    except ValueError as e:
        print(f"[brandnamer] Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"[brandnamer] Generating {args.count} names via {args.provider}…\n")

    try:
        rows, raw = generate(
            description=description,
            provider=provider,
            count=args.count,
            extra_constraints=constraints or None,
        )
    except Exception as e:
        print(f"[brandnamer] LLM error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.raw or not rows:
        print(raw)
    else:
        _print_table(rows, raw)


if __name__ == "__main__":
    main()
