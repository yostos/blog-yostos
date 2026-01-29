# ホスティング作業 TODO

## 概要

Zolaブログを **GitHub Pages + Cloudflare CDN** でホスティングする作業計画。

- **ホスティング先**: GitHub Pages + Cloudflare CDN
- **カスタムドメイン**: blog.yostos.org
- **DNS管理**: Fastmail（またはCloudflare）
- **GitHubリポジトリ**: yostos/blog-yostos

---

## タスク一覧

### 1. GitHubリポジトリ作成・プッシュ

- [x] GitHubに `blog-yostos` リポジトリを作成
- [x] `.gitignore` に `public/` を追加
- [x] ローカルリポジトリを初期化
- [x] リモートリポジトリにプッシュ
- [x] テーマをサブモジュールとして設定

### 2. ホスティング先検討（完了）

- [x] Cloudflare Pages を試行 → Zola V2サポート問題で断念
- [x] 代替案を比較検討
- [x] **GitHub Pages + Cloudflare CDN** に決定

### 3. GitHub Pages 設定

- [ ] GitHub Actions ワークフロー作成（Zolaビルド）
- [ ] GitHub Pages 有効化（gh-pages ブランチ）
- [ ] 初回デプロイ確認

### 4. Cloudflare CDN + カスタムドメイン設定

- [ ] Cloudflare にサイト追加（blog.yostos.org）
- [ ] DNS設定（CNAMEまたはプロキシ）
- [ ] SSL/TLS 設定
- [ ] キャッシュ設定

### 5. 確認・テスト

- [ ] デプロイ成功を確認
- [ ] カスタムドメインでアクセス確認
- [ ] HTTPS 有効化確認
- [ ] 各ページの表示確認
- [ ] 速度テスト

---

## 作業ログ

作業の詳細は `docs/hosting-log.md` に記録。

---

# tabi テーマ機能追加 TODO

## 実装済みの機能（2026-01-29）

### 1. giscus（コメント機能）
- [x] giscus vs utterances の比較検討 → **giscus を継続**
- [x] 既存コメントの移行（1件：`late-summer-greetings`）
- [x] config.toml に giscus 設定を追加

### 2. Mermaid（ダイアグラム）
- [x] グローバルは無効のまま、記事ごとに `[extra] mermaid = true` で有効化する方式に決定

### 3. Previous/Next article links
- [x] config.toml で `show_previous_next_article_links = true` に設定

### 4. Skins（カラースキーム）
- [x] teal（デフォルト）を継続

### 5. Social media links
- [x] GitHub 追加
- [x] Bluesky 追加
- [x] LinkedIn 追加
- [x] NOSTR 追加

### 6. iine（いいねボタン）
- [x] config.toml で `iine = true` に設定

### 7. Remote repository integration
- [x] `remote_repository_url` 設定
- [x] `show_remote_source = true`（フッターに「Site source」リンク）
- [x] `show_remote_changes = true`（記事に更新日があれば表示）

### 8. Footer menu
- [x] license ページへのリンクを追加

### 9. Copyright notice
- [x] CC BY-NC-ND 4.0 で設定
- [x] author を「Toshiyuki Yoshida」に変更

### 10. License ページ
- [x] `content/license.md` を作成
- [x] コンテンツライセンス（CC BY-NC-ND 4.0）
- [x] ソースコードライセンス（MIT）
- [x] 記事内コードスニペットはMIT適用の注記を追加

---

## 後日対応

### 11. 有償Webフォントの導入
GitHub Pages では有償フォントをリポジトリに含めるとライセンス違反の可能性あり。

**選択肢:**
1. S3をそのまま使い続ける（フォントファイルだけS3に配置、CORSが必要）
2. Cloudflare R2（S3互換、無料枠あり）
3. リポジトリをprivateにする

**決定事項:**
- [ ] 方式を選択
- [ ] 設定・動作確認

### 12. Projects page
ポートフォリオ/プロジェクト紹介ページ

### 13. Webmentions
IndieWeb 対応機能。後日説明を聞いてから検討。

---

## 比較メモ

### giscus vs utterances

| 項目 | giscus | utterances |
|------|--------|------------|
| バックエンド | GitHub Discussions | GitHub Issues |
| スレッド返信 | 可能 | 不可 |
| リアクション | 投稿ごとに可能 | 全体のみ |
| 検索性 | Discussionsで整理しやすい | Issuesと混在 |
| 既存コメント移行 | Discussionsへの移行が必要 | Issuesへの移行が必要 |

**結論**: 既存のgiscusコメントがあるため、giscusを継続が最善。
