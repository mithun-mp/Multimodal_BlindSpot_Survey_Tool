import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

candidates = [
    'cardiffnlp/twitter-roberta-base-sentiment',
    'aychang/roberta-base-imdb',
    'textattack/albert-base-v2-rotten-tomatoes',
    'Alireza1044/albert-base-v2-sst2'
]

test_sents = ['I loved the movie.', 'I hated the movie.', 'The movie was okay.', 'I don\'t think the movie was not entirely without merit.', 'All that glitters is not gold.']

for model_id in candidates:
    print(f"=== Testing {model_id} ===")
    try:
        tok = AutoTokenizer.from_pretrained(model_id, local_files_only=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_id, local_files_only=True)
        model.eval()
        print(f"Loaded successfully! Architecture: {model.__class__.__name__}")
        print(f"id2label: {model.config.id2label}")
        for s in test_sents:
            inputs = tok(s, return_tensors='pt')
            with torch.no_grad():
                out = model(**inputs)
                probs = torch.softmax(out.logits, dim=-1)[0]
                pred = torch.argmax(probs).item()
                label = model.config.id2label[pred]
                print(f"  '{s}' -> {label} (conf={probs[pred]:.4f})")
    except Exception as e:
        print(f"  Failed: {e}")
