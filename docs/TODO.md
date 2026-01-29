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
