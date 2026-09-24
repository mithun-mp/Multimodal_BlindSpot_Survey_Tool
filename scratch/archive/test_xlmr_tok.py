from transformers import AutoTokenizer

try:
    tok = AutoTokenizer.from_pretrained("cardiffnlp/twitter-xlm-roberta-base-sentiment")
    print("XLM-R tokenizer success:", type(tok))
except Exception as e:
    print("XLM-R tokenizer error:", e)
