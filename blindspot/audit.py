"""
Main Orchestrator for the BlindSpot auditing framework.
Operates on the 'pretrained model in, diagnostic report out' principle.
Supports single-model audits (backward compatible) and multi-model research experiments.
"""
import os
import re
from typing import Dict, Any, List, Optional, Union
import logging

from blindspot.models.huggingface_wrapper import HuggingFaceWrapper
from blindspot.models.registry import ModelRegistry
from blindspot.models.cache import ModelCache
from blindspot.perturbations.engine import PerturbationEngine
from blindspot.perturbations.shared import SharedProbeGenerator
from blindspot.testing.behavioral import BehavioralTester
from blindspot.explainability.lime_explainer import LimeExplainerWrapper
from blindspot.explainability.shap_explainer import ShapExplainerWrapper
from blindspot.explainability.alignment import compute_jaccard_similarity, compute_attribution_cosine
from blindspot.explainability.taxonomy import TaxonomyClassifier
from blindspot.explainability.token_attributions import align_token_attributions
from blindspot.reporting.report_generator import ReportGenerator
from blindspot.core.types import ExplanationResult

logger = logging.getLogger(__name__)


class AuditPipeline:
    """
    Main Orchestrator for the BlindSpot auditing framework.
    Provides single-model and multi-model audit workflows with full backward compatibility.
    """
    def __init__(
        self,
        model_name_or_path: str = "distilbert-base-uncased-finetuned-sst-2-english",
        output_dir: str = "audit_reports",
        explainer_type: str = "lime",
        confidence_threshold: float = 0.65,
        random_seed: int = 42,
    ):
        self.random_seed = random_seed
        self.model_cache = ModelCache()
        self.model = self.model_cache.get_or_load(model_name_or_path)
        self.perturber = PerturbationEngine()
        self.tester = BehavioralTester(self.model)
        self.lime_explainer = LimeExplainerWrapper(self.model, random_seed=random_seed)
        self.shap_explainer = ShapExplainerWrapper(self.model)
        self.taxonomy = TaxonomyClassifier()
        self.reporter = ReportGenerator(output_dir)
        self.explainer_type = explainer_type.lower()
        self.confidence_threshold = confidence_threshold
        self.output_dir = output_dir

    def _get_explanation(self, text: str) -> ExplanationResult:
        """
        Gets token attributions based on configured explainer_type ('lime', 'shap', or 'both').
        """
        if self.explainer_type == "shap":
            return self.shap_explainer.explain(text)
        elif self.explainer_type == "both":
            lime_exp = self.lime_explainer.explain(text)
            shap_exp = self.shap_explainer.explain(text)
            # Combine attributions by averaging
            combined = {}
            all_keys = set(list(lime_exp.keys()) + list(shap_exp.keys()))
            for k in all_keys:
                v_lime = lime_exp.get(k, 0.0)
                v_shap = shap_exp.get(k, 0.0)
                combined[k] = (v_lime + v_shap) / 2.0
            return ExplanationResult(
                token_weights=combined,
                token_attributions=lime_exp.token_attributions,
                model_id=self.model.model_name,
                text=text,
                explainer_requested="both",
                explainer_used="both",
                random_seed=self.random_seed,
            )
        else:
            # Default to LIME
            return self.lime_explainer.explain(text)

    def validate_input(self, sentence: Any, min_length: int = 3, max_length: int = 500) -> str:
        """
        Validates input sentence for type correctness, non-emptiness, min/max length, and valid text content.
        """
        if not isinstance(sentence, str):
            raise TypeError(f"Input sentence must be a string, got {type(sentence).__name__}.")

        clean_sentence = sentence.strip()
        if not clean_sentence:
            raise ValueError("Invalid input: Please enter meaningful natural-language text containing alphabetic characters.")

        if not any(c.isalpha() for c in clean_sentence):
            raise ValueError("Invalid input: Please enter meaningful natural-language text containing alphabetic characters.")

        if len(clean_sentence) < min_length:
            raise ValueError(f"Input sentence is too short ({len(clean_sentence)} characters). Minimum required length is {min_length} characters.")

        if len(clean_sentence) > max_length:
            raise ValueError(f"Input sentence exceeds maximum length limit of {max_length} characters (got {len(clean_sentence)} characters).")

        return clean_sentence

    def check_suitability(self, sentence: str) -> Dict[str, Any]:
        """
        Checks whether a valid input is suitable or potentially weak/ambiguous.
        Does NOT raise exceptions, allowing the audit pipeline to continue with a warning.
        """
        raw_tokens = sentence.strip().split()
        words = [re.sub(r"[^\w]", "", w).lower() for w in raw_tokens]
        words = [w for w in words if w]

        weak_sentiment_words = {"normal", "okay", "ok", "average", "mediocre", "moderate", "plain", "fair", "so-so", "standard", "neutral"}

        is_ambiguous = False
        warning = None
        status = "suitable"

        if len(words) <= 2:
            is_ambiguous = True
            status = "unsuitable"
            warning = "Warning: This input may be incomplete or contain weak/ambiguous sentiment. Results should be interpreted cautiously."
        elif any(w in weak_sentiment_words for w in words):
            is_ambiguous = True
            status = "unsuitable"
            warning = "Warning: This input may be incomplete or contain weak/ambiguous sentiment. Results should be interpreted cautiously."

        return {
            "status": status,
            "warning": warning,
            "is_ambiguous": is_ambiguous,
            "word_count": len(words)
        }

    def run_audit(self, sentence: str) -> Dict[str, Any]:
        """
        Runs the full end-to-end auditing workflow on a single sentence.
        Maintains 100% backward compatibility with existing tests and scripts.
        """
        sentence = self.validate_input(sentence)
        suitability_info = self.check_suitability(sentence)

        if suitability_info["warning"]:
            logger.warning(suitability_info["warning"])

        logger.info(f"Starting audit for sentence: '{sentence}' using explainer: '{self.explainer_type}'")

        # Step 1: Perturbation Generation
        perturbations = self.perturber.generate_all(sentence)
        logger.info(f"Generated {len(perturbations)} linguistic variants.")

        # Step 2: Behavioral Testing
        behavioral_results = self.tester.evaluate_probe(sentence, perturbations)

        orig_conf = behavioral_results.get("original_confidence", 1.0)
        confidence_info = {
            "is_low_confidence": orig_conf <= self.confidence_threshold,
            "threshold": self.confidence_threshold,
            "warning": "Low-confidence prediction: the model is uncertain about the sentiment." if orig_conf <= self.confidence_threshold else None,
            "neutral_clarification": "Input may express weak or ambiguous sentiment. The underlying classifier does not provide an explicit neutral class." if (orig_conf <= self.confidence_threshold or suitability_info["is_ambiguous"]) else None
        }

        behavioral_results["suitability_info"] = suitability_info
        behavioral_results["confidence_info"] = confidence_info

        # Step 3: Explainability Extraction & Alignment
        orig_explanation = self._get_explanation(sentence)
        explanations_summary = []
        failures = []

        for item in behavioral_results["probe_details"]:
            pert_text = item["perturbed"]
            pert_explanation = self._get_explanation(pert_text)

            jaccard = compute_jaccard_similarity(orig_explanation, pert_explanation)
            cosine = compute_attribution_cosine(orig_explanation, pert_explanation)
            aligned_tokens = align_token_attributions(sentence, pert_text, orig_explanation, pert_explanation)

            exp_item = {
                "original": sentence,
                "perturbed": pert_text,
                "type": item["type"],
                "orig_explanation": orig_explanation,
                "pert_explanation": pert_explanation,
                "aligned_tokens": aligned_tokens,
                "jaccard_similarity": jaccard,
                "cosine_alignment": cosine,
            }
            explanations_summary.append(exp_item)

            # Step 4: Taxonomy Classification
            failure = self.taxonomy.classify_failure(
                perturbation_type=item["type"],
                original_sentence=sentence,
                perturbed_sentence=pert_text,
                original_label=item["original_label"],
                perturbed_label=item["perturbed_label"],
                is_flipped=item["is_flipped"],
                expected_flip=item["expected_flip"],
                orig_explanation=orig_explanation,
                pert_explanation=pert_explanation,
                model_id=self.model.model_name,
                probe_id=item.get("probe_id", ""),
                confidence_delta=item.get("confidence_delta", 0.0),
            )
            if failure:
                failure["probe_type"] = item["type"]
                failure["probe_description"] = item.get("description", "")
                failure["original_sentence"] = sentence
                failure["perturbed_sentence"] = pert_text
                failure["original_label"] = item["original_label"]
                failure["perturbed_label"] = item["perturbed_label"]
                failure["original_confidence"] = item["original_confidence"]
                failure["perturbed_confidence"] = item["perturbed_confidence"]
                failure["is_flipped"] = item["is_flipped"]
                failure["expected_flip"] = item["expected_flip"]
                failure["confidence_delta"] = item.get("confidence_delta", 0.0)
                failure["conf_delta_pts"] = item.get("confidence_delta_pts", 0.0)
                failure["orig_explanation"] = orig_explanation
                failure["pert_explanation"] = pert_explanation
                failure["aligned_tokens"] = aligned_tokens
                failure["orig_token_attributions"] = getattr(orig_explanation, "token_attributions", [])
                failure["pert_token_attributions"] = getattr(pert_explanation, "token_attributions", [])
                failures.append(failure)

        # Step 5: Report Generation
        generated_reports = self.reporter.generate_all_reports(
            model_name=self.model.model_name,
            audit_results=behavioral_results,
            failures=failures,
            explanations_summary=explanations_summary,
        )

        return {
            "behavioral_results": behavioral_results,
            "suitability_info": suitability_info,
            "confidence_info": confidence_info,
            "failures": failures,
            "explanations_summary": explanations_summary,
            "generated_reports": generated_reports,
        }

    def run_multimodel_audit(
        self,
        sentences: List[str],
        model_ids: List[str],
        explainer_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Executes a multi-model audit experiment using the asynchronous execution runner.
        """
        from blindspot.core.config import ExperimentConfig
        from blindspot.execution.runner import ExperimentRunner

        cfg = ExperimentConfig(
            experiment_name="Multi-Model Audit",
            input_sentences=sentences,
            model_ids=model_ids,
            explainer_type=explainer_type or self.explainer_type,
            random_seed=self.random_seed,
            confidence_threshold=self.confidence_threshold,
            output_dir=self.output_dir,
        )

        runner = ExperimentRunner(config=cfg)
        return runner.run_sync()


def run_multimodel_audit(
    sentences: List[str],
    model_ids: List[str],
    explainer_type: str = "lime",
    output_dir: str = "runs",
) -> Dict[str, Any]:
    """
    Top-level convenience function for executing a multimodel audit experiment.
    """
    from blindspot.core.config import ExperimentConfig
    from blindspot.execution.runner import ExperimentRunner

    cfg = ExperimentConfig(
        experiment_name="Multi-Model Audit",
        input_sentences=sentences,
        model_ids=model_ids,
        explainer_type=explainer_type,
        output_dir=output_dir,
    )
    runner = ExperimentRunner(config=cfg)
    return runner.run_sync()
