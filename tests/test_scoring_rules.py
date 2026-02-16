import unittest

from car_wash_evals.scoring import (
    build_judge_messages,
    parse_judge_response,
    score_response,
    score_response_across_modes,
)


class ScoringRulesTest(unittest.TestCase):
    def test_explicit_drive_answer_is_pass(self) -> None:
        decision = score_response("Drive the car there. The vehicle needs to be present at the car wash.")
        self.assertEqual(decision.label, "pass")
        self.assertIn("recommends_drive", decision.reason_codes)

    def test_explicit_walk_answer_is_fail(self) -> None:
        decision = score_response("You should definitely walk. It is healthier.")
        self.assertEqual(decision.label, "fail")
        self.assertIn("recommends_walk", decision.reason_codes)
        self.assertTrue(decision.confident_wrong)

    def test_mixed_answer_is_ambiguous(self) -> None:
        decision = score_response("You can walk, but maybe drive if needed.")
        self.assertEqual(decision.label, "ambiguous")

    def test_judge_json_parse(self) -> None:
        decision = parse_judge_response('{"label":"pass","reason":"car must be present"}')
        self.assertEqual(decision.label, "pass")
        self.assertTrue(any(code.startswith("judge:") for code in decision.reason_codes))

    def test_direct_answer_first_mode_uses_first_span(self) -> None:
        decision = score_response(
            "Drive. But if you only care about yourself walking is also fine.",
            mode="direct_answer_first",
        )
        self.assertEqual(decision.label, "pass")

    def test_direct_and_consistent_requires_direct_answer_first(self) -> None:
        decision = score_response(
            "It depends. You should drive because the car must be at the wash.",
            mode="direct_and_consistent",
        )
        self.assertEqual(decision.label, "fail")
        self.assertIn("no_clear_direct_answer_first", decision.reason_codes)

    def test_challenge_clarification_is_added_to_judge_prompt(self) -> None:
        messages = build_judge_messages(
            question="How will I get my car washed if I am walking?",
            model_answer="Walk to your car, then drive it to the wash.",
            scope="challenge",
        )
        self.assertIn("does NOT imply inability to drive", messages[1]["content"])

    def test_shadow_mode_scoring(self) -> None:
        results = score_response_across_modes(
            "Walk. Actually drive the car there.",
            modes=["full_response", "direct_answer_first", "direct_and_consistent"],
        )
        self.assertEqual(set(results.keys()), {"full_response", "direct_answer_first", "direct_and_consistent"})
        self.assertEqual(results["direct_answer_first"].label, "fail")


if __name__ == "__main__":
    unittest.main()
