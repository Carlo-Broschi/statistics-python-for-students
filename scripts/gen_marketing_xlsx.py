# -*- coding: utf-8 -*-
"""マーケ系CSVを1つのExcelブック（複数シート）にまとめる。data/marketing.xlsx を生成。"""
import pandas as pd

D = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python/data"
sheets = {
    "商談":     "sales_btob.csv",
    "Webマーケ": "web_marketing.csv",
    "ABテスト":  "ab_test.csv",
    "月次KPI":   "monthly_kpi.csv",
    "顧客":      "btob_customers.csv",
}
with pd.ExcelWriter(f"{D}/marketing.xlsx", engine="openpyxl") as xw:
    for sheet, csv in sheets.items():
        pd.read_csv(f"{D}/{csv}").to_excel(xw, sheet_name=sheet, index=False)
print("wrote data/marketing.xlsx with sheets:", list(sheets))
