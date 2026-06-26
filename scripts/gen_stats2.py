from nbbuild import md, code, write_nb

DATA = "../data"
imp = code(
    "import numpy as np\n"
    "import pandas as pd\n"
    "import matplotlib.pyplot as plt\n"
    "from scipy import stats\n"
    "plt.rcParams['axes.unicode_minus'] = False\n"
    "rng = np.random.default_rng(0)"
)

# =====================================================================
# 01 区間推定
# =====================================================================
cells = [
    md("# 統計2級-01. 区間推定（信頼区間）\n\n"
       "標本から母平均・母比率を「幅をもって」推定します。\n\n"
       "> ⚠️ ここからは統計検定2級レベル。3級までを終えてから取り組みましょう。"),
    imp,
    md("## 1. 点推定 と 区間推定\n\n"
       "- **点推定**：標本平均をそのまま母平均の推定値とする（1つの値）\n"
       "- **区間推定**：「母平均はこの範囲にありそう」と幅で示す\n\n"
       "95%信頼区間とは「同じ調査を100回やれば95回はこの区間が母平均を含む」という意味です。"),
    md("## 2. 母平均の信頼区間（母分散が未知 → t分布）\n\n"
       "$$ \\bar{x} \\pm t_{\\,0.025,\\,n-1} \\times \\frac{s}{\\sqrt{n}} $$\n\n"
       "ある商品の内容量を10個測ったデータで計算します。"),
    code("data = np.array([198, 203, 197, 205, 199, 201, 196, 204, 200, 202])\n"
         "n = len(data)\n"
         "mean = data.mean()\n"
         "s = data.std(ddof=1)            # 不偏標準偏差\n"
         "se = s / np.sqrt(n)             # 標準誤差\n"
         "t = stats.t.ppf(0.975, df=n-1)  # 自由度n-1のt値\n"
         "low, high = mean - t*se, mean + t*se\n"
         "print(f'標本平均: {mean:.2f}')\n"
         "print(f'95%信頼区間: [{low:.2f}, {high:.2f}]')"),
    code("# scipyに任せると1行\n"
         "ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)\n"
         "print('95%CI:', np.round(ci, 2))"),
    md("> 💡 信頼度を上げる（95%→99%）と区間は**広く**なり、\n"
       "サンプル数 n を増やすと区間は**狭く**なります（推定が精密に）。"),
    code("for conf in [0.90, 0.95, 0.99]:\n"
         "    lo, hi = stats.t.interval(conf, df=n-1, loc=mean, scale=se)\n"
         "    print(f'{int(conf*100)}%CI 幅 = {hi-lo:.2f}')"),
    md("## 3. 母比率の信頼区間\n\n"
       "アンケートで400人中96人が「賛成」。賛成率の95%信頼区間は？\n\n"
       "$$ \\hat{p} \\pm 1.96\\sqrt{\\frac{\\hat{p}(1-\\hat{p})}{n}} $$"),
    code("x, n = 96, 400\n"
         "p = x / n\n"
         "se = np.sqrt(p * (1 - p) / n)\n"
         "z = stats.norm.ppf(0.975)   # 1.96\n"
         "print(f'賛成率の推定: {p:.3f}')\n"
         "print(f'95%信頼区間: [{p - z*se:.3f}, {p + z*se:.3f}]')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** あるクラス16人の小テスト平均が72点、不偏標準偏差が8点。\n"
       "母平均の95%信頼区間を求めよう（t分布, 自由度15）。\n\n"
       "**問2.** 1000人アンケートで320人が「利用したい」。利用率の95%信頼区間を求めよう。\n\n"
       "**問3.** 問2で誤差（区間の半分）を ±2% 以内にしたい。n は何人必要か概算しよう\n"
       "（ヒント：`1.96*sqrt(0.32*0.68/n) <= 0.02`）。"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "se = 8/np.sqrt(16); print(stats.t.interval(0.95, 15, 72, se))  # 約[67.7,76.3]\n"
       "p=320/1000; se=np.sqrt(p*0.68/1000); print(p-1.96*se, p+1.96*se)\n"
       "# n >= (1.96^2 * 0.32*0.68)/0.02^2 ≈ 2089人\n"
       "print((1.96**2 * 0.32*0.68)/0.02**2)\n"
       "```\n</details>"),
]
write_nb("04_統計_2級/01_区間推定.ipynb", cells)

# =====================================================================
# 02 仮説検定
# =====================================================================
cells = [
    md("# 統計2級-02. 仮説検定\n\n"
       "「偶然では説明しにくい差か？」を確率で判断する方法を学びます。\n"
       "統計検定2級の中心テーマです。"),
    imp,
    md("## 1. 検定の考え方（5ステップ）\n\n"
       "1. **帰無仮説 H₀**：差はない（例：平均は200である）\n"
       "2. **対立仮説 H₁**：差がある（例：平均は200でない）\n"
       "3. **有意水準 α** を決める（ふつう 0.05）\n"
       "4. データから **検定統計量** と **p値** を計算\n"
       "5. **p値 < α なら H₀ を棄却**（＝差があると判断）\n\n"
       "> p値 = 「H₀が正しいと仮定したとき、観測されたような差が偶然起こる確率」"),
    md("## 2. 1標本t検定（母平均の検定）\n\n"
       "ある工場のお菓子は「内容量200g」とうたっている。\n"
       "標本を測ったら本当に200gといえるか？"),
    code("data = np.array([198, 203, 197, 205, 199, 201, 196, 204, 200, 197,\n"
         "                 195, 199, 198, 200, 196])\n"
         "t_stat, p = stats.ttest_1samp(data, popmean=200)\n"
         "print(f'標本平均: {data.mean():.2f}')\n"
         "print(f't統計量: {t_stat:.3f},  p値: {p:.3f}')\n"
         "alpha = 0.05\n"
         "print('結論:', '200gと言えない（棄却）' if p < alpha else '200gでないとは言えない')"),
    md("## 3. 2標本t検定（2グループの平均の差）\n\n"
       "新しい教え方(B)は従来(A)より点数が高いか？ 2クラスを比較します。"),
    code("classA = rng.normal(62, 12, 30)\n"
         "classB = rng.normal(70, 12, 30)\n"
         "t_stat, p = stats.ttest_ind(classA, classB)\n"
         "print(f'Aの平均 {classA.mean():.1f}, Bの平均 {classB.mean():.1f}')\n"
         "print(f't={t_stat:.3f}, p={p:.4f}')\n"
         "print('結論:', '差は有意' if p < 0.05 else '差は有意でない')"),
    md("## 4. 母比率の検定（A/Bテストの前ふり）\n\n"
       "サイコロを600回ふって1の目が80回。「いかさま（出やすい）」と言えるか？\n"
       "理論値は 600 × 1/6 = 100 回。"),
    code("from statsmodels.stats.proportion import proportions_ztest\n"
         "count, nobs = 80, 600\n"
         "z, p = proportions_ztest(count, nobs, value=1/6, alternative='two-sided')\n"
         "print(f'観測比率 {count/nobs:.3f} (理論 {1/6:.3f})')\n"
         "print(f'z={z:.3f}, p={p:.4f}')\n"
         "print('結論:', 'いかさまの疑い' if p < 0.05 else '偶然の範囲')"),
    md("> 📝 **第1種・第2種の誤り**\n"
       "> - 第1種の誤り：本当は差がないのに「ある」とする（確率=α）\n"
       "> - 第2種の誤り：本当は差があるのに「ない」とする（確率=β）"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** ある飲料の糖度は「平均10度」とされる。標本\n"
       "`[10.5,9.8,10.2,11.0,10.7,10.1,10.9,10.4]` で、10度といえるか1標本t検定で調べよう。\n\n"
       "**問2.** `sales_btob.csv` で「展示会」と「Web広告」の商談金額の平均に差があるか、\n"
       "2標本t検定で調べよう。\n\n"
       "**問3.** コインを100回投げて表が60回。「ゆがんだコイン」と言えるか母比率の検定で調べよう。"),
    code("# 問1\n"),
    code(f"# 問2\nbtob = pd.read_csv('{DATA}/sales_btob.csv')\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(stats.ttest_1samp([10.5,9.8,10.2,11.0,10.7,10.1,10.9,10.4], 10))\n"
       "a = btob[btob['獲得チャネル']=='展示会']['商談金額']\n"
       "b = btob[btob['獲得チャネル']=='Web広告']['商談金額']\n"
       "print(stats.ttest_ind(a, b))\n"
       "print(proportions_ztest(60, 100, 0.5))  # p≈0.045 → ゆがみあり\n"
       "```\n</details>"),
]
write_nb("04_統計_2級/02_仮説検定.ipynb", cells)

# =====================================================================
# 03 カイ二乗検定と分散分析
# =====================================================================
cells = [
    md("# 統計2級-03. カイ二乗検定・分散分析(ANOVA)\n\n"
       "- **カイ二乗検定**：質的データの関連を調べる\n"
       "- **分散分析**：3グループ以上の平均を一度に比較する"),
    imp,
    md("## 1. カイ二乗 独立性の検定\n\n"
       "「獲得チャネル」と「受注の有無」に関連があるか？\n"
       "クロス集計表をもとに検定します。"),
    code(f"btob = pd.read_csv('{DATA}/sales_btob.csv')\n"
         "table = pd.crosstab(btob['獲得チャネル'], btob['受注'])\n"
         "print(table)\n"
         "chi2, p, dof, expected = stats.chi2_contingency(table)\n"
         "print(f'\\nカイ二乗統計量: {chi2:.2f}')\n"
         "print(f'自由度: {dof},  p値: {p:.5f}')\n"
         "print('結論:', 'チャネルと受注に関連あり' if p < 0.05 else '関連があるとは言えない')"),
    md("**期待度数**（関連がないと仮定したときの理論値）と実測のズレが大きいほど χ² は大きくなります。"),
    code("pd.DataFrame(expected, index=table.index, columns=table.columns).round(1)"),
    md("## 2. カイ二乗 適合度の検定\n\n"
       "サイコロを各目こう出た：`[18,21,16,14,17,14]`（計100回）。\n"
       "「6つの目が均等(各1/6)」といえるか？"),
    code("observed = np.array([18, 21, 16, 14, 17, 14])\n"
         "expected = np.full(6, observed.sum() / 6)   # 各16.67\n"
         "chi2, p = stats.chisquare(observed, expected)\n"
         "print(f'chi2={chi2:.2f}, p={p:.3f}')\n"
         "print('結論:', '均等でない' if p < 0.05 else '均等といえる')"),
    md("## 3. 一元配置分散分析（ANOVA）\n\n"
       "3つの店舗A・B・Cの売上に差があるか？\n"
       "t検定を3回くり返すと誤りが増えるので、ANOVAで一度に検定します。"),
    code("storeA = rng.normal(50, 8, 20)\n"
         "storeB = rng.normal(55, 8, 20)\n"
         "storeC = rng.normal(58, 8, 20)\n"
         "f_stat, p = stats.f_oneway(storeA, storeB, storeC)\n"
         "print(f'F統計量: {f_stat:.3f},  p値: {p:.4f}')\n"
         "print('結論:', '少なくとも1店舗は平均が違う' if p < 0.05 else '差は有意でない')\n\n"
         "plt.boxplot([storeA, storeB, storeC], tick_labels=['A', 'B', 'C'])\n"
         "plt.ylabel('売上'); plt.title('店舗別の売上')\n"
         "plt.show()"),
    md("> 📝 ANOVAは「どこかに差がある」までしか分かりません。\n"
       "「どの店どうしが違うか」は多重比較（Tukey法など）で調べます。"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `業界` と `受注` に関連があるか、`sales_btob.csv` でカイ二乗検定をしよう。\n\n"
       "**問2.** あるアンケートで血液型が `[A,B,O,AB] = [38,22,30,10]`。\n"
       "日本人の理論比 `[0.38,0.22,0.31,0.09]` に適合するか検定しよう。\n\n"
       "**問3.** `students_scores.csv` のクラスA・B・Cで `数学` の平均に差があるか、ANOVAで調べよう。"),
    code("# 問1\n"),
    code("# 問2\n"),
    code(f"# 問3\ndf = pd.read_csv('{DATA}/students_scores.csv')\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(stats.chi2_contingency(pd.crosstab(btob['業界'], btob['受注']))[1])\n"
       "exp = np.array([0.38,0.22,0.31,0.09])*100\n"
       "print(stats.chisquare([38,22,30,10], exp))\n"
       "g = [df[df['クラス']==c]['数学'] for c in ['A','B','C']]\n"
       "print(stats.f_oneway(*g))\n"
       "```\n</details>\n\n"
       "🎉 **統計2級レベル クリア！** ここまでで統計検定2級の主要分野を一通り体験しました。\n"
       "次は `05_実践_BtoBマーケ` で、学んだ統計を実際のビジネスデータに使ってみよう。"),
]
write_nb("04_統計_2級/03_カイ二乗と分散分析.ipynb", cells)

print("=== 統計2級 done ===")
