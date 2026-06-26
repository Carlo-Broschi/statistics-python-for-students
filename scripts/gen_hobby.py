from nbbuild import md, code, write_nb

shrink = md(
    "### 🏺 陶芸ならではの注意：収縮率\n\n"
    "粘土は乾燥・焼成で **10〜15%ちぢみます**。焼き上がりで口径120mmにしたいなら、\n"
    "モデルは `120 ÷ (1 - 0.13) ≈ 138mm` で作ります。これは比の良い練習にもなります。\n\n"
    "```python\n"
    "finish = 120          # 焼き上がりで欲しい口径(mm)\n"
    "shrink = 0.13         # 収縮率13%\n"
    "model = finish / (1 - shrink)\n"
    "print(round(model, 1), 'mm で設計する')\n"
    "```"
)

# =====================================================================
# 01 FreeCAD
# =====================================================================
cells = [
    md("# ホビー-01. FreeCAD で陶芸の器をつくる\n\n"
       "**FreeCAD** は無料のCADソフト。正確な寸法（mm単位）で設計でき、\n"
       "ろくろで作る器のような「回転体」がとても得意です。\n\n"
       "このノートは **設計図と考え方** を説明します。\n"
       "コードは FreeCAD の中の Python コンソールに貼り付けて動かします。\n\n"
       "> 💡 このノート自体は実行しなくてOK。FreeCADを開いて、コードをコピーして使います。"),
    md("## 0. 準備\n\n"
       "1. [freecad.org](https://www.freecad.org/) から FreeCAD をインストール\n"
       "2. メニュー **表示 → パネル → Python コンソール** にチェック\n"
       "3. 下に出てくる黒い入力欄に、これから出てくるコードを貼り付けます"),
    md("## 1. 器づくりの考え方：回転体\n\n"
       "茶碗や湯のみは、**断面（半分の輪郭）を1本の軸のまわりに360°回す**とできます。\n"
       "ろくろと同じ発想です。\n\n"
       "```\n"
       "  輪郭(プロファイル)        回転        器\n"
       "   |‾\\                                  ___\n"
       "   |  \\         ──360°回す──>          /   \\\n"
       "   |__/                                \\___/\n"
       "```\n\n"
       "やることは「断面を点でかく → 面にする → 回す」の3ステップだけです。"),
    shrink,
    md("## 2. 茶碗をつくるスクリプト\n\n"
       "FreeCAD の Python コンソールに貼り付けてください。\n"
       "単位は mm。点は `(半径, 高さ)` の順で、内側と外側をぐるりと一周する閉じた輪郭です。"),
    code("# === FreeCADのPythonコンソールに貼り付け ===\n"
         "import FreeCAD as App\n"
         "import Part\n"
         "from FreeCAD import Vector\n\n"
         "doc = App.newDocument('Chawan')\n\n"
         "# 断面プロファイル (半径, 高さ) ※閉じた輪郭にする\n"
         "pts = [\n"
         "    Vector(0,   0, 0),   # 底の中心（外）\n"
         "    Vector(45,  0, 0),   # 底の外ふち\n"
         "    Vector(62, 70, 0),   # 口の外ふち（口が広がる）\n"
         "    Vector(56, 70, 0),   # 口の内ふち → 肉厚6mm\n"
         "    Vector(39,  8, 0),   # 見込み（内側の壁）\n"
         "    Vector(0,   8, 0),   # 内側の底\n"
         "    Vector(0,   0, 0),   # 閉じる\n"
         "]\n\n"
         "wire = Part.makePolygon(pts)\n"
         "face = Part.Face(wire)\n"
         "# Y軸(高さ方向)のまわりに360°回転\n"
         "bowl = face.revolve(Vector(0,0,0), Vector(0,1,0), 360)\n\n"
         "Part.show(bowl, 'Chawan')\n"
         "doc.recompute()\n"
         "# 全体を見る: メニュー 表示→標準ビュー→軸測 / マウスホイールでズーム"),
    md("実行すると、画面に茶碗が現れます！ 数字を変えると形が変わります。\n\n"
       "- `62 → 50`：口がすぼまった湯のみ風に\n"
       "- 高さ `70 → 110`：背の高いカップに\n"
       "- 肉厚（外と内の半径の差）を大きく：どっしりした器に"),
    md("## 3. 高台（こうだい）をつける\n\n"
       "器の底の輪っか状の脚を「高台」といいます。\n"
       "小さな円柱を引き算（くり抜き）して表現できます。"),
    code("# 底をへこませて高台をつくる（コンソールに追記）\n"
         "cut = Part.makeCylinder(33, 6, Vector(0,0,0), Vector(0,1,0))\n"
         "chawan_with_foot = bowl.cut(cut)\n"
         "Part.show(chawan_with_foot, 'Chawan_kodai')\n"
         "doc.recompute()"),
    md("## 4. STLで書き出して3Dプリント／型に使う\n\n"
       "メニュー **ファイル → エクスポート** で `.stl` を選ぶか、コードでも出せます。"),
    code("# 書き出し（パスは自分の環境に合わせて）\n"
         "bowl.exportStl('/Users/あなた/Desktop/chawan.stl')\n"
         "print('保存しました')"),
    md("---\n## 🏆 チャレンジ課題\n\n"
       "**課題1.** 焼き上がりで口径100mm・高さ60mmの湯のみにしたい。\n"
       "収縮率12%を考えて、モデルの寸法を計算し、`pts` を書き換えよう。\n\n"
       "**課題2.** 口が外に大きく開く「抹茶碗」と、まっすぐな「そば猪口」を作り分けよう。\n\n"
       "**課題3.**（発展）`pts` の中間に点を増やして、ふくらみのある曲線的な器にしよう。\n\n"
       "> 次は同じ器を **Blender** で、より自由な曲面として作ってみます（02のノートへ）。"),
]
write_nb("07_ホビー_陶芸3D/01_FreeCADで器をつくる.ipynb", cells)

# =====================================================================
# 02 Blender
# =====================================================================
cells = [
    md("# ホビー-02. Blender で陶芸の器をつくる\n\n"
       "**Blender** は無料の3DCGソフト。FreeCADより**曲面が自由**で、\n"
       "ぷっくりした花瓶や有機的な形が得意です。Pythonで自動生成できます。\n\n"
       "このノートのコードは Blender の **Scripting** タブに貼り付けて実行します。"),
    md("## 0. 準備\n\n"
       "1. [blender.org](https://www.blender.org/) から Blender をインストール\n"
       "2. 上のタブの **Scripting** をクリック\n"
       "3. 中央の **New** で新しいテキストを作り、コードを貼り付け\n"
       "4. ▶ (Run Script) または `Alt+P` で実行"),
    md("## 1. 考え方：プロファイルを spin（回転）させる\n\n"
       "FreeCADと同じ「回転体」ですが、Blenderでは輪郭を**点の鎖**で作り、\n"
       "`bmesh.ops.spin` でぐるっと回してメッシュ（面の集まり）にします。\n"
       "あとから厚み・なめらかさを足せるのが強みです。"),
    shrink,
    md("## 2. 花瓶をつくるスクリプト\n\n"
       "`profile` は `(半径, 高さ)` の点。くびれや膨らみを自由に作れます。"),
    code("# === BlenderのScriptingタブに貼り付け ===\n"
         "import bpy, bmesh, math\n\n"
         "# 既存オブジェクトを消す\n"
         "bpy.ops.object.select_all(action='SELECT')\n"
         "bpy.ops.object.delete()\n\n"
         "# 花瓶の輪郭 (半径, 高さ) ※下から上へ。膨らみとくびれ\n"
         "profile = [\n"
         "    (20, 0), (40, 4), (55, 30), (50, 60),   # 下半分がふくらむ\n"
         "    (30, 90), (28, 110), (40, 130), (38, 140) # 上でくびれて口が開く\n"
         "]\n\n"
         "mesh = bpy.data.meshes.new('Vase')\n"
         "obj = bpy.data.objects.new('Vase', mesh)\n"
         "bpy.context.collection.objects.link(obj)\n\n"
         "bm = bmesh.new()\n"
         "verts = [bm.verts.new((r, 0, h)) for r, h in profile]\n"
         "edges = [bm.edges.new((verts[i], verts[i+1])) for i in range(len(verts)-1)]\n\n"
         "# Z軸まわりに360°回す（64分割でなめらかに）\n"
         "geom = verts + edges\n"
         "bmesh.ops.spin(bm, geom=geom, cent=(0,0,0), axis=(0,0,1),\n"
         "               angle=math.radians(360), steps=64)\n"
         "bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)\n"
         "bm.to_mesh(mesh)\n"
         "bm.free()"),
    md("ここまでで「紙のように薄い」花瓶ができます。次に厚みとなめらかさを足します。"),
    code("# 厚み(肉厚)をつける Solidify モディファイア\n"
         "solid = obj.modifiers.new('thick', 'SOLIDIFY')\n"
         "solid.thickness = 5   # 肉厚5mm\n\n"
         "# 表面をなめらかにする\n"
         "for p in mesh.polygons:\n"
         "    p.use_smooth = True\n"
         "subsurf = obj.modifiers.new('smooth', 'SUBSURF')\n"
         "subsurf.levels = 2\n\n"
         "print('花瓶ができました！ テンキー1で正面、マウス中ボタンで回転')"),
    md("## 3. 形をいじって遊ぶ\n\n"
       "`profile` の数字を変えるだけで、いろんな器になります。\n\n"
       "| 作りたいもの | ヒント |\n"
       "|---|---|\n"
       "| 茶碗 | 点を少なく、低く広く。最後の高さを60くらいに |\n"
       "| 徳利（とっくり） | 真ん中を太く、首を細く（半径を急に小さく） |\n"
       "| 一輪挿し | 全体を細長く、口をすぼめる |\n\n"
       "> 💡 数字を少し変えて ▶ を押す、をくり返すと感覚がつかめます。"),
    md("## 4. 書き出し\n\n"
       "メニュー **File → Export → STL (.stl)** で保存。3Dプリンタや、\n"
       "石こう型づくりの参考形状として使えます。コードでも出せます。"),
    code("# STLで書き出し（パスは自分用に変更）\n"
         "bpy.ops.object.select_all(action='DESELECT')\n"
         "obj.select_set(True)\n"
         "bpy.ops.wm.stl_export(filepath='/Users/あなた/Desktop/vase.stl',\n"
         "                      export_selected_objects=True)"),
    md("---\n## 🏆 チャレンジ課題\n\n"
       "**課題1.** `profile` を増やして、上にいくほど口が開く「ラッパ型の花器」を作ろう。\n\n"
       "**課題2.** `solid.thickness` を 2 と 10 で比べ、見た目と「重そうさ」の違いを確かめよう。\n\n"
       "**課題3.**（発展）`profile` の半径を `math.sin` で波打たせ、ねじれ・凹凸のある現代的な器に挑戦。\n\n"
       "> 次は **SolidPython** で、コードそのもので形を定義する作り方を学びます（03のノートへ）。"),
]
write_nb("07_ホビー_陶芸3D/02_Blenderで器をつくる.ipynb", cells)

# =====================================================================
# 03 SolidPython（実行可能）
# =====================================================================
cells = [
    md("# ホビー-03. SolidPython で器を「コードで」つくる\n\n"
       "**SolidPython** は Python のコードがそのまま3Dモデルになるライブラリ。\n"
       "書いたコードは **OpenSCAD** という形式(`.scad`)になり、無料ソフトで見られます。\n\n"
       "**このノートは Jupyter でそのまま実行できます！**（`.scad` ファイルが書き出されます）\n\n"
       "> プログラミングと3Dが完全につながる、いちばん「理系」な作り方です。"),
    md("## 0. 準備\n\n"
       "**ライブラリのインストール**（このセルを実行）"),
    code("# uv環境なら: ターミナルで  uv pip install solidpython2\n"
         "# このノート内で入れるなら↓のコメントを外す\n"
         "# %pip install solidpython2\n"
         "from solid2 import polygon, rotate_extrude, cylinder, scad_render_to_file\n"
         "print('準備OK')"),
    md("`.scad` を**見る**には [OpenSCAD](https://openscad.org/)（無料）をインストールし、\n"
       "書き出したファイルを開きます。OpenSCADから `.stl` も書き出せます。"),
    shrink,
    md("## 1. 断面 → 回転体（rotate_extrude）\n\n"
       "考え方はFreeCAD・Blenderと同じ「回転体」。\n"
       "2Dの輪郭 `polygon` を `rotate_extrude` で360°回すと器になります。\n"
       "点は `(半径, 高さ)`。"),
    code("# 茶碗の断面（半径, 高さ）— 内側と外側を一周する閉じた輪郭\n"
         "profile = [\n"
         "    (0,  0), (45, 0), (45, 6),    # 底\n"
         "    (52, 68), (60, 70),           # 外壁→口の外\n"
         "    (54, 70), (47, 66),           # 口の内（肉厚）\n"
         "    (39, 8), (0, 8), (0, 0),      # 内壁→内側の底\n"
         "]\n\n"
         "chawan = rotate_extrude(angle=360, _fn=120)(polygon(points=profile))\n"
         "chawan.save_as_scad('chawan.scad')\n"
         "print('chawan.scad を書き出しました。OpenSCADで開いてね')"),
    md("`_fn=120` は「何角形で円を近似するか」。大きいほどなめらか（その分重い）。"),
    md("## 2. 関数にして、いろんな器を量産する\n\n"
       "プログラミングの強み＝**パラメータを変えるだけで何個でも作れる**こと。\n"
       "器の「口径・高さ・肉厚」を引数にした関数を作ります。"),
    code("def make_bowl(diameter=120, height=70, thickness=6, foot=33, fn=120):\n"
         "    r = diameter / 2\n"
         "    inner_r = r - thickness\n"
         "    profile = [\n"
         "        (0, 0), (r*0.75, 0), (r*0.75, thickness),\n"
         "        (r*0.9, height-2), (r, height),\n"
         "        (r-3, height), (inner_r*0.95, height-4),\n"
         "        (inner_r*0.6, thickness+2), (0, thickness+2), (0, 0),\n"
         "    ]\n"
         "    bowl = rotate_extrude(angle=360, _fn=fn)(polygon(points=profile))\n"
         "    return bowl\n\n"
         "# 焼き上がりサイズから収縮を逆算して設計\n"
         "shrink = 0.13\n"
         "yunomi = make_bowl(diameter=80/(1-shrink), height=90/(1-shrink), thickness=5)\n"
         "yunomi.save_as_scad('yunomi.scad')\n\n"
         "chawan = make_bowl(diameter=120/(1-shrink), height=70/(1-shrink), thickness=6)\n"
         "chawan.save_as_scad('chawan2.scad')\n"
         "print('湯のみ・茶碗を書き出しました')"),
    md("## 3. 高台をくり抜く（引き算）\n\n"
       "SolidPythonでは図形どうしを `+`（合体）`-`（くり抜き）で組み合わせられます。"),
    code("def add_foot(bowl, foot_d=66, foot_h=6, fn=120):\n"
         "    cutter = cylinder(d=foot_d, h=foot_h, _fn=fn)\n"
         "    return bowl - cutter   # 底をへこませて高台に\n\n"
         "chawan_kodai = add_foot(make_bowl())\n"
         "chawan_kodai.save_as_scad('chawan_kodai.scad')\n"
         "print('高台つきの茶碗を書き出しました')"),
    md("## 4. 書き出したファイルを確認"),
    code("import glob, os\n"
         "for f in sorted(glob.glob('*.scad')):\n"
         "    print(f, f'({os.path.getsize(f)} bytes)')"),
    md("---\n## 🏆 チャレンジ課題\n\n"
       "**課題1.** `make_bowl` を使って「小皿（口径150・高さ25・肉厚5）」を作ろう。\n\n"
       "**課題2.** for文で、口径を 80→160mm まで20mm刻みで変えた器を5個、\n"
       "`bowl_80.scad` … のように連番で書き出そう。\n\n"
       "**課題3.**（発展）`profile` を工夫して、口が花びらのように波打つ器に挑戦（ヒント：\n"
       "`rotate_extrude` の前に複数の山を作るのは難しいので、まず口径を変えた輪で重ねてみる）。\n\n"
       "**課題4.**（統計とつなぐ）課題2で作った5個の器の「容積のおよそ」を円柱で近似計算し、\n"
       "`02_統計` で習った平均・標準偏差を求めてみよう。"),
    code("# 課題1\n"),
    code("# 課題2\n"
         "for d in range(80, 161, 20):\n"
         "    pass  # ここに書く\n"),
    md("<details><summary>解答例</summary>\n\n"
       "```python\n"
       "make_bowl(diameter=150, height=25, thickness=5).save_as_scad('kozara.scad')\n\n"
       "for d in range(80, 161, 20):\n"
       "    make_bowl(diameter=d, height=d*0.6).save_as_scad(f'bowl_{d}.scad')\n"
       "```\n</details>\n\n"
       "🎉 **ホビー編クリア！** FreeCAD（精密）・Blender（自由曲面）・SolidPython（コード）の\n"
       "3つの作り方を体験しました。同じ「回転体」でも道具で得意分野が違うのが面白いところです。"),
]
write_nb("07_ホビー_陶芸3D/03_SolidPythonで器をつくる.ipynb", cells)

print("=== ホビー done ===")
