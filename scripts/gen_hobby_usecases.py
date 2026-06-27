# -*- coding: utf-8 -*-
import json, os, urllib.parse
from nbbuild import md, code, write_nb
ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
def colab(rel): return "https://colab.research.google.com/github/Carlo-Broschi/statistics-python-for-students/blob/main/" + urllib.parse.quote(rel)
def badge(rel): return f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab(rel)})"

# =========================================================
# (A) 00 はじめに：3Dツールの選び方（特色まとめ）
# =========================================================
rel = "07_ホビー_陶芸3D/00_はじめに_3Dツールの選び方.ipynb"
cells = [
 md(f"{badge(rel)}\n\n# ホビー-00. はじめに：陶芸×3D の使いどころとツールの選び方\n\n"
    "「器の3Dモデルを作ったけど、いつ・何に使うの？」に答える地図です。"),
 md("## 🏺 いつ3Dを使う？（陶芸での場面）\n\n"
    "1. **石こう型の原型（マスター）** … 同じ器を何個も作りたいとき。原型を印刷→石こう型→**鋳込み/型押し**で量産。\n"
    "2. **スタンプ・型押し飾り（sprig）・テクスチャローラー** … 模様やロゴを粘土に押す道具。**一番手軽**。\n"
    "3. **こて（プロファイルリブ）・ゲージ・抜き型** … ろくろで一定の曲線にする、板を同じ形に抜く。\n"
    "4. **粘土3Dプリンタ（クレイプリンタ）への入力** … モデルがそのまま作品に。\n"
    "5. **設計検討・容量(ml)計算・蓋合わせ** … 作る前に確認。\n"
    "6. **複雑形状・勘合** … 注ぎ口・取っ手・かみ合う部品など精度がいる所。"),
 md("## 逆に、3Dが要らないとき\n"
    "一点物の**手びねり・ろくろの有機的な器**は、伝統技法のほうが速く・表現も豊か。"
    "3Dは「**反復・精度・型・道具・クレイプリント**」で輝きます。"),
 md("## 🧰 ツールの特色まとめ（選び方）\n\n"
    "| ツール | 操作スタイル | 得意 | 苦手 | 陶芸での使いどころ | 出力・閲覧 |\n"
    "|---|---|---|---|---|---|\n"
    "| **SolidPython** | コードで寸法指定（パラメトリック） | 正確な寸法・**サイズ違いを一括生成**・再現性 | 自由な有機曲面 | 入れ子の鉢セット、食器ラインの原型、収縮逆算の型、**道具(04)** | `.scad`→OpenSCAD |\n"
    "| **Blender** | マウスで自由造形・彫刻 | **有機的な形・模様**・アート | 正確な寸法管理 | アート器、スタンプ/sprig、クレイプリント造形 | アプリ内→STL |\n"
    "| **FreeCAD** | 数値・拘束の精密CAD | **寸法・勘合の精度** | 自由曲面・芸術表現 | 蓋の勘合、こて/テンプレ、抜き型、型の位置決め | アプリ内→STL |\n\n"
    "> ざっくり：**正確さ・量産＝SolidPython/FreeCAD**、**自由な造形＝Blender**。"),
 md("## 🔄 共通ワークフロー\n\n"
    "```\nモデルを作る → 画面で確認/操作 → .stl に書き出す → ①石こう型の原型 / ②クレイプリント / ③道具を印刷\n```\n\n"
    "⚠️ **収縮率**：粘土は焼成で約10〜13%縮みます。仕上がり寸法 ÷ (1−収縮率) で**一回り大きく**設計（型・原型で重要）。"),
 md("## 📚 このフォルダの歩き方\n\n"
    f"- [01 FreeCADで器をつくる]({colab('07_ホビー_陶芸3D/01_FreeCADで器をつくる.ipynb')})（精密・型/道具向き）\n"
    f"- [02 Blenderで器をつくる]({colab('07_ホビー_陶芸3D/02_Blenderで器をつくる.ipynb')})（自由造形・アート向き）\n"
    f"- [03 SolidPythonで器をつくる]({colab('07_ホビー_陶芸3D/03_SolidPythonで器をつくる.ipynb')})（コードで量産・型の原型）\n"
    f"- [04 実用ツールをつくる]({colab('07_ホビー_陶芸3D/04_実用ツールをつくる.ipynb')})（スタンプ・こて・抜き型／**クレイプリンタ不要・一番実用的**）"),
]
write_nb(rel, cells)

# =========================================================
# (B) 各ノートに「🏺 こんな時に使う」を挿入
# =========================================================
INTRO = {
 "01_FreeCADで器をつくる.ipynb":
  "> 🏺 **このツールはこんな時に**：寸法が命のもの。**蓋がぴったり合う**部品、ろくろ用の**こて/テンプレ**、"
  "粘土の**抜き型**、石こう型の位置決め。→ 道具づくりは [04 実用ツール](04_%E5%AE%9F%E7%94%A8%E3%83%84%E3%83%BC%E3%83%AB%E3%82%92%E3%81%A4%E3%81%8F%E3%82%8B.ipynb) も参照。",
 "02_Blenderで器をつくる.ipynb":
  "> 🏺 **このツールはこんな時に**：**有機的な形や模様**。一点物のアート器、**スタンプ/sprig（型押し飾り）**、"
  "クレイプリンタ用の造形。",
 "03_SolidPythonで器をつくる.ipynb":
  "> 🏺 **このツールはこんな時に**：寸法を数値で扱い、**サイズ違いを一括生成**（入れ子の鉢セット・食器ライン）。"
  "収縮率を逆算した**石こう型の原型**づくり。",
}
for fname, note in INTRO.items():
    p = os.path.join(ROOT, "07_ホビー_陶芸3D", fname); nb = json.load(open(p, encoding="utf-8"))
    if any("🏺 **このツールはこんな時に**" in "".join(c["source"]) for c in nb["cells"]):
        continue
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith("# ホビー-0"):
            nb["cells"].insert(i+1, md(note)); break
    json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("intro ->", fname)

# =========================================================
# (C) 03 に「容量計算」＋「石こう型の流れ」を挿入（📦の直前）
# =========================================================
p = os.path.join(ROOT, "07_ホビー_陶芸3D/03_SolidPythonで器をつくる.ipynb")
nb = json.load(open(p, encoding="utf-8"))
if not any("円板法" in "".join(c["source"]) for c in nb["cells"]):
    block = [
      md("## 🥣 容量(ml)を計算する\n\n"
         "器の内側の輪郭 `(内半径, 高さ)` から、薄い**円板を積み上げて**容積を概算します（円板法）。"),
      code("import numpy as np\n"
           "# 内側の輪郭（内半径mm, 高さmm）を下から\n"
           "inner = [(0,8), (20,8), (30,30), (33,68)]\n"
           "r = np.array([p[0] for p in inner]); h = np.array([p[1] for p in inner])\n"
           "# 各区間を円板(円柱)とみなして体積を合計： π r² × 高さ\n"
           "vol_mm3 = np.sum(np.pi * ((r[:-1]+r[1:])/2)**2 * np.diff(h))\n"
           "print(round(vol_mm3/1000, 1), 'ml  (1ml = 1000mm³)')"),
      md("### 🏺 この器を「石こう型の原型」に使う流れ\n"
         "1. モデルを `.scad`→OpenSCADで **`.stl`** に書き出す\n"
         "2. PLA等で3Dプリント（＝原型）\n"
         "3. 原型の周りに石こうを流して **型** を取る\n"
         "4. 型に泥漿を流す＝**鋳込み（スリップキャスト）**で同じ器を量産\n\n"
         "> ⚠️ 焼成で約10〜13%縮むので **仕上がり÷(1−収縮率)** で一回り大きく作る"
         "（`make_bowl` は収縮逆算に対応）。"),
    ]
    for i,c in enumerate(nb["cells"]):
        if "📦 出力ファイル" in "".join(c["source"]):
            nb["cells"][i:i] = block; break
    else:
        nb["cells"] += block
    json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
    print("03 volume+mold inserted")

# =========================================================
# (D) 04 実用ツールをつくる（SolidPython・実行可能）
# =========================================================
rel = "07_ホビー_陶芸3D/04_実用ツールをつくる.ipynb"
ans_rel = "解答集/07_ホビー_陶芸3D/04_実用ツールをつくる.md"
setup = code(
 "# === ① セットアップ（最初に実行）===\n"
 "try:\n    from solid2 import cylinder, cube, circle, linear_extrude, translate\nexcept ImportError:\n"
 "    import subprocess, sys; subprocess.run([sys.executable,'-m','pip','install','-q','solidpython2'])\n"
 "    from solid2 import cylinder, cube, circle, linear_extrude, translate\n"
 "import math\nprint('準備OK')")
cells = [
 md(f"{badge(rel)}\n\n# ホビー-04. 実用ツールをつくる（スタンプ・こて・抜き型）\n\n"
    "> 🟢 Colabで実行できます。**最初に「① セットアップ」**を実行。\n\n"
    "> 🏺 **クレイプリンタが無くてもOK**。ふつうの3Dプリンタ（PLA）で印刷して**すぐ使える道具**を作ります。"
    "陶芸で一番手軽な3D活用です。"),
 setup,
 md("## 1. スタンプ（型押し）\n\n"
    "底面のドット模様を粘土に押しつけて模様をつけます。上に持ち手付き。"),
 code("def make_stamp(diameter=40, thickness=8, dot_d=4, dot_h=3, n=8, fn=80):\n"
      "    disk = cylinder(d=diameter, h=thickness, _fn=fn)                    # 本体の円盤\n"
      "    handle = translate([0,0,thickness])(cylinder(d=diameter*0.4, h=25, _fn=40))  # 持ち手\n"
      "    dots = translate([0,0,-dot_h])(cylinder(d=dot_d, h=dot_h, _fn=24))  # 中心のドット（下面）\n"
      "    r = diameter*0.3\n"
      "    for i in range(n):                                                  # 周囲にドットを並べる\n"
      "        a = 2*math.pi*i/n\n"
      "        dots += translate([r*math.cos(a), r*math.sin(a), -dot_h])(cylinder(d=dot_d, h=dot_h, _fn=24))\n"
      "    return disk + handle + dots\n\n"
      "make_stamp(n=8).save_as_scad('stamp.scad')\n"
      "print('stamp.scad を書き出しました')"),
 md("> 💡 ドット模様は左右対称なので問題ありませんが、**文字を入れると粘土側では鏡像**になります（入れるなら反転を）。"),
 md("## 2. プロファイルこて（リブ）\n\n"
    "板の片側を曲線にえぐった道具。ろくろで器の内/外を**一定の曲面にならす**のに使います。"),
 code("def make_rib(radius=60, plate_w=80, plate_h=60, t=4):\n"
      "    plate = cube([plate_w, plate_h, t])                                  # 平らな板\n"
      "    arc = translate([plate_w+radius-15, plate_h/2, -1])(cylinder(r=radius, h=t+2, _fn=120))  # 円で削る\n"
      "    return plate - arc                                                   # 板から円弧を引く＝凹カーブ\n\n"
      "make_rib(radius=60).save_as_scad('rib.scad')\n"
      "print('rib.scad を書き出しました（radiusを変えるとカーブが変わる）')"),
 md("## 3. 抜き型（クッキーカッター式）\n\n"
    "薄い壁の輪っか。たたら（板作り）で粘土を**同じ形に抜く**のに使います。`fn` で形が変わります（円=100, 六角=6）。"),
 code("def make_cutter(size=70, wall=1.5, height=25, fn=100):\n"
      "    outer = circle(d=size, _fn=fn)                 # 外側の輪郭\n"
      "    inner = circle(d=size-2*wall, _fn=fn)          # 内側（壁の厚みぶん小さく）\n"
      "    return linear_extrude(height)(outer - inner)   # 輪郭の差を上に押し出す＝壁\n\n"
      "make_cutter(size=70, fn=100).save_as_scad('cutter_circle.scad')   # 丸\n"
      "make_cutter(size=70, fn=6).save_as_scad('cutter_hex.scad')        # 六角\n"
      "print('cutter_circle.scad / cutter_hex.scad を書き出しました')"),
 code("import glob, os\nfor f in sorted(glob.glob('*.scad')):\n    print(f, f'({os.path.getsize(f)} bytes)')"),
 md("---\n## 🏆 練習問題\n\n"
    "**問1.** `make_stamp` の `n`（ドットの数）を 12 にして印刷データを作ろう。\n\n"
    "**問2.** `make_cutter` で **五角形**（fn=5）の抜き型を作ろう。\n\n"
    "**問3.** `make_rib` の `radius` を 40 と 100 で作り、カーブの違いを OpenSCAD で見比べよう。"),
 code("# 問1〜3\n"),
 md("> 🔑 **解答例は別ページ**（ネタバレ防止）👉 "
    "**[解答例を開く](https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/"
    + urllib.parse.quote(ans_rel) + ")**"),
 md("## 📒 用語集 ＆ チートシート\n\n"
    "| 道具 | 何に使う |\n|---|---|\n"
    "| スタンプ | 模様・ロゴを型押し |\n| こて(リブ) | ろくろで曲面をならす |\n"
    "| 抜き型 | 板を同じ形に抜く |\n| sprig | 別作りの飾りを貼る型 |\n\n"
    "印刷したら：OpenSCADで `.scad`→`.stl` 書き出し → スライサー(Cura等)で印刷。"),
 code("# チートシート（SolidPythonの基本操作）\n"
      "cylinder(d=40, h=8, _fn=80)      # 円柱\ncube([80, 60, 4])               # 直方体\n"
      "circle(d=70, _fn=6)             # 2D 六角\nlinear_extrude(25)(circle(d=70))  # 2D→3D 押し出し\n"
      "translate([10,0,0])(cube([5,5,5]))   # 移動\n# A + B = 合体,  A - B = くり抜き"),
]
write_nb(rel, cells)
ans_md = """# 04_実用ツールをつくる ― 解答例

```python
# 問1: ドット12個のスタンプ
make_stamp(n=12).save_as_scad('stamp12.scad')

# 問2: 五角形の抜き型
make_cutter(size=70, fn=5).save_as_scad('cutter_penta.scad')

# 問3: カーブ違いのこて
make_rib(radius=40).save_as_scad('rib_r40.scad')
make_rib(radius=100).save_as_scad('rib_r100.scad')
```
💡 半径が小さいほど急なカーブ、大きいほどゆるいカーブのこてになる。OpenSCADで開いて見比べよう。
"""
os.makedirs(os.path.dirname(os.path.join(ROOT, ans_rel)), exist_ok=True)
open(os.path.join(ROOT, ans_rel), "w", encoding="utf-8").write(ans_md)
print("=== hobby usecases done ===")
