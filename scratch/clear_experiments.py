import os
import shutil
from pathlib import Path

def clear_all_experiments():
    root = Path(__file__).resolve().parent.parent
    print(f"Clearing experiment data in: {root}")

    # 1. Clear runs directory
    runs_dir = root / "runs"
    if runs_dir.exists():
        count = 0
        for item in list(runs_dir.iterdir()):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                count += 1
            except Exception as e:
                print(f"Warning removing {item.name}: {e}")
        print(f"Cleared runs/ directory: removed {count} experiment run folders.")
        runs_dir.mkdir(exist_ok=True)
    else:
        runs_dir.mkdir(exist_ok=True)
        print("Created empty runs/ directory.")

    # 2. Clear audit_reports directory
    audit_dir = root / "audit_reports"
    if audit_dir.exists():
        count = 0
        for item in list(audit_dir.iterdir()):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                count += 1
            except Exception as e:
                print(f"Warning removing {item.name}: {e}")
        print(f"Cleared audit_reports/ directory: removed {count} items.")
        audit_dir.mkdir(exist_ok=True)
    else:
        audit_dir.mkdir(exist_ok=True)
        print("Created empty audit_reports/ directory.")

    # 3. Clear temporary scratch debug dirs
    scratch_dir = root / "scratch"
    for scratch_temp in ["debug_figs", "debug_vis", "debug_figs.py", "debug_plots.py"]:
        p = scratch_dir / scratch_temp
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()
                print(f"Removed scratch/{scratch_temp}")
            except Exception as e:
                print(f"Warning removing scratch/{scratch_temp}: {e}")

    # 4. Truncate log file
    log_file = root / "logs" / "blindspot.log"
    if log_file.exists():
        try:
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("")
            print("Reset logs/blindspot.log")
        except Exception as e:
            print(f"Warning truncating log: {e}")

    print("=" * 60)
    print("ALL EXPERIMENT DATA AND REPORT FILES SUCCESSFULLY CLEARED!")
    print("=" * 60)

if __name__ == "__main__":
    clear_all_experiments()
