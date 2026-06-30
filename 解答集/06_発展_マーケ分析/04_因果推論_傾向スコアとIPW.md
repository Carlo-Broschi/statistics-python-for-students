# 04_因果推論（傾向スコア・IPW） ― 解答例（解説つき）

```python
import statsmodels.formula.api as smf
import numpy as np

# 問1: 関心度を入れない定数モデルにすると IPW は素朴な差に戻る
ps2 = smf.logit('ウェビナー ~ 1', data=df).fit(disp=0)
e2 = ps2.predict(df)                         # 全員同じ＝全体の参加率
t, y = df['ウェビナー'].values, df['受注'].values
mu1 = ((t/e2)*y).sum()/(t/e2).sum(); mu0 = (((1-t)/(1-e2))*y).sum()/((1-t)/(1-e2)).sum()
print('定数モデルのIPW:', round(mu1-mu0, 3), ' / 素朴な差:', round(naive_diff, 3))
# → ほぼ一致。交絡（関心度）を入れないと調整にならず、素朴な比較と同じになる。

# 問2: 重みの最大値（positivityの崩れチェック）
w1 = t/df['ps'].values; w0 = (1-t)/(1-df['ps'].values)
print('最大の重み w1:', round(w1.max(),1), ' w0:', round(w0.max(),1))
# → 極端に大きい重みが無ければOK。あると少数の個体が結果を支配して不安定。
```

**問3（考察）**：未観測交絡の例 ＝「営業担当の熱量」「既存の取引関係の深さ」「決裁者の関与度」など。これらが参加と受注の両方に効いていても、データに無ければ傾向スコアに入れられず、IPWでも調整できない。だから観察データの因果推論は「測れている交絡」前提の慎重な主張になる。
