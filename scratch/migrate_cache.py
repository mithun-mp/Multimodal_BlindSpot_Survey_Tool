import json
from blindspot.semantic.analyzer import get_exact_analyzer
from blindspot.semantic.types import SemanticReferenceLabel

analyzer = get_exact_analyzer()
cache_path = "cache/semantic_cache.json"

with open(cache_path, "r", encoding="utf-8") as f:
    cache = json.load(f)

migrated = 0
for key, item in cache.items():
    current_pol = item.get("final_semantic_polarity")
    text = item.get("sentence_text", "")
    if current_pol == "NEUTRAL":
        exact_pol, conf, reason = analyzer.analyze(text)
        if exact_pol != SemanticReferenceLabel.NEUTRAL:
            migrated += 1
            item["semantic_polarity"] = exact_pol.value
            item["final_semantic_polarity"] = exact_pol.value
            item["confidence"] = round(conf, 4)
            item["reason"] = f"[Antigravity Exact Prediction] {reason}"
            item["verification_source"] = "ANTIGRAVITY_EXACT"
            item["model_used"] = "antigravity_exact_engine"
            print(f"Migrated [{migrated}]: {text!r:50} -> {exact_pol.value}")

with open(cache_path, "w", encoding="utf-8") as f:
    json.dump(cache, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully migrated {migrated} entries in {cache_path}!")
