# -*- coding: utf-8 -*-
"""3級 02-06 を見本基準に底上げ（増築方式）。01は見本済み・07は実践で別枠。"""
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
"02_相関と回帰.ipynb":{
 "title":"# 統計3級-02. 相関と回帰直線\n\n"
   "**🎯 できるようになること**\n- 散布図と相関係数で「関係の強さ」を読める\n"
   "- 相関≠因果（擬相関）を説明できる\n- 回帰直線でxからyを予測できる\n\n"
   "**前提**：`01_Python基礎`・統計3級01　/　**所要**：約30分　/　**レベル**：統計検定3級相当",
 "misc":"> ⚠️ **よくある間違い**：相関があっても**因果とは限らない**（裏に共通の原因＝擬相関）。"
        "また相関係数が測るのは**直線関係の強さ**だけで、曲線の関係は0に近く出ることがあります。",
 "checks":[code("import numpy as np\n"
                "x = [1,2,3,4,5]; y = [2,4,6,8,10]\n"
                "# Q1: x と y の相関係数を ans に（完全な正の相関）\n"
                "ans = None   # 例: np.corrcoef(x, y)[0,1]\n"
                "_check('Q1 相関係数', ans, np.corrcoef(x,y)[0,1])"),
           code("import numpy as np\n"
                "x = [1,2,3,4,5]; y = [2,4,6,8,10]\n"
                "# Q2: y = a*x + b の傾き a を ans に\n"
                "ans = None   # 例: np.polyfit(x, y, 1)[0]\n"
                "_check('Q2 回帰の傾き', ans, np.polyfit(x,y,1)[0])")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 散布図 | 2つの量を点で表す図 |\n| 相関係数 r | 直線関係の強さ（−1〜1） |\n"
   "| 擬相関 | 共通原因による見かけの相関 |\n| 最小二乗法 | 点に最も近い直線を引く方法 |\n"
   "| 回帰係数 | 回帰直線の傾き・切片 |",
 "cheat":"# チートシート（相関・回帰）\n"
   "df['数学'].corr(df['英語'])        # 相関係数\n"
   "df[['数学','英語','国語']].corr()   # 相関行列\n"
   "import numpy as np\n"
   "a, b = np.polyfit(df['数学'], df['英語'], 1)   # 回帰直線 傾きa・切片b\n"
   "plt.scatter(df['数学'], df['英語'])           # 散布図",
 "answer":"""# 02_相関と回帰 ― 解答例（解説つき）

**問1. 勉強時間と数学の散布図・相関**
```python
df['勉強時間'].corr(df['数学'])   # 正の相関（プラス）
plt.scatter(df['勉強時間'], df['数学']); plt.show()
```
💡 点が右上がりに散らばる＝正の相関。rがプラスで0から離れるほど強い。

**問2. 勉強時間→数学 の回帰と予測**
```python
import numpy as np
a, b = np.polyfit(df['勉強時間'], df['数学'], 1)
print(a*3 + b)   # 3時間の予測
```
💡 回帰直線は点の真ん中を通る直線。xを入れるとyの「平均的な予測」が出る（個人差はある）。

**問3. 国語と数学の相関**
```python
print(df['国語'].corr(df['数学']))   # 0に近い＝関係は弱い
```
💡 |r|が小さい＝直線的な関係は弱い、という意味（無関係とは限らないが直線では捉えにくい）。
""",
},
"03_確率分布.ipynb":{
 "title":"# 統計3級-03. 確率分布（二項分布・正規分布）\n\n"
   "**🎯 できるようになること**\n- 二項分布・正規分布の形と使い所がわかる\n"
   "- pmf/cdf で確率を計算できる\n- 68-95-99.7ルール・標準化で確率を出せる\n\n"
   "**前提**：統計3級01　/　**所要**：約30分　/　**レベル**：統計検定3級相当",
 "misc":"> ⚠️ **よくある間違い**：`pmf`（ちょうどその値の確率）と `cdf`（その値**以下**の累積）は別物。"
        "また正規分布など連続分布では「ちょうど◯◯」の確率は0で、**範囲（面積）**で考えます。",
 "checks":[code("# Q1: コインを10回投げて表がちょうど5回出る確率を ans に（二項分布）\n"
                "ans = None   # 例: stats.binom.pmf(5, 10, 0.5)\n"
                "_check('Q1 二項 P(X=5)', ans, stats.binom.pmf(5, 10, 0.5))"),
           code("# Q2: 標準正規分布で「z ≤ 0」となる確率を ans に\n"
                "ans = None   # 例: stats.norm.cdf(0)\n"
                "_check('Q2 P(z<=0)', ans, stats.norm.cdf(0))"),
           code("# Q3: 平均50・標準偏差10で「70点以上」の確率を ans に\n"
                "ans = None   # 例: 1 - stats.norm.cdf(70, 50, 10)\n"
                "_check('Q3 上側確率', ans, 1 - stats.norm.cdf(70, 50, 10))")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 二項分布 | 成功/失敗をn回くり返した成功数の分布 |\n| 正規分布 | 左右対称のつりがね型 |\n"
   "| pmf | ちょうどその値の確率（離散） |\n| pdf | 確率密度（連続）。確率は面積 |\n"
   "| cdf | その値以下の累積確率 |\n| 68-95-99.7 | ±1σ/±2σ/±3σ に入る割合 |",
 "cheat":"# チートシート（確率分布）\n"
   "stats.binom.pmf(k, n, p)        # 二項：ちょうどk回\n"
   "stats.binom.cdf(k, n, p)        # 二項：k回以下\n"
   "stats.norm.pdf(x, mu, sigma)    # 正規：高さ\n"
   "stats.norm.cdf(x, mu, sigma)    # 正規：x以下の確率\n"
   "1 - stats.norm.cdf(x, mu, sigma)  # x以上（上側）",
 "answer":"""# 03_確率分布 ― 解答例（解説つき）

**問1. サイコロ12回で1がちょうど2回**
```python
stats.binom.pmf(2, 12, 1/6)   # ≈ 0.296
```
💡 二項分布 B(n=12, p=1/6) の「ちょうど2回」は pmf。

**問2. 身長170・σ6 で176cm以上**
```python
1 - stats.norm.cdf(176, 170, 6)   # ≈ 0.159
```
💡 176は平均+1σ。上側はおよそ16%（68-95-99.7ルールと整合）。

**問3. 164〜176（±1σ）の割合**
```python
stats.norm.cdf(176,170,6) - stats.norm.cdf(164,170,6)   # ≈ 0.683
```
💡 ±1σの中に約68%、というルールどおり。
""",
},
"04_母集団と標本.ipynb":{
 "title":"# 統計3級-04. 母集団と標本・推定の入口\n\n"
   "**🎯 できるようになること**\n- 母集団と標本の関係を説明できる\n"
   "- 標準誤差 = σ/√n を計算できる\n- 中心極限定理・大数の法則を直感で理解する\n\n"
   "**前提**：統計3級01〜03　/　**所要**：約30分　/　**レベル**：統計検定3級相当",
 "misc":"> ⚠️ **よくある間違い**：**標準偏差**（データ自体の散らばり）と**標準誤差**（標本平均の散らばり）は別物。"
        "標準誤差は n を増やすほど小さくなり、推定が正確になります。",
 "checks":[code("import numpy as np\n"
                "# Q1: 母標準偏差σ=8, 標本サイズn=100 のときの標準誤差を ans に\n"
                "ans = None   # 例: 8 / np.sqrt(100)\n"
                "_check('Q1 標準誤差', ans, 8/np.sqrt(100))"),
           code("# Q2: n を4倍にすると標準誤差は何倍になる？（√nが分母）を ans に\n"
                "ans = None   # ヒント: 1/√4\n"
                "_check('Q2 何倍', ans, 0.5)"),
           code("import numpy as np\n"
                "# Q3: σ=10で標準誤差を0.5以下にする最小のn を ans に\n"
                "ans = None   # ヒント: (10/0.5)**2\n"
                "_check('Q3 必要なn', ans, (10/0.5)**2)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 母集団 | 本当に知りたい全体 |\n| 標本 | 実際に調べた一部 |\n"
   "| 標本平均 | 標本の平均（母平均の推定） |\n| 標準誤差 | 標本平均の散らばり＝σ/√n |\n"
   "| 中心極限定理 | nが大きいと標本平均は正規分布に近づく |\n| 大数の法則 | nが大きいと実測が理論に近づく |",
 "cheat":"# チートシート（標本）― そのまま実行できます\n"
   "import numpy as np\n"
   "sigma, n = 8, 100\n"
   "se = sigma / np.sqrt(n)                 # 標準誤差 = σ/√n\n"
   "print('標準誤差:', round(se, 3))\n"
   "pop = np.random.default_rng(0).normal(165, 8, 10000)   # 母集団の例\n"
   "sample = np.random.default_rng(1).choice(pop, 100)     # 標本を抽出\n"
   "print('標本平均:', round(sample.mean(), 2))",
 "answer":"""# 04_母集団と標本 ― 解答例（解説つき）

**問1. n=400 の標本平均 vs n=100**
```python
print(rng.choice(population, 400).mean())   # 母平均165により近い
```
💡 nが大きいほど標準誤差(σ/√n)が小さく、標本平均は母平均に近づく。

**問2. 標準誤差を0.5以下にするn**
```python
# 10/√n <= 0.5 → √n >= 20 → n >= 400
```

**問3. 出口調査が当たる理由**
無作為に十分な数の標本を取れば、標本平均は母平均の近くに集中し（標準誤差が小さい）、
全数調査をしなくても全体の傾向を高い精度で推測できるから。
💡 「全員に聞く」必要はなく、「偏りなく・ある程度の数」を聞けばよい、が要点。
""",
},
"05_実験と条件付き確率.ipynb":{
 "title":"# 統計3級-05. 実験・観察研究と確率（条件付き・独立）\n\n"
   "**🎯 できるようになること**\n- 観察研究と実験研究・処理群/対照群を説明できる\n"
   "- 独立な試行の確率を計算できる\n- 条件付き確率をクロス表から求められる\n\n"
   "**前提**：統計3級01　/　**所要**：約25分　/　**レベル**：統計検定3級相当",
 "misc":"> ⚠️ **よくある間違い**：相関や関連が見えても、**交絡**（裏の共通原因）があるため因果は言えない。"
        "因果を確かめるには**無作為割付の実験**が強い。独立なら `P(A|B)=P(A)`。",
 "checks":[code("# Q1: コインが表(1/2) かつ サイコロが6(1/6) の確率を ans に（独立）\n"
                "ans = None   # (1/2)*(1/6)\n"
                "_check('Q1 同時確率', ans, (1/2)*(1/6))"),
           code("# Q2: 運動部240人中180人が朝食あり。P(朝食あり|運動部) を ans に\n"
                "ans = None   # 180/240\n"
                "_check('Q2 条件付き確率', ans, 180/240)"),
           code("# Q3: 朝食なし180人中60人が運動部。P(運動部|朝食なし) を ans に\n"
                "ans = None   # 60/180\n"
                "_check('Q3 条件付き確率', ans, 60/180)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 観察研究 | ありのまま観察 |\n| 実験研究 | 条件を割り当てて比較 |\n"
   "| 処理群/対照群 | 対策あり/なしのグループ |\n| 無作為割付 | くじ引きで群を決める |\n"
   "| 交絡 | 両方に効く第3の原因 |\n| 条件付き確率 | P(A\\|B)=P(A∩B)/P(B) |\n| 独立 | P(A∩B)=P(A)P(B) |",
 "cheat":"# チートシート（確率）― そのまま実行できます\n"
   "P_A, P_B = 1/2, 1/6\n"
   "print('独立な同時確率 P(A∩B):', P_A * P_B)\n"
   "import pandas as pd\n"
   "t = pd.DataFrame({'あり':[180,40], 'なし':[60,120]}, index=['運動部','帰宅部'])\n"
   "print('条件付き確率（行比率）:')\n"
   "print((t.div(t.sum(axis=1), axis=0)).round(2))",
 "answer":"""# 05_実験と条件付き確率 ― 解答例（解説つき）

**問1. 交絡と実験**
アプリ利用と成績の両方に効く第3の要因（もともとの生活習慣・意識など）が**交絡**。
だから観察だけでは「アプリが成績を上げた」とは言えない。
→ 無作為に2群に分け、片方だけアプリを使わせて成績を比べる**実験**で因果を検証する。

**問2. 独立な事象**
```python
print((1/2)*(1/6))   # 1/12
```
💡 独立なら確率はかけ算。

**問3. 条件付き確率**
```python
print(60/180)   # 1/3
```
💡 「朝食なし」に絞った中での「運動部」の割合＝クロス表の行比率。
""",
},
"06_共分散・変動係数・正規近似.ipynb":{
 "title":"# 統計3級-06. 共分散・変動係数・二項分布の正規近似\n\n"
   "**🎯 できるようになること**\n- 共分散から相関係数を導ける\n"
   "- 変動係数でスケールの違うばらつきを比べられる\n- 二項分布の正規近似を使える\n\n"
   "**前提**：統計3級01〜03　/　**所要**：約30分　/　**レベル**：統計検定3級相当",
 "misc":"> ⚠️ **よくある間違い**：共分散は**単位に依存**するので、値の大小だけで関係の強さは比べられない。"
        "強さを比べるには無単位の**相関係数**（共分散÷各標準偏差）にする。",
 "checks":[code("import numpy as np\n"
                "x = [1,2,3]; y = [2,4,6]\n"
                "# Q1: x,y の共分散（÷n）を ans に\n"
                "ans = None   # 例: np.cov(x, y, ddof=0)[0,1]\n"
                "_check('Q1 共分散', ans, np.cov(x,y,ddof=0)[0,1])"),
           code("import numpy as np\n"
                "d = [10, 20, 30]\n"
                "# Q2: d の変動係数（標準偏差÷平均, ÷n）を ans に\n"
                "ans = None   # 例: np.std(d)/np.mean(d)\n"
                "_check('Q2 変動係数', ans, np.std(d)/np.mean(d))"),
           code("import numpy as np\n"
                "# Q3: 二項分布 B(100, 0.5) の標準偏差 √(np(1-p)) を ans に\n"
                "ans = None   # 例: np.sqrt(100*0.5*0.5)\n"
                "_check('Q3 標準偏差', ans, np.sqrt(100*0.5*0.5))")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 共分散 | 一緒に増減する傾向（単位依存） |\n| 相関係数 | 共分散÷(各標準偏差)、−1〜1 |\n"
   "| 変動係数 | 標準偏差÷平均（相対ばらつき） |\n| 正規近似 | nが大きい二項分布≈正規分布 |\n"
   "| 連続補正 | 離散→連続の0.5のずらし |",
 "cheat":"# チートシート（共分散・近似）\n"
   "import numpy as np\n"
   "np.cov(x, y, ddof=0)[0,1]            # 共分散(÷n)\n"
   "df['数学'].corr(df['英語'])           # 相関係数\n"
   "df['数学'].std()/df['数学'].mean()    # 変動係数\n"
   "np.sqrt(n*p*(1-p))                   # 二項の標準偏差",
 "answer":"""# 06_共分散・変動係数・正規近似 ― 解答例（解説つき）

**問1. 勉強時間と数学：共分散→相関係数**
```python
import numpy as np
a=df['勉強時間'].values; b=df['数学'].values
cov=np.mean((a-a.mean())*(b-b.mean()))
print(cov/(a.std()*b.std()))   # = df['勉強時間'].corr(df['数学'])
```
💡 相関係数は共分散を各標準偏差で割って無単位にしたもの。だから−1〜1に収まる。

**問2. A店・B店の変動係数**
```python
import numpy as np
for d in [np.array([50,52,48,51,49]), np.array([10,14,8,12,16])]:
    print(d.std()/d.mean())   # B店のCVが大きい＝相対的に不安定
```
💡 平均が違う店どうしのばらつきは、CV（相対化）で比べる。

**問3. サイコロ180回（1の目）の正規近似**
```python
from scipy import stats
import numpy as np
mu, sig = 180/6, np.sqrt(180*(1/6)*(5/6))
print(mu, sig, 1 - stats.norm.cdf(34.5, mu, sig))   # 35回以上（連続補正34.5）
```
💡 nが大きいので二項≈正規。「35回以上」は連続補正で34.5を境にする。
""",
},
}

for fname, spec in NB.items():
    p = os.path.join(ROOT, "03_統計_3級", fname)
    nb = json.load(open(p, encoding="utf-8")); cells = nb["cells"]
    for c in cells:
        if c["cell_type"]=="markdown" and "".join(c["source"]).startswith("# 統計3級"):
            if "🎯" not in "".join(c["source"]): c["source"]=spec["title"]
            break
    if not any("🧠 確認テスト" in "".join(c["source"]) for c in cells):
        for i,c in enumerate(cells):
            if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith("---"):
                cells[i:i] = [md(spec["misc"]), md(CHECK_HEADER), code(HELPER)] + spec["checks"]; break
    if not any("📒 用語集" in "".join(c["source"]) for c in cells):
        cells += [md(spec["glossary"]), code(spec["cheat"])]
    json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    ap = os.path.join(ROOT, "解答集/03_統計_3級", fname.replace(".ipynb",".md"))
    os.makedirs(os.path.dirname(ap), exist_ok=True)
    open(ap,"w",encoding="utf-8").write(spec["answer"])
    print("upgraded", fname, "->", len(cells), "cells")
print("=== 3級 rollout done ===")
