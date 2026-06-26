import numpy as np
import pandas as pd

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python/data"
rng = np.random.default_rng(42)

# --- 1. 生徒のテスト点数 -------------------------------------------------
n = 120
classes = rng.choice(["A", "B", "C"], size=n)
math = np.clip(rng.normal(65, 15, n), 0, 100).round().astype(int)
# 英語は数学と相関を持たせる
english = np.clip(0.6 * math + rng.normal(28, 10, n), 0, 100).round().astype(int)
japanese = np.clip(rng.normal(70, 12, n), 0, 100).round().astype(int)
study_hours = np.clip(rng.normal(1.5, 0.8, n) + math / 100, 0, None).round(1)
students = pd.DataFrame({
    "生徒ID": [f"S{i:03d}" for i in range(1, n + 1)],
    "クラス": classes,
    "数学": math,
    "英語": english,
    "国語": japanese,
    "勉強時間": study_hours,
})
students.to_csv(f"{ROOT}/students_scores.csv", index=False, encoding="utf-8-sig")

# --- 2. 1か月の天気 ------------------------------------------------------
days = pd.date_range("2026-06-01", periods=30, freq="D")
temp = (24 + 4 * np.sin(np.arange(30) / 5) + rng.normal(0, 2, 30)).round(1)
rain = np.clip(rng.gamma(1.2, 4, 30) * (rng.random(30) < 0.4), 0, None).round(1)
weather = pd.DataFrame({"日付": days.strftime("%Y-%m-%d"), "気温": temp, "降水量": rain})
weather.to_csv(f"{ROOT}/weather.csv", index=False, encoding="utf-8-sig")

# --- 3. BtoB 商談データ（マーケ実践用） ----------------------------------
m = 400
industries = ["製造", "IT", "小売", "医療", "金融", "建設"]
channels = ["展示会", "Web広告", "メルマガ", "紹介", "テレアポ"]
ind = rng.choice(industries, m, p=[.25, .2, .18, .12, .15, .1])
ch = rng.choice(channels, m, p=[.2, .3, .2, .15, .15])
deal_size = (rng.lognormal(13, 0.7, m)).round(-3).astype(int)  # 数十万〜数百万円
# チャネルごとに受注率を変える
ch_winrate = {"展示会": .35, "Web広告": .18, "メルマガ": .12, "紹介": .45, "テレアポ": .15}
won = np.array([rng.random() < ch_winrate[c] for c in ch])
dates = pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 180, m), unit="D")
btob = pd.DataFrame({
    "商談ID": [f"D{i:04d}" for i in range(1, m + 1)],
    "受注日": dates.strftime("%Y-%m-%d"),
    "業界": ind,
    "獲得チャネル": ch,
    "商談金額": deal_size,
    "担当者": rng.choice(["田中", "鈴木", "佐藤", "高橋"], m),
    "受注": won.astype(int),
})
btob.to_csv(f"{ROOT}/sales_btob.csv", index=False, encoding="utf-8-sig")

# --- 4. Webマーケのファネルデータ（月×チャネル） ------------------------
months = pd.date_range("2026-01-01", periods=6, freq="MS").strftime("%Y-%m")
rows = []
base = {"展示会": 2000, "Web広告": 12000, "メルマガ": 6000, "紹介": 800, "テレアポ": 1500}
ctr = {"展示会": .08, "Web広告": .03, "メルマガ": .05, "紹介": .2, "テレアポ": .12}
cvr = {"展示会": .12, "Web広告": .04, "メルマガ": .06, "紹介": .25, "テレアポ": .09}
cpc = {"展示会": 30, "Web広告": 80, "メルマガ": 5, "紹介": 0, "テレアポ": 200}
for mo in months:
    for c in channels:
        imp = int(base[c] * rng.uniform(0.8, 1.3))
        clk = int(imp * ctr[c] * rng.uniform(0.8, 1.2))
        cv = int(clk * cvr[c] * rng.uniform(0.7, 1.3))
        cost = int(clk * cpc[c] * rng.uniform(0.9, 1.1))
        rows.append([mo, c, imp, clk, cv, cost])
funnel = pd.DataFrame(rows, columns=["月", "チャネル", "表示回数", "クリック数", "獲得数", "費用"])
funnel.to_csv(f"{ROOT}/web_marketing.csv", index=False, encoding="utf-8-sig")

# --- 5. A/Bテスト（LPの申込ボタン色） ------------------------------------
ab_rows = []
for grp, p, size in [("A_青ボタン", 0.082, 2400), ("B_緑ボタン", 0.104, 2380)]:
    conv = rng.random(size) < p
    for c in conv:
        ab_rows.append([grp, int(c)])
ab = pd.DataFrame(ab_rows, columns=["グループ", "申込"])
ab = ab.sample(frac=1, random_state=1).reset_index(drop=True)
ab.to_csv(f"{ROOT}/ab_test.csv", index=False, encoding="utf-8-sig")

for f in ["students_scores", "weather", "sales_btob", "web_marketing", "ab_test"]:
    print(f, "ok")
