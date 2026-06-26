# -*- coding: utf-8 -*-
import os, urllib.parse
from nbbuild import md, code, write_nb

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
GH = "https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/"
NB_REL = "03_統計_3級/07_実践_タイタニック分析.ipynb"
ANS_REL = "解答集/03_統計_3級/07_実践_タイタニック分析.md"
colab = "https://colab.research.google.com/github/Carlo-Broschi/statistics-python-for-students/blob/main/" + urllib.parse.quote(NB_REL)
ans_url = GH + urllib.parse.quote(ANS_REL)

setup = code(
    "# === ① セットアップ（最初に実行してください）===\n"
    "import pandas as pd               # 表データ\n"
    "import numpy as np                # 数値計算\n"
    "import matplotlib.pyplot as plt   # グラフ描画\n"
    "import os\n"
    "plt.rcParams['axes.unicode_minus'] = False   # マイナス記号の文字化け防止\n"
    "# ローカルにあればそれを、無ければ公開URL（Kaggle trainと同じ内容）から読み込む\n"
    "local = '../data/titanic.csv'\n"
    "url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'\n"
    "df = pd.read_csv(local) if os.path.exists(local) else pd.read_csv(url)  # データを読み込む\n"
    "print('乗客数:', len(df))         # 行数＝乗客の人数\n"
    "df.head()                        # 先頭5行を確認"
)

cells = [
    md(f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})\n\n"
       "# 統計3級-07. 実践：タイタニック号データで「生存の分かれ目」を分析\n\n"
       "> 🟢 Colab（ブラウザ）で実行できます。Privateでなく公開リポジトリなのでGoogleアカウントだけでOK。\n"
       "> **最初に下の「① セットアップ」セルを実行**してください（データを自動で読み込みます）。\n\n"
       "**これは4級〜3級の総まとめ**です。Kaggleで有名な「タイタニック号」の乗客データを使い、\n"
       "*誰が助かりやすかったのか* を、習った道具（**データの種類・代表値・ばらつき・箱ひげ図・"
       "ヒストグラム・クロス集計・条件付き確率・相関**）だけで読み解きます。\n\n"
       "> 📌 「その差は“偶然”ではないか？」を確かめる検定（カイ二乗検定など）は **2級** で学びます。\n"
       "> ここでは「差がありそう」と読み取るところまでがゴールです。"),
    setup,
    md("### 📋 使うデータ：タイタニック号 乗客891人（Kaggle Titanic と同じ内容）\n"
       "1行＝乗客1人。`Survived` は **1=生存 / 0=死亡**。\n\n"
       "| 列 | 意味 | データの種類 |\n"
       "|---|---|---|\n"
       "| Survived | 生存(1)/死亡(0) | 質的（名義） |\n"
       "| Pclass | 客室の等級 1/2/3 | 質的（順序） |\n"
       "| Sex | 性別 | 質的（名義） |\n"
       "| Age | 年齢 | 量的 |\n"
       "| SibSp | 同乗の兄弟姉妹・配偶者の数 | 量的 |\n"
       "| Parch | 同乗の親・子の数 | 量的 |\n"
       "| Fare | 運賃 | 量的 |\n"
       "| Embarked | 乗船した港 C/Q/S | 質的（名義） |"),
    md("## 1. データの種類と欠損を確認する\n\n"
       "分析の第一歩は「どんな列か」「欠けている値はないか」の確認です。"),
    code("print(df.dtypes)            # 各列のデータ型（object=文字列, int/float=数値）\n"
         "print('\\n欠損（空欄）の数:')\n"
         "print(df.isna().sum())      # Age と Cabin に欠損が多い"),
    md("> 💡 **欠損値（けっそんち）**＝記録が空欄のデータ。`Age` は177人ぶん欠けています。\n"
       "平均などの計算では pandas が欠損を自動でとばします。年齢で分けるときは `dropna()` を使います。"),
    md("## 2. 代表値とばらつき（Age と Fare）\n\n"
       "年齢と運賃について、平均・中央値・標準偏差・変動係数を出します。"),
    code("for col in ['Age', 'Fare']:                      # 年齢と運賃について\n"
         "    s = df[col]\n"
         "    print(f'【{col}】平均 {s.mean():.1f} / 中央値 {s.median():.1f} / "
         "標準偏差 {s.std():.1f} / 変動係数 {s.std()/s.mean():.2f}')"),
    md("**読み取り**\n"
       "- `Fare` は **平均(32) ≫ 中央値(14.5)**。少数の高額運賃に平均が引っ張られている（右に裾が長い）。\n"
       "- `Fare` は **変動係数が大きい** ＝ 平均に対してばらつきが激しい（運賃の差が大きい）。\n"
       "- `Age` は平均と中央値が近く、わりと左右対称。"),
    code("fig, ax = plt.subplots(1, 2, figsize=(10, 4))   # 1行2列のグラフ\n"
         "df.boxplot(column='Age', ax=ax[0]); ax[0].set_title('年齢')   # 年齢の箱ひげ図\n"
         "df.boxplot(column='Fare', ax=ax[1]); ax[1].set_title('運賃')  # 運賃の箱ひげ図\n"
         "plt.show()"),
    md("運賃の箱ひげ図は上に外れ値（高額運賃）がたくさん。**「ふつうの乗客」を表すなら中央値**が向いています。"),
    md("## 3. ヒストグラムで分布を見る"),
    code("fig, ax = plt.subplots(1, 2, figsize=(10, 4))\n"
         "ax[0].hist(df['Age'].dropna(), bins=20, edgecolor='white')   # 年齢（欠損は除く）\n"
         "ax[0].set_title('年齢の分布')\n"
         "ax[1].hist(df['Fare'], bins=30, edgecolor='white')           # 運賃\n"
         "ax[1].set_title('運賃の分布（右に裾）')\n"
         "plt.show()"),
    md("## 4. 全体の生存率（確率の基礎）\n\n"
       "`Survived` は 0/1 なので、**平均＝生存した人の割合＝生存率**になります。"),
    code("print('全体の生存率:', round(df['Survived'].mean(), 3))   # 生存者数 ÷ 全員\n"
         "print('→ およそ38%が生存。これを基準に、グループ別で比べる')"),
    md("## 5. クロス集計と条件付き確率 ★ここが3級の山場\n\n"
       "「性別によって生存率はどれだけ違う？」をクロス集計＋行比率で見ます。\n"
       "行比率は **P(生存 | そのグループ)** ＝ 条件付き確率そのものです。"),
    code("ct = pd.crosstab(df['Sex'], df['Survived'])     # 性別×生存 の人数表\n"
         "print(ct)\n"
         "print('\\n行ごとの割合 = P(生存 | 性別):')\n"
         "print(pd.crosstab(df['Sex'], df['Survived'], normalize='index').round(3))"),
    md("**読み取り**：P(生存 | 女性) ≈ **0.74**、P(生存 | 男性) ≈ **0.19**。\n"
       "全体の0.38と比べ、女性で大きく上がり男性で下がる → **性別と生存に強い関連**"
       "（“women and children first”）。"),
    code("print('等級別の生存率 P(生存 | Pclass):')\n"
         "print(df.groupby('Pclass')['Survived'].mean().round(3))   # 等級ごとの生存率\n"
         "df.groupby('Pclass')['Survived'].mean().plot(kind='bar', title='等級別の生存率')\n"
         "plt.ylabel('生存率'); plt.xticks(rotation=0); plt.show()"),
    md("1等 0.63 → 2等 0.47 → 3等 0.24。**等級が上がるほど生存率が高い**。"),
    md("### 性別×等級の合わせ技\n"
       "2つの条件を重ねると、もっとはっきり見えます。"),
    code("# 性別と等級の組み合わせごとの生存率\n"
         "pd.crosstab([df['Sex'], df['Pclass']], df['Survived'], normalize='index').round(2)"),
    md("1等の女性はほぼ全員生存、3等の男性は最も低い、と読み取れます。"),
    md("## 6. 相関の入口（数値どうしの関係）\n\n"
       "等級(Pclass)と運賃(Fare)の関係を相関係数で見ます。"),
    code("# Pclassは順序尺度だが、数値として相関を見る（1等=1, 3等=3）\n"
         "print('Pclass と Fare の相関係数:', round(df['Pclass'].corr(df['Fare']), 3))\n\n"
         "df['家族人数'] = df['SibSp'] + df['Parch'] + 1     # 本人＋同乗家族＝家族人数\n"
         "print('家族人数 と Fare の相関係数:', round(df['家族人数'].corr(df['Fare']), 3))\n"
         "plt.scatter(df['家族人数'], df['Fare'], alpha=0.3)  # 散布図\n"
         "plt.xlabel('家族人数'); plt.ylabel('運賃'); plt.title('家族人数と運賃'); plt.show()"),
    md("- `Pclass × Fare` は **負の相関**（等級の数字が小さい＝上等ほど運賃が高い）。\n"
       "- `家族人数 × Fare` は **やや正**（大人数はまとめて高額になりがち）。"),
    md("## 🧭 まとめ\n\n"
       "- 助かりやすさ：**女性 > 男性**、**1等 > 2等 > 3等**（年齢が低い子どもも有利）。\n"
       "- `Fare` は外れ値だらけ → **中央値・箱ひげ図**が役立つ。\n"
       "- ここで見たのは「差が**ありそう**」まで。**その差が偶然でないか**の確認（カイ二乗検定・t検定）は **2級** で学びます。"),
    md("---\n## 🏆 練習問題（3級まで）\n\n"
       "**問1.** `Embarked`（乗船港 C/Q/S）ごとの生存率を、クロス集計の行比率で求めよう。最も高い港は？\n\n"
       "**問2.** 「子ども(16歳未満)」と「大人」に分けて生存率を比べよう。\n"
       "ヒント：`df['子ども'] = df['Age'] < 16` を作って `groupby`。\n\n"
       "**問3.** 運賃が中央値以上のグループと未満のグループで、生存率を比べよう。\n\n"
       "**問4.** `家族人数` と `Age` の相関係数を求めよう。関係は強い？弱い？"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    code("# 問4\n"),
    md("> 🔑 **解答例は別ページにまとめています**（ネタバレ防止）。\n"
       f"> 自分で解いてから 👉 **[07_実践_タイタニック分析 の解答例を開く]({ans_url})**"),
]
write_nb(NB_REL, cells)

# --- 解答集 ---
ans = f"""# 07_実践_タイタニック分析 ― 解答例

> 出典ノート: `{NB_REL}`　／　[本編ノートを開く]({GH + urllib.parse.quote(NB_REL)})

**問1. 乗船港ごとの生存率**
```python
print(pd.crosstab(df['Embarked'], df['Survived'], normalize='index').round(3))
# C(シェルブール)が最も高い。S(サウサンプトン)が低め。
```

**問2. 子ども(16歳未満) と 大人 の生存率**
```python
df['子ども'] = df['Age'] < 16          # 16歳未満ならTrue
print(df.groupby('子ども')['Survived'].mean().round(3))
# 子ども(True)の方が生存率が高い（"children first"）。
```

**問3. 運賃 中央値以上 / 未満 の生存率**
```python
med = df['Fare'].median()              # 運賃の中央値
print(df.groupby(df['Fare'] >= med)['Survived'].mean().round(3))
# 高運賃グループ(True)ほど生存率が高い（＝上等客が多い）。
```

**問4. 家族人数 と Age の相関**
```python
print(round(df['家族人数'].corr(df['Age']), 3))
# 弱い負の相関（大家族ほどやや若い傾向）。|r|が小さく関係は弱い。
```
"""
ans_abs = os.path.join(ROOT, ANS_REL)
os.makedirs(os.path.dirname(ans_abs), exist_ok=True)
open(ans_abs, "w", encoding="utf-8").write(ans)
print("wrote answer:", ANS_REL)
