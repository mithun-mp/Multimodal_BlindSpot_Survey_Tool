import os

def get_dir_size(path):
    total = 0
    count = 0
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    total += os.path.getsize(fp)
                    count += 1
                except Exception:
                    pass
    return total, count

dirs = ['runs', 'logs', 'scratch', 'audit_reports', 'blindspot', 'tests', 'docs']
print("=== DIRECTORY FOOTPRINT ===")
for d in dirs:
    size, count = get_dir_size(d)
    print(f"{d:15s}: {count:5d} files, {size / (1024*1024):8.2f} MB")

hf_cache = os.path.expanduser("~/.cache/huggingface/hub")
hf_size, hf_count = get_dir_size(hf_cache)
print(f"{'HF hub cache':15s}: {hf_count:5d} files, {hf_size / (1024*1024):8.2f} MB")

ws_size, ws_count = get_dir_size(".")
print(f"{'Workspace total':15s}: {ws_count:5d} files, {ws_size / (1024*1024):8.2f} MB")
