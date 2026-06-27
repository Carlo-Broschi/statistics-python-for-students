# -*- coding: utf-8 -*-
"""2級 01-07 を見本基準に底上げ（増築方式）。08は実践タイタニックで別枠。"""
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
"01_区間推定.ipynb":{
 "title":"# 統計2級-01. 区間推定（信頼区間）\n\n"
   "**🎯 できるようになること**\n- 点推定と区間推定の違いを説明できる\n"
   "- 母平均(t分布)・母比率の信頼区間を計算できる\n- 信頼度やnで区間の幅がどう変わるか説明できる\n\n"
   "**前提**：統計3級04（標本・標準誤差）　/　**所要**：約30分　/　**レベル**：統計検定2級相当",
 "misc":"> ⚠️ **よくある間違い**：95%信頼区間は「母平均がこの区間に入る確率が95%」ではありません。"
        "正しくは「同じ調査を100回やれば、95回はこの方法で作った区間が母平均を含む」という意味です。",
 "checks":[code("from scipy import stats\n# Q1: 両側95%信頼区間で使う標準正規の z 値を ans に（約1.96）\n"
                "ans = None   # 例: stats.norm.ppf(0.975)\n_check('Q1 z(95%)', ans, stats.norm.ppf(0.975))"),
           code("import numpy as np\n# Q2: 賛成率0.24・n=400 のときの標準誤差 √(p(1-p)/n) を ans に\n"
                "ans = None\n_check('Q2 標準誤差', ans, np.sqrt(0.24*0.76/400))"),
           code("from scipy import stats\n# Q3: 信頼度を99%に上げたときの片側 z 値を ans に（95%より大きい）\n"
                "ans = None   # 例: stats.norm.ppf(0.995)\n_check('Q3 z(99%)', ans, stats.norm.ppf(0.995))")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 点推定 | 1つの値で推定 |\n| 区間推定 | 幅で推定 |\n| 信頼区間 | 母数が入ると考える範囲 |\n"
   "| 信頼係数 | 95%など信頼の度合い |\n| 標準誤差 | 推定値の散らばり |",
 "cheat":"# チートシート（区間推定）\nfrom scipy import stats\nimport numpy as np\n"
   "data = np.array([198,203,197,205,199,201])\nse = data.std(ddof=1)/np.sqrt(len(data))\n"
   "print(stats.t.interval(0.95, len(data)-1, data.mean(), se))   # 母平均の95%CI",
 "answer":"""# 01_区間推定 ― 解答例（解説つき）

**問1. 16人・平均72・不偏SD8 の母平均95%CI**
```python
from scipy import stats
se = 8/16**0.5
print(stats.t.interval(0.95, 15, 72, se))   # 約[67.7, 76.3]
```
💡 標本が小さいので t分布（自由度15）。±t×標準誤差 が区間。

**問2. 1000人中320人「利用したい」の95%CI**
```python
import numpy as np
p = 320/1000; se = np.sqrt(p*(1-p)/1000)
print(p-1.96*se, p+1.96*se)
```

**問3. 誤差±2%以内に必要なn**
```python
print((1.96**2 * 0.32*0.68)/0.02**2)   # ≈ 2089人
```
💡 必要なnは「誤差を小さくするほど」「pが0.5に近いほど」大きくなる。
""",
},
"02_仮説検定.ipynb":{
 "title":"# 統計2級-02. 仮説検定\n\n"
   "**🎯 できるようになること**\n- 帰無仮説・対立仮説・有意水準・p値を説明できる\n"
   "- 1標本/2標本のt検定、母比率の検定ができる\n- 第1種・第2種の過誤を区別できる\n\n"
   "**前提**：統計2級01　/　**所要**：約35分　/　**レベル**：統計検定2級相当",
 "misc":"> ⚠️ **よくある間違い**：p値は「帰無仮説が正しい確率」ではありません。また「有意差なし」は"
        "「差が無いことの証明」ではなく、「差があるとは言い切れない」だけです。",
 "checks":[code("from scipy import stats\nA=[5,6,7]; B=[8,9,10]\n"
                "# Q1: A,B の2標本t検定の p値 を ans に\n"
                "ans = None   # 例: stats.ttest_ind(A,B).pvalue\n_check('Q1 p値', ans, stats.ttest_ind(A,B).pvalue)"),
           code("# Q2: 第1種の過誤の確率は有意水準αに等しい。α=0.05 のとき ans は？\n"
                "ans = None   # 0.05\n_check('Q2 第1種の過誤', ans, 0.05)"),
           code("# Q3: コイン100回で表60回。母比率0.5の検定統計量 z=(0.6-0.5)/√(0.5*0.5/100) を ans に\n"
                "ans = None   # 0.1/0.05\n_check('Q3 z統計量', ans, (0.6-0.5)/(0.5*0.5/100)**0.5)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 帰無仮説 H₀ | 差はない（の仮定） |\n| 対立仮説 H₁ | 差がある |\n| 有意水準 α | 棄却の基準（ふつう0.05） |\n"
   "| p値 | H₀のもとで今の差以上が出る確率 |\n| 第1種の過誤 | 本当は差が無いのに「ある」 |\n"
   "| 第2種の過誤 | 本当は差があるのに「ない」 |",
 "cheat":"# チートシート（仮説検定）\nfrom scipy import stats\n"
   "stats.ttest_1samp([10,11,9,12], 10)      # 1標本t検定\n"
   "stats.ttest_ind([1,2,3],[4,5,6])         # 2標本t検定\n"
   "from statsmodels.stats.proportion import proportions_ztest\n"
   "proportions_ztest(60, 100, 0.5)          # 母比率の検定",
 "answer":"""# 02_仮説検定 ― 解答例（解説つき）

**問1. 糖度は10度といえるか（1標本t検定）**
```python
from scipy import stats
print(stats.ttest_1samp([10.5,9.8,10.2,11.0,10.7,10.1,10.9,10.4], 10))
```
💡 p<0.05 なら「10度とは言えない」。

**問2. 展示会 vs Web広告 の商談金額（2標本t検定）**
```python
import pandas as pd
from scipy import stats
btob = pd.read_csv('../data/sales_btob.csv')
a = btob[btob['獲得チャネル']=='展示会']['商談金額']
b = btob[btob['獲得チャネル']=='Web広告']['商談金額']
print(stats.ttest_ind(a, b))
```

**問3. コイン100回表60回（母比率の検定）**
```python
from statsmodels.stats.proportion import proportions_ztest
print(proportions_ztest(60, 100, 0.5))   # p≈0.045 → ゆがみの疑い
```
💡 「偏りがある」と言えるかを、観測比率0.6と理論0.5の差で検定。
""",
},
"03_カイ二乗と分散分析.ipynb":{
 "title":"# 統計2級-03. カイ二乗検定・分散分析(ANOVA)\n\n"
   "**🎯 できるようになること**\n- カイ二乗（独立性・適合度）の検定ができる\n"
   "- 期待度数の意味がわかる\n- 一元配置分散分析で3群以上の平均を比較できる\n\n"
   "**前提**：統計2級02　/　**所要**：約30分　/　**レベル**：統計検定2級相当",
 "misc":"> ⚠️ **よくある間違い**：カイ二乗検定は**度数（カウント）**に使うもの。割合や平均そのものには使いません。"
        "また期待度数が小さすぎる（目安5未満）と近似が崩れます。",
 "checks":[code("from scipy import stats\n# Q1: サイコロ観測[18,21,16,14,17,14]の適合度検定のカイ二乗統計量 を ans に\n"
                "ans = None   # 例: stats.chisquare([18,21,16,14,17,14]).statistic\n"
                "_check('Q1 カイ二乗', ans, stats.chisquare([18,21,16,14,17,14]).statistic)"),
           code("from scipy import stats\n# Q2: 3群の分散分析のF統計量 を ans に\n"
                "ans = None   # 例: stats.f_oneway([50,52,48],[60,61,59],[70,69,71]).statistic\n"
                "_check('Q2 F統計量', ans, stats.f_oneway([50,52,48],[60,61,59],[70,69,71]).statistic)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 適合度検定 | 理論比に合うか |\n| 独立性の検定 | 2つの質的変数に関連があるか |\n"
   "| 期待度数 | 関連が無い場合の理論値 |\n| 一元配置分散分析 | 3群以上の平均の比較 |\n| F比 | 群間/群内のばらつきの比 |",
 "cheat":"# チートシート（カイ二乗・ANOVA）\nfrom scipy import stats\n"
   "stats.chi2_contingency([[30,10],[20,40]])   # 独立性の検定\n"
   "stats.chisquare([18,21,16,14,17,14])        # 適合度検定\n"
   "stats.f_oneway([1,2,3],[4,5,6],[7,8,9])     # 一元配置分散分析",
 "answer":"""# 03_カイ二乗と分散分析 ― 解答例（解説つき）

**問1. 業界×受注 の独立性の検定**
```python
from scipy import stats
print(stats.chi2_contingency(pd.crosstab(btob['業界'], btob['受注']))[1])   # p値
```

**問2. 血液型の適合度検定**
```python
import numpy as np
from scipy import stats
exp = np.array([0.38,0.22,0.31,0.09])*100
print(stats.chisquare([38,22,30,10], exp))
```
💡 観測と理論比から計算した期待度数のズレを見る。

**問3. クラスABCの数学の平均（ANOVA）**
```python
from scipy import stats
g = [df[df['クラス']==c]['数学'] for c in ['A','B','C']]
print(stats.f_oneway(*g))
```
💡 ANOVAは「どこかに差がある」まで。どの組かは多重比較で。
""",
},
"04_母分散・F検定・母比率の差.ipynb":{
 "title":"# 統計2級-04. 母分散の検定・分散比(F)・母比率の差\n\n"
   "**🎯 できるようになること**\n- 母分散の検定（カイ二乗）ができる\n"
   "- 2群の分散比(F)・母比率の差を検定できる\n- 等分散かどうかでt検定を使い分けられる\n\n"
   "**前提**：統計2級02・03　/　**所要**：約30分　/　**レベル**：統計検定2級相当",
 "misc":"> ⚠️ **よくある間違い**：2群のt検定で「分散が等しい」と勝手に決めない。"
        "F検定で確認するか、迷ったら**Welch（等分散を仮定しない）**を既定にすると安全。",
 "checks":[code("import numpy as np\na=[2,4,6]; b=[1,2,3]\n"
                "# Q1: 分散比 F = (aの不偏分散)/(bの不偏分散) を ans に\n"
                "ans = None   # 例: np.var(a,ddof=1)/np.var(b,ddof=1)\n"
                "_check('Q1 F', ans, np.var(a,ddof=1)/np.var(b,ddof=1))"),
           code("# Q2: 母分散の検定統計量 χ²=(n-1)s²/σ0²。n=10, s²=6, σ0²=4 のとき ans は？\n"
                "ans = None   # 9*6/4\n_check('Q2 χ²', ans, 9*6/4)"),
           code("from statsmodels.stats.proportion import proportions_ztest\n"
                "# Q3: 申込[84,120]/訪問[1000,1050] の母比率の差の z を ans に\n"
                "ans = None   # 例: proportions_ztest([84,120],[1000,1050])[0]\n"
                "_check('Q3 z', ans, proportions_ztest([84,120],[1000,1050])[0])")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 母分散の検定 | 分散が規定値かをχ²で |\n| 分散比 F検定 | 2群の分散が等しいか |\n"
   "| 等分散/Welch | 等分散仮定する/しないt検定 |\n| 母比率の差 | 2群の割合の差の検定 |",
 "cheat":"# チートシート（分散・比率）\nfrom scipy import stats\n"
   "stats.f.cdf(2.0, 5, 7)                          # F分布の確率\n"
   "stats.ttest_ind([1,2,3],[2,3,4], equal_var=False)   # Welchのt検定\n"
   "from statsmodels.stats.proportion import proportions_ztest\n"
   "proportions_ztest([84,120],[1000,1050])         # 母比率の差",
 "answer":"""# 04_母分散・F検定・母比率の差 ― 解答例（解説つき）

**問1. 加工誤差の分散が規格0.5より大きいか**
```python
import numpy as np
from scipy import stats
d=np.array([10.2,9.7,10.5,9.4,10.8,9.6,10.1,10.6]); n=len(d)
chi2=(n-1)*d.var(ddof=1)/0.5
print(1-stats.chi2.cdf(chi2, n-1))   # 上側p値
```

**問2. 2クラスの分散が等しいか→t検定**
```python
from scipy import stats
A=rng.normal(60,8,20); B=rng.normal(60,15,20)
F=A.var(ddof=1)/B.var(ddof=1)   # まずF検定で等分散を確認
print(stats.ttest_ind(A, B, equal_var=False))   # 非等分散ならWelch
```

**問3. 広告A/Bのクリック率の差**
```python
from statsmodels.stats.proportion import proportions_ztest
print(proportions_ztest([160,180],[2000,1800]))
```
💡 比率の差は z検定。p<0.05 で「差あり」。
""",
},
"05_いろいろな確率分布とベイズ.ipynb":{
 "title":"# 統計2級-05. いろいろな確率分布とベイズの定理\n\n"
   "**🎯 できるようになること**\n- ポアソン・幾何・一様・指数分布の使い所がわかる\n"
   "- 各分布の確率を計算できる\n- ベイズの定理で確率を更新できる\n\n"
   "**前提**：統計3級03（確率分布）　/　**所要**：約30分　/　**レベル**：統計検定2級相当",
 "misc":"> ⚠️ **よくある間違い**：有病率が低いと、検査の感度が高くても**陽性的中率は低い**（ベイズの教訓）。"
        "「検査で陽性＝ほぼ病気」ではありません。",
 "checks":[code("from scipy import stats\n# Q1: 平均3件のポアソンで「0件」の確率を ans に\n"
                "ans = None   # 例: stats.poisson.pmf(0, 3)\n_check('Q1 P(X=0)', ans, stats.poisson.pmf(0, 3))"),
           code("from scipy import stats\n# Q2: 成功率0.2で「3回目に初成功」の確率を ans に\n"
                "ans = None   # 例: stats.geom.pmf(3, 0.2)\n_check('Q2 幾何 P(X=3)', ans, stats.geom.pmf(3, 0.2))"),
           code("# Q3: 有病率0.01・感度0.99・特異度0.95。P(病気|陽性) を ans に\n"
                "ans = None   # .99*.01 / (.99*.01 + .05*.99)\n"
                "_check('Q3 陽性的中率', ans, .99*.01/(.99*.01 + .05*.99))")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| ポアソン分布 | まれな事象の件数 |\n| 幾何分布 | 初成功までの回数 |\n"
   "| 一様分布 | 区間で等確率 |\n| 指数分布 | 次の出来事までの待ち時間 |\n"
   "| ベイズの定理 | 情報で確率を更新 |",
 "cheat":"# チートシート（分布・ベイズ）\nfrom scipy import stats\n"
   "stats.poisson.pmf(2, 3)            # ポアソン\nstats.geom.pmf(3, 0.2)             # 幾何\n"
   "stats.expon.cdf(0.5, scale=1/2)   # 指数\n# ベイズ: P(A|B) = P(B|A)P(A) / P(B)",
 "answer":"""# 05_いろいろな確率分布とベイズ ― 解答例（解説つき）

**問1. エラー平均2件/日（ポアソン）**
```python
from scipy import stats
print(stats.poisson.pmf(0,2), 1-stats.poisson.cdf(3,2))   # 0件 / 4件以上
```

**問2. 成功率10%のガチャ（幾何分布）**
```python
from scipy import stats
print(stats.geom.pmf(5,0.1), 1/0.1)   # 5回目で初当たり / 平均10回
```

**問3. 迷惑メール判定（ベイズ）**
```python
print(.8*.4 / (.8*.4 + .1*.6))   # ≈ 0.842
```
💡 「無料を含む」という情報で、迷惑である確率が40%→84%に更新された。
""",
},
"06_重回帰分析.ipynb":{
 "title":"# 統計2級-06. 重回帰分析\n\n"
   "**🎯 できるようになること**\n- 複数の要因で結果を説明・予測できる\n"
   "- 偏回帰係数・決定係数・係数のp値を読める\n- ダミー変数・多重共線性(VIF)を扱える\n\n"
   "**前提**：統計3級02（相関と回帰）　/　**所要**：約35分　/　**レベル**：統計検定2級相当",
 "misc":"> ⚠️ **よくある間違い**：決定係数R²が高い＝良いモデルとは限らない（過学習・多重共線性に注意）。"
        "また 0/1 の結果（受注/生存など）には重回帰でなく**ロジスティック回帰**が適切。",
 "checks":[code("import statsmodels.formula.api as smf\nr = df['数学'].corr(df['英語'])\n"
                "# Q1: 単回帰 数学~英語 の決定係数は相関係数の2乗。ans に r**2 を入れよう\n"
                "ans = None   # 例: r**2\n"
                "_check('Q1 R^2 = r^2', ans, smf.ols('数学 ~ 英語', data=df).fit().rsquared)"),
           code("# Q2: 3カテゴリの質的変数をダミー変数にすると何本？（基準を1つ除く）を ans に\n"
                "ans = None   # 3 - 1\n_check('Q2 ダミーの本数', ans, 3-1)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 偏回帰係数 | 他を一定にしたときの効き目 |\n| 決定係数 R² | 当てはまりの良さ |\n"
   "| 自由度調整済みR² | 変数の数を考慮 |\n| ダミー変数 | 質的変数を0/1に |\n| 多重共線性(VIF) | 説明変数どうしの強い相関 |",
 "cheat":"# チートシート（重回帰）\nimport statsmodels.formula.api as smf\n"
   "m = smf.ols('数学 ~ 英語 + 国語', data=df).fit()\n"
   "print(m.rsquared, m.rsquared_adj)   # 決定係数・自由度調整済み\n"
   "print(m.params)                     # 偏回帰係数\nprint(m.pvalues)                    # 係数のp値",
 "answer":"""# 06_重回帰分析 ― 解答例（解説つき）

**問1. 英語を数学・国語・勉強時間で説明**
```python
import statsmodels.formula.api as smf
m = smf.ols('英語 ~ 数学 + 国語 + 勉強時間', data=df).fit()
print(m.rsquared, m.pvalues)   # 有意な変数は p<0.05
```

**問2. 商談金額を業界(ダミー)で説明**
```python
smf.ols('商談金額 ~ C(業界)', data=btob).fit().params
```
💡 `C(業界)` で自動的にダミー変数化。係数は基準業界との差。

**問3. クラスのダミーを足すと自由度調整済みR²は？**
```python
smf.ols('英語 ~ 数学 + 国語 + 勉強時間 + C(クラス)', data=df).fit().rsquared_adj
```
💡 効かない変数を足すと、自由度調整済みR²は下がることがある（過剰な変数のペナルティ）。
""",
},
"07_抽出法・実験計画・格差指標.ipynb":{
 "title":"# 統計2級-07. 標本抽出法・実験計画・歪度尖度・ジニ係数\n\n"
   "**🎯 できるようになること**\n- 各種の標本抽出法とフィッシャーの3原則を説明できる\n"
   "- 歪度・尖度で分布の形を表せる\n- ローレンツ曲線・ジニ係数で格差を測れる\n\n"
   "**前提**：統計3級04・05　/　**所要**：約30分　/　**レベル**：統計検定2級相当",
 "misc":"> ⚠️ **よくある間違い**：サンプルを増やしても、**取り方が偏っていれば**誤差（偏り）は減りません。"
        "大事なのは数より**無作為性**（偏りのない抽出）です。",
 "checks":[code("from scipy import stats\n# Q1: 左右対称データ[1,2,3,4,5]の歪度を ans に（ほぼ0）\n"
                "ans = None   # 例: stats.skew([1,2,3,4,5])\n_check('Q1 歪度', ans, stats.skew([1,2,3,4,5]))"),
           code("# Q2: 全員同じ所得[10,10,10,10]のジニ係数を ans に（完全平等）\n"
                "ans = None   # 例: gini([10,10,10,10])[0]\n_check('Q2 ジニ係数', ans, gini([10,10,10,10])[0])"),
           code("# Q3: 1000人中ある層が250人。層化抽出で全体100人取るときその層から何人？を ans に\n"
                "ans = None   # 250/1000*100\n_check('Q3 層の人数', ans, 250/1000*100)")],
 "glossary":"## 📒 用語集 ＆ チートシート\n\n| 用語 | 意味 |\n|---|---|\n"
   "| 単純無作為/系統/層化 | 完全ランダム/一定間隔/層ごと |\n| クラスター/多段 | 集団ごと/段階的 |\n"
   "| フィッシャーの3原則 | 反復・無作為化・局所管理 |\n| 歪度/尖度 | 非対称さ/とがり |\n| ジニ係数 | 格差(0平等〜1独占) |",
 "cheat":"# チートシート（抽出・格差）\nimport pandas as pd, numpy as np\nfrom scipy import stats\n"
   "pop = pd.DataFrame({'id':range(100), '層':np.random.default_rng(0).choice(['A','B'],100)})\n"
   "pop.groupby('層', group_keys=False).sample(5, random_state=1)   # 層化抽出\n"
   "print(stats.skew([1,2,3,10]), stats.kurtosis([1,2,3,10]))      # 歪度・尖度",
 "answer":"""# 07_抽出法・実験計画・格差指標 ― 解答例（解説つき）

**問1. 人数比に応じた層化抽出（合計100人）**
```python
for 層, g in pop.groupby('年代'):
    print(層, round(len(g)/len(pop)*100))   # 各層から取る人数
```
💡 各層を「全体に占める割合」どおりに抽出＝比例配分の層化抽出。

**問2. 数学と国語、より左右対称なのは？**
```python
from scipy import stats
print(stats.skew(df['数学']), stats.skew(df['国語']))   # 歪度が0に近い方が対称
```

**問3. 平等な社会と格差社会のジニ係数**
```python
print(gini([10,10,10,10,10])[0], gini([1,2,5,12,80])[0])   # 0 と 大きい値
```
💡 ジニ係数は0(完全平等)〜1(独占)。格差が大きいほど1に近づく。
""",
},
}

for fname, spec in NB.items():
    p = os.path.join(ROOT, "04_統計_2級", fname)
    nb = json.load(open(p, encoding="utf-8")); cells = nb["cells"]
    for c in cells:
        if c["cell_type"]=="markdown" and "".join(c["source"]).startswith("# 統計2級"):
            if "🎯" not in "".join(c["source"]): c["source"]=spec["title"]
            break
    if not any("🧠 確認テスト" in "".join(c["source"]) for c in cells):
        for i,c in enumerate(cells):
            if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith("---"):
                cells[i:i] = [md(spec["misc"]), md(CHECK_HEADER), code(HELPER)] + spec["checks"]; break
    if not any("📒 用語集" in "".join(c["source"]) for c in cells):
        cells += [md(spec["glossary"]), code(spec["cheat"])]
    json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    ap = os.path.join(ROOT, "解答集/04_統計_2級", fname.replace(".ipynb",".md"))
    os.makedirs(os.path.dirname(ap), exist_ok=True)
    open(ap,"w",encoding="utf-8").write(spec["answer"])
    print("upgraded", fname, "->", len(cells), "cells")
print("=== 2級 rollout done ===")
