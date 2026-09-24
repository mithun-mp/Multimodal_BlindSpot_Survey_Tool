from typing import List, Dict, Any, Optional
from .negation import NegationPerturber, DoubleNegationPerturber
from .connectives import ConnectivePerturber
from .substitution import SynonymSubstitutionPerturber
from .intensity import IntensityPerturber
from .structure import StructurePerturber

class PerturbationEngine:
    """
    Unified engine to run all controlled linguistic perturbations on input text.
    """
    SUPPORTED_CATEGORIES = [
        "negation",
        "double_negation",
        "connective",
        "synonym_substitution",
        "intensity",
        "structure",
        "contrast_positive",
    ]

    def __init__(self, categories: Optional[List[str]] = None):
        all_perturbers = [
            NegationPerturber(),
            DoubleNegationPerturber(),
            ConnectivePerturber(),
            SynonymSubstitutionPerturber(),
            IntensityPerturber(),
            StructurePerturber(),
        ]
        if categories:
            allowed = set(categories)
            if "contrast_positive" in allowed:
                allowed.add("connective")
            self.perturbers = [p for p in all_perturbers if p.perturbation_type in allowed]
        else:
            self.perturbers = all_perturbers

    def generate_all(self, sentence: str) -> List[Dict[str, Any]]:
        all_variants = []
        for perturber in self.perturbers:
            variants = perturber.perturb(sentence)
            all_variants.extend(variants)
        return all_variants

