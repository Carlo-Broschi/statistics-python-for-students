# -*- coding: utf-8 -*-
import json, glob, os
ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"

PAIRS = [
# 2級 共通import（01,02,03,04,05,07）
(r'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
plt.rcParams['axes.unicode_minus'] = False
rng = np.random.default_rng(0)''',
r'''import numpy as np               # 数値計算
import pandas as pd              # 表データ
import matplotlib.pyplot as plt  # グラフ描画
from scipy import stats          # 統計関数（分布・検定など）
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
rng = np.random.default_rng(0)   # 乱数生成器（seedで結果を固定）'''),
# 2級06 import
(r'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../data/students_scores.csv')
df.head()''',
r'''import numpy as np               # 数値計算
import pandas as pd              # 表データ
import matplotlib.pyplot as plt  # グラフ描画
import statsmodels.formula.api as smf   # 回帰分析
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
df = pd.read_csv('../data/students_scores.csv')   # 生徒データを読み込む
df.head()                        # 先頭5行を確認'''),
# 01
(r'''data = np.array([198, 203, 197, 205, 199, 201, 196, 204, 200, 202])
n = len(data)
mean = data.mean()
s = data.std(ddof=1)            # 不偏標準偏差
se = s / np.sqrt(n)             # 標準誤差
t = stats.t.ppf(0.975, df=n-1)  # 自由度n-1のt値
low, high = mean - t*se, mean + t*se
print(f'標本平均: {mean:.2f}')
print(f'95%信頼区間: [{low:.2f}, {high:.2f}]')''',
r'''data = np.array([198, 203, 197, 205, 199, 201, 196, 204, 200, 202])  # 標本データ
n = len(data)                   # 標本サイズ
mean = data.mean()              # 標本平均
s = data.std(ddof=1)            # 不偏標準偏差
se = s / np.sqrt(n)             # 標準誤差
t = stats.t.ppf(0.975, df=n-1)  # 自由度n-1のt値（両側95%）
low, high = mean - t*se, mean + t*se  # 信頼区間の下限・上限
print(f'標本平均: {mean:.2f}')
print(f'95%信頼区間: [{low:.2f}, {high:.2f}]')'''),
(r'''# scipyに任せると1行
ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
print('95%CI:', np.round(ci, 2))''',
r'''# scipyに任せると1行で95%信頼区間が出る
ci = stats.t.interval(0.95, df=n-1, loc=mean, scale=se)
print('95%CI:', np.round(ci, 2))'''),
(r'''for conf in [0.90, 0.95, 0.99]:
    lo, hi = stats.t.interval(conf, df=n-1, loc=mean, scale=se)
    print(f'{int(conf*100)}%CI 幅 = {hi-lo:.2f}')''',
r'''# 信頼度を変えると区間の幅がどう変わるか
for conf in [0.90, 0.95, 0.99]:
    lo, hi = stats.t.interval(conf, df=n-1, loc=mean, scale=se)  # 各信頼度の区間
    print(f'{int(conf*100)}%CI 幅 = {hi-lo:.2f}')   # 信頼度が高いほど幅が広い'''),
(r'''x, n = 96, 400
p = x / n
se = np.sqrt(p * (1 - p) / n)
z = stats.norm.ppf(0.975)   # 1.96
print(f'賛成率の推定: {p:.3f}')
print(f'95%信頼区間: [{p - z*se:.3f}, {p + z*se:.3f}]')''',
r'''x, n = 96, 400                  # 賛成人数と回答者数
p = x / n                       # 標本比率
se = np.sqrt(p * (1 - p) / n)   # 比率の標準誤差
z = stats.norm.ppf(0.975)   # 1.96（両側95%）
print(f'賛成率の推定: {p:.3f}')
print(f'95%信頼区間: [{p - z*se:.3f}, {p + z*se:.3f}]')'''),
# 02
(r'''data = np.array([198, 203, 197, 205, 199, 201, 196, 204, 200, 197,
                 195, 199, 198, 200, 196])
t_stat, p = stats.ttest_1samp(data, popmean=200)
print(f'標本平均: {data.mean():.2f}')
print(f't統計量: {t_stat:.3f},  p値: {p:.3f}')
alpha = 0.05
print('結論:', '200gと言えない（棄却）' if p < alpha else '200gでないとは言えない')''',
r'''data = np.array([198, 203, 197, 205, 199, 201, 196, 204, 200, 197,   # 内容量の標本
                 195, 199, 198, 200, 196])
t_stat, p = stats.ttest_1samp(data, popmean=200)  # 母平均=200 との1標本t検定
print(f'標本平均: {data.mean():.2f}')
print(f't統計量: {t_stat:.3f},  p値: {p:.3f}')
alpha = 0.05                    # 有意水準
print('結論:', '200gと言えない（棄却）' if p < alpha else '200gでないとは言えない')'''),
(r'''classA = rng.normal(62, 12, 30)
classB = rng.normal(70, 12, 30)
t_stat, p = stats.ttest_ind(classA, classB)
print(f'Aの平均 {classA.mean():.1f}, Bの平均 {classB.mean():.1f}')
print(f't={t_stat:.3f}, p={p:.4f}')
print('結論:', '差は有意' if p < 0.05 else '差は有意でない')''',
r'''classA = rng.normal(62, 12, 30)            # A組（平均62）
classB = rng.normal(70, 12, 30)            # B組（平均70）
t_stat, p = stats.ttest_ind(classA, classB)  # 2標本t検定（平均の差）
print(f'Aの平均 {classA.mean():.1f}, Bの平均 {classB.mean():.1f}')
print(f't={t_stat:.3f}, p={p:.4f}')
print('結論:', '差は有意' if p < 0.05 else '差は有意でない')'''),
(r'''from statsmodels.stats.proportion import proportions_ztest
count, nobs = 80, 600
z, p = proportions_ztest(count, nobs, value=1/6, alternative='two-sided')
print(f'観測比率 {count/nobs:.3f} (理論 {1/6:.3f})')
print(f'z={z:.3f}, p={p:.4f}')
print('結論:', 'いかさまの疑い' if p < 0.05 else '偶然の範囲')''',
r'''from statsmodels.stats.proportion import proportions_ztest  # 母比率の検定
count, nobs = 80, 600           # 1の目の回数と総試行
z, p = proportions_ztest(count, nobs, value=1/6, alternative='two-sided')  # 比率=1/6の検定
print(f'観測比率 {count/nobs:.3f} (理論 {1/6:.3f})')
print(f'z={z:.3f}, p={p:.4f}')
print('結論:', 'いかさまの疑い' if p < 0.05 else '偶然の範囲')'''),
(r'''# 問2
btob = pd.read_csv('../data/sales_btob.csv')''',
r'''# 問2
btob = pd.read_csv('../data/sales_btob.csv')   # 商談データを読み込む'''),
# 03
(r'''btob = pd.read_csv('../data/sales_btob.csv')
table = pd.crosstab(btob['獲得チャネル'], btob['受注'])
print(table)
chi2, p, dof, expected = stats.chi2_contingency(table)
print(f'\nカイ二乗統計量: {chi2:.2f}')
print(f'自由度: {dof},  p値: {p:.5f}')
print('結論:', 'チャネルと受注に関連あり' if p < 0.05 else '関連があるとは言えない')''',
r'''btob = pd.read_csv('../data/sales_btob.csv')   # 商談データ読み込み
table = pd.crosstab(btob['獲得チャネル'], btob['受注'])  # チャネル×受注のクロス表
print(table)
chi2, p, dof, expected = stats.chi2_contingency(table)  # カイ二乗 独立性の検定
print(f'\nカイ二乗統計量: {chi2:.2f}')
print(f'自由度: {dof},  p値: {p:.5f}')
print('結論:', 'チャネルと受注に関連あり' if p < 0.05 else '関連があるとは言えない')'''),
(r'''pd.DataFrame(expected, index=table.index, columns=table.columns).round(1)''',
r'''pd.DataFrame(expected, index=table.index, columns=table.columns).round(1)  # 期待度数（関連が無い場合の理論値）'''),
(r'''observed = np.array([18, 21, 16, 14, 17, 14])
expected = np.full(6, observed.sum() / 6)   # 各16.67
chi2, p = stats.chisquare(observed, expected)
print(f'chi2={chi2:.2f}, p={p:.3f}')
print('結論:', '均等でない' if p < 0.05 else '均等といえる')''',
r'''observed = np.array([18, 21, 16, 14, 17, 14])  # 各目の観測回数
expected = np.full(6, observed.sum() / 6)   # 均等なら各回数（期待度数）
chi2, p = stats.chisquare(observed, expected)  # 適合度検定
print(f'chi2={chi2:.2f}, p={p:.3f}')
print('結論:', '均等でない' if p < 0.05 else '均等といえる')'''),
(r'''storeA = rng.normal(50, 8, 20)
storeB = rng.normal(55, 8, 20)
storeC = rng.normal(58, 8, 20)
f_stat, p = stats.f_oneway(storeA, storeB, storeC)
print(f'F統計量: {f_stat:.3f},  p値: {p:.4f}')
print('結論:', '少なくとも1店舗は平均が違う' if p < 0.05 else '差は有意でない')

plt.boxplot([storeA, storeB, storeC], tick_labels=['A', 'B', 'C'])
plt.ylabel('売上'); plt.title('店舗別の売上')
plt.show()''',
r'''storeA = rng.normal(50, 8, 20)             # 店舗Aの売上
storeB = rng.normal(55, 8, 20)             # 店舗B
storeC = rng.normal(58, 8, 20)             # 店舗C
f_stat, p = stats.f_oneway(storeA, storeB, storeC)  # 一元配置分散分析（3群の平均比較）
print(f'F統計量: {f_stat:.3f},  p値: {p:.4f}')
print('結論:', '少なくとも1店舗は平均が違う' if p < 0.05 else '差は有意でない')

plt.boxplot([storeA, storeB, storeC], tick_labels=['A', 'B', 'C'])  # 箱ひげ図で比較
plt.ylabel('売上'); plt.title('店舗別の売上')
plt.show()'''),
(r'''# 問3
df = pd.read_csv('../data/students_scores.csv')''',
r'''# 問3
df = pd.read_csv('../data/students_scores.csv')  # 生徒データを読み込む'''),
# 04
(r'''data = np.array([50.5, 49.2, 51.8, 48.6, 52.3, 47.9, 50.1, 53.0, 48.0, 51.2])
n = len(data)
s2 = data.var(ddof=1)
sigma0_2 = 4.0          # 帰無仮説の分散
chi2 = (n - 1) * s2 / sigma0_2
# 片側(分散が大きい方)の検定
p = 1 - stats.chi2.cdf(chi2, df=n - 1)
print(f'標本分散 s^2 = {s2:.2f}')
print(f'χ² = {chi2:.2f},  p値 = {p:.4f}')
print('結論:', '分散は4より大きい' if p < 0.05 else '規格内といえる')''',
r'''data = np.array([50.5, 49.2, 51.8, 48.6, 52.3, 47.9, 50.1, 53.0, 48.0, 51.2])  # 重さの標本
n = len(data)           # 標本サイズ
s2 = data.var(ddof=1)   # 不偏分散
sigma0_2 = 4.0          # 帰無仮説の分散
chi2 = (n - 1) * s2 / sigma0_2   # 検定統計量（カイ二乗）
# 片側(分散が大きい方)の検定
p = 1 - stats.chi2.cdf(chi2, df=n - 1)   # 上側のp値
print(f'標本分散 s^2 = {s2:.2f}')
print(f'χ² = {chi2:.2f},  p値 = {p:.4f}')
print('結論:', '分散は4より大きい' if p < 0.05 else '規格内といえる')'''),
(r'''groupA = rng.normal(50, 5, 15)
groupB = rng.normal(50, 9, 18)   # Bの方がばらつき大
F = groupA.var(ddof=1) / groupB.var(ddof=1)
dfA, dfB = len(groupA) - 1, len(groupB) - 1
# 両側p値
p = 2 * min(stats.f.cdf(F, dfA, dfB), 1 - stats.f.cdf(F, dfA, dfB))
print(f'F = {F:.3f},  p値 = {p:.4f}')
print('結論:', '分散は等しくない' if p < 0.05 else '等分散といえる')''',
r'''groupA = rng.normal(50, 5, 15)             # A群（ばらつき小）
groupB = rng.normal(50, 9, 18)   # Bの方がばらつき大
F = groupA.var(ddof=1) / groupB.var(ddof=1)  # 分散比（F統計量）
dfA, dfB = len(groupA) - 1, len(groupB) - 1  # それぞれの自由度
# 両側p値
p = 2 * min(stats.f.cdf(F, dfA, dfB), 1 - stats.f.cdf(F, dfA, dfB))  # 両側のp値
print(f'F = {F:.3f},  p値 = {p:.4f}')
print('結論:', '分散は等しくない' if p < 0.05 else '等分散といえる')'''),
(r'''# 同じ2群を2通りで検定
print('Student (等分散仮定):', stats.ttest_ind(groupA, groupB, equal_var=True))
print('Welch  (非等分散)  :', stats.ttest_ind(groupA, groupB, equal_var=False))''',
r'''# 同じ2群を2通りで検定
print('Student (等分散仮定):', stats.ttest_ind(groupA, groupB, equal_var=True))   # 等分散を仮定
print('Welch  (非等分散)  :', stats.ttest_ind(groupA, groupB, equal_var=False))  # 等分散を仮定しない'''),
(r'''from statsmodels.stats.proportion import proportions_ztest
count = np.array([84, 120])     # 申込数
nobs = np.array([1000, 1050])   # 訪問数
z, p = proportions_ztest(count, nobs)
print(f'A: {count[0]/nobs[0]:.3f},  B: {count[1]/nobs[1]:.3f}')
print(f'z = {z:.3f},  p値 = {p:.4f}')
print('結論:', '比率に差あり' if p < 0.05 else '差は有意でない')''',
r'''from statsmodels.stats.proportion import proportions_ztest  # 母比率の検定
count = np.array([84, 120])     # 申込数
nobs = np.array([1000, 1050])   # 訪問数
z, p = proportions_ztest(count, nobs)  # 2群の比率の差の検定
print(f'A: {count[0]/nobs[0]:.3f},  B: {count[1]/nobs[1]:.3f}')
print(f'z = {z:.3f},  p値 = {p:.4f}')
print('結論:', '比率に差あり' if p < 0.05 else '差は有意でない')'''),
# 05
(r'''lam = 3   # 1時間に平均3件
k = np.arange(0, 11)
plt.bar(k, stats.poisson.pmf(k, lam))
plt.title(f'ポアソン分布 λ={lam}'); plt.xlabel('件数'); plt.show()
print('1時間に0件の確率:', round(stats.poisson.pmf(0, lam), 4))
print('5件以上の確率   :', round(1 - stats.poisson.cdf(4, lam), 4))''',
r'''lam = 3   # 1時間に平均3件
k = np.arange(0, 11)                       # 件数の候補（0〜10）
plt.bar(k, stats.poisson.pmf(k, lam))      # ポアソン分布の確率を棒グラフに
plt.title(f'ポアソン分布 λ={lam}'); plt.xlabel('件数'); plt.show()
print('1時間に0件の確率:', round(stats.poisson.pmf(0, lam), 4))      # ちょうど0件
print('5件以上の確率   :', round(1 - stats.poisson.cdf(4, lam), 4))  # 1−(4件以下)'''),
(r'''print('B(1000, 0.003) で k=2:', round(stats.binom.pmf(2, 1000, 0.003), 5))
print('Poisson(3)    で k=2:', round(stats.poisson.pmf(2, 3), 5))''',
r'''print('B(1000, 0.003) で k=2:', round(stats.binom.pmf(2, 1000, 0.003), 5))  # 二項分布
print('Poisson(3)    で k=2:', round(stats.poisson.pmf(2, 3), 5))           # ポアソン近似（λ=np=3）'''),
(r'''p = 0.2
k = np.arange(1, 21)
plt.bar(k, stats.geom.pmf(k, p))
plt.title(f'幾何分布 p={p}（平均 {1/p:.0f}回）'); plt.show()
print('3回目で初成功:', round(stats.geom.pmf(3, p), 4))''',
r'''p = 0.2                                    # 1回の成功確率
k = np.arange(1, 21)                       # 初成功までの回数の候補
plt.bar(k, stats.geom.pmf(k, p))           # 幾何分布の確率を棒グラフに
plt.title(f'幾何分布 p={p}（平均 {1/p:.0f}回）'); plt.show()
print('3回目で初成功:', round(stats.geom.pmf(3, p), 4))  # ちょうど3回目で初成功'''),
(r'''xs = np.linspace(0, 5, 200)
fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
ax[0].plot(xs, stats.uniform.pdf(xs, 0, 2)); ax[0].set_title('一様分布 U(0,2)')
ax[1].plot(xs, stats.expon.pdf(xs, scale=1/1.5)); ax[1].set_title('指数分布 λ=1.5')
plt.show()
# 平均2件/時のとき、次の客まで30分以上空く確率
print('指数分布 P(待ち>0.5h):', round(1 - stats.expon.cdf(0.5, scale=1/2), 4))''',
r'''xs = np.linspace(0, 5, 200)                # 横軸の値
fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))  # 1行2列のグラフ
ax[0].plot(xs, stats.uniform.pdf(xs, 0, 2)); ax[0].set_title('一様分布 U(0,2)')   # 左：一様分布
ax[1].plot(xs, stats.expon.pdf(xs, scale=1/1.5)); ax[1].set_title('指数分布 λ=1.5')  # 右：指数分布
plt.show()
# 平均2件/時のとき、次の客まで30分以上空く確率
print('指数分布 P(待ち>0.5h):', round(1 - stats.expon.cdf(0.5, scale=1/2), 4))  # 1−(0.5h以下)'''),
(r'''prior = 0.01                 # 有病率 P(病気)
sens = 0.99                  # 感度 P(陽性|病気)
spec = 0.95                  # 特異度 P(陰性|健康)
p_pos = sens * prior + (1 - spec) * (1 - prior)   # P(陽性)
posterior = sens * prior / p_pos
print(f'P(陽性) = {p_pos:.4f}')
print(f'P(病気 | 陽性) = {posterior:.3f}')
print('→ 陽性でも実際に病気の確率は約', round(posterior*100), '%（直感より低い！）')''',
r'''prior = 0.01                 # 有病率 P(病気)
sens = 0.99                  # 感度 P(陽性|病気)
spec = 0.95                  # 特異度 P(陰性|健康)
p_pos = sens * prior + (1 - spec) * (1 - prior)   # P(陽性)＝病気で陽性＋健康で誤陽性
posterior = sens * prior / p_pos                  # ベイズの定理 P(病気|陽性)
print(f'P(陽性) = {p_pos:.4f}')
print(f'P(病気 | 陽性) = {posterior:.3f}')
print('→ 陽性でも実際に病気の確率は約', round(posterior*100), '%（直感より低い！）')'''),
# 06
(r'''model = smf.ols('数学 ~ 英語 + 国語 + 勉強時間', data=df).fit()
print(model.summary())''',
r'''model = smf.ols('数学 ~ 英語 + 国語 + 勉強時間', data=df).fit()  # 重回帰モデルを当てはめる
print(model.summary())                     # 回帰の詳しい結果を表示'''),
(r'''print('決定係数 R^2      :', round(model.rsquared, 3))
print('自由度調整済み R^2:', round(model.rsquared_adj, 3))
print('\n偏回帰係数:')
print(model.params.round(3))
print('\n各係数のp値:')
print(model.pvalues.round(4))''',
r'''print('決定係数 R^2      :', round(model.rsquared, 3))       # 当てはまりの良さ
print('自由度調整済み R^2:', round(model.rsquared_adj, 3))   # 変数の数を考慮した決定係数
print('\n偏回帰係数:')
print(model.params.round(3))               # 各変数の係数
print('\n各係数のp値:')
print(model.pvalues.round(4))              # 各係数が有意か（0.05未満で有意）'''),
(r'''new = pd.DataFrame({'英語':[70], '国語':[75], '勉強時間':[2.0]})
print('予測される数学の点数:', round(model.predict(new)[0], 1))''',
r'''new = pd.DataFrame({'英語':[70], '国語':[75], '勉強時間':[2.0]})  # 予測したい人の値
print('予測される数学の点数:', round(model.predict(new)[0], 1))   # モデルで予測'''),
(r'''model2 = smf.ols('数学 ~ 英語 + C(クラス)', data=df).fit()
print(model2.params.round(2))
print('→ [T.B],[T.C] は基準クラスAと比べた差を表す')''',
r'''model2 = smf.ols('数学 ~ 英語 + C(クラス)', data=df).fit()  # 質的変数クラスをダミー化して投入
print(model2.params.round(2))
print('→ [T.B],[T.C] は基準クラスAと比べた差を表す')'''),
(r'''from statsmodels.stats.outliers_influence import variance_inflation_factor
X = df[['英語', '国語', '勉強時間']].copy()
X['const'] = 1
vif = pd.Series(
    [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
    index=X.columns)
print(vif.round(2))
print('→ const以外が10未満なら多重共線性は問題なし')''',
r'''from statsmodels.stats.outliers_influence import variance_inflation_factor  # VIF計算
X = df[['英語', '国語', '勉強時間']].copy()  # 説明変数
X['const'] = 1                             # 切片用の列
# 各変数のVIF（分散拡大係数）を計算
vif = pd.Series(
    [variance_inflation_factor(X.values, i) for i in range(X.shape[1])],
    index=X.columns)
print(vif.round(2))
print('→ const以外が10未満なら多重共線性は問題なし')'''),
# 07
(r'''rng = np.random.default_rng(1)
pop = pd.DataFrame({'id': range(1, 1001),
                    '年代': rng.choice(['10代','20代','30代','40代'], 1000)})

# 単純無作為抽出
simple = pop.sample(n=40, random_state=1)
# 系統抽出（25人おき）
systematic = pop.iloc[rng.integers(0,25)::25]
# 層化抽出（各年代から10人ずつ）
strat = pop.groupby('年代', group_keys=False).sample(n=10, random_state=1)
print('単純無作為:', len(simple), '人')
print('系統抽出  :', len(systematic), '人')
print('層化抽出の年代構成:\n', strat['年代'].value_counts())''',
r'''rng = np.random.default_rng(1)             # 乱数生成器（seed固定）
# 1000人の母集団（idと年代）を作る
pop = pd.DataFrame({'id': range(1, 1001),
                    '年代': rng.choice(['10代','20代','30代','40代'], 1000)})

# 単純無作為抽出
simple = pop.sample(n=40, random_state=1)            # 完全ランダムに40人
# 系統抽出（25人おき）
systematic = pop.iloc[rng.integers(0,25)::25]        # 一定間隔で抽出
# 層化抽出（各年代から10人ずつ）
strat = pop.groupby('年代', group_keys=False).sample(n=10, random_state=1)  # 層ごとに抽出
print('単純無作為:', len(simple), '人')
print('系統抽出  :', len(systematic), '人')
print('層化抽出の年代構成:\n', strat['年代'].value_counts())'''),
(r'''normal_data = rng.normal(0, 1, 5000)
right_skew = rng.exponential(1, 5000)   # 右に裾が長い
for name, d in [('正規っぽい', normal_data), ('右に裾(指数)', right_skew)]:
    print(f'{name}: 歪度={stats.skew(d):.2f}, 尖度={stats.kurtosis(d):.2f}')

plt.hist(right_skew, bins=40); plt.title('右に裾が長い分布（歪度>0）'); plt.show()''',
r'''normal_data = rng.normal(0, 1, 5000)       # 左右対称な正規データ
right_skew = rng.exponential(1, 5000)   # 右に裾が長い
# それぞれの歪度（左右の非対称さ）と尖度（とがり具合）を計算
for name, d in [('正規っぽい', normal_data), ('右に裾(指数)', right_skew)]:
    print(f'{name}: 歪度={stats.skew(d):.2f}, 尖度={stats.kurtosis(d):.2f}')

plt.hist(right_skew, bins=40); plt.title('右に裾が長い分布（歪度>0）'); plt.show()'''),
(r'''def gini(x):
    x = np.sort(np.asarray(x, float))
    n = len(x)
    cum = np.cumsum(x) / x.sum()
    lorenz = np.insert(cum, 0, 0)
    pop = np.linspace(0, 1, n + 1)
    area = np.sum(np.diff(pop) * (lorenz[:-1] + lorenz[1:]) / 2)  # 台形則
    g = 1 - 2 * area
    return g, pop, lorenz

incomes = rng.lognormal(3, 0.6, 500)   # 所得（不平等あり）
g, popshare, lorenz = gini(incomes)
plt.plot(popshare, lorenz, label='ローレンツ曲線')
plt.plot([0,1],[0,1],'--', label='完全平等線')
plt.xlabel('累積人口比'); plt.ylabel('累積所得比')
plt.title(f'ジニ係数 = {g:.3f}'); plt.legend(); plt.show()''',
r'''# ジニ係数とローレンツ曲線を計算する関数
def gini(x):
    x = np.sort(np.asarray(x, float))      # 小さい順に並べる
    n = len(x)
    cum = np.cumsum(x) / x.sum()            # 累積所得の割合
    lorenz = np.insert(cum, 0, 0)           # 先頭に0を足す（ローレンツ曲線）
    pop = np.linspace(0, 1, n + 1)          # 累積人口の割合
    area = np.sum(np.diff(pop) * (lorenz[:-1] + lorenz[1:]) / 2)  # 台形則で曲線下の面積
    g = 1 - 2 * area                        # ジニ係数
    return g, pop, lorenz

incomes = rng.lognormal(3, 0.6, 500)   # 所得（不平等あり）
g, popshare, lorenz = gini(incomes)        # ジニ係数とローレンツ曲線を求める
plt.plot(popshare, lorenz, label='ローレンツ曲線')
plt.plot([0,1],[0,1],'--', label='完全平等線')  # 全員同じならこの直線
plt.xlabel('累積人口比'); plt.ylabel('累積所得比')
plt.title(f'ジニ係数 = {g:.3f}'); plt.legend(); plt.show()'''),
# === マーケ 01 ===
(r'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
btob = pd.read_csv('../data/sales_btob.csv')
print('商談数:', len(btob))
btob.head()''',
r'''import pandas as pd              # 表データ
import numpy as np               # 数値計算
import matplotlib.pyplot as plt  # グラフ描画
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
btob = pd.read_csv('../data/sales_btob.csv')      # 商談データを読み込む
print('商談数:', len(btob))      # 行数（商談件数）
btob.head()                      # 先頭5行を確認'''),
(r'''btob.info()
btob.describe(include='all')''',
r'''btob.info()                                # 各列の型・欠損の有無
btob.describe(include='all')               # 数値・文字すべての要約'''),
(r'''won = btob[btob['受注'] == 1]
print('受注率: {:.1%}'.format(btob['受注'].mean()))
print('受注件数:', len(won))
print('売上合計: {:,} 円'.format(won['商談金額'].sum()))
print('平均単価: {:,.0f} 円'.format(won['商談金額'].mean()))''',
r'''won = btob[btob['受注'] == 1]              # 受注（成約）した商談だけ抽出
print('受注率: {:.1%}'.format(btob['受注'].mean()))   # 受注=1の割合
print('受注件数:', len(won))                # 成約件数
print('売上合計: {:,} 円'.format(won['商談金額'].sum()))   # 受注金額の合計
print('平均単価: {:,.0f} 円'.format(won['商談金額'].mean()))  # 1件あたり平均'''),
(r'''by_ch = won.groupby('獲得チャネル')['商談金額'].sum().sort_values(ascending=False)
print(by_ch)
by_ch.plot(kind='bar', figsize=(7,4), title='チャネル別の受注売上')
plt.ylabel('売上(円)'); plt.xticks(rotation=0); plt.show()''',
r'''by_ch = won.groupby('獲得チャネル')['商談金額'].sum().sort_values(ascending=False)  # チャネル別の売上（多い順）
print(by_ch)
by_ch.plot(kind='bar', figsize=(7,4), title='チャネル別の受注売上')  # 棒グラフ
plt.ylabel('売上(円)'); plt.xticks(rotation=0); plt.show()'''),
(r'''ratio = (by_ch / by_ch.sum() * 100).round(1)
cum = ratio.cumsum()
pd.DataFrame({'売上構成比%': ratio, '累積%': cum})''',
r'''ratio = (by_ch / by_ch.sum() * 100).round(1)  # 各チャネルの売上構成比(%)
cum = ratio.cumsum()                          # 上から積み上げた累積(%)
pd.DataFrame({'売上構成比%': ratio, '累積%': cum})  # パレート分析の表'''),
(r'''won = won.copy()
won['受注月'] = pd.to_datetime(won['受注日']).dt.to_period('M').astype(str)
monthly = won.groupby('受注月')['商談金額'].sum()
monthly.plot(marker='o', figsize=(7,4), title='月別売上の推移')
plt.ylabel('売上(円)'); plt.grid(alpha=0.3); plt.show()
monthly''',
r'''won = won.copy()                           # コピーして警告を防ぐ
won['受注月'] = pd.to_datetime(won['受注日']).dt.to_period('M').astype(str)  # 受注日を「年月」に変換
monthly = won.groupby('受注月')['商談金額'].sum()  # 月ごとの売上合計
monthly.plot(marker='o', figsize=(7,4), title='月別売上の推移')  # 折れ線グラフ
plt.ylabel('売上(円)'); plt.grid(alpha=0.3); plt.show()
monthly'''),
# === マーケ 02 ===
(r'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False
mk = pd.read_csv('../data/web_marketing.csv')
mk.head()''',
r'''import pandas as pd              # 表データ
import numpy as np               # 数値計算
import matplotlib.pyplot as plt  # グラフ描画
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
mk = pd.read_csv('../data/web_marketing.csv')     # マーケ実績データを読み込む
mk.head()                        # 先頭5行を確認'''),
(r'''g = mk.groupby('チャネル')[['表示回数','クリック数','獲得数','費用']].sum()
g['CTR'] = (g['クリック数'] / g['表示回数'] * 100).round(2)
g['CVR'] = (g['獲得数'] / g['クリック数'] * 100).round(2)
g''',
r'''g = mk.groupby('チャネル')[['表示回数','クリック数','獲得数','費用']].sum()  # チャネル別に合計
g['CTR'] = (g['クリック数'] / g['表示回数'] * 100).round(2)  # クリック率＝クリック÷表示
g['CVR'] = (g['獲得数'] / g['クリック数'] * 100).round(2)    # 獲得率＝獲得÷クリック
g'''),
(r'''g['CPA'] = (g['費用'] / g['獲得数']).round(0)
g[['獲得数','費用','CPA']].sort_values('CPA')''',
r'''g['CPA'] = (g['費用'] / g['獲得数']).round(0)   # 獲得単価＝費用÷獲得数（低いほど効率的）
g[['獲得数','費用','CPA']].sort_values('CPA')   # CPAの低い順に表示'''),
(r'''g['CPA'].sort_values().plot(kind='barh', figsize=(7,4),
    title='チャネル別CPA（低いほど効率的）')
plt.xlabel('1件あたり獲得コスト(円)'); plt.show()''',
r'''g['CPA'].sort_values().plot(kind='barh', figsize=(7,4),   # CPAを横棒グラフに
    title='チャネル別CPA（低いほど効率的）')
plt.xlabel('1件あたり獲得コスト(円)'); plt.show()'''),
(r'''fig, ax = plt.subplots(figsize=(7,5))
ax.scatter(g['獲得数'], g['CPA'], s=g['費用']/300, alpha=0.5)
for name, row in g.iterrows():
    ax.annotate(name, (row['獲得数'], row['CPA']))
ax.set_xlabel('獲得数（量）'); ax.set_ylabel('CPA（コスト効率）')
ax.set_title('チャネルの量×効率マップ'); plt.show()''',
r'''fig, ax = plt.subplots(figsize=(7,5))                     # グラフ領域
ax.scatter(g['獲得数'], g['CPA'], s=g['費用']/300, alpha=0.5)  # バブルチャート（円の大きさ=費用）
# 各点にチャネル名を付ける
for name, row in g.iterrows():
    ax.annotate(name, (row['獲得数'], row['CPA']))
ax.set_xlabel('獲得数（量）'); ax.set_ylabel('CPA（コスト効率）')
ax.set_title('チャネルの量×効率マップ'); plt.show()'''),
(r'''# 課題2（ヒント）
ad = mk[mk['チャネル']=='Web広告'].copy()
ad['CPA'] = ad['費用'] / ad['獲得数']''',
r'''# 課題2（ヒント）
ad = mk[mk['チャネル']=='Web広告'].copy()   # Web広告の行だけ抽出
ad['CPA'] = ad['費用'] / ad['獲得数']        # 月ごとのCPAを計算'''),
# === マーケ 03 ===
(r'''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
plt.rcParams['axes.unicode_minus'] = False
ab = pd.read_csv('../data/ab_test.csv')
ab.head()''',
r'''import pandas as pd              # 表データ
import numpy as np               # 数値計算
import matplotlib.pyplot as plt  # グラフ描画
from scipy import stats          # 統計関数（検定など）
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
ab = pd.read_csv('../data/ab_test.csv')           # A/Bテストデータを読み込む
ab.head()                        # 先頭5行を確認'''),
(r'''summary = ab.groupby('グループ')['申込'].agg(['count','sum','mean'])
summary.columns = ['訪問数','申込数','申込率']
summary['申込率'] = (summary['申込率']*100).round(2)
summary''',
r'''summary = ab.groupby('グループ')['申込'].agg(['count','sum','mean'])  # 群ごとに件数・申込数・申込率
summary.columns = ['訪問数','申込数','申込率']   # 列名を分かりやすく
summary['申込率'] = (summary['申込率']*100).round(2)  # 割合を%に
summary'''),
(r'''summary['申込率'].plot(kind='bar', figsize=(5,4), title='ボタン色別の申込率(%)')
plt.ylabel('申込率(%)'); plt.xticks(rotation=0); plt.show()''',
r'''summary['申込率'].plot(kind='bar', figsize=(5,4), title='ボタン色別の申込率(%)')  # 群別の申込率を棒グラフに
plt.ylabel('申込率(%)'); plt.xticks(rotation=0); plt.show()'''),
(r'''table = pd.crosstab(ab['グループ'], ab['申込'])
print(table)
chi2, p, dof, exp = stats.chi2_contingency(table)
print(f'\nカイ二乗={chi2:.3f}, p値={p:.4f}')
if p < 0.05:
    print('→ 有意差あり！ ボタンの色で申込率は本当に変わる')
else:
    print('→ 有意差なし。偶然の範囲かもしれない')''',
r'''table = pd.crosstab(ab['グループ'], ab['申込'])   # グループ×申込のクロス表
print(table)
chi2, p, dof, exp = stats.chi2_contingency(table)  # カイ二乗検定（差が偶然か）
print(f'\nカイ二乗={chi2:.3f}, p値={p:.4f}')
if p < 0.05:
    print('→ 有意差あり！ ボタンの色で申込率は本当に変わる')
else:
    print('→ 有意差なし。偶然の範囲かもしれない')'''),
(r'''rate_a = summary.loc['A_青ボタン','申込率'] / 100
rate_b = summary.loc['B_緑ボタン','申込率'] / 100
lift = (rate_b - rate_a) / rate_a * 100
print(f'改善率（リフト）: {lift:+.1f}%')

# 月10万訪問・1申込5000円の価値と仮定したら？
monthly_visits = 100000
value_per = 5000
gain = monthly_visits * (rate_b - rate_a) * value_per
print(f'Bに変えると月あたり約 {gain:,.0f} 円の増加見込み')''',
r'''rate_a = summary.loc['A_青ボタン','申込率'] / 100   # Aの申込率（割合に戻す）
rate_b = summary.loc['B_緑ボタン','申込率'] / 100   # Bの申込率
lift = (rate_b - rate_a) / rate_a * 100             # 改善率（リフト）
print(f'改善率（リフト）: {lift:+.1f}%')

# 月10万訪問・1申込5000円の価値と仮定したら？
monthly_visits = 100000                    # 月間訪問数
value_per = 5000                           # 1申込の価値
gain = monthly_visits * (rate_b - rate_a) * value_per   # 増加見込み額
print(f'Bに変えると月あたり約 {gain:,.0f} 円の増加見込み')'''),
(r'''# 課題4（ヒント）
from statsmodels.stats.proportion import proportions_ztest''',
r'''# 課題4（ヒント）
from statsmodels.stats.proportion import proportions_ztest  # 母比率の差の検定'''),
]

MAP = {k.strip(): v for k, v in PAIRS}
replaced = 0; unmatched = []
for folder in ["04_統計_2級","05_実践_BtoBマーケ"]:
    for p in sorted(glob.glob(f"{ROOT}/{folder}/*.ipynb")):
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
