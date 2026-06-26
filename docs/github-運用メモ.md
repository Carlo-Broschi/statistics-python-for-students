# GitHub 運用メモ（このリポジトリの更新・管理コマンド集）

このリポジトリ（`Carlo-Broschi/statistics-python-for-students`）を更新・管理するための実コマンドです。
GitHub操作は専用スクリプトを作らず、`git` と GitHub API(`curl`) を直接使っています。

## 前提
- リモート `origin` は設定済み（HTTPS）。`git remote -v` で確認。
- 認証トークンは環境変数 **`GITHUB_PERSONAL_ACCESS_TOKEN`**（fine-grained PAT）にある。**`.git/config` には保存していない**。
- コミット作者メールはローカル設定で GitHub の noreply に固定済み（個人Gmailを出さない）。
- このトークンの権限：**push / 閲覧は可。リポジトリ新規作成・公開設定の変更は不可**（その2つは Web UI で行う）。

---

## ① いちばん使う：変更を push
```bash
cd ~/Workspace/Dev/Education_Python
git add -A
git commit -m "変更内容のメッセージ"
git -c credential.helper='!f(){ echo username=x-access-token; echo "password=$GITHUB_PERSONAL_ACCESS_TOKEN"; }; f' push origin main
```
- credential.helper にトークンを一時供給する方式。**URLや設定にトークンを残さない**。
- 毎回打つのが面倒なら、シェルにエイリアス／関数を入れてもよい（例）:
  ```bash
  ghpush() { git -c credential.helper='!f(){ echo username=x-access-token; echo "password=$GITHUB_PERSONAL_ACCESS_TOKEN"; }; f' push "$@"; }
  ```

## ② 状態を確認する
```bash
# 認証できているユーザー
curl -s -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user

# リポジトリの公開状態・デフォルトブランチ
curl -s -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  https://api.github.com/repos/Carlo-Broschi/statistics-python-for-students

# 直近コミット（作者メールがnoreplyか確認するのにも使える）
curl -s -H "Authorization: Bearer $GITHUB_PERSONAL_ACCESS_TOKEN" \
  "https://api.github.com/repos/Carlo-Broschi/statistics-python-for-students/commits?per_page=1"
```

## ③ コミット履歴のメールを秘匿（公開前の1回だけ・実施済み）
> ⚠️ 履歴の書き換え＝force push。共同作業者がいるとトラブルになる。**通常は不要**（今後のコミットは②の設定で自動的にnoreply）。
```bash
git config user.email "59012768+Carlo-Broschi@users.noreply.github.com"   # 今後のコミット用
git filter-branch -f --env-filter \
  "export GIT_AUTHOR_EMAIL='59012768+Carlo-Broschi@users.noreply.github.com'; \
   export GIT_COMMITTER_EMAIL='59012768+Carlo-Broschi@users.noreply.github.com'" -- --all
git -c credential.helper='!f(){ echo username=x-access-token; echo "password=$GITHUB_PERSONAL_ACCESS_TOKEN"; }; f' push --force origin main
```

## ④ このトークンでは「できない」操作 → Web UI で行う
| やりたいこと | 方法 |
|---|---|
| 新しいリポジトリを作る | https://github.com/new （Private/Public・README無しで作成 → 上記①でpush） |
| Private ⇄ Public を切り替える | リポジトリ **Settings → 最下部 Danger Zone → Change repository visibility**（確認のためリポジトリ名の入力が必要） |
| 共同作業者を招待 | Settings → Collaborators |

## トラブルシュート
- `Could not resolve host: github.com`：一時的なネットワーク/DNS。**そのまま再実行**で通ることが多い。
- push が認証で弾かれる：`echo ${#GITHUB_PERSONAL_ACCESS_TOKEN}` でトークンが空でないか確認。`curl .../user` で有効性を確認。
- 「Resource not accessible by personal access token」：そのトークンの権限外（③の作成・可視性変更など）。Web UI で行う。

## Colabリンクの作り方（共有用）
ノートのColab URL は次の形（パスはURLエンコード）:
```
https://colab.research.google.com/github/Carlo-Broschi/statistics-python-for-students/blob/main/<ノートのパス>
```
Public公開済みなので、相手は Google アカウントだけで開ける（GitHubアカウント不要）。
