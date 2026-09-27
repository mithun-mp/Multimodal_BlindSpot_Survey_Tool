import os
import json
from blindspot.reporting.thesis_graphs import ThesisVisualizer

path = os.path.abspath('runs/exp_1790537272_6f4cc1/figures/fig01_prediction_distribution.png')
print('Target file:', path)
if os.path.exists(path):
    os.remove(path)
    print('Removed old file')
res = json.load(open('runs/exp_1790537272_6f4cc1/results.json'))
viz = ThesisVisualizer(os.path.dirname(path))
ret = viz.plot_model_prediction_distribution(res)
print('Generated:', ret, 'Exists now:', os.path.exists(ret), 'Size:', os.path.getsize(ret))

path11 = os.path.abspath('runs/exp_1790537272_6f4cc1/figures/fig11_model_agreement.png')
if os.path.exists(path11):
    os.remove(path11)
ret11 = viz.plot_model_agreement(res)
print('Generated 11:', ret11, 'Exists now:', os.path.exists(ret11), 'Size:', os.path.getsize(ret11))
