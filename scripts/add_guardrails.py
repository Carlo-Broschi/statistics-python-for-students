# -*- coding: utf-8 -*-
"""数III/大学範囲が必要な箇所の直前に、1ステップの『📐 数IIIメモ』を挿入。"""
import json, os

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"

# (相対パス, アンカー=直前に入れたいコードの一部, メモ本文)
ITEMS = [
 ("03_統計_3級/03_確率分布.ipynb",
  "y = stats.norm.pdf(x, mu, sigma)",
  "> 📐 **数IIIメモ（ここだけ1分）**：正規分布の式には eˣ（指数関数）が出てきますが、"
  "**式の暗記は不要**です。押さえるのは「**連続データの確率＝曲線の下の“面積”**」という考え方だけ。"
  "その面積（確率）は `scipy` が計算してくれます。"),

 ("04_統計_2級/01_区間推定.ipynb",
  "t = stats.t.ppf(0.975, df=n-1)",
  "> 📐 **数IIIメモ**：**t分布**は「正規分布に似た、すそが少し重い連続分布」。標本が小さいときの"
  "不確かさを表します。形は自由度（n−1）で決まる、とだけ分かればOK（値は `scipy` が出します）。"),

 ("04_統計_2級/02_仮説検定.ipynb",
  "stats.ttest_1samp(data, popmean=200)",
  "> 📐 **数IIIメモ**：**p値**は「連続分布のすその“面積”」です。面積を出す積分は `scipy` がやるので、"
  "ここでは『**p値が小さい＝めったに起きない＝偶然では説明しにくい**』という意味だけ押さえれば十分。"),

 ("04_統計_2級/03_カイ二乗と分散分析.ipynb",
  "stats.chi2_contingency(table)",
  "> 📐 **数IIIメモ**：**カイ二乗分布・F分布**も連続分布の一種で、導出は大学範囲。"
  "ここでは検定のための“ものさし”として `scipy` に計算してもらい、**p値の読み方**に集中します。"),

 ("04_統計_2級/05_いろいろな確率分布とベイズ.ipynb",
  "stats.poisson.pmf(k, lam)",
  "> 📐 **数IIIメモ**：ポアソン分布・指数分布の式には e（自然対数の底）が出てきますが、"
  "**形と使いどころ**が分かれば十分です。確率の値は `scipy` が計算します。"),

 ("04_統計_2級/05_いろいろな確率分布とベイズ.ipynb",
  "p_pos = sens * prior + (1 - spec) * (1 - prior)",
  "> 📐 **ひとことメモ**：ベイズの定理は『**新しい情報で確率を更新する**』という考え方が要点。"
  "数IIIは不要で、下の式は“かけ算と足し算”だけで計算できます。"),

 ("04_統計_2級/06_重回帰分析.ipynb",
  "smf.ols('数学 ~ 英語 + 国語 + 勉強時間', data=df).fit()",
  "> 📐 **数IIIメモ**：重回帰の係数は内部で**行列の計算（大学範囲）**で求まりますが、**手計算は不要**。"
  "ここでは『各要因が結果をどれだけ動かすか（偏回帰係数）』の**読み方**に集中します。"),

 ("06_発展_マーケ分析/01_ドライバー分析_回帰.ipynb",
  "smf.logit('受注 ~ 商談金額 + C(獲得チャネル)', data=btob).fit()",
  "> 📐 **数IIIメモ**：ロジスティック回帰は内部で **log（対数）と eˣ** を使い、結果を0〜1の確率に変換します。"
  "導出は大学範囲なので不要。**『オッズ比＝何倍そうなりやすいか』**の読み方だけ押さえればOK。"),

 ("06_発展_マーケ分析/02_時系列予測.ipynb",
  "ExponentialSmoothing(ts, trend='add', seasonal='add'",
  "> 📐 **ひとことメモ**：指数平滑は『**最近のデータほど重くした加重平均**』。重みが指数的に減るので“指数”平滑。"
  "理屈の式は不要で、`statsmodels` に任せて**予測の使い方**を学びます。"),

 ("06_発展_マーケ分析/03_顧客セグメンテーション_RFM.ipynb",
  "PCA(n_components=2)",
  "> 📐 **数IIIメモ**：PCA（主成分分析）は内部で**線形代数（大学範囲）**を使いますが、ここでの役割は"
  "『**3つの数値(R/F/M)を、情報をなるべく保ったまま2つに圧縮して絵にする**』だけ。計算は `sklearn` がやります。"),
]

def mdcell(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text}

inserted = 0; missing = []
for rel, anchor, note in ITEMS:
    p = os.path.join(ROOT, rel)
    nb = json.load(open(p, encoding="utf-8"))
    cells = nb["cells"]
    # すでに同じメモがあればスキップ（冪等）
    if any(note[:18] in "".join(c["source"]) for c in cells if c["cell_type"] == "markdown"):
        continue
    idx = None
    for i, c in enumerate(cells):
        if c["cell_type"] == "code" and anchor in "".join(c["source"]):
            idx = i; break
    if idx is None:
        missing.append((rel, anchor)); continue
    cells.insert(idx, mdcell(note))
    json.dump(nb, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    inserted += 1
    print("inserted into", rel)

print("\ninserted:", inserted)
if missing:
    print("ANCHOR NOT FOUND:")
    for m in missing: print("  ", m)
