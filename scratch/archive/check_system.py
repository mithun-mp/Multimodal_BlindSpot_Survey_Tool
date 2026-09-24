import py_compile
import os
import sys
import importlib
import traceback

workspace = r"c:\Dev\Projects\BlinkSpot-main"
if workspace not in sys.path:
    sys.path.insert(0, workspace)

print("=== 1. CHECKING SYNTAX FOR ALL .PY FILES ===")
syntax_errors = []
for root, dirs, files in os.walk(workspace):
    if any(x in root for x in [".git", "__pycache__", "venv", ".agents", ".gemini"]):
        continue
    for f in files:
        if f.endswith(".py"):
            path = os.path.join(root, f)
            try:
                py_compile.compile(path, doraise=True)
            except py_compile.PyCompileError as e:
                syntax_errors.append((path, str(e)))

if syntax_errors:
    print(f"FAILED: Found {len(syntax_errors)} syntax errors:")
    for path, err in syntax_errors:
        print(f"  {path}: {err}")
else:
    print("SUCCESS: 0 syntax errors found.")

print("\n=== 2. CHECKING IMPORT OF ALL MODULES IN BLINDSPOT ===")
import_errors = []
for root, dirs, files in os.walk(os.path.join(workspace, "blindspot")):
    if "__pycache__" in root:
        continue
    for f in files:
        if f.endswith(".py"):
            rel_dir = os.path.relpath(root, workspace)
            if f == "__init__.py":
                mod_name = rel_dir.replace(os.path.sep, ".")
            else:
                mod_name = os.path.join(rel_dir, f[:-3]).replace(os.path.sep, ".")
            try:
                importlib.import_module(mod_name)
            except Exception as e:
                import_errors.append((mod_name, str(e), traceback.format_exc()))

if import_errors:
    print(f"FAILED: Found {len(import_errors)} import errors:")
    for mod, err, tb in import_errors:
        print(f"  [ERROR] {mod}: {err}")
        print(tb)
else:
    print("SUCCESS: All blindspot modules imported cleanly.")

print("\n=== 3. CHECKING ALL PRESET MODELS LOAD/INIT ===")
from blindspot.models.registry import ModelRegistry
try:
    registry = ModelRegistry()
    presets = registry.list_presets()
    print(f"Registered presets ({len(presets)}): {presets}")
    for p in presets:
        meta = registry.get_metadata(p)
        print(f"  - {p}: {meta.name if meta else 'No meta'} ({meta.task if meta else ''})")
except Exception as e:
    print(f"FAILED to check presets: {e}")
    traceback.print_exc()

print("\n=== 4. CHECKING STREAMLIT UI PAGE FUNCTIONS ===")
# Try importing each UI page and inspect what functions it defines
ui_pages = [
    "blindspot.ui.overview",
    "blindspot.ui.experiment_lab",
    "blindspot.ui.probe_lab",
    "blindspot.ui.live_run",
    "blindspot.ui.comparison",
    "blindspot.ui.explanation_lab",
    "blindspot.ui.failure_lab",
    "blindspot.ui.reports_view",
    "blindspot.ui.run_history",
    "blindspot.ui.model_lab",
    "blindspot.ui.system_monitor",
    "blindspot.ui.console",
    "blindspot.ui.shell",
]

for p in ui_pages:
    try:
        mod = importlib.import_module(p)
        funcs = [attr for attr in dir(mod) if attr.startswith("render_") and callable(getattr(mod, attr))]
        print(f"  {p}: {funcs}")
    except Exception as e:
        print(f"  [ERROR] importing {p}: {e}")
        traceback.print_exc()

print("\nDONE.")
