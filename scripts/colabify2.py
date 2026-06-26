import json, glob, re, os, html

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"

# データセット紹介（実データ先頭3行つき）
DATASET_INFO = {
 "students_scores": (
  "### 📋 使うデータ：`students_scores.csv`（架空の生徒120人の成績）\n"
  "1行＝生徒1人。数学・英語・国語は0〜100点、勉強時間は1日あたりの時間です。\n\n"
  "| 生徒ID | クラス | 数学 | 英語 | 国語 | 勉強時間 |\n"
  "|---|---|---|---|---|---|\n"
  "| S001 | A | 52 | 58 | 49 | 2.0 |\n"
  "| S002 | C | 80 | 79 | 74 | 3.4 |\n"
  "| S003 | B | 40 | 65 | 91 | 2.0 |\n\n"
  "（下のセルの `df.head()` で先頭5行を実際に確認できます）"),
 "weather": (
  "### 📋 使うデータ：`weather.csv`（2026年6月・30日間の天気）\n"
  "1行＝1日。気温(℃)と降水量(mm)。\n\n"
  "| 日付 | 気温 | 降水量 |\n|---|---|---|\n"
  "| 2026-06-01 | 19.2 | 5.9 |\n| 2026-06-02 | 23.2 | 0.0 |\n| 2026-06-03 | 22.2 | 4.5 |"),
 "sales_btob": (
  "### 📋 使うデータ：`sales_btob.csv`（架空のBtoB商談400件）\n"
  "1行＝商談1件。`受注`は 1=成約 / 0=失注。\n\n"
  "| 商談ID | 受注日 | 業界 | 獲得チャネル | 商談金額 | 担当者 | 受注 |\n"
  "|---|---|---|---|---|---|---|\n"
  "| D0001 | 2026-01-15 | 小売 | 紹介 | 1,211,000 | 佐藤 | 0 |\n"
  "| D0002 | 2026-02-05 | 医療 | テレアポ | 400,000 | 田中 | 0 |\n"
  "| D0003 | 2026-02-19 | IT | 紹介 | 542,000 | 高橋 | 1 |"),
 "web_marketing": (
  "### 📋 使うデータ：`web_marketing.csv`（月×チャネルのマーケ実績）\n"
  "1行＝ある月・あるチャネルの実績。表示→クリック→獲得 の数と費用(円)。\n\n"
  "| 月 | チャネル | 表示回数 | クリック数 | 獲得数 | 費用 |\n"
  "|---|---|---|---|---|---|\n"
  "| 2026-01 | 展示会 | 1855 | 149 | 22 | 4363 |\n"
  "| 2026-01 | Web広告 | 14854 | 532 | 26 | 39715 |\n"
  "| 2026-01 | メルマガ | 7258 | 294 | 16 | 1578 |"),
 "ab_test": (
  "### 📋 使うデータ：`ab_test.csv`（LPボタン色のA/Bテスト）\n"
  "1行＝訪問1件。`申込`は 1=申込んだ / 0=申込まず。グループは A_青ボタン / B_緑ボタン の2群（各2400件前後）。\n\n"
  "| グループ | 申込 |\n|---|---|\n"
  "| B_緑ボタン | 0 |\n| A_青ボタン | 0 |\n| B_緑ボタン | 1 |"),
}

def md(t): return {"cell_type":"markdown","metadata":{},"source":t}

def fence_to_pre(text):
    """<details>内の ```code``` を <pre><code> に変換（Colabで確実に表示・折りたたみ）"""
    def repl(m):
        inner = m.group(1)
        if inner.endswith("\n"): inner = inner[:-1]
        return ("<pre style=\"background:#f6f8fa;padding:10px;border-radius:6px;"
                "overflow:auto\"><code>" + html.escape(inner) + "</code></pre>")
    return re.sub(r"```[a-zA-Z0-9]*\n(.*?)```", repl, text, flags=re.DOTALL)

sol_n = data_n = 0
for p in sorted(glob.glob(f"{ROOT}/**/*.ipynb", recursive=True)):
    nb = json.load(open(p, encoding="utf-8"))
    cells = nb["cells"]

    # --- 1) 解答例: <details>内コードを<pre>化 + summary明確化 ---
    for c in cells:
        if c["cell_type"] != "markdown": continue
        s = "".join(c["source"])
        if "<details>" not in s: continue
        new = s
        if "```" in new:
            new = fence_to_pre(new)
        new = new.replace("<details><summary>", "<details>\n<summary>")
        new = re.sub(r"<summary>\s*(▶\s*)?解答例[^<]*</summary>",
                     "<summary>▶ 解答例を見る（クリックで開く）</summary>", new)
        if new != s:
            c["source"] = new; sol_n += 1

    # --- 2) データプレビュー: 最初のread_csvの直後に列説明+サンプルを挿入 ---
    if not any(c["cell_type"]=="markdown" and "📋 使うデータ" in "".join(c["source"]) for c in cells):
        first_read = None
        for i, c in enumerate(cells):
            if c["cell_type"]=="code" and "read_csv" in "".join(c["source"]):
                first_read = i; break
        if first_read is not None:
            used = []
            for c in cells:
                if c["cell_type"]=="code":
                    for name in re.findall(r"read_csv\(['\"]\.\./data/(\w+)\.csv", "".join(c["source"])):
                        if name in DATASET_INFO and name not in used:
                            used.append(name)
            if used:
                body = "\n\n---\n\n".join(DATASET_INFO[n] for n in used)
                cells.insert(first_read+1, md(body))
                data_n += 1
                print(f"  +preview {os.path.relpath(p,ROOT)} -> {used}")

    json.dump(nb, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"\n解答例セル整形: {sol_n}  /  データプレビュー挿入: {data_n}")
