from nbbuild import md, code, write_nb

DATA = "../data"

# =====================================================================
# 01 売上データ分析ワークシート
# =====================================================================
cells = [
    md("# 実践マーケ-01. BtoB売上データ分析ワークシート\n\n"
       "**舞台設定**：あなたは法人向けソフトを売る会社のデータ分析担当。\n"
       "半年分の商談データ `sales_btob.csv` を分析し、社内会議で報告します。\n\n"
       "**使う統計（4〜3級）**：合計・平均・構成比・クロス集計・グループ別比較\n\n"
       "> 💼 BtoB（Business to Business）= 会社が会社に売るビジネス。"
       "1件の金額が大きく、受注までの検討が長いのが特徴です。"),
    code("import pandas as pd\n"
         "import numpy as np\n"
         "import matplotlib.pyplot as plt\n"
         "plt.rcParams['axes.unicode_minus'] = False\n"
         f"btob = pd.read_csv('{DATA}/sales_btob.csv')\n"
         "print('商談数:', len(btob))\n"
         "btob.head()"),
    md("## 1. まずデータを知る\n\n"
       "分析の第一歩は「どんな列があり、どんな値か」を把握することです。"),
    code("btob.info()\n"
         "btob.describe(include='all')"),
    md("## 2. 全体のKPIを出す\n\n"
       "KPI = 重要な指標。BtoB営業では次がよく使われます。\n"
       "- 受注率（受注した商談の割合）\n"
       "- 受注金額の合計（売上）\n"
       "- 平均商談単価"),
    code("won = btob[btob['受注'] == 1]\n"
         "print('受注率: {:.1%}'.format(btob['受注'].mean()))\n"
         "print('受注件数:', len(won))\n"
         "print('売上合計: {:,} 円'.format(won['商談金額'].sum()))\n"
         "print('平均単価: {:,.0f} 円'.format(won['商談金額'].mean()))"),
    md("## 3. チャネル別に分解する（どこから売上が来たか）\n\n"
       "「獲得チャネル」ごとに受注売上を集計し、棒グラフにします。"),
    code("by_ch = won.groupby('獲得チャネル')['商談金額'].sum().sort_values(ascending=False)\n"
         "print(by_ch)\n"
         "by_ch.plot(kind='bar', figsize=(7,4), title='チャネル別の受注売上')\n"
         "plt.ylabel('売上(円)'); plt.xticks(rotation=0); plt.show()"),
    md("### 構成比（パレート分析）\n"
       "「売上の8割はどのチャネルから？」を割合で見ます。"),
    code("ratio = (by_ch / by_ch.sum() * 100).round(1)\n"
         "cum = ratio.cumsum()\n"
         "pd.DataFrame({'売上構成比%': ratio, '累積%': cum})"),
    md("## 4. 月ごとの推移を見る（時系列）\n\n"
       "受注日を月単位にまとめ、売上の伸びを折れ線で確認します。"),
    code("won = won.copy()\n"
         "won['受注月'] = pd.to_datetime(won['受注日']).dt.to_period('M').astype(str)\n"
         "monthly = won.groupby('受注月')['商談金額'].sum()\n"
         "monthly.plot(marker='o', figsize=(7,4), title='月別売上の推移')\n"
         "plt.ylabel('売上(円)'); plt.grid(alpha=0.3); plt.show()\n"
         "monthly"),
    md("---\n## 🏆 ワークシート課題\n\n"
       "**課題1.** 業界別の受注売上を集計し、最も売れている業界トップ3を答えよう。\n\n"
       "**課題2.** 担当者別の受注件数と受注率を出し、「最も成績が良い担当者」を見つけよう。\n\n"
       "**課題3.**（報告書）この会社の社長に向けて、分かったことを3行でまとめよう。\n"
       "「①売上の柱は◯◯チャネル ②◯◯業界が有望 ③△△を強化すべき」のように。"),
    code("# 課題1\n"),
    code("# 課題2\n"),
    md("<details><summary>ヒント / 解答例</summary>\n\n"
       "```python\n"
       "won.groupby('業界')['商談金額'].sum().sort_values(ascending=False).head(3)\n\n"
       "btob.groupby('担当者').agg(件数=('受注','sum'), 受注率=('受注','mean'))\n"
       "```\n</details>"),
]
write_nb("05_実践_BtoBマーケ/01_売上データ分析.ipynb", cells)

# =====================================================================
# 02 チャネル/顧客セグメント分析
# =====================================================================
cells = [
    md("# 実践マーケ-02. マーケティング・ファネルとチャネル効率\n\n"
       "**舞台設定**：半年分のマーケ施策データ `web_marketing.csv` を分析し、\n"
       "「来年はどのチャネルに予算を回すべきか」を提案します。\n\n"
       "**使う統計（4〜3級）**：割合・率の計算・チャネル比較・費用対効果"),
    code("import pandas as pd\n"
         "import numpy as np\n"
         "import matplotlib.pyplot as plt\n"
         "plt.rcParams['axes.unicode_minus'] = False\n"
         f"mk = pd.read_csv('{DATA}/web_marketing.csv')\n"
         "mk.head()"),
    md("## 1. マーケティング・ファネル\n\n"
       "見込み客は段階的に減っていきます（じょうご＝ファネル）。\n\n"
       "```\n表示(Impression) → クリック(Click) → 獲得(Conversion=問い合わせ/申込)\n```\n\n"
       "各段階の「通過率」を計算します。\n"
       "- **CTR**（クリック率）= クリック ÷ 表示\n"
       "- **CVR**（獲得率）= 獲得 ÷ クリック"),
    code("g = mk.groupby('チャネル')[['表示回数','クリック数','獲得数','費用']].sum()\n"
         "g['CTR'] = (g['クリック数'] / g['表示回数'] * 100).round(2)\n"
         "g['CVR'] = (g['獲得数'] / g['クリック数'] * 100).round(2)\n"
         "g"),
    md("## 2. 費用対効果（CPA）\n\n"
       "**CPA**（Cost Per Acquisition）= 費用 ÷ 獲得数 = 1件獲得するのにかかったお金。\n"
       "**小さいほど効率が良い**チャネルです。"),
    code("g['CPA'] = (g['費用'] / g['獲得数']).round(0)\n"
         "g[['獲得数','費用','CPA']].sort_values('CPA')"),
    code("g['CPA'].sort_values().plot(kind='barh', figsize=(7,4),\n"
         "    title='チャネル別CPA（低いほど効率的）')\n"
         "plt.xlabel('1件あたり獲得コスト(円)'); plt.show()"),
    md("> 💡 **獲得数が多い ≠ 効率が良い**。Web広告は数を稼げてもCPAが高いことが多い。\n"
       "紹介やメルマガはCPAが低い「おいしい」チャネルになりがちです。"),
    md("## 3. 効率と量のバランス（バブルチャート）\n\n"
       "横軸=獲得数（量）、縦軸=CPA（効率）、円の大きさ=費用 で一望します。\n"
       "**右下（量が多くCPAが低い）が理想**。"),
    code("fig, ax = plt.subplots(figsize=(7,5))\n"
         "ax.scatter(g['獲得数'], g['CPA'], s=g['費用']/300, alpha=0.5)\n"
         "for name, row in g.iterrows():\n"
         "    ax.annotate(name, (row['獲得数'], row['CPA']))\n"
         "ax.set_xlabel('獲得数（量）'); ax.set_ylabel('CPA（コスト効率）')\n"
         "ax.set_title('チャネルの量×効率マップ'); plt.show()"),
    md("---\n## 🏆 ワークシート課題\n\n"
       "**課題1.** 最もCVR（獲得率）が高いチャネルと、最もCPAが低いチャネルを答えよう。\n\n"
       "**課題2.** 月ごとに「Web広告」のCPAは改善しているか？ 月別に集計して折れ線で確認しよう。\n\n"
       "**課題3.**（提案）来年100万円の追加予算がある。どのチャネルにいくら配分するか、\n"
       "CPAとCVRを根拠に提案文を書こう。"),
    code("# 課題1\n"),
    code("# 課題2（ヒント）\n"
         "ad = mk[mk['チャネル']=='Web広告'].copy()\n"
         "ad['CPA'] = ad['費用'] / ad['獲得数']\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(g['CVR'].idxmax(), g['CPA'].idxmin())\n"
       "ad.groupby('月')['CPA'].mean().plot(marker='o'); plt.show()\n"
       "```\n</details>"),
]
write_nb("05_実践_BtoBマーケ/02_ファネルとチャネル効率.ipynb", cells)

# =====================================================================
# 03 A/BテストとKPI
# =====================================================================
cells = [
    md("# 実践マーケ-03. A/Bテストで意思決定する\n\n"
       "**舞台設定**：申込ページのボタンの色を「青(A)」と「緑(B)」で出し分けた。\n"
       "どちらが申込率が高いか、`ab_test.csv` で科学的に判断します。\n\n"
       "**使う統計（3〜2級）**：比率の比較・カイ二乗検定・「差は偶然か？」の判断"),
    code("import pandas as pd\n"
         "import numpy as np\n"
         "import matplotlib.pyplot as plt\n"
         "from scipy import stats\n"
         "plt.rcParams['axes.unicode_minus'] = False\n"
         f"ab = pd.read_csv('{DATA}/ab_test.csv')\n"
         "ab.head()"),
    md("## 1. 各グループの申込率を出す\n\n"
       "まず単純に「見た目の率」を比べます。"),
    code("summary = ab.groupby('グループ')['申込'].agg(['count','sum','mean'])\n"
         "summary.columns = ['訪問数','申込数','申込率']\n"
         "summary['申込率'] = (summary['申込率']*100).round(2)\n"
         "summary"),
    code("summary['申込率'].plot(kind='bar', figsize=(5,4), title='ボタン色別の申込率(%)')\n"
         "plt.ylabel('申込率(%)'); plt.xticks(rotation=0); plt.show()"),
    md("## 2. その差は「偶然」ではない？\n\n"
       "Bの方が高く見えても、たまたまかもしれません。\n"
       "**カイ二乗検定**で「色と申込に関連があるか」を確かめます。\n\n"
       "- H₀（帰無仮説）：色と申込率は関係ない（差は偶然）\n"
       "- H₁（対立仮説）：色によって申込率が違う"),
    code("table = pd.crosstab(ab['グループ'], ab['申込'])\n"
         "print(table)\n"
         "chi2, p, dof, exp = stats.chi2_contingency(table)\n"
         "print(f'\\nカイ二乗={chi2:.3f}, p値={p:.4f}')\n"
         "if p < 0.05:\n"
         "    print('→ 有意差あり！ ボタンの色で申込率は本当に変わる')\n"
         "else:\n"
         "    print('→ 有意差なし。偶然の範囲かもしれない')"),
    md("## 3. 効果の大きさと事業インパクト\n\n"
       "「統計的に有意」だけでなく「ビジネスとして何円得か」も大事です。"),
    code("rate_a = summary.loc['A_青ボタン','申込率'] / 100\n"
         "rate_b = summary.loc['B_緑ボタン','申込率'] / 100\n"
         "lift = (rate_b - rate_a) / rate_a * 100\n"
         "print(f'改善率（リフト）: {lift:+.1f}%')\n\n"
         "# 月10万訪問・1申込5000円の価値と仮定したら？\n"
         "monthly_visits = 100000\n"
         "value_per = 5000\n"
         "gain = monthly_visits * (rate_b - rate_a) * value_per\n"
         "print(f'Bに変えると月あたり約 {gain:,.0f} 円の増加見込み')"),
    md("> 📝 **A/Bテストの注意点**\n"
       "> - 途中で何度も覗いて「有意になった瞬間にやめる」のはNG（偽陽性が増える）\n"
       "> - 事前に必要なサンプル数を決めておく\n"
       "> - 期間は曜日の偏りをならすため1週間以上が目安"),
    md("---\n## 🏆 ワークシート課題\n\n"
       "**課題1.** AとBの申込率の差を「パーセントポイント」と「リフト%」の両方で表そう。\n\n"
       "**課題2.** もし有意水準を 0.01（より厳しく）にしても結論は変わるか、p値を見て判断しよう。\n\n"
       "**課題3.**（意思決定）上司に「緑ボタンを採用すべきか」を、\n"
       "統計的根拠（p値）とビジネス的根拠（増加見込み金額）の両方で説明する文を書こう。\n\n"
       "**課題4.**（発展）`proportions_ztest` を使って同じ検定を比率の検定で行い、\n"
       "カイ二乗検定とp値がほぼ一致することを確かめよう。"),
    code("# 課題1\n"),
    code("# 課題4（ヒント）\n"
         "from statsmodels.stats.proportion import proportions_ztest\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "count = ab.groupby('グループ')['申込'].sum().values\n"
       "nobs  = ab.groupby('グループ')['申込'].count().values\n"
       "z, p = proportions_ztest(count, nobs)\n"
       "print(z, p)   # カイ二乗のp値とほぼ一致\n"
       "```\n</details>\n\n"
       "🎉 **実践マーケ編 クリア！** 統計が「ビジネスの意思決定の道具」だと実感できたはず。\n"
       "ひと息ついたら `07_ホビー_陶芸3D` で 3Dモデリングを楽しもう。"),
]
write_nb("05_実践_BtoBマーケ/03_ABテストとKPI.ipynb", cells)

print("=== マーケ実践 done ===")
