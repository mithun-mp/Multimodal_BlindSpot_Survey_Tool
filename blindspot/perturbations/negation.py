import re
from typing import List, Dict, Any
from .base import BasePerturber

def _clean_text(text: str) -> str:
    """Helper to clean whitespace, space before punctuation, and space after hyphens."""
    # Normalize multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    # Remove space before punctuation
    text = re.sub(r"\s+([,.\!?])", r"\1", text)
    # Fix space after prefix hyphen (e.g., 'un- awesome' -> 'un-awesome')
    text = re.sub(r"\b(un|non|in|im|dis|re)-\s+(\w+)", r"\1-\2", text, flags=re.IGNORECASE)
    return text

def _format_subject(sentence: str) -> str:
    """Formats sentence subject for inclusion after a clause prefix, preserving 'I' capitalization."""
    sentence = sentence.strip()
    if not sentence:
        return sentence
    if sentence.startswith("I ") or sentence.startswith("I'") or sentence.startswith("I\t"):
        return sentence
    return sentence[0].lower() + sentence[1:]

class NegationPerturber(BasePerturber):
    """
    Generates controlled single negation perturbations.
    """
    def __init__(self):
        super().__init__(name="Negation Engine", perturbation_type="negation")

    def perturb(self, sentence: str) -> List[Dict[str, Any]]:
        results = []
        clean_sentence = _clean_text(sentence)

        aux_patterns = [
            (r"\b(is|was|are|were|am|feels|looks|seems|tastes|sounds)\b", r"\1 not"),
            (r"\b(can|could|would|should|will|must)\b", r"\1 not"),
            (r"\b(has|have|had)\b", r"\1 not"),
        ]

        # Check if sentence already has negation
        if re.search(r"\b(not|never|no|n't)\b", clean_sentence, re.IGNORECASE):
            # Remove negation
            de_negated = re.sub(r"\b(not|never)\s*", "", clean_sentence, flags=re.IGNORECASE)
            de_negated = re.sub(r"n't\b", "", de_negated, flags=re.IGNORECASE)
            results.append({
                "original": sentence,
                "perturbed": _clean_text(de_negated),
                "type": "negation_removal",
                "description": "Removed negation token from sentence."
            })
        else:
            for pattern, replacement in aux_patterns:
                if re.search(pattern, clean_sentence, re.IGNORECASE):
                    perturbed = re.sub(pattern, replacement, clean_sentence, count=1, flags=re.IGNORECASE)
                    if perturbed != clean_sentence:
                        results.append({
                            "original": sentence,
                            "perturbed": _clean_text(perturbed),
                            "type": "negation_insertion",
                            "description": "Inserted negation 'not' after auxiliary verb."
                        })
                        break

            # Fallback insertion before adjectives/main verbs
            if not results:
                subj = _format_subject(clean_sentence)
                perturbed = f"It is not true that {subj}"
                results.append({
                    "original": sentence,
                    "perturbed": _clean_text(perturbed),
                    "type": "negation_prefix",
                    "description": "Prefixed sentence with explicit negation frame."
                })

        return results


class DoubleNegationPerturber(BasePerturber):
    """
    Generates controlled double negation perturbations using standard English litotes and double negative framing.
    """
    def __init__(self):
        super().__init__(name="Double Negation Engine", perturbation_type="double_negation")

    def perturb(self, sentence: str) -> List[Dict[str, Any]]:
        results = []
        clean_sentence = _clean_text(sentence)
        
        # Check if already negated
        if re.search(r"\b(not|n't)\b", clean_sentence, re.IGNORECASE):
            double_neg = re.sub(r"\bnot\b", "not entirely non-", clean_sentence, flags=re.IGNORECASE)
            results.append({
                "original": sentence,
                "perturbed": _clean_text(double_neg),
                "type": "double_negation",
                "description": "Constructed double negation pattern."
            })
        else:
            subj = _format_subject(clean_sentence)
            
            # Variant 1: "It is not impossible that..."
            double_neg1 = f"It is not impossible that {subj}"
            results.append({
                "original": sentence,
                "perturbed": _clean_text(double_neg1),
                "type": "double_negation",
                "description": "Framed sentence with double negation ('It is not impossible that')."
            })
            
            # Variant 2: "It is not untrue that..."
            double_neg2 = f"It is not untrue that {subj}"
            results.append({
                "original": sentence,
                "perturbed": _clean_text(double_neg2),
                "type": "double_negation",
                "description": "Framed sentence with double negation ('It is not untrue that')."
            })

        return results


