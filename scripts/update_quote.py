"""Rotate only the marked README quote once per Toronto calendar day."""

import json
import re
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- DAILY-QUOTE:START -->"
END = "<!-- DAILY-QUOTE:END -->"
EPOCH = date(2026, 10, 25)


def markdown(text):
    return re.sub(r'([\\`*_{}\[\]<>])', r'\\\1', text)


def render(readme, quotes, today):
    if len(quotes) < 2 or len({q["text"] for q in quotes}) != len(quotes):
        raise ValueError("Provide at least two distinct quotes.")
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
