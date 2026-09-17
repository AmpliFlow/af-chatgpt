"""Contract checks for bounded annual management-plan guidance."""

import unittest
from pathlib import Path

REFERENCE = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "using-ampliflow"
    / "references"
    / "assurance-content-and-planning.md"
)


class YearWheelRoutingTests(unittest.TestCase):
    def test_reference_resolves_one_wheel_and_bounds_reads(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("## Annual management-plan review", text)
        self.assertIn("Resolve one exact year wheel", text)
        self.assertIn("at most 20 categories", text)
        self.assertIn("50 items", text)
        self.assertIn("10 focused item-detail reads", text)

    def test_reference_blocks_unsupported_plan_inferences_and_writes(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("possible collisions, not scheduling errors", text)
        self.assertIn("A scheduled item is not completed work", text)
        self.assertIn("A recurrence rule is not an expanded occurrence list", text)
        self.assertIn("label an omitted or failed field \"not verified.\"", text)
        self.assertIn("do not create, update, delete, or apply year-wheel templates", text)


if __name__ == "__main__":
    unittest.main()
