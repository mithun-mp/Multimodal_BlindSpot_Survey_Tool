import requests
import time

url = "https://huggingface.co/textattack/albert-base-v2-SST-2/resolve/main/pytorch_model.bin"
print(f"Testing direct download from {url}...", flush=True)
t0 = time.time()
r = requests.get(url, stream=True, timeout=10)
print(f"Status: {r.status_code}, headers: {r.headers.get('content-length')}", flush=True)
chunk = next(r.iter_content(chunk_size=1024*1024))
print(f"Downloaded chunk of {len(chunk)} bytes in {time.time()-t0:.2f}s", flush=True)
