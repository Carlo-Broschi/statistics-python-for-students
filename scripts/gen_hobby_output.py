# -*- coding: utf-8 -*-
"""陶芸3ノートの末尾に「📦 出力ファイルの見方・操作」を追加（冪等）。"""
import json, os
ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
def md(t): return {"cell_type":"markdown","metadata":{},"source":t}
def code(t): return {"cell_type":"code","execution_count":None,"metadata":{},"outputs":[],"source":t}

STL = ("### `.stl` ファイルの見方・使い道（共通）\n\n"
       "`.stl` は3D形状の標準フォーマット。次のように扱えます。\n"
       "- **見るだけ**：ダブルクリックでOSの3Dビューア（Mac=プレビュー / Win=3Dビューア）。"
       "または無料オンラインビューア（`viewstl.com` などにファイルをドラッグ）。\n"
       "- **編集**：Blender や FreeCAD に読み込んで形を調整。\n"
       "- **3Dプリント**：スライサー（**Cura** / **PrusaSlicer**、無料）で `.stl` を開く → 印刷設定 → プリンタへ。\n\n"
       "> 🏺 **陶芸での使い道**：プリントした器そのものは焼けませんが、**石こう型の原型**や、"
       "ろくろ・たたら作りの**テンプレート/ゲージ**として活用できます。")

ADD = {
"01_FreeCADで器をつくる.ipynb":[
  md("## 📦 出力ファイルの見方・操作\n\n"
     "**可視化は FreeCAD の中で完結**します（上で `Part.show()` した器を、その場で回せます）。\n"
     "- 回転：マウス中ボタンドラッグ／画面右上のナビゲーションキューブ\n"
     "- ズーム：マウスホイール\n"
     "- 書き出し：メニュー **ファイル → エクスポート** で `.stl` を選ぶ（コードの `exportStl` でも可）"),
  md(STL),
],
"02_Blenderで器をつくる.ipynb":[
  md("## 📦 出力ファイルの見方・操作\n\n"
     "**可視化は Blender のビューポート内**で完結します。\n"
     "- 回転：マウス中ボタンドラッグ／テンキー **1**=正面・**7**=真上\n"
     "- ズーム：マウスホイール\n"
     "- 書き出し：メニュー **File → Export → STL**（コードの `wm.stl_export` でも可）\n"
     "- 💡 Blenderの強み：書き出す前に **スカルプトモード**で手彫りのように凹凸を足せます。"),
  md(STL),
],
"03_SolidPythonで器をつくる.ipynb":[
  md("## 📦 出力ファイルの見方・操作\n\n"
     "SolidPython が出す `.scad` は**設計レシピ（テキスト）**なので、見るには **OpenSCAD**（無料）で開きます。\n\n"
     "**OpenSCAD での手順**\n"
     "1. [openscad.org](https://openscad.org/) からインストール\n"
     "2. **File → Open** で `chawan.scad` を開く（自動で3Dプレビューが出る）\n"
     "3. 操作：左ドラッグ=回転 / ホイール=ズーム / 右ドラッグ=平行移動\n"
     "4. **F5**=高速プレビュー、**F6**=本レンダリング（正確な形）\n"
     "5. **F7**（または **File → Export → Export as STL**）で `.stl` を書き出す"),
  md("### Colab で動かした場合：まずダウンロード\n\n"
     "Colab はクラウド上で動くので、生成された `.scad` を**自分のPCに落として**から OpenSCAD で開きます。\n"
     "（ローカルのJupyterなら、ノートと同じフォルダにすでに保存されています。）"),
  code("# Colabなら生成した.scadをダウンロード（ローカルJupyterでは不要）\n"
       "try:\n"
       "    from google.colab import files\n"
       "    files.download('chawan.scad')          # 必要なら他の.scadも同様に\n"
       "except Exception:\n"
       "    import glob\n"
       "    print('ローカル環境です。次の .scad がノートと同じフォルダにあります:')\n"
       "    print(glob.glob('*.scad'))"),
  md(STL),
],
}

for fname, newcells in ADD.items():
    p = os.path.join(ROOT, "07_ホビー_陶芸3D", fname)
    nb = json.load(open(p, encoding="utf-8"))
    if any("📦 出力ファイル" in "".join(c["source"]) for c in nb["cells"]):
        print("skip (already)", fname); continue
    nb["cells"] += newcells
    json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("appended", fname, "->", len(nb["cells"]), "cells")
print("=== hobby output sections done ===")
