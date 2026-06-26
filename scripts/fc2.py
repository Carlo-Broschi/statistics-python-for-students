import sys, nbformat, glob, os
from nbformat import validate
from nbconvert.preprocessors import ExecutePreprocessor
ROOT='/Users/carlobroschi_imac/Workspace/Dev/Education_Python'
nbs=sorted(glob.glob(f'{ROOT}/**/*.ipynb',recursive=True))
bad=0
for p in nbs:
    try: validate(nbformat.read(p,as_version=4))
    except Exception as e: bad+=1; print('INVALID',p,e,flush=True)
print('VALIDATE invalid=',bad,'/',len(nbs),flush=True)
targets=['04_統計_2級/03_カイ二乗と分散分析.ipynb','05_実践_BtoBマーケ/03_ABテストとKPI.ipynb',
 '04_統計_2級/06_重回帰分析.ipynb','04_統計_2級/07_抽出法・実験計画・格差指標.ipynb',
 '03_統計_3級/06_共分散・変動係数・正規近似.ipynb','05_実践_BtoBマーケ/01_売上データ分析.ipynb',
 '02_統計_4級/05_PPDACとグラフの読み方.ipynb','02_統計_4級/06_時系列と場合の数.ipynb']
for rel in targets:
    p=os.path.join(ROOT,rel); nb=nbformat.read(p,as_version=4)
    try:
        ExecutePreprocessor(timeout=180,kernel_name='python3').preprocess(nb,{'metadata':{'path':os.path.dirname(p)}})
        print('OK  ',rel,flush=True)
    except Exception as e:
        print('FAIL',rel,'->',str(e).splitlines()[-1][:140],flush=True)
print('DONE',flush=True)
