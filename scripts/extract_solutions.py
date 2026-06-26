# -*- coding: utf-8 -*-
import json, glob, os, re, html, urllib.parse

ROOT = "/Users/carlobroschi_imac/Workspace/Dev/Education_Python"
GH = "https://github.com/Carlo-Broschi/statistics-python-for-students/blob/main/"
ANSDIR = "解答集"

def pre_to_fence(m):
    code = html.unescape(m.group(1))
    return "```python\n" + code + "\n```"

def details_to_md(block):
    # <details>…</details> の中身を、表示用のmarkdownに変換
    s = block
    s = re.sub(r"</?details>", "", s)
    s = re.sub(r"<summary>.*?</summary>", "", s, flags=re.DOTALL)
    s = re.sub(r'<pre[^>]*><code>(.*?)</code></pre>', pre_to_fence, s, flags=re.DOTALL)
    return s.strip()

index_lines = ["# 解答集\n",
               "各ノートの練習問題の解答例をまとめています（ネタバレ防止のため本編ノートとは分離）。\n"]
made = 0
for p in sorted(glob.glob(f"{ROOT}/**/*.ipynb", recursive=True)):
    rel = os.path.relpath(p, ROOT)
    nb = json.load(open(p, encoding="utf-8"))
    name = os.path.splitext(os.path.basename(p))[0]
    folder = os.path.dirname(rel)
    ans_rel = f"{ANSDIR}/{folder}/{name}.md" if folder else f"{ANSDIR}/{name}.md"
    ans_abs = os.path.join(ROOT, ans_rel)
    ans_url = GH + urllib.parse.quote(ans_rel)

    answers = []
    changed = False
    for c in nb["cells"]:
        if c["cell_type"] != "markdown":
            continue
        src = "".join(c["source"])
        if "<details>" not in src:
            continue
        # cell内の <details>…</details> を抜き出して、本文側はリンクに置換
        blocks = re.findall(r"<details>.*?</details>", src, flags=re.DOTALL)
        for b in blocks:
            answers.append(details_to_md(b))
        pointer = (f"> 🔑 **解答例は別ページにまとめています**（ネタバレ防止）。\n"
                   f"> 自分で解いてから 👉 **[{name} の解答例を開く]({ans_url})**")
        new_src = re.sub(r"<details>.*?</details>", pointer, src, flags=re.DOTALL)
        if new_src != src:
            c["source"] = new_src
            changed = True

    if answers:
        os.makedirs(os.path.dirname(ans_abs), exist_ok=True)
        body = (f"# {name} ― 解答例\n\n"
                f"> 出典ノート: `{rel}`　／　[本編ノートを開く]({GH + urllib.parse.quote(rel)})\n\n"
                + "\n\n---\n\n".join(answers) + "\n")
        open(ans_abs, "w", encoding="utf-8").write(body)
        index_lines.append(f"- [{name}]({urllib.parse.quote(f'{folder}/{name}.md' if folder else f'{name}.md')}) — `{folder}`")
        made += 1
    if changed:
        json.dump(nb, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

open(os.path.join(ROOT, ANSDIR, "README.md"), "w", encoding="utf-8").write("\n".join(index_lines) + "\n")
print(f"解答ファイル作成: {made}  / 索引: {ANSDIR}/README.md")
