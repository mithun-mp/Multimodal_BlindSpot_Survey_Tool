"""
Unit Tests for Model Registry and Verification.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.models.registry import ModelRegistry


class TestModelRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ModelRegistry()

    def test_presets_exist_and_include_default(self):
        presets = self.registry.list_presets()
        self.assertEqual(len(presets), 5)

        preset_ids = [p["model_id"] for p in presets]
        self.assertIn("distilbert-base-uncased-finetuned-sst-2-english", preset_ids)
        self.assertIn("cardiffnlp/twitter-roberta-base-sentiment", preset_ids)

        default_preset = self.registry.get_preset("distilbert-base-uncased-finetuned-sst-2-english")
        self.assertIsNotNone(default_preset)
        self.assertEqual(default_preset["num_classes"], 2)
        self.assertEqual(default_preset["label_names"], ["NEGATIVE", "POSITIVE"])
        self.assertTrue(default_preset["default"])

    def test_custom_registration(self):
        entry = self.registry.register_custom(
            model_id="my-org/custom-sentiment",
            name="Custom Sentiment",
            num_classes=3,
            label_names=["NEG", "NEU", "POS"],
            description="A test custom model",
        )
        self.assertEqual(entry["model_id"], "my-org/custom-sentiment")
        self.assertEqual(entry["num_classes"], 3)

        retrieved = self.registry.get_preset("my-org/custom-sentiment")
        self.assertEqual(retrieved["name"], "Custom Sentiment")

    def test_verify_preset_model(self):
        verification = self.registry.verify_model("distilbert-base-uncased-finetuned-sst-2-english")
        self.assertTrue(verification["verified"])
        self.assertIsNone(verification["error"])
        self.assertEqual(verification["num_classes"], 2)
        self.assertEqual(verification["label_names"], ["NEGATIVE", "POSITIVE"])


if __name__ == "__main__":
    unittest.main()
