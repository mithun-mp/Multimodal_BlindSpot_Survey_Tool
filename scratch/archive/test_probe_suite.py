import sys
import os

workspace = r"c:\Dev\Projects\BlinkSpot-main"
if workspace not in sys.path:
    sys.path.insert(0, workspace)

from blindspot.perturbations.shared import SharedProbeGenerator

gen = SharedProbeGenerator()
test_sentences = [
    "The movie was great and the acting was top notch.",
    "The service at the restaurant was terrible and the food was cold.",
    "All that glitters is not gold.",
]

for s in test_sentences:
    print(f"\n==========================================")
    print(f"SEED: '{s}'")
    pset = gen.generate_probes([s])
    print(f"Total probes generated: {len(pset.probes)}")
    for i, p in enumerate(pset.probes):
        print(f"  #{i+1}: [{p.perturbation_type}] '{p.perturbed_text}'")
        print(f"       expected_flip: {p.expected_flip} | effect: {p.expected_semantic_effect} | intent: {getattr(p, 'semantic_intent', None)}")
