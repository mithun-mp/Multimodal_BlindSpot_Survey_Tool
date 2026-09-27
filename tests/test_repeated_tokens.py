import sys
import os
import unittest

# Ensure workspace root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from blindspot.explainability.token_attributions import (
    TokenAttributionsDict,
    extract_words_with_positions,
    align_token_attributions,
)
from blindspot.app import find_key_misweighted_token, resolve_failure_metadata


class TestRepeatedTokenAttributions(unittest.TestCase):
    def test_extract_words_with_positions(self):
        text = "The movie was great and the acting was great."
        tokens = extract_words_with_positions(text)
        
        # 9 words total
        self.assertEqual(len(tokens), 9)
        
        # Check first occurrence of "great"
        occ1 = [t for t in tokens if t["token"].lower() == "great" and t["occurrence"] == 1][0]
        self.assertEqual(occ1["position"], 4)
        
        # Check second occurrence of "great"
        occ2 = [t for t in tokens if t["token"].lower() == "great" and t["occurrence"] == 2][0]
        self.assertEqual(occ2["position"], 9)
        self.assertNotEqual(occ1["position"], occ2["position"])

    def test_align_token_attributions_repeated_words(self):
        orig_text = "The movie was great and the acting was great."
        pert_text = "The film was great and the acting was great."
        
        # Mock TokenAttributionsDict with distinct weights for each occurrence
        orig_recs = [
            {"token": "The", "position": 1, "occurrence": 1, "attribution": 0.01},
            {"token": "movie", "position": 2, "occurrence": 1, "attribution": 0.08},
            {"token": "was", "position": 3, "occurrence": 1, "attribution": -0.02},
            {"token": "great", "position": 4, "occurrence": 1, "attribution": 0.1696},
            {"token": "and", "position": 5, "occurrence": 1, "attribution": 0.01},
            {"token": "the", "position": 6, "occurrence": 1, "attribution": 0.01},
            {"token": "acting", "position": 7, "occurrence": 1, "attribution": 0.03},
            {"token": "was", "position": 8, "occurrence": 2, "attribution": -0.02},
            {"token": "great", "position": 9, "occurrence": 2, "attribution": 0.0832},
        ]
        orig_dict = TokenAttributionsDict({r["token"]: r["attribution"] for r in orig_recs}, token_attributions=orig_recs)

        pert_recs = [
            {"token": "The", "position": 1, "occurrence": 1, "attribution": 0.01},
            {"token": "film", "position": 2, "occurrence": 1, "attribution": 0.07},
            {"token": "was", "position": 3, "occurrence": 1, "attribution": -0.02},
            {"token": "great", "position": 4, "occurrence": 1, "attribution": 0.1180},
            {"token": "and", "position": 5, "occurrence": 1, "attribution": 0.01},
            {"token": "the", "position": 6, "occurrence": 1, "attribution": 0.01},
            {"token": "acting", "position": 7, "occurrence": 1, "attribution": 0.02},
            {"token": "was", "position": 8, "occurrence": 2, "attribution": -0.02},
            {"token": "great", "position": 9, "occurrence": 2, "attribution": 0.0614},
        ]
        pert_dict = TokenAttributionsDict({r["token"]: r["attribution"] for r in pert_recs}, token_attributions=pert_recs)

        aligned = align_token_attributions(orig_text, pert_text, orig_dict, pert_dict)
        
        # Verify occurrences of 'great'
        great_rows = [r for r in aligned if r.get("token", "").lower() == "great"]
        self.assertEqual(len(great_rows), 2)
        
        # First great at position 4
        g1 = great_rows[0]
        self.assertEqual(g1["orig_pos"], 4)
        self.assertEqual(g1["pert_pos"], 4)
        self.assertEqual(g1["orig_occ"], 1)
        self.assertEqual(g1["pert_occ"], 1)
        self.assertEqual(round(g1["orig_val"], 4), 0.1696)
        self.assertEqual(round(g1["pert_val"], 4), 0.1180)
        
        # Second great at position 9
        g2 = great_rows[1]
        self.assertEqual(g2["orig_pos"], 9)
        self.assertEqual(g2["pert_pos"], 9)
        self.assertEqual(g2["orig_occ"], 2)
        self.assertEqual(g2["pert_occ"], 2)
        self.assertEqual(round(g2["orig_val"], 4), 0.0832)
        self.assertEqual(round(g2["pert_val"], 4), 0.0614)
        
        # movie -> film replacement
        movie_row = [r for r in aligned if r.get("token") == "movie"][0]
        self.assertEqual(movie_row["status"], "removed")
        self.assertIsNotNone(movie_row["orig_val"])
        self.assertIsNone(movie_row["pert_val"])
        
        film_row = [r for r in aligned if r.get("token") == "film"][0]
        self.assertEqual(film_row["status"], "inserted")
        self.assertIsNone(film_row["orig_val"])
        self.assertIsNotNone(film_row["pert_val"])

    def test_contrast_repeated_words(self):
        orig_text = "The movie was not great, but the acting was great."
        orig_words = extract_words_with_positions(orig_text)
        greats = [w for w in orig_words if w["token"].lower() == "great"]
        self.assertEqual(len(greats), 2)
        self.assertEqual(greats[0]["position"], 5)
        self.assertEqual(greats[1]["position"], 10)
        self.assertEqual(greats[0]["occurrence"], 1)
        self.assertEqual(greats[1]["occurrence"], 2)

    def test_find_key_misweighted_token_occurrence_awareness(self):
        aligned = [
            {"token": "great", "orig_pos": 4, "pert_pos": 4, "orig_occ": 1, "pert_occ": 1, "total_occ": 2, "orig_val": 0.16, "pert_val": 0.12, "delta": -0.04, "polarity_changed": False, "status": "aligned", "is_key_shift": False},
            {"token": "great", "orig_pos": 9, "pert_pos": 9, "orig_occ": 2, "pert_occ": 2, "total_occ": 2, "orig_val": 0.08, "pert_val": -0.03, "delta": -0.11, "polarity_changed": True, "status": "aligned", "is_key_shift": True},
        ]
        key_ev = find_key_misweighted_token(aligned)
        self.assertIsNotNone(key_ev)
        self.assertEqual(key_ev["token"], "great")
        self.assertEqual(key_ev["occurrence"], 2)
        self.assertEqual(key_ev["position"], 9)
        self.assertTrue(key_ev["polarity_changed"])


if __name__ == "__main__":
    unittest.main()
