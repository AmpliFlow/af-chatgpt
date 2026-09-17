"""Contract checks for bounded process-map completeness guidance."""

import unittest
from pathlib import Path

REFERENCE = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "using-ampliflow"
    / "references"
    / "processes-risks-controls-and-improvements.md"
)


class ProcessRoutingTests(unittest.TestCase):
    def test_reference_bounds_process_traversal(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("## Process-map completeness review", text)
        self.assertIn("at most 50 returned nodes", text)
        self.assertIn("5 tree levels", text)
        self.assertIn("10 focused detail reads", text)
        self.assertIn("state the covered roots and branches", text)

    def test_reference_limits_supported_findings_and_side_effects(self):
        text = REFERENCE.read_text(encoding="utf-8")
        self.assertIn("only when successful responses return those fields", text)
        self.assertIn('"not verified" rather than missing', text)
        self.assertIn("recorded facts, structural inconsistencies", text)
        self.assertIn("Do not claim freshness, revision history, process effectiveness", text)
        self.assertIn("do not update charts or processes, export content, open files", text)


if __name__ == "__main__":
    unittest.main()
