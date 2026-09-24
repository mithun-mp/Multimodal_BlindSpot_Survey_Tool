import torch
import time

bin_path = r"C:\Users\maste\.cache\huggingface\hub\models--jbeno--electra-base-classifier-sentiment\snapshots\73296c777ced3e2176d811ecffeb9673e610d7a6\pytorch_model.bin"
print("Loading with torch.load...", flush=True)
t0 = time.time()
try:
    state_dict = torch.load(bin_path, map_location="cpu", weights_only=True)
    print(f"torch.load (weights_only=True) succeeded in {time.time()-t0:.2f}s! Keys: {len(state_dict)}", flush=True)
except Exception as e:
    print(f"torch.load failed: {e}", flush=True)
