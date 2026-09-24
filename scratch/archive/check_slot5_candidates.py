import sys
from transformers import AutoConfig

candidates = [
    'textattack/albert-base-v2-SST-2',
    'bhadresh-psavani/albert-base-v2-sst2',
    'Chaarangan/albert-base-v2-sentiment-analysis',
    'cardiffnlp/twitter-roberta-base-sentiment-latest',
    'distilbert/distilbert-base-uncased-finetuned-sst-2-english',
    'ProsusAI/finbert',
    'siebert/sentiment-roberta-large-english',
    'finiteautomata/bertweet-base-sentiment-analysis',
    'roberta-base-openai-detector'
]

for c in candidates:
    try:
        cfg = AutoConfig.from_pretrained(c)
        print(f"=== {c} ===")
        print(f"  arch: {cfg.architectures}")
        print(f"  model_type: {getattr(cfg, 'model_type', None)}")
        print(f"  id2label: {getattr(cfg, 'id2label', None)}")
    except Exception as e:
        print(f"=== {c} === Error: {e}")
