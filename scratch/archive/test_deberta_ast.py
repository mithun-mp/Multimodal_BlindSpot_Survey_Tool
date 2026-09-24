import torch
from transformers import AutoConfig, AutoModelForSequenceClassification

print("PyTorch version:", torch.__version__)
cfg = AutoConfig.from_pretrained("sileod/deberta-v3-base-tasksource-sentiment")
print("Config loaded. Trying to instantiate model without weights...")
try:
    m = AutoModelForSequenceClassification.from_config(cfg)
    print("Model instantiated successfully!")
except Exception as e:
    print("Instantiation error:", e)
