import json
import matplotlib.pyplot as plt
from blindspot.reporting.thesis_graphs import ThesisVisualizer, get_model_short_name

res = json.load(open('runs/exp_1790537272_6f4cc1/results.json'))
models_data = res.get("models", {})
names = [get_model_short_name(m) for m in models_data.keys()]
print("Model names:", names)

viz = ThesisVisualizer('runs/exp_1790537272_6f4cc1/figures')
out = viz.plot_model_prediction_distribution(res, filename="test_fig01.png")
print("Saved to:", out)

# Check text in figure
import PIL.Image
img = PIL.Image.open(out)
print("Image size:", img.size)
