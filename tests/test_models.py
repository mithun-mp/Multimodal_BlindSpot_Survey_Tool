import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import numpy as np
from blindspot.models.huggingface_wrapper import HuggingFaceWrapper

def test_huggingface_wrapper():
    model = HuggingFaceWrapper("distilbert-base-uncased-finetuned-sst-2-english")
    assert model.labels is not None
    assert len(model.labels) >= 2

    probas = model.predict_proba(["This film is wonderful!"])
    assert isinstance(probas, np.ndarray)
    assert probas.shape == (1, len(model.labels))
    assert np.isclose(np.sum(probas[0]), 1.0, atol=1e-3)

    preds = model.predict(["This is awful."])
    assert len(preds) == 1
    assert preds[0] in model.labels
