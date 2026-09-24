import sys
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_id = "sileod/deberta-v3-base-tasksource-sentiment"
print(f"Loading tokenizer for {model_id}...", flush=True)
tok = AutoTokenizer.from_pretrained(model_id)
print(f"Loading model for {model_id}...", flush=True)
model = AutoModelForSequenceClassification.from_pretrained(model_id)
model.eval()

sentences = [
    "I loved the movie.",
    "I hated the movie.",
]

for s in sentences:
    inputs = tok(s, return_tensors="pt")
    with torch.no_grad():
        out = model(**inputs)
        logits = out.logits[0]
        probs = torch.softmax(logits, dim=-1).tolist()
        pred_idx = torch.argmax(logits).item()
        pred_label = model.config.id2label.get(pred_idx, str(pred_idx))
    print(f"Sentence: {s} -> {pred_label} (prob={probs[pred_idx]:.4f}, probs={probs})", flush=True)
