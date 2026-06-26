# -*- coding: utf-8 -*-
import os, urllib.parse
from nbbuild import md, code, write_nb

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
GH = "https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/"
FOLDER = "07_発展_マーケ分析"

def badge(rel):
    u = "https://colab.research.google.com/github/Carlo-Broschi/statistics-python-for-students/blob/main/" + urllib.parse.quote(rel)
    return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({u})"

def ans_url(rel):
    return GH + urllib.parse.quote(rel)

SETUP = (
    "# === ① セットアップ（最初に実行してください）===\n"
    "import pandas as pd               # 表データ\n"
    "import numpy as np                # 数値計算\n"
    "import matplotlib.pyplot as plt   # グラフ描画\n"
    "import os\n"
    "plt.rcParams['axes.unicode_minus'] = False   # マイナス記号の文字化け防止\n"
    "# ローカルに無ければ公開リポジトリ(raw)から読み込む共通関数\n"
    "RAW = 'https://raw.githubusercontent.com/Carlo-Broschi/statistics-python-for-students/main/data/'\n"
    "def load(name):\n"
    "    p = f'../data/{name}'\n"
    "    return pd.read_csv(p) if os.path.exists(p) else pd.read_csv(RAW + name)\n"
)

INTRO_NOTE = ("> 🟢 Colab（ブラウザ）で実行できます。**最初に「① セットアップ」セルを実行**してください。\n"
              "> 📌 **発展編（統計検定2級の先：準1級〜実務/データサイエンス）**。scikit-learn・statsmodels を使います"
              "（Colabは導入済み。ローカルは `uv add scikit-learn statsmodels`）。")

# =====================================================================
# 01 ドライバー分析（回帰・ロジスティック回帰）
# =====================================================================
rel = f"{FOLDER}/01_ドライバー分析_回帰.ipynb"
ans_rel = f"解答集/{FOLDER}/01_ドライバー分析_回帰.md"
cells = [
    md(f"{badge(rel)}\n\n# 発展マーケ-01. ドライバー分析（重回帰・ロジスティック回帰）\n\n"
       f"{INTRO_NOTE}\n\n"
       "「**何が受注を左右しているか**」を回帰で定量化します。\n"
       "受注は 0/1 なので、確率を扱える **ロジスティック回帰** が主役です。"),
    code(SETUP + "btob = load('sales_btob.csv')   # BtoB商談データ\nbtob.head()"),
    md("## 1. ウォームアップ：重回帰で「商談金額」を業界で説明\n\n"
       "質的変数（業界）はダミー変数にして投入します（`C(業界)`）。"),
    code("import statsmodels.formula.api as smf            # 回帰\n"
         "m = smf.ols('商談金額 ~ C(業界)', data=btob).fit()  # 業界で商談金額を説明\n"
         "print('決定係数 R^2:', round(m.rsquared, 3))\n"
         "print(m.params.round(0))   # 基準業界との金額差（偏回帰係数）"),
    md("## 2. ロジスティック回帰：受注(0/1)の要因\n\n"
       "受注は2値なので直線回帰は不適。**ロジスティック回帰**は「受注する確率」を0〜1で扱えます。"),
    code("logit = smf.logit('受注 ~ 商談金額 + C(獲得チャネル)', data=btob).fit()  # 受注の要因を推定\n"
         "print('pseudo R^2:', round(logit.prsquared, 3))\n"
         "print(logit.params.round(3))   # 係数（プラスほど受注しやすい）"),
    md("## 3. オッズ比で読む（係数を直感的に）\n\n"
       "係数を `exp()` すると **オッズ比**。「基準チャネル(Web広告)に比べ受注オッズが何倍か」を表します。"),
    code("odds = np.exp(logit.params).round(2)   # 係数→オッズ比\n"
         "print('オッズ比（基準 = Web広告）:')\n"
         "print(odds)"),
    md("**読み取り**：`紹介` ≈ 5倍、`展示会` ≈ 4.5倍 受注しやすい（基準=Web広告）。\n"
       "`商談金額` のオッズ比はほぼ1＝金額の大小は受注に効いていない。→ **チャネルが受注のドライバー**。"),
    md("## 4. 受注確率を予測する\n\n"
       "同じ金額でもチャネルで受注確率が変わることを確認します。"),
    code("# 金額は同じ100万円、チャネルだけ変えて受注確率を予測\n"
         "new = pd.DataFrame({'商談金額':[1000000, 1000000], '獲得チャネル':['紹介', 'Web広告']})\n"
         "new['受注確率'] = logit.predict(new).round(3)   # モデルで確率を予測\n"
         "print(new)"),
    md("→ 「紹介」を増やす・「Web広告」のクオリティを上げる、といった施策の根拠になります。"),
    md("## 🧭 まとめ\n"
       "- 受注の主ドライバーは **獲得チャネル**（紹介・展示会が強い）。金額はほぼ無関係。\n"
       "- ロジスティック回帰なら「受注確率」を予測でき、施策の効果を見積もれる。\n\n"
       "> 重回帰（直線）は連続値の予測、ロジスティック回帰は0/1（確率）の予測、と使い分けます。"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `商談金額 ~ C(獲得チャネル)` の重回帰で、チャネル別の平均単価の差を見よう。\n\n"
       "**問2.** ロジスティック回帰に `C(業界)` も加え、pseudo R² が上がるか比べよう。\n\n"
       "**問3.** `テレアポ` の受注オッズ比はいくつ？ Web広告より受注しやすい？\n\n"
       "**問4.** 担当者別の受注率を `groupby` で出し、回帰の結果と照らし合わせよう。"),
    code("# 問1〜4\n"),
    md("> 🔑 **解答例は別ページ**（ネタバレ防止）👉 "
       f"**[解答例を開く]({ans_url(ans_rel)})**"),
]
write_nb(rel, cells)
ans1 = f"""# 01_ドライバー分析（回帰）― 解答例

> 本編: [{rel}]({GH + urllib.parse.quote(rel)})

```python
# 問1: チャネル別の平均単価
print(smf.ols('商談金額 ~ C(獲得チャネル)', data=btob).fit().params.round(0))

# 問2: 業界を加える
l2 = smf.logit('受注 ~ 商談金額 + C(獲得チャネル) + C(業界)', data=btob).fit()
print(l2.prsquared)   # 元(0.089)とほぼ同じ→業界は受注にあまり効かない

# 問3: テレアポのオッズ比
print(np.exp(logit.params['C(獲得チャネル)[T.テレアポ]']))  # ≈1.4倍

# 問4: 担当者別の受注率
print(btob.groupby('担当者')['受注'].mean().round(3))
```
"""
os.makedirs(os.path.dirname(os.path.join(ROOT, ans_rel)), exist_ok=True)
open(os.path.join(ROOT, ans_rel), "w", encoding="utf-8").write(ans1)

# =====================================================================
# 02 時系列予測
# =====================================================================
rel = f"{FOLDER}/02_時系列予測.ipynb"
ans_rel = f"解答集/{FOLDER}/02_時系列予測.md"
cells = [
    md(f"{badge(rel)}\n\n# 発展マーケ-02. 時系列予測（トレンド・季節性・指数平滑）\n\n"
       f"{INTRO_NOTE}\n\n"
       "36か月分の売上から、**来月以降を予測**します。移動平均→線形トレンド→"
       "**Holt-Winters（指数平滑）** と段階的に。"),
    code(SETUP + "kpi = load('monthly_kpi.csv')   # 月次KPI（売上・新規リード・受注数）\nkpi.head()"),
    md("## 1. まず眺める（トレンド＋季節性）"),
    code("kpi['売上'].plot(marker='o', figsize=(10,4), title='月別売上（36か月）')  # 折れ線\n"
         "plt.ylabel('売上(万円)'); plt.show()\n"
         "print('右肩上がりのトレンド＋年末(12月)が高い季節性が見える')"),
    md("## 2. 移動平均でならす\n"
       "12か月移動平均で季節の波を消し、大きな流れ（トレンド）を見ます。"),
    code("kpi['移動平均12'] = kpi['売上'].rolling(12).mean()   # 12か月移動平均\n"
         "kpi[['売上','移動平均12']].plot(figsize=(10,4)); plt.ylabel('売上'); plt.show()"),
    md("## 3. 線形トレンドで予測（時間で回帰）\n"
       "「月の番号 t」で売上を回帰し、直線を伸ばして予測します。"),
    code("t = np.arange(len(kpi))                      # 0,1,2,... の月番号\n"
         "a, b = np.polyfit(t, kpi['売上'], 1)          # 最小二乗で 傾きa・切片b\n"
         "print(f'トレンド: 売上 ≈ {a:.1f}×月 + {b:.0f}')\n"
         "future = np.arange(len(kpi), len(kpi)+3)     # 次の3か月\n"
         "print('単純トレンド予測:', (a*future + b).round().astype(int))\n"
         "print('→ 直線だけだと季節性（年末の山）を無視してしまう')"),
    md("## 4. Holt-Winters（指数平滑：トレンド＋季節性）\n"
       "**最近のデータを重視**しつつ、トレンドと季節性を同時に学習する定番手法です。"),
    code("from statsmodels.tsa.holtwinters import ExponentialSmoothing\n"
         "ts = kpi['売上'].astype(float)               # 予測対象の系列\n"
         "model = ExponentialSmoothing(ts, trend='add', seasonal='add',\n"
         "                             seasonal_periods=12).fit()   # 加法トレンド＋12か月季節\n"
         "fc = model.forecast(3)                       # 来3か月を予測\n"
         "print('来3か月の予測:', fc.round().astype(int).tolist())\n\n"
         "ts.plot(label='実績')                                    # 実績\n"
         "model.fittedvalues.plot(label='あてはめ')                # モデルの再現\n"
         "pd.Series(fc.values, index=range(len(ts), len(ts)+3)).plot(\n"
         "          label='予測', marker='o')                       # 予測\n"
         "plt.legend(); plt.title('Holt-Wintersによる予測'); plt.show()"),
    md("季節性を反映し、年末の山も織り込んだ予測になります。"),
    md("## 5. 予測の精度を測る（学習/検証に分ける）\n"
       "最後の6か月を「答え合わせ用」に取り分け、予測のズレを測ります。"),
    code("train, test = ts[:-6], ts[-6:]               # 学習用と検証用に分割\n"
         "m2 = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=12).fit()\n"
         "pred = m2.forecast(6)                         # 検証期間を予測\n"
         "mae = np.abs(pred.values - test.values).mean()                 # 平均絶対誤差\n"
         "mape = (np.abs(pred.values - test.values) / test.values).mean() * 100  # 平均絶対%誤差\n"
         "print(f'MAE = {mae:.1f} 万円,  MAPE = {mape:.1f}%')\n"
         "print('→ MAPEが小さいほど予測が当たっている')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `受注数` を同じ手順で予測しよう。\n\n"
       "**問2.** `seasonal='mul'`（乗法季節）や `trend=None` に変え、MAPEがどう変わるか比べよう。\n\n"
       "**問3.** 移動平均を3か月と12か月で重ね、見え方の違いを確かめよう。\n\n"
       "**問4.** 検証期間を最後の12か月に変えてMAPEを測り直そう。"),
    code("# 問1〜4\n"),
    md("> 🔑 **解答例は別ページ**（ネタバレ防止）👉 "
       f"**[解答例を開く]({ans_url(ans_rel)})**"),
]
write_nb(rel, cells)
ans2 = f"""# 02_時系列予測 ― 解答例

> 本編: [{rel}]({GH + urllib.parse.quote(rel)})

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
"""
os.makedirs(os.path.dirname(os.path.join(ROOT, ans_rel)), exist_ok=True)
open(os.path.join(ROOT, ans_rel), "w", encoding="utf-8").write(ans2)

# =====================================================================
# 03 顧客セグメンテーション（RFM + KMeans）
# =====================================================================
rel = f"{FOLDER}/03_顧客セグメンテーション_RFM.ipynb"
ans_rel = f"解答集/{FOLDER}/03_顧客セグメンテーション_RFM.md"
cells = [
    md(f"{badge(rel)}\n\n# 発展マーケ-03. 顧客セグメンテーション（RFM × K-meansクラスタリング）\n\n"
       f"{INTRO_NOTE}\n\n"
       "顧客を **RFM**（Recency 最近性・Frequency 頻度・Monetary 金額）で数値化し、"
       "**K-means** で似た顧客をグループ分けします（教師なし学習＝多変量解析）。"),
    code(SETUP + "cust = load('btob_customers.csv')   # 顧客データ\ncust.head()"),
    md("## 1. RFM指標を作る\n\n"
       "- **R** Recency：最後に買ってからの日数（小さいほど良い）\n"
       "- **F** Frequency：購入回数\n"
       "- **M** Monetary：累計購入額"),
    code("基準日 = pd.Timestamp('2026-01-01')                                  # 分析の基準日\n"
         "cust['Recency'] = (基準日 - pd.to_datetime(cust['最終購入日'])).dt.days  # 最終購入からの日数\n"
         "cust['Frequency'] = cust['購入回数']                                 # 購入回数\n"
         "cust['Monetary'] = cust['累計売上']                                  # 累計額\n"
         "cust[['顧客ID','Recency','Frequency','Monetary']].head()"),
    md("## 2. 標準化（単位をそろえる）\n\n"
       "R(日)・F(回)・M(円) は単位が違うので、**標準化（z得点）**してから距離を測ります。"),
    code("from sklearn.preprocessing import StandardScaler\n"
         "X = StandardScaler().fit_transform(cust[['Recency','Frequency','Monetary']])  # 平均0・分散1に\n"
         "print('標準化後の形:', X.shape)"),
    md("## 3. K-means でクラスタリング\n\n"
       "似たRFMの顧客を4グループに分けます（k=4）。"),
    code("from sklearn.cluster import KMeans\n"
         "km = KMeans(n_clusters=4, random_state=0, n_init=10)   # 4グループに分ける\n"
         "cust['cluster'] = km.fit_predict(X)                    # 各顧客にクラスタ番号を付与\n"
         "print(cust['cluster'].value_counts().sort_index())     # クラスタごとの人数"),
    md("## 4. クラスタの意味を読む（セグメント命名）\n\n"
       "各クラスタの R/F/M の平均を見て、ビジネス上の意味をつけます。"),
    code("prof = cust.groupby('cluster')[['Recency','Frequency','Monetary']].mean().round(0)\n"
         "print(prof)\n"
         "print('\\n読み方の例:')\n"
         "print(' F・Mが高くRが小 → 優良顧客 / Rが大きい → 離反 / F・Mが小さくRも小 → 新規')"),
    md("> 💡 クラスタ番号そのものに意味はありません。**R/F/Mの平均プロフィールで解釈**し、\n"
       "「優良・一般・新規・離反」のような名前をつけて施策につなげます。"),
    md("## 5. 2次元で可視化（PCA）\n\n"
       "3次元(R,F,M)を主成分分析(PCA)で2次元に圧縮して散布図にします。"),
    code("from sklearn.decomposition import PCA\n"
         "xy = PCA(n_components=2).fit_transform(X)              # 2次元へ圧縮\n"
         "plt.scatter(xy[:,0], xy[:,1], c=cust['cluster'], cmap='tab10', alpha=0.6)  # 色=クラスタ\n"
         "plt.title('顧客セグメント（PCAで2次元化）'); plt.xlabel('第1主成分'); plt.ylabel('第2主成分')\n"
         "plt.show()"),
    md("## 🧭 まとめ\n"
       "- RFMで顧客を数値化 → 標準化 → K-meansで自動グループ分け。\n"
       "- セグメントごとに施策を変える（優良=維持・特別対応、離反=掘り起こし、新規=育成）。"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `k=3` で分け直し、R/F/M平均からセグメントを解釈しよう。\n\n"
       "**問2.** エルボー法（k=1〜8 の `inertia_`）を折れ線にして、適切な k を考えよう。\n\n"
       "**問3.** 各クラスタの `業界` 構成を `crosstab` で見よう。偏りはある？\n\n"
       "**問4.** 最も Recency が大きいクラスタ（＝離反候補）の `顧客ID` を抽出しよう。"),
    code("# 問1〜4\n"),
    md("> 🔑 **解答例は別ページ**（ネタバレ防止）👉 "
       f"**[解答例を開く]({ans_url(ans_rel)})**"),
]
write_nb(rel, cells)
ans3 = f"""# 03_顧客セグメンテーション（RFM）― 解答例

> 本編: [{rel}]({GH + urllib.parse.quote(rel)})

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
"""
os.makedirs(os.path.dirname(os.path.join(ROOT, ans_rel)), exist_ok=True)
open(os.path.join(ROOT, ans_rel), "w", encoding="utf-8").write(ans3)
print("=== 発展マーケ 3冊 + 解答 done ===")
