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
    # Check contrast connective "X but Y", "X however Y"
    # In English linguistics, the second clause after "but/however/yet" carries dominant discourse weight
    t_lower = text.lower()
    contrast_match = re.split(r'\b(?:but|however|yet|nevertheless|nonetheless|although|though)\b', t_lower)
    if len(contrast_match) > 1:
        # Check first and second clause
        c1, c2 = contrast_match[0].strip(), contrast_match[1].strip()
        score1 = sia.polarity_scores(c1)['compound']
        score2 = sia.polarity_scores(c2)['compound']
        # Weighted discourse score: second clause carries 70% weight
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

sentences = [
    'i am healthy but still hospitalized',
    'i am not healthy but still hospitalized',
    'He is a Good boy but very naughty',
    'He is a good boy',
    'He is very naughty',
    'i am healthy',
    'i am not healthy',
    'The package arrived on Monday',
    'The food was terrible',
    'The film was breathtaking and wonderful',
    'The engine stopped working',
    'She felt miserable',
    'We enjoyed the sunny day at the beach',
]

for s in sentences:
    pol = resolve_polarity(s)
    print(f"{s!r:45} -> {pol}")
