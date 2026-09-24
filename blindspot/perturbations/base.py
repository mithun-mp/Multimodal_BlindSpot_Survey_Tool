from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BasePerturber(ABC):
    """
    Abstract base class for all controlled linguistic perturbers.
    """
    def __init__(self, name: str, perturbation_type: str):
        self.name = name
        self.perturbation_type = perturbation_type

    @abstractmethod
    def perturb(self, sentence: str) -> List[Dict[str, Any]]:
        """
        Generates perturbed variants of input sentence.
        Returns a list of dicts with keys:
        - original: str
        - perturbed: str
        - type: str
        - description: str
        """
        pass
