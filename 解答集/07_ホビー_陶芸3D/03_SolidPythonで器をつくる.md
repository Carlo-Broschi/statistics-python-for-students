# 03_SolidPythonで器をつくる ― 解答例

> 出典ノート: `07_ホビー_陶芸3D/03_SolidPythonで器をつくる.ipynb`　／　[本編ノートを開く](https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/07_%E3%83%9B%E3%83%93%E3%83%BC_%E9%99%B6%E8%8A%B83D/03_SolidPython%E3%81%A7%E5%99%A8%E3%82%92%E3%81%A4%E3%81%8F%E3%82%8B.ipynb)

```python
make_bowl(diameter=150, height=25, thickness=5).save_as_scad('kozara.scad')

for d in range(80, 161, 20):
    make_bowl(diameter=d, height=d*0.6).save_as_scad(f'bowl_{d}.scad')
```
