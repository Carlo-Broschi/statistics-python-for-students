# scripts/ — 教材ノートのビルド用スクリプト

この `.ipynb` 教材は手書きではなく、ここにあるスクリプトで**生成・加工**しています。
ノートを作り直したり、一括で修正したりするための「足場」です。

> ⚠️ 各スクリプト冒頭の `ROOT` はローカルの絶対パス（`/Users/.../Education_Python`）を直書きしています。
> 別環境で動かすときは `ROOT` を書き換えてください。実行は `python3 scripts/xxx.py`（必要に応じて `uv run --with ...`）。

## 共通ヘルパ
| ファイル | 役割 |
|---|---|
| `nbbuild.py` | `md()` / `code()` / `write_nb()`。最小構成のJupyterノートをJSONで書き出す土台。各 `gen_*` が import する |
| `gen_data.py` | `data/*.csv`（生徒成績・天気・BtoB商談・Webマーケ・A/Bテスト）を合成生成。seed固定で再現可能 |

## ① 本体ノート生成（gen_*）
| ファイル | 生成先 |
|---|---|
| `gen_python.py` | `01_Python基礎/01〜04`（純Python） |
| `gen_bridge.py` | `01_Python基礎/05〜07`（NumPy / pandas / matplotlib 入門） |
| `gen_stats4.py` | `02_統計_4級/01〜04` |
| `gen_stats3.py` | `03_統計_3級/01〜04` |
| `gen_stats2.py` | `04_統計_2級/01〜03` |
| `gen_marketing.py` | `05_実践_BtoBマーケ/01〜03` |
| `gen_hobby.py` | `07_ホビー_陶芸3D/01〜03` |
| `gen_supp_4.py` `gen_supp_3.py` `gen_supp_2.py` | 各級の追加ノート（4級05-06 / 3級05-06 / 2級04-07） |

## ② 一括加工（生成後にこの順で当てる。すべて冪等）
| ファイル | 役割 |
|---|---|
| `colabify.py` | 全ノートに「Open in Colab」バッジ＋「① セットアップ」セル（Colabでデータ自動生成 / solidpython2自動install）を付与。FreeCAD/Blenderは非対応注記 |
| `colabify2.py` | 解答例の整形（`<details>`化）＋データを使う箇所に「列の説明＋サンプル行」プレビューを挿入 |
| `cmt_batch1.py` 〜 `cmt_batch4.py` / `cmt_hobby.py` | 動かすコードの**全行コメント化**（旧→新の文字列置換で実施） |
| `extract_solutions.py` | 解答例を本編から抜き出し `解答集/` に分離。本編には解答ページへのリンクのみ残す（GitHubプレビューでもネタバレ防止） |

## ③ 検証
| ファイル | 役割 |
|---|---|
| `run_check.py` / `finalcheck.py` / `run_new.py` / `verify_colab.py` | 全ノートのJSON妥当性チェック＋nbconvertでの実行テスト |
| `eq.py` | Colab用に埋め込んだデータ生成コードが、committed CSVとバイト一致するかの照合 |
| `extract.py` `fc2.py` `test_solid.py` | 一時的な確認用（PDF抽出・部分実行・SolidPython API確認） |

## ノートを一から作り直す手順
```bash
cd Education_Python
uv run --with numpy --with pandas python scripts/gen_data.py     # データ
python3 scripts/gen_python.py && python3 scripts/gen_bridge.py \
  && python3 scripts/gen_stats4.py && python3 scripts/gen_stats3.py \
  && python3 scripts/gen_stats2.py && python3 scripts/gen_marketing.py \
  && python3 scripts/gen_hobby.py \
  && python3 scripts/gen_supp_4.py && python3 scripts/gen_supp_3.py && python3 scripts/gen_supp_2.py
python3 scripts/colabify.py && python3 scripts/colabify2.py      # バッジ・プレビュー・解答整形
python3 scripts/cmt_batch1.py && python3 scripts/cmt_batch2.py \
  && python3 scripts/cmt_batch3.py && python3 scripts/cmt_batch4.py && python3 scripts/cmt_hobby.py  # 全行コメント
python3 scripts/extract_solutions.py                            # 解答を 解答集/ へ分離
```

> 注：`cmt_*` と `colabify2`（解答整形）は「特定の旧文字列」を前提に置換します。`gen_*` を編集して内容が変わると一致しなくなるので、**コメントや構造を変えるなら `gen_*` 側に直接書く**のが本筋です。これらの加工スクリプトは「当時の状態を一括変換した記録」と捉えてください。
