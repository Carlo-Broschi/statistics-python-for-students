import json, glob, os, hashlib, tempfile, shutil
import nbformat
from nbformat import validate
from nbconvert.preprocessors import ExecutePreprocessor
ROOT="/Users/carlobroschi_imac/Workspace/Dev/Education_Python"

# 1) validate all
nbs=sorted(glob.glob(f"{ROOT}/**/*.ipynb",recursive=True))
bad=0
for p in nbs:
    try: validate(nbformat.read(p,as_version=4))
    except Exception as e: bad+=1; print("INVALID",p,e)
print(f"[validate] {len(nbs)} notebooks, invalid={bad}")

# 2) execute a representative sample locally (setup cell must be a no-op)
sample=["02_統計_4級/01_データの種類と度数分布.ipynb",
        "05_実践_BtoBマーケ/03_ABテストとKPI.ipynb",
        "01_Python基礎/07_matplotlib入門.ipynb",
        "03_統計_3級/03_確率分布.ipynb",
        "07_ホビー_陶芸3D/03_SolidPythonで器をつくる.ipynb"]
for rel in sample:
    p=os.path.join(ROOT,rel); nb=nbformat.read(p,as_version=4)
    try:
        ExecutePreprocessor(timeout=180,kernel_name="python3").preprocess(nb,{"metadata":{"path":os.path.dirname(p)}})
        print("[exec] OK  ",rel)
    except Exception as e:
        print("[exec] FAIL",rel,"->",str(e).splitlines()[-1][:150])

# 3) data-gen equality: extract generator from DATA_SETUP, run into temp, compare md5 with committed
src=open("colabify.py",encoding="utf-8").read()
# pull the inner generation block by re-deriving: easier—run the committed gen path used originally
# Here we re-run the exact inner code by importing it indirectly: replicate by exec of a trimmed cell.
