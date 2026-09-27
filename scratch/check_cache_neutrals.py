import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

sia = SentimentIntensityAnalyzer()
sia.lexicon.update({
    'hospitalized': -2.5,
    'hospital': -1.2,
    'naughty': -1.8,
    'healthy': 2.0,
    'ill': -2.0,
    'unwell': -2.0,
    'sick': -2.0,
    'disease': -2.5,
    'infected': -2.5,
    'infection': -2.0,
    'painful': -2.2,
    'hurts': -2.0,
    'injury': -2.0,
    'injured': -2.0,
    'wound': -2.0,
})

def resolve_polarity(text: str) -> str:
    t_lower = text.lower()
    contrast_match = re.split(r'\b(?:but|however|yet|nevertheless|nonetheless|although|though)\b', t_lower)
    if len(contrast_match) > 1:
        c1, c2 = contrast_match[0].strip(), contrast_match[1].strip()
        score1 = sia.polarity_scores(c1)['compound']
        score2 = sia.polarity_scores(c2)['compound']
        weighted = (0.25 * score1) + (0.75 * score2)
        if weighted >= 0.05:
            return "POSITIVE"
        elif weighted <= -0.05:
            return "NEGATIVE"

    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        return "POSITIVE"
    elif score <= -0.05:
        return "NEGATIVE"
    return "NEUTRAL"

with open('cache/semantic_cache.json', 'r', encoding='utf-8') as f:
    cache = json.load(f)

changed = 0
for k, v in cache.items():
    old_pol = v.get('final_semantic_polarity')
    txt = v.get('sentence_text', '')
    new_pol = resolve_polarity(txt)
    if old_pol == 'NEUTRAL' and new_pol != 'NEUTRAL':
        changed += 1
        print(f"FIX: {txt!r:50} : NEUTRAL -> {new_pol}")

print(f"\nTotal false neutrals found in cache: {changed} / {len(cache)}")
