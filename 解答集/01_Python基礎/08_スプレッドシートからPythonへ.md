# 08_スプレッドシートからPythonへ ― 解答例（解説つき）

**問1. Webマーケ：チャネル別クリック数の合計**
```python
mk = pd.read_excel(xlsx, sheet_name='Webマーケ')
print(mk.groupby('チャネル')['クリック数'].sum())
```
💡 シートを指定して読み、`groupby('チャネル')` で合計。Excelのピボットと同じ集計。

**問2. 顧客：業界別の累計売上の平均**
```python
cust = pd.read_excel(xlsx, sheet_name='顧客')
print(cust.groupby('業界')['累計売上'].mean().round(0))
```
💡 `sum` を `mean` に変えるだけで「合計→平均」。

**問3. 結果をExcelに書き出す**
```python
result = cust.groupby('業界')['累計売上'].mean().round(0)
result.to_excel('業界別売上.xlsx')
```
💡 `to_excel` でそのままExcelファイルに。上司や同僚に渡しやすい。
