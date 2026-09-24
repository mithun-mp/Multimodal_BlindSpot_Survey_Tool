import json
from transformers import AutoConfig

candidates = [
    "distilbert-base-uncased-finetuned-sst-2-english",
    "jbeno/electra-base-classifier-sentiment",
    "sileod/deberta-v3-base-tasksource-sentiment",
    "cardiffnlp/twitter-xlm-roberta-base-sentiment",
    "textattack/albert-base-v2-SST-2",
    "textattack/xlnet-base-cased-SST-2",
]

for c in candidates:
    try:
        cfg = AutoConfig.from_pretrained(c)
        print(f"=== {c} ===")
        print(f"  Architectures: {getattr(cfg, 'architectures', None)}")
        print(f"  Model Type: {getattr(cfg, 'model_type', None)}")
        print(f"  Num Labels: {getattr(cfg, 'num_labels', None)}")
        print(f"  id2label: {getattr(cfg, 'id2label', None)}")
        print(f"  label2id: {getattr(cfg, 'label2id', None)}")
    except Exception as e:
        print(f"=== {c} === ERROR: {e}")
