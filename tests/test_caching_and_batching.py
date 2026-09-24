"""
Unit Tests for Model LRU Caching and Batched Inference.
"""
import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.models.cache import ModelCache
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper


class TestCachingAndBatching(unittest.TestCase):
    def test_model_cache_lru(self):
        cache = ModelCache(max_size=2)
        self.assertEqual(cache.size(), 0)

        # Load model 1
        m1 = cache.get_or_load("distilbert-base-uncased-finetuned-sst-2-english")
        self.assertEqual(cache.size(), 1)
        self.assertTrue(cache.is_cached("distilbert-base-uncased-finetuned-sst-2-english"))

        # Second access -> cache hit (same instance)
        m1_again = cache.get_or_load("distilbert-base-uncased-finetuned-sst-2-english")
        self.assertIs(m1, m1_again)

        # Clear cache
        cache.clear()
        self.assertEqual(cache.size(), 0)

    def test_batch_vs_single_prediction_consistency(self):
        wrapper = HuggingFaceWrapper()
        sentences = [
            "The movie was great and fantastic.",
            "The food was terrible and cold.",
            "The acting was surprisingly good.",
        ]

        # Single predictions
        single_preds = [wrapper.predict_result(s) for s in sentences]

        # Batch predictions
        batch_preds = wrapper.predict_results_batch(sentences, batch_size=2)

        self.assertEqual(len(single_preds), len(batch_preds))
        for sp, bp in zip(single_preds, batch_preds):
            self.assertEqual(sp.label, bp.label)
            self.assertAlmostEqual(sp.confidence, bp.confidence, places=4)


if __name__ == "__main__":
    unittest.main()
