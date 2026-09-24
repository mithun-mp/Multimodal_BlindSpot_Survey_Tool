import logging
logging.basicConfig(level=logging.INFO)
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper

models = [
    "distilbert-base-uncased-finetuned-sst-2-english",
    "textattack/albert-base-v2-SST-2",
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "textattack/bert-base-uncased-SST-2",
    "cardiffnlp/twitter-roberta-base-sentiment",
]

test_sents = [
    "I loved the movie.",
    "I hated the movie.",
    "The movie was okay.",
    "All that glitters is not gold."
]

for m in models:
    print(f"\n==================== Testing Wrapper: {m} ====================")
    w = HuggingFaceWrapper(m, device="cpu", allow_fallback=False)
    print(f"Loaded: pipeline={w.pipeline is not None}, labels={w.labels}, num_classes={w.num_classes}, params={w.parameters_millions}M")
    for s in test_sents:
        res = w.predict_result(s)
        print(f"  '{s}' -> {res.label} (conf={res.confidence:.4f}, status={res.model_status})")
