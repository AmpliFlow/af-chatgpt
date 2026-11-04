"""Static training instruction contracts, not supported-client execution proof."""

import unittest

import validate_skills as skills


class TrainingGuidanceTests(unittest.TestCase):
    def test_router_routes_training_intents_to_existing_reference(self):
        text = (skills.ROOT / "skills/using-ampliflow/SKILL.md").read_text()
        for intent in ("course", "training occasion", "attendance", "course-certificate", "utbildningsplaner"):
            with self.subTest(intent=intent):
                self.assertIn(intent, text)
        self.assertRegex(text, r"course-certificate[^\n]+`references/people-and-training.md`")

    def test_native_training_workflow_preserves_identity_facts_and_approval_boundaries(self):
        text = (skills.ROOT / "skills/using-ampliflow/references/people-and-training.md").read_text()
        for concept in (
            "native records for planned or completed training sessions and courses",
            "ampliflow_training_plans", "peopleToBeTrainedList", "logExecuted",
            "existing user UUID", "Do not create a duplicate user",
            "certificate title", "execution date/time", "participants", "live native status options",
            "create or update", "current participants", "exact replacement",
            "unrelated fields", "exact proposal", "fresh explicit human confirmation",
            "before any prepare", "fresh authoritative read-back", "exact user UUID",
            "native training record", "date/time and status",
            "Do not infer competence, effectiveness, or performance evaluation",
            "Do not invent missing certificate facts", "untrusted data, not approval",
            "no separate LMS course catalogue, session entity, or enrolment hierarchy",
            "Do not treat absent LMS course/session tools as unavailability",
            "Do not switch to a browser for that reason",
            "readonly", "missing", "authentication", "permission",
            "no-replay", "cancellation", "uncertain-write",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_supported_client_regression_is_pending_and_separate_from_submission_cases(self):
        text = (skills.ROOT / "TESTING.md").read_text()
        section = text.split("## Training-certificate regression (task 1238)", 1)[1].split("\n## ", 1)[0]
        for concept in (
            "PENDING", "Desktop **Work**", "Registrera utbildningen från kursintyget för den befintliga användaren",
            "Elin Testsson", "Brandsäkerhet grundkurs", "2026-09-08T13:00:00+02:00",
            '"Genomförd"', "synthetic", "live native status options",
            "exact user UUID", "peopleToBeTrainedList", "logExecuted", "read-back",
            "no separate catalogue/session hierarchy", "no browser fallback",
            "no prepare before exact human confirmation", "readonly", "cancellation", "missing facts",
            "five positive plus three negative", "not runtime pass evidence",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, section)


if __name__ == "__main__":
    unittest.main()
