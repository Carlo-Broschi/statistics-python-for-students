import nbformat, os
from nbconvert.preprocessors import ExecutePreprocessor
ROOT="/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
new=[
 "02_統計_4級/05_PPDACとグラフの読み方.ipynb",
 "02_統計_4級/06_時系列と場合の数.ipynb",
 "03_統計_3級/05_実験と条件付き確率.ipynb",
 "03_統計_3級/06_共分散・変動係数・正規近似.ipynb",
 "04_統計_2級/04_母分散・F検定・母比率の差.ipynb",
 "04_統計_2級/05_いろいろな確率分布とベイズ.ipynb",
 "04_統計_2級/06_重回帰分析.ipynb",
 "04_統計_2級/07_抽出法・実験計画・格差指標.ipynb",
]
for rel in new:
    p=os.path.join(ROOT,rel)
    nb=nbformat.read(p,as_version=4)
    try:
        ExecutePreprocessor(timeout=180,kernel_name="python3").preprocess(nb,{"metadata":{"path":os.path.dirname(p)}})
        print("OK  ",rel)
    except Exception as e:
        print("FAIL",rel,"->",str(e).splitlines()[-1][:200])
