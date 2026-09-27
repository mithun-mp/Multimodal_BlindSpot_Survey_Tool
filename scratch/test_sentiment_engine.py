from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
sentences = [
    'i am healthy but still hospitalized',
    'i am not healthy but still hospitalized',
    'i am healthy',
    'i am not healthy',
    'He is a Good boy but very naughty',
    'He is a good boy',
    'He is very naughty',
    'The movie was great',
    'The movie was not great',
    'The package arrived on Monday',
    'All that glitters is not gold.',
    'She is kind and helpful',
    'He is rude and annoying',
    'The food was neither good nor bad',
]
for s in sentences:
    res = sia.polarity_scores(s)
    pol = 'POSITIVE' if res['compound'] >= 0.05 else ('NEGATIVE' if res['compound'] <= -0.05 else 'NEUTRAL')
    print(f"{s!r:45} -> {pol:8} (compound: {res['compound']:+.4f}, pos={res['pos']:.2f}, neg={res['neg']:.2f})")
