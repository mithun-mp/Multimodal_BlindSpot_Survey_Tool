import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_id = "textattack/albert-base-v2-SST-2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)
model.eval()

sentences = [
    "I loved the movie.",
    "I hated the movie.",
]

for s in sentences:
    inputs = tokenizer(s, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits[0]
        probs = torch.softmax(logits, dim=-1).tolist()
    print(f"Sentence: {s}")
    print(f"  Logits: {logits.tolist()}")
    print(f"  Probs: {probs}")
    print(f"  Argmax: {torch.argmax(logits).item()}")
