import json
import torch
import numpy as np
from transformers import AutoConfig, AutoTokenizer, AutoModelForSequenceClassification
from blindspot.models.registry import ModelRegistry
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper, normalize_label_name

test_sentences = [
    "I loved the movie.",
    "I hated the movie.",
    "The movie was okay.",
    "I don't think the movie was not entirely without merit.",
]

models_to_test = [
    "distilbert-base-uncased-finetuned-sst-2-english",
    "cardiffnlp/twitter-roberta-base-sentiment-latest",
    "textattack/bert-base-uncased-SST-2",
    "roberta-base-openai-detector",
    "cardiffnlp/twitter-roberta-base-sentiment",
]

report_data = {}

for mid in models_to_test:
    print(f"=== Testing {mid} ===")
    model_data = {"model_id": mid}
    try:
        cfg = AutoConfig.from_pretrained(mid)
        model_data["raw_id2label"] = getattr(cfg, "id2label", None)
        model_data["raw_label2id"] = getattr(cfg, "label2id", None)
        model_data["num_classes"] = getattr(cfg, "num_labels", None)
        model_data["architectures"] = getattr(cfg, "architectures", None)
        model_data["model_type"] = getattr(cfg, "model_type", None)
    except Exception as e:
        model_data["config_error"] = str(e)

    try:
        tok = AutoTokenizer.from_pretrained(mid)
        model_data["tokenizer_type"] = type(tok).__name__
    except Exception as e:
        model_data["tokenizer_error"] = str(e)

    try:
        mdl = AutoModelForSequenceClassification.from_pretrained(mid)
        model_data["head_type"] = type(mdl.classifier if hasattr(mdl, "classifier") else getattr(mdl, "score", None)).__name__
        model_data["model_class"] = type(mdl).__name__
    except Exception as e:
        model_data["model_load_error"] = str(e)

    # Now test via HuggingFaceWrapper
    try:
        wrapper = HuggingFaceWrapper(model_name_or_path=mid, device="cpu")
        model_data["wrapper_labels"] = wrapper.labels
        model_data["wrapper_loaded"] = wrapper.pipeline is not None

        sentence_results = []
        for s in test_sentences:
            res = wrapper.predict_result(s)
            # Also get raw pipeline output if possible
            raw_out = None
            if wrapper.pipeline:
                try:
                    raw_out = wrapper.pipeline(s, top_k=None)
                except Exception as e:
                    raw_out = str(e)

            sentence_results.append({
                "sentence": s,
                "predicted_label": res.label,
                "confidence": res.confidence,
                "probabilities": res.probabilities,
                "raw_pipeline_output": raw_out,
            })
        model_data["sentences"] = sentence_results
    except Exception as e:
        model_data["wrapper_error"] = str(e)

    report_data[mid] = model_data

with open("scratch/model_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(report_data, f, indent=2)

print("Diagnostic complete. Results saved to scratch/model_audit_results.json")
