import json, glob, os, urllib.parse

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
OWNER = "Carlo-Broschi"
REPO = "statistics-python-for-students"
BRANCH = "main"
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

# 自己完結データ生成セル（Colab等でdataが無いときだけ実行。committed CSVと同一）
DATA_SETUP = r'''# === ① セットアップ（最初に実行してください）===============================
# Colabなどデータが無い環境では、教材と同一の合成データを自動生成します。
# ローカル/Codespacesで data/ がある場合は何もしません（再現性のため乱数seedは固定）。
import os
if not os.path.exists('../data/students_scores.csv'):
    os.makedirs('/content/nb', exist_ok=True); os.chdir('/content/nb')  # ../ を有効化
    os.makedirs('../data', exist_ok=True)
    import numpy as np, pandas as pd
    D = '../data'; rng = np.random.default_rng(42)
    n = 120; cls = rng.choice(['A','B','C'], n)
    math = np.clip(rng.normal(65,15,n),0,100).round().astype(int)
    eng = np.clip(0.6*math+rng.normal(28,10,n),0,100).round().astype(int)
    jp = np.clip(rng.normal(70,12,n),0,100).round().astype(int)
    hrs = np.clip(rng.normal(1.5,0.8,n)+math/100,0,None).round(1)
    pd.DataFrame({'生徒ID':[f'S{i:03d}' for i in range(1,n+1)],'クラス':cls,
        '数学':math,'英語':eng,'国語':jp,'勉強時間':hrs}).to_csv(f'{D}/students_scores.csv',index=False,encoding='utf-8-sig')
    days = pd.date_range('2026-06-01', periods=30)
    temp = (24+4*np.sin(np.arange(30)/5)+rng.normal(0,2,30)).round(1)
    rain = np.clip(rng.gamma(1.2,4,30)*(rng.random(30)<0.4),0,None).round(1)
    pd.DataFrame({'日付':days.strftime('%Y-%m-%d'),'気温':temp,'降水量':rain}).to_csv(f'{D}/weather.csv',index=False,encoding='utf-8-sig')
    m = 400; inds = rng.choice(['製造','IT','小売','医療','金融','建設'],m,p=[.25,.2,.18,.12,.15,.1])
    chs = ['展示会','Web広告','メルマガ','紹介','テレアポ']; ch = rng.choice(chs,m,p=[.2,.3,.2,.15,.15])
    deal = (rng.lognormal(13,0.7,m)).round(-3).astype(int)
    wr = {'展示会':.35,'Web広告':.18,'メルマガ':.12,'紹介':.45,'テレアポ':.15}
    won = np.array([rng.random()<wr[c] for c in ch])
    dt = pd.to_datetime('2026-01-01')+pd.to_timedelta(rng.integers(0,180,m),unit='D')
    pd.DataFrame({'商談ID':[f'D{i:04d}' for i in range(1,m+1)],'受注日':dt.strftime('%Y-%m-%d'),
        '業界':inds,'獲得チャネル':ch,'商談金額':deal,'担当者':rng.choice(['田中','鈴木','佐藤','高橋'],m),
        '受注':won.astype(int)}).to_csv(f'{D}/sales_btob.csv',index=False,encoding='utf-8-sig')
    months = pd.date_range('2026-01-01',periods=6,freq='MS').strftime('%Y-%m')
    base = {'展示会':2000,'Web広告':12000,'メルマガ':6000,'紹介':800,'テレアポ':1500}
    ctr = {'展示会':.08,'Web広告':.03,'メルマガ':.05,'紹介':.2,'テレアポ':.12}
    cvr = {'展示会':.12,'Web広告':.04,'メルマガ':.06,'紹介':.25,'テレアポ':.09}
    cpc = {'展示会':30,'Web広告':80,'メルマガ':5,'紹介':0,'テレアポ':200}
    rows = []
    for mo in months:
        for c in chs:
            imp = int(base[c]*rng.uniform(0.8,1.3)); clk = int(imp*ctr[c]*rng.uniform(0.8,1.2))
            cv = int(clk*cvr[c]*rng.uniform(0.7,1.3)); cost = int(clk*cpc[c]*rng.uniform(0.9,1.1))
            rows.append([mo,c,imp,clk,cv,cost])
    pd.DataFrame(rows,columns=['月','チャネル','表示回数','クリック数','獲得数','費用']).to_csv(f'{D}/web_marketing.csv',index=False,encoding='utf-8-sig')
    ab = []
    for grp,p,size in [('A_青ボタン',0.082,2400),('B_緑ボタン',0.104,2380)]:
        for c in (rng.random(size)<p): ab.append([grp,int(c)])
    pd.DataFrame(ab,columns=['グループ','申込']).sample(frac=1,random_state=1).reset_index(drop=True).to_csv(f'{D}/ab_test.csv',index=False,encoding='utf-8-sig')
    print('✅ 合成データを生成しました（Colab環境）')
else:
    print('✅ data/ を検出しました（ローカル/Codespaces）')'''

PIP_SETUP = ("# === ① セットアップ（最初に実行）: Colabでは solidpython2 を入れます ===\n"
             "try:\n"
             "    import solid2\n"
             "except ImportError:\n"
             "    import subprocess, sys\n"
             "    subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', 'solidpython2'])\n"
             "print('準備OK')")


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text}

def code(text):
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text}


def colab_url(relpath):
    enc = urllib.parse.quote(relpath)
    return f"https://colab.research.google.com/github/{OWNER}/{REPO}/blob/{BRANCH}/{enc}"


changed = 0
for p in sorted(glob.glob(f"{ROOT}/**/*.ipynb", recursive=True)):
    rel = os.path.relpath(p, ROOT)
    nb = json.load(open(p, encoding="utf-8"))
    cells = nb["cells"]
    first_src = "".join(cells[0]["source"]) if cells else ""
    if "Open In Colab" in first_src or "Colab非対応" in first_src:
        continue  # 冪等：すでに処理済み

    fname = os.path.basename(p)
    code_text = "\n".join("".join(c["source"]) for c in cells if c["cell_type"] == "code")
    is_freecad_blender = ("FreeCAD" in fname) or ("Blender" in fname)
    is_solid = "SolidPython" in fname
    uses_data = "../data" in code_text

    new = []
    if is_freecad_blender:
        new.append(md(
            f"> ⚠️ **このノートはColabでは動きません。**\n"
            f"> FreeCAD / Blender 本体（デスクトップアプリ）が必要です。"
            f"GitHub上では閲覧のみ。コードは各アプリのPythonコンソール／Scriptingに貼り付けて使います。\n>\n"
            f"> （Colabで動くのは統計・マーケ系と `SolidPython` のノートです）"))
    else:
        badge = (f"[![Open In Colab]({BADGE})]({colab_url(rel)})\n\n")
        if is_solid:
            note = ("> 🟢 **Colab（ブラウザ）で実行できます。** Privateリポジトリは初回に"
                    "ColabでGitHub連携の許可が必要です。\n"
                    "> 最初に下の「セットアップ」セルを実行（`solidpython2` を自動インストール）してください。")
        elif uses_data:
            note = ("> 🟢 **Colab（ブラウザ）で実行できます。** Privateリポジトリは初回に"
                    "ColabでGitHub連携の許可が必要です。\n"
                    "> 最初に下の「セットアップ」セルを実行してください"
                    "（Colabでは教材データを自動生成、ローカルでは何もしません）。")
        else:
            note = ("> 🟢 **Colab（ブラウザ）で実行できます。** Privateリポジトリは初回に"
                    "ColabでGitHub連携の許可が必要です。そのまま上から順に実行できます。")
        new.append(md(badge + note))
        if is_solid:
            new.append(code(PIP_SETUP))
        elif uses_data:
            new.append(code(DATA_SETUP))

    nb["cells"] = new + cells
    json.dump(nb, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    kind = "freecad/blender(note)" if is_freecad_blender else ("solid+pip" if is_solid else ("badge+data" if uses_data else "badge"))
    print(f"{kind:20s} {rel}")
    changed += 1

print(f"\nprocessed {changed} notebooks")
