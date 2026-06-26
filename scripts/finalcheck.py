import nbformat, glob, os
from nbformat import validate
from nbconvert.preprocessors import ExecutePreprocessor
ROOT='/Users/carlobroschi_imac/Workspace/Dev/Education_Python'
nbs=sorted(glob.glob(f'{ROOT}/**/*.ipynb',recursive=True))
bad=0
for p in nbs:
    try: validate(nbformat.read(p,as_version=4))
    except Exception as e: bad+=1; print('INVALID',p,e)
print('VALIDATE invalid=',bad,'/',len(nbs))
fails=0
for p in nbs:
    b=os.path.basename(p)
    if '01_Pythonをはじめよう' in b or 'FreeCAD' in b or 'Blender' in b: continue
    nb=nbformat.read(p,as_version=4)
    try:
        ExecutePreprocessor(timeout=180,kernel_name='python3').preprocess(nb,{'metadata':{'path':os.path.dirname(p)}})
    except Exception as e:
        fails+=1; print('FAIL',os.path.relpath(p,ROOT),'->',str(e).splitlines()[-1][:140])
print('EXEC fails=',fails)
