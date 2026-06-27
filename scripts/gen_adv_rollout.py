# -*- coding: utf-8 -*-
"""発展マーケ3冊を見本基準に底上げ（増築方式）。タイトルはバッジ内包なので🎯を別セルで追加。"""
import json, os
ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
HELPER = ("# 採点用の関数を実行（答え合わせに使うだけ）\n"
          "def _check(name, got, want, tol=1e-2):\n"
          "    if got is None:\n"
          "        print(f'⬜ {name}: まだ入力されていません（ans を埋めてね）'); return\n"
          "    ok = abs(got - want) <= tol\n"
          "    print(('✅ 正解！ ' if ok else '❌ もう一度 ') + f'{name}: あなたの答え = {got}')")
CHECK_HEADER = ("## 🧠 確認テスト（自動採点）\n\n"
                "`ans = None` を**自分の計算で置き換えて実行**すると、その場で正誤が出ます（答えは表示されません）。")
def md(t): return {"cell_type":"markdown","metadata":{},"source":t}
def code(t): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":t}

NB = {
"01_ドライバー分析_回帰.ipynb":{
 "obj":"## 🎯 この章でできるようになること\n"
   "- 重回帰とロジスティック回帰を使い分けられる\n"
   "- オッズ比で「受注を左右する要因」を読める\n"
   "- 受注確率を予測して施策に使える\n\n"
   "**前提**：統計2級06（重回帰）　/　**所要**：約35分　/　**レベル**：発展（準1級〜実務）",
 "misc":"> ⚠️ **よくある間違い**：受注は0/1なので**直線回帰は不適**（確率が0〜1をはみ出す）。"
        "→ ロジスティック回帰。また回帰で関係が出ても、無作為化した実験でない限り**因果**とは言い切れない。",
 "checks":[code("import numpy as np\n# Q1: ロジスティック回帰の係数が 0.7 のとき、オッズ比 exp(係数) を ans に\n"
                "ans = None   # 例: np.exp(0.7)\n_check('Q1 オッズ比', ans, np.exp(0.7))"),
           code("import numpy as np\n# Q2: ロジスティックの予測確率 1/(1+e^-z)。z=0 のとき ans は？\n"
                "ans = None   # 例: 1/(1+np.exp(0))\n_check('Q2 予測確率(z=0)', ans, 1/(1+np.exp(0)))")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 重回帰 | 連続値を複数要因で予測 |\n| ロジスティック回帰 | 0/1（確率）を予測 |\n"
   "| オッズ | 起こる/起こらない の比 |\n| オッズ比 | exp(係数)。基準比 何倍なりやすいか |\n"
   "| 偏回帰係数 | 他を一定にしたときの効き目 |",
 "cheat":"# チートシート（回帰・ロジスティック）\nimport statsmodels.formula.api as smf\nimport numpy as np\n"
   "m = smf.logit('受注 ~ 商談金額 + C(獲得チャネル)', data=btob).fit(disp=0)\n"
   "print(np.exp(m.params).round(2))   # オッズ比（基準=Web広告）",
 "answer":"""# 01_ドライバー分析（回帰）― 解答例（解説つき）

```python
# 問1: チャネル別の平均単価
print(smf.ols('商談金額 ~ C(獲得チャネル)', data=btob).fit().params.round(0))

# 問2: 業界を加える
l2 = smf.logit('受注 ~ 商談金額 + C(獲得チャネル) + C(業界)', data=btob).fit(disp=0)
print(l2.prsquared)   # 元(≈0.089)とほぼ同じ → 業界は受注にあまり効かない

# 問3: テレアポのオッズ比
import numpy as np
print(np.exp(logit.params['C(獲得チャネル)[T.テレアポ]']))   # ≈1.4倍

# 問4: 担当者別の受注率
print(btob.groupby('担当者')['受注'].mean().round(3))
```
💡 オッズ比が1より大きい＝基準(Web広告)より受注しやすい。係数のp値も見て「効いているか」を判断する。
""",
},
"02_時系列予測.ipynb":{
 "obj":"## 🎯 この章でできるようになること\n"
   "- トレンドと季節性を見分けられる\n"
   "- 移動平均・線形トレンド・Holt-Wintersで予測できる\n"
   "- 予測精度をMAE/MAPEで評価できる\n\n"
   "**前提**：統計4級06（時系列）　/　**所要**：約35分　/　**レベル**：発展（準1級〜実務）",
 "misc":"> ⚠️ **よくある間違い**：過去によく当てはまる＝未来に当たる、ではない（過学習）。"
        "未来は不確実なので、**学習/検証に分けて精度(MAPE)を確かめる**。線形トレンドだけだと季節性を無視します。",
 "checks":[code("# Q1: 売上が 100→120 になったときの増加率(%) を ans に\n"
                "ans = None   # (120-100)/100*100\n_check('Q1 増加率%', ans, (120-100)/100*100)"),
           code("# Q2: 予測100・実績110 のときの MAPE(%)=|予測−実績|/実績×100 を ans に\n"
                "ans = None   # abs(100-110)/110*100\n_check('Q2 MAPE%', ans, abs(100-110)/110*100)"),
           code("# Q3: [10,20,30] の3項移動平均（最後の値）を ans に\n"
                "ans = None   # (10+20+30)/3\n_check('Q3 移動平均', ans, (10+20+30)/3)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| トレンド | 長期の上下の流れ |\n| 季節性 | 周期的なくり返し |\n| 移動平均 | 数期間の平均でならす |\n"
   "| Holt-Winters | トレンド＋季節を学ぶ指数平滑 |\n| MAE/MAPE | 平均誤差/平均%誤差（小さいほど良い） |",
 "cheat":"# チートシート（時系列予測）\nfrom statsmodels.tsa.holtwinters import ExponentialSmoothing\n"
   "ts = kpi['売上'].astype(float)\n"
   "fit = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=12).fit()\n"
   "print(fit.forecast(3).round().tolist())   # 来3か月の予測",
 "answer":"""# 02_時系列予測 ― 解答例（解説つき）

```python
# 問1: 受注数を予測
w = kpi['受注数'].astype(float)
print(ExponentialSmoothing(w, trend='add', seasonal='add', seasonal_periods=12).fit().forecast(3).round().tolist())

# 問2: 乗法季節やトレンド無しと比較（MAPEで）
def mape_of(seasonal=None, trend='add'):
    m = ExponentialSmoothing(train, trend=trend, seasonal=seasonal, seasonal_periods=12).fit()
    p = m.forecast(6)
    return (abs(p.values-test.values)/test.values).mean()*100
print(mape_of('add'), mape_of('mul'), mape_of(None, None))

# 問3: 移動平均の比較
kpi['MA3']=kpi['売上'].rolling(3).mean()
kpi[['売上','MA3','移動平均12']].plot(); plt.show()

# 問4: 検証12か月
train2, test2 = ts[:-12], ts[-12:]
m4 = ExponentialSmoothing(train2, trend='add', seasonal='add', seasonal_periods=12).fit()
p4 = m4.forecast(12)
print((abs(p4.values-test2.values)/test2.values).mean()*100)
```
💡 MAPEが小さいモデルほど「当たる」。当てはまりの良さ(学習)ではなく検証での精度で選ぶ。
""",
},
"03_顧客セグメンテーション_RFM.ipynb":{
 "obj":"## 🎯 この章でできるようになること\n"
   "- RFM（最近性・頻度・金額）で顧客を数値化できる\n"
   "- 標準化→K-meansでセグメント分けできる\n"
   "- クラスタを解釈して施策につなげられる\n\n"
   "**前提**：統計3級01（標準化）　/　**所要**：約35分　/　**レベル**：発展（実務/DS）",
 "misc":"> ⚠️ **よくある間違い**：クラスタ番号そのものに意味はない（R/F/Mの平均で解釈する）。"
        "また**標準化を忘れる**と、金額(Monetary)の大きい単位に距離が引っ張られ、まともに分かれません。",
 "checks":[code("import pandas as pd\n# Q1: 基準2026-01-01・最終購入2025-12-02 のRecency(日数)を ans に\n"
                "ans = None   # (pd.Timestamp('2026-01-01')-pd.Timestamp('2025-12-02')).days\n"
                "_check('Q1 Recency', ans, (pd.Timestamp('2026-01-01')-pd.Timestamp('2025-12-02')).days)"),
           code("# Q2: 標準化 z=(x-平均)/標準偏差。x=20, 平均10, 標準偏差5 のとき ans は？\n"
                "ans = None   # (20-10)/5\n_check('Q2 z得点', ans, (20-10)/5)"),
           code("# Q3: 標準化後のデータの平均は？を ans に\n"
                "ans = None   # 0\n_check('Q3 標準化後の平均', ans, 0)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| RFM | 最近性・頻度・金額 |\n| 標準化 | 単位をそろえる(平均0・σ1) |\n"
   "| K-means | 似たデータをk個に分ける |\n| クラスタ | 分けられたグループ |\n"
   "| エルボー法 | 適切なkの目安 |\n| PCA | 次元を圧縮して可視化 |",
 "cheat":"# チートシート（セグメンテーション）\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.cluster import KMeans\n"
   "X = StandardScaler().fit_transform(cust[['Recency','Frequency','Monetary']])   # 標準化\n"
   "cust['cluster'] = KMeans(4, n_init=10, random_state=0).fit_predict(X)           # クラスタリング\n"
   "print(cust.groupby('cluster')[['Recency','Frequency','Monetary']].mean().round(0))",
 "answer":"""# 03_顧客セグメンテーション（RFM）― 解答例（解説つき）

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
""",
},
}

for fname, spec in NB.items():
    p = os.path.join(ROOT, "06_発展_マーケ分析", fname)
    nb = json.load(open(p, encoding="utf-8")); cells = nb["cells"]
    # 🎯 を「## 1.」の直前に
    if not any("🎯 この章" in "".join(c["source"]) for c in cells):
        for i,c in enumerate(cells):
            if c["cell_type"]=="markdown" and "".join(c["source"]).startswith("## 1."):
                cells.insert(i, md(spec["obj"])); break
    # 確認テスト
    if not any("🧠 確認テスト" in "".join(c["source"]) for c in cells):
        for i,c in enumerate(cells):
            if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith("---"):
                cells[i:i] = [md(spec["misc"]), md(CHECK_HEADER), code(HELPER)] + spec["checks"]; break
    # 用語集
    if not any("📒 用語集" in "".join(c["source"]) for c in cells):
        cells += [md(spec["glossary"]), code(spec["cheat"])]
    json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    ap = os.path.join(ROOT, "解答集/06_発展_マーケ分析", fname.replace(".ipynb",".md"))
    os.makedirs(os.path.dirname(ap), exist_ok=True)
    open(ap,"w",encoding="utf-8").write(spec["answer"])
    print("upgraded", fname, "->", len(cells), "cells")
print("=== 発展マーケ rollout done ===")
