"""
Descriptive Cross-Model Comparative Analytics for BlindSpot.
Strictly non-normative: compiles Model x Probe response matrices, pairwise prediction agreements,
and cross-model failure distributions without assigning rankings, scores, or winner/loser status.
"""
from typing import Dict, List, Any, Optional
from collections import defaultdict

from blindspot.core.types import ModelProbeEvaluation, FailureCategory
from blindspot.analysis.fingerprint import ModelBehavioralFingerprint, compute_model_fingerprint
from blindspot.testing.metrics import compute_prediction_agreement


class CrossModelAnalyzer:
    """
    Analyzes and formats comparative metrics across multiple models evaluated against the same probes.
    """
    def __init__(self):
        pass

    def build_model_probe_matrix(
        self,
        model_evaluations: Dict[str, List[ModelProbeEvaluation]],
    ) -> List[Dict[str, Any]]:
        """
        Builds the canonical Model x Probe matrix.
        Rows: Probes. Columns: Per-model outputs (label, confidence, flipped, satisfied).
        """
        if not model_evaluations:
            return []

        # Index evaluations by probe_id
        probes_by_id: Dict[str, Dict[str, Any]] = {}

        for model_id, evals in model_evaluations.items():
            for e in evals:
                pid = e.probe_id
                if pid not in probes_by_id:
                    probes_by_id[pid] = {
                        "probe_id": pid,
                        "seed_text": e.seed_text,
                        "perturbed_text": e.perturbed_text,
                        "perturbation_type": e.perturbation_type,
                        "expected_flip": e.expected_flip,
                        "expected_semantic_effect": e.expected_semantic_effect,
                        "models": {},
                    }

                probes_by_id[pid]["models"][model_id] = {
                    "original_label": e.original_prediction.label,
                    "original_confidence": e.original_prediction.confidence,
                    "formatted_orig_confidence": e.original_prediction.formatted_confidence,
                    "perturbed_label": e.perturbed_prediction.label,
                    "perturbed_confidence": e.perturbed_prediction.confidence,
                    "formatted_pert_confidence": e.perturbed_prediction.formatted_confidence,
                    "is_flipped": e.is_flipped,
                    "expectation_satisfied": e.expectation_satisfied,
                    "confidence_delta_pts": e.confidence_delta_pts,
                    "formatted_delta": e.formatted_confidence_delta,
                }

        return list(probes_by_id.values())

    def compute_pairwise_agreement(
        self,
        model_evaluations: Dict[str, List[ModelProbeEvaluation]],
    ) -> Dict[str, Dict[str, float]]:
        """
        Computes pairwise prediction agreement rates between all evaluated models.
        """
        model_ids = sorted(list(model_evaluations.keys()))
        matrix: Dict[str, Dict[str, float]] = {m: {m2: 1.0 for m2 in model_ids} for m in model_ids}

        # Align predictions on perturbed text by probe_id
        for i, m1 in enumerate(model_ids):
            for j, m2 in enumerate(model_ids):
                if i >= j:
                    continue

                evals1 = {e.probe_id: e.perturbed_prediction.label for e in model_evaluations[m1]}
                evals2 = {e.probe_id: e.perturbed_prediction.label for e in model_evaluations[m2]}

                common_pids = sorted(list(set(evals1.keys()) & set(evals2.keys())))
                if common_pids:
                    preds1 = [evals1[p] for p in common_pids]
                    preds2 = [evals2[p] for p in common_pids]
                    agreement = compute_prediction_agreement(preds1, preds2)
                else:
                    agreement = 0.0

                matrix[m1][m2] = agreement
                matrix[m2][m1] = agreement

        return matrix

    def summarize_cross_model_failures(
        self,
        model_failures: Dict[str, List[Dict[str, Any]]],
    ) -> Dict[str, Dict[str, int]]:
        """
        Aggregates failure counts per model broken down by the 4-way taxonomy.
        """
        breakdown: Dict[str, Dict[str, int]] = {}
        all_categories = [c.value for c in FailureCategory]

        for model_id, failures in model_failures.items():
            counts = {cat: 0 for cat in all_categories}
            for f in failures:
                cat = f.get("category")
                if cat in counts:
                    counts[cat] += 1
                else:
                    counts[FailureCategory.UNDETERMINED.value] += 1
            breakdown[model_id] = counts

        return breakdown

    def compare_models(
        self,
        model_evaluations: Dict[str, List[ModelProbeEvaluation]],
        model_failures: Dict[str, List[Dict[str, Any]]],
        model_eces: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Produces full descriptive cross-model comparative report data.
        """
        eces = model_eces or {}
        model_ids = sorted(list(model_evaluations.keys()))

        # 1. Behavioral fingerprints
        fingerprints: Dict[str, Dict[str, Any]] = {}
        for m_id in model_ids:
            evals = model_evaluations.get(m_id, [])
            fails = model_failures.get(m_id, [])
            ece_val = eces.get(m_id, 0.0)
            fp = compute_model_fingerprint(m_id, evals, fails, ece=ece_val)
            fingerprints[m_id] = fp.to_dict()

        # 2. Pairwise agreement
        pairwise_agreement = self.compute_pairwise_agreement(model_evaluations)

        # Average agreement across distinct model pairs
        agreements = []
        for i, m1 in enumerate(model_ids):
            for j, m2 in enumerate(model_ids):
                if i < j:
                    agreements.append(pairwise_agreement[m1][m2])
        overall_agreement = float(sum(agreements) / len(agreements)) if agreements else 1.0

        # 3. Model x Probe Matrix
        matrix = self.build_model_probe_matrix(model_evaluations)

        # 4. Failures Breakdown
        failure_summary = self.summarize_cross_model_failures(model_failures)

        return {
            "model_ids": model_ids,
            "overall_agreement_rate": overall_agreement,
            "pairwise_agreement": pairwise_agreement,
            "fingerprints": fingerprints,
            "failure_summary": failure_summary,
            "model_probe_matrix": matrix,
        }
