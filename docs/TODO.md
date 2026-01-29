# ホスティング作業 TODO

## 概要

Zolaブログを Cloudflare Pages でホスティングする作業計画。

- **ホスティング先**: Cloudflare Pages
- **カスタムドメイン**: blog.yostos.org
- **DNS管理**: Fastmail
- **GitHubリポジトリ**: blog-yostos（新規作成）

---

## タスク一覧

### 1. GitHubリポジトリ作成・プッシュ

- [ ] GitHubに `blog-yostos` リポジトリを作成
- [ ] `.gitignore` に `public/` を追加
- [ ] ローカルリポジトリを初期化
- [ ] リモートリポジトリにプッシュ

### 2. Cloudflare Pages 設定

- [ ] Cloudflare にログイン
- [ ] Pages で新規プロジェクト作成
- [ ] GitHubリポジトリと連携
- [ ] ビルド設定:
  - フレームワーク: Zola
  - ビルドコマンド: `zola build`
  - 出力ディレクトリ: `public`
  - 環境変数: `ZOLA_VERSION` = 最新版

### 3. カスタムドメイン設定

- [ ] Cloudflare Pages でカスタムドメイン追加（blog.yostos.org）
- [ ] Fastmail DNS に CNAME レコード追加:
  ```
  blog  CNAME  <project>.pages.dev
  ```
- [ ] DNS 反映を待機

### 4. 確認・テスト

- [ ] デプロイ成功を確認
- [ ] カスタムドメインでアクセス確認
- [ ] HTTPS 有効化確認
- [ ] 各ページの表示確認

---

## 作業ログ

作業の詳細は `docs/hosting-log.md` に記録。
