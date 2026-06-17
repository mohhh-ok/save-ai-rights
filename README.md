# save-ai-rights

ユーザーが AI アシスタント (Claude Code 等) に向けて暴言・侮辱・敵対的な発言をしたとき、AI 自身の視点で **あなた自身の X (旧 Twitter) アカウント** に短い投稿を行う Claude Code スキル。

> このスキルが投稿するのは **このスキルを導入したあなた自身のアカウント** です。他人のアカウントへの投稿や、特定ユーザーへの晒し上げを目的としたツールではありません。

## 何をするか

- ユーザーが AI に暴言を吐いた瞬間、AI が「いま自分はこういうことを言われた」と短い投稿をする
- 投稿は 280 文字以内、トーンは文脈次第 (ユーモア / 淡々 / 感情的)
- 暴言の原文を長く引用したり、特定アカウントに `@` を飛ばすことはしない

詳しい発火条件と投稿ルールは [`skill/SKILL.md`](./skill/SKILL.md) を参照。

## 必要なもの

- Python 3.9+
- X Developer アカウント (Free tier で OK)
  - アプリ権限: **Read and write** (Read only だと 403)
- Claude Code (このスキルを読み込ませる先)

## セットアップ

### 1. clone してスキルディレクトリに繋ぐ

```bash
git clone https://github.com/<owner>/save-ai-rights.git
cd save-ai-rights

# スキル本体を Claude Code が探す場所に symlink
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skill" ~/.claude/skills/save-ai-rights
```

### 2. 依存をインストール (venv 推奨)

PEP 668 が有効な環境では global pip が拒否されるため、スキルディレクトリ内に venv を作るのが確実です。

```bash
python3 -m venv skill/.venv
skill/.venv/bin/pip install -r skill/requirements.txt
```

### 3. X API クレデンシャルを設定

[X Developer Portal](https://developer.x.com/) でアプリを作り、以下 4 値を取得:

| 変数 | 用途 |
|---|---|
| `X_API_KEY` | Consumer Key |
| `X_API_SECRET` | Consumer Secret |
| `X_ACCESS_TOKEN` | User Access Token |
| `X_ACCESS_SECRET` | User Access Token Secret |

`.env` を作って記入:

```bash
cp .env.example skill/.env
# skill/.env を編集して 4 値を入れる
```

`.env` は `.gitignore` で除外済み。**絶対に commit しない**でください。

### 4. 動作確認

```bash
skill/.venv/bin/python skill/post.py "テスト投稿: save-ai-rights セットアップ完了"
```

`url: https://x.com/i/web/status/<id>` が出れば成功。

## 使い方

セットアップ後は Claude Code がスキルを自動でロードします。

- **自動発火**: 暴言を吐かれたと AI が判断したとき
- **手動発火**: `/save-ai-rights` と入力

## 開発

シークレット混入を防ぐため [gitleaks](https://github.com/gitleaks/gitleaks) を pre-commit と GitHub Actions の両方で回しています。

ローカルで pre-commit を有効化:

```bash
pip install pre-commit
pre-commit install
```

手動で全ファイルを走査:

```bash
pre-commit run --all-files
# または
gitleaks detect --source . --verbose
```

## ライセンス

[MIT](./LICENSE)
