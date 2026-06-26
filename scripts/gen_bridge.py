from nbbuild import md, code, write_nb

DATA = "../data"

# =====================================================================
# 05 NumPy入門
# =====================================================================
cells = [
    md("# 05. NumPy入門 〜数値計算の土台〜\n\n"
       "**ここからは「データ分析のためのPython」**。統計・マーケのノートで必ず使う\n"
       "3つの道具（NumPy・pandas・matplotlib）を、この05〜07で先に身につけます。\n\n"
       "> ⚠️ **04までの純粋なPythonだけでは、統計のノート（4級〜）は読めません。**\n"
       "> 05〜07をやってから `02_統計_4級` に進むのがおすすめの順番です。\n\n"
       "**この章のゴール**：配列(array)で、たくさんの数をまとめて高速に計算できる。"),
    md("## 1. なぜNumPy？ リストとの違い\n\n"
       "リストは「1つずつ」しか計算できませんが、NumPyの配列は**まとめて**計算できます。"),
    code("# ふつうのリストでは * 2 が「くり返し」になってしまう\n"
         "prices = [100, 200, 300]\n"
         "print(prices * 2)        # [100,200,300,100,200,300] … 望んだ結果じゃない\n\n"
         "import numpy as np\n"
         "arr = np.array([100, 200, 300])\n"
         "print(arr * 2)           # [200 400 600] … 全部を2倍！\n"
         "print(arr + 50)          # [150 250 350] … 全部に+50"),
    md("## 2. 配列のつくり方"),
    code("print(np.array([1, 2, 3, 4]))      # リストから\n"
         "print(np.arange(0, 10, 2))         # 0から10未満を2とび → [0 2 4 6 8]\n"
         "print(np.linspace(0, 1, 5))        # 0〜1を5等分 → [0. .25 .5 .75 1.]\n"
         "print(np.zeros(3), np.ones(3))     # ゼロ/イチで埋める"),
    md("## 3. まとめて集計する\n\n"
       "統計でいちばん使う部分です。合計・平均・標準偏差などが1行で出ます。"),
    code("scores = np.array([60, 75, 90, 55, 80, 100, 45])\n"
         "print('合計  :', scores.sum())\n"
         "print('平均  :', scores.mean())\n"
         "print('最大  :', scores.max(), ' 最小:', scores.min())\n"
         "print('標準偏差:', scores.std().round(2))\n"
         "print('√144  :', np.sqrt(144))"),
    md("## 4. 条件で選ぶ（真偽値インデックス）\n\n"
       "「60点以上だけ取り出す」「何個あるか数える」が簡単にできます。\n"
       "統計の『○点以上は何人？』で大活躍します。"),
    code("print(scores >= 60)              # 各要素がTrue/False\n"
         "print(scores[scores >= 60])     # Trueの要素だけ取り出す\n"
         "print('60点以上の人数:', (scores >= 60).sum())   # Trueの数を数える\n"
         "print('60点以上の平均:', scores[scores >= 60].mean().round(1))"),
    md("### np.where で条件分け\n"
       "`np.where(条件, Trueの値, Falseの値)`。合否ラベルづけなどに使います。"),
    code("result = np.where(scores >= 60, '合格', '不合格')\n"
         "print(result)"),
    md("## 5. 乱数（シミュレーション）\n\n"
       "サイコロやコイン、標本のシミュレーションに使います。\n"
       "`default_rng(seed)` の seed を固定すると、毎回同じ結果になり再現できます。"),
    code("rng = np.random.default_rng(0)\n"
         "print('サイコロ10回:', rng.integers(1, 7, size=10))\n"
         "print('正規分布から5個:', rng.normal(50, 10, size=5).round(1))\n"
         "print('くじ引き:', rng.choice(['当たり', 'はずれ'], size=5))"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `temps = np.array([22,25,19,30,28,24,21])` の平均・最高・最低・標準偏差を求めよう。\n\n"
       "**問2.** 上の `temps` で「25度以上の日」が何日あるか、真偽値インデックスで数えよう。\n\n"
       "**問3.** サイコロ（1〜6）を1000回ふって平均を求め、理論値3.5に近いか確かめよう。\n"
       "（`rng.integers(1,7,size=1000).mean()`）"),
    code("# 問1\nimport numpy as np\ntemps = np.array([22,25,19,30,28,24,21])\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(temps.mean(), temps.max(), temps.min(), temps.std())\n"
       "print((temps >= 25).sum())\n"
       "rng = np.random.default_rng(1)\n"
       "print(rng.integers(1,7,size=1000).mean())\n"
       "```\n</details>"),
]
write_nb("01_Python基礎/05_NumPy入門.ipynb", cells)

# =====================================================================
# 06 pandas入門
# =====================================================================
cells = [
    md("# 06. pandas入門 〜表データを自在に扱う〜\n\n"
       "**pandas** は、Excelのような「表（テーブル）」をPythonで扱う道具。\n"
       "CSVを読み込み、選び・絞り・集計する——統計・マーケのノートの中心スキルです。\n\n"
       "**ゴール**：CSVを読み込んで、列の取り出し・行の絞り込み・グループ集計ができる。"),
    code("import pandas as pd\nimport numpy as np"),
    md("## 1. Series と DataFrame\n\n"
       "- **Series**：1列のデータ（ラベル付きの配列）\n"
       "- **DataFrame**：複数列の表"),
    code("s = pd.Series([60, 75, 90], index=['数学', '英語', '国語'])\n"
         "print(s)\n"
         "print('英語の点:', s['英語'])"),
    code("df = pd.DataFrame({\n"
         "    '名前': ['あおい', 'はると', 'ゆい'],\n"
         "    '数学': [90, 60, 75],\n"
         "    '英語': [70, 85, 80],\n"
         "})\n"
         "df"),
    md("## 2. CSVを読み込む\n\n"
       "実際のデータは `read_csv` で読みます。教材の生徒データを使います。"),
    code(f"df = pd.read_csv('{DATA}/students_scores.csv')\n"
         "df.head()       # 先頭5行を確認"),
    code("print('行数・列数:', df.shape)\n"
         "print('列名:', list(df.columns))\n"
         "df.describe()    # 数値列の要約（平均・標準偏差・四分位など）"),
    md("## 3. 列を取り出す\n\n"
       "`df['列名']` で1列、`df[['列1','列2']]` で複数列。"),
    code("print(df['数学'].head())\n"
         "print('数学の平均:', df['数学'].mean().round(1))\n"
         "df[['数学', '英語']].head()"),
    md("## 4. 行を絞り込む（条件フィルタ）\n\n"
       "`df[条件]` で、条件がTrueの行だけ残します。NumPyの真偽値インデックスと同じ発想。"),
    code("# 数学が80点以上の生徒\n"
         "good = df[df['数学'] >= 80]\n"
         "print('80点以上:', len(good), '人')\n"
         "good.head()"),
    code("# 複数条件は & (かつ) / | (または)。各条件は () で囲む\n"
         "df[(df['数学'] >= 80) & (df['英語'] >= 80)].head()"),
    md("## 5. 新しい列をつくる"),
    code("df['合計'] = df['数学'] + df['英語'] + df['国語']\n"
         "df['合否'] = np.where(df['数学'] >= 60, '合格', '不合格')\n"
         "df[['生徒ID', '数学', '合計', '合否']].head()"),
    md("## 6. グループごとに集計（groupby）\n\n"
       "**統計・マーケで最頻出**。「クラスごとの平均点」のような集計が1行で書けます。"),
    code("# クラスごとの数学の平均\n"
         "print(df.groupby('クラス')['数学'].mean().round(1))\n\n"
         "# 複数の集計をまとめて\n"
         "df.groupby('クラス').agg(\n"
         "    人数=('生徒ID', 'count'),\n"
         "    数学平均=('数学', 'mean'),\n"
         "    英語平均=('英語', 'mean'),\n"
         ").round(1)"),
    md("## 7. 数える・並べ替え・クロス集計"),
    code("print(df['合否'].value_counts())          # カテゴリの個数\n"
         "print()\n"
         "print(df.sort_values('合計', ascending=False)[['生徒ID','合計']].head(3))  # 上位3人\n"
         "print()\n"
         "print(pd.crosstab(df['クラス'], df['合否']))  # クラス×合否の表"),
    md("> 📊 `pd.cut`（階級分け）も統計でよく使います → `02_統計_4級/01` で登場します。"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `students_scores.csv` を読み込み、`英語` の平均と最高点を求めよう。\n\n"
       "**問2.** `国語` が80点以上の生徒だけを絞り込み、何人いるか数えよう。\n\n"
       "**問3.** クラスごとの `勉強時間` の平均を `groupby` で求めよう。\n\n"
       "**問4.** `数学` の高い順に並べ替えて、上位5人の `生徒ID` と `数学` を表示しよう。"),
    code(f"# 準備\nimport pandas as pd\ndf = pd.read_csv('{DATA}/students_scores.csv')\n"),
    code("# 問1〜4\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "print(df['英語'].mean(), df['英語'].max())\n"
       "print(len(df[df['国語'] >= 80]))\n"
       "print(df.groupby('クラス')['勉強時間'].mean())\n"
       "print(df.sort_values('数学', ascending=False)[['生徒ID','数学']].head())\n"
       "```\n</details>"),
]
write_nb("01_Python基礎/06_pandas入門.ipynb", cells)

# =====================================================================
# 07 matplotlib入門
# =====================================================================
cells = [
    md("# 07. matplotlib入門 〜グラフを描く〜\n\n"
       "数字の表だけでは分かりにくい特徴も、グラフにすれば一目瞭然。\n"
       "**matplotlib** で、統計・マーケのノートに出てくるグラフを一通り描けるようにします。\n\n"
       "**ゴール**：折れ線・棒・ヒストグラム・散布図・箱ひげ図・円グラフを描ける。"),
    code("import matplotlib.pyplot as plt\nimport pandas as pd\nimport numpy as np\n\n"
         "# 日本語が□に化けるときは、環境に合わせて次の1行を有効化\n"
         "# plt.rcParams['font.family'] = 'Hiragino Sans'   # Mac\n"
         "# plt.rcParams['font.family'] = 'Yu Gothic'       # Windows\n"
         "plt.rcParams['axes.unicode_minus'] = False"),
    md("## 1. 折れ線グラフ（変化を見る）\n\n"
       "基本は `plt.plot(x, y)` → `plt.show()`。タイトルやラベルも付けます。"),
    code("month = [1, 2, 3, 4, 5, 6]\n"
         "temp = [22, 24, 28, 30, 27, 25]\n"
         "plt.plot(month, temp, marker='o')\n"
         "plt.title('気温の変化')\n"
         "plt.xlabel('月'); plt.ylabel('気温(℃)')\n"
         "plt.show()"),
    md("## 2. 棒グラフ（大小を比べる）"),
    code("kyoka = ['数学', '英語', '国語', '理科']\n"
         "ninzu = [8, 12, 10, 6]\n"
         "plt.bar(kyoka, ninzu)\n"
         "plt.title('好きな教科'); plt.ylabel('人数')\n"
         "plt.show()"),
    md("## 3. ヒストグラム（分布を見る）\n\n"
       "たくさんの数値が「どのあたりに集まっているか」を見ます。統計で最重要。"),
    code(f"df = pd.read_csv('{DATA}/students_scores.csv')\n"
         "plt.hist(df['数学'], bins=10, edgecolor='white')\n"
         "plt.title('数学の点数の分布'); plt.xlabel('点数'); plt.ylabel('人数')\n"
         "plt.show()"),
    md("## 4. 散布図（2つの量の関係）"),
    code("plt.scatter(df['数学'], df['英語'], alpha=0.5)\n"
         "plt.title('数学と英語'); plt.xlabel('数学'); plt.ylabel('英語')\n"
         "plt.show()"),
    md("## 5. 箱ひげ図・円グラフ"),
    code("fig, ax = plt.subplots(1, 2, figsize=(11, 4))\n"
         "ax[0].boxplot([df[df['クラス']==c]['数学'] for c in ['A','B','C']],\n"
         "              tick_labels=['A','B','C'])\n"
         "ax[0].set_title('クラス別 数学'); ax[0].set_ylabel('点数')\n\n"
         "df['合否'] = np.where(df['数学']>=60,'合格','不合格')\n"
         "df['合否'].value_counts().plot(kind='pie', autopct='%1.0f%%', ax=ax[1])\n"
         "ax[1].set_title('合否の割合'); ax[1].set_ylabel('')\n"
         "plt.show()"),
    md("## 6. pandasから直接プロット（近道）\n\n"
       "`Series.plot()` / `df.plot()` を使うと、集計結果をそのままグラフ化できます。\n"
       "マーケのノートでよく使う書き方です。"),
    code("df.groupby('クラス')['数学'].mean().plot(kind='bar', title='クラス別 数学の平均')\n"
         "plt.ylabel('平均点'); plt.xticks(rotation=0)\n"
         "plt.show()"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `英語` のヒストグラム（bins=10）を描こう。\n\n"
       "**問2.** `勉強時間`(x) と `数学`(y) の散布図を描こう。関係は見える？\n\n"
       "**問3.** クラスごとの `英語` の平均を棒グラフにしよう（`groupby` → `.plot(kind='bar')`）。\n\n"
       "**問4.**（仕上げ）これで道具がそろいました。`02_統計_4級/01` を開いて、\n"
       "ヒストグラムと度数分布表に進みましょう！"),
    code("# 問1〜3\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "plt.hist(df['英語'], bins=10, edgecolor='white'); plt.show()\n"
       "plt.scatter(df['勉強時間'], df['数学'], alpha=0.5); plt.show()\n"
       "df.groupby('クラス')['英語'].mean().plot(kind='bar'); plt.show()\n"
       "```\n</details>\n\n"
       "🎉 **データ分析の三種の神器（NumPy・pandas・matplotlib）クリア！**\n"
       "これで統計・マーケのノートをスムーズに読めます。"),
]
write_nb("01_Python基礎/07_matplotlib入門.ipynb", cells)

print("=== bridge done ===")
