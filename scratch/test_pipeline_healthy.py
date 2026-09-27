from blindspot.semantic.service import get_semantic_service
from blindspot.perturbations.shared import SharedProbeGenerator

gen = SharedProbeGenerator()
pset = gen.generate_probes(["i am healthy but still hospitalized"])
svc = get_semantic_service()
ref = svc.annotate_experiment("i am healthy but still hospitalized", pset.probes, force_refresh=True)

print("Baseline:", repr(ref.baseline_annotation.sentence_text), "->", ref.baseline_annotation.final_semantic_polarity.value)
for pid, pa in list(ref.probe_annotations.items()):
    rel = pa.semantic_relation_to_baseline.value if hasattr(pa.semantic_relation_to_baseline, 'value') else str(pa.semantic_relation_to_baseline)
    print(f"Probe: {pa.sentence_text!r:65} -> {pa.final_semantic_polarity.value:8} (Rel: {rel})")
