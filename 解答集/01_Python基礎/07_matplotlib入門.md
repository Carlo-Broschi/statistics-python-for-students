# 07_matplotlib入門 ― 解答例

> 出典ノート: `01_Python基礎/07_matplotlib入門.ipynb`　／　[本編ノートを開く](https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/01_Python%E5%9F%BA%E7%A4%8E/07_matplotlib%E5%85%A5%E9%96%80.ipynb)

```python
plt.hist(df['英語'], bins=10, edgecolor='white'); plt.show()
plt.scatter(df['勉強時間'], df['数学'], alpha=0.5); plt.show()
df.groupby('クラス')['英語'].mean().plot(kind='bar'); plt.show()
```
