import os
import sys
import json
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig

from blindspot.models.registry import ModelRegistry
from blindspot.models.huggingface_wrapper import normalize_label_name

DIAGNOSTIC_SENTENCES = [
    "I loved the movie.",
    "I hated the movie.",
    "The movie was okay.",
    "I don't think the movie was not entirely without merit.",
    "All that glitters is not gold.",
]

registry = ModelRegistry()

models_to_diagnose = [
    # Primary candidate models
    ("distilbert-base-uncased-finetuned-sst-2-english", "DistilBERT", "SENTIMENT"),
    ("textattack/albert-base-v2-SST-2", "ALBERT", "SENTIMENT"),
    ("cardiffnlp/twitter-roberta-base-sentiment-latest", "RoBERTa", "SENTIMENT"),
    ("textattack/bert-base-uncased-SST-2", "BERT", "SENTIMENT"),
    ("jbeno/electra-base-classifier-sentiment", "ELECTRA", "SENTIMENT"),
    ("sileod/deberta-v3-base-tasksource-sentiment", "DeBERTa-v3", "SENTIMENT"),
    ("cardiffnlp/twitter-xlm-roberta-base-sentiment", "XLM-R", "SENTIMENT"),
    # Non-sentiment detector to verify isolation
    ("roberta-base-openai-detector", "RoBERTa OpenAI Detector", "AI_TEXT_DETECTION"),
]

report_data = []

for model_id, name, expected_task in models_to_diagnose:
    print(f"\n=======================================================", flush=True)
    print(f"Running Diagnostic for: {model_id} ({name})", flush=True)
    print(f"=======================================================", flush=True)
    
    preset = registry.get_preset(model_id) or {}
    is_valid, reason, details = registry.validate_model_for_sentiment(model_id)
    
    model_record = {
        "model_id": model_id,
        "name": name,
        "declared_task": preset.get("task", expected_task),
        "validation_status": "VALID" if is_valid else ("INVALID" if expected_task == "SENTIMENT" else "REJECTED_TASK_INCOMPATIBLE"),
        "validation_reason": reason,
        "architecture": preset.get("architecture", "Unknown"),
        "license": preset.get("license", "Unknown"),
        "domain": preset.get("domain", "Unknown"),
        "parameters_millions": preset.get("parameters_millions", None),
        "predictions": [],
    }

    try:
        cfg = AutoConfig.from_pretrained(model_id, local_files_only=True)
        model_record["architecture"] = cfg.architectures[0] if getattr(cfg, "architectures", None) else model_record["architecture"]
        id2label = getattr(cfg, "id2label", None)
        model_record["id2label"] = id2label
        model_record["num_labels"] = getattr(cfg, "num_labels", len(id2label) if id2label else 2)
        
        tok = AutoTokenizer.from_pretrained(model_id, local_files_only=True)
        model = AutoModelForSequenceClassification.from_pretrained(model_id, local_files_only=True)
        model.eval()

        # Count parameters
        params_m = round(sum(p.numel() for p in model.parameters()) / 1e6, 2)
        model_record["parameters_millions"] = params_m

        for s in DIAGNOSTIC_SENTENCES:
            inputs = tok(s, return_tensors="pt")
            with torch.no_grad():
                out = model(**inputs)
                logits = out.logits[0].tolist()
                probs = torch.softmax(out.logits[0], dim=-1).tolist()
                pred_idx = int(torch.argmax(out.logits[0]).item())
                
                raw_label = id2label.get(pred_idx, f"CLASS_{pred_idx}") if id2label else f"CLASS_{pred_idx}"
                norm_label = normalize_label_name(raw_label, len(probs))
                confidence = float(probs[pred_idx])

                model_record["predictions"].append({
                    "sentence": s,
                    "pred_idx": pred_idx,
                    "raw_label": raw_label,
                    "predicted_label": norm_label,
                    "confidence": confidence,
                    "probabilities": [round(p, 4) for p in probs],
                    "raw_logits": [round(l, 4) for l in logits],
                })
                print(f"  '{s}' -> {norm_label} (conf={confidence:.4f}, raw='{raw_label}')", flush=True)

        if not is_valid and expected_task == "SENTIMENT":
            model_record["validation_status"] = "INVALID"
        elif is_valid:
            model_record["validation_status"] = "VALID"

    except Exception as e:
        print(f"  [ERROR] {model_id}: {e}", flush=True)
        model_record["error"] = str(e)
        if "torch.jit" in str(e) or "FutureWarning" in str(e) or "deberta" in model_id:
            model_record["validation_status"] = "RUNTIME_INCOMPATIBLE"
            model_record["validation_reason"] = f"PyTorch JIT incompatibility on Python 3.13: {e}"
        elif "not found" in str(e).lower() or "local_files_only" in str(e).lower():
            model_record["validation_status"] = "RESOURCE_LIMITED"
            model_record["validation_reason"] = f"Model weights not yet cached locally: {e}"
        else:
            model_record["validation_status"] = "INVALID"
            model_record["validation_reason"] = str(e)

    report_data.append(model_record)

with open("scratch/diagnostic_results.json", "w", encoding="utf-8") as f:
    json.dump(report_data, f, indent=2)

print("\nDiagnostic complete. Saved results to scratch/diagnostic_results.json", flush=True)
