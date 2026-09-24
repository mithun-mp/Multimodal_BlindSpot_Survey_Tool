"""
Run History: Persistent Research Archive & Experiment Inspector.
Provides tabular audit logs, detailed read-only run inspection, artifact downloads,
and one-click session reloading.
"""
import streamlit as st
import time
import os
import pandas as pd
from typing import Dict, Any, List

from blindspot.storage.run_store import RunStore
from blindspot.ui.components import render_empty_state
from blindspot.execution.runner import ExperimentRunner


def render_run_history():
    st.markdown(
        """
        <div style="margin-bottom:16px;">
            <div style="font-size:1.3rem; font-weight:700; color:#f1f5f9; letter-spacing:0.02em;">
                RESEARCH RUN ARCHIVE
            </div>
            <div style="color:#94a3b8; font-size:0.85rem;">
                Browse, inspect, and reload previous auditing experiments persisted on the local filesystem.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    store = RunStore()
    runs = store.list_runs()

    if not runs:
        clicked = render_empty_state(
            title="NO PERSISTED RUNS FOUND",
            message="No prior experiment runs were found in the `runs/` directory. Complete an audit experiment to populate the archive.",
            action_label="CONFIGURE FIRST AUDIT",
            action_key="hist_empty_to_exp",
        )
        if clicked:
            st.session_state["current_page"] = "Experiment"
            st.rerun()
        return

    # Table Overview
    table_rows = []
    for r in runs:
        exp_id = r.get("experiment_id", "unknown")
        exp_name = r.get("experiment_name") or exp_id
        status = r.get("status", "unknown").upper()
        created_at = r.get("created_at", 0)
        date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(created_at)) if created_at else "--"
        models = r.get("models", [])
        num_models = len(models)
        num_probes = r.get("num_probes")
        probes_str = str(num_probes) if num_probes is not None else "--"
        dur = r.get("total_duration_sec", 0.0)
        dur_str = f"{dur:.1f}s" if dur else "--"

        table_rows.append({
            "Experiment Title": exp_name,
            "Run ID": exp_id,
            "Date": date_str,
            "Models": str(num_models),
            "Probes": probes_str,
            "Status": status,
            "Duration": dur_str,
            "Model IDs": ", ".join(models),
        })

    df_runs = pd.DataFrame(table_rows)
    st.dataframe(df_runs[["Experiment Title", "Run ID", "Date", "Models", "Probes", "Status", "Duration"]], use_container_width=True, hide_index=True)

    st.markdown("---")

    # Detailed Run Inspector & Reloader
    st.subheader("Run Inspector & Session Loader")
    exp_ids = [r.get("experiment_id", "unknown") for r in runs]

    selected_exp_id = st.selectbox(
        "Select Experiment to Inspect:",
        options=exp_ids,
        format_func=lambda x: f"{store.get_run_title(x)} ({x})",
        key="hist_sel_exp",
    )

    if selected_exp_id:
        try:
            run_data = store.load_run(selected_exp_id)
            meta = run_data.get("metadata", {})
            config = run_data.get("config", {})
            results = run_data.get("results")

            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.caption(f"**Experiment Name:** {config.get('experiment_name', meta.get('experiment_name', 'Unnamed'))}")
            with col_m2:
                st.caption(f"**Status:** `{meta.get('status', 'complete').upper()}`")
            with col_m3:
                st.caption(f"**Total Probes:** `{meta.get('num_probes', '--')}`")
            with col_m4:
                st.caption(f"**Duration:** `{meta.get('total_duration_sec', 0):.2f}s`")

            st.caption(f"**Evaluated Models:** {', '.join(meta.get('models', []))}")

            run_status = str(meta.get("status", "completed")).lower()
            is_resumable = run_status in ("incomplete", "failed", "cancelled", "running") or not results

            col_btn_load, col_btn_resume, col_btn_down = st.columns([2, 2, 2])
            with col_btn_load:
                if st.button("Load Run Into Session", type="primary" if not is_resumable else "secondary", use_container_width=True, key=f"btn_load_{selected_exp_id}"):
                    if results:
                        st.session_state["active_results"] = results
                        st.session_state["active_experiment_id"] = selected_exp_id
                        st.session_state["active_experiment_title"] = config.get("experiment_name") or store.get_run_title(selected_exp_id)
                        st.success(f"Experiment '{st.session_state['active_experiment_title']}' [{selected_exp_id}] loaded into active session! Navigate to Model Comparison or Reports.")
                    else:
                        st.warning("No complete results.json payload exists for this run. You can resume this run using the RESUME button.")

            with col_btn_resume:
                if is_resumable:
                    if st.button("▶ RESUME RUN", type="primary", use_container_width=True, key=f"btn_resume_{selected_exp_id}"):
                        try:
                            resumed_runner = ExperimentRunner.resume_run(selected_exp_id)
                            resumed_runner.run_async()
                            st.session_state["active_runner"] = resumed_runner
                            st.session_state["active_experiment_id"] = selected_exp_id
                            st.session_state["active_experiment_title"] = config.get("experiment_name") or store.get_run_title(selected_exp_id)
                            st.session_state["active_results"] = None
                            st.session_state["current_page"] = "Live Run"
                            st.success(f"Resuming experiment '{st.session_state['active_experiment_title']}' [{selected_exp_id}]...")
                            st.rerun()
                        except Exception as resume_err:
                            st.error(f"Failed to resume run: {resume_err}")
                else:
                    st.button("Run Fully Completed", disabled=True, use_container_width=True, key=f"btn_done_{selected_exp_id}")

            with col_btn_down:
                run_dir = store.get_run_dir(selected_exp_id)
                summary_md_path = os.path.join(run_dir, "reports", "summary.md")
                if os.path.exists(summary_md_path):
                    with open(summary_md_path, "r", encoding="utf-8") as f:
                        md_content = f.read()
                    st.download_button(
                        label="Download Markdown Report",
                        data=md_content,
                        file_name=f"{selected_exp_id}_summary.md",
                        mime="text/markdown",
                        use_container_width=True,
                    )

            col_act_archive, col_act_del = st.columns([1, 1])
            with col_act_archive:
                if st.button("📦 Archive Run (Preserve Data)", key=f"btn_arch_{selected_exp_id}", use_container_width=True):
                    try:
                        arch_path = store.archive_run(selected_exp_id)
                        st.success(f"Run '{selected_exp_id}' safely archived.")
                        st.rerun()
                    except Exception as err:
                        st.error(f"Archive failed: {err}")

            with col_act_del:
                with st.expander("🗑️ Permanent Deletion (Requires Confirmation)", expanded=False):
                    st.warning(f"Are you sure you want to delete `{selected_exp_id}`? Historical data is never deleted automatically.")
                    confirm_check = st.checkbox("Confirm permanent deletion of this run", key=f"del_confirm_{selected_exp_id}")
                    if st.button("CONFIRM PERMANENT DELETION", type="secondary", disabled=not confirm_check, key=f"btn_del_exec_{selected_exp_id}"):
                        try:
                            store.delete_run(selected_exp_id, confirmation=True)
                            st.success(f"Run '{selected_exp_id}' permanently deleted.")
                            st.rerun()
                        except Exception as err:
                            st.error(f"Deletion failed: {err}")

            if results:
                with st.expander("Inspect Raw Results Metadata Payload", expanded=False):
                    st.json(meta)

        except Exception as e:
            st.error(f"Failed to load experiment '{selected_exp_id}': {e}")
