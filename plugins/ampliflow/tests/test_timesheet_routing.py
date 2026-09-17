"""Contract checks for bounded, privacy-safe timesheet routing guidance."""

import unittest
from pathlib import Path

REFERENCE = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "using-ampliflow"
    / "references"
    / "projects-work-and-time.md"
)


class TimesheetRoutingTests(unittest.TestCase):
    def test_reference_requires_bounded_scope(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("## Timesheet completion review", text)
        self.assertIn("clear start date, end date", text)
        self.assertIn("maximum 31-day range", text)
        self.assertIn("at most 10 selected users or projects", text)
        self.assertIn("stop rather than fetching or reproducing the raw set", text)

    def test_reference_blocks_privacy_and_performance_overreach(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("Keep recorded entries and outstanding weeks separate", text)
        self.assertIn("Do not echo free-text notes", text)
        self.assertIn("Never rank people", text)
        self.assertIn("characterize missing time as misconduct", text)
        self.assertIn("do not create, update, approve, export", text)


if __name__ == "__main__":
    unittest.main()
