# 中高生のための Python × 統計 × データ分析 × 3Dモデリング

Jupyter Notebook で「Pythonの基礎」→「統計（統計検定 4〜2級レベル）」→「ビジネスデータ分析の実践」→「3Dモデリングで陶芸」までを、手を動かしながら学べる教材です。

## 学習の流れ

| フォルダ | 内容 | レベルの目安 |
|---|---|---|
| `01_Python基礎` | print・変数・リスト・ループ・関数 | はじめての人 |
| `02_統計_4級` | データの種類・代表値・ばらつき・確率・クロス集計／PPDAC・基本グラフ・時系列・場合の数 | 統計検定4級相当 |
| `03_統計_3級` | 標準偏差・相関と回帰・確率分布・標本／実験と条件付き確率・共分散・変動係数・正規近似 | 統計検定3級相当 |
| `04_統計_2級` | 区間推定・仮説検定・カイ二乗・分散分析／母分散F検定・各種分布とベイズ・重回帰・抽出法・格差指標 | 統計検定2級相当 |
| `05_実践_BtoBマーケ` | 売上分析・マーケファネル・A/Bテスト（架空のBtoB企業データ） | 4〜3級の応用 |
| `06_ホビー_陶芸3D` | FreeCAD / Blender / SolidPython で器を3Dモデリング | お楽しみ |

各ノートは「説明 → 例 → 🏆 練習問題 → 解答例（折りたたみ）」の順。番号順に進めるのがおすすめです。

> 📌 「統計検定」とは明記していませんが、各級の出題範囲・過去問のテーマに沿って構成しています。
> 公式の出題範囲・試験形式・過去問の入手先は [`docs/統計検定_出題範囲と過去問.md`](docs/統計検定_出題範囲と過去問.md) にまとめています（各範囲項目↔ノートの対応表つき）。

## セットアップ（uv 利用）

```bash
cd Education_Python
uv sync                 # 依存をインストール
uv run jupyter lab      # JupyterLab を起動
```

`uv` を使わない場合は `pip install jupyterlab numpy pandas matplotlib scipy statsmodels solidpython2`。

### 日本語が文字化けするとき（グラフ）

各ノートの最初のセルにあるコメントを有効にしてください。

```python
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Hiragino Sans'   # Mac
# plt.rcParams['font.family'] = 'Yu Gothic'     # Windows
# plt.rcParams['font.family'] = 'IPAexGothic'   # Linux
```

## サンプルデータ（`data/` フォルダ）

すべて学習用に生成した架空データです（実在の企業・個人とは関係ありません）。

| ファイル | 内容 | 主に使う章 |
|---|---|---|
| `students_scores.csv` | 120人の教科別テスト点数・勉強時間・クラス | 統計4〜3級 |
| `weather.csv` | 1か月の気温・降水量 | 統計4級の練習 |
| `sales_btob.csv` | 400件のBtoB商談（業界・チャネル・金額・受注） | 実践マーケ・2級 |
| `web_marketing.csv` | チャネル×月のマーケファネル（表示・クリック・獲得・費用） | 実践マーケ |
| `ab_test.csv` | LPボタン色のA/Bテスト結果 | 実践マーケ・2級 |

## 3Dモデリングのノートについて

- **FreeCAD / Blender**：ソフト内蔵のPythonで動かします。ノートのコードを各ソフトのPythonコンソール／Scriptingタブに貼り付けて使います（このJupyter上では実行しません）。
- **SolidPython**：このJupyter上でそのまま実行でき、`.scad` ファイルを書き出します。表示には無料の [OpenSCAD](https://openscad.org/) を使います。

3つとも共通テーマは「回転体（ろくろと同じ発想）で器をつくる」。粘土の収縮率を考えた寸法設計など、陶芸ならではの計算も練習できます。
