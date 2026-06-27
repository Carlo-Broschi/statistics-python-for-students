# -*- coding: utf-8 -*-
"""4級6冊を見本基準に底上げ（増築方式）：🎯目標・⚠️誤解・🧠自動採点・📒用語集を追加、解答に💡解説。"""
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
"01_データの種類と度数分布.ipynb": {
 "title":"# 統計4級-01. データの種類と度数分布表\n\n"
   "**🎯 できるようになること**\n"
   "- データを質的/量的・4つの尺度（名義・順序・間隔・比例）に見分けられる\n"
   "- 度数分布表（度数・相対度数・累積度数）を作れる\n"
   "- ヒストグラムで分布の形を読める\n\n"
   "**前提**：`01_Python基礎`（pandas入門まで）　/　**所要**：約25分　/　**レベル**：統計検定4級相当",
 "misc":"> ⚠️ **よくある間違い**：気温(℃)の「0」は“無い”を意味しない（**間隔尺度**）。"
        "一方で点数・人数の「0」は“無い”を表す（**比例尺度**）。0の意味で尺度が変わります。",
 "checks":[code("# Q1: 数学が80点以上の人数を ans に入れよう\n"
                "ans = None   # 例: (df['数学'] >= 80).sum()\n"
                "_check('Q1 80点以上の人数', ans, int((df['数学'] >= 80).sum()))"),
           code("# Q2: 80点以上の人の割合（相対度数, 0〜1）を ans に\n"
                "ans = None   # 例: (df['数学'] >= 80).mean()\n"
                "_check('Q2 相対度数', ans, float((df['数学'] >= 80).mean()))")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n"
   "| 用語 | 意味 |\n|---|---|\n"
   "| 質的/量的 | 種類を表す/数量を表す |\n"
   "| 名義・順序 | 区別だけ/順番に意味 |\n"
   "| 間隔・比例 | 0が便宜的/0が“無い” |\n"
   "| 度数・相対度数 | 各階級の個数/全体に対する割合 |\n"
   "| 累積度数 | その階級までの合計 |\n"
   "| 階級・階級値 | 区間/区間の代表値 |\n"
   "| ヒストグラム | 量の分布を棒で表す図（棒がくっつく） |",
 "cheat":"# チートシート（度数分布）\n"
   "pd.cut(df['数学'], bins=[0,20,40,60,80,100])   # 階級に分ける\n"
   "df['数学'].value_counts()                       # 値ごとの個数\n"
   "plt.hist(df['数学'], bins=10)                   # ヒストグラム",
 "answer":"""# 01_データの種類と度数分布 ― 解答例（解説つき）

**問1. 尺度の判定**
(a)都道府県名＝**名義** (b)順位＝**順序** (c)体重＝**比例** (d)摂氏温度＝**間隔**
💡 見分け方：順番に意味がある？→順序以上。差を引き算できる？→間隔以上。0が“無い”を表す（比も意味）？→比例。

**問2・問3. 英語の度数分布とヒストグラム**
```python
df['英語階級'] = pd.cut(df['英語'], bins=[0,20,40,60,80,100], right=False)
print(df['英語階級'].value_counts().sort_index())
plt.hist(df['英語'], bins=[0,20,40,60,80,100], edgecolor='white'); plt.show()
```
💡 `value_counts()` は並びがバラバラなので `.sort_index()` で階級順に。最も人数が多い階級＝棒が一番高い区間。
""",
},

"02_代表値.ipynb": {
 "title":"# 統計4級-02. 代表値（平均・中央値・最頻値）\n\n"
   "**🎯 できるようになること**\n"
   "- 平均・中央値・最頻値を計算して使い分けられる\n"
   "- 外れ値に強いのは中央値、と理由つきで説明できる\n"
   "- グループ別に代表値を比べられる\n\n"
   "**前提**：`01_Python基礎`　/　**所要**：約25分　/　**レベル**：統計検定4級相当",
 "misc":"> ⚠️ **よくある間違い**：「平均＝真ん中」ではありません。分布が左右非対称だと、"
        "平均は裾（極端な値）に引っ張られ、中央値とズレます（年収・運賃などが典型）。",
 "checks":[code("x = [60, 75, 80, 75, 90, 75, 55]\n"
                "# Q1: x の中央値を ans に\n"
                "ans = None   # 例: np.median(x)\n"
                "_check('Q1 中央値', ans, np.median(x))"),
           code("x = [60, 75, 80, 75, 90, 75, 55]\n"
                "# Q2: x の平均を ans に\n"
                "ans = None\n"
                "_check('Q2 平均', ans, np.mean(x))")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n"
   "| 用語 | 意味 | 強い/弱い |\n|---|---|---|\n"
   "| 平均値 | 合計÷個数 | 計算しやすい/外れ値に弱い |\n"
   "| 中央値 | 真ん中の値 | 外れ値に強い |\n"
   "| 最頻値 | 最も多い値 | 質的データにも使える |",
 "cheat":"# チートシート（代表値）\n"
   "s = df['数学']\n"
   "s.mean(); s.median(); s.mode()        # 平均・中央値・最頻値\n"
   "df.groupby('クラス')['数学'].mean()    # グループ別の平均",
 "answer":"""# 02_代表値 ― 解答例（解説つき）

**問1. 7人の代表値**
```python
import numpy as np, statistics
x = [60,75,80,75,90,75,55]
print(np.mean(x), np.median(x), statistics.mode(x))   # 72.86, 75, 75
```
💡 平均は計算で出る1点、中央値は並べた真ん中、最頻値は一番多い値（ここでは75が3回）。

**問2. クラス別の中央値**
```python
df.groupby('クラス')['英語'].median()
```

**問3. 来客数 平均 vs 中央値**
```python
import numpy as np
x = [20, 22, 21, 19, 200]
print(np.mean(x), np.median(x))   # 平均56.4, 中央値21
```
💡 平均は「200の日」に引っ張られ実態とズレる。**中央値21**のほうが“ふつうの日”を表す。
""",
},

"03_ばらつきと箱ひげ図.ipynb": {
 "title":"# 統計4級-03. ばらつき・四分位数・箱ひげ図\n\n"
   "**🎯 できるようになること**\n"
   "- 範囲・四分位範囲(IQR)で散らばりを数で表せる\n"
   "- 箱ひげ図を読める／グループ間で比較できる\n"
   "- 外れ値をIQRの方法で見つけられる\n\n"
   "**前提**：`01_Python基礎`　/　**所要**：約25分　/　**レベル**：統計検定4級相当",
 "misc":"> ⚠️ **よくある間違い**：外れ値を見つけても**勝手に消さない**。記録ミスなのか"
        "“本物の珍しい値”なのかを確認してから扱います（消すと事実が歪むことがある）。",
 "checks":[code("d = [12, 15, 18, 22, 25, 30, 35]\n"
                "# Q1: 範囲（最大−最小）を ans に\n"
                "ans = None\n"
                "_check('Q1 範囲', ans, max(d) - min(d))"),
           code("import numpy as np\n"
                "d = [12, 15, 18, 22, 25, 30, 35]\n"
                "# Q2: 第1四分位数(Q1)を ans に\n"
                "ans = None   # 例: np.quantile(d, 0.25)\n"
                "_check('Q2 第1四分位数', ans, np.quantile(d, 0.25))"),
           code("import numpy as np\n"
                "d = [12, 15, 18, 22, 25, 30, 35]\n"
                "# Q3: IQR（Q3−Q1）を ans に\n"
                "ans = None\n"
                "_check('Q3 IQR', ans, np.quantile(d,0.75) - np.quantile(d,0.25))")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n"
   "| 用語 | 意味 |\n|---|---|\n"
   "| 範囲 | 最大−最小 |\n"
   "| 四分位数 | データを4等分する境目(Q1/Q2/Q3) |\n"
   "| 四分位範囲 IQR | Q3−Q1（真ん中50%の幅） |\n"
   "| 箱ひげ図 | 四分位数を図にしたもの |\n"
   "| 外れ値 | Q1−1.5×IQR 未満 / Q3+1.5×IQR 超 |",
 "cheat":"# チートシート（ばらつき）\n"
   "s = df['数学']\n"
   "s.max() - s.min()               # 範囲\n"
   "s.quantile([.25, .5, .75])      # 四分位数\n"
   "s.describe()                    # まとめて確認\n"
   "df.boxplot(column='数学', by='クラス')   # 箱ひげ図",
 "answer":"""# 03_ばらつきと箱ひげ図 ― 解答例（解説つき）

**問1. 四分位数とIQR**
```python
import pandas as pd
x = pd.Series([12,15,18,22,25,30,35])
print(x.quantile([.25,.5,.75]))     # Q1=16.5, Q2=22, Q3=27.5
print(x.quantile(.75) - x.quantile(.25))  # IQR
```
💡 IQRは「真ん中50%がどれだけ広がっているか」。範囲(最大−最小)より外れ値に強い散らばり指標。

**問2. 国語の箱ひげ図（クラス別）**
```python
df.boxplot(column='国語', by='クラス'); plt.show()
```
💡 箱が長いクラスほどばらつき大。中の線が中央値。

**問3. 英語の外れ値（IQR法）**
```python
q1,q3 = df['英語'].quantile([.25,.75]); iqr=q3-q1
df[(df['英語'] < q1-1.5*iqr) | (df['英語'] > q3+1.5*iqr)][['生徒ID','英語']]
```
""",
},

"04_確率とクロス集計.ipynb": {
 "title":"# 統計4級-04. 確率の基礎とクロス集計表\n\n"
   "**🎯 できるようになること**\n"
   "- 確率・期待値を計算できる\n"
   "- クロス集計表と行比率（割合）を読める\n"
   "- 大数の法則をシミュレーションで体感できる\n\n"
   "**前提**：`01_Python基礎`　/　**所要**：約25分　/　**レベル**：統計検定4級相当",
 "misc":"> ⚠️ **よくある間違い**：確率は必ず 0〜1（0〜100%）。1を超えたら計算ミス。"
        "また**期待値は「平均してこのくらい」**であって、毎回もらえる額ではありません。",
 "checks":[code("# Q1: サイコロで「3以上の目」が出る確率を ans に（3,4,5,6 の4通り）\n"
                "ans = None   # 4/6\n"
                "_check('Q1 確率', ans, 4/6)"),
           code("# Q2: 当たり500円(確率0.2)・はずれ0円(確率0.8) のくじの期待値を ans に\n"
                "ans = None   # 500*0.2 + 0*0.8\n"
                "_check('Q2 期待値', ans, 500*0.2)"),
           code("# Q3: トランプ52枚で絵札(J,Q,K=12枚)が出る確率を ans に\n"
                "ans = None   # 12/52\n"
                "_check('Q3 絵札の確率', ans, 12/52)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n"
   "| 用語 | 意味 |\n|---|---|\n"
   "| 確率 | 起こる場合 ÷ 全部の場合（0〜1） |\n"
   "| 期待値 | Σ(値 × その確率)＝平均的な値 |\n"
   "| クロス集計表 | 2つの観点で数えた表 |\n"
   "| 行比率/列比率 | 行/列ごとに割合にしたもの |\n"
   "| 大数の法則 | 回数を増やすと実測が理論確率に近づく |",
 "cheat":"# チートシート（確率・クロス集計）\n"
   "pd.crosstab(df['クラス'], df['合否'])                      # クロス集計\n"
   "pd.crosstab(df['クラス'], df['合否'], normalize='index')  # 行比率\n"
   "np.sum(np.array([1000,0]) * np.array([0.1,0.9]))          # 期待値 Σ(値×確率)",
 "answer":"""# 04_確率とクロス集計 ― 解答例（解説つき）

**問1. トランプの確率**
```python
print(13/52, 12/52)   # ハート=1/4=0.25, 絵札=12/52≈0.231
```
💡 確率＝(あてはまる枚数)÷(全52枚)。

**問2. チャネル×受注のクロス集計**
```python
btob = pd.read_csv('../data/sales_btob.csv')
pd.crosstab(btob['獲得チャネル'], btob['受注'])
```

**問3. サイコロの期待値**
```python
import numpy as np
v = np.arange(1,7); p = np.full(6, 1/6)
print(np.sum(v*p))   # 3.5
```
💡 期待値は「1〜6を平均したら3.5」。実際に3.5は出ないが、何回も振った平均が3.5に近づく。
""",
},

"05_PPDACとグラフの読み方.ipynb": {
 "title":"# 統計4級-05. 統計的問題解決(PPDAC)と基本グラフの読み方\n\n"
   "**🎯 できるようになること**\n"
   "- PPDACで問題解決の流れを説明できる\n"
   "- 目的に合うグラフを選び、正しく読める\n"
   "- パレート図・幹葉図を作れる\n\n"
   "**前提**：`01_Python基礎`　/　**所要**：約25分　/　**レベル**：統計検定4級相当",
 "misc":"> ⚠️ **よくある間違い**：円グラフは項目が多い／差が小さいと読みにくい。"
        "比較が目的なら棒グラフが無難。3D円グラフは面積が歪むので避けましょう。",
 "checks":[code("import pandas as pd\n"
                "c = pd.Series({'A':60, 'B':25, 'C':10, 'D':5})\n"
                "# Q1: 最大項目Aの構成比(%)を ans に\n"
                "ans = None   # 60 / 合計 * 100\n"
                "_check('Q1 構成比%', ans, 60/c.sum()*100)"),
           code("import pandas as pd\n"
                "c = pd.Series({'A':60, 'B':25, 'C':10, 'D':5})\n"
                "# Q2: 上位2項目(A,B)の累積構成比(%)を ans に\n"
                "ans = None\n"
                "_check('Q2 累積%', ans, (60+25)/c.sum()*100)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n"
   "| 用語 | 使う場面 |\n|---|---|\n"
   "| PPDAC | 問題→計画→データ→分析→結論 |\n"
   "| 棒グラフ | 量の大小を比べる |\n"
   "| 折れ線 | 時間の変化を見る |\n"
   "| 円・帯 | 割合（構成比）を見る |\n"
   "| パレート図 | 重要な少数を見つける |\n"
   "| 幹葉図 | 元の数字を残して分布を見る |",
 "cheat":"# チートシート（グラフ）\n"
   "import pandas as pd\n"
   "s = pd.Series({'A':8, 'B':12, 'C':10})\n"
   "s.plot(kind='bar')      # 棒\n"
   "s.plot(kind='line')     # 折れ線\n"
   "s.plot(kind='pie')      # 円\n"
   "s.cumsum()/s.sum()*100  # 累積構成比（パレート）",
 "answer":"""# 05_PPDACとグラフの読み方 ― 解答例（解説つき）

**問1. 適切なグラフ**
(a)毎月の売上推移＝**折れ線**（時間変化） (b)賛成/反対の割合＝**円 or 帯**（構成比） (c)5店舗の比較＝**棒**（大小比較）
💡 「変化＝折れ線／割合＝円・帯／比較＝棒」が基本の対応。

**問2. 数学を幹葉図に**
```python
stem_leaf(df['数学'].tolist())
```
💡 幹葉図は元の数字が残るので、分布の形と実際の値を同時に確認できる。

**問3. パレート図**
```python
import pandas as pd
s = pd.Series({'部品A':60,'部品B':25,'部品C':10,'その他':5}).sort_values(ascending=False)
cum = s.cumsum()/s.sum()*100
print(cum)   # 上位2項目(部品A,B)で85% → 8割超
```
💡 「上位の少数で全体の大半を占める」＝パレートの法則。対策の優先順位づけに使う。
""",
},

"06_時系列と場合の数.ipynb": {
 "title":"# 統計4級-06. 時系列データと場合の数（樹形図）\n\n"
   "**🎯 できるようになること**\n"
   "- 増減率・指数・移動平均で時系列を読める\n"
   "- 場合の数を樹形図/列挙で数えられる\n"
   "- 場合の数を確率につなげられる\n\n"
   "**前提**：`01_Python基礎`　/　**所要**：約25分　/　**レベル**：統計検定4級相当",
 "misc":"> ⚠️ **よくある間違い**：「％」と「％ポイント」は別物（20%→24%は **+4%ポイント**、"
        "“+20%増”ではない）。また移動平均は両端が計算できず**欠ける**ことに注意。",
 "checks":[code("# Q1: 売上が 1月200→2月180 のとき、2月の前月比(%)を ans に\n"
                "ans = None   # (180-200)/200*100\n"
                "_check('Q1 前月比%', ans, (180-200)/200*100)"),
           code("# Q2: 1月を100としたとき、3月(売上210)の指数を ans に（1月=200）\n"
                "ans = None   # 210/200*100\n"
                "_check('Q2 指数', ans, 210/200*100)"),
           code("# Q3: コインを3枚投げたときの場合の数（表裏の組合せ）を ans に\n"
                "ans = None   # 2の3乗\n"
                "_check('Q3 場合の数', ans, 2**3)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n"
   "| 用語 | 意味 |\n|---|---|\n"
   "| 増減率 | (今−前)÷前 ×100(%) |\n"
   "| 指数 | 基準を100としたときの大きさ |\n"
   "| 移動平均 | 数期間の平均をずらして計算 |\n"
   "| 場合の数 | 何通りあるか |\n"
   "| 樹形図 | 枝分かれで場合を整理する図 |",
 "cheat":"# チートシート（時系列・場合の数）\n"
   "sales.pct_change()*100         # 増減率(%)\n"
   "sales / sales.iloc[0] * 100    # 指数（最初=100）\n"
   "sales.rolling(3).mean()        # 3期間の移動平均\n"
   "import itertools\n"
   "list(itertools.product([1,2,3], repeat=2))   # 場合の列挙",
 "answer":"""# 06_時系列と場合の数 ― 解答例（解説つき）

**問1. 増減率と指数**
```python
import pandas as pd
s = pd.Series([200,180,210,240,230,260])
print(s.pct_change()*100)      # 前月比(%)
print(s/s.iloc[0]*100)         # 1月=100の指数
```
💡 増減率は「前の月から何％動いたか」、指数は「基準からどれだけ伸びたか」。役割が違う。

**問2. 気温の5日移動平均**
```python
w = pd.read_csv('../data/weather.csv')
w['気温'].rolling(5).mean().plot(); w['気温'].plot(); plt.show()
```
💡 移動平均は短期の上下を消してトレンドを見る。最初の4日は平均が作れず欠ける。

**問3. サイコロ2個の場合の数と確率**
```python
import itertools
dice = list(itertools.product(range(1,7), repeat=2))
seven = [d for d in dice if sum(d)==7]
print(len(dice), len(seven), len(seven)/len(dice))   # 36通り, 7は6通り, 1/6
```
💡 全36通りのうち合計7は6通り → 確率6/36=1/6。場合の数が確率の土台。
""",
},
}

for fname, spec in NB.items():
    p = os.path.join(ROOT, "02_統計_4級", fname)
    nb = json.load(open(p, encoding="utf-8"))
    cells = nb["cells"]
    # 1) タイトル差し替え（🎯が無ければ）
    for c in cells:
        if c["cell_type"]=="markdown" and "".join(c["source"]).startswith("# 統計4級-0"):
            if "🎯" not in "".join(c["source"]):
                c["source"] = spec["title"]
            break
    # 2) 確認テスト＋⚠️ を 練習(---) の直前に挿入
    if not any("🧠 確認テスト" in "".join(c["source"]) for c in cells):
        for i,c in enumerate(cells):
            if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith("---"):
                block = [md(spec["misc"]), md(CHECK_HEADER), code(HELPER)] + spec["checks"]
                cells[i:i] = block
                break
    # 3) 用語集＆チートシート を末尾に追加
    if not any("📒 用語集" in "".join(c["source"]) for c in cells):
        cells += [md(spec["glossary"]), code(spec["cheat"])]
    json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    # 4) 解答集を解説つきで上書き
    ap = os.path.join(ROOT, "解答集/02_統計_4級", fname.replace(".ipynb",".md"))
    os.makedirs(os.path.dirname(ap), exist_ok=True)
    open(ap,"w",encoding="utf-8").write(spec["answer"])
    print("upgraded", fname, "->", len(cells), "cells")
print("=== 4級 rollout done ===")
