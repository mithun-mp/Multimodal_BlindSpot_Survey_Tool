import torch
from transformers import AutoConfig, AutoModelForSequenceClassification

for m in ["jbeno/electra-base-classifier-sentiment", "cardiffnlp/twitter-xlm-roberta-base-sentiment"]:
    print(f"Testing instantiation for {m}...", flush=True)
    cfg = AutoConfig.from_pretrained(m)
    model = AutoModelForSequenceClassification.from_config(cfg)
    print(f"  SUCCESS for {m}: {type(model).__name__}", flush=True)
