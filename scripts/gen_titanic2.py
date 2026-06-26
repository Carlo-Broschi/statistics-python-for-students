# -*- coding: utf-8 -*-
import os, urllib.parse
from nbbuild import md, code, write_nb

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
GH = "https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/"
NB_REL = "04_統計_2級/08_実践_タイタニック分析.ipynb"
ANS_REL = "解答集/04_統計_2級/08_実践_タイタニック分析.md"
colab = "https://colab.research.google.com/github/Carlo-Broschi/statistics-python-for-students/blob/main/" + urllib.parse.quote(NB_REL)
ans_url = GH + urllib.parse.quote(ANS_REL)
nb3_url = GH + urllib.parse.quote("03_統計_3級/07_実践_タイタニック分析.ipynb")

setup = code(
    "# === ① セットアップ（最初に実行してください）===\n"
    "import pandas as pd               # 表データ\n"
    "import numpy as np                # 数値計算\n"
    "import matplotlib.pyplot as plt   # グラフ描画\n"
    "from scipy import stats           # 検定・分布\n"
    "import os\n"
    "plt.rcParams['axes.unicode_minus'] = False   # マイナス記号の文字化け防止\n"
    "# ローカルにあればそれを、無ければ公開URL（Kaggle trainと同じ内容）から読み込む\n"
    "local = '../data/titanic.csv'\n"
    "url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'\n"
    "df = pd.read_csv(local) if os.path.exists(local) else pd.read_csv(url)  # データを読み込む\n"
    "df['家族人数'] = df['SibSp'] + df['Parch'] + 1   # 本人＋同乗家族＝家族人数（後で使う）\n"
    "print('乗客数:', len(df))\n"
    "df.head()"
)

cells = [
    md(f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})\n\n"
       "# 統計2級-08. 実践：タイタニックを「検定」で分析する\n\n"
       "> 🟢 Colab（ブラウザ）で実行できます。**最初に下の「① セットアップ」セルを実行**してください。\n\n"
       f"[3級の実践ノート]({nb3_url})では「女性の生存率が高い**ように見える**（0.74 vs 0.19）」まで読み取りました。\n"
       "**この2級ノートでは、その差が“偶然ではない”かを検定で確かめます。**\n\n"
       "使う2級の道具：**カイ二乗検定・母比率の差の検定・2標本t検定・区間推定・分散分析(ANOVA)・重回帰**。"),
    setup,
    md("## 1. 出発点：3級で見えた“差”\n\n"
       "性別ごとの生存率をもう一度確認します。これが「本物の差」かを以降で検定します。"),
    code("print('性別ごとの生存率 P(生存 | 性別):')\n"
         "print(df.groupby('Sex')['Survived'].mean().round(3))\n"
         "print('全体:', round(df['Survived'].mean(), 3))"),
    md("## 2. カイ二乗 独立性の検定（性別と生存は関連がある？）\n\n"
       "- 帰無仮説 H₀：性別と生存は**無関係**（差は偶然）\n"
       "- 対立仮説 H₁：性別と生存に**関連がある**\n\n"
       "クロス集計表からカイ二乗検定をします。"),
    code("ct = pd.crosstab(df['Sex'], df['Survived'])         # 性別×生存 の人数表\n"
         "print(ct)\n"
         "chi2, p, dof, expected = stats.chi2_contingency(ct)  # カイ二乗 独立性の検定\n"
         "print(f'\\nカイ二乗 = {chi2:.1f}, 自由度 = {dof}, p値 = {p:.2e}')\n"
         "print('結論:', '性別と生存に関連あり（有意）' if p < 0.05 else '関連があるとは言えない')"),
    md("p値はほぼ0（≈10⁻⁵⁸）。**「偶然こんな差が出る確率はほぼゼロ」→ 性別と生存は確かに関連**しています。\n"
       "3級の「ありそう」が、2級の検定で「確かにある」になりました。"),
    md("## 3. 母比率の差の検定（女性と男性の生存率の差）\n\n"
       "2グループの**割合の差**を直接検定します（A/Bテストと同じ手法）。"),
    code("from statsmodels.stats.proportion import proportions_ztest\n"
         "f = df[df['Sex'] == 'female']['Survived']    # 女性の生存(0/1)\n"
         "m = df[df['Sex'] == 'male']['Survived']      # 男性の生存(0/1)\n"
         "z, p = proportions_ztest([f.sum(), m.sum()], [len(f), len(m)])  # 2群の比率の差の検定\n"
         "print(f'女性 {f.mean():.3f} vs 男性 {m.mean():.3f}')\n"
         "print(f'z = {z:.1f}, p値 = {p:.2e}')\n"
         "print('結論:', '生存率に差あり（有意）' if p < 0.05 else '差は有意でない')"),
    md("## 4. 2標本t検定（生存者と死亡者で運賃の平均は違う？）\n\n"
       "今度は**量的データ（運賃）の平均の差**。等分散を仮定しないWelchのt検定を使います。"),
    code("s = df[df['Survived'] == 1]['Fare']    # 生存者の運賃\n"
         "d = df[df['Survived'] == 0]['Fare']    # 死亡者の運賃\n"
         "t, p = stats.ttest_ind(s, d, equal_var=False)   # Welchの2標本t検定\n"
         "print(f'平均運賃  生存 {s.mean():.1f} / 死亡 {d.mean():.1f}')\n"
         "print(f't = {t:.1f}, p値 = {p:.2e}')\n"
         "print('結論:', '運賃の平均に差あり（生存者が高い）' if p < 0.05 else '差は有意でない')"),
    md("生存者のほうが平均運賃が高い（48.4 vs 22.1）＝**高い運賃＝上等客ほど助かりやすかった**ことの裏づけ。"),
    md("## 5. 区間推定（信頼区間）\n\n"
       "1つの数（点推定）ではなく「だいたいこの範囲」と幅で示します。"),
    code("# (1) 全体の生存率の95%信頼区間（母比率の区間推定）\n"
         "n = len(df); ph = df['Survived'].mean()\n"
         "se = np.sqrt(ph * (1 - ph) / n)               # 比率の標準誤差\n"
         "print(f'生存率 {ph:.3f}  95%CI [{ph - 1.96*se:.3f}, {ph + 1.96*se:.3f}]')\n\n"
         "# (2) 平均運賃の95%信頼区間（母平均の区間推定・t分布）\n"
         "fare = df['Fare']\n"
         "ci = stats.t.interval(0.95, len(fare) - 1, loc=fare.mean(),\n"
         "                      scale=fare.std(ddof=1) / np.sqrt(len(fare)))\n"
         "print('平均運賃 95%CI:', np.round(ci, 1))"),
    md("## 6. 一元配置分散分析（ANOVA：等級で運賃の平均は違う？）\n\n"
       "3グループ以上（1等・2等・3等）の平均を**一度に**比較します。"),
    code("groups = [df[df['Pclass'] == c]['Fare'] for c in [1, 2, 3]]  # 等級ごとの運賃\n"
         "F, p = stats.f_oneway(*groups)                  # 一元配置分散分析\n"
         "print(f'F = {F:.1f}, p値 = {p:.2e}')\n"
         "print('結論:', '等級によって平均運賃が違う（有意）' if p < 0.05 else '差は有意でない')\n"
         "df.boxplot(column='Fare', by='Pclass'); plt.suptitle(''); plt.title('等級別の運賃'); plt.show()"),
    md("## 7. 重回帰分析（運賃を複数の要因で説明する）\n\n"
       "運賃 `Fare` を **等級・家族人数・年齢** で説明します（等級はダミー変数）。\n"
       "偏回帰係数・決定係数・各係数のp値を読みます。"),
    code("import statsmodels.formula.api as smf\n"
         "d2 = df.dropna(subset=['Age'])                 # Ageの欠損行を除く\n"
         "model = smf.ols('Fare ~ C(Pclass) + 家族人数 + Age', data=d2).fit()  # 重回帰\n"
         "print('決定係数 R^2:', round(model.rsquared, 3))\n"
         "print('\\n偏回帰係数:'); print(model.params.round(2))\n"
         "print('\\n各係数のp値:'); print(model.pvalues.round(4))"),
    md("R²≈0.42。`C(Pclass)` の係数から、2等・3等は1等より運賃が大きく下がる（基準=1等）と読めます。"),
    md("## 🧭 まとめ\n\n"
       "- 3級の「差がありそう」→ **2級の検定で「偶然ではない」と確認**できた（性別・等級と生存、運賃の差すべて有意）。\n"
       "- 区間推定で「生存率は約35〜42%」のように**幅**で表現できた。\n"
       "- ANOVA・重回帰で複数グループ・複数要因も扱えた。\n\n"
       "> 🔭 **発展メモ**：`Survived` は0/1なので、「生存の確率」を予測するなら本当は\n"
       "> **ロジスティック回帰**が適切です（直線回帰だと確率が0〜1をはみ出す）。\n"
       "> これは2級の少し先（準1級〜）のテーマです。"),
    md("---\n## 🏆 練習問題（2級）\n\n"
       "**問1.** `Pclass` と `Survived` のカイ二乗 独立性の検定を行い、等級と生存に関連があるか確かめよう。\n\n"
       "**問2.** 生存者と死亡者で `Age` の平均に差があるか、Welchの2標本t検定で調べよう（欠損は `dropna()`）。\n\n"
       "**問3.** 全体の平均運賃の **99%** 信頼区間を求め、95%のときと幅を比べよう。\n\n"
       "**問4.** 重回帰 `Fare ~ C(Pclass) + 家族人数 + C(Embarked)` を作り、決定係数を確認しよう。"),
    code("# 問1\n"),
    code("# 問2\n"),
    code("# 問3\n"),
    code("# 問4\n"),
    md("> 🔑 **解答例は別ページにまとめています**（ネタバレ防止）。\n"
       f"> 自分で解いてから 👉 **[08_実践_タイタニック分析 の解答例を開く]({ans_url})**"),
]
write_nb(NB_REL, cells)

ans = f"""# 08_実践_タイタニック分析（2級）― 解答例

> 出典ノート: `{NB_REL}`　／　[本編ノートを開く]({GH + urllib.parse.quote(NB_REL)})

**問1. Pclass × Survived のカイ二乗検定**
```python
ct = pd.crosstab(df['Pclass'], df['Survived'])
chi2, p, dof, _ = stats.chi2_contingency(ct)
print(f'chi2={{chi2:.1f}}, p={{p:.2e}}')   # p≈4.5e-23 → 等級と生存に関連あり（有意）
```

**問2. 生存者 vs 死亡者の Age の平均差（Welch t検定）**
```python
sa = df[df['Survived']==1]['Age'].dropna()
da = df[df['Survived']==0]['Age'].dropna()
t, p = stats.ttest_ind(sa, da, equal_var=False)
print(f't={{t:.2f}}, p={{p:.3f}} (生{{sa.mean():.1f}} 死{{da.mean():.1f}})')
# p≈0.04 → わずかだが有意。生存者のほうがやや若い。
```

**問3. 平均運賃の99%信頼区間（95%と比較）**
```python
fare = df['Fare']; se = fare.std(ddof=1)/ (len(fare)**0.5)
for conf in [0.95, 0.99]:
    lo, hi = stats.t.interval(conf, len(fare)-1, loc=fare.mean(), scale=se)
    print(f'{{int(conf*100)}}%CI [{{lo:.1f}}, {{hi:.1f}}]  幅={{hi-lo:.1f}}')
# 99%のほうが区間は広い（確信度を上げると幅が広がる）。
```

**問4. 重回帰に乗船港(Embarked)も入れる**
```python
import statsmodels.formula.api as smf
d2 = df.dropna(subset=['Age', 'Embarked'])
model = smf.ols('Fare ~ C(Pclass) + 家族人数 + C(Embarked)', data=d2).fit()
print('R^2:', round(model.rsquared, 3))
print(model.pvalues.round(4))
```
"""
ans_abs = os.path.join(ROOT, ANS_REL)
os.makedirs(os.path.dirname(ans_abs), exist_ok=True)
open(ans_abs, "w", encoding="utf-8").write(ans)
print("wrote answer:", ANS_REL)
