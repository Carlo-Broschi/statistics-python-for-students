import glob, json, sys, os
import nbformat
from nbformat import validate
from nbconvert.preprocessors import ExecutePreprocessor

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
nbs = sorted(glob.glob(f"{ROOT}/**/*.ipynb", recursive=True))

# 1) validate all
bad = 0
for p in nbs:
    nb = nbformat.read(p, as_version=4)
    try:
        validate(nb)
    except Exception as e:
        bad += 1; print("INVALID", p, e)
print(f"validated {len(nbs)} notebooks, invalid={bad}")

# 2) execute data-driven notebooks (skip Python基礎 = 意図的エラーあり)
to_run = [p for p in nbs if "01_Python基礎" not in p]
fails = []
for p in to_run:
    nb = nbformat.read(p, as_version=4)
    ep = ExecutePreprocessor(timeout=120, kernel_name="python3")
    workdir = os.path.dirname(p)
    try:
        ep.preprocess(nb, {"metadata": {"path": workdir}})
        print("OK  ", os.path.relpath(p, ROOT))
    except Exception as e:
        fails.append((p, str(e).splitlines()[-1] if str(e) else repr(e)))
        print("FAIL", os.path.relpath(p, ROOT), "->", str(e).splitlines()[-1][:160])
print("\n=== FAILS:", len(fails), "===")
