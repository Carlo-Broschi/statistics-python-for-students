# 06_pandas入門 ― 解答例

> 出典ノート: `01_Python基礎/06_pandas入門.ipynb`　／　[本編ノートを開く](https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/01_Python%E5%9F%BA%E7%A4%8E/06_pandas%E5%85%A5%E9%96%80.ipynb)

```python
print(df['英語'].mean(), df['英語'].max())
print(len(df[df['国語'] >= 80]))
print(df.groupby('クラス')['勉強時間'].mean())
print(df.sort_values('数学', ascending=False)[['生徒ID','数学']].head())
```
