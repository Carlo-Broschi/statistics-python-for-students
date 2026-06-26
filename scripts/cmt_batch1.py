# -*- coding: utf-8 -*-
import json, glob, os

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"

# 共通データ準備セル（コメント付き版）。署名で検出して全ノート一括置換。
DATA_SETUP_NEW = '''# === ① セットアップ（最初に実行してください）===============================
# Colabなどデータが無い環境では、教材と同一の合成データを自動生成します。
# ローカル/Codespacesで data/ がある場合は何もしません（再現性のため乱数seedは固定）。
import os
if not os.path.exists('../data/students_scores.csv'):   # データが無い環境（Colab等）か判定
    os.makedirs('/content/nb', exist_ok=True); os.chdir('/content/nb')  # ../data を使えるよう作業場所を作る
    os.makedirs('../data', exist_ok=True)               # データ保存先フォルダを作る
    import numpy as np, pandas as pd                     # 数値計算と表データのライブラリ
    D = '../data'; rng = np.random.default_rng(42)       # 保存先と、結果を固定する乱数生成器
    # --- 生徒120人の成績データを作る ---
    n = 120; cls = rng.choice(['A','B','C'], n)          # 人数とクラス
    math = np.clip(rng.normal(65,15,n),0,100).round().astype(int)        # 数学（0〜100点）
    eng = np.clip(0.6*math+rng.normal(28,10,n),0,100).round().astype(int) # 英語（数学と相関）
    jp = np.clip(rng.normal(70,12,n),0,100).round().astype(int)          # 国語
    hrs = np.clip(rng.normal(1.5,0.8,n)+math/100,0,None).round(1)        # 勉強時間
    pd.DataFrame({'生徒ID':[f'S{i:03d}' for i in range(1,n+1)],'クラス':cls,
        '数学':math,'英語':eng,'国語':jp,'勉強時間':hrs}).to_csv(f'{D}/students_scores.csv',index=False,encoding='utf-8-sig')
    # --- 30日間の天気データ ---
    days = pd.date_range('2026-06-01', periods=30)       # 6月の30日分の日付
    temp = (24+4*np.sin(np.arange(30)/5)+rng.normal(0,2,30)).round(1)    # 気温
    rain = np.clip(rng.gamma(1.2,4,30)*(rng.random(30)<0.4),0,None).round(1)  # 降水量
    pd.DataFrame({'日付':days.strftime('%Y-%m-%d'),'気温':temp,'降水量':rain}).to_csv(f'{D}/weather.csv',index=False,encoding='utf-8-sig')
    # --- BtoB商談400件 ---
    m = 400; inds = rng.choice(['製造','IT','小売','医療','金融','建設'],m,p=[.25,.2,.18,.12,.15,.1])  # 業界
    chs = ['展示会','Web広告','メルマガ','紹介','テレアポ']; ch = rng.choice(chs,m,p=[.2,.3,.2,.15,.15])  # 獲得チャネル
    deal = (rng.lognormal(13,0.7,m)).round(-3).astype(int)   # 商談金額
    wr = {'展示会':.35,'Web広告':.18,'メルマガ':.12,'紹介':.45,'テレアポ':.15}  # チャネル別の受注率
    won = np.array([rng.random()<wr[c] for c in ch])         # 受注したか（チャネルで確率を変える）
    dt = pd.to_datetime('2026-01-01')+pd.to_timedelta(rng.integers(0,180,m),unit='D')  # 受注日
    pd.DataFrame({'商談ID':[f'D{i:04d}' for i in range(1,m+1)],'受注日':dt.strftime('%Y-%m-%d'),
        '業界':inds,'獲得チャネル':ch,'商談金額':deal,'担当者':rng.choice(['田中','鈴木','佐藤','高橋'],m),
        '受注':won.astype(int)}).to_csv(f'{D}/sales_btob.csv',index=False,encoding='utf-8-sig')
    # --- 月×チャネルのマーケ実績 ---
    months = pd.date_range('2026-01-01',periods=6,freq='MS').strftime('%Y-%m')  # 6か月分
    base = {'展示会':2000,'Web広告':12000,'メルマガ':6000,'紹介':800,'テレアポ':1500}  # 表示回数の目安
    ctr = {'展示会':.08,'Web広告':.03,'メルマガ':.05,'紹介':.2,'テレアポ':.12}   # クリック率
    cvr = {'展示会':.12,'Web広告':.04,'メルマガ':.06,'紹介':.25,'テレアポ':.09}   # 獲得率
    cpc = {'展示会':30,'Web広告':80,'メルマガ':5,'紹介':0,'テレアポ':200}        # クリック単価
    rows = []
    for mo in months:                                    # 月ごと
        for c in chs:                                    # チャネルごとに実績を作る
            imp = int(base[c]*rng.uniform(0.8,1.3)); clk = int(imp*ctr[c]*rng.uniform(0.8,1.2))
            cv = int(clk*cvr[c]*rng.uniform(0.7,1.3)); cost = int(clk*cpc[c]*rng.uniform(0.9,1.1))
            rows.append([mo,c,imp,clk,cv,cost])
    pd.DataFrame(rows,columns=['月','チャネル','表示回数','クリック数','獲得数','費用']).to_csv(f'{D}/web_marketing.csv',index=False,encoding='utf-8-sig')
    # --- A/Bテストの申込ログ ---
    ab = []
    for grp,p,size in [('A_青ボタン',0.082,2400),('B_緑ボタン',0.104,2380)]:  # 2群の申込率と人数
        for c in (rng.random(size)<p): ab.append([grp,int(c)])   # 各訪問が申込んだか
    pd.DataFrame(ab,columns=['グループ','申込']).sample(frac=1,random_state=1).reset_index(drop=True).to_csv(f'{D}/ab_test.csv',index=False,encoding='utf-8-sig')
    print('✅ 合成データを生成しました（Colab環境）')
else:
    print('✅ data/ を検出しました（ローカル/Codespaces）')'''

# 旧→新（キーは旧ソースを strip したもの）
MAP = {
'print("こんにちは、Python！")':
'print("こんにちは、Python！")  # 文字を画面に表示する',

'3 + 4':
'3 + 4  # セルの最後の式の値は自動で表示される（ここでは 7）',

'print("とじカッコを忘れた"':
'print("とじカッコを忘れた"  # わざとエラー：閉じカッコ ) を忘れている',

# --- 02 ---
'''name = "山田はなこ"
age = 15
height = 158.5
print(name, age, height)''':
'''name = "山田はなこ"   # 文字列を変数 name に入れる
age = 15              # 整数を age に入れる
height = 158.5        # 小数を height に入れる
print(name, age, height)  # 3つの変数の中身をまとめて表示''',

'''age = age + 1   # 1歳ふえた
print(age)''':
'''age = age + 1   # 今の age に1を足して入れ直す（1歳ふえた）
print(age)      # 更新後の age を表示''',

'''print(type(15))
print(type(158.5))
print(type("はなこ"))
print(type(True))''':
'''print(type(15))        # 整数の型を調べる → int
print(type(158.5))     # 小数の型 → float
print(type("はなこ"))   # 文字列の型 → str
print(type(True))      # 真偽値の型 → bool''',

'''moji = "100"
print(moji + moji)        # 文字列の足し算は連結 → 100100
print(int(moji) + 50)     # 数にすれば計算できる → 150''':
'''moji = "100"              # 見た目は数字だが、これは文字列
print(moji + moji)        # 文字列の + は連結 → 100100
print(int(moji) + 50)     # int()で数に変換してから計算 → 150''',

'''name = "はなこ"
age = 15
print(f"{name}さんは{age}歳です。来年は{age + 1}歳。")''':
'''name = "はなこ"   # 名前
age = 15          # 年齢
print(f"{name}さんは{age}歳です。来年は{age + 1}歳。")  # f-stringで変数を文に埋め込む''',

'''s = "Python"
print(len(s))        # 文字数 → 6
print(s.upper())     # 大文字 → PYTHON
print(s * 3)         # くり返し → PythonPythonPython
print(s[0])          # 先頭の文字 → P''':
'''s = "Python"         # 文字列を変数 s に入れる
print(len(s))        # 文字数 → 6
print(s.upper())     # 大文字に変換 → PYTHON
print(s * 3)         # 文字列をくり返す → PythonPythonPython
print(s[0])          # 先頭の1文字を取り出す → P''',

# --- 03 ---
'''scores = [60, 75, 90, 55, 80]
print(scores)
print(scores[0])     # 1番目（番号は0から！）
print(scores[-1])    # 最後
print(len(scores))   # 個数''':
'''scores = [60, 75, 90, 55, 80]  # 数をならべたリストを作る
print(scores)        # リスト全体を表示
print(scores[0])     # 1番目の要素（番号は0から！）
print(scores[-1])    # 最後の要素
print(len(scores))   # 要素の個数''',

'''print(sum(scores))            # 合計
print(max(scores))            # 最大
print(min(scores))            # 最小
print(sum(scores) / len(scores))  # 平均''':
'''print(sum(scores))            # 合計
print(max(scores))            # 最大値
print(min(scores))            # 最小値
print(sum(scores) / len(scores))  # 合計÷個数 ＝ 平均''',

'''scores.append(100)   # 末尾に追加
print(scores)
scores.sort()        # 小さい順に並べ替え
print(scores)''':
'''scores.append(100)   # リストの末尾に100を追加
print(scores)        # 追加後を表示
scores.sort()        # 小さい順に並べ替え
print(scores)        # 並べ替え後を表示''',

'''student = {"名前": "はなこ", "数学": 90, "英語": 75}
print(student["名前"])
print(student["数学"])''':
'''student = {"名前": "はなこ", "数学": 90, "英語": 75}  # キーと値の辞書を作る
print(student["名前"])   # キー"名前"の値を取り出す
print(student["数学"])   # キー"数学"の値を取り出す''',

'''for s in scores:
    print(s, '点')''':
'''# リストの要素を1つずつ取り出してくり返す
for s in scores:
    print(s, '点')   # 取り出した値を表示''',

'''for i in range(5):    # 0,1,2,3,4
    print(i, 'かいめ')''':
'''# range(5) で 0〜4 の5回くり返す
for i in range(5):
    print(i, 'かいめ')   # 今の回数を表示''',

'''scores = [60, 75, 90, 55, 80, 100, 45]
count = 0
for s in scores:
    if s >= 60:
        count = count + 1
print('合格者は', count, '人')''':
'''scores = [60, 75, 90, 55, 80, 100, 45]  # 点数のリスト
count = 0                # 合格者を数えるカウンター（最初は0）
# 各点数を見て、60以上なら数える
for s in scores:
    if s >= 60:          # 60点以上か判定
        count = count + 1  # 条件を満たせば1増やす
print('合格者は', count, '人')  # 数えた結果を表示''',

# --- 04 ---
'''score = 72
if score >= 80:
    print('すごい！')
elif score >= 60:
    print('合格')
else:
    print('もう少し')''':
'''score = 72             # 点数
# 点数によって表示を変える（場合分け）
if score >= 80:
    print('すごい！')    # 80以上のとき
elif score >= 60:
    print('合格')        # 60以上80未満のとき
else:
    print('もう少し')    # それ未満のとき''',

'''temp = 28
if temp >= 25 and temp < 30:
    print('夏日です')''':
'''temp = 28              # 気温
# 25以上 かつ 30未満 なら「夏日」
if temp >= 25 and temp < 30:
    print('夏日です')''',

'''def greet(name):
    return f'こんにちは、{name}さん！'

print(greet('はなこ'))
print(greet('たろう'))''':
'''# 名前を受け取ってあいさつ文を返す関数を定義
def greet(name):
    return f'こんにちは、{name}さん！'

print(greet('はなこ'))   # 関数を呼び出して結果を表示
print(greet('たろう'))''',

'''def average(numbers):
    return sum(numbers) / len(numbers)

print(average([60, 70, 80]))
print(average([100, 90]))''':
'''# 数のリストを受け取って平均を返す関数
def average(numbers):
    return sum(numbers) / len(numbers)   # 合計÷個数

print(average([60, 70, 80]))   # → 70.0
print(average([100, 90]))      # → 95.0''',

'''import math
print(math.sqrt(144))   # 平方根 → 12.0
print(math.pi)          # 円周率

import random
print(random.randint(1, 6))  # サイコロ（1〜6のランダム）''':
'''import math               # 数学の便利機能を読み込む
print(math.sqrt(144))     # 平方根 → 12.0
print(math.pi)            # 円周率

import random             # 乱数の機能を読み込む
print(random.randint(1, 6))  # 1〜6のランダムな整数（サイコロ）''',

# --- 05 NumPy ---
'''# ふつうのリストでは * 2 が「くり返し」になってしまう
prices = [100, 200, 300]
print(prices * 2)        # [100,200,300,100,200,300] … 望んだ結果じゃない

import numpy as np
arr = np.array([100, 200, 300])
print(arr * 2)           # [200 400 600] … 全部を2倍！
print(arr + 50)          # [150 250 350] … 全部に+50''':
'''# ふつうのリストでは * 2 が「くり返し」になってしまう
prices = [100, 200, 300]   # ふつうのリスト
print(prices * 2)        # [100,200,300,100,200,300] … 望んだ結果じゃない

import numpy as np        # NumPyを np という名前で読み込む
arr = np.array([100, 200, 300])  # リストをNumPyの配列に変換
print(arr * 2)           # [200 400 600] … 全要素を2倍！
print(arr + 50)          # [150 250 350] … 全要素に+50''',

'''print(np.array([1, 2, 3, 4]))      # リストから
print(np.arange(0, 10, 2))         # 0から10未満を2とび → [0 2 4 6 8]
print(np.linspace(0, 1, 5))        # 0〜1を5等分 → [0. .25 .5 .75 1.]
print(np.zeros(3), np.ones(3))     # ゼロ/イチで埋める''':
'''print(np.array([1, 2, 3, 4]))      # リストから配列を作る
print(np.arange(0, 10, 2))         # 0から10未満を2とび → [0 2 4 6 8]
print(np.linspace(0, 1, 5))        # 0〜1を5等分 → [0. .25 .5 .75 1.]
print(np.zeros(3), np.ones(3))     # 0で埋めた配列 / 1で埋めた配列''',

'''scores = np.array([60, 75, 90, 55, 80, 100, 45])
print('合計  :', scores.sum())
print('平均  :', scores.mean())
print('最大  :', scores.max(), ' 最小:', scores.min())
print('標準偏差:', scores.std().round(2))
print('√144  :', np.sqrt(144))''':
'''scores = np.array([60, 75, 90, 55, 80, 100, 45])  # 点数の配列
print('合計  :', scores.sum())     # 合計
print('平均  :', scores.mean())    # 平均
print('最大  :', scores.max(), ' 最小:', scores.min())  # 最大と最小
print('標準偏差:', scores.std().round(2))  # 標準偏差（小数2桁に丸め）
print('√144  :', np.sqrt(144))     # 平方根''',

'''print(scores >= 60)              # 各要素がTrue/False
print(scores[scores >= 60])     # Trueの要素だけ取り出す
print('60点以上の人数:', (scores >= 60).sum())   # Trueの数を数える
print('60点以上の平均:', scores[scores >= 60].mean().round(1))''':
'''print(scores >= 60)              # 各要素が60以上か（True/False）
print(scores[scores >= 60])     # Trueの要素だけ取り出す
print('60点以上の人数:', (scores >= 60).sum())   # Trueの数を数える
print('60点以上の平均:', scores[scores >= 60].mean().round(1))  # 60以上だけの平均''',

'''result = np.where(scores >= 60, '合格', '不合格')
print(result)''':
'''# 条件がTrueなら'合格'、Falseなら'不合格'を割り当てる
result = np.where(scores >= 60, '合格', '不合格')
print(result)''',

'''rng = np.random.default_rng(0)
print('サイコロ10回:', rng.integers(1, 7, size=10))
print('正規分布から5個:', rng.normal(50, 10, size=5).round(1))
print('くじ引き:', rng.choice(['当たり', 'はずれ'], size=5))''':
'''rng = np.random.default_rng(0)   # 乱数生成器（seed=0で結果を固定）
print('サイコロ10回:', rng.integers(1, 7, size=10))    # 1〜6の整数を10個
print('正規分布から5個:', rng.normal(50, 10, size=5).round(1))  # 平均50・標準偏差10から5個
print('くじ引き:', rng.choice(['当たり', 'はずれ'], size=5))   # 候補からランダムに5個''',

'''# 問1
import numpy as np
temps = np.array([22,25,19,30,28,24,21])''':
'''# 問1
import numpy as np                          # NumPyを読み込む
temps = np.array([22,25,19,30,28,24,21])    # 1週間の気温の配列''',

# --- 06 pandas ---
'''import pandas as pd
import numpy as np''':
'''import pandas as pd   # 表データ用ライブラリ pandas を pd として読み込む
import numpy as np    # 数値計算用 NumPy を np として読み込む''',

'''s = pd.Series([60, 75, 90], index=['数学', '英語', '国語'])
print(s)
print('英語の点:', s['英語'])''':
'''# ラベル(index)付きの1列データ Series を作る
s = pd.Series([60, 75, 90], index=['数学', '英語', '国語'])
print(s)                  # Series全体を表示
print('英語の点:', s['英語'])  # ラベル'英語'の値を取り出す''',

'''df = pd.DataFrame({
    '名前': ['あおい', 'はると', 'ゆい'],
    '数学': [90, 60, 75],
    '英語': [70, 85, 80],
})
df''':
'''# 辞書から複数列の表 DataFrame を作る
df = pd.DataFrame({
    '名前': ['あおい', 'はると', 'ゆい'],
    '数学': [90, 60, 75],
    '英語': [70, 85, 80],
})
df   # 表を表示''',

'''df = pd.read_csv('../data/students_scores.csv')
df.head()       # 先頭5行を確認''':
'''df = pd.read_csv('../data/students_scores.csv')  # CSVファイルを読み込む
df.head()       # 先頭5行を確認''',

'''print('行数・列数:', df.shape)
print('列名:', list(df.columns))
df.describe()    # 数値列の要約（平均・標準偏差・四分位など）''':
'''print('行数・列数:', df.shape)        # (行数, 列数)
print('列名:', list(df.columns))      # 列名の一覧
df.describe()    # 数値列の要約（平均・標準偏差・四分位など）''',

'''print(df['数学'].head())
print('数学の平均:', df['数学'].mean().round(1))
df[['数学', '英語']].head()''':
'''print(df['数学'].head())          # '数学'列の先頭5行
print('数学の平均:', df['数学'].mean().round(1))  # '数学'列の平均
df[['数学', '英語']].head()        # 2列を選んで先頭5行''',

'''# 数学が80点以上の生徒
good = df[df['数学'] >= 80]
print('80点以上:', len(good), '人')
good.head()''':
'''# 数学が80点以上の行だけを残す（条件フィルタ）
good = df[df['数学'] >= 80]
print('80点以上:', len(good), '人')   # 残った行数 ＝ 人数
good.head()''',

'''# 複数条件は & (かつ) / | (または)。各条件は () で囲む
df[(df['数学'] >= 80) & (df['英語'] >= 80)].head()''':
'''# 複数条件は & (かつ) / | (または)。各条件は () で囲む
df[(df['数学'] >= 80) & (df['英語'] >= 80)].head()  # 数学80以上 かつ 英語80以上''',

'''df['合計'] = df['数学'] + df['英語'] + df['国語']
df['合否'] = np.where(df['数学'] >= 60, '合格', '不合格')
df[['生徒ID', '数学', '合計', '合否']].head()''':
'''df['合計'] = df['数学'] + df['英語'] + df['国語']  # 3教科の合計を新しい列に
df['合否'] = np.where(df['数学'] >= 60, '合格', '不合格')  # 数学60以上で合否を判定
df[['生徒ID', '数学', '合計', '合否']].head()   # 必要な列だけ先頭5行''',

'''# クラスごとの数学の平均
print(df.groupby('クラス')['数学'].mean().round(1))

# 複数の集計をまとめて
df.groupby('クラス').agg(
    人数=('生徒ID', 'count'),
    数学平均=('数学', 'mean'),
    英語平均=('英語', 'mean'),
).round(1)''':
'''# クラスごとに'数学'の平均を計算
print(df.groupby('クラス')['数学'].mean().round(1))

# クラスごとに複数の集計をまとめて行う
df.groupby('クラス').agg(
    人数=('生徒ID', 'count'),    # 人数（件数）
    数学平均=('数学', 'mean'),    # 数学の平均
    英語平均=('英語', 'mean'),    # 英語の平均
).round(1)''',

'''print(df['合否'].value_counts())          # カテゴリの個数
print()
print(df.sort_values('合計', ascending=False)[['生徒ID','合計']].head(3))  # 上位3人
print()
print(pd.crosstab(df['クラス'], df['合否']))  # クラス×合否の表''':
'''print(df['合否'].value_counts())          # カテゴリごとの個数を数える
print()
print(df.sort_values('合計', ascending=False)[['生徒ID','合計']].head(3))  # 合計の高い順 上位3人
print()
print(pd.crosstab(df['クラス'], df['合否']))  # クラス×合否のクロス集計表''',

'''# 準備
import pandas as pd
df = pd.read_csv('../data/students_scores.csv')''':
'''# 準備
import pandas as pd                               # pandasを読み込む
df = pd.read_csv('../data/students_scores.csv')   # データを読み込む''',

# --- 07 matplotlib ---
'''import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 日本語が□に化けるときは、環境に合わせて次の1行を有効化
# plt.rcParams['font.family'] = 'Hiragino Sans'   # Mac
# plt.rcParams['font.family'] = 'Yu Gothic'       # Windows
plt.rcParams['axes.unicode_minus'] = False''':
'''import matplotlib.pyplot as plt   # グラフ描画ライブラリを plt として読み込む
import pandas as pd               # 表データ用
import numpy as np                # 数値計算用

# 日本語が□に化けるときは、環境に合わせて次の1行を有効化
# plt.rcParams['font.family'] = 'Hiragino Sans'   # Mac
# plt.rcParams['font.family'] = 'Yu Gothic'       # Windows
plt.rcParams['axes.unicode_minus'] = False        # マイナス記号の文字化けを防ぐ''',

'''month = [1, 2, 3, 4, 5, 6]
temp = [22, 24, 28, 30, 27, 25]
plt.plot(month, temp, marker='o')
plt.title('気温の変化')
plt.xlabel('月'); plt.ylabel('気温(℃)')
plt.show()''':
'''month = [1, 2, 3, 4, 5, 6]          # x軸（月）
temp = [22, 24, 28, 30, 27, 25]     # y軸（気温）
plt.plot(month, temp, marker='o')   # 折れ線グラフ（点付き）
plt.title('気温の変化')             # タイトル
plt.xlabel('月'); plt.ylabel('気温(℃)')  # 軸ラベル
plt.show()                          # グラフを表示''',

'''kyoka = ['数学', '英語', '国語', '理科']
ninzu = [8, 12, 10, 6]
plt.bar(kyoka, ninzu)
plt.title('好きな教科'); plt.ylabel('人数')
plt.show()''':
'''kyoka = ['数学', '英語', '国語', '理科']  # 棒のラベル
ninzu = [8, 12, 10, 6]                   # 棒の高さ（人数）
plt.bar(kyoka, ninzu)                    # 棒グラフ
plt.title('好きな教科'); plt.ylabel('人数')  # タイトルと軸ラベル
plt.show()''',

'''df = pd.read_csv('../data/students_scores.csv')
plt.hist(df['数学'], bins=10, edgecolor='white')
plt.title('数学の点数の分布'); plt.xlabel('点数'); plt.ylabel('人数')
plt.show()''':
'''df = pd.read_csv('../data/students_scores.csv')   # データ読み込み
plt.hist(df['数学'], bins=10, edgecolor='white')  # ヒストグラム（10階級）
plt.title('数学の点数の分布'); plt.xlabel('点数'); plt.ylabel('人数')  # タイトルと軸ラベル
plt.show()''',

'''plt.scatter(df['数学'], df['英語'], alpha=0.5)
plt.title('数学と英語'); plt.xlabel('数学'); plt.ylabel('英語')
plt.show()''':
'''plt.scatter(df['数学'], df['英語'], alpha=0.5)  # 散布図（alpha=半透明）
plt.title('数学と英語'); plt.xlabel('数学'); plt.ylabel('英語')  # タイトルと軸ラベル
plt.show()''',

'''fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].boxplot([df[df['クラス']==c]['数学'] for c in ['A','B','C']],
              tick_labels=['A','B','C'])
ax[0].set_title('クラス別 数学'); ax[0].set_ylabel('点数')

df['合否'] = np.where(df['数学']>=60,'合格','不合格')
df['合否'].value_counts().plot(kind='pie', autopct='%1.0f%%', ax=ax[1])
ax[1].set_title('合否の割合'); ax[1].set_ylabel('')
plt.show()''':
'''fig, ax = plt.subplots(1, 2, figsize=(11, 4))   # 1行2列のグラフ領域を用意
# 左：クラス別の数学を箱ひげ図にする
ax[0].boxplot([df[df['クラス']==c]['数学'] for c in ['A','B','C']],
              tick_labels=['A','B','C'])
ax[0].set_title('クラス別 数学'); ax[0].set_ylabel('点数')

df['合否'] = np.where(df['数学']>=60,'合格','不合格')  # 合否ラベルを作る
# 右：合否の割合を円グラフにする
df['合否'].value_counts().plot(kind='pie', autopct='%1.0f%%', ax=ax[1])
ax[1].set_title('合否の割合'); ax[1].set_ylabel('')
plt.show()''',

'''df.groupby('クラス')['数学'].mean().plot(kind='bar', title='クラス別 数学の平均')
plt.ylabel('平均点'); plt.xticks(rotation=0)
plt.show()''':
'''# クラス別の数学平均を棒グラフにする
df.groupby('クラス')['数学'].mean().plot(kind='bar', title='クラス別 数学の平均')
plt.ylabel('平均点'); plt.xticks(rotation=0)  # y軸ラベルとx軸目盛りの向き
plt.show()''',
}

MAP = {k.strip(): v for k, v in MAP.items()}

replaced = 0
unmatched = []
for p in sorted(glob.glob(f"{ROOT}/**/*.ipynb", recursive=True)):
    nb = json.load(open(p, encoding="utf-8"))
    changed = False
    for c in nb["cells"]:
        if c["cell_type"] != "code":
            continue
        j = "".join(c["source"])
        key = j.strip()
        if "① セットアップ（最初に実行してください）" in j:
            if j != DATA_SETUP_NEW:
                c["source"] = DATA_SETUP_NEW; changed = True; replaced += 1
            continue
        if key in MAP:
            if j != MAP[key]:
                c["source"] = MAP[key]; changed = True; replaced += 1
        elif p.split("/")[-2] == "01_Python基礎":
            # 01_Python基礎内で未対応の実行セル（空の#問x以外）を検出
            body = [l for l in j.splitlines() if l.strip() and not l.strip().startswith("#")]
            if body:
                unmatched.append((os.path.relpath(p, ROOT), j.splitlines()[0][:40]))
    if changed:
        json.dump(nb, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print("replaced cells:", replaced)
print("unmatched runnable cells in 01_Python基礎:", len(unmatched))
for u in unmatched:
    print("  ", u)
