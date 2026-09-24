import sys
import time
from huggingface_hub import hf_hub_download

model_id = "jbeno/electra-base-classifier-sentiment"
print(f"Downloading weights for {model_id}...", flush=True)
t0 = time.time()
try:
    path = hf_hub_download(
        repo_id=model_id,
        filename="pytorch_model.bin",
    )
    print(f"Downloaded weights to {path} in {time.time()-t0:.2f}s", flush=True)
except Exception as e:
    print(f"Download error: {e}", flush=True)
