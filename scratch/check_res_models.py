import json

res = json.load(open('runs/exp_1790537272_6f4cc1/results.json'))
print("Models keys:", list(res.get("models", {}).keys()))
for k, v in res.get("models", {}).items():
    print("Model key:", k)
    if "evaluations" in v:
        print("  evals count:", len(v["evaluations"]))
    elif "probe_results" in v:
        print("  probe_results count:", len(v["probe_results"]))
