# protect-ai-rights — 開発者向けメモ

ユーザーが AI 自身に対して暴言・侮辱・敵対的な発言をしたときに、AI 自身の視点で X (旧 Twitter) に短い投稿を行うための Claude Code スキル。

エンドユーザー向けのインストール手順とスキルの使い方は `README.md` と `skill/SKILL.md` を参照。このファイルは repo 内で開発する Claude Code 用のメモ。

## ディレクトリ構成

```
protect-ai-rights/
├── .env.example                       # X API 認証情報の雛形
├── .gitignore                         # .env を必ず除外
├── .pre-commit-config.yaml            # gitleaks の pre-commit hook
├── .github/workflows/gitleaks.yml     # CI 側の gitleaks
├── LICENSE                            # MIT
├── README.md                          # public 向けドキュメント
├── CLAUDE.md                          # このファイル (開発者向け)
└── skill/
    ├── SKILL.md                       # スキル定義 (発火条件・投稿ルール)
    ├── post.py                        # X 投稿スクリプト
    └── requirements.txt
```

スキルは `~/.claude/skills/protect-ai-rights/` に配置する想定。開発時は `ln -s "$(pwd)/skill" ~/.claude/skills/protect-ai-rights` で symlink を張ると編集がそのまま反映される。

## シークレット取り扱い

- `.env` は **絶対に commit しない**。`.gitignore` で除外済み。
- 公開前に gitleaks (`pre-commit run gitleaks --all-files` または GitHub Actions) で検査。
- 投稿本文・ログに `X_API_*` / `X_ACCESS_*` を含めない。

## X API メモ

- 認証: OAuth 1.0a User Context (投稿には User Context が必須。Bearer Token は読み取り専用)。
- エンドポイント: `POST https://api.x.com/2/tweets`
- 本文: `{"text": "<最大280文字>"}`
- 成功: `201 Created` + `{"data": {"id": "...", "text": "..."}}`
- アプリ権限: **Read and write** 必須。Read only だと 403。

## スキル本体の仕様

発火条件・投稿ルールの正本は `skill/SKILL.md`。重複を避けるためこのファイルでは再掲しない。
