import sys
import os

workspace = r"c:\Dev\Projects\BlinkSpot-main"
if workspace not in sys.path:
    sys.path.insert(0, workspace)

from streamlit.testing.v1 import AppTest

print("=== RUNNING AppTest ON blindspot/app.py ===")
try:
    at = AppTest.from_file(os.path.join(workspace, "blindspot", "app.py"), default_timeout=30)
    at.run()
    print("Initial run completed.")
    if at.exception:
        print(f"EXCEPTION ON INITIAL RUN: {at.exception}")
        for ex in at.exception:
            print("  Exception detail:", ex.value)
    else:
        print("Initial run SUCCESS without exceptions!")

    from blindspot.ui.shell import PRIMARY_DOMAINS, DOMAIN_SUBPAGES
    all_pages = [
        "Overview", "Experiment", "Probes", "Live Run", "Console",
        "Comparison", "Explainability", "Failure Analysis",
        "Reports", "Run History", "Models", "System"
    ]
    
    for page in all_pages:
        print(f"\n--- Testing navigation to page: {page} ---")
        try:
            at.session_state["current_page"] = page
            # Also set active_domain accordingly
            for domain, subpages in DOMAIN_SUBPAGES.items():
                if page in subpages:
                    at.session_state["active_domain"] = domain
                    break
            at.run()
            if at.exception:
                print(f"FAILED on page '{page}':")
                for ex in at.exception:
                    print(" ", ex.value)
            else:
                print(f"Page '{page}' rendered cleanly!")
        except Exception as e:
            print(f"Exception while switching to '{page}': {e}")

except Exception as e:
    import traceback
    print(f"AppTest failed to initialize or run: {e}")
    traceback.print_exc()
