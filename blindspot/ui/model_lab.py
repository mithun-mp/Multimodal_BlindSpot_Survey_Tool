"""
Model Lab: Model Registry Catalog and Verification Console.
"""
import streamlit as st
from blindspot.models.registry import ModelRegistry


def render_model_lab():
    st.title("Model Lab: Catalog & Verification")
    st.markdown("Browse curated model presets and verify custom Hugging Face classification models.")

    registry = ModelRegistry()

    st.subheader("Curated Model Presets")
    presets = registry.list_presets(task=None)
    for p in presets:
        task_str = p.get("task", "SENTIMENT")
        badge = "🟢 SENTIMENT" if task_str == "SENTIMENT" else f"⚠️ {task_str}"
        with st.expander(f"**{p['name']}** — {badge} (`{p['model_id']}`)", expanded=p.get("default", False)):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Task**: `{task_str}` | **Classes**: {p['num_classes']} ({', '.join(p['label_names'])})")
            with col2:
                st.write(f"**Architecture**: `{p['architecture']}`")
            with col3:
                params = f"{p['parameters_millions']}M" if p.get('parameters_millions') else "Unknown"
                st.write(f"**Parameters**: {params}")
            st.markdown(f"*{p['description']}*")

    st.markdown("---")
    st.subheader("Verify Custom Hugging Face Model")
    st.markdown("Inspect metadata and class labels for any public Hugging Face repository prior to running an audit.")

    with st.form("verify_model_form"):
        model_input = st.text_input(
            "Model ID / Path:",
            value="cardiffnlp/twitter-roberta-base-sentiment-latest",
            placeholder="e.g. distilbert-base-uncased-finetuned-sst-2-english",
        )
        verify_btn = st.form_submit_button("Verify Model Compatibility")

    if verify_btn and model_input.strip():
        with st.spinner(f"Verifying '{model_input}'..."):
            result = registry.verify_model(model_input.strip())
            if result.get("verified"):
                st.success(f"Model `{model_input}` verified successfully!")
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Num Classes", result["num_classes"])
                    st.write(f"**Labels**: {', '.join(result['label_names'])}")
                with c2:
                    st.metric("Architecture", result["architecture"])
            else:
                st.error(f"Verification failed: {result.get('error')}")
