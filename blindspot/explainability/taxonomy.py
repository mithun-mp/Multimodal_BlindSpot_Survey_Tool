"""
Evidence-Backed 4-Way Failure Taxonomy Classifier for BlindSpot.
Diagnoses model failures into:
1. Blind: The model fails to register explicit syntactic operators (negation/connectives).
2. Spurious: Model decisions are altered by irrelevant or meaning-preserving perturbations.
3. Misweighted: Token weights are inappropriately allocated across clauses or inconsistent with degree shift.
4. Undetermined: An unexpected behavioral deviation occurred, but evidence does not cleanly isolate causality.
"""
from typing import Dict, Any, List, Optional
import uuid

from blindspot.core.types import FailureCategory, BehavioralOutcome
from blindspot.testing.behavioral import classify_behavior


class TaxonomyClassifier:
    """
    Classifies auditing failures into the 4-way traceable taxonomy:
    Blind, Spurious, Misweighted, and Undetermined.
    Backed by probe contract expectations and optional XAI attribution evidence.
    """
    def __init__(self):
        self.stop_words = {
            "the", "a", "an", "is", "was", "are", "were", "it", "this", "that",
            "in", "on", "at", "to", "for", "of", "and", "or", "by", "with"
        }
        self.negation_tokens = {
            "not", "never", "no", "n't", "neither", "nor", "hardly", "barely", "scarcely"
        }

    def classify_failure(
        self,
        perturbation_type: str,
        original_sentence: str,
        perturbed_sentence: str,
        original_label: str,
        perturbed_label: str,
        is_flipped: bool,
        expected_flip: bool,
        orig_explanation: Optional[Dict[str, float]] = None,
        pert_explanation: Optional[Dict[str, float]] = None,
        model_id: str = "",
        probe_id: str = "",
        confidence_delta: float = 0.0,
        expected_semantic_effect: str = "",
        semantic_intent: str = "",
        original_confidence: float = 1.0,
        perturbed_confidence: float = 1.0,
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluates a single original-perturbed pair and returns traceable failure diagnosis if a failure occurs.
        Returns None if model behaved correctly and explanation is sound.
        """
        orig_exp = dict(orig_explanation) if orig_explanation else {}
        pert_exp = dict(pert_explanation) if pert_explanation else {}

        eff = expected_semantic_effect or ("invert" if expected_flip else "preserve")

        # 1. Primary Behavioral Classification
        outcome, failure_cat, base_evidence, rationale = classify_behavior(
            original_label=original_label,
            probe_label=perturbed_label,
            original_confidence=original_confidence,
            probe_confidence=perturbed_confidence,
            expected_effect=eff,
            semantic_intent=semantic_intent or ("REVERSE_POLARITY" if expected_flip else "PRESERVE_MEANING"),
            expected_label_relation="DIFFERENT_LABEL" if expected_flip else "SAME_LABEL",
        )

        # 2. If behavioral failure detected, enrich with XAI evidence if available
        if failure_cat != FailureCategory.NONE:
            evidence = dict(base_evidence)
            evidence.update({
                "probe_type": perturbation_type,
                "model_id": model_id,
                "probe_id": probe_id,
                "confidence_delta": confidence_delta,
            })

            # Check negation tokens in explanation
            if pert_exp:
                neg_tokens = [w for w in pert_exp.keys() if w.lower() in self.negation_tokens]
                neg_weight = max([abs(pert_exp.get(w, 0.0)) for w in neg_tokens], default=0.0)
                evidence["negation_tokens_found"] = neg_tokens
                evidence["max_negation_attribution"] = neg_weight
                evidence["top_attributions"] = sorted(pert_exp.items(), key=lambda x: abs(x[1]), reverse=True)[:5]

            severity = "high" if failure_cat in (FailureCategory.BLIND, FailureCategory.SPURIOUS) else "medium"

            recommendations = {
                FailureCategory.BLIND.value: "Fine-tune target model on negation augmentations and verify syntactic modifier attention heads.",
                FailureCategory.SPURIOUS.value: "Apply adversarial synonym swaps and invariant regularization to suppress spurious sensitivity.",
                FailureCategory.MISWEIGHTED.value: "Incorporate contrastive loss and clause-level balancing to align degree sensitivity.",
                FailureCategory.UNDETERMINED.value: "Examine counterfactual variations and inspect full probability distribution shifts.",
            }

            return {
                "category": failure_cat.value,
                "reason": rationale,
                "details": f"Under {perturbation_type}, model transition '{original_label} -> {perturbed_label}' was diagnosed as {failure_cat.value}. {rationale}",
                "recommendation": recommendations.get(failure_cat.value, "Review linguistic test suite coverage."),
                "severity": severity,
                "evidence": evidence,
            }

        # 3. If behavioral prediction was preserved, check explanation-level anomalies
        if pert_exp and orig_exp:
            # Check synonym substitution attribution instability
            if "substitution" in perturbation_type.lower() and not is_flipped:
                syn_keys = set(orig_exp.keys()).intersection(set(pert_exp.keys()))
                if syn_keys:
                    orig_pos = sum(1 for k in syn_keys if orig_exp[k] > 0)
                    pert_pos = sum(1 for k in syn_keys if pert_exp[k] > 0)
                    if (orig_pos > 0 and pert_pos == 0) or (orig_pos == 0 and pert_pos > 0):
                        return {
                            "category": FailureCategory.MISWEIGHTED.value,
                            "reason": "Synonym substitution caused unstable attribution polarity shift.",
                            "details": "Substituting a word with its synonym inverted attribution weights without label flip.",
                            "recommendation": "Incorporate embedding regularization to align representation spaces of close synonyms.",
                            "severity": "medium",
                            "evidence": {
                                "common_tokens": list(syn_keys),
                                "orig_positive_count": orig_pos,
                                "pert_positive_count": pert_pos,
                            },
                        }

        return None
