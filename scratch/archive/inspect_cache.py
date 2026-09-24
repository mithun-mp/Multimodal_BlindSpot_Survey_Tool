import os
from pathlib import Path

hub_dir = Path(r"C:\Users\maste\.cache\huggingface\hub")
for m_dir in sorted(hub_dir.glob("models--*")):
    m_name = m_dir.name.replace("models--", "").replace("--", "/")
    snapshots = list((m_dir / "snapshots").glob("*")) if (m_dir / "snapshots").exists() else []
    files = []
    has_weights = False
    total_size_mb = 0
    for s in snapshots:
        for f in s.glob("*"):
            sz = f.stat().st_size / (1024 * 1024)
            total_size_mb += sz
            files.append(f"{f.name} ({sz:.1f}MB)")
            if f.suffix in {".bin", ".safetensors", ".pt", ".h5"} or "weight" in f.name:
                has_weights = True
    print(f"=== {m_name} ===")
    print(f"  has_weights: {has_weights}, total_size: {total_size_mb:.1f}MB")
    print(f"  files: {', '.join(files[:6])}")
