from blindspot.models.cache import ModelCache
cache = ModelCache.get_shared_cache()
m = cache.get('cardiffnlp/twitter-roberta-base-sentiment-latest')
for s in [
    'i am healthy but still hospitalized',
    'i am not healthy but still hospitalized',
    'He is a Good boy but very naughty',
    'He is very naughty',
    'i am healthy',
    'i am not healthy'
]:
    r = m.predict(s)
    print(f"{s!r:45} -> {r.predicted_label:8} ({r.confidence*100:.1f}%) probs: {r.probabilities}")
