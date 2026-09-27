import json

with open('cache/semantic_cache.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('Total cached entries:', len(d))
for k, v in list(d.items())[:20]:
    txt = v.get('sentence_text')
    pol = v.get('final_semantic_polarity')
    src = v.get('verification_source')
    model = v.get('model_used')
    print(f"[{src}|{model}] {txt!r} -> {pol}")
