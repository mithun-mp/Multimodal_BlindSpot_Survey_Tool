import sys
import os

workspace = r"c:\Dev\Projects\BlinkSpot-main"
if workspace not in sys.path:
    sys.path.insert(0, workspace)

from streamlit.testing.v1 import AppTest
from blindspot.perturbations.shared import SharedProbeGenerator

print("=== TESTING INTERACTIVE USER FLOWS ===")

# Test 1: Empty state -> Generate probes in Probe Lab -> Stage Probes
at = AppTest.from_file(os.path.join(workspace, "blindspot", "app.py"), default_timeout=30)
at.run()

print("\n1. Navigating to Probes...")
at.session_state["current_page"] = "Probes"
at.session_state["active_domain"] = "Probes"
at.run()
assert not at.exception, f"Exception in Probes: {at.exception}"
print("   Probes view rendered cleanly.")

# Test 2: Stage probes manually into session_state and navigate to Experiment
print("\n2. Staging probes into session_state and navigating to Experiment...")
gen = SharedProbeGenerator()
probe_set = gen.generate_probes(["The film was brilliant and captivating."])
at.session_state["staged_probe_set"] = probe_set
at.session_state["current_page"] = "Experiment"
at.session_state["active_domain"] = "Experiment"
at.run()
assert not at.exception, f"Exception in Experiment with staged probes: {at.exception}"
print("   Experiment view rendered cleanly with staged probes.")

# Test 3: Navigate to Comparison with active results
print("\n3. Loading a real run into session_state and testing Comparison, Explainability, Failure Analysis...")
from blindspot.storage.run_store import RunStore
store = RunStore()
latest_id = store.get_latest_run_id()
if latest_id:
    run_data = store.load_run(latest_id)
    at.session_state["active_results"] = run_data.get("results")
    at.session_state["active_experiment_id"] = latest_id
    
    # Test Comparison
    at.session_state["current_page"] = "Comparison"
    at.session_state["active_domain"] = "Analyze"
    at.run()
    assert not at.exception, f"Exception in Comparison with data: {at.exception}"
    print("   Comparison view rendered cleanly with loaded data.")
    
    # Test Explainability
    at.session_state["current_page"] = "Explainability"
    at.session_state["active_domain"] = "Analyze"
    at.run()
    assert not at.exception, f"Exception in Explainability with data: {at.exception}"
    print("   Explainability view rendered cleanly with loaded data.")

    # Test Failure Analysis
    at.session_state["current_page"] = "Failure Analysis"
    at.session_state["active_domain"] = "Analyze"
    at.run()
    assert not at.exception, f"Exception in Failure Analysis with data: {at.exception}"
    print("   Failure Analysis view rendered cleanly with loaded data.")

    # Test Reports
    at.session_state["current_page"] = "Reports"
    at.session_state["active_domain"] = "Reports"
    at.run()
    assert not at.exception, f"Exception in Reports with data: {at.exception}"
    print("   Reports view rendered cleanly with loaded data.")

    # Test Run History
    at.session_state["current_page"] = "Run History"
    at.session_state["active_domain"] = "Reports"
    at.run()
    assert not at.exception, f"Exception in Run History with data: {at.exception}"
    print("   Run History view rendered cleanly with loaded data.")

print("\nALL USER FLOW TESTS PASSED COMPLETELY WITH 0 EXCEPTIONS!")
