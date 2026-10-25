"""Rotate only the marked README quote once per Toronto calendar day."""

import json
import re
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- DAILY-QUOTE:START -->"
END = "<!-- DAILY-QUOTE:END -->"
EPOCH = date(2026, 10, 25)


def markdown(text):
    return re.sub(r'([\\`*_{}\[\]<>])', r'\\\1', text)


def validate_quotes(quotes):
    if not isinstance(quotes, list) or len(quotes) < 2:
        raise ValueError("Provide a list with at least two distinct quotes.")
    seen = set()
    for index, quote in enumerate(quotes, 1):
        if not isinstance(quote, dict):
            raise ValueError(f"Quote {index} must be an object.")
        for field in ("text", "author", "source"):
            value = quote.get(field)
            if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
                raise ValueError(f"Quote {index}: {field} must be nonempty, single-line text.")
        source = urlsplit(quote["source"])
        if source.scheme != "https" or not source.hostname:
            raise ValueError(f"Quote {index}: source must be an HTTPS URL.")
        normalized = " ".join(quote["text"].casefold().split())
        if normalized in seen:
            raise ValueError(f"Quote {index} duplicates an earlier quote.")
        seen.add(normalized)


def render(readme, quotes, today):
    validate_quotes(quotes)
    if readme.count(START) != 1 or readme.count(END) != 1:
        raise ValueError("README must contain exactly one pair of quote markers.")
    before, remainder = readme.split(START)
    old_quote, after = remainder.split(END)
    quote = quotes[(today - EPOCH).days % len(quotes)]
    block = f'\n> “{markdown(quote["text"])}”  \n> — [{markdown(quote["author"])}]({quote["source"]})\n'
    return before + START + block + END + after


if __name__ == "__main__":
    path = ROOT / "README.md"
    current = path.read_text(encoding="utf-8")
    quotes = json.loads((ROOT / "quotes.json").read_text(encoding="utf-8"))
    updated = render(current, quotes, datetime.now(ZoneInfo("America/Toronto")).date())
    if updated != current:
        path.write_text(updated, encoding="utf-8", newline="\n")
        print("Updated daily quote.")
    else:
        print("Today's quote is already current.")
