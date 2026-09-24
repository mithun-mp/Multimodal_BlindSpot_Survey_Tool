import numpy as np
from typing import Dict, List, Any

def compute_jaccard_similarity(exp1: Dict[str, float], exp2: Dict[str, float], top_k: int = 5) -> float:
    """
    Computes Jaccard similarity of top K tokens by absolute attribution score.
    """
    sorted1 = sorted(exp1.items(), key=lambda x: abs(x[1]), reverse=True)[:top_k]
    sorted2 = sorted(exp2.items(), key=lambda x: abs(x[1]), reverse=True)[:top_k]

    set1 = set(k.lower() for k, _ in sorted1)
    set2 = set(k.lower() for k, _ in sorted2)

    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0

    intersection = set1.intersection(set2)
    union = set1.union(set2)

    return float(len(intersection) / len(union))

def compute_attribution_cosine(exp1: Dict[str, float], exp2: Dict[str, float]) -> float:
    """
    Computes Cosine Similarity between attribution vectors across common vocabulary.
    """
    common_words = set(exp1.keys()).union(set(exp2.keys()))
    if not common_words:
        return 1.0

    v1 = np.array([exp1.get(w, 0.0) for w in common_words])
    v2 = np.array([exp2.get(w, 0.0) for w in common_words])

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return float(np.dot(v1, v2) / (norm1 * norm2))
