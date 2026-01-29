# ホスティング作業ログ

## 作業情報

- **開始日**: 2026-01-29
- **ホスティング先**: Cloudflare Pages
- **カスタムドメイン**: blog.yostos.org
- **DNS管理**: Fastmail
- **GitHubリポジトリ**: yostos/blog-yostos

---

## 作業履歴

### 2026-01-29: 計画策定

#### 実施内容

1. ホスティング方針を決定
   - Cloudflare Pages を選択（高速CDN、無料枠）
   - カスタムドメイン blog.yostos.org を使用
   - GitHubリポジトリ blog-yostos を新規作成

2. ドキュメント作成
   - `docs/TODO.md`: 作業計画
   - `docs/hosting-log.md`: 作業ログ（本ファイル）

#### 次のステップ

- GitHubリポジトリの作成とプッシュ

---

### 2026-01-29: GitHubリポジトリ作成・プッシュ

#### 実施内容

1. `.gitignore` 作成
   - gitignore.io で macOS, Vim, Rust 用テンプレートを生成
   - Zola ビルド出力 `public/` を追加

2. Git リポジトリ初期化
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Zola blog with tabi theme"
   ```

3. GitHub リポジトリ作成・プッシュ
   ```bash
   gh repo create blog-yostos --public --source=. --remote=origin --push
   ```
   - リポジトリURL: https://github.com/yostos/blog-yostos

#### 次のステップ

- Cloudflare Pages の設定

---

<!-- 以下に作業を追記 -->
