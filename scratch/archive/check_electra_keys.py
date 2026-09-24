import torch

bin_path = r"C:\Users\maste\.cache\huggingface\hub\models--jbeno--electra-base-classifier-sentiment\snapshots\73296c777ced3e2176d811ecffeb9673e610d7a6\pytorch_model.bin"
sd = torch.load(bin_path, map_location="cpu", weights_only=True)
classifier_keys = [k for k in sd.keys() if "classifier" in k]
for k in classifier_keys:
    print(f"  {k}: {sd[k].shape}")
