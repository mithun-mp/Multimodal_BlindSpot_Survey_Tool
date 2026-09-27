import os

for root, dirs, files in os.walk('blindspot'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, encoding='utf-8', errors='ignore') as fp:
                for idx, line in enumerate(fp, 1):
                    lower = line.lower()
                    if ('split("/")' in line or "split('/')" in line or '[:1' in line or '[:2' in line or '[:8' in line) and ('model' in lower or 'm_' in lower or 'm.' in lower or 'm ' in lower or 'mid' in lower):
                        print(f"{p}:{idx} -> {line.strip()}")
