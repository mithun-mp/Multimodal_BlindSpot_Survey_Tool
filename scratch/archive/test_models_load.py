import sys
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

models_to_test = [
    "distilbert-base-uncased-finetuned-sst-2-english",
    "jbeno/electra-base-classifier-sentiment",
    "sileod/deberta-v3-base-tasksource-sentiment",
    "cardiffnlp/twitter-xlm-roberta-base-sentiment",
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "ProsusAI/finbert",
    "siebert/sentiment-roberta-large-english",
]

for m in models_to_test:
    print(f"\n==================== Testing: {m} ====================")
    try:
        tok = AutoTokenizer.from_pretrained(m)
        print(f"  [OK] Tokenizer loaded: {type(tok).__name__}")
        model = AutoModelForSequenceClassification.from_pretrained(m)
        model.eval()
        print(f"  [OK] Model loaded: {type(model).__name__}")
        inputs = tok("I loved the movie.", return_tensors="pt")
        with torch.no_grad():
            out = model(**inputs)
            logits = out.logits[0]
            probs = torch.softmax(logits, dim=-1).tolist()
            pred_idx = torch.argmax(logits).item()
            pred_label = model.config.id2label.get(pred_idx, str(pred_idx))
        print(f"  [OK] Inference: logits={logits.tolist()}, probs={probs}, pred={pred_label}")
    except Exception as e:
        print(f"  [FAILED] {m}: {e}")
