from transformers import AutoConfig

candidates = [
    'textattack/albert-base-v2-imdb',
    'textattack/albert-base-v2-rotten-tomatoes',
    'textattack/xlnet-base-cased-imdb',
    'textattack/xlnet-base-cased-rotten-tomatoes',
    'valhalla/bart-large-sst2',
    'facebook/bart-large-mnli',
    'aychang/roberta-base-imdb',
    'anarn/albert-base-v2-finetuned-sst2',
    'Alireza1044/albert-base-v2-sst2',
]

for c in candidates:
    try:
        cfg = AutoConfig.from_pretrained(c)
        print(f"=== {c} ===")
        print(f"  arch: {cfg.architectures}")
        print(f"  model_type: {getattr(cfg, 'model_type', None)}")
        print(f"  id2label: {getattr(cfg, 'id2label', None)}")
    except Exception as e:
        pass
