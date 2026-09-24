import sys
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_id = "jbeno/electra-base-classifier-sentiment"
print(f"Loading tokenizer for {model_id}...", flush=True)
tok = AutoTokenizer.from_pretrained(model_id, local_files_only=True)
print(f"Loading model for {model_id}...", flush=True)
model = AutoModelForSequenceClassification.from_pretrained(model_id, local_files_only=True)
model.eval()

sentences = [
    "I loved the movie.",
    "I hated the movie.",
    "The movie was okay.",
    "I don't think the movie was not entirely without merit.",
    "All that glitters is not gold."
]

for s in sentences:
    inputs = tok(s, return_tensors="pt")
    with torch.no_grad():
        out = model(**inputs)
        logits = out.logits[0]
        probs = torch.softmax(logits, dim=-1).tolist()
        pred_idx = torch.argmax(logits).item()
        pred_label = model.config.id2label.get(pred_idx, str(pred_idx))
    print(f"'{s}' -> {pred_label} (prob={probs[pred_idx]:.4f}, logits={logits.tolist()}, probs={probs})", flush=True)
