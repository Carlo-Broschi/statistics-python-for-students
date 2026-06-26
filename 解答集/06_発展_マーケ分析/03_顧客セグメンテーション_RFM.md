# 03_顧客セグメンテーション（RFM）― 解答例

> 本編: [06_発展_マーケ分析/03_顧客セグメンテーション_RFM.ipynb](https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/06_%E7%99%BA%E5%B1%95_%E3%83%9E%E3%83%BC%E3%82%B1%E5%88%86%E6%9E%90/03_%E9%A1%A7%E5%AE%A2%E3%82%BB%E3%82%B0%E3%83%A1%E3%83%B3%E3%83%86%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3_RFM.ipynb)

```python
# 問1: k=3
cust['c3'] = KMeans(n_clusters=3, random_state=0, n_init=10).fit_predict(X)
print(cust.groupby('c3')[['Recency','Frequency','Monetary']].mean().round(0))

# 問2: エルボー法
inertia = [KMeans(n_clusters=k, random_state=0, n_init=10).fit(X).inertia_ for k in range(1,9)]
plt.plot(range(1,9), inertia, marker='o'); plt.xlabel('k'); plt.ylabel('inertia'); plt.show()
# 折れ線の「ひじ」がkの目安（ここでは3〜4あたり）

# 問3: クラスタ×業界
print(pd.crosstab(cust['cluster'], cust['業界']))

# 問4: 離反候補（Recency最大のクラスタ）
churn = cust.groupby('cluster')['Recency'].mean().idxmax()
print(cust[cust['cluster']==churn]['顧客ID'].tolist()[:20])
```
