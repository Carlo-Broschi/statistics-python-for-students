# 03_ABテストとKPI ― 解答例

> 出典ノート: `05_実践_BtoBマーケ/03_ABテストとKPI.ipynb`　／　[本編ノートを開く](https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/05_%E5%AE%9F%E8%B7%B5_BtoB%E3%83%9E%E3%83%BC%E3%82%B1/03_AB%E3%83%86%E3%82%B9%E3%83%88%E3%81%A8KPI.ipynb)

```python
count = ab.groupby('グループ')['申込'].sum().values
nobs  = ab.groupby('グループ')['申込'].count().values
z, p = proportions_ztest(count, nobs)
print(z, p)   # カイ二乗のp値とほぼ一致
```
