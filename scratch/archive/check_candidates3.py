from transformers import AutoConfig

candidates = [
    'TehranNLP-org/albert-base-v2-sentiment-sst2',
    'yiyanghkust/finbert-tone',
    'distilbert/distilbert-base-uncased-finetuned-sst-2-english',
    'cardiffnlp/twitter-roberta-base-sentiment-latest',
    'albert/albert-base-v2',
    'bhadresh-psavani/distilbert-base-uncased-emotion', # emotion - should be rejected!
    'google/electra-base-discriminator',
    'facebook/bart-base',
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
