"""Instruction contracts for the discovery failures observed in model traces."""

import unittest

import validate_skills as skills


class ImprovementPreflightTests(unittest.TestCase):
    def setUp(self):
        root = skills.ROOT / "skills/using-ampliflow"
        self.router = (root / "SKILL.md").read_text()
        self.grading = (root / "references/processes-risks-controls-and-improvements.md").read_text()

    def check_preflight(self, router, grading):
        for contract in (
            "These read-only prerequisite lookups do not need write confirmation.",
            "Resolve customer and user selections by their owning read tools before proposing a write.",
            "Do not seek confirmation for a draft containing unresolved selection placeholders.",
            "Do not ask permission to repeat catalog discovery within the existing read bound.",
        ):
            self.assertIn(contract, router)
        for contract in (
            "list_impact_grading_options",
            "show_impact_grading",
            "Before proposing a score",
            "all five",
            "A label-only option is not scoring evidence.",
        ):
            self.assertIn(contract, grading)

    def test_live_reads_precede_exact_proposal(self):
        self.check_preflight(self.router, self.grading)

    def test_missing_reads_or_premature_confirmation_are_rejected(self):
        self.check_preflight(self.router, self.grading)
        for source, old, new in (
            ("router", "do not need write confirmation", "need write confirmation"),
            ("router", "before proposing a write", "after proposing a write"),
            ("router", "Do not seek confirmation for a draft containing unresolved selection placeholders.", "Confirm the placeholders."),
            ("router", "Do not ask permission to repeat catalog discovery within the existing read bound.", "Ask permission to repeat discovery."),
            ("grading", "show_impact_grading", "missing_detail"),
            ("grading", "A label-only option is not scoring evidence.", "Guess scores from labels."),
        ):
            with self.subTest(source=source, removed=old):
                self.assertIn(old, self.router if source == "router" else self.grading)
                router = self.router.replace(old, new) if source == "router" else self.router
                grading = self.grading.replace(old, new) if source == "grading" else self.grading
                with self.assertRaises(AssertionError):
                    self.check_preflight(router, grading)

    def test_headings_do_not_define_the_read_contract(self):
        self.check_preflight(
            self.router.replace("## Normal operation workflow", "## Operation sequence"),
            self.grading.replace("## Improvement grading and creation", "## Report scoring"),
        )


if __name__ == "__main__":
    unittest.main()
