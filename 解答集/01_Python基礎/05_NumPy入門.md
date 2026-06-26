# 05_NumPy入門 ― 解答例

> 出典ノート: `01_Python基礎/05_NumPy入門.ipynb`　／　[本編ノートを開く](https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/01_Python%E5%9F%BA%E7%A4%8E/05_NumPy%E5%85%A5%E9%96%80.ipynb)

```python
print(temps.mean(), temps.max(), temps.min(), temps.std())
print((temps >= 25).sum())
rng = np.random.default_rng(1)
print(rng.integers(1,7,size=1000).mean())
```
