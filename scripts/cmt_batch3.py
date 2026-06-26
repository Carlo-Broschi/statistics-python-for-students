# -*- coding: utf-8 -*-
import json, glob, os
ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"

PAIRS = [
# import 01/02
(r'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../data/students_scores.csv')
df.head()''',
r'''import numpy as np               # 数値計算
import pandas as pd              # 表データ
import matplotlib.pyplot as plt  # グラフ描画
from scipy import stats          # 統計関数（分布・検定など）
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
df = pd.read_csv('../data/students_scores.csv')   # 生徒データを読み込む
df.head()                        # 先頭5行を確認'''),
# import 03
(r'''import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
plt.rcParams['axes.unicode_minus'] = False''',
r'''import numpy as np               # 数値計算
import matplotlib.pyplot as plt  # グラフ描画
from scipy import stats          # 統計関数（分布・検定など）
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ'''),
# import 04
(r'''import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
plt.rcParams['axes.unicode_minus'] = False
rng = np.random.default_rng(7)''',
r'''import numpy as np               # 数値計算
import matplotlib.pyplot as plt  # グラフ描画
from scipy import stats          # 統計関数
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
rng = np.random.default_rng(7)   # 乱数生成器（seedで結果を固定）'''),
# import 05
(r'''import numpy as np
import pandas as pd
rng = np.random.default_rng(3)''',
r'''import numpy as np               # 数値計算
import pandas as pd              # 表データ
rng = np.random.default_rng(3)   # 乱数生成器（seedで結果を固定）'''),
# import 06
(r'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../data/students_scores.csv')''',
r'''import numpy as np               # 数値計算
import pandas as pd              # 表データ
import matplotlib.pyplot as plt  # グラフ描画
from scipy import stats          # 統計関数
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
df = pd.read_csv('../data/students_scores.csv')   # 生徒データを読み込む'''),
# 01
(r'''x = np.array([60, 70, 80, 90, 100])
mean = x.mean()
deviation = x - mean
print('偏差:', deviation)
print('分散:', np.mean(deviation**2))         # 手計算
print('分散(np):', x.var())                   # numpyは標本分散(÷n)
print('標準偏差:', x.std().round(2))''',
r'''x = np.array([60, 70, 80, 90, 100])        # データ
mean = x.mean()                            # 平均
deviation = x - mean                       # 偏差（各データ − 平均）
print('偏差:', deviation)
print('分散:', np.mean(deviation**2))         # 偏差を2乗して平均＝分散（手計算）
print('分散(np):', x.var())                   # numpyは標本分散(÷n)
print('標準偏差:', x.std().round(2))           # 分散の平方根＝標準偏差'''),
(r'''s = pd.Series([60, 70, 80, 90, 100])
print('pandas .var() ÷(n-1):', s.var())
print('numpy  .var() ÷n   :', np.var(s))
print('ddof指定で合わせる :', np.var(s, ddof=1))''',
r'''s = pd.Series([60, 70, 80, 90, 100])
print('pandas .var() ÷(n-1):', s.var())     # pandasは不偏分散(÷n-1)
print('numpy  .var() ÷n   :', np.var(s))    # numpyは÷n
print('ddof指定で合わせる :', np.var(s, ddof=1))  # ddof=1で÷(n-1)に揃う'''),
(r'''math = df['数学']
z = (math - math.mean()) / math.std()
print('標準化後の平均:', round(z.mean(), 5), ' 標準偏差:', round(z.std(), 3))''',
r'''math = df['数学']                          # 数学の列
z = (math - math.mean()) / math.std()      # 標準化：(値−平均)÷標準偏差
print('標準化後の平均:', round(z.mean(), 5), ' 標準偏差:', round(z.std(), 3))  # 平均0・標準偏差1になる'''),
(r'''df['数学偏差値'] = 50 + 10 * (math - math.mean()) / math.std()
df[['生徒ID', '数学', '数学偏差値']].sort_values('数学', ascending=False).head()''',
r'''df['数学偏差値'] = 50 + 10 * (math - math.mean()) / math.std()  # 偏差値＝50+10×z
df[['生徒ID', '数学', '数学偏差値']].sort_values('数学', ascending=False).head()  # 点数の高い順に表示'''),
# 02
(r'''plt.figure(figsize=(6, 5))
plt.scatter(df['数学'], df['英語'], alpha=0.6)
plt.xlabel('数学')
plt.ylabel('英語')
plt.title('数学と英語の関係')
plt.show()''',
r'''plt.figure(figsize=(6, 5))                  # グラフの大きさ
plt.scatter(df['数学'], df['英語'], alpha=0.6)  # 散布図（数学×英語）
plt.xlabel('数学')                          # x軸ラベル
plt.ylabel('英語')                          # y軸ラベル
plt.title('数学と英語の関係')               # タイトル
plt.show()'''),
(r'''r = df['数学'].corr(df['英語'])
print('相関係数 r =', round(r, 3))

# 全教科の相関行列
df[['数学', '英語', '国語', '勉強時間']].corr().round(2)''',
r'''r = df['数学'].corr(df['英語'])             # 数学と英語の相関係数
print('相関係数 r =', round(r, 3))

# 全教科の相関行列（各ペアの相関をまとめて表示）
df[['数学', '英語', '国語', '勉強時間']].corr().round(2)'''),
(r'''x = df['数学']
y = df['英語']
a, b = np.polyfit(x, y, 1)   # 傾きa・切片b
print(f'回帰直線: y = {a:.2f} x + {b:.2f}')

plt.figure(figsize=(6, 5))
plt.scatter(x, y, alpha=0.5)
xs = np.linspace(x.min(), x.max(), 100)
plt.plot(xs, a * xs + b, color='red', label=f'y={a:.2f}x+{b:.2f}')
plt.xlabel('数学'); plt.ylabel('英語'); plt.legend()
plt.show()''',
r'''x = df['数学']                             # 説明変数（x）
y = df['英語']                             # 目的変数（y）
a, b = np.polyfit(x, y, 1)   # 最小二乗法で 傾きa・切片b を求める
print(f'回帰直線: y = {a:.2f} x + {b:.2f}')

plt.figure(figsize=(6, 5))                 # グラフの大きさ
plt.scatter(x, y, alpha=0.5)               # 散布図
xs = np.linspace(x.min(), x.max(), 100)    # 直線を描くためのx
plt.plot(xs, a * xs + b, color='red', label=f'y={a:.2f}x+{b:.2f}')  # 回帰直線
plt.xlabel('数学'); plt.ylabel('英語'); plt.legend()
plt.show()'''),
(r'''pred = a * 85 + b
print(f'数学85点 → 英語の予測 {pred:.1f}点')''',
r'''pred = a * 85 + b                          # 回帰式に数学85を入れて英語を予測
print(f'数学85点 → 英語の予測 {pred:.1f}点')'''),
# 03
(r'''n, p = 10, 0.5
k = np.arange(0, n + 1)
prob = stats.binom.pmf(k, n, p)

plt.bar(k, prob)
plt.xlabel('表が出た回数'); plt.ylabel('確率')
plt.title(f'二項分布 B(n={n}, p={p})')
plt.show()
print('平均(np):', n*p, ' 標準偏差:', round(np.sqrt(n*p*(1-p)), 2))''',
r'''n, p = 10, 0.5                             # 試行回数nと成功確率p
k = np.arange(0, n + 1)                    # 成功回数の候補（0〜10）
prob = stats.binom.pmf(k, n, p)            # 各回数の確率（二項分布）

plt.bar(k, prob)                           # 棒グラフで分布を表示
plt.xlabel('表が出た回数'); plt.ylabel('確率')
plt.title(f'二項分布 B(n={n}, p={p})')
plt.show()
print('平均(np):', n*p, ' 標準偏差:', round(np.sqrt(n*p*(1-p)), 2))  # 平均np・標準偏差√(np(1-p))'''),
(r'''# 表がちょうど7回出る確率
print('P(X=7) =', round(stats.binom.pmf(7, 10, 0.5), 4))
# 表が8回以上出る確率
print('P(X>=8) =', round(1 - stats.binom.cdf(7, 10, 0.5), 4))''',
r'''# 表がちょうど7回出る確率
print('P(X=7) =', round(stats.binom.pmf(7, 10, 0.5), 4))     # pmf＝ちょうどその回数の確率
# 表が8回以上出る確率
print('P(X>=8) =', round(1 - stats.binom.cdf(7, 10, 0.5), 4))  # 1−(7回以下の累積)'''),
(r'''mu, sigma = 50, 10   # 平均50, 標準偏差10（偏差値の分布）
x = np.linspace(10, 90, 200)
y = stats.norm.pdf(x, mu, sigma)
plt.plot(x, y)
plt.axvline(mu, color='red', linestyle='--', label='平均')
plt.title('正規分布 N(50, 10²)'); plt.legend()
plt.show()''',
r'''mu, sigma = 50, 10   # 平均50, 標準偏差10（偏差値の分布）
x = np.linspace(10, 90, 200)               # 横軸の値
y = stats.norm.pdf(x, mu, sigma)           # 正規分布の高さ（確率密度）
plt.plot(x, y)                             # 曲線を描く
plt.axvline(mu, color='red', linestyle='--', label='平均')  # 平均の位置に縦線
plt.title('正規分布 N(50, 10²)'); plt.legend()
plt.show()'''),
(r'''for k in [1, 2, 3]:
    p = stats.norm.cdf(k) - stats.norm.cdf(-k)
    print(f'±{k}σ の中に {p*100:.1f}%')''',
r'''# 平均から±kσの範囲に入る割合を計算
for k in [1, 2, 3]:
    p = stats.norm.cdf(k) - stats.norm.cdf(-k)  # (+kσ以下の確率) − (−kσ以下の確率)
    print(f'±{k}σ の中に {p*100:.1f}%')'''),
(r'''# z = (70-50)/10 = 2.0 → 上側の確率
p = 1 - stats.norm.cdf(70, 50, 10)
print(f'偏差値70以上は上位 {p*100:.1f}%')''',
r'''# z = (70-50)/10 = 2.0 → 上側の確率
p = 1 - stats.norm.cdf(70, 50, 10)         # 70以上になる確率（上側）
print(f'偏差値70以上は上位 {p*100:.1f}%')'''),
# 04
(r'''population = rng.normal(165, 8, 100000)
print('母平均:', population.mean().round(2))

sample = rng.choice(population, size=100)
print('標本平均(100人):', sample.mean().round(2))
print('→ 全部調べなくても、母平均にかなり近い！')''',
r'''population = rng.normal(165, 8, 100000)    # 仮想の母集団（平均165・標準偏差8の身長10万人）
print('母平均:', population.mean().round(2))

sample = rng.choice(population, size=100)  # そこから100人を無作為に抽出
print('標本平均(100人):', sample.mean().round(2))
print('→ 全部調べなくても、母平均にかなり近い！')'''),
(r'''means = [rng.choice(population, 100).mean() for _ in range(2000)]
plt.hist(means, bins=40, edgecolor='white')
plt.axvline(165, color='red', linestyle='--', label='母平均')
plt.title('標本平均の分布（n=100を2000回）'); plt.legend()
plt.show()
print('標本平均たちの平均:', np.mean(means).round(2))
print('標本平均たちの標準偏差:', np.std(means).round(3))''',
r'''# 100人の標本平均を2000回くり返して集める
means = [rng.choice(population, 100).mean() for _ in range(2000)]
plt.hist(means, bins=40, edgecolor='white')         # 標本平均の分布
plt.axvline(165, color='red', linestyle='--', label='母平均')  # 母平均の位置
plt.title('標本平均の分布（n=100を2000回）'); plt.legend()
plt.show()
print('標本平均たちの平均:', np.mean(means).round(2))      # 母平均165に近い
print('標本平均たちの標準偏差:', np.std(means).round(3))    # ＝標準誤差'''),
(r'''for n in [25, 100, 400]:
    se = 8 / np.sqrt(n)
    print(f'n={n:3d} → 標準誤差 {se:.3f}（nが4倍で誤差は半分）')''',
r'''# サンプルサイズnを変えて標準誤差（母標準偏差÷√n）を比べる
for n in [25, 100, 400]:
    se = 8 / np.sqrt(n)                    # 標準誤差
    print(f'n={n:3d} → 標準誤差 {se:.3f}（nが4倍で誤差は半分）')'''),
# 05
(r'''p = (1/2) * (1/6)
print('表 かつ 6 の確率:', round(p, 4))''',
r'''p = (1/2) * (1/6)                          # 独立な事象は確率をかけ算
print('表 かつ 6 の確率:', round(p, 4))'''),
(r'''table = pd.DataFrame({'朝食あり':[180, 40], '朝食なし':[60, 120]},
                     index=['運動部', '帰宅部'])
table['合計'] = table.sum(axis=1)
print(table)

# 「運動部である」条件のもとで「朝食ありの確率」
p_break_given_sports = 180 / table.loc['運動部','合計']
print('P(朝食あり | 運動部) =', round(p_break_given_sports, 3))

# 全体での朝食ありの確率と比べる
p_break = (180+40) / table['合計'].sum()
print('P(朝食あり) =', round(p_break, 3), ' → 運動部の方が高い＝関連あり')''',
r'''# 「部活 × 朝食」のクロス集計表を作る
table = pd.DataFrame({'朝食あり':[180, 40], '朝食なし':[60, 120]},
                     index=['運動部', '帰宅部'])
table['合計'] = table.sum(axis=1)          # 行ごとの合計
print(table)

# 「運動部である」条件のもとで「朝食ありの確率」
p_break_given_sports = 180 / table.loc['運動部','合計']  # 条件付き確率 P(朝食あり|運動部)
print('P(朝食あり | 運動部) =', round(p_break_given_sports, 3))

# 全体での朝食ありの確率と比べる
p_break = (180+40) / table['合計'].sum()   # 全体の朝食あり率
print('P(朝食あり) =', round(p_break, 3), ' → 運動部の方が高い＝関連あり')'''),
# 06
(r'''x = df['数学'].values
y = df['英語'].values
cov = np.mean((x - x.mean()) * (y - y.mean()))   # 手計算(÷n)
print('共分散:', round(cov, 2))
print('np.cov(÷n-1):', round(np.cov(x, y, ddof=0)[0,1], 2))''',
r'''x = df['数学'].values                      # 数学（配列）
y = df['英語'].values                      # 英語（配列）
cov = np.mean((x - x.mean()) * (y - y.mean()))   # 共分散＝偏差の積の平均（÷n）
print('共分散:', round(cov, 2))
print('np.cov(÷n-1):', round(np.cov(x, y, ddof=0)[0,1], 2))  # numpyでも確認（ddof=0で÷n）'''),
(r'''r = cov / (x.std() * y.std())
print('相関係数(共分散から):', round(r, 3))
print('pandas .corr() で確認:', round(df['数学'].corr(df['英語']), 3))''',
r'''r = cov / (x.std() * y.std())              # 相関係数＝共分散÷(各標準偏差)
print('相関係数(共分散から):', round(r, 3))
print('pandas .corr() で確認:', round(df['数学'].corr(df['英語']), 3))'''),
(r'''height = np.array([158, 162, 170, 165, 168, 160])
weight = np.array([48, 55, 70, 60, 65, 50])
for name, d in [('身長', height), ('体重', weight)]:
    cv = d.std() / d.mean()
    print(f'{name}: 標準偏差{d.std():.1f}, 平均{d.mean():.1f}, CV={cv:.3f}')
print('→ CVが大きい方が、平均に対して相対的にばらついている')''',
r'''height = np.array([158, 162, 170, 165, 168, 160])  # 身長
weight = np.array([48, 55, 70, 60, 65, 50])        # 体重
# それぞれ 変動係数＝標準偏差÷平均 を計算
for name, d in [('身長', height), ('体重', weight)]:
    cv = d.std() / d.mean()                # 変動係数
    print(f'{name}: 標準偏差{d.std():.1f}, 平均{d.mean():.1f}, CV={cv:.3f}')
print('→ CVが大きい方が、平均に対して相対的にばらついている')'''),
(r'''n, p = 100, 0.5
k = np.arange(0, n + 1)
binom = stats.binom.pmf(k, n, p)
mu, sigma = n * p, np.sqrt(n * p * (1 - p))
xs = np.linspace(0, n, 300)
normal = stats.norm.pdf(xs, mu, sigma)

plt.bar(k, binom, alpha=0.5, label='二項分布 B(100,0.5)')
plt.plot(xs, normal, 'r-', label=f'正規近似 N({mu:.0f},{sigma**2:.0f})')
plt.legend(); plt.title('二項分布の正規近似'); plt.show()
print(f'平均 np={mu}, 標準偏差 √(np(1-p))={sigma:.2f}')''',
r'''n, p = 100, 0.5                            # 試行回数と成功確率
k = np.arange(0, n + 1)                    # 成功回数の候補
binom = stats.binom.pmf(k, n, p)           # 二項分布の確率
mu, sigma = n * p, np.sqrt(n * p * (1 - p))  # 対応する正規分布の平均と標準偏差
xs = np.linspace(0, n, 300)                # 正規曲線用のx
normal = stats.norm.pdf(xs, mu, sigma)     # 正規分布の高さ

plt.bar(k, binom, alpha=0.5, label='二項分布 B(100,0.5)')   # 二項分布（棒）
plt.plot(xs, normal, 'r-', label=f'正規近似 N({mu:.0f},{sigma**2:.0f})')  # 正規近似（曲線）
plt.legend(); plt.title('二項分布の正規近似'); plt.show()
print(f'平均 np={mu}, 標準偏差 √(np(1-p))={sigma:.2f}')'''),
(r'''exact = 1 - stats.binom.cdf(59, n, p)
# 連続補正（59.5を境にする）を入れた正規近似
approx = 1 - stats.norm.cdf(59.5, mu, sigma)
print(f'二項分布での厳密値: {exact:.4f}')
print(f'正規近似(連続補正): {approx:.4f}  → ほぼ一致')''',
r'''exact = 1 - stats.binom.cdf(59, n, p)      # 二項分布での厳密な P(X≥60)
# 連続補正（59.5を境にする）を入れた正規近似
approx = 1 - stats.norm.cdf(59.5, mu, sigma)  # 正規近似での P(X≥60)
print(f'二項分布での厳密値: {exact:.4f}')
print(f'正規近似(連続補正): {approx:.4f}  → ほぼ一致')'''),
]

MAP = {k.strip(): v for k, v in PAIRS}
replaced = 0; unmatched = []
for p in sorted(glob.glob(f"{ROOT}/03_統計_3級/*.ipynb")):
    nb = json.load(open(p, encoding="utf-8")); changed = False
    for c in nb["cells"]:
        if c["cell_type"] != "code": continue
        j = "".join(c["source"]); key = j.strip()
        if "① セットアップ（最初に実行" in j: continue
        if key in MAP:
            if j != MAP[key]: c["source"] = MAP[key]; changed = True; replaced += 1
        else:
            body = [l for l in j.splitlines() if l.strip() and not l.strip().startswith("#")]
            if body: unmatched.append((os.path.basename(p), j.splitlines()[0][:46]))
    if changed:
        json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("replaced:", replaced, " unmatched:", len(unmatched))
for u in unmatched: print("  ", u)
