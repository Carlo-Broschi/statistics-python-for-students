# -*- coding: utf-8 -*-
"""発展マーケ編で使うデータを生成（data/monthly_kpi.csv, data/btob_customers.csv）。"""
import numpy as np, pandas as pd

D = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python/data"
rng = np.random.default_rng(7)

# --- 月次KPI 36か月（トレンド＋季節性）---
months = pd.date_range("2023-01-01", periods=36, freq="MS")
t = np.arange(36)
seas = {1:0.95,2:0.93,3:1.05,4:1.0,5:0.98,6:0.9,7:0.88,8:0.9,9:1.05,10:1.1,11:1.15,12:1.3}
base = 800 + 14 * t
sales = (base * np.array([seas[m.month] for m in months]) * (1 + rng.normal(0,0.04,36))).round().astype(int)
leads = (sales * rng.uniform(0.9,1.1,36) / 10).round().astype(int)
won = (leads * rng.uniform(0.15,0.25,36)).round().astype(int)
pd.DataFrame({"月":months.strftime("%Y-%m"),"売上":sales,"新規リード":leads,"受注数":won}
            ).to_csv(f"{D}/monthly_kpi.csv", index=False, encoding="utf-8-sig")

# --- 顧客 320件（RFM用・潜在セグメント）---
inds = ["製造","IT","小売","医療","金融","建設"]
segs = [("優良",70,(6,12),(8e6,2.5e6),(0,60)),
        ("一般",120,(2,5),(2.5e6,1e6),(30,200)),
        ("新規",70,(1,2),(8e5,4e5),(0,40)),
        ("離反",60,(1,4),(1.5e6,8e5),(200,500))]
rows = []; cid = 1
for name,n,(fl,fh),(mm,ms),(rl,rh) in segs:
    for _ in range(n):
        f = rng.integers(fl, fh+1)
        m = max(1e5, rng.normal(mm, ms))
        r = rng.integers(rl, rh+1)
        last = pd.Timestamp("2026-01-01") - pd.Timedelta(days=int(r))
        rows.append([f"C{cid:04d}", rng.choice(inds), int(f), int(round(m,-3)), last.strftime("%Y-%m-%d"), name])
        cid += 1
cust = pd.DataFrame(rows, columns=["顧客ID","業界","購入回数","累計売上","最終購入日","（正解セグメント）"])
cust = cust.sample(frac=1, random_state=1).reset_index(drop=True)
cust.to_csv(f"{D}/btob_customers.csv", index=False, encoding="utf-8-sig")
print("monthly_kpi:", len(months), " customers:", len(cust))
