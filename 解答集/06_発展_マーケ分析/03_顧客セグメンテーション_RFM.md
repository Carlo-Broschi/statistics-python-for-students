# 03_顧客セグメンテーション（RFM）― 解答例（解説つき）

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
💡 クラスタは番号でなく「R/F/Mの平均プロフィール」で意味づけし、優良=維持・離反=掘り起こし のように施策を変える。
