"""
Unit tests for ExactSentimentAnalyzer and Antigravity false-neutral elimination.
Validates:
1. Contrastive constructions ("X but Y", "X however Y") dominated by adverse or favorable clauses.
2. Negation handling ("not healthy", "not good", "never smiled").
3. Domain vocabulary (health/hospitalization, moral/conduct, performance).
4. Strict neutral preservation on objective, non-evaluative facts.
5. Antigravity calibration guardrail overriding false neutrals from external engines.
"""
import unittest
from blindspot.semantic.analyzer import get_exact_analyzer, ExactSentimentAnalyzer
from blindspot.semantic.types import SemanticReferenceLabel


class TestExactSentimentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = get_exact_analyzer()

    def test_01_contrastive_clauses_adverse_dominance(self):
        """Contrast clause 'X but Y' where Y is adverse must be strictly NEGATIVE, not NEUTRAL."""
        cases = [
            "i am healthy but still hospitalized",
            "i am not healthy but still hospitalized",
            "He is a Good boy but very naughty",
            "The phone looks pretty but breaks easily",
            "I wanted to love it, but the experience was dreadful",
        ]
        for text in cases:
            label, conf, reason = self.analyzer.analyze(text)
            self.assertEqual(
                label,
                SemanticReferenceLabel.NEGATIVE,
                f"Expected NEGATIVE for '{text}', got {label.value}. Reason: {reason}",
            )
            self.assertGreaterEqual(conf, 0.75)

    def test_02_contrastive_clauses_favorable_dominance(self):
        """Contrast clause 'X but Y' where Y is favorable must be strictly POSITIVE, not NEUTRAL."""
        cases = [
            "The car was expensive, but it runs exquisitely",
            "She was tired, but she delivered a brilliant presentation",
            "The movie is long, but it is deeply romantic and touching",
        ]
        for text in cases:
            label, conf, reason = self.analyzer.analyze(text)
            self.assertEqual(
                label,
                SemanticReferenceLabel.POSITIVE,
                f"Expected POSITIVE for '{text}', got {label.value}. Reason: {reason}",
            )
            self.assertGreaterEqual(conf, 0.75)

    def test_03_negated_positive_sentiment(self):
        """Negating positive attributes must be strictly NEGATIVE, not NEUTRAL."""
        cases = [
            "i am not healthy",
            "The movie was not great",
            "He is not kind",
            "The food was not good",
        ]
        for text in cases:
            label, conf, reason = self.analyzer.analyze(text)
            self.assertEqual(
                label,
                SemanticReferenceLabel.NEGATIVE,
                f"Expected NEGATIVE for '{text}', got {label.value}. Reason: {reason}",
            )

    def test_04_positive_sentiment_lexicon(self):
        """Sentences with positive words must be POSITIVE."""
        cases = [
            "i am healthy",
            "He is a good boy",
            "the way she looked him was so romantic",
            "She felt delighted with the outcome",
            "The team displayed remarkable skill",
        ]
        for text in cases:
            label, conf, reason = self.analyzer.analyze(text)
            self.assertEqual(
                label,
                SemanticReferenceLabel.POSITIVE,
                f"Expected POSITIVE for '{text}', got {label.value}. Reason: {reason}",
            )

    def test_05_negative_sentiment_lexicon(self):
        """Sentences with negative words must be NEGATIVE."""
        cases = [
            "the king had a injury in his left leg",
            "He is very naughty",
            "The engine broke down completely",
            "She felt miserable and unwell",
            "The food was terrible",
        ]
        for text in cases:
            label, conf, reason = self.analyzer.analyze(text)
            self.assertEqual(
                label,
                SemanticReferenceLabel.NEGATIVE,
                f"Expected NEGATIVE for '{text}', got {label.value}. Reason: {reason}",
            )

    def test_06_strictly_objective_neutral(self):
        """Objective factual statements devoid of sentiment words must remain NEUTRAL."""
        cases = [
            "The package arrived on Monday",
            "The table has four legs",
            "Water boils at 100 degrees Celsius",
            "The train leaves at five o'clock",
        ]
        for text in cases:
            label, conf, reason = self.analyzer.analyze(text)
            self.assertEqual(
                label,
                SemanticReferenceLabel.NEUTRAL,
                f"Expected NEUTRAL for '{text}', got {label.value}. Reason: {reason}",
            )

    def test_07_calibrate_label_overrides_false_neutral(self):
        """calibrate_label must override false neutrals on sentiment-bearing statements."""
        # False neutral from external source
        cal_label, was_cal, reason = self.analyzer.calibrate_label(
            "i am healthy but still hospitalized",
            SemanticReferenceLabel.NEUTRAL,
        )
        self.assertTrue(was_cal)
        self.assertEqual(cal_label, SemanticReferenceLabel.NEGATIVE)
        self.assertIn("Antigravity Calibration", reason)

        # Genuine neutral must be preserved
        cal_label2, was_cal2, reason2 = self.analyzer.calibrate_label(
            "The package arrived on Monday",
            SemanticReferenceLabel.NEUTRAL,
        )
        self.assertFalse(was_cal2)
        self.assertEqual(cal_label2, SemanticReferenceLabel.NEUTRAL)


if __name__ == "__main__":
    unittest.main()
