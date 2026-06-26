# -*- coding: utf-8 -*-
import json, glob, os
ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"

PAIRS = [
(r'''# === FreeCADのPythonコンソールに貼り付け ===
import FreeCAD as App
import Part
from FreeCAD import Vector

doc = App.newDocument('Chawan')

# 断面プロファイル (半径, 高さ) ※閉じた輪郭にする
pts = [
    Vector(0,   0, 0),   # 底の中心（外）
    Vector(45,  0, 0),   # 底の外ふち
    Vector(62, 70, 0),   # 口の外ふち（口が広がる）
    Vector(56, 70, 0),   # 口の内ふち → 肉厚6mm
    Vector(39,  8, 0),   # 見込み（内側の壁）
    Vector(0,   8, 0),   # 内側の底
    Vector(0,   0, 0),   # 閉じる
]

wire = Part.makePolygon(pts)
face = Part.Face(wire)
# Y軸(高さ方向)のまわりに360°回転
bowl = face.revolve(Vector(0,0,0), Vector(0,1,0), 360)

Part.show(bowl, 'Chawan')
doc.recompute()
# 全体を見る: メニュー 表示→標準ビュー→軸測 / マウスホイールでズーム''',
r'''# === FreeCADのPythonコンソールに貼り付け ===
import FreeCAD as App        # FreeCAD本体
import Part                  # 立体（パート）を作るモジュール
from FreeCAD import Vector   # 3D座標 (x, y, z)

doc = App.newDocument('Chawan')   # 新しいドキュメントを作る

# 断面プロファイル (半径, 高さ) ※閉じた輪郭にする
pts = [
    Vector(0,   0, 0),   # 底の中心（外）
    Vector(45,  0, 0),   # 底の外ふち
    Vector(62, 70, 0),   # 口の外ふち（口が広がる）
    Vector(56, 70, 0),   # 口の内ふち → 肉厚6mm
    Vector(39,  8, 0),   # 見込み（内側の壁）
    Vector(0,   8, 0),   # 内側の底
    Vector(0,   0, 0),   # 閉じる
]

wire = Part.makePolygon(pts)   # 点をつないだ輪郭線（ワイヤ）
face = Part.Face(wire)         # 輪郭を面にする
# Y軸(高さ方向)のまわりに360°回転
bowl = face.revolve(Vector(0,0,0), Vector(0,1,0), 360)   # 面を回して立体（器）に

Part.show(bowl, 'Chawan')      # 画面に表示
doc.recompute()                # 再計算して反映
# 全体を見る: メニュー 表示→標準ビュー→軸測 / マウスホイールでズーム'''),
(r'''# 底をへこませて高台をつくる（コンソールに追記）
cut = Part.makeCylinder(33, 6, Vector(0,0,0), Vector(0,1,0))
chawan_with_foot = bowl.cut(cut)
Part.show(chawan_with_foot, 'Chawan_kodai')
doc.recompute()''',
r'''# 底をへこませて高台をつくる（コンソールに追記）
cut = Part.makeCylinder(33, 6, Vector(0,0,0), Vector(0,1,0))   # くり抜く円柱（半径33・高さ6）
chawan_with_foot = bowl.cut(cut)             # 器から円柱を引き算
Part.show(chawan_with_foot, 'Chawan_kodai')  # 表示
doc.recompute()                              # 再計算'''),
(r'''# 書き出し（パスは自分の環境に合わせて）
bowl.exportStl('/Users/あなた/Desktop/chawan.stl')
print('保存しました')''',
r'''# 書き出し（パスは自分の環境に合わせて）
bowl.exportStl('/Users/あなた/Desktop/chawan.stl')   # STL形式で保存（3Dプリンタ用）
print('保存しました')'''),
# Blender
(r'''# === BlenderのScriptingタブに貼り付け ===
import bpy, bmesh, math

# 既存オブジェクトを消す
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# 花瓶の輪郭 (半径, 高さ) ※下から上へ。膨らみとくびれ
profile = [
    (20, 0), (40, 4), (55, 30), (50, 60),   # 下半分がふくらむ
    (30, 90), (28, 110), (40, 130), (38, 140) # 上でくびれて口が開く
]

mesh = bpy.data.meshes.new('Vase')
obj = bpy.data.objects.new('Vase', mesh)
bpy.context.collection.objects.link(obj)

bm = bmesh.new()
verts = [bm.verts.new((r, 0, h)) for r, h in profile]
edges = [bm.edges.new((verts[i], verts[i+1])) for i in range(len(verts)-1)]

# Z軸まわりに360°回す（64分割でなめらかに）
geom = verts + edges
bmesh.ops.spin(bm, geom=geom, cent=(0,0,0), axis=(0,0,1),
               angle=math.radians(360), steps=64)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
bm.to_mesh(mesh)
bm.free()''',
r'''# === BlenderのScriptingタブに貼り付け ===
import bpy, bmesh, math      # bpy=Blender操作, bmesh=メッシュ編集, math=数学

# 既存オブジェクトを消す
bpy.ops.object.select_all(action='SELECT')   # 全オブジェクトを選択
bpy.ops.object.delete()                       # 削除

# 花瓶の輪郭 (半径, 高さ) ※下から上へ。膨らみとくびれ
profile = [
    (20, 0), (40, 4), (55, 30), (50, 60),   # 下半分がふくらむ
    (30, 90), (28, 110), (40, 130), (38, 140) # 上でくびれて口が開く
]

mesh = bpy.data.meshes.new('Vase')            # 空のメッシュを作る
obj = bpy.data.objects.new('Vase', mesh)      # メッシュを持つオブジェクト
bpy.context.collection.objects.link(obj)      # シーンに追加

bm = bmesh.new()                              # 編集用のメッシュ
verts = [bm.verts.new((r, 0, h)) for r, h in profile]   # 輪郭の各点を頂点にする
edges = [bm.edges.new((verts[i], verts[i+1])) for i in range(len(verts)-1)]  # 隣どうしを線で結ぶ

# Z軸まわりに360°回す（64分割でなめらかに）
geom = verts + edges                          # 回す対象（頂点と辺）
bmesh.ops.spin(bm, geom=geom, cent=(0,0,0), axis=(0,0,1),
               angle=math.radians(360), steps=64)        # 回転体にする
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001) # 重なった頂点を結合
bm.to_mesh(mesh)                              # 編集結果をメッシュに反映
bm.free()                                     # 後片付け'''),
(r'''# 厚み(肉厚)をつける Solidify モディファイア
solid = obj.modifiers.new('thick', 'SOLIDIFY')
solid.thickness = 5   # 肉厚5mm

# 表面をなめらかにする
for p in mesh.polygons:
    p.use_smooth = True
subsurf = obj.modifiers.new('smooth', 'SUBSURF')
subsurf.levels = 2

print('花瓶ができました！ テンキー1で正面、マウス中ボタンで回転')''',
r'''# 厚み(肉厚)をつける Solidify モディファイア
solid = obj.modifiers.new('thick', 'SOLIDIFY')   # 厚みを足す機能を追加
solid.thickness = 5   # 肉厚5mm

# 表面をなめらかにする
for p in mesh.polygons:           # すべての面を
    p.use_smooth = True           # なめらか表示にする
subsurf = obj.modifiers.new('smooth', 'SUBSURF')   # 細分化でさらになめらかに
subsurf.levels = 2                # 細かさのレベル

print('花瓶ができました！ テンキー1で正面、マウス中ボタンで回転')'''),
(r'''# STLで書き出し（パスは自分用に変更）
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.ops.wm.stl_export(filepath='/Users/あなた/Desktop/vase.stl',
                      export_selected_objects=True)''',
r'''# STLで書き出し（パスは自分用に変更）
bpy.ops.object.select_all(action='DESELECT')   # いったん選択を解除
obj.select_set(True)                            # 花瓶だけ選択
bpy.ops.wm.stl_export(filepath='/Users/あなた/Desktop/vase.stl',   # STLで保存
                      export_selected_objects=True)'''),
# SolidPython
(r'''# uv環境なら: ターミナルで  uv pip install solidpython2
# このノート内で入れるなら↓のコメントを外す
# %pip install solidpython2
from solid2 import polygon, rotate_extrude, cylinder, scad_render_to_file
print('準備OK')''',
r'''# uv環境なら: ターミナルで  uv pip install solidpython2
# このノート内で入れるなら↓のコメントを外す
# %pip install solidpython2
from solid2 import polygon, rotate_extrude, cylinder, scad_render_to_file   # 使う機能を読み込む
print('準備OK')'''),
(r'''# 茶碗の断面（半径, 高さ）— 内側と外側を一周する閉じた輪郭
profile = [
    (0,  0), (45, 0), (45, 6),    # 底
    (52, 68), (60, 70),           # 外壁→口の外
    (54, 70), (47, 66),           # 口の内（肉厚）
    (39, 8), (0, 8), (0, 0),      # 内壁→内側の底
]

chawan = rotate_extrude(angle=360, _fn=120)(polygon(points=profile))
chawan.save_as_scad('chawan.scad')
print('chawan.scad を書き出しました。OpenSCADで開いてね')''',
r'''# 茶碗の断面（半径, 高さ）— 内側と外側を一周する閉じた輪郭
profile = [
    (0,  0), (45, 0), (45, 6),    # 底
    (52, 68), (60, 70),           # 外壁→口の外
    (54, 70), (47, 66),           # 口の内（肉厚）
    (39, 8), (0, 8), (0, 0),      # 内壁→内側の底
]

chawan = rotate_extrude(angle=360, _fn=120)(polygon(points=profile))   # 断面を360°回して器に
chawan.save_as_scad('chawan.scad')        # OpenSCAD形式(.scad)で保存
print('chawan.scad を書き出しました。OpenSCADで開いてね')'''),
(r'''def make_bowl(diameter=120, height=70, thickness=6, foot=33, fn=120):
    r = diameter / 2
    inner_r = r - thickness
    profile = [
        (0, 0), (r*0.75, 0), (r*0.75, thickness),
        (r*0.9, height-2), (r, height),
        (r-3, height), (inner_r*0.95, height-4),
        (inner_r*0.6, thickness+2), (0, thickness+2), (0, 0),
    ]
    bowl = rotate_extrude(angle=360, _fn=fn)(polygon(points=profile))
    return bowl

# 焼き上がりサイズから収縮を逆算して設計
shrink = 0.13
yunomi = make_bowl(diameter=80/(1-shrink), height=90/(1-shrink), thickness=5)
yunomi.save_as_scad('yunomi.scad')

chawan = make_bowl(diameter=120/(1-shrink), height=70/(1-shrink), thickness=6)
chawan.save_as_scad('chawan2.scad')
print('湯のみ・茶碗を書き出しました')''',
r'''# 口径・高さ・肉厚を指定して器を作る関数
def make_bowl(diameter=120, height=70, thickness=6, foot=33, fn=120):
    r = diameter / 2                       # 外側の半径
    inner_r = r - thickness                # 内側の半径
    profile = [                            # 断面の輪郭（半径, 高さ）を組み立てる
        (0, 0), (r*0.75, 0), (r*0.75, thickness),
        (r*0.9, height-2), (r, height),
        (r-3, height), (inner_r*0.95, height-4),
        (inner_r*0.6, thickness+2), (0, thickness+2), (0, 0),
    ]
    bowl = rotate_extrude(angle=360, _fn=fn)(polygon(points=profile))   # 回転体にする
    return bowl                            # 器を返す

# 焼き上がりサイズから収縮を逆算して設計
shrink = 0.13                              # 収縮率13%
yunomi = make_bowl(diameter=80/(1-shrink), height=90/(1-shrink), thickness=5)   # 湯のみ
yunomi.save_as_scad('yunomi.scad')         # 保存

chawan = make_bowl(diameter=120/(1-shrink), height=70/(1-shrink), thickness=6)  # 茶碗
chawan.save_as_scad('chawan2.scad')        # 保存
print('湯のみ・茶碗を書き出しました')'''),
(r'''def add_foot(bowl, foot_d=66, foot_h=6, fn=120):
    cutter = cylinder(d=foot_d, h=foot_h, _fn=fn)
    return bowl - cutter   # 底をへこませて高台に

chawan_kodai = add_foot(make_bowl())
chawan_kodai.save_as_scad('chawan_kodai.scad')
print('高台つきの茶碗を書き出しました')''',
r'''# 器の底に高台（こうだい）をくり抜く関数
def add_foot(bowl, foot_d=66, foot_h=6, fn=120):
    cutter = cylinder(d=foot_d, h=foot_h, _fn=fn)   # くり抜く円柱
    return bowl - cutter   # 底をへこませて高台に

chawan_kodai = add_foot(make_bowl())       # 高台つきの茶碗を作る
chawan_kodai.save_as_scad('chawan_kodai.scad')   # 保存
print('高台つきの茶碗を書き出しました')'''),
(r'''import glob, os
for f in sorted(glob.glob('*.scad')):
    print(f, f'({os.path.getsize(f)} bytes)')''',
r'''import glob, os                            # ファイル一覧と情報を扱う
# 書き出した .scad ファイルを一覧表示
for f in sorted(glob.glob('*.scad')):
    print(f, f'({os.path.getsize(f)} bytes)')   # ファイル名とサイズ'''),
(r'''# 課題2
for d in range(80, 161, 20):
    pass  # ここに書く''',
r'''# 課題2
for d in range(80, 161, 20):   # 口径80〜160mmを20mm刻みで
    pass  # ここに書く'''),
]

MAP = {k.strip(): v for k, v in PAIRS}
replaced = 0; unmatched = []
for p in sorted(glob.glob(f"{ROOT}/07_ホビー_陶芸3D/*.ipynb")):
    nb = json.load(open(p, encoding="utf-8")); changed = False
    for c in nb["cells"]:
        if c["cell_type"] != "code": continue
        j = "".join(c["source"]); key = j.strip()
        if "① セットアップ" in j: continue
        if key in MAP:
            if j != MAP[key]: c["source"] = MAP[key]; changed = True; replaced += 1
        else:
            body = [l for l in j.splitlines() if l.strip() and not l.strip().startswith("#")]
            if body: unmatched.append((os.path.basename(p), j.splitlines()[0][:46]))
    if changed:
        json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("replaced:", replaced, " unmatched:", len(unmatched))
for u in unmatched: print("  ", u)
