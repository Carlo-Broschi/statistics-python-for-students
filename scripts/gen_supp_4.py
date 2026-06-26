from nbbuild import md, code, write_nb

DATA = "../data"

# =====================================================================
# 4級-05 PPDAC とグラフの読み方
# =====================================================================
cells = [
    md("# 統計4級-05. 統計的問題解決(PPDAC)と基本グラフの読み方\n\n"
       "**この章で学ぶこと（4級の頻出テーマ）**\n"
       "- PPDACサイクル（統計的問題解決の流れ）\n"
       "- 棒・折れ線・円・帯・積み上げ・パレート図など**基本グラフの使い分けと読み方**\n"
       "- 幹葉図（みきはず）\n\n"
       "4級では「どのグラフが適切か」「グラフから値を読む」問題が多く出ます。"),
    code("import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n"
         "plt.rcParams['axes.unicode_minus'] = False"),
    md("## 1. PPDAC サイクル\n\n"
       "統計で問題を解くときの流れです。頭文字をとってPPDAC。\n\n"
       "| 段階 | 意味 | 例（自販機の売上を伸ばしたい） |\n"
       "|---|---|---|\n"
       "| **P**roblem | 問題を決める | どの商品がいつ売れる？ |\n"
       "| **P**lan | 計画する | 1か月、時間帯別に記録しよう |\n"
       "| **D**ata | データを集める | レジ記録を集計 |\n"
       "| **A**nalysis | 分析する | グラフ化・平均を比較 |\n"
       "| **C**onclusion | 結論を出す | 夏の午後は冷たい飲料を増やす |\n\n"
       "> 💡 結論からまた新しいProblemが生まれ、サイクルは回り続けます。"),
    md("## 2. 基本グラフの使い分け\n\n"
       "| グラフ | 得意なこと | 使う場面 |\n"
       "|---|---|---|\n"
       "| 棒グラフ | 量の大小を比べる | クラス別の人数 |\n"
       "| 折れ線グラフ | 変化（時間）を見る | 毎月の気温 |\n"
       "| 円グラフ | 割合（構成比）を見る | 好きな教科の割合 |\n"
       "| 帯グラフ | 割合を複数で比べる | 年ごとの構成比の変化 |\n"
       "| 積み上げ棒 | 量と内訳を同時に | 店舗別×商品別売上 |\n"
       "| パレート図 | 「重要な少数」を見る | 上位で大半を占める要因 |"),
    md("### 棒グラフ・折れ線・円グラフを描いてみる"),
    code("kyoka = pd.Series({'数学':8,'英語':12,'国語':10,'理科':6,'社会':4}, name='人数')\n\n"
         "fig, ax = plt.subplots(1, 3, figsize=(13,4))\n"
         "kyoka.plot(kind='bar', ax=ax[0], title='棒：好きな教科の人数')\n"
         "ax[0].tick_params(axis='x', rotation=0)\n"
         "pd.Series([22,24,28,30,27,25],\n"
         "          index=['1月','2月','3月','4月','5月','6月']).plot(\n"
         "          marker='o', ax=ax[1], title='折れ線：気温の変化')\n"
         "kyoka.plot(kind='pie', ax=ax[2], autopct='%1.0f%%', title='円：割合')\n"
         "ax[2].set_ylabel('')\n"
         "plt.tight_layout(); plt.show()"),
    md("### 帯グラフ（割合を複数で比較）"),
    code("df_taikei = pd.DataFrame({\n"
         "    '2020年':[40,35,25], '2026年':[55,30,15]\n"
         "}, index=['スマホ','PC','その他']).T\n"
         "ratio = df_taikei.div(df_taikei.sum(axis=1), axis=0) * 100\n"
         "ratio.plot(kind='barh', stacked=True, figsize=(8,3),\n"
         "           title='帯グラフ：利用端末の割合の変化(%)')\n"
         "plt.xlabel('％'); plt.show()"),
    md("### パレート図（重要な少数を見つける）\n"
       "棒（大きい順）＋累積割合の折れ線。上位2〜3項目で全体の大半を占めることを示します。"),
    code("claims = pd.Series({'配送遅延':52,'破損':28,'数量違い':12,'その他':8})\n"
         "claims = claims.sort_values(ascending=False)\n"
         "cum = claims.cumsum() / claims.sum() * 100\n\n"
         "fig, ax1 = plt.subplots(figsize=(7,4))\n"
         "ax1.bar(claims.index, claims.values)\n"
         "ax2 = ax1.twinx()\n"
         "ax2.plot(claims.index, cum.values, color='red', marker='o')\n"
         "ax2.set_ylim(0,110); ax2.set_ylabel('累積％')\n"
         "ax1.set_ylabel('件数'); plt.title('パレート図：クレームの内訳')\n"
         "plt.show()\n"
         "print('上位2項目で全体の', round(cum.iloc[1],1), '%')"),
    md("## 3. 幹葉図（みきはず）\n\n"
       "数を「十の位（幹）」と「一の位（葉）」に分けて並べる図。\n"
       "ヒストグラムに似ていますが、**元の数字が残る**のが特徴です。"),
    code("def stem_leaf(data):\n"
         "    data = sorted(data)\n"
         "    stems = {}\n"
         "    for v in data:\n"
         "        stems.setdefault(v // 10, []).append(v % 10)\n"
         "    for s in range(min(stems), max(stems) + 1):\n"
         "        leaves = ''.join(str(x) for x in stems.get(s, []))\n"
         "        print(f'{s} | {leaves}')\n\n"
         "scores = [62,65,67,71,73,73,78,81,82,85,88,90,52,59]\n"
         "stem_leaf(scores)\n"
         "print('読み方: 7|1338 は 71,73,73,78 点の4人')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** 次のデータに最も適したグラフを選べ：\n"
       "(a) 1年間の毎月の売上の推移 (b) アンケートの賛成・反対・どちらでもないの割合\n"
       "(c) 5つの店舗の来客数の比較\n\n"
       "**問2.** `students_scores.csv` の `数学` を幹葉図にしよう。\n\n"
       "**問3.** ある店の不具合原因 `{部品A:60, 部品B:25, 部品C:10, その他:5}` でパレート図を描き、\n"
       "「上位いくつの原因で全体の8割を超えるか」を答えよう。"),
    code(f"# 問2\nimport pandas as pd\ndf = pd.read_csv('{DATA}/students_scores.csv')\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "問1: (a)折れ線 (b)円グラフ(または帯) (c)棒グラフ\n\n"
       "```python\n"
       "stem_leaf(df['数学'].tolist())\n"
       "```\n</details>"),
]
write_nb("02_統計_4級/05_PPDACとグラフの読み方.ipynb", cells)

# =====================================================================
# 4級-06 時系列と場合の数
# =====================================================================
cells = [
    md("# 統計4級-06. 時系列データと場合の数（樹形図）\n\n"
       "**この章で学ぶこと**\n"
       "- 時系列データ：増減率・指数・移動平均\n"
       "- 場合の数と樹形図（確率の土台）"),
    code("import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n"
         "plt.rcParams['axes.unicode_minus'] = False"),
    md("## 1. 時系列データ\n\n"
       "時間とともに変化するデータ。3つの見方を学びます。\n"
       "ここでは、ある店の月別売上（万円）を例にします。"),
    code("sales = pd.Series([100, 110, 121, 115, 130, 143],\n"
         "    index=['1月','2月','3月','4月','5月','6月'], name='売上')\n"
         "sales"),
    md("### ① 増減率（前の月から何％増えたか）\n"
       "$$ 増減率 = \\frac{今月 - 先月}{先月} \\times 100 $$"),
    code("growth = sales.pct_change() * 100\n"
         "print(growth.round(1))\n"
         "print('→ 2月は前月比 +10%、4月はマイナス')"),
    md("### ② 指数（基準を100としたときの大きさ）\n"
       "1月を基準(100)にして、各月が基準の何倍かを見ます。単位の違うものを比べやすい。"),
    code("index = sales / sales['1月'] * 100\n"
         "print(index.round(1))\n"
         "print('→ 6月は1月の143（=43%増）')"),
    md("### ③ 移動平均（でこぼこをならす）\n"
       "数か月の平均をずらしながら計算。短期の上下を消し、大きな流れ（トレンド）を見ます。"),
    code("ma3 = sales.rolling(window=3).mean()\n"
         "print(ma3.round(1))\n\n"
         "sales.plot(marker='o', label='売上')\n"
         "ma3.plot(marker='s', label='3か月移動平均')\n"
         "plt.legend(); plt.title('売上と移動平均'); plt.show()"),
    md("> 💡 移動平均は、気温・株価・感染者数など「上下が激しいデータの傾向」を見るのに使われます。"),
    md("## 2. 場合の数と樹形図\n\n"
       "「何通りあるか」を数えるのが場合の数。枝分かれの図＝**樹形図**で整理します。\n\n"
       "例：コインを2回投げると？\n"
       "```\n"
       "1回目   2回目   結果\n"
       "        表 ── 表表\n"
       "  表 <\n"
       "        裏 ── 表裏\n"
       "        表 ── 裏表\n"
       "  裏 <\n"
       "        裏 ── 裏裏\n"
       "```\n"
       "→ 全部で 2×2 = **4通り**。"),
    code("import itertools\n"
         "# コイン2回の全パターンを列挙\n"
         "outcomes = list(itertools.product(['表','裏'], repeat=2))\n"
         "for o in outcomes:\n"
         "    print(o)\n"
         "print('全', len(outcomes), '通り')"),
    md("### 場合の数から確率へ\n"
       "「2回とも表」になる確率は、1通り ÷ 4通り = 1/4。"),
    code("rng = np.random.default_rng(0)\n"
         "trials = rng.integers(0, 2, size=(10000, 2))   # 0=表,1=表… 2回\n"
         "both_head = np.sum(np.all(trials == 0, axis=1))\n"
         "print('実験での割合:', both_head / 10000, ' (理論 0.25)')"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** 売上 `[200,180,210,240,230,260]`（1〜6月）について、\n"
       "前月比（増減率）と、1月を100とした指数を計算しよう。\n\n"
       "**問2.** `weather.csv` の `気温` の **5日移動平均**を計算し、元データと一緒に折れ線で描こう。\n\n"
       "**問3.** サイコロを2回ふるとき、出る目の組み合わせは全部で何通り？\n"
       "また「合計が7になる」のは何通りで、確率はいくつ？（`itertools.product`を使おう）"),
    code("# 問1\n"),
    code(f"# 問2\nw = pd.read_csv('{DATA}/weather.csv')\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "s = pd.Series([200,180,210,240,230,260])\n"
       "print(s.pct_change()*100); print(s/s.iloc[0]*100)\n\n"
       "w['気温'].rolling(5).mean().plot(); w['気温'].plot(); plt.show()\n\n"
       "import itertools\n"
       "dice = list(itertools.product(range(1,7), repeat=2))\n"
       "seven = [d for d in dice if sum(d)==7]\n"
       "print(len(dice), len(seven), len(seven)/len(dice))  # 36, 6, 1/6\n"
       "```\n</details>\n\n"
       "🎉 これで**4級の出題範囲をほぼ全てカバー**しました。"),
]
write_nb("02_統計_4級/06_時系列と場合の数.ipynb", cells)

print("=== 4級補強 done ===")
