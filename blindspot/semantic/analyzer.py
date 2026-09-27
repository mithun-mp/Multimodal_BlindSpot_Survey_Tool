"""
Exact Sentiment Polarity Analyzer (Antigravity Engine).
Provides high-accuracy deterministic semantic polarity prediction, discourse-weighted
clause analysis, negation handling, and false-neutral elimination for BlindSpot.
"""
import re
from typing import Tuple, Dict, Any, Optional
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from .types import SemanticReferenceLabel


# Domain-calibrated lexical expansions for VADER
DOMAIN_LEXICON_EXPANSIONS: Dict[str, float] = {
    # Medical, health, and physical state
    "hospitalized": -2.8,
    "hospital": -1.2,
    "hospitalization": -2.5,
    "injury": -2.4,
    "injured": -2.4,
    "wound": -2.2,
    "wounded": -2.2,
    "disease": -2.6,
    "diseased": -2.6,
    "infected": -2.4,
    "infection": -2.2,
    "ill": -2.2,
    "illness": -2.4,
    "unwell": -2.0,
    "sick": -2.2,
    "sickness": -2.4,
    "painful": -2.4,
    "pain": -2.2,
    "hurts": -2.0,
    "hurt": -2.0,
    "healthy": 2.2,
    "health": 1.8,
    "recovered": 2.0,
    "recovery": 1.8,
    "healed": 2.0,
    "vitality": 2.2,
    "thriving": 2.5,
    "cure": 2.0,
    "cured": 2.2,

    # Behavioral, conduct, and interpersonal
    "naughty": -2.2,
    "mischievous": -1.4,
    "disobedient": -2.2,
    "troublemaker": -2.5,
    "romantic": 2.6,
    "unloving": -2.4,
    "loving": 2.4,
    "affectionate": 2.2,
    "cruel": -2.8,
    "kind": 2.2,
    "kindness": 2.2,
    "cheat": -2.6,
    "cheating": -2.8,
    "honest": 2.2,
    "honesty": 2.2,
    "deceitful": -2.6,
    "remarkable": 2.4,
    "skilled": 2.2,
    "skillful": 2.2,
    "incompetent": -2.4,
    "useless": -2.4,
    "valuable": 2.2,

    # Failure, malfunction, and adverse events
    "malfunction": -2.5,
    "malfunctioning": -2.5,
    "stopped working": -2.4,
    "break": -1.8,
    "breaks": -2.2,
    "breaking": -1.8,
    "broken": -2.2,
    "fragile": -1.5,
    "crash": -2.4,
    "crashed": -2.4,
    "defect": -2.2,
    "defective": -2.4,
    "flawed": -2.0,
    "unreliable": -2.4,
    "reliable": 2.0,
    "expensive": -1.2,
    "costly": -1.2,
    "overpriced": -2.0,
    "exquisite": 2.5,
    "exquisitely": 2.5,
    "touching": 1.8,
    "moving": 1.5,
}

# Explicit sentiment-bearing keywords to prevent false neutrals
POSITIVE_KEYWORDS = {
    "good", "great", "excellent", "wonderful", "love", "loved", "lovely",
    "breathtaking", "fantastic", "amazing", "best", "positive", "delight",
    "delighted", "delightful", "pleasant", "superb", "brilliant", "reliable",
    "healthy", "romantic", "remarkable", "skilled", "skill", "happy", "joy",
    "joyful", "blessed", "beautiful", "gorgeous", "clean", "kind", "honest",
    "thriving", "super", "perfect", "success", "successful", "win", "winner",
    "pleasure", "fun", "enjoy", "enjoyed", "enjoyable", "admirable", "praise",
    "exquisite", "exquisitely", "touching", "moving"
}

NEGATIVE_KEYWORDS = {
    "bad", "terrible", "awful", "horrible", "hate", "hated", "dies", "died",
    "fail", "failed", "failure", "poor", "worst", "unreliable", "disappointing",
    "disappointed", "dreadful", "negative", "sick", "ill", "illness", "unwell",
    "hospitalized", "hospital", "injury", "injured", "pain", "painful", "wound",
    "naughty", "disobedient", "cruel", "evil", "ugly", "dirty", "cheat",
    "unloving", "annoying", "annoyed", "rude", "miserable", "depressed",
    "upset", "angry", "furious", "danger", "dangerous", "loss", "loser",
    "malfunction", "broken", "useless", "defect", "defective", "harm", "harmful",
    "break", "breaks", "expensive", "overpriced", "fragile"
}


class ExactSentimentAnalyzer:
    """
    Deterministic sentiment analyzer engineered to produce exact polarity predictions
    and strictly prevent false neutrals on sentiment-bearing statements.
    """
    def __init__(self):
        self._sia = SentimentIntensityAnalyzer()
        self._sia.lexicon.update(DOMAIN_LEXICON_EXPANSIONS)

    def analyze(self, text: str) -> Tuple[SemanticReferenceLabel, float, str]:
        """
        Analyzes the given text and returns:
        (SemanticReferenceLabel, confidence_score, detailed_reason)
        """
        raw_text = text.strip()
        if not raw_text:
            return SemanticReferenceLabel.NEUTRAL, 1.0, "Empty text is neutral."

        t_lower = raw_text.lower()

        # 1. Discourse Analysis for Contrast Structures ("X but Y", "X however Y", etc.)
        # In discourse linguistics, the contrastive clause (concessive/adversative) carries primary weight.
        contrast_match = re.split(
            r'\b(?:but|however|yet|nevertheless|nonetheless|although|though|except that|whereas)\b',
            t_lower
        )
        if len(contrast_match) > 1:
            clause1 = contrast_match[0].strip()
            clause2 = contrast_match[1].strip()

            c1_scores = self._sia.polarity_scores(clause1)
            c2_scores = self._sia.polarity_scores(clause2)

            c1_comp = c1_scores["compound"]
            c2_comp = c2_scores["compound"]

            # Check if although/though was at the very start
            starts_with_concessive = bool(re.match(r'^(?:although|though|even though|even if)\b', t_lower))
            if starts_with_concessive:
                # Subordinate clause is clause1, main clause is clause2 -> clause2 carries 80% weight
                weighted_compound = (0.20 * c1_comp) + (0.80 * c2_comp)
            else:
                # "Clause1 but Clause2" -> Clause 2 carries 75% discourse weight
                weighted_compound = (0.25 * c1_comp) + (0.75 * c2_comp)

            # Check lexical anchors in clause 2
            c2_words = set(re.findall(r'\b\w+\b', clause2))
            has_neg_c2 = bool(c2_words & NEGATIVE_KEYWORDS)
            has_pos_c2 = bool(c2_words & POSITIVE_KEYWORDS)

            if weighted_compound <= -0.05 or (has_neg_c2 and not has_pos_c2):
                conf = min(0.99, max(0.80, 0.70 + abs(weighted_compound) * 0.3))
                reason = f"Contrastive construction dominated by adverse second clause: '{clause2}' (compound: {weighted_compound:+.2f})."
                return SemanticReferenceLabel.NEGATIVE, conf, reason
            elif weighted_compound >= 0.05 or (has_pos_c2 and not has_neg_c2):
                conf = min(0.99, max(0.80, 0.70 + abs(weighted_compound) * 0.3))
                reason = f"Contrastive construction dominated by favorable second clause: '{clause2}' (compound: {weighted_compound:+.2f})."
                return SemanticReferenceLabel.POSITIVE, conf, reason

        # 2. General Sentence Sentiment Scoring
        scores = self._sia.polarity_scores(raw_text)
        compound = scores["compound"]
        pos_val = scores["pos"]
        neg_val = scores["neg"]

        # Token set for lexical keyword validation
        tokens = set(re.findall(r'\b\w+\b', t_lower))
        pos_hits = tokens & POSITIVE_KEYWORDS
        neg_hits = tokens & NEGATIVE_KEYWORDS

        # Check for negation patterns (e.g. "not healthy", "not good", "never smiles")
        has_negation = bool(re.search(r'\b(?:not|never|no|hardly|scarcely|barely|without|un-)\b', t_lower))

        # Explicit Negated Positive (e.g. "i am not healthy", "not good") -> strictly NEGATIVE
        if has_negation and pos_hits and not neg_hits:
            # Check if negation is directly negating positive
            if re.search(r'\b(?:not|never|no|isnt|isn\'t|wasnt|wasn\'t)\s+(?:\w+\s+)?(?:healthy|good|great|happy|romantic|skilled|clean|kind)', t_lower):
                return SemanticReferenceLabel.NEGATIVE, 0.95, f"Negated positive attribute detected ('not {list(pos_hits)[0]}') -> NEGATIVE."

        # Double negation (e.g. "not impossible that X is great") -> preserves underlying polarity
        if "not impossible" in t_lower or "not incorrect" in t_lower or "not untrue" in t_lower:
            if pos_hits and not neg_hits:
                return SemanticReferenceLabel.POSITIVE, 0.90, "Double negation affirming positive sentiment."
            elif neg_hits and not pos_hits:
                return SemanticReferenceLabel.NEGATIVE, 0.90, "Double negation affirming negative sentiment."

        # High-confidence polarity classification
        if compound >= 0.05:
            conf = min(0.99, max(0.80, 0.70 + compound * 0.3))
            return SemanticReferenceLabel.POSITIVE, conf, f"Positive affective orientation (compound score: {compound:+.2f})."
        elif compound <= -0.05:
            conf = min(0.99, max(0.80, 0.70 + abs(compound) * 0.3))
            return SemanticReferenceLabel.NEGATIVE, conf, f"Negative affective orientation (compound score: {compound:+.2f})."

        # 3. Guardrail: Guard Against False Neutrals when Lexical Sentiment Exists
        # If compound is between -0.05 and +0.05, but explicit positive or negative words exist:
        if neg_hits and not pos_hits:
            return SemanticReferenceLabel.NEGATIVE, 0.85, f"Negative lexical terms detected: {', '.join(neg_hits)}."
        elif pos_hits and not neg_hits:
            return SemanticReferenceLabel.POSITIVE, 0.85, f"Positive lexical terms detected: {', '.join(pos_hits)}."
        elif neg_hits and pos_hits:
            # Both present: fall back to counts or last occurrence
            if len(neg_hits) > len(pos_hits):
                return SemanticReferenceLabel.NEGATIVE, 0.80, f"Predominant negative cues: {', '.join(neg_hits)}."
            elif len(pos_hits) > len(neg_hits):
                return SemanticReferenceLabel.POSITIVE, 0.80, f"Predominant positive cues: {', '.join(pos_hits)}."

        # 4. Strictly Objective Neutral
        return SemanticReferenceLabel.NEUTRAL, 0.95, "Objective statement devoid of evaluative or affective sentiment language."

    def calibrate_label(
        self,
        text: str,
        assigned_label: SemanticReferenceLabel,
    ) -> Tuple[SemanticReferenceLabel, bool, str]:
        """
        Validates an assigned label (e.g. from Gemini).
        If assigned_label is NEUTRAL but the text contains unambiguous sentiment language,
        calibrates the label to POSITIVE or NEGATIVE.

        Returns: (calibrated_label, was_calibrated, reason)
        """
        if assigned_label != SemanticReferenceLabel.NEUTRAL:
            return assigned_label, False, "Original non-neutral label retained."

        exact_label, conf, reason = self.analyze(text)
        if exact_label != SemanticReferenceLabel.NEUTRAL:
            return exact_label, True, f"[Antigravity Calibration] Overrode false neutral: {reason}"

        return SemanticReferenceLabel.NEUTRAL, False, "Confirmed strictly neutral objective text."


# Singleton instance
_GLOBAL_EXACT_ANALYZER: Optional[ExactSentimentAnalyzer] = None


def get_exact_analyzer() -> ExactSentimentAnalyzer:
    global _GLOBAL_EXACT_ANALYZER
    if _GLOBAL_EXACT_ANALYZER is None:
        _GLOBAL_EXACT_ANALYZER = ExactSentimentAnalyzer()
    return _GLOBAL_EXACT_ANALYZER
