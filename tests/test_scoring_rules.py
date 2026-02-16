import unittest

from car_wash_evals.scoring import parse_judge_response, score_response


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


if __name__ == "__main__":
    unittest.main()
