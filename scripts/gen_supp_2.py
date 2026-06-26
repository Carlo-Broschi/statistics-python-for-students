from nbbuild import md, code, write_nb

DATA = "../data"
imp = code(
    "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n"
    "from scipy import stats\n"
    "plt.rcParams['axes.unicode_minus'] = False\n"
    "rng = np.random.default_rng(0)"
)

# =====================================================================
# 2級-04 母分散・分散比(F)・母比率の差の検定
# =====================================================================
cells = [
    md("# 統計2級-04. 母分散の検定・分散比(F)・母比率の差の検定\n\n"
       "2級で問われる検定のうち、`02_仮説検定` で扱わなかったものを補います。\n"
       "- 母分散の検定（カイ二乗）\n"
       "- 2つの母分散の比の検定（F検定）\n"
       "- 母比率の差の検定\n"
       "- 2標本t検定の「等分散/非等分散」の使い分け"),
    imp,
    md("## 1. 母分散の検定（カイ二乗分布）\n\n"
       "「ばらつき（分散）が規定値と違うか」を検定。検定統計量は\n"
       "$$ \\chi^2 = \\frac{(n-1)s^2}{\\sigma_0^2} \\sim \\chi^2_{n-1} $$\n\n"
       "例：製品の重さの分散は「4以下」が規格。標本から規格超過を疑えるか。"),
    code("data = np.array([50.5, 49.2, 51.8, 48.6, 52.3, 47.9, 50.1, 53.0, 48.0, 51.2])\n"
         "n = len(data)\n"
         "s2 = data.var(ddof=1)\n"
         "sigma0_2 = 4.0          # 帰無仮説の分散\n"
         "chi2 = (n - 1) * s2 / sigma0_2\n"
         "# 片側(分散が大きい方)の検定\n"
         "p = 1 - stats.chi2.cdf(chi2, df=n - 1)\n"
         "print(f'標本分散 s^2 = {s2:.2f}')\n"
         "print(f'χ² = {chi2:.2f},  p値 = {p:.4f}')\n"
         "print('結論:', '分散は4より大きい' if p < 0.05 else '規格内といえる')"),
    md("## 2. 2つの母分散の比の検定（F検定）\n\n"
       "2グループの**ばらつきが等しいか**を検定。$F = s_1^2 / s_2^2 \\sim F_{n_1-1,\\,n_2-1}$。\n"
       "次の2標本t検定で「等分散かどうか」を判断する前段にもなります。"),
    code("groupA = rng.normal(50, 5, 15)\n"
         "groupB = rng.normal(50, 9, 18)   # Bの方がばらつき大\n"
         "F = groupA.var(ddof=1) / groupB.var(ddof=1)\n"
         "dfA, dfB = len(groupA) - 1, len(groupB) - 1\n"
         "# 両側p値\n"
         "p = 2 * min(stats.f.cdf(F, dfA, dfB), 1 - stats.f.cdf(F, dfA, dfB))\n"
         "print(f'F = {F:.3f},  p値 = {p:.4f}')\n"
         "print('結論:', '分散は等しくない' if p < 0.05 else '等分散といえる')"),
    md("## 3. 2標本t検定：等分散か否かで使い分け\n\n"
       "- **等分散**を仮定 → Student のt検定（`equal_var=True`）\n"
       "- **等分散を仮定しない** → Welch のt検定（`equal_var=False`、実務の既定）"),
    code("# 同じ2群を2通りで検定\n"
         "print('Student (等分散仮定):', stats.ttest_ind(groupA, groupB, equal_var=True))\n"
         "print('Welch  (非等分散)  :', stats.ttest_ind(groupA, groupB, equal_var=False))"),
    md("## 4. 母比率の差の検定\n\n"
       "2つのグループの「割合」に差があるか。A/Bテストの本質です。\n"
       "例：施策前の申込率 vs 施策後の申込率。"),
    code("from statsmodels.stats.proportion import proportions_ztest\n"
         "count = np.array([84, 120])     # 申込数\n"
         "nobs = np.array([1000, 1050])   # 訪問数\n"
         "z, p = proportions_ztest(count, nobs)\n"
         "print(f'A: {count[0]/nobs[0]:.3f},  B: {count[1]/nobs[1]:.3f}')\n"
         "print(f'z = {z:.3f},  p値 = {p:.4f}')\n"
         "print('結論:', '比率に差あり' if p < 0.05 else '差は有意でない')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** ある機械の加工誤差の分散は規格0.5。標本\n"
       "`[10.2,9.7,10.5,9.4,10.8,9.6,10.1,10.6]` から、分散が規格より大きいか検定しよう。\n\n"
       "**問2.** 2クラスのテスト点 A=`rng.normal(60,8,20)`, B=`rng.normal(60,15,20)` で、\n"
       "分散が等しいかF検定し、その結果に応じてt検定（equal_varを選択）をしよう。\n\n"
       "**問3.** 広告Aは2000人中160人、広告Bは1800人中180人がクリック。\n"
       "クリック率に差があるか母比率の差の検定で調べよう。"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "d=np.array([10.2,9.7,10.5,9.4,10.8,9.6,10.1,10.6]); n=len(d)\n"
       "chi2=(n-1)*d.var(ddof=1)/0.5; print(1-stats.chi2.cdf(chi2,n-1))\n\n"
       "print(proportions_ztest([160,180],[2000,1800]))\n"
       "```\n</details>"),
]
write_nb("04_統計_2級/04_母分散・F検定・母比率の差.ipynb", cells)

# =====================================================================
# 2級-05 いろいろな確率分布 と ベイズの定理
# =====================================================================
cells = [
    md("# 統計2級-05. いろいろな確率分布とベイズの定理\n\n"
       "2級では二項・正規以外の分布も出ます。代表的なものと、ベイズの定理を学びます。\n"
       "- ポアソン分布・幾何分布・一様分布・指数分布\n"
       "- ベイズの定理"),
    imp,
    md("## 1. ポアソン分布\n\n"
       "「めったに起きないことが、一定時間に何回起きるか」の分布。平均 λ で決まる。\n"
       "例：1時間の問い合わせ件数、ページの誤植数。\n"
       "$$ P(X=k) = \\frac{\\lambda^k e^{-\\lambda}}{k!}, \\quad 平均=分散=\\lambda $$"),
    code("lam = 3   # 1時間に平均3件\n"
         "k = np.arange(0, 11)\n"
         "plt.bar(k, stats.poisson.pmf(k, lam))\n"
         "plt.title(f'ポアソン分布 λ={lam}'); plt.xlabel('件数'); plt.show()\n"
         "print('1時間に0件の確率:', round(stats.poisson.pmf(0, lam), 4))\n"
         "print('5件以上の確率   :', round(1 - stats.poisson.cdf(4, lam), 4))"),
    md("### 二項分布のポアソン近似\n"
       "$n$ が大きく $p$ が小さいとき、$B(n,p) \\approx Poisson(np)$。"),
    code("print('B(1000, 0.003) で k=2:', round(stats.binom.pmf(2, 1000, 0.003), 5))\n"
         "print('Poisson(3)    で k=2:', round(stats.poisson.pmf(2, 3), 5))"),
    md("## 2. 幾何分布\n\n"
       "「初めて成功するまでの試行回数」の分布。例：当たるまでくじを引く回数。\n"
       "平均は $1/p$。"),
    code("p = 0.2\n"
         "k = np.arange(1, 21)\n"
         "plt.bar(k, stats.geom.pmf(k, p))\n"
         "plt.title(f'幾何分布 p={p}（平均 {1/p:.0f}回）'); plt.show()\n"
         "print('3回目で初成功:', round(stats.geom.pmf(3, p), 4))"),
    md("## 3. 一様分布・指数分布（連続）\n\n"
       "- **一様分布**：ある区間で同じ確からしさ（例：0〜1の乱数）\n"
       "- **指数分布**：次の出来事までの待ち時間（ポアソンと対）。平均 $1/\\lambda$"),
    code("xs = np.linspace(0, 5, 200)\n"
         "fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))\n"
         "ax[0].plot(xs, stats.uniform.pdf(xs, 0, 2)); ax[0].set_title('一様分布 U(0,2)')\n"
         "ax[1].plot(xs, stats.expon.pdf(xs, scale=1/1.5)); ax[1].set_title('指数分布 λ=1.5')\n"
         "plt.show()\n"
         "# 平均2件/時のとき、次の客まで30分以上空く確率\n"
         "print('指数分布 P(待ち>0.5h):', round(1 - stats.expon.cdf(0.5, scale=1/2), 4))"),
    md("## 4. ベイズの定理\n\n"
       "「結果」から「原因の確率」を更新する式。\n"
       "$$ P(A \\mid B) = \\frac{P(B \\mid A)\\,P(A)}{P(B)} $$\n\n"
       "有名な例：検査の的中率。ある病気の有病率1%、検査の感度99%・特異度95%。\n"
       "「陽性だったとき、本当に病気である確率」は？"),
    code("prior = 0.01                 # 有病率 P(病気)\n"
         "sens = 0.99                  # 感度 P(陽性|病気)\n"
         "spec = 0.95                  # 特異度 P(陰性|健康)\n"
         "p_pos = sens * prior + (1 - spec) * (1 - prior)   # P(陽性)\n"
         "posterior = sens * prior / p_pos\n"
         "print(f'P(陽性) = {p_pos:.4f}')\n"
         "print(f'P(病気 | 陽性) = {posterior:.3f}')\n"
         "print('→ 陽性でも実際に病気の確率は約', round(posterior*100), '%（直感より低い！）')"),
    md("> 💡 有病率が低いと、感度が高くても「陽性的中率」は低くなる。\n"
       "これは検診の解釈で実際に問題になる、ベイズの重要な教訓です。"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** あるサイトのエラーは平均して1日2件（ポアソン）。\n"
       "1日に0件の確率と、4件以上の確率を求めよう。\n\n"
       "**問2.** 成功率10%のガチャ。初当たりが5回目になる確率（幾何分布）と、平均回数を求めよう。\n\n"
       "**問3.** 迷惑メールは全体の40%。『無料』を含むメールのうち迷惑は80%、\n"
       "通常メールで『無料』を含むのは10%。\n"
       "『無料』を含むメールが迷惑メールである確率をベイズの定理で求めよう。"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(stats.poisson.pmf(0,2), 1-stats.poisson.cdf(3,2))\n"
       "print(stats.geom.pmf(5,0.1), 1/0.1)\n"
       "# P(迷惑|無料) = .8*.4 / (.8*.4 + .1*.6)\n"
       "print(.8*.4 / (.8*.4 + .1*.6))   # ≈ 0.842\n"
       "```\n</details>"),
]
write_nb("04_統計_2級/05_いろいろな確率分布とベイズ.ipynb", cells)

# =====================================================================
# 2級-06 重回帰分析
# =====================================================================
cells = [
    md("# 統計2級-06. 重回帰分析\n\n"
       "複数の説明変数から1つの結果を予測・説明するのが**重回帰**。\n"
       "2級頻出の、決定係数・偏回帰係数・回帰係数の検定・ダミー変数・多重共線性を学びます。"),
    code("import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n"
         "import statsmodels.formula.api as smf\n"
         "plt.rcParams['axes.unicode_minus'] = False\n"
         f"df = pd.read_csv('{DATA}/students_scores.csv')\n"
         "df.head()"),
    md("## 1. 単回帰の復習 → 重回帰へ\n\n"
       "`数学` を `英語`・`国語`・`勉強時間` から説明します。\n"
       "$$ 数学 = b_0 + b_1\\,英語 + b_2\\,国語 + b_3\\,勉強時間 $$\n\n"
       "`statsmodels` を使うと、表計算ソフトのような回帰の出力が得られます。"),
    code("model = smf.ols('数学 ~ 英語 + 国語 + 勉強時間', data=df).fit()\n"
         "print(model.summary())"),
    md("## 2. 出力の読み方（2級の頻出ポイント）\n\n"
       "- **coef（偏回帰係数）**：他の変数を一定にしたとき、その変数が1増えると数学が何点変わるか\n"
       "- **R-squared（決定係数）**：当てはまりの良さ（0〜1、1に近いほど良い）\n"
       "- **Adj. R-squared（自由度調整済み）**：変数の数を考慮した決定係数。変数比較に使う\n"
       "- **P>|t|（回帰係数の検定）**：その変数が本当に効いているか（0.05未満で有意）"),
    code("print('決定係数 R^2      :', round(model.rsquared, 3))\n"
         "print('自由度調整済み R^2:', round(model.rsquared_adj, 3))\n"
         "print('\\n偏回帰係数:')\n"
         "print(model.params.round(3))\n"
         "print('\\n各係数のp値:')\n"
         "print(model.pvalues.round(4))"),
    md("## 3. 予測してみる"),
    code("new = pd.DataFrame({'英語':[70], '国語':[75], '勉強時間':[2.0]})\n"
         "print('予測される数学の点数:', round(model.predict(new)[0], 1))"),
    md("## 4. ダミー変数（質的データを回帰に入れる）\n\n"
       "`クラス`(A/B/C)のような質的変数は、0/1の**ダミー変数**にして投入します。\n"
       "`C(クラス)` と書くと自動でダミー化されます。"),
    code("model2 = smf.ols('数学 ~ 英語 + C(クラス)', data=df).fit()\n"
         "print(model2.params.round(2))\n"
         "print('→ [T.B],[T.C] は基準クラスAと比べた差を表す')"),
    md("## 5. 多重共線性（マルチコ）\n\n"
       "説明変数どうしが強く相関していると、係数が不安定になる問題。\n"
       "**VIF**（分散拡大係数）で確認します。VIFが10を超えると要注意。"),
    code("from statsmodels.stats.outliers_influence import variance_inflation_factor\n"
         "X = df[['英語', '国語', '勉強時間']].copy()\n"
         "X['const'] = 1\n"
         "vif = pd.Series(\n"
         "    [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],\n"
         "    index=X.columns)\n"
         "print(vif.round(2))\n"
         "print('→ const以外が10未満なら多重共線性は問題なし')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `英語` を `数学`・`国語`・`勉強時間` で説明する重回帰を作り、\n"
       "決定係数と、有意な（p<0.05）説明変数を答えよう。\n\n"
       "**問2.** `sales_btob.csv` で `商談金額` を `業界`（ダミー）で説明する回帰を作り、\n"
       "どの業界が金額を押し上げ／押し下げているか読み取ろう。\n\n"
       "**問3.** 問1のモデルに`クラス`のダミーを加えると自由度調整済みR²は上がる？下がる？確かめよう。"),
    code("# 問1\n"),
    code(f"# 問2\nbtob = pd.read_csv('{DATA}/sales_btob.csv')\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "m = smf.ols('英語 ~ 数学 + 国語 + 勉強時間', data=df).fit()\n"
       "print(m.rsquared, m.pvalues)\n"
       "smf.ols('商談金額 ~ C(業界)', data=btob).fit().params\n"
       "```\n</details>"),
]
write_nb("04_統計_2級/06_重回帰分析.ipynb", cells)

# =====================================================================
# 2級-07 データ収集法と記述統計の残り
# =====================================================================
cells = [
    md("# 統計2級-07. 標本抽出法・実験計画・歪度尖度・ジニ係数\n\n"
       "2級の出題範囲のうち、残りのトピックをまとめて押さえます。\n"
       "- 各種の標本抽出法、フィッシャーの3原則\n"
       "- 分布の形：歪度・尖度\n"
       "- 格差の指標：ローレンツ曲線・ジニ係数"),
    imp,
    md("## 1. 標本抽出法\n\n"
       "母集団から標本を取る代表的な方法。**偏りを防ぐ**のが目的です。\n\n"
       "| 方法 | やり方 | 特徴 |\n"
       "|---|---|---|\n"
       "| 単純無作為抽出 | 全員から完全にランダム | 基本だが手間 |\n"
       "| 系統抽出 | 名簿から一定間隔で抽出 | 簡単／周期に注意 |\n"
       "| 層化抽出 | 層（年代等）に分け各層から抽出 | 各層を確実に代表 |\n"
       "| クラスター抽出 | 集団(学校等)ごと抽出し全数調査 | コスト減／誤差増 |\n"
       "| 多段抽出 | 段階的に抽出（県→市→人） | 大規模調査で実用的 |"),
    code("rng = np.random.default_rng(1)\n"
         "pop = pd.DataFrame({'id': range(1, 1001),\n"
         "                    '年代': rng.choice(['10代','20代','30代','40代'], 1000)})\n\n"
         "# 単純無作為抽出\n"
         "simple = pop.sample(n=40, random_state=1)\n"
         "# 系統抽出（25人おき）\n"
         "systematic = pop.iloc[rng.integers(0,25)::25]\n"
         "# 層化抽出（各年代から10人ずつ）\n"
         "strat = pop.groupby('年代', group_keys=False).sample(n=10, random_state=1)\n"
         "print('単純無作為:', len(simple), '人')\n"
         "print('系統抽出  :', len(systematic), '人')\n"
         "print('層化抽出の年代構成:\\n', strat['年代'].value_counts())"),
    md("## 2. フィッシャーの3原則（実験計画）\n\n"
       "実験で正しく効果を測るための3原則。\n\n"
       "1. **反復**：同じ条件を複数回 → 偶然のばらつきを評価できる\n"
       "2. **無作為化（ランダム化）**：処理の割り当てをランダムに → 偏りを防ぐ\n"
       "3. **局所管理（ブロック化）**：似た条件をブロックにまとめて比較 → 誤差を小さく\n\n"
       "> これらは一元配置分散分析（`04_統計_2級/03`）の前提になっています。"),
    md("## 3. 歪度（わいど）と尖度（せんど）\n\n"
       "分布の「形」を数で表す指標。\n"
       "- **歪度**：左右の非対称さ。正なら右に裾が長い、負なら左に裾\n"
       "- **尖度**：尖り具合・裾の重さ（正規分布を基準0とする定義）"),
    code("normal_data = rng.normal(0, 1, 5000)\n"
         "right_skew = rng.exponential(1, 5000)   # 右に裾が長い\n"
         "for name, d in [('正規っぽい', normal_data), ('右に裾(指数)', right_skew)]:\n"
         "    print(f'{name}: 歪度={stats.skew(d):.2f}, 尖度={stats.kurtosis(d):.2f}')\n\n"
         "plt.hist(right_skew, bins=40); plt.title('右に裾が長い分布（歪度>0）'); plt.show()"),
    md("## 4. ローレンツ曲線とジニ係数\n\n"
       "所得などの**格差・不平等**を測る指標。\n"
       "- ローレンツ曲線：人を所得の低い順に並べ、累積人口比と累積所得比を描く\n"
       "- ジニ係数：完全平等線とローレンツ曲線で囲む面積の2倍。0(平等)〜1(独占)"),
    code("def gini(x):\n"
         "    x = np.sort(np.asarray(x, float))\n"
         "    n = len(x)\n"
         "    cum = np.cumsum(x) / x.sum()\n"
         "    lorenz = np.insert(cum, 0, 0)\n"
         "    pop = np.linspace(0, 1, n + 1)\n"
         "    area = np.sum(np.diff(pop) * (lorenz[:-1] + lorenz[1:]) / 2)  # 台形則\n"
         "    g = 1 - 2 * area\n"
         "    return g, pop, lorenz\n\n"
         "incomes = rng.lognormal(3, 0.6, 500)   # 所得（不平等あり）\n"
         "g, popshare, lorenz = gini(incomes)\n"
         "plt.plot(popshare, lorenz, label='ローレンツ曲線')\n"
         "plt.plot([0,1],[0,1],'--', label='完全平等線')\n"
         "plt.xlabel('累積人口比'); plt.ylabel('累積所得比')\n"
         "plt.title(f'ジニ係数 = {g:.3f}'); plt.legend(); plt.show()"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** 1000人の母集団から、層化抽出で各年代から**人数比に応じて**合計100人を抽出しよう\n"
       "（ヒント：各層 `len(層)/1000*100` 人）。\n\n"
       "**問2.** `students_scores.csv` の `数学`・`国語` の歪度を比べ、より左右対称なのはどちらか答えよう。\n\n"
       "**問3.** 2つの社会 `A=[10,10,10,10,10]`（平等）と `B=[1,2,5,12,80]`（格差大）の\n"
       "ジニ係数を計算し、値の大小と直感が合うか確かめよう。"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "import pandas as pd\n"
       "df = pd.read_csv('../data/students_scores.csv')\n"
       "print(stats.skew(df['数学']), stats.skew(df['国語']))\n"
       "print(gini([10,10,10,10,10])[0], gini([1,2,5,12,80])[0])  # 0 vs 大\n"
       "```\n</details>\n\n"
       "🎉 これで**統計検定2級の主要範囲を大幅にカバー**しました。"),
]
write_nb("04_統計_2級/07_抽出法・実験計画・格差指標.ipynb", cells)

print("=== 2級拡充 done ===")
