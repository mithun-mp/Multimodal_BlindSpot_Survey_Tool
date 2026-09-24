import re
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

def _clean_text(text: str) -> str:
    """Helper to clean whitespace and spacing before punctuation."""
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.\!?])", r"\1", text)
    return text

@dataclass
class SentenceFeatures:
    """
    Structured linguistic properties extracted from a sentence using spaCy and NLTK.
    """
    original_text: str
    tokens: List[str]
    pos_tags: List[Tuple[str, str]]
    subject: str
    pronoun: str
    possessive_pronoun: str
    is_plural: bool
    is_past_tense: bool
    copula: str
    negative_copula: str
    aux_do: str
    aux_do_not: str
    root_lemma: str
    direct_object: Optional[str]
    is_human_agent: bool
    is_human_object: bool
    entity_domain: str
    descriptor: Optional[str]
    descriptor_pos: Optional[str]
    descriptor_lemma: Optional[str]
    is_negative_sentiment: bool
    antonyms: List[str] = field(default_factory=list)
    noun_chunks: List[str] = field(default_factory=list)

class LinguisticAnalyzer:
    """
    Performs syntactic deconstruction and feature extraction using spaCy and NLTK:
    - spaCy Dependency Parsing & Morphology (subject, verb, root, direct object, tense, plurality)
    - Semantic Category & Animacy Typing (Human/Animate, Technology, Weather, Food, Service)
    - NLTK WordNet Lexical Opposites (direct antonyms & satellite synsets)
    - NLTK SentiWordNet Sentiment Polarity Ranking
    """

    NEGATIVE_KEYWORDS = {
        "bad", "poor", "slow", "slowly", "expensive", "ugly", "terrible",
        "horrible", "awful", "subpar", "difficult", "hard", "dirty",
        "broken", "defective", "flawed", "buggy", "noisy", "loud", "heavy"
    }

    HUMAN_PRONOUNS = {
        "i", "me", "we", "us", "you", "he", "him", "she", "her",
        "they", "them", "who", "whom", "someone", "anyone", "everyone",
        "person", "man", "woman", "boy", "girl", "child", "people"
    }

    _RESOURCES_CHECKED = False
    _NLP = None
    _PERSON_SYNSET = None

    def __init__(self):
        self._ensure_resources()
        if LinguisticAnalyzer._NLP is None:
            self._init_spacy()
        if LinguisticAnalyzer._PERSON_SYNSET is None:
            from nltk.corpus import wordnet as wn
            try:
                LinguisticAnalyzer._PERSON_SYNSET = wn.synset("person.n.01")
            except Exception:
                pass

    @classmethod
    def _ensure_resources(cls):
        """Ensures required NLTK tokenizers, taggers, and corpora are available."""
        if cls._RESOURCES_CHECKED:
            return
        import nltk
        resources = [
            ("tokenizers/punkt_tab", "punkt_tab"),
            ("taggers/averaged_perceptron_tagger_eng", "averaged_perceptron_tagger_eng"),
            ("corpora/wordnet", "wordnet"),
            ("corpora/sentiwordnet", "sentiwordnet"),
            ("sentiment/vader_lexicon", "vader_lexicon"),
        ]
        for res_path, pkg_name in resources:
            try:
                nltk.data.find(res_path)
            except (LookupError, OSError):
                try:
                    nltk.download(pkg_name, quiet=True)
                except Exception:
                    pass
        cls._RESOURCES_CHECKED = True

    @classmethod
    def _init_spacy(cls):
        """Initializes the spaCy language pipeline."""
        try:
            import spacy
            try:
                cls._NLP = spacy.load("en_core_web_sm")
            except Exception:
                try:
                    import spacy.cli
                    spacy.cli.download("en_core_web_sm")
                    cls._NLP = spacy.load("en_core_web_sm")
                except Exception:
                    cls._NLP = None
        except Exception:
            cls._NLP = None

    def is_human_entity(self, token_text: str, ent_type: str = "") -> bool:
        """Determines if a token represents an animate/human entity using pronouns, NER, and WordNet hypernyms."""
        if not token_text:
            return False
        w_low = token_text.lower()
        if w_low in self.HUMAN_PRONOUNS:
            return True
        if ent_type in ("PERSON", "NORP"):
            return True
        from nltk.corpus import wordnet as wn
        try:
            syns = wn.synsets(w_low, pos=wn.NOUN)
            if self._PERSON_SYNSET:
                for syn in syns[:2]:
                    for path in syn.hypernym_paths():
                        if self._PERSON_SYNSET in path:
                            return True
        except Exception:
            pass
        return False

    def detect_entity_domain(self, text: str, is_human: bool) -> str:
        """Categorizes the semantic domain of the input sentence."""
        if is_human:
            return "human"
        t_low = text.lower()
        weather_words = {"hot", "cold", "rain", "raining", "sunny", "weather", "storm", "wind", "snow", "outside", "summer", "winter"}
        tech_words = {"battery", "algorithm", "algorithms", "laptop", "laptops", "software", "hardware", "code", "program", "system", "device", "phone"}
        food_words = {"food", "meal", "dish", "dinner", "lunch", "breakfast", "delicious", "tasty", "restaurant", "coffee", "soup"}
        service_words = {"service", "staff", "support", "waiter", "waitress", "assistance", "agent"}
        media_words = {"movie", "film", "acting", "actor", "music", "book", "novel", "show", "game"}

        words = set(re.findall(r"\b\w+\b", t_low))
        if words & weather_words:
            return "weather"
        if words & food_words:
            return "food"
        if words & media_words:
            return "media"
        if words & service_words:
            return "service"
        if words & tech_words:
            return "tech"
        return "general"

    def is_negative_word(self, word: str, pos_tag: str = "ADJ") -> bool:
        """Determines if a word carries negative sentiment using SentiWordNet and keyword lookup."""
        if not word:
            return False
        w = word.lower()
        if w in self.NEGATIVE_KEYWORDS:
            return True
        from nltk.corpus import wordnet as wn
        from nltk.corpus import sentiwordnet as swn
        wn_pos = wn.ADJ if pos_tag in ("ADJ", "JJ") else (wn.ADV if pos_tag in ("ADV", "RB") else None)
        syns = wn.synsets(w, pos=wn_pos)
        if syns:
            try:
                swn_syn = swn.senti_synset(syns[0].name())
                return swn_syn.neg_score() > swn_syn.pos_score()
            except Exception:
                pass
        return False

    def get_word_sentiment(self, word: str, pos_tag: str = "ADJ") -> float:
        """Computes net sentiment score using NLTK SentiWordNet."""
        from nltk.corpus import wordnet as wn
        from nltk.corpus import sentiwordnet as swn
        
        wn_pos = wn.ADJ if pos_tag in ("ADJ", "JJ") else (wn.ADV if pos_tag in ("ADV", "RB") else None)
        syns = wn.synsets(word, pos=wn_pos)
        if not syns:
            return 0.0
        
        pos_score = 0.0
        neg_score = 0.0
        count = 0
        for syn in syns[:3]:
            try:
                swn_syn = swn.senti_synset(syn.name())
                pos_score += swn_syn.pos_score()
                neg_score += swn_syn.neg_score()
                count += 1
            except Exception:
                pass
        return (pos_score - neg_score) / count if count else 0.0

    def get_ranked_opposites(self, word: str, pos_tag: str = "ADJ") -> List[str]:
        """
        Retrieves antonyms from NLTK WordNet and ranks them using SentiWordNet
        polarity inversion to select the most natural opposite.
        """
        from nltk.corpus import wordnet as wn
        wn_pos = wn.ADJ if pos_tag in ("ADJ", "JJ") else (wn.ADV if pos_tag in ("ADV", "RB") else None)
        if not wn_pos or not word:
            return []

        candidates = []
        w_low = word.lower()

        for syn in wn.synsets(w_low, pos=wn_pos):
            # 1. Priority 1: Direct lemma antonyms
            for lemma in syn.lemmas():
                for ant in lemma.antonyms():
                    name = ant.name().replace("_", " ").lower()
                    if name != w_low and name not in [c[0] for c in candidates]:
                        candidates.append((name, 1.0))

            # 2. Priority 2: Satellite synset antonyms (similar_to)
            for sim in syn.similar_tos():
                for lemma in sim.lemmas():
                    for ant in lemma.antonyms():
                        name = ant.name().replace("_", " ").lower()
                        if name != w_low and name not in [c[0] for c in candidates]:
                            candidates.append((name, 0.5))

        orig_negative = self.is_negative_word(w_low, pos_tag)

        # Sort candidate opposites by polarity inversion and priority
        def sort_key(item):
            c_name, prio = item
            c_sent = self.get_word_sentiment(c_name, pos_tag)
            # If original is positive/neutral, lower c_sent (more negative) is preferred.
            # If original is negative, higher c_sent (more positive) is preferred.
            sentiment_diff = c_sent if orig_negative else -c_sent
            return (prio, sentiment_diff)

        candidates.sort(key=sort_key, reverse=True)
        return [c[0] for c in candidates]

    def extract_features(self, sentence: str) -> SentenceFeatures:
        """
        Extracts syntactic, grammatical, and animacy properties from the input sentence
        using spaCy dependency parsing and NLTK lexical semantics.
        """
        clean_s = _clean_text(sentence)

        if self._NLP is not None:
            doc = self._NLP(clean_s)
            tokens = [t.text for t in doc]
            pos_tags = [(t.text, t.tag_) for t in doc]
            noun_chunks = [nc.text for nc in doc.noun_chunks]

            # 1. Subject extraction via dependency parse
            subj_tokens = [t for t in doc if "subj" in t.dep_]
            subj_token = subj_tokens[0] if subj_tokens else None
            
            # Direct object extraction (transitivity)
            dobj_tokens = [t for t in doc if t.dep_ in ("dobj", "obj")]
            dobj_token = dobj_tokens[0] if dobj_tokens else None
            direct_object_text = " ".join(t.text for t in dobj_token.subtree) if dobj_token else None

            # Animacy checking
            is_human_agent = self.is_human_entity(subj_token.text, subj_token.ent_type_) if subj_token else False
            is_human_object = self.is_human_entity(dobj_token.text, dobj_token.ent_type_) if dobj_token else False
            entity_domain = self.detect_entity_domain(clean_s, is_human_agent)

            # Root verb
            root_tokens = [t for t in doc if t.dep_ == "ROOT"]
            root = root_tokens[0] if root_tokens else doc[0]
            root_lemma = root.lemma_.lower()

            # 2. Pronoun & plurality resolution
            is_plural = False
            pronoun = "it"
            possessive_pronoun = "its"

            if subj_token:
                w_low = subj_token.text.lower()
                if w_low in ("i", "me"):
                    pronoun = "I"
                    possessive_pronoun = "my"
                elif w_low in ("they", "them") or subj_token.tag_ in ("NNS", "NNPS"):
                    is_plural = True
                    pronoun = "they"
                    possessive_pronoun = "their"
                elif w_low in ("we", "us"):
                    is_plural = True
                    pronoun = "we"
                    possessive_pronoun = "our"
                elif w_low in ("he", "him"):
                    pronoun = "he"
                    possessive_pronoun = "his"
                elif w_low in ("she", "her"):
                    pronoun = "she"
                    possessive_pronoun = "her"
                elif (
                    subj_token.text.endswith("s")
                    and not subj_token.text.endswith(("ss", "us", "is"))
                    and len(subj_token.text) > 3
                ):
                    is_plural = True
                    pronoun = "they"
                    possessive_pronoun = "their"
                elif is_human_agent:
                    pronoun = "they"
                    possessive_pronoun = "their"
                subject_text = subj_token.text
            else:
                subject_text = "it"

            # 3. Tense resolution
            is_past = any(
                t.tag_ in ("VBD", "VBN") or t.text.lower() in ("was", "were", "had", "did")
                for t in doc
            )

            # 4. Copula and auxiliary verbs
            copula = "were" if (is_plural and is_past) else ("was" if is_past else ("are" if is_plural else "is"))
            negative_copula = f"{copula} not"
            aux_do = "did" if is_past else ("do" if is_plural else "does")
            aux_do_not = f"{aux_do} not"

            # 5. Descriptive attribute / focus extraction
            desc_token = None
            for t in doc:
                if (
                    t.dep_ in ("acomp", "advmod", "amod", "attr")
                    and t.pos_ in ("ADJ", "ADV")
                    and t.text.lower() not in ("not", "never", "very", "really", "too", "so", "quite", "more", "most")
                ):
                    desc_token = t
                    break

            descriptor = desc_token.text if desc_token else None
            descriptor_pos = desc_token.pos_ if desc_token else None
            descriptor_lemma = desc_token.lemma_.lower() if desc_token else None

            # 6. Antonyms and sentiment
            if descriptor_lemma:
                antonyms = self.get_ranked_opposites(descriptor_lemma, descriptor_pos)
                is_negative_sentiment = self.is_negative_word(descriptor_lemma, descriptor_pos)
            else:
                antonyms = []
                is_negative_sentiment = False

            return SentenceFeatures(
                original_text=clean_s,
                tokens=tokens,
                pos_tags=pos_tags,
                subject=subject_text,
                pronoun=pronoun,
                possessive_pronoun=possessive_pronoun,
                is_plural=is_plural,
                is_past_tense=is_past,
                copula=copula,
                negative_copula=negative_copula,
                aux_do=aux_do,
                aux_do_not=aux_do_not,
                root_lemma=root_lemma,
                direct_object=direct_object_text,
                is_human_agent=is_human_agent,
                is_human_object=is_human_object,
                entity_domain=entity_domain,
                descriptor=descriptor,
                descriptor_pos=descriptor_pos,
                descriptor_lemma=descriptor_lemma,
                is_negative_sentiment=is_negative_sentiment,
                antonyms=antonyms,
                noun_chunks=noun_chunks,
            )

        # Fallback if spaCy is unavailable
        import nltk
        tokens = nltk.word_tokenize(clean_s)
        pos_tags = nltk.pos_tag(tokens)
        nouns = [w for w, t in pos_tags if t in ("NN", "NNS", "NNP", "NNPS")]
        subject_text = nouns[0] if nouns else "it"
        is_plural = any(t in ("NNS", "NNPS") for w, t in pos_tags if w.lower() == subject_text.lower())
        pronoun = "they" if is_plural else "it"
        possessive_pronoun = "their" if is_plural else "its"

        is_past = any(t in ("VBD", "VBN") or w.lower() in ("was", "were", "had", "did") for w, t in pos_tags)
        copula = "were" if (is_plural and is_past) else ("was" if is_past else ("are" if is_plural else "is"))
        negative_copula = f"{copula} not"
        aux_do = "did" if is_past else ("do" if is_plural else "does")
        aux_do_not = f"{aux_do} not"

        desc_token = None
        desc_pos = None
        for w, t in pos_tags:
            if t.startswith("JJ") or t.startswith("RB"):
                if w.lower() not in ("not", "never", "very", "really", "too", "so"):
                    desc_token = w
                    desc_pos = "ADJ" if t.startswith("JJ") else "ADV"
                    break

        antonyms = self.get_ranked_opposites(desc_token, desc_pos) if desc_token else []

        return SentenceFeatures(
            original_text=clean_s,
            tokens=tokens,
            pos_tags=pos_tags,
            subject=subject_text,
            pronoun=pronoun,
            possessive_pronoun=possessive_pronoun,
            is_plural=is_plural,
            is_past_tense=is_past,
            copula=copula,
            negative_copula=negative_copula,
            aux_do=aux_do,
            aux_do_not=aux_do_not,
            root_lemma="operate",
            direct_object=None,
            is_human_agent=False,
            is_human_object=False,
            entity_domain="general",
            descriptor=desc_token,
            descriptor_pos=desc_pos,
            descriptor_lemma=desc_token.lower() if desc_token else None,
            is_negative_sentiment=False,
            antonyms=antonyms,
            noun_chunks=nouns,
        )
