"""Regression checks for the public profile's automated daily edits."""

import copy
import json
import unittest
from datetime import timedelta
from pathlib import Path

from scripts.update_quote import END, EPOCH, START, markdown, render, validate_quotes

ROOT = Path(__file__).resolve().parents[1]


class DailyQuoteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.quotes = json.loads((ROOT / "quotes.json").read_text(encoding="utf-8"))
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")

    def test_collection_has_500_valid_distinct_quotes(self):
        self.assertEqual(len(self.quotes), 500)
        validate_quotes(self.quotes)

    def test_full_cycle_without_repeats(self):
        outputs = [render(self.readme, self.quotes, EPOCH + timedelta(days=i)) for i in range(500)]
        self.assertEqual(len(set(outputs)), 500)
        self.assertEqual(outputs[0], render(self.readme, self.quotes, EPOCH + timedelta(days=500)))

    def test_only_marked_section_changes(self):
        sentinel = "Custom profile text\n" + self.readme + "\nCustom footer\n"
        result = render(sentinel, self.quotes, EPOCH + timedelta(days=1))
        self.assertEqual(result.split(START)[0], sentinel.split(START)[0])
        self.assertEqual(result.split(END)[1], sentinel.split(END)[1])

    def test_same_day_is_idempotent(self):
        result = render(self.readme, self.quotes, EPOCH)
        self.assertEqual(result, render(result, self.quotes, EPOCH))

    def test_missing_duplicate_and_reversed_markers_fail(self):
        for readme in (self.readme.replace(START, ""), self.readme + END, END + START):
            with self.subTest(readme=readme), self.assertRaises(ValueError):
                render(readme, self.quotes, EPOCH)

    def test_invalid_records_fail_before_rendering(self):
        invalid = [None, {}, [], [self.quotes[0]], [None, self.quotes[0]]]
        for field, value in (("text", ""), ("author", 42), ("source", "javascript:alert(1)"),
                             ("source", "https:///missing-host"), ("text", "line\nbreak")):
            records = copy.deepcopy(self.quotes[:2])
            records[0][field] = value
            invalid.append(records)
        for records in invalid:
            with self.subTest(records=records), self.assertRaises(ValueError):
                render(self.readme, records, EPOCH)

    def test_duplicates_ignore_case_and_whitespace(self):
        records = copy.deepcopy(self.quotes[:2])
        records[1]["text"] = "  " + records[0]["text"].upper().replace(" ", "  ") + " "
        with self.assertRaisesRegex(ValueError, "duplicates"):
            validate_quotes(records)

    def test_quote_cannot_inject_markdown_formatting(self):
        self.assertEqual(markdown("[link] *bold* <tag> `code`"),
                         r"\[link\] \*bold\* \<tag\> \`code\`")


if __name__ == "__main__":
    unittest.main()
