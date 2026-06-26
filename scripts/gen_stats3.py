from nbbuild import md, code, write_nb

DATA = "../data"
setup = code(
    "import numpy as np\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "from scipy import stats\n"
    "plt.rcParams['axes.unicode_minus'] = False\n"
    f"df = pd.read_csv('{DATA}/students_scores.csv')\n"
    "df.head()"
)

# =====================================================================
# 01 分散・標準偏差・標準化
# =====================================================================
cells = [
    md("# 統計3級-01. 分散・標準偏差・標準化\n\n"
       "ばらつきを「1つの数」で表す本格的な指標を学びます。\n"
       "偏差値の正体もここでわかります。"),
    setup,
    md("## 1. 偏差 → 分散 → 標準偏差\n\n"
       "1. **偏差** = 各データ − 平均（平均からのズレ）\n"
       "2. **分散** = 偏差を2乗して平均したもの\n"
       "3. **標準偏差** = 分散の平方根（単位が元データと同じに戻る）\n\n"
       "$$ 分散\\ s^2 = \\frac{1}{n}\\sum (x_i - \\bar{x})^2, \\quad 標準偏差\\ s = \\sqrt{s^2} $$"),
    code("x = np.array([60, 70, 80, 90, 100])\n"
         "mean = x.mean()\n"
         "deviation = x - mean\n"
         "print('偏差:', deviation)\n"
         "print('分散:', np.mean(deviation**2))         # 手計算\n"
         "print('分散(np):', x.var())                   # numpyは標本分散(÷n)\n"
         "print('標準偏差:', x.std().round(2))"),
    md("> ⚠️ 分散には2種類あります。`÷n`（母分散）と `÷(n-1)`（不偏分散）。\n"
       "pandasの `.var()` は既定で `÷(n-1)`、numpyは `÷n`。3級では区別を意識しましょう。"),
    code("s = pd.Series([60, 70, 80, 90, 100])\n"
         "print('pandas .var() ÷(n-1):', s.var())\n"
         "print('numpy  .var() ÷n   :', np.var(s))\n"
         "print('ddof指定で合わせる :', np.var(s, ddof=1))"),
    md("## 2. データを比べる：標準化（z得点）\n\n"
       "単位や平均が違うデータを公平に比べるため、\n"
       "$$ z = \\frac{x - 平均}{標準偏差} $$\n"
       "に変換します。平均0・標準偏差1になります。"),
    code("math = df['数学']\n"
         "z = (math - math.mean()) / math.std()\n"
         "print('標準化後の平均:', round(z.mean(), 5), ' 標準偏差:', round(z.std(), 3))"),
    md("## 3. 偏差値\n\n"
       "z得点を見やすくしたものが偏差値です。\n"
       "$$ 偏差値 = 50 + 10 \\times z $$\n"
       "平均が偏差値50、標準偏差が10になります。"),
    code("df['数学偏差値'] = 50 + 10 * (math - math.mean()) / math.std()\n"
         "df[['生徒ID', '数学', '数学偏差値']].sort_values('数学', ascending=False).head()"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `[2, 4, 6, 8, 10]` の分散と標準偏差を手計算の式で求めよう。\n\n"
       "**問2.** ある生徒は数学70点、英語70点だった。`数学`と`英語`それぞれで偏差値を計算し、\n"
       "「どちらの教科のほうが相対的に良かったか」を答えよう。\n\n"
       "**問3.** `国語` の偏差値列を作り、偏差値60以上の生徒が何人いるか数えよう。"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "x = np.array([2,4,6,8,10]); print(np.var(x), np.std(x))  # 8, 2.83\n"
       "for col in ['数学','英語']:\n"
       "    m, s = df[col].mean(), df[col].std()\n"
       "    print(col, 50 + 10*(70-m)/s)\n"
       "kokugo_hensa = 50 + 10*(df['国語']-df['国語'].mean())/df['国語'].std()\n"
       "print((kokugo_hensa >= 60).sum())\n"
       "```\n</details>"),
]
write_nb("03_統計_3級/01_分散・標準偏差・標準化.ipynb", cells)

# =====================================================================
# 02 相関と回帰
# =====================================================================
cells = [
    md("# 統計3級-02. 相関と回帰直線\n\n"
       "2つの量の関係を、散布図・相関係数・回帰直線で分析します。"),
    setup,
    md("## 1. 散布図\n\n"
       "2つの量的データの関係を点で表します。ここでは「数学」と「英語」の関係を見ます。"),
    code("plt.figure(figsize=(6, 5))\n"
         "plt.scatter(df['数学'], df['英語'], alpha=0.6)\n"
         "plt.xlabel('数学')\n"
         "plt.ylabel('英語')\n"
         "plt.title('数学と英語の関係')\n"
         "plt.show()"),
    md("## 2. 相関係数 r\n\n"
       "関係の強さを −1〜+1 の数で表します。\n\n"
       "| r の値 | 関係 |\n|---|---|\n"
       "| +0.7〜+1.0 | 強い正の相関 |\n"
       "| +0.4〜+0.7 | やや正の相関 |\n"
       "| −0.2〜+0.2 | ほぼ無相関 |\n"
       "| −1.0〜−0.7 | 強い負の相関 |"),
    code("r = df['数学'].corr(df['英語'])\n"
         "print('相関係数 r =', round(r, 3))\n\n"
         "# 全教科の相関行列\n"
         "df[['数学', '英語', '国語', '勉強時間']].corr().round(2)"),
    md("> ⚠️ **相関 ≠ 因果**。「アイスの売上」と「水難事故」は相関するが、\n"
       "原因は両方とも「気温（夏）」。見かけの相関に注意！"),
    md("## 3. 回帰直線（最小二乗法）\n\n"
       "点の真ん中を通る直線 `y = a·x + b` を引き、xからyを予測します。"),
    code("x = df['数学']\n"
         "y = df['英語']\n"
         "a, b = np.polyfit(x, y, 1)   # 傾きa・切片b\n"
         "print(f'回帰直線: y = {a:.2f} x + {b:.2f}')\n\n"
         "plt.figure(figsize=(6, 5))\n"
         "plt.scatter(x, y, alpha=0.5)\n"
         "xs = np.linspace(x.min(), x.max(), 100)\n"
         "plt.plot(xs, a * xs + b, color='red', label=f'y={a:.2f}x+{b:.2f}')\n"
         "plt.xlabel('数学'); plt.ylabel('英語'); plt.legend()\n"
         "plt.show()"),
    md("### 予測してみる\n"
       "数学が85点の人の英語を予測すると？"),
    code("pred = a * 85 + b\n"
         "print(f'数学85点 → 英語の予測 {pred:.1f}点')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `勉強時間` と `数学` の散布図を描き、相関係数を求めよう。正の相関はある？\n\n"
       "**問2.** `勉強時間`(x) から `数学`(y) を予測する回帰直線を求め、\n"
       "「3時間勉強した人」の数学点数を予測しよう。\n\n"
       "**問3.** `国語` と `数学` の相関係数を求めよう。関係は強い？弱い？"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(df['勉強時間'].corr(df['数学']))\n"
       "a,b = np.polyfit(df['勉強時間'], df['数学'], 1)\n"
       "print(a*3+b)\n"
       "print(df['国語'].corr(df['数学']))\n"
       "```\n</details>"),
]
write_nb("03_統計_3級/02_相関と回帰.ipynb", cells)

# =====================================================================
# 03 確率分布（二項分布・正規分布）
# =====================================================================
cells = [
    md("# 統計3級-03. 確率分布（二項分布・正規分布）\n\n"
       "「ばらつき方のパターン」を数式で表したものが確率分布です。"),
    code("import numpy as np\nimport matplotlib.pyplot as plt\nfrom scipy import stats\n"
         "plt.rcParams['axes.unicode_minus'] = False"),
    md("## 1. 二項分布\n\n"
       "「成功確率 p の試行を n 回くり返したときの成功回数」の分布。\n"
       "例：コインを10回投げて表が出る回数。"),
    code("n, p = 10, 0.5\n"
         "k = np.arange(0, n + 1)\n"
         "prob = stats.binom.pmf(k, n, p)\n\n"
         "plt.bar(k, prob)\n"
         "plt.xlabel('表が出た回数'); plt.ylabel('確率')\n"
         "plt.title(f'二項分布 B(n={n}, p={p})')\n"
         "plt.show()\n"
         "print('平均(np):', n*p, ' 標準偏差:', round(np.sqrt(n*p*(1-p)), 2))"),
    code("# 表がちょうど7回出る確率\n"
         "print('P(X=7) =', round(stats.binom.pmf(7, 10, 0.5), 4))\n"
         "# 表が8回以上出る確率\n"
         "print('P(X>=8) =', round(1 - stats.binom.cdf(7, 10, 0.5), 4))"),
    md("## 2. 正規分布\n\n"
       "自然界・社会で最もよく現れる、左右対称のつりがね型。\n"
       "身長・テストの点数などが近似的に従います。"),
    code("mu, sigma = 50, 10   # 平均50, 標準偏差10（偏差値の分布）\n"
         "x = np.linspace(10, 90, 200)\n"
         "y = stats.norm.pdf(x, mu, sigma)\n"
         "plt.plot(x, y)\n"
         "plt.axvline(mu, color='red', linestyle='--', label='平均')\n"
         "plt.title('正規分布 N(50, 10²)'); plt.legend()\n"
         "plt.show()"),
    md("## 3. 68-95-99.7 ルール\n\n"
       "正規分布では、平均から\n"
       "- ±1σ の範囲に約 **68%**\n"
       "- ±2σ の範囲に約 **95%**\n"
       "- ±3σ の範囲に約 **99.7%**\n"
       "のデータが入ります。"),
    code("for k in [1, 2, 3]:\n"
         "    p = stats.norm.cdf(k) - stats.norm.cdf(-k)\n"
         "    print(f'±{k}σ の中に {p*100:.1f}%')"),
    md("### 確率の計算（標準化を使う）\n"
       "偏差値が70以上（平均50,σ10）の人は何%？"),
    code("# z = (70-50)/10 = 2.0 → 上側の確率\n"
         "p = 1 - stats.norm.cdf(70, 50, 10)\n"
         "print(f'偏差値70以上は上位 {p*100:.1f}%')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** サイコロを12回ふって「1の目」がちょうど2回出る確率を二項分布で求めよう（p=1/6）。\n\n"
       "**問2.** 平均170cm・標準偏差6cmの身長分布で、176cm以上の人の割合を求めよう。\n\n"
       "**問3.** 同じ身長分布で、164cm〜176cm（±1σ）に入る割合を求め、68%に近いか確かめよう。"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(stats.binom.pmf(2, 12, 1/6))             # 約0.296\n"
       "print(1 - stats.norm.cdf(176, 170, 6))         # 約0.159\n"
       "print(stats.norm.cdf(176,170,6) - stats.norm.cdf(164,170,6))  # 約0.683\n"
       "```\n</details>"),
]
write_nb("03_統計_3級/03_確率分布.ipynb", cells)

# =====================================================================
# 04 母集団と標本・推定の入口
# =====================================================================
cells = [
    md("# 統計3級-04. 母集団と標本・推定の入口\n\n"
       "一部を調べて全体を知る「標本調査」の考え方を学びます。\n"
       "2級の推定・検定への橋渡しです。"),
    code("import numpy as np\nimport matplotlib.pyplot as plt\nfrom scipy import stats\n"
         "plt.rcParams['axes.unicode_minus'] = False\n"
         "rng = np.random.default_rng(7)"),
    md("## 1. 母集団と標本\n\n"
       "- **母集団**：本当に知りたい全体（例：日本の高校生全員の身長）\n"
       "- **標本**：実際に調べた一部（例：100人の身長）\n"
       "- **標本平均**から**母平均**を推測する\n\n"
       "全数調査が難しいので、標本調査で代用します。"),
    md("仮想の母集団（平均165, 標準偏差8の身長10万人）を作り、そこから標本を取ってみます。"),
    code("population = rng.normal(165, 8, 100000)\n"
         "print('母平均:', population.mean().round(2))\n\n"
         "sample = rng.choice(population, size=100)\n"
         "print('標本平均(100人):', sample.mean().round(2))\n"
         "print('→ 全部調べなくても、母平均にかなり近い！')"),
    md("## 2. 標本平均はばらつく（標本分布）\n\n"
       "標本を取り直すたびに標本平均は少し変わります。\n"
       "「標本平均を何度も計算した分布」を調べます。"),
    code("means = [rng.choice(population, 100).mean() for _ in range(2000)]\n"
         "plt.hist(means, bins=40, edgecolor='white')\n"
         "plt.axvline(165, color='red', linestyle='--', label='母平均')\n"
         "plt.title('標本平均の分布（n=100を2000回）'); plt.legend()\n"
         "plt.show()\n"
         "print('標本平均たちの平均:', np.mean(means).round(2))\n"
         "print('標本平均たちの標準偏差:', np.std(means).round(3))"),
    md("### 中心極限定理\n"
       "標本平均の分布は、サンプルサイズ n が大きいほど**正規分布に近づき**、\n"
       "その標準偏差（=標準誤差）は\n"
       "$$ 標準誤差 = \\frac{母標準偏差}{\\sqrt{n}} $$\n"
       "で小さくなります。「nを増やすほど推定が正確になる」根拠です。"),
    code("for n in [25, 100, 400]:\n"
         "    se = 8 / np.sqrt(n)\n"
         "    print(f'n={n:3d} → 標準誤差 {se:.3f}（nが4倍で誤差は半分）')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `population` から n=400 の標本を取り、標本平均を母平均165と比べよう。\n"
       "n=100のときとどちらが近い？\n\n"
       "**問2.** 母標準偏差が10のとき、標準誤差を0.5以下にするには n をいくつにすればよい？\n"
       "（ヒント：`10/√n <= 0.5` を解く）\n\n"
       "**問3.** なぜテレビの視聴率や選挙の出口調査は、全員に聞かなくても当たるのか、\n"
       "この章の言葉（標本・標準誤差）を使って説明しよう。"),
    code("# 問1\n"),
    code("# 問2\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(rng.choice(population, 400).mean())  # 165により近い\n"
       "# 10/√n <= 0.5 → √n >= 20 → n >= 400\n"
       "```\n"
       "問3: 無作為に十分な数の標本を取れば、標本平均は母平均の近くに集中し（標準誤差が小さい）、\n"
       "全数調査しなくても全体の傾向を高い精度で推測できるから。\n</details>\n\n"
       "🎉 **統計3級レベル クリア！** 次は `04_統計_2級` へ。"),
]
write_nb("03_統計_3級/04_母集団と標本.ipynb", cells)

print("=== 統計3級 done ===")
