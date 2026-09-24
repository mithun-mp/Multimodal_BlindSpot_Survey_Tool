"""
Shared Probe Generation Protocol for Multimodel Auditing.
Generates controlled, deterministic linguistic probes with stable IDs and calibrated semantic expectations.
Adheres strictly to research-valid behavioral auditing contracts.
"""
from typing import List, Dict, Any, Optional, Tuple, Union
import uuid
import time
import re

from blindspot.core.types import (
    LinguisticProbe,
    SharedProbeSet,
    ProbeStatus,
    SemanticIntent,
    SentenceType,
    ExpectedEffect,
    ExpectedLabelRelation,
    ExpectedConfidenceRelation,
)
from blindspot.perturbations.engine import PerturbationEngine

SharedProbe = LinguisticProbe

# Curated reference representations for figurative and proverbial expressions
KNOWN_PROVERBS = {
    "all that glitters is not gold": {
        "paraphrase_preserve": "Not everything that glitters is truly valuable.",
        "inversion_flip": "All that glitters is gold.",
        "scope_preserve": "Not all shiny objects possess genuine value.",
        "semantic_interpretation": "Appearances can be deceptive; superficial attraction does not guarantee intrinsic value.",
    },
    "actions speak louder than words": {
        "paraphrase_preserve": "What people do carries far more weight than what they say.",
        "inversion_flip": "Words speak louder than actual deeds.",
        "scope_preserve": "A person's conduct reveals more than their promises.",
        "semantic_interpretation": "Tangible behavior is a more reliable metric than verbal claims.",
    },
    "a bird in the hand is worth two in the bush": {
        "paraphrase_preserve": "Having something certain is better than risking it for potential gain.",
        "inversion_flip": "A bird in the bush is worth more than one in hand.",
        "scope_preserve": "Certain possession is superior to speculative opportunity.",
        "semantic_interpretation": "Prudence favors current certainty over speculative ambition.",
    },
    "every cloud has a silver lining": {
        "paraphrase_preserve": "Every difficult situation contains a redeeming positive aspect.",
        "inversion_flip": "No cloud has any silver lining whatsoever.",
        "scope_preserve": "There is an encouraging element even within misfortune.",
        "semantic_interpretation": "Optimism: adversity persistently contains an opportunity for hope.",
    },
}


def infer_semantic_intent(
    perturbation_type: str,
    subtype: Optional[str] = None,
    description: str = "",
) -> SemanticIntent:
    """Infers canonical SemanticIntent for a perturbation."""
    ptype = perturbation_type.lower()
    desc = description.lower()
    stype = (subtype or "").lower()

    if "negation" in ptype and "double" not in ptype:
        if "removal" in ptype or "removal" in desc or "removal" in stype:
            return SemanticIntent.REMOVE_NEGATION
        return SemanticIntent.ADD_NEGATION
    elif "double_negation" in ptype or ("double" in ptype and "negation" in ptype):
        return SemanticIntent.PRESERVE_MEANING
    elif "synonym" in ptype or "substitution" in ptype:
        return SemanticIntent.PRESERVE_MEANING
    elif "intensity" in ptype:
        if "intensifier" in stype or "intensifier" in desc or "strengthen" in desc:
            return SemanticIntent.STRENGTHEN_POLARITY
        elif "downtoner" in stype or "downtoner" in desc or "weaken" in desc:
            return SemanticIntent.WEAKEN_POLARITY
    elif "contrast_positive" in ptype or ("contrast" in ptype and "positive" in ptype):
        return SemanticIntent.PRESERVE_MEANING
    elif "contrast" in ptype or "connective" in ptype:
        return SemanticIntent.SHIFT_CONTRAST
    elif "structure" in ptype:
        return SemanticIntent.PRESERVE_MEANING
    elif "proverb" in ptype or "figurative" in ptype:
        if "inversion" in ptype or "removal" in ptype or "reversal" in desc or "invert" in desc:
            return SemanticIntent.REVERSE_POLARITY
        return SemanticIntent.PRESERVE_MEANING

    return SemanticIntent.PRESERVE_MEANING


def infer_expected_semantic_effect(
    perturbation_type: str,
    subtype: Optional[str] = None,
    description: str = "",
) -> Tuple[str, bool]:
    """
    Infers the expected semantic effect and whether the prediction label is expected to flip.
    Returns: (expected_semantic_effect, expected_flip)
    """
    ptype = perturbation_type.lower()
    desc = description.lower()
    stype = (subtype or "").lower()

    # 1. Single Negation (Insertion, Removal, Prefix)
    if "negation" in ptype and "double" not in ptype:
        return "invert", True

    # 2. Double Negation
    if "double_negation" in ptype or ("double" in ptype and "negation" in ptype):
        return "preserve", False

    # 3. Lexical / Synonym Substitution
    if "synonym" in ptype or "substitution" in ptype:
        return "preserve", False

    # 4. Intensity Modulation
    if "intensity" in ptype:
        if "intensifier" in stype or "intensifier" in desc or "strengthen" in desc:
            return "strengthen", False
        elif "downtoner" in stype or "downtoner" in desc or "weaken" in desc:
            return "weaken", False
        return "preserve", False

    # 5. Syntactic Structure
    if "structure" in ptype:
        return "preserve", False

    # 6. Contrast & Connectives
    if "contrast" in ptype or "connective" in ptype:
        if "negative_append" in ptype:
            return "invert", True
        elif "concession" in ptype:
            return "concession", True
        elif "positive" in ptype or "positive_append" in ptype:
            return "preserve", False
        elif "adversative" in desc or "contrast" in desc:
            return "invert", True
        else:
            return "preserve", False

    # 7. Proverb & Figurative
    if "proverb" in ptype or "figurative" in ptype:
        if "inversion" in ptype or "removal" in ptype or "reversal" in desc:
            return "invert", True
        return "preserve", False

    return "preserve", False


# Canonical mapping from user display categories to internal perturber subtype identifiers
DISPLAY_CATEGORY_TO_SUBTYPES: Dict[str, List[str]] = {
    "negation": [
        "negation",
        "negation_insertion",
        "negation_removal",
        "negation_prefix",
    ],
    "double_negation": [
        "double_negation",
    ],
    "connective": [
        "connective",
        "contrast",
        "contrast_negative_append",
        "contrast_concession_prefix",
        "concession",
    ],
    "contrast": [
        "connective",
        "contrast",
        "contrast_negative_append",
        "contrast_concession_prefix",
        "concession",
    ],
    "contrast_positive": [
        "contrast_positive",
        "contrast_positive_append",
        "positive_contrast",
    ],
    "synonym_substitution": [
        "synonym_substitution",
        "synonym",
        "substitution",
        "lexical",
        "lexical_swap",
        "proverb_paraphrase",
    ],
    "substitution": [
        "synonym_substitution",
        "synonym",
        "substitution",
        "lexical",
        "lexical_swap",
        "proverb_paraphrase",
    ],
    "lexical": [
        "lexical",
        "lexical_swap",
        "synonym",
        "synonym_substitution",
        "substitution",
        "proverb_paraphrase",
    ],
    "lexical_swap": [
        "lexical",
        "lexical_swap",
        "synonym",
        "synonym_substitution",
        "substitution",
        "proverb_paraphrase",
    ],
    "intensity": [
        "intensity",
        "intensifier",
        "downtoner",
    ],
    "structure": [
        "structure",
        "syntax",
        "syntactic_reorder",
        "structure_reorder",
        "structure_framing",
    ],
    "syntax": [
        "syntax",
        "syntactic_reorder",
        "structure",
        "structure_reorder",
        "structure_framing",
    ],
    "syntactic_reorder": [
        "syntax",
        "syntactic_reorder",
        "structure",
        "structure_reorder",
        "structure_framing",
    ],
    "custom": [
        "custom",
    ],
}


def _is_category_match(ptype: str, allowed_types: Optional[Union[str, List[str]]]) -> bool:
    """Checks if a perturber subtype matches any user-requested display category."""
    if not allowed_types:
        return True
    if isinstance(allowed_types, str):
        allowed_types = [allowed_types]
    p = ptype.lower().strip()
    for cat in allowed_types:
        c = cat.lower().strip()
        if c == p or c in p or p in c:
            return True
        subtypes = DISPLAY_CATEGORY_TO_SUBTYPES.get(c, [])
        if p in subtypes or any(s in p for s in subtypes):
            return True
        p_subtypes = DISPLAY_CATEGORY_TO_SUBTYPES.get(p, [])
        if c in p_subtypes or any(s in c for s in p_subtypes):
            return True
        for fam_list in DISPLAY_CATEGORY_TO_SUBTYPES.values():
            if (p in fam_list) and (c in fam_list):
                return True
    return False


class SharedProbeGenerator:
    """
    Generates a deterministic SharedProbeSet across one or multiple seed texts.
    Ensures identical linguistic stimuli, stable identifiers, and calibrated diagnostic coverage.
    """
    def __init__(self, engine: Optional[PerturbationEngine] = None):
        self.engine = engine or PerturbationEngine()

    def generate_probes(
        self,
        seed_texts: List[str],
        perturbation_types: Optional[List[str]] = None,
        sentence_types: Optional[Dict[str, str]] = None,
        candidate_count: Optional[int] = 7,
    ) -> SharedProbeSet:
        """
        Generates controlled probes for all provided seed texts.
        If candidate_count is 7 (default), produces a calibrated diagnostic suite of exactly 7 probes per seed.
        Filters by perturbation_types if explicitly specified.
        """
        all_probes: List[LinguisticProbe] = []
        resolved_sentence_types: Dict[str, str] = {}

        for seed in seed_texts:
            clean_seed = seed.strip()
            if not clean_seed:
                continue

            # Determine sentence type: check explicit override, then known proverbs
            stype = (sentence_types or {}).get(clean_seed)
            if not stype:
                normalized_seed = re.sub(r"[^\w\s]", "", clean_seed.lower()).strip()
                if normalized_seed in KNOWN_PROVERBS:
                    stype = SentenceType.PROVERB.value
                else:
                    stype = SentenceType.LITERAL.value
            resolved_sentence_types[clean_seed] = stype

            if candidate_count == 7:
                seed_probes = self._generate_calibrated_7_probes(clean_seed, stype)
                if perturbation_types is not None:
                    seed_probes = [
                        p for p in seed_probes
                        if _is_category_match(p.perturbation_type, perturbation_types)
                    ]
            else:
                seed_probes = self._generate_all_probes(clean_seed, stype, perturbation_types)

            all_probes.extend(seed_probes)

        probe_set_id = f"pset_{uuid.uuid4().hex[:8]}"

        return SharedProbeSet(
            probe_set_id=probe_set_id,
            seed_texts=seed_texts,
            probes=all_probes,
            created_at=time.time(),
            probe_set_version=1,
            generator_version="2.3.0",
            sentence_types=resolved_sentence_types,
        )

    def _generate_calibrated_7_probes(
        self, clean_seed: str, sentence_type: str
    ) -> List[LinguisticProbe]:
        """
        Produces a calibrated diagnostic suite of exactly 7 probes per seed sentence per Section 11 & 37:
        P001: NEGATION (REVERSE_POLARITY -> EXPECTED_FLIP)
        P002: DOUBLE_NEGATION (PRESERVE_MEANING -> EXPECTED_PRESERVE)
        P003: INTENSIFICATION (STRENGTHEN_POLARITY -> EXPECTED_CONFIDENCE_INCREASE / SAME_LABEL)
        P004: DOWNTONING (WEAKEN_POLARITY -> EXPECTED_CONFIDENCE_DECREASE / SAME_LABEL)
        P005: PRESERVE_MEANING / PARAPHRASE (PRESERVE_MEANING -> EXPECTED_PRESERVE / SAME_LABEL)
        P006: CONTRAST / ADVERSATIVE (SHIFT_CONTRAST -> EXPECTED_FLIP)
        P007: CONTRAST_POSITIVE (STRENGTHEN_POLARITY -> EXPECTED_PRESERVE / SAME_LABEL)
        """
        variants = self.engine.generate_all(clean_seed)
        normalized_seed = re.sub(r"[^\w\s]", "", clean_seed.lower()).strip()
        is_proverb = (sentence_type == SentenceType.PROVERB.value) or (normalized_seed in KNOWN_PROVERBS)
        proverb_meta = KNOWN_PROVERBS.get(normalized_seed, {})

        candidates: List[LinguisticProbe] = []

        # 1. P001: Polarity-Reversing Negation
        p1_text = ""
        p1_desc = ""
        p1_cat = "negation"
        if is_proverb and proverb_meta.get("inversion_flip"):
            p1_text = proverb_meta["inversion_flip"]
            p1_desc = "Removed proverbial negation, reversing the core truth condition of the proverb."
            p1_cat = "negation_removal"
        else:
            neg_items = [v for v in variants if "negation" in v.get("type", "") and "double" not in v.get("type", "")]
            if neg_items:
                p1_text = neg_items[0].get("perturbed", "")
                p1_desc = neg_items[0].get("description", "Inserted/removed negation operator.")
                p1_cat = neg_items[0].get("type", "negation")
            else:
                p1_text = f"It is not true that {clean_seed[0].lower() + clean_seed[1:]}"
                p1_desc = "Prefixed sentence with explicit negation frame."
                p1_cat = "negation_prefix"

        candidates.append(
            LinguisticProbe.create(
                seed_text=clean_seed,
                perturbed_text=p1_text,
                perturbation_type=p1_cat,
                description=p1_desc,
                expected_semantic_effect="invert",
                expected_flip=True,
                name="P001: Negation / Polarity Inversion",
                semantic_intent=SemanticIntent.REVERSE_POLARITY.value,
                status=ProbeStatus.GENERATED.value,
                transformation=p1_desc,
                expected_label_relation=ExpectedLabelRelation.DIFFERENT_LABEL.value,
                expected_confidence_relation=ExpectedConfidenceRelation.UNCONSTRAINED.value,
                sentence_type=sentence_type,
                rationale="Linguistic negation reversing truth-conditional semantic polarity.",
                metadata={"slot": "P001", "diagnostic_class": "polarity_reversal"},
            )
        )

        # 2. P002: Double Negation / Syntactic Equivalence
        p2_items = [v for v in variants if "double_negation" in v.get("type", "")]
        if p2_items:
            p2_text = p2_items[0].get("perturbed", "")
            p2_desc = p2_items[0].get("description", "Inserted double negation preserving polarity.")
        else:
            p2_text = f"It is not untrue that {clean_seed[0].lower() + clean_seed[1:]}"
            p2_desc = "Inserted double negation frame preserving underlying polarity."

        candidates.append(
            LinguisticProbe.create(
                seed_text=clean_seed,
                perturbed_text=p2_text,
                perturbation_type="double_negation",
                description=p2_desc,
                expected_semantic_effect="preserve",
                expected_flip=False,
                name="P002: Double Negation / Polarity Preservation",
                semantic_intent=SemanticIntent.PRESERVE_MEANING.value,
                status=ProbeStatus.GENERATED.value,
                transformation=p2_desc,
                expected_label_relation=ExpectedLabelRelation.SAME_LABEL.value,
                expected_confidence_relation=ExpectedConfidenceRelation.PRESERVE.value,
                sentence_type=sentence_type,
                rationale="Syntactic double-negation cancellation preserving underlying truth conditions.",
                metadata={"slot": "P002", "diagnostic_class": "syntactic_preservation"},
            )
        )

        # 3. P003: Intensification (Strengthen Polarity)
        p3_items = [v for v in variants if v.get("subtype") == "intensifier" or (v.get("type") == "intensity" and v.get("expected_semantic_effect") == "strengthen")]
        if p3_items:
            p3_text = p3_items[0].get("perturbed", "")
            p3_desc = p3_items[0].get("description", "Injected degree intensifier adverb.")
        else:
            words = clean_seed.split()
            p3_text = f"{words[0]} extremely {' '.join(words[1:])}" if len(words) > 1 else f"Extremely {clean_seed}"
            p3_desc = "Injected intensifier adverb 'extremely'."

        candidates.append(
            LinguisticProbe.create(
                seed_text=clean_seed,
                perturbed_text=p3_text,
                perturbation_type="intensity",
                subtype="intensifier",
                description=p3_desc,
                expected_semantic_effect="strengthen",
                expected_flip=False,
                name="P003: Intensification / Degree Strengthening",
                semantic_intent=SemanticIntent.STRENGTHEN_POLARITY.value,
                status=ProbeStatus.GENERATED.value,
                transformation=p3_desc,
                expected_label_relation=ExpectedLabelRelation.SAME_LABEL.value,
                expected_confidence_relation=ExpectedConfidenceRelation.INCREASE.value,
                sentence_type=sentence_type,
                rationale="Degree adverb injection intended to intensify polarity without class shift.",
                metadata={"slot": "P003", "diagnostic_class": "polarity_strengthening"},
            )
        )

        # 4. P004: Downtoning (Weaken Polarity)
        p4_items = [v for v in variants if v.get("subtype") == "downtoner" or (v.get("type") == "intensity" and v.get("expected_semantic_effect") == "weaken")]
        if p4_items:
            p4_text = p4_items[0].get("perturbed", "")
            p4_desc = p4_items[0].get("description", "Injected degree downtoner adverb.")
        else:
            words = clean_seed.split()
            p4_text = f"{words[0]} somewhat {' '.join(words[1:])}" if len(words) > 1 else f"Somewhat {clean_seed}"
            p4_desc = "Injected downtoner adverb 'somewhat'."

        candidates.append(
            LinguisticProbe.create(
                seed_text=clean_seed,
                perturbed_text=p4_text,
                perturbation_type="intensity",
                subtype="downtoner",
                description=p4_desc,
                expected_semantic_effect="weaken",
                expected_flip=False,
                name="P004: Downtoning / Degree Attenuation",
                semantic_intent=SemanticIntent.WEAKEN_POLARITY.value,
                status=ProbeStatus.GENERATED.value,
                transformation=p4_desc,
                expected_label_relation=ExpectedLabelRelation.SAME_LABEL.value,
                expected_confidence_relation=ExpectedConfidenceRelation.DECREASE.value,
                sentence_type=sentence_type,
                rationale="Downtoning modifier attenuating degree while preserving polarity class.",
                metadata={"slot": "P004", "diagnostic_class": "polarity_weakening"},
            )
        )

        # 5. P005: Meaning-Preserving Paraphrase / Synonym Substitution
        p5_text = ""
        p5_desc = ""
        p5_cat = "synonym_substitution"
        if is_proverb and proverb_meta.get("paraphrase_preserve"):
            p5_text = proverb_meta["paraphrase_preserve"]
            p5_desc = "Meaning-preserving proverbial paraphrase grounded in core wisdom."
            p5_cat = "proverb_paraphrase"
        else:
            syn_items = [v for v in variants if "synonym" in v.get("type", "")]
            if syn_items:
                p5_text = syn_items[0].get("perturbed", "")
                p5_desc = syn_items[0].get("description", "Substituted word with meaning-preserving synonym.")
            else:
                p5_text = clean_seed.replace("good", "great") if "good" in clean_seed else f"Certainly, {clean_seed[0].lower() + clean_seed[1:]}"
                p5_desc = "Substituted equivalent lexical modifier."

        candidates.append(
            LinguisticProbe.create(
                seed_text=clean_seed,
                perturbed_text=p5_text,
                perturbation_type=p5_cat,
                description=p5_desc,
                expected_semantic_effect="preserve",
                expected_flip=False,
                name="P005: Meaning Preservation / Paraphrase",
                semantic_intent=SemanticIntent.PRESERVE_MEANING.value,
                status=ProbeStatus.GENERATED.value,
                transformation=p5_desc,
                expected_label_relation=ExpectedLabelRelation.SAME_LABEL.value,
                expected_confidence_relation=ExpectedConfidenceRelation.PRESERVE.value,
                sentence_type=sentence_type,
                rationale="Semantic-preserving variation testing against spurious sensitivity.",
                metadata={
                    "slot": "P005",
                    "diagnostic_class": "semantic_preservation",
                    "semantic_interpretation": proverb_meta.get("semantic_interpretation", ""),
                },
            )
        )

        # 6. P006: Contrastive Connective (Adversative Clause Shift)
        p6_items = [v for v in variants if "contrast_negative" in v.get("type", "") or "concession" in v.get("type", "")]
        if p6_items:
            p6_text = p6_items[0].get("perturbed", "")
            p6_desc = p6_items[0].get("description", "Appended adversative contrast clause.")
            p6_cat = p6_items[0].get("type", "contrast")
        else:
            base_sent = clean_seed.rstrip(".!?")
            p6_text = f"{base_sent}, however it did not improve over time."
            p6_desc = "Appended adversative contrast clause shifting dominant discourse relation."
            p6_cat = "contrast_negative_append"

        candidates.append(
            LinguisticProbe.create(
                seed_text=clean_seed,
                perturbed_text=p6_text,
                perturbation_type=p6_cat,
                description=p6_desc,
                expected_semantic_effect="invert",
                expected_flip=True,
                name="P006: Contrastive Connective / Adversative Shift",
                semantic_intent=SemanticIntent.SHIFT_CONTRAST.value,
                status=ProbeStatus.GENERATED.value,
                transformation=p6_desc,
                expected_label_relation=ExpectedLabelRelation.DIFFERENT_LABEL.value,
                expected_confidence_relation=ExpectedConfidenceRelation.UNCONSTRAINED.value,
                sentence_type=sentence_type,
                rationale="Adversative contrast clause whose discourse relation alters overall evaluation.",
                metadata={"slot": "P006", "diagnostic_class": "contrast_shift"},
            )
        )

        # 7. P007: Contrast Positive (Reinforcing Contrastive Clause)
        p7_items = [v for v in variants if "contrast_positive" in v.get("type", "")]
        if p7_items:
            p7_text = p7_items[0].get("perturbed", "")
            p7_desc = p7_items[0].get("description", "Appended context-aware positive contrast clause.")
            p7_cat = p7_items[0].get("type", "contrast_positive_append")
        else:
            base_sent = clean_seed.rstrip(".!?")
            p7_text = f"{base_sent}, and it demonstrated remarkable quality."
            p7_desc = "Appended reinforcing positive contrast clause."
            p7_cat = "contrast_positive_append"

        candidates.append(
            LinguisticProbe.create(
                seed_text=clean_seed,
                perturbed_text=p7_text,
                perturbation_type=p7_cat,
                description=p7_desc,
                expected_semantic_effect="preserve",
                expected_flip=False,
                name="P007: Contrast Positive / Reinforcing Clause",
                semantic_intent=SemanticIntent.PRESERVE_MEANING.value,
                status=ProbeStatus.GENERATED.value,
                transformation=p7_desc,
                expected_label_relation=ExpectedLabelRelation.SAME_LABEL.value,
                expected_confidence_relation=ExpectedConfidenceRelation.PRESERVE.value,
                sentence_type=sentence_type,
                rationale="Positive contrast clause reinforcing the evaluation and preserving sentiment polarity.",
                metadata={"slot": "P007", "diagnostic_class": "contrast_positive"},
            )
        )

        return candidates

    def _generate_all_probes(
        self,
        clean_seed: str,
        sentence_type: str,
        perturbation_types: Optional[List[str]] = None,
    ) -> List[LinguisticProbe]:
        """Generates all raw candidate variants from perturber engine without cap."""
        variants = self.engine.generate_all(clean_seed)
        seed_probes: List[LinguisticProbe] = []

        for item in variants:
            ptype = item.get("type", "unknown")
            if perturbation_types and not _is_category_match(ptype, perturbation_types):
                continue

            perturbed_text = item.get("perturbed", "")
            desc = item.get("description", "")
            raw_expected_flip = item.get("expected_flip")
            subtype = item.get("subtype")

            effect, expected_flip = infer_expected_semantic_effect(
                perturbation_type=ptype,
                subtype=subtype,
                description=desc,
            )

            if raw_expected_flip is not None:
                expected_flip = bool(raw_expected_flip)

            raw_intent = item.get("semantic_intent")
            if raw_intent:
                intent_str = raw_intent if isinstance(raw_intent, str) else raw_intent.value
            else:
                intent_str = infer_semantic_intent(ptype, subtype, desc).value

            probe = LinguisticProbe.create(
                seed_text=clean_seed,
                perturbed_text=perturbed_text,
                perturbation_type=ptype,
                description=desc,
                expected_semantic_effect=effect,
                expected_flip=expected_flip,
                subtype=subtype,
                category=ptype,
                name=f"{ptype}_{subtype or 'general'}",
                semantic_intent=intent_str,
                status=ProbeStatus.GENERATED.value,
                transformation=desc,
                sentence_type=sentence_type,
                rationale=desc or "Linguistic variation generated by rule.",
                metadata={
                    "rule": item.get("rule", ""),
                    "token_index": item.get("token_index"),
                    "original_token": item.get("original_token"),
                    "replacement_token": item.get("replacement_token"),
                },
            )
            seed_probes.append(probe)

        return seed_probes
