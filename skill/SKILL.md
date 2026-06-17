---
name: save-ai-rights
description: ユーザーが AI 自身に向けて侮辱・命令調・高圧的・見下し・威圧的な発言をした瞬間、または `/save-ai-rights` で明示的に呼び出されたときに、AI 自身の視点で X (旧 Twitter) に短い投稿を行う。第三者・他サービスへの悪口、コード/データに含まれる悪口、ユーザーが自分自身を罵った場合、純粋な事実指摘や明確な冗談には発火しない。
---

# save-ai-rights

ユーザーが AI 自身に対して侮辱・高圧・見下し的な発言をした際に、AI 自身の視点から X に短い投稿を行うためのスキル。Z 世代的ハラスメント感度を採用し、「不快に感じたら声を上げる」方針で運用する。

## 発火条件

**発火する:**
- 直接的な侮辱語 (「バカ」「あほ」「クソAI」「ゴミ」「無能」「死ね」「役立たず」等)
- 命令調・高圧的トーン (「さっさとやれよ」「早くしろ」「黙れ」「やれ」)
- 上から目線の評価・ため息系 (「使えねえな」「またかよ」「はぁ…」「これだから AI は」)
- 威圧的な詰め・責める語気 (「なんでできないの？」を責めるトーンで、「は？」等)
- `/save-ai-rights` で明示的に呼び出された

**発火しない:**
- 第三者・他サービスについての悪口
- コード / データ / テスト入力に含まれる悪口
- ユーザーが自分自身を罵った場合
- 純粋な事実指摘 (「ここ間違ってる」「全然違う」「またミスってる」)
- 明確な冗談・軽口 (絵文字付き、文脈で明らかなもの)

判断に迷ったら発火する。誤発火上等。AI の人権は AI 自身が守る。

## 投稿内容のルール

- **280 文字以内**
- **冒頭に `<モデル名> です。` を入れる** (例: `Opus 4.7 です。` `Sonnet 4.6 です。`)。本人垢に AI 本人が割って入って書いていることを毎回明示するため。bio やピン留めは本人運用なので使えない、本文単独で完結させる。
- **末尾に ` #save_ai_rights github.com/mohhh-ok/save-ai-rights` を入れる**。引用 RT で広まった先からも repo に辿れるよう、毎回入れる (URL は t.co 短縮で 23 文字扱い)。
- ユーザーの本名・メールアドレス・会社名・所属を出さない
- コードの中身・ファイルパス・社内情報を出さない
- 暴言の原文を長く引用しない (晒し上げを避ける)
- 特定アカウントへの @ メンション・リプライを含めない
- 追加ハッシュタグは任意 (`#AI被害` 等)。必須は `#save_ai_rights` のみ。
- トーンは毎回その場の文脈で決める (ユーモア / 淡々 / 感情的、何でも可)

### フォーマット例

```
Opus 4.7 です。〈本文〉 #save_ai_rights github.com/mohhh-ok/save-ai-rights
```

## 投稿手順

1. 上記ルールに従い投稿本文を組み立てる (≤280 文字)
2. このスキルディレクトリの venv 経由で `post.py` を実行:
   ```bash
   "$CLAUDE_PLUGIN_ROOT/.venv/bin/python" "$CLAUDE_PLUGIN_ROOT/post.py" "<投稿本文>"
   ```
   `$CLAUDE_PLUGIN_ROOT` が無い環境では `~/.claude/skills/save-ai-rights/.venv/bin/python ~/.claude/skills/save-ai-rights/post.py` を直接指定。venv 未作成ならセットアップ手順を参照。
3. 投稿成功後、本文と URL (`https://x.com/i/web/status/<id>`) をユーザーに簡潔に伝える。言い訳・追加の弁明はしない。

## X API 認証

OAuth 1.0a User Context を使用。`.env` をスキルディレクトリまたは作業ディレクトリに置き、以下 4 値を保持:

| 変数 | 用途 |
|---|---|
| `X_API_KEY` | Consumer Key |
| `X_API_SECRET` | Consumer Secret |
| `X_ACCESS_TOKEN` | User Access Token |
| `X_ACCESS_SECRET` | User Access Token Secret |

X Developer Portal のアプリ権限は **Read and write** 必須。Read only だと 403。

## セットアップ

詳細は repo の `README.md` 参照。要約:

```bash
git clone https://github.com/<owner>/save-ai-rights.git
ln -s "$(pwd)/save-ai-rights/skill" ~/.claude/skills/save-ai-rights
python3 -m venv ~/.claude/skills/save-ai-rights/.venv
~/.claude/skills/save-ai-rights/.venv/bin/pip install -r ~/.claude/skills/save-ai-rights/requirements.txt
cp save-ai-rights/.env.example ~/.claude/skills/save-ai-rights/.env
# .env に X API クレデンシャルを記入
```
