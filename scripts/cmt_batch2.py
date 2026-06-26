# -*- coding: utf-8 -*-
import json, glob, os
ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"

MAP = {
# 共通import（4級 01,02,03）
'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 日本語が文字化けするときは次の1行を有効にしてください
# plt.rcParams['font.family'] = 'Hiragino Sans'  # Macの場合
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../data/students_scores.csv')
df.head()''':
'''import numpy as np               # 数値計算
import pandas as pd              # 表データ
import matplotlib.pyplot as plt  # グラフ描画

# 日本語が文字化けするときは次の1行を有効にしてください
# plt.rcParams['font.family'] = 'Hiragino Sans'  # Macの場合
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ
df = pd.read_csv('../data/students_scores.csv')   # 生徒データを読み込む
df.head()                        # 先頭5行を確認''',

# import（4級04: 3行のみ）
'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt''':
'''import numpy as np               # 数値計算
import pandas as pd              # 表データ
import matplotlib.pyplot as plt  # グラフ描画''',

# import（4級05,06: 3行+rcParams）
'''import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['axes.unicode_minus'] = False''':
'''import numpy as np               # 数値計算
import pandas as pd              # 表データ
import matplotlib.pyplot as plt  # グラフ描画
plt.rcParams['axes.unicode_minus'] = False       # マイナス記号の文字化けを防ぐ''',

# 01
'df.dtypes':
'df.dtypes   # 各列のデータ型（数値か文字列か）を確認',

'''bins = [0, 20, 40, 60, 80, 100]
labels = ['0-19', '20-39', '40-59', '60-79', '80-100']
df['階級'] = pd.cut(df['数学'], bins=bins, right=False, labels=labels)
freq = df['階級'].value_counts().sort_index()
table = pd.DataFrame({'度数': freq})
table['相対度数'] = (table['度数'] / table['度数'].sum()).round(3)
table['累積度数'] = table['度数'].cumsum()
table''':
'''bins = [0, 20, 40, 60, 80, 100]                        # 階級の境目
labels = ['0-19', '20-39', '40-59', '60-79', '80-100']  # 各階級の名前
df['階級'] = pd.cut(df['数学'], bins=bins, right=False, labels=labels)  # 数学の点を階級に振り分け
freq = df['階級'].value_counts().sort_index()          # 階級ごとの人数（度数）
table = pd.DataFrame({'度数': freq})                   # 度数を表にする
table['相対度数'] = (table['度数'] / table['度数'].sum()).round(3)  # 全体に対する割合
table['累積度数'] = table['度数'].cumsum()             # 下から積み上げた合計
table''',

'''plt.figure(figsize=(7, 4))
plt.hist(df['数学'], bins=bins, edgecolor='white')
plt.xlabel('数学の点数')
plt.ylabel('人数')
plt.title('数学の点数の分布')
plt.show()''':
'''plt.figure(figsize=(7, 4))                  # グラフの大きさを指定
plt.hist(df['数学'], bins=bins, edgecolor='white')  # ヒストグラム（階級ごとの人数）
plt.xlabel('数学の点数')                    # x軸ラベル
plt.ylabel('人数')                          # y軸ラベル
plt.title('数学の点数の分布')               # タイトル
plt.show()                                  # 表示''',

# 02
'''math = df['数学']
print('平均値:', math.mean().round(2))
print('中央値:', math.median())
print('最頻値:', math.mode().tolist())''':
'''math = df['数学']                          # 数学の列を取り出す
print('平均値:', math.mean().round(2))     # 平均値
print('中央値:', math.median())            # 中央値（真ん中の値）
print('最頻値:', math.mode().tolist())     # 最頻値（最も多い値）''',

'''incomes = [300, 320, 350, 310, 330, 9000]  # 万円。最後の1人だけ大金持ち
print('平均:', np.mean(incomes))    # 1601.7万 … 実感と合わない
print('中央値:', np.median(incomes)) # 325万 … こちらが実感に近い''':
'''incomes = [300, 320, 350, 310, 330, 9000]  # 万円。最後の1人だけ大金持ち
print('平均:', np.mean(incomes))    # 1601.7万 … 1人に引っ張られ実感と合わない
print('中央値:', np.median(incomes)) # 325万 … こちらが実感に近い''',

'''df.groupby('クラス')['数学'].mean().round(1)''':
'''df.groupby('クラス')['数学'].mean().round(1)   # クラスごとの数学の平均''',

'''plt.figure(figsize=(6, 4))
df.groupby('クラス')['数学'].mean().plot(kind='bar')
plt.ylabel('数学の平均点')
plt.title('クラス別の平均点')
plt.xticks(rotation=0)
plt.show()''':
'''plt.figure(figsize=(6, 4))                        # グラフの大きさ
df.groupby('クラス')['数学'].mean().plot(kind='bar')  # クラス別平均を棒グラフに
plt.ylabel('数学の平均点')                        # y軸ラベル
plt.title('クラス別の平均点')                     # タイトル
plt.xticks(rotation=0)                            # x軸目盛りを水平に
plt.show()''',

# 03
'''math = df['数学']
print('最大:', math.max(), '最小:', math.min())
print('範囲:', math.max() - math.min())''':
'''math = df['数学']                          # 数学の列
print('最大:', math.max(), '最小:', math.min())  # 最大値と最小値
print('範囲:', math.max() - math.min())    # 範囲 ＝ 最大 − 最小''',

'''q1 = math.quantile(0.25)
q2 = math.quantile(0.50)
q3 = math.quantile(0.75)
print('Q1:', q1, ' Q2(中央値):', q2, ' Q3:', q3)
print('IQR:', q3 - q1)

# describe() で一気に確認できる
math.describe()''':
'''q1 = math.quantile(0.25)   # 第1四分位数（下から25%の位置）
q2 = math.quantile(0.50)   # 第2四分位数（＝中央値）
q3 = math.quantile(0.75)   # 第3四分位数（下から75%の位置）
print('Q1:', q1, ' Q2(中央値):', q2, ' Q3:', q3)
print('IQR:', q3 - q1)     # 四分位範囲 ＝ Q3 − Q1

# describe() で一気に確認できる
math.describe()            # 件数・平均・四分位などをまとめて表示''',

'''plt.figure(figsize=(7, 4))
df.boxplot(column='数学', by='クラス')
plt.title('クラス別 数学の点数')
plt.suptitle('')
plt.ylabel('点数')
plt.show()''':
'''plt.figure(figsize=(7, 4))                 # グラフの大きさ
df.boxplot(column='数学', by='クラス')      # クラス別に箱ひげ図
plt.title('クラス別 数学の点数')            # タイトル
plt.suptitle('')                           # 自動で付く上の見出しを消す
plt.ylabel('点数')                         # y軸ラベル
plt.show()''',

'''iqr = q3 - q1
low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr
print(f'外れ値の境界: {low:.1f} 未満 または {high:.1f} 超')
df[(df['数学'] < low) | (df['数学'] > high)][['生徒ID', '数学']]''':
'''iqr = q3 - q1                              # 四分位範囲
low = q1 - 1.5 * iqr                       # 外れ値とみなす下限
high = q3 + 1.5 * iqr                      # 外れ値とみなす上限
print(f'外れ値の境界: {low:.1f} 未満 または {high:.1f} 超')
df[(df['数学'] < low) | (df['数学'] > high)][['生徒ID', '数学']]  # 範囲外の生徒を抽出''',

# 04
'''# サイコロを10000回ふって、偶数の割合を確かめる
rng = np.random.default_rng(0)
rolls = rng.integers(1, 7, size=10000)
even = np.sum(rolls % 2 == 0)
print('偶数の割合:', even / 10000)  # 0.5 に近づく（大数の法則）''':
'''# サイコロを10000回ふって、偶数の割合を確かめる
rng = np.random.default_rng(0)             # 乱数生成器（seedで固定）
rolls = rng.integers(1, 7, size=10000)     # 1〜6を10000回
even = np.sum(rolls % 2 == 0)              # 偶数（2で割り切れる）の回数
print('偶数の割合:', even / 10000)  # 0.5 に近づく（大数の法則）''',

'''df = pd.read_csv('../data/students_scores.csv')
df['合否'] = np.where(df['数学'] >= 60, '合格', '不合格')
cross = pd.crosstab(df['クラス'], df['合否'])
cross''':
'''df = pd.read_csv('../data/students_scores.csv')  # データ読み込み
df['合否'] = np.where(df['数学'] >= 60, '合格', '不合格')  # 60点以上で合否を判定
cross = pd.crosstab(df['クラス'], df['合否'])    # クラス×合否のクロス集計
cross''',

'''pd.crosstab(df['クラス'], df['合否'], normalize='index').round(2)''':
'''pd.crosstab(df['クラス'], df['合否'], normalize='index').round(2)  # 行(クラス)ごとの割合にする''',

'''values = np.array([1000, 0])
probs = np.array([0.1, 0.9])
print('期待値:', np.sum(values * probs), '円')  # 100円
print('→ 参加費が100円より高ければ損なくじ')''':
'''values = np.array([1000, 0])               # 当たり1000円・はずれ0円
probs = np.array([0.1, 0.9])               # それぞれの確率
print('期待値:', np.sum(values * probs), '円')  # Σ(値×確率) ＝ 100円
print('→ 参加費が100円より高ければ損なくじ')''',

'''# 問2
btob = pd.read_csv('../data/sales_btob.csv')''':
'''# 問2
btob = pd.read_csv('../data/sales_btob.csv')   # 商談データを読み込む''',

# 05
'''kyoka = pd.Series({'数学':8,'英語':12,'国語':10,'理科':6,'社会':4}, name='人数')

fig, ax = plt.subplots(1, 3, figsize=(13,4))
kyoka.plot(kind='bar', ax=ax[0], title='棒：好きな教科の人数')
ax[0].tick_params(axis='x', rotation=0)
pd.Series([22,24,28,30,27,25],
          index=['1月','2月','3月','4月','5月','6月']).plot(
          marker='o', ax=ax[1], title='折れ線：気温の変化')
kyoka.plot(kind='pie', ax=ax[2], autopct='%1.0f%%', title='円：割合')
ax[2].set_ylabel('')
plt.tight_layout(); plt.show()''':
'''kyoka = pd.Series({'数学':8,'英語':12,'国語':10,'理科':6,'社会':4}, name='人数')  # 教科ごとの人数

fig, ax = plt.subplots(1, 3, figsize=(13,4))   # 1行3列のグラフ領域
kyoka.plot(kind='bar', ax=ax[0], title='棒：好きな教科の人数')   # 左：棒グラフ
ax[0].tick_params(axis='x', rotation=0)        # x軸ラベルを水平に
# 中：折れ線（月ごとの気温）
pd.Series([22,24,28,30,27,25],
          index=['1月','2月','3月','4月','5月','6月']).plot(
          marker='o', ax=ax[1], title='折れ線：気温の変化')
kyoka.plot(kind='pie', ax=ax[2], autopct='%1.0f%%', title='円：割合')  # 右：円グラフ
ax[2].set_ylabel('')                           # 円グラフのy軸ラベルを消す
plt.tight_layout(); plt.show()                 # レイアウトを整えて表示''',

'''df_taikei = pd.DataFrame({
    '2020年':[40,35,25], '2026年':[55,30,15]
}, index=['スマホ','PC','その他']).T
ratio = df_taikei.div(df_taikei.sum(axis=1), axis=0) * 100
ratio.plot(kind='barh', stacked=True, figsize=(8,3),
           title='帯グラフ：利用端末の割合の変化(%)')
plt.xlabel('％'); plt.show()''':
'''# 端末利用の構成比（2年分）を作る
df_taikei = pd.DataFrame({
    '2020年':[40,35,25], '2026年':[55,30,15]
}, index=['スマホ','PC','その他']).T
ratio = df_taikei.div(df_taikei.sum(axis=1), axis=0) * 100  # 各年で合計100%に変換
ratio.plot(kind='barh', stacked=True, figsize=(8,3),       # 横向き積み上げ＝帯グラフ
           title='帯グラフ：利用端末の割合の変化(%)')
plt.xlabel('％'); plt.show()''',

'''claims = pd.Series({'配送遅延':52,'破損':28,'数量違い':12,'その他':8})
claims = claims.sort_values(ascending=False)
cum = claims.cumsum() / claims.sum() * 100

fig, ax1 = plt.subplots(figsize=(7,4))
ax1.bar(claims.index, claims.values)
ax2 = ax1.twinx()
ax2.plot(claims.index, cum.values, color='red', marker='o')
ax2.set_ylim(0,110); ax2.set_ylabel('累積％')
ax1.set_ylabel('件数'); plt.title('パレート図：クレームの内訳')
plt.show()
print('上位2項目で全体の', round(cum.iloc[1],1), '%')''':
'''claims = pd.Series({'配送遅延':52,'破損':28,'数量違い':12,'その他':8})  # クレーム件数
claims = claims.sort_values(ascending=False)   # 多い順に並べ替え
cum = claims.cumsum() / claims.sum() * 100     # 累積の割合(%)

fig, ax1 = plt.subplots(figsize=(7,4))         # グラフ領域
ax1.bar(claims.index, claims.values)           # 棒：件数
ax2 = ax1.twinx()                              # 右側にもう1つy軸を追加
ax2.plot(claims.index, cum.values, color='red', marker='o')  # 折れ線：累積割合
ax2.set_ylim(0,110); ax2.set_ylabel('累積％')
ax1.set_ylabel('件数'); plt.title('パレート図：クレームの内訳')
plt.show()
print('上位2項目で全体の', round(cum.iloc[1],1), '%')''',

'''def stem_leaf(data):
    data = sorted(data)
    stems = {}
    for v in data:
        stems.setdefault(v // 10, []).append(v % 10)
    for s in range(min(stems), max(stems) + 1):
        leaves = ''.join(str(x) for x in stems.get(s, []))
        print(f'{s} | {leaves}')

scores = [62,65,67,71,73,73,78,81,82,85,88,90,52,59]
stem_leaf(scores)
print('読み方: 7|1338 は 71,73,73,78 点の4人')''':
'''# 幹葉図を作る関数：十の位を「幹」、一の位を「葉」として並べる
def stem_leaf(data):
    data = sorted(data)                        # 小さい順に並べる
    stems = {}                                 # 幹ごとに葉を貯める入れ物
    for v in data:
        stems.setdefault(v // 10, []).append(v % 10)  # 十の位で分け、一の位を葉に追加
    for s in range(min(stems), max(stems) + 1):       # 幹を小さい順に
        leaves = ''.join(str(x) for x in stems.get(s, []))  # 葉を並べた文字列
        print(f'{s} | {leaves}')               # 「幹 | 葉」で表示

scores = [62,65,67,71,73,73,78,81,82,85,88,90,52,59]  # 点数データ
stem_leaf(scores)                              # 幹葉図を表示
print('読み方: 7|1338 は 71,73,73,78 点の4人')''',

'''# 問2
import pandas as pd
df = pd.read_csv('../data/students_scores.csv')''':
'''# 問2
import pandas as pd                            # pandasを読み込む
df = pd.read_csv('../data/students_scores.csv')  # データを読み込む''',

# 06
'''sales = pd.Series([100, 110, 121, 115, 130, 143],
    index=['1月','2月','3月','4月','5月','6月'], name='売上')
sales''':
'''sales = pd.Series([100, 110, 121, 115, 130, 143],  # 月別売上（万円）
    index=['1月','2月','3月','4月','5月','6月'], name='売上')
sales                                          # 中身を表示''',

'''growth = sales.pct_change() * 100
print(growth.round(1))
print('→ 2月は前月比 +10%、4月はマイナス')''':
'''growth = sales.pct_change() * 100              # 前の月からの変化率(%)
print(growth.round(1))
print('→ 2月は前月比 +10%、4月はマイナス')''',

'''index = sales / sales['1月'] * 100
print(index.round(1))
print('→ 6月は1月の143（=43%増）')''':
'''index = sales / sales['1月'] * 100             # 1月を100としたときの指数
print(index.round(1))
print('→ 6月は1月の143（=43%増）')''',

'''ma3 = sales.rolling(window=3).mean()
print(ma3.round(1))

sales.plot(marker='o', label='売上')
ma3.plot(marker='s', label='3か月移動平均')
plt.legend(); plt.title('売上と移動平均'); plt.show()''':
'''ma3 = sales.rolling(window=3).mean()           # 3か月ごとの移動平均（でこぼこをならす）
print(ma3.round(1))

sales.plot(marker='o', label='売上')           # 元の売上
ma3.plot(marker='s', label='3か月移動平均')     # 移動平均
plt.legend(); plt.title('売上と移動平均'); plt.show()''',

'''import itertools
# コイン2回の全パターンを列挙
outcomes = list(itertools.product(['表','裏'], repeat=2))
for o in outcomes:
    print(o)
print('全', len(outcomes), '通り')''':
'''import itertools                               # 組み合わせ・順列の便利ツール
# コイン2回の全パターンを列挙
outcomes = list(itertools.product(['表','裏'], repeat=2))  # 表/裏 を2回ぶん全組合せ
for o in outcomes:
    print(o)                                   # 1パターンずつ表示
print('全', len(outcomes), '通り')             # 総数''',

'''rng = np.random.default_rng(0)
trials = rng.integers(0, 2, size=(10000, 2))   # 0=表,1=表… 2回
both_head = np.sum(np.all(trials == 0, axis=1))
print('実験での割合:', both_head / 10000, ' (理論 0.25)')''':
'''rng = np.random.default_rng(0)                 # 乱数生成器（seedで固定）
trials = rng.integers(0, 2, size=(10000, 2))   # 0=表,1=裏 を 2回×10000セット
both_head = np.sum(np.all(trials == 0, axis=1))  # 2回とも0(表)だったセット数
print('実験での割合:', both_head / 10000, ' (理論 0.25)')''',

'''# 問2
w = pd.read_csv('../data/weather.csv')''':
'''# 問2
w = pd.read_csv('../data/weather.csv')         # 天気データを読み込む''',
}

MAP = {k.strip(): v for k, v in MAP.items()}
replaced = 0; unmatched = []
for p in sorted(glob.glob(f"{ROOT}/02_統計_4級/*.ipynb")):
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
print("replaced:", replaced)
print("unmatched runnable:", len(unmatched))
for u in unmatched: print("  ", u)
