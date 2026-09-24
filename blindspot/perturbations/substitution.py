import re
from typing import List, Dict, Any
from .base import BasePerturber

def _clean_text(text: str) -> str:
    """Helper to clean whitespace and space before punctuation."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.\!?])", r"\1", text)
    return text

class SynonymSubstitutionPerturber(BasePerturber):
    """
    Generates controlled word substitution perturbations using WordNet or rule tables,
    strictly targeting content words (adjectives, nouns, sentiment words) while ignoring pronouns/stopwords.
    """
    def __init__(self):
        super().__init__(name="Synonym Substitution Engine", perturbation_type="substitution")
        self.stop_words = {
            "i", "me", "my", "myself", "we", "our", "you", "your", "he", "him", "his",
            "she", "her", "it", "its", "they", "them", "their", "this", "that", "these",
            "those", "am", "is", "are", "was", "were", "be", "been", "being", "have",
            "has", "had", "do", "does", "did", "a", "an", "the", "and", "but", "if",
            "or", "because", "as", "until", "while", "of", "at", "by", "for", "with",
            "about", "against", "between", "into", "through", "during", "before",
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on",
            "off", "over", "under", "again", "further", "then", "once"
        }
        # Curated dictionary for key sentiment and content domain terms
        self.synonym_map = {
            "awesome": ["impressive", "brilliant", "outstanding", "fantastic"],
            "great": ["fantastic", "excellent", "wonderful"],
            "good": ["decent", "fine", "respectable"],
            "fun": ["a great time", "delight"],
            "bad": ["poor", "subpar", "unfortunate"],
            "terrible": ["horrible", "awful", "dreadful"],
            "movie": ["film", "picture", "flick"],
            "book": ["novel", "work", "volume"],
            "food": ["meal", "cuisine", "dish"],
            "service": ["staff", "support", "assistance"],
            "festival": ["event", "celebration", "gala"],
            "product": ["item", "offering", "good"],
            "performance": ["show", "act", "presentation"],
        }

    def _match_case(self, original: str, replacement: str) -> str:
        """Matches original word capitalization on the replacement string."""
        if original.isupper():
            return replacement.upper()
        elif original and original[0].isupper():
            return replacement.capitalize()
        return replacement.lower()

    def _get_nltk_synonyms(self, word: str) -> List[str]:
        try:
            from nltk.corpus import wordnet
            synonyms = set()
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    syn_name = lemma.name().replace("_", " ")
                    # Filter out obscure, multi-word, non-alphabetic, or tiny lemmas
                    if (
                        syn_name.lower() != word.lower()
                        and syn_name.isalpha()
                        and len(syn_name) >= 3
                        and syn_name.lower() not in self.stop_words
                    ):
                        synonyms.add(syn_name)
            return list(synonyms)
        except Exception:
            return []

    def perturb(self, sentence: str) -> List[Dict[str, Any]]:
        results = []
        clean_sentence = _clean_text(sentence)
        words = clean_sentence.split()

        # Step 1: High-priority check using curated synonym map
        for idx, word in enumerate(words):
            clean_word = re.sub(r"[^\w]", "", word).lower()
            if clean_word in self.synonym_map:
                chosen_syn = self.synonym_map[clean_word][0]
                matched_syn = self._match_case(word.rstrip(",.!?"), chosen_syn)
                
                punct = word[len(re.sub(r"[^\w]", "", word)):] if len(word) > len(re.sub(r"[^\w]", "", word)) else ""
                new_words = list(words)
                new_words[idx] = matched_syn + punct

                perturbed = " ".join(new_words)
                results.append({
                    "original": sentence,
                    "perturbed": _clean_text(perturbed),
                    "type": "synonym_substitution",
                    "description": f"Substituted '{word}' with synonym '{matched_syn}'."
                })
                return results

        # Step 2: Fallback using NLTK WordNet on non-stopword content tokens
        for idx, word in enumerate(words):
            clean_word = re.sub(r"[^\w]", "", word).lower()
            if clean_word in self.stop_words or len(clean_word) < 3:
                continue

            synonyms = self._get_nltk_synonyms(clean_word)
            if synonyms:
                chosen_syn = synonyms[0]
                matched_syn = self._match_case(word.rstrip(",.!?"), chosen_syn)
                
                punct = word[len(re.sub(r"[^\w]", "", word)):] if len(word) > len(re.sub(r"[^\w]", "", word)) else ""
                new_words = list(words)
                new_words[idx] = matched_syn + punct

                perturbed = " ".join(new_words)
                results.append({
                    "original": sentence,
                    "perturbed": _clean_text(perturbed),
                    "type": "synonym_substitution",
                    "description": f"Substituted word '{word}' with synonym '{matched_syn}'."
                })
                break

        return results

