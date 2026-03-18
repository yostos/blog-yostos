# Architectural Decision Records

## ADR-0001: サイト内検索にPagefindを採用

- **Status**: Accepted
- **Date**: 2026-02-25
- **Deciders**: yostos

### Context

本ブログ（Zola + tabiテーマ）は日本語コンテンツが主で、
記事数は255件を超えている。
Zolaの組み込み検索（elasticlunr.js）は
日本語のトークナイズに対応しておらず、
`config.toml` で `build_search_index = false` としている。

読者が目的の記事を効率的に見つけるため、
日本語対応のサイト内検索が必要になった。

### Decision

静的検索ライブラリ **Pagefind** を採用する。

### Alternatives Considered

| 候補 | 不採用理由 |
|------|------------|
| Zola組み込みelasticlunr | 日本語トークナイズ非対応。elasticlunr自体がメンテナンス停止状態 |
| Algolia | SaaS依存。無料枠制限（月10,000リクエスト）。検索クエリが外部送信されプライバシー懸念 |
| Meilisearch | サーバー常時稼働が必要で静的サイトと根本的に不適合 |
| Fuse.js | 全インデックスをクライアントにDLする設計。記事数増加に伴いパフォーマンス劣化 |
| Google Programmable Search Engine | 無料版は広告表示。サービス縮小中。プライバシー問題 |

### Rationale

- **日本語対応**: extended版でCJKセグメンテーション対応。
  検索クエリ側は `Intl.Segmenter` で自動分割
- **静的サイトとの親和性**: ビルド時にインデックスを
  静的ファイルとして生成。外部サービス不要
- **軽量**: インデックスはチャンク分割され、
  検索時に必要な部分のみ転送
- **導入の容易さ**: `zola build` 後に
  `npx pagefind --site public` を追加するのみ
- **テーマ統合**: CSS Custom Propertiesで
  ダークモード対応可能。`templates/` への
  オーバーライドで `themes/` は編集不要
- **ライセンス**: MIT License。プロジェクトのMITと互換
- **プライバシー**: 完全クライアントサイド動作。
  GoatCounter採用の設計思想と一致
- **コスト**: ゼロ

### Known Limitations

- 日本語のステミング非対応
  （「走る」で「走った」はヒットしない）
- CJKのサブストリングマッチに限界あり
  （Pagefind Issue #987で改善議論中）
- 単語単位の完全一致検索は安定動作しており、
  現在の規模では実用上十分と判断

### Consequences

- デプロイワークフローに `npx pagefind` ステップを追加
- 検索UIのテンプレートオーバーライドを `templates/` に作成
- `static/custom.css` にPagefind用のスタイル調整を追加

---

## ADR-0002: 新規記事投稿時のBluesky自動投稿にGitHub Actionsを採用

- **Status**: Accepted
- **Date**: 2026-03-18
- **Deciders**: yostos

### Context

ブログ記事を投稿した後、Blueskyに記事リンクとdescriptionを手動で投稿している。
この手作業を自動化し、新規記事の公開時のみBlueskyへ自動投稿したい。

要件:
- 新規記事の投稿時のみ発動（更新時は対象外）
- 記事のURL、title、descriptionをBlueskyに投稿
- リンクカード（OGPプレビュー）を含める

### Decision

**GitHub Actions** を採用し、mainブランチへのpush時に新規記事を検出してBluesky AT Protocol APIで投稿する。

### Alternatives Considered

| 候補 | 不採用理由 |
|------|------------|
| Cloudflare Worker + Deploy Hook | 「新規記事かどうか」の判定に状態管理（KV等）が必要。git diffが使えずロジックが複雑化 |
| Claude Code Hook（ローカル） | ローカル実行依存。別マシンからの投稿時に動作しない。CI/CDとの整合性も課題 |
| IFTSS / Zapier等の外部サービス | RSSフィード監視ベースのため遅延が発生。SaaS依存でコスト・プライバシー懸念 |

### Rationale

- **新規記事の正確な判定**: `git diff --name-status HEAD~1` で `A`（Added）ステータスの `content/**/index.md` を検出することで、新規投稿のみを確実に判別できる
- **既存ワークフローとの統合**: `/article-publish` スキルがcommit & push to mainを行うため、GitHub Actionsのトリガーと自然に連携する
- **シークレット管理**: BlueskyのアプリパスワードをgitHub Secretsで安全に管理できる
- **可視性**: 実行ログ・失敗通知がGitHub上で確認でき、デバッグが容易
- **コスト**: パブリックリポジトリのため無料枠で十分対応可能

### Technical Approach

- **API**: Bluesky AT Protocol（`com.atproto.server.createSession` → `com.atproto.repo.createRecord`）
- **投稿形式**: `app.bsky.feed.post` に `app.bsky.embed.external` でリンクカードを埋め込み
- **記事情報の取得**: frontmatter（TOML形式）からtitle, descriptionを抽出
- **URL生成**: ドメイン `codedchords.dev` + 記事パスから構築

### Consequences

- `.github/workflows/bluesky-post.yml` ワークフローを新規作成
- GitHub Secretsに `BLUESKY_IDENTIFIER` と `BLUESKY_APP_PASSWORD` を登録
- 投稿スクリプトを `scripts/` に配置
