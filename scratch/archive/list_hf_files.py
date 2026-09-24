import os
from huggingface_hub import HfApi

api = HfApi()
models = [
    "jbeno/electra-base-classifier-sentiment",
    "sileod/deberta-v3-base-tasksource-sentiment",
    "cardiffnlp/twitter-xlm-roberta-base-sentiment",
]

for m in models:
    try:
        files = api.list_repo_files(m)
        print(f"=== {m} ===")
        print(f"  files: {files}")
    except Exception as e:
        print(f"=== {m} === Error: {e}")
