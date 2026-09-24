from setuptools import setup, find_packages

setup(
    name="blindspot",
    version="0.1.0",
    description="A Behavioral and Explainable-AI Framework for Auditing Text Classifiers",
    author="Ziya Fathima M P",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "transformers",
        "torch",
        "huggingface_hub",
        "spacy",
        "nltk",
        "lime",
        "shap",
        "pandas",
        "numpy",
        "scikit-learn",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "blindspot=blindspot.cli:main",
        ],
    },
)
