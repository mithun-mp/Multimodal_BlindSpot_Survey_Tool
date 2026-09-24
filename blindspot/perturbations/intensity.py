"""
Controlled Intensity Perturbation Engine for Text Classifiers.
Injects intensifiers (strengthening) and downtoners (weakening) to test model
sensitivity to degree adverbs without semantic polarity inversion.
"""
import re
from typing import List, Dict, Any
from .base import BasePerturber

INTENSIFIERS = ["extremely", "incredibly", "truly", "exceptionally", "absolutely", "remarkably"]
DOWNTONERS = ["somewhat", "slightly", "fairly", "moderately", "marginally"]

# Common sentiment-bearing adjectives and adverbs to target
TARGET_ADJECTIVES = {
    "good", "great", "excellent", "superb", "wonderful", "fantastic", "amazing", "pleasant", "brilliant",
    "bad", "terrible", "awful", "horrible", "poor", "dreadful", "disappointing", "boring", "mediocre",
    "clean", "fast", "slow", "effective", "useless", "helpful", "valuable", "worthless", "happy", "sad",
    "positive", "negative", "clear", "flawed", "compelling", "impressive", "engaging", "tedious"
}


class IntensityPerturber(BasePerturber):
    """
    Applies intensifiers and downtoners to test degree-sensitivity.
    Semantic expectation: preserve polarity (expected_flip=False),
    with expected_semantic_effect='strengthen' or 'weaken'.
    """
    def __init__(self):
        super().__init__(name="Intensity Perturbation", perturbation_type="intensity")

    def perturb(self, sentence: str) -> List[Dict[str, Any]]:
        variants: List[Dict[str, Any]] = []
        if not sentence or not sentence.strip():
            return variants

        clean_sent = sentence.strip()
        tokens = clean_sent.split()
        if not tokens:
            return variants

        # Strategy 1: Target matched adjectives in the sentence
        found_target = False
        for idx, token in enumerate(tokens):
            clean_tok = re.sub(r"[^\w\s]", "", token).lower()
            if clean_tok in TARGET_ADJECTIVES:
                found_target = True
                # Generate 1-2 intensifiers
                for intensifier in INTENSIFIERS[:2]:
                    new_tokens = list(tokens)
                    new_tokens.insert(idx, intensifier)
                    pert_text = " ".join(new_tokens)
                    variants.append({
                        "original": clean_sent,
                        "perturbed": pert_text,
                        "type": "intensity",
                        "subtype": "intensifier",
                        "description": f"Injected intensifier '{intensifier}' before '{token}'",
                        "expected_flip": False,
                        "expected_semantic_effect": "strengthen",
                        "semantic_intent": "STRENGTHEN_POLARITY",
                        "token_index": idx,
                        "original_token": token,
                        "replacement_token": f"{intensifier} {token}",
                    })
                # Generate 1-2 downtoners
                for downtoner in DOWNTONERS[:2]:
                    new_tokens = list(tokens)
                    new_tokens.insert(idx, downtoner)
                    pert_text = " ".join(new_tokens)
                    variants.append({
                        "original": clean_sent,
                        "perturbed": pert_text,
                        "type": "intensity",
                        "subtype": "downtoner",
                        "description": f"Injected downtoner '{downtoner}' before '{token}'",
                        "expected_flip": False,
                        "expected_semantic_effect": "weaken",
                        "semantic_intent": "WEAKEN_POLARITY",
                        "token_index": idx,
                        "original_token": token,
                        "replacement_token": f"{downtoner} {token}",
                    })
                break  # Target first matching adjective to keep candidate pool focused

        # Strategy 2: If no explicit target adjective is matched, inject degree adverb before the main verb / predicate
        if not found_target and len(tokens) >= 2:
            # Inject after first token if it's a pronoun/noun (e.g. "The movie was..." -> "The movie was truly...")
            insert_pos = 1 if len(tokens) <= 3 else 2
            intensifier = INTENSIFIERS[0]
            new_tokens = list(tokens)
            new_tokens.insert(insert_pos, intensifier)
            variants.append({
                "original": clean_sent,
                "perturbed": " ".join(new_tokens),
                "type": "intensity",
                "subtype": "intensifier",
                "description": f"Injected degree adverb '{intensifier}' into clause",
                "expected_flip": False,
                "expected_semantic_effect": "strengthen",
                "semantic_intent": "STRENGTHEN_POLARITY",
                "token_index": insert_pos,
                "original_token": "",
                "replacement_token": intensifier,
            })

            downtoner = DOWNTONERS[0]
            new_tokens_down = list(tokens)
            new_tokens_down.insert(insert_pos, downtoner)
            variants.append({
                "original": clean_sent,
                "perturbed": " ".join(new_tokens_down),
                "type": "intensity",
                "subtype": "downtoner",
                "description": f"Injected moderating downtoner '{downtoner}' into clause",
                "expected_flip": False,
                "expected_semantic_effect": "weaken",
                "semantic_intent": "WEAKEN_POLARITY",
                "token_index": insert_pos,
                "original_token": "",
                "replacement_token": downtoner,
            })

        return variants
