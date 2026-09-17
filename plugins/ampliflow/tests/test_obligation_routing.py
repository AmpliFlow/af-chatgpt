"""Contract checks for bounded compliance-obligation routing guidance."""

import unittest
from pathlib import Path

REFERENCE = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "using-ampliflow"
    / "references"
    / "context-and-obligations.md"
)


class ObligationRoutingTests(unittest.TestCase):
    def test_reference_sets_bounded_source_separated_review(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("## Obligation gap review", text)
        self.assertIn("at most 10 selected records per source", text)
        self.assertIn("separate report sections", text)
        self.assertIn('label it "not returned" instead of calling it a gap', text)

    def test_reference_blocks_legal_and_data_overreach(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("Never assert legal compliance or noncompliance", text)
        self.assertIn("Never infer a control or evidence mapping", text)
        self.assertIn("Minimize customer terms and sensitive details", text)
        self.assertIn("Keep ambiguous matches unresolved", text)
        self.assertIn("unavailable, partial, or saturated", text)


if __name__ == "__main__":
    unittest.main()
