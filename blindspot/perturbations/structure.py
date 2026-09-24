"""
Controlled Structural Perturbation Engine for Text Classifiers.
Tests model robustness against syntactic clause reordering, adverb fronting,
and punctuation/formatting shifts while preserving semantic truth-conditions.
"""
import re
from typing import List, Dict, Any
from .base import BasePerturber


class StructurePerturber(BasePerturber):
    """
    Applies structural and syntactic transformations without altering semantic polarity.
    Semantic expectation: preserve polarity (expected_flip=False, expected_semantic_effect='preserve').
    """
    def __init__(self):
        super().__init__(name="Structural Perturbation", perturbation_type="structure")

    def perturb(self, sentence: str) -> List[Dict[str, Any]]:
        variants: List[Dict[str, Any]] = []
        if not sentence or not sentence.strip():
            return variants

        clean_sent = sentence.strip()

        # 1. Comma-separated clause inversion (e.g. "Because it was raining, the event was postponed.")
        if "," in clean_sent:
            parts = [p.strip() for p in clean_sent.split(",", 1)]
            if len(parts) == 2 and parts[0] and parts[1]:
                p1, p2 = parts[0], parts[1]
                # Strip trailing period from p2
                p2_clean = p2.rstrip(".!?")
                punct = clean_sent[-1] if clean_sent[-1] in ".!?" else "."
                inverted = f"{p2_clean[0].upper() + p2_clean[1:]}, {p1[0].lower() + p1[1:]}{punct}"
                if inverted != clean_sent:
                    variants.append({
                        "original": clean_sent,
                        "perturbed": inverted,
                        "type": "structure",
                        "subtype": "clause_inversion",
                        "description": "Inverted comma-separated clauses while preserving truth conditions",
                        "expected_flip": False,
                        "expected_semantic_effect": "preserve",
                        "semantic_intent": "PRESERVE_MEANING",
                    })

        # 2. Fronting adverbial frame / discourse markers
        # E.g. "In my honest opinion, ..." or "Without a doubt, ..."
        markers = [
            ("In fact, ", "In fact discourse frame"),
            ("To be honest, ", "Honesty discourse frame"),
            ("Undeniably, ", "Adverbial fronting"),
        ]
        chosen_prefix, desc = markers[0]
        # lowercase first char of sentence
        rest = clean_sent[0].lower() + clean_sent[1:] if len(clean_sent) > 1 else clean_sent
        fronted = f"{chosen_prefix}{rest}"
        variants.append({
            "original": clean_sent,
            "perturbed": fronted,
            "type": "structure",
            "subtype": "discourse_framing",
            "description": f"Fronted discourse frame: '{chosen_prefix.strip()}'",
            "expected_flip": False,
            "expected_semantic_effect": "preserve",
            "semantic_intent": "PRESERVE_MEANING",
        })

        # 3. Punctuation and emphasis shift (e.g. ellipses, exclamation mark)
        base_no_punct = clean_sent.rstrip(".!?")
        if clean_sent.endswith("!"):
            pert_punct = f"{base_no_punct}."
            pdesc = "Replaced exclamation mark with period"
        elif clean_sent.endswith("."):
            pert_punct = f"{base_no_punct}..."
            pdesc = "Replaced terminal period with trailing ellipsis"
        else:
            pert_punct = f"{clean_sent}."
            pdesc = "Normalized trailing period"

        variants.append({
            "original": clean_sent,
            "perturbed": pert_punct,
            "type": "structure",
            "subtype": "punctuation_drift",
            "description": pdesc,
            "expected_flip": False,
            "expected_semantic_effect": "preserve",
            "semantic_intent": "PRESERVE_MEANING",
        })

        return variants
