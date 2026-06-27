# -*- coding: utf-8 -*-
import os, urllib.parse
from nbbuild import md, code, write_nb

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
GH = "https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/"
NB = "01_Python基礎/08_スプレッドシートからPythonへ.ipynb"
ANS = "解答集/01_Python基礎/08_スプレッドシートからPythonへ.md"
colab = "https://colab.research.google.com/github/Carlo-Broschi/statistics-python-for-students/blob/main/" + urllib.parse.quote(NB)
ans_url = GH + urllib.parse.quote(ANS)

setup = code(
    "# === ① セットアップ（最初に実行してください）===\n"
    "import pandas as pd               # 表データ\n"
    "import os\n"
    "# ローカルに無ければ公開リポジトリ(raw)からExcelを読み込む\n"
    "RAW = 'https://raw.githubusercontent.com/Carlo-Broschi/statistics-python-for-students/main/data/'\n"
    "xlsx = '../data/marketing.xlsx' if os.path.exists('../data/marketing.xlsx') else RAW + 'marketing.xlsx'\n"
    "print('読み込み元:', xlsx)"
)

cells = [
    md(f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab})\n\n"
       "# Python基礎-08. スプレッドシートからPythonへ\n\n"
       "> 🟢 Colab（ブラウザ）で実行できます。**最初に「① セットアップ」セルを実行**してください。\n\n"
       "ふだん **Excel / Googleスプレッドシート** で見ているデータを、Pythonに取り込んで分析する方法です。"
       "「いつものスプレッドシート」と「Python」を**つなぐ**のがこの章のねらいです。"),
    setup,
    md("## 🎯 この章でできるようになること\n"
       "- Excelブックのデータを Python に読み込める（`read_excel`）\n"
       "- 1つのブックの**複数シート**を扱える\n"
       "- Excelの**ピボット集計**を pandas の `groupby` で再現できる\n"
       "- Googleスプレッドシートを URL で読み込める\n"
       "- 分析結果を **Excelに書き出せる**（`to_excel`）\n\n"
       "**前提**：`01_Python基礎/06 pandas入門`　/　**所要**：約25分"),
    md("## 1. Excelブックを読む（`read_excel`）\n\n"
       "教材の `marketing.xlsx` は、商談・Webマーケ・ABテスト・月次KPI・顧客 の5シートが入った"
       "**1つのブック**です（実務でよくある“タブで分けた1ファイル”の形）。"),
    code("deals = pd.read_excel(xlsx, sheet_name='商談')   # 「商談」シートを読み込む\n"
         "deals.head()"),
    md("### 📋 「商談」シート（架空のBtoB商談400件）\n"
       "| 列 | 意味 |\n|---|---|\n| 商談ID | 商談の番号 |\n| 受注日 | 日付 |\n| 業界 | 顧客の業界 |\n"
       "| 獲得チャネル | 展示会/Web広告/メルマガ/紹介/テレアポ |\n| 商談金額 | 円 |\n| 担当者 | 営業担当 |\n| 受注 | 1=成約 / 0=失注 |"),
    md("## 2. シート一覧と全シート読み込み"),
    code("xls = pd.ExcelFile(xlsx)\n"
         "print('シート名:', xls.sheet_names)            # ブックに入っているシート一覧\n\n"
         "all_sheets = pd.read_excel(xlsx, sheet_name=None)   # 全シートをまとめて辞書で取得\n"
         "all_sheets['顧客'].head()                       # 「顧客」シートの先頭"),
    md("## 3. Excelのピボットを pandas で再現する\n\n"
       "Excelの「ピボットテーブルで**チャネル別の受注金額合計**」は、pandasの `groupby` で1行です。"),
    code("won = deals[deals['受注'] == 1]                 # 受注した商談だけ\n"
         "by_ch = won.groupby('獲得チャネル')['商談金額'].sum().sort_values(ascending=False)\n"
         "print(by_ch)"),
    md("> 💡 **Pythonの嬉しさ**：同じ集計を毎回ピボットで作り直す必要がない。"
       "データが更新されても、このセルを実行するだけで結果が更新されます（再現性）。"),
    md("## 4. Googleスプレッドシートを読む（URL）\n\n"
       "Googleスプレッドシートは、共有URLを **CSV書き出しURL** に変えると `read_csv` で読めます。\n\n"
       "```\nhttps://docs.google.com/spreadsheets/d/<ファイルID>/export?format=csv&gid=<シートのgid>\n```\n\n"
       "手順：対象シートを開く → URL の `/edit#gid=...` の `<ファイルID>` と `gid` を上の形に当てはめる。"),
    code("# 例（自分のスプレッドシートのIDとgidに置き換えて実行）:\n"
         "# url = 'https://docs.google.com/spreadsheets/d/XXXXXXXX/export?format=csv&gid=0'\n"
         "# my_df = pd.read_csv(url)\n"
         "# my_df.head()\n"
         "print('↑ コメントを外し、自分のスプレッドシートのURLに変えて使います')"),
    md("> ⚠️ **注意**：URLで読むには、そのスプレッドシートが「リンクを知っている全員が閲覧可」または"
       "「ウェブに公開」されている必要があります。**社外秘・個人情報のデータは公開しないこと。**"),
    md("## 5. 結果をExcelに書き出す（`to_excel`）\n\n"
       "分析結果を「Excelで」上司や同僚に渡したいとき。"),
    code("summary = won.groupby('獲得チャネル')['商談金額'].agg(['count', 'sum'])  # 件数と合計\n"
         "summary.columns = ['受注件数', '売上合計']\n"
         "summary.to_excel('チャネル別集計.xlsx')          # Excelファイルに書き出し\n"
         "print('チャネル別集計.xlsx を書き出しました')"),
    md("## 🧠 確認テスト（自動採点）\n\n"
       "`ans = None` を自分の計算で置き換えて実行すると、その場で正誤が出ます。"),
    code("# 採点用の関数（答え合わせに使うだけ）\n"
         "def _check(name, got, want, tol=1e-2):\n"
         "    if got is None:\n"
         "        print(f'⬜ {name}: まだ入力されていません（ans を埋めてね）'); return\n"
         "    ok = abs(got - want) <= tol\n"
         "    print(('✅ 正解！ ' if ok else '❌ もう一度 ') + f'{name}: あなたの答え = {got}')"),
    code("# Q1: 商談の件数（deals の行数）を ans に\n"
         "ans = None   # 例: len(deals)\n"
         "_check('Q1 商談件数', ans, len(deals))"),
    code("# Q2: 受注した商談の件数を ans に\n"
         "ans = None   # 例: (deals['受注'] == 1).sum()\n"
         "_check('Q2 受注件数', ans, int((deals['受注'] == 1).sum()))"),
    md("---\n## 🏆 練習問題\n\n"
       "**問1.** `Webマーケ` シートを読み、チャネル別の **クリック数の合計** を出そう。\n\n"
       "**問2.** `顧客` シートを読み、**業界別の累計売上の平均** を出そう。\n\n"
       "**問3.** 問2の結果を `to_excel` で `業界別売上.xlsx` に書き出そう。"),
    code("# 問1〜3\n"),
    md("> 🔑 **解答例は別ページ**（ネタバレ防止）👉 "
       f"**[解答例を開く]({ans_url})**"),
    md("## 📒 用語集 ＆ チートシート\n\n"
       "| やりたいこと | コード |\n|---|---|\n"
       "| 1シートを読む | `pd.read_excel('book.xlsx', sheet_name='商談')` |\n"
       "| シート名一覧 | `pd.ExcelFile('book.xlsx').sheet_names` |\n"
       "| 全シート読む | `pd.read_excel('book.xlsx', sheet_name=None)` |\n"
       "| ピボット集計 | `df.groupby('列')['値'].sum()` |\n"
       "| Excelに書き出す | `df.to_excel('out.xlsx', index=False)` |\n"
       "| Googleスプレッドシート | `.../export?format=csv&gid=...` を `read_csv` |"),
    code("# チートシート（スプレッドシート I/O）\n"
         "pd.read_excel(xlsx, sheet_name='Webマーケ')        # シート指定で読む\n"
         "pd.ExcelFile(xlsx).sheet_names                     # シート一覧\n"
         "deals.groupby('業界')['商談金額'].sum()             # ピボット相当\n"
         "deals.head().to_excel('sample.xlsx', index=False)  # 書き出し"),
]
write_nb(NB, cells)

ans_md = """# 08_スプレッドシートからPythonへ ― 解答例（解説つき）

**問1. Webマーケ：チャネル別クリック数の合計**
```python
mk = pd.read_excel(xlsx, sheet_name='Webマーケ')
print(mk.groupby('チャネル')['クリック数'].sum())
```
💡 シートを指定して読み、`groupby('チャネル')` で合計。Excelのピボットと同じ集計。

**問2. 顧客：業界別の累計売上の平均**
```python
cust = pd.read_excel(xlsx, sheet_name='顧客')
print(cust.groupby('業界')['累計売上'].mean().round(0))
```
💡 `sum` を `mean` に変えるだけで「合計→平均」。

**問3. 結果をExcelに書き出す**
```python
result = cust.groupby('業界')['累計売上'].mean().round(0)
result.to_excel('業界別売上.xlsx')
```
💡 `to_excel` でそのままExcelファイルに。上司や同僚に渡しやすい。
"""
os.makedirs(os.path.dirname(os.path.join(ROOT, ANS)), exist_ok=True)
open(os.path.join(ROOT, ANS), "w", encoding="utf-8").write(ans_md)
print("wrote", NB)
