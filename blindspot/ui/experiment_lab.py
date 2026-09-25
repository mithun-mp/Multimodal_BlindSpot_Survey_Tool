"""
Experiment Lab: Guided Multimodel Auditing Workflow.
Implements 01 PROBES (from Probe Workbench) -> 02 MODELS -> 03 EXECUTION -> 04 REVIEW
with technical cards, hardware-aware execution controls, and deterministic probe staging.
"""
import streamlit as st
from typing import List, Dict, Any, Optional

from blindspot.core.config import ExperimentConfig, PerformanceMode
from blindspot.models.registry import ModelRegistry
from blindspot.models.cache import ModelCache
from blindspot.execution.runner import ExperimentRunner
from blindspot.execution.resources import ResourceManager
from blindspot.ui.components import render_technical_model_card, render_probe_preview_card


def render_experiment_lab():
    st.markdown(
        """
        <div style="margin-bottom:18px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                EXPERIMENT CONFIGURATION
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Guided workstation workflow for multimodel behavioral and explainability auditing.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    registry = ModelRegistry()
    presets = registry.list_sentiment_models()
    cache = ModelCache.get_shared_cache()
    specs = ResourceManager.get_system_specs()
    host_device = specs.get("pytorch_device", "cpu")

    staged_probe_set = st.session_state.get("staged_probe_set")

    # ==========================================
    # 01 PROBES — VERIFIED PROBES FROM PROBE WORKBENCH
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:16px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">01 PROBES — VERIFIED PROBES FROM PROBE WORKBENCH</strong>
            <div style="color:#94a3b8; font-size:0.75rem;">Controlled linguistic perturbations curated and verified in the Probe Research Workbench.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    num_staged = len(staged_probe_set.probes) if staged_probe_set is not None else 0
    with st.expander(f"Inspect Staged Probes ({num_staged} stimuli)", expanded=False):
        if staged_probe_set is not None and staged_probe_set.probes:
            for p in staged_probe_set.probes:
                render_probe_preview_card(
                    probe_id=p.probe_id,
                    original_text=p.seed_text,
                    perturbed_text=p.perturbed_text,
                    perturbation_type=p.perturbation_type,
                    expected_semantic_effect=p.expected_semantic_effect,
                    expected_flip=p.expected_flip,
                )
        else:
            st.markdown(
                """
                <div style="color:#94a3b8; font-size:0.85rem; padding:8px 4px;">
                    No stimuli currently staged. Configure and stage probes in the <strong>Probes</strong> tab.
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ==========================================
    # 02 MODELS — TARGET CLASSIFIERS
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:16px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">02 MODELS — TARGET CLASSIFIERS</strong>
            <div style="color:#94a3b8; font-size:0.75rem;">Select verified model presets or register custom HuggingFace architectures.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Preset selection state
    if "selected_models" not in st.session_state:
        st.session_state["selected_models"] = ["distilbert-base-uncased-finetuned-sst-2-english"]

    col_m_act1, col_m_act2, col_m_spacer = st.columns([2, 2, 4])
    with col_m_act1:
        if st.button("Select All Presets", key="btn_select_all_presets", use_container_width=True):
            st.session_state["selected_models"] = [p["model_id"] for p in presets]
            st.rerun()
    with col_m_act2:
        if st.button("Deselect All", key="btn_deselect_all_presets", use_container_width=True):
            st.session_state["selected_models"] = []
            st.rerun()

    # Render technical cards for preset models
    cols = st.columns(2)
    selected_models_list = list(st.session_state["selected_models"])

    for idx, preset in enumerate(presets):
        m_id = preset["model_id"]
        is_checked = m_id in selected_models_list
        is_cached = cache.is_cached(m_id)

        with cols[idx % 2]:
            new_checked = st.checkbox(
                f"**{preset['name']}** (`{m_id.split('/')[-1]}`)",
                value=is_checked,
                key=f"chk_model_{m_id}",
            )
            if new_checked != is_checked:
                if new_checked and m_id not in selected_models_list:
                    selected_models_list.append(m_id)
                elif not new_checked and m_id in selected_models_list:
                    selected_models_list.remove(m_id)
                st.session_state["selected_models"] = selected_models_list
                st.rerun()

            render_technical_model_card(
                model_id=m_id,
                architecture=preset.get("architecture", "Transformer"),
                num_classes=preset.get("num_classes", 2),
                params_millions=preset.get("parameters_millions"),
                is_cached=is_cached,
                is_selected=new_checked,
                device=host_device,
            )

    # Custom Model Registration
    with st.expander("Register Custom HuggingFace Model", expanded=False):
        custom_m_input = st.text_input(
            "HuggingFace Repository Identifier:",
            placeholder="e.g. cardiffnlp/twitter-roberta-base-sentiment-latest",
            key="custom_hf_input",
        )
        if st.button("Add Model", key="btn_add_custom_model"):
            clean_cm = custom_m_input.strip()
            if clean_cm and clean_cm not in selected_models_list:
                selected_models_list.append(clean_cm)
                st.session_state["selected_models"] = selected_models_list
                st.success(f"Added '{clean_cm}' to target models.")
                st.rerun()

    # Explicit Model Count Confirmation
    num_selected_models = len(st.session_state["selected_models"])
    st.markdown(
        f"""
        <div style="background:#0b1329; border:1px solid #1e3a8a; border-radius:4px; padding:8px 12px; margin:10px 0 18px 0; font-size:0.8rem; font-family:monospace;">
            <span style="color:#60a5fa; font-weight:bold;">● {num_selected_models} model(s) selected:</span>
            <span style="color:#93c5fd; margin-left:6px;">All models will receive identical deterministic probes.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==========================================
    # 03 EXECUTION — WORKSTATION SCHEDULER & RUN PLAN
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:16px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">03 EXECUTION — WORKSTATION SCHEDULER & RUN PLAN</strong>
            <div style="color:#94a3b8; font-size:0.75rem;">Specify experiment title, inspect exact Run Plan, and launch the audit.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    perf_mode = "performance"
    xai_mode = "both"

    exp_title = st.text_input(
        "Experiment Title:",
        value="Multimodel Robustness Audit",
        key="txt_exp_title",
        help="Specify an informative title to label and identify this evaluation across reports and archives.",
    )

    # Compute Exact Run Plan
    num_seeds = len(staged_probe_set.seed_texts) if staged_probe_set is not None else 0
    total_probes_planned = len(staged_probe_set.probes) if staged_probe_set is not None else 0
    total_baselines = num_selected_models * num_seeds
    total_probe_inferences = num_selected_models * total_probes_planned
    total_model_calls = total_baselines + total_probe_inferences

    st.markdown(
        f"""
        <div style="background:#141824; border:1px solid #26334d; border-radius:6px; padding:12px 16px; margin:12px 0 16px 0; font-family:monospace; font-size:0.8rem;">
            <div style="color:#f1f5f9; font-weight:bold; margin-bottom:8px;">EXACT RUN PLAN (BASELINE + PROBES × MODELS):</div>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:8px; color:#94a3b8;">
                <div>Seed Sentences: <span style="color:#e2e8f0;">{num_seeds}</span></div>
                <div>Target Models: <span style="color:#e2e8f0;">{num_selected_models}</span></div>
                <div>Planned Probes: <span style="color:#38bdf8;">{total_probes_planned}</span></div>
                <div>Baseline Evals: <span style="color:#10b981;">{total_baselines}</span></div>
                <div>Probe Evals: <span style="color:#e2e8f0;">{total_probe_inferences}</span></div>
                <div>Total Predictions: <span style="color:#f59e0b; font-weight:bold;">{total_model_calls}</span></div>
                <div>Catalog Source: <span style="color:#38bdf8;">{'VERIFIED WORKBENCH' if staged_probe_set is not None else 'NONE (AWAITING STAGING)'}</span></div>
                <div>Explainer: <span style="color:#e2e8f0;">BOTH (LIME + SHAP)</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Active Runner check
    runner: Optional[ExperimentRunner] = st.session_state.get("active_runner")
    is_running = runner is not None and runner.status == "running"

    if is_running:
        st.warning(f"⚠️ Audit experiment is currently running [{runner.experiment_id}]. Step: {runner.current_step}")
        col_c1, col_c2 = st.columns([2, 3])
        with col_c1:
            if st.button("■ CANCEL ACTIVE RUN", key="btn_cancel_active_run", type="secondary", use_container_width=True):
                runner.cancel()
                st.warning("Cancellation requested.")
                st.rerun()
        with col_c2:
            if st.button("JUMP TO LIVE RUN MONITOR", key="btn_jump_live_run", type="primary", use_container_width=True):
                st.session_state["current_page"] = "Live Run"
                st.rerun()
    else:
        col_btn, col_empty = st.columns([2, 3])
        with col_btn:
            launch_clicked = st.button("▶ RUN EXPERIMENT", type="primary", use_container_width=True, key="btn_launch_exp")

        if launch_clicked:
            # Validations
            if not selected_models_list:
                st.error("Validation Error: Please select at least one target model in Step 02.")
                return

            if staged_probe_set is None:
                st.error("Validation Error: No probe catalog staged. Please curate and stage probes in the 'Probes' tab before launching.")
                return

            final_probe_set = staged_probe_set
            final_probe_ids = [p.probe_id for p in final_probe_set.probes]
            selected_ptypes = list(set(p.perturbation_type for p in final_probe_set.probes))

            # Construct ExperimentConfig
            config = ExperimentConfig(
                experiment_name=exp_title,
                model_ids=selected_models_list,
                seed_texts=final_probe_set.seed_texts,
                perturbation_types=selected_ptypes,
                explainer_type=xai_mode,
                performance_mode=PerformanceMode.from_str(perf_mode),
                selected_probe_set=final_probe_set,
                selected_probe_ids=final_probe_ids,
                sentence_types=getattr(final_probe_set, "sentence_types", {}),
            )

            new_runner = ExperimentRunner(config=config)
            new_runner.run_async()

            st.session_state["active_runner"] = new_runner
            st.session_state["active_experiment_id"] = new_runner.experiment_id
            st.session_state["active_experiment_title"] = exp_title
            st.session_state["active_results"] = None  # Clear stale results from prior runs

            st.success(f"Audit Experiment '{exp_title}' [{new_runner.experiment_id}] launched!")
            st.session_state["current_page"] = "Live Run"
            st.rerun()

    # ==========================================
    # 04 REVIEW & SHORTCUTS
    # ==========================================
    st.markdown(
        """
        <div style="background:#141824; border-left:3px solid #38bdf8; padding:8px 12px; margin:20px 0 10px 0;">
            <strong style="color:#38bdf8; font-family:monospace; font-size:0.9rem;">04 REVIEW — WORKSTATION JUMP GATES</strong>
            <div style="color:#94a3b8; font-size:0.75rem;">Direct navigation to telemetry, comparisons, and persistent research archives.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_rev1, col_rev2, col_rev3 = st.columns(3)
    with col_rev1:
        if st.button("Live Execution Monitor", key="rev_btn_live", use_container_width=True):
            st.session_state["current_page"] = "Live Run"
            st.rerun()
    with col_rev2:
        if st.button("Model Comparison", key="rev_btn_comp", use_container_width=True):
            st.session_state["current_page"] = "Comparison"
            st.rerun()
    with col_rev3:
        if st.button("Run History Archive", key="rev_btn_hist", use_container_width=True):
            st.session_state["current_page"] = "Run History"
            st.rerun()
