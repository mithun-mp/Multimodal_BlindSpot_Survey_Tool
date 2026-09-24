import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel

bin_path = r"C:\Users\maste\.cache\huggingface\hub\models--jbeno--electra-base-classifier-sentiment\snapshots\73296c777ced3e2176d811ecffeb9673e610d7a6\pytorch_model.bin"
sd = torch.load(bin_path, map_location="cpu", weights_only=True)

class ElectraCustomClassifier(nn.Module):
    def __init__(self, electra_encoder, sd):
        super().__init__()
        self.electra = electra_encoder
        # Build the exact classifier structure from state_dict
        # layers.0: Linear(768, 1024)
        # layers.1: GeLU or similar / projection? Let's check layers
        # layers.3: Linear(1024, 1024)
        # layers.6: Linear(1024, 3)
        self.l0 = nn.Linear(768, 1024)
        self.l0.weight.data = sd["classifier.layers.0.weight"]
        self.l0.bias.data = sd["classifier.layers.0.bias"]
        
        self.l3 = nn.Linear(1024, 1024)
        self.l3.weight.data = sd["classifier.layers.3.weight"]
        self.l3.bias.data = sd["classifier.layers.3.bias"]
        
        self.l6 = nn.Linear(1024, 3)
        self.l6.weight.data = sd["classifier.layers.6.weight"]
        self.l6.bias.data = sd["classifier.layers.6.bias"]
        self.act = nn.GELU()

    def forward(self, input_ids, attention_mask=None, token_type_ids=None):
        out = self.electra(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        cls_rep = out.last_hidden_state[:, 0, :]
        x = self.act(self.l0(cls_rep))
        x = self.act(self.l3(x))
        logits = self.l6(x)
        return logits

tok = AutoTokenizer.from_pretrained("jbeno/electra-base-classifier-sentiment", local_files_only=True)
encoder = AutoModel.from_pretrained("jbeno/electra-base-classifier-sentiment", local_files_only=True)
custom_model = ElectraCustomClassifier(encoder, sd)
custom_model.eval()

sentences = [
    "I loved the movie.",
    "I hated the movie.",
    "The movie was okay."
]
id2label = {0: "negative", 1: "neutral", 2: "positive"}
for s in sentences:
    inp = tok(s, return_tensors="pt")
    with torch.no_grad():
        logits = custom_model(**inp)[0]
        probs = torch.softmax(logits, dim=-1).tolist()
        pred = id2label[torch.argmax(logits).item()]
    print(f"'{s}' -> {pred} ({probs})")
