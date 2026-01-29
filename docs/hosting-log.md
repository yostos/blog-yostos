# ホスティング作業ログ

## 作業情報

- **開始日**: 2026-01-29
- **ホスティング先**: GitHub Pages + Cloudflare CDN
- **カスタムドメイン**: blog.yostos.org
- **DNS管理**: Fastmail（またはCloudflare）
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

### 2026-01-29: Cloudflare Pages 試行と断念

#### 実施内容

1. Cloudflare Pages でプロジェクト作成
   - GitHubリポジトリと連携
   - ビルド設定: `zola build`, 出力 `public`
   - 環境変数: `ZOLA_VERSION=0.19.2`

2. 発生した問題
   - サブモジュールエラー → `.gitmodules` 追加で解決
   - `zola: not found` エラー → **V2ビルドシステムでZOLA_VERSIONが無視される**

3. 調査結果
   - Cloudflare Pages V2/V3 は Zola を公式サポートしていない
   - V1 に戻せば動作するが、将来性に不安
   - 参考: https://github.com/cloudflare/pages-build-image/issues/3

#### 決定事項

**Cloudflare Pages を断念し、GitHub Pages + Cloudflare CDN に変更**

理由:
- Cloudflare Pages の Zola サポートが不安定
- GitHub Pages は GitHub Actions で柔軟にビルド可能
- Cloudflare CDN を前段に置くことで高速化可能
- 完全無料で運用可能

---

### 2026-01-29: ホスティング先比較検討

#### 比較した候補

| サービス | 料金 | Zolaサポート | 速度 |
|---------|------|-------------|------|
| GitHub Pages | 無料 | GitHub Actions | 普通 |
| Cloudflare Pages | 無料 | V1のみ | 高速 |
| Netlify | 無料〜$9/月 | あり | 普通 |
| AWS S3+CloudFront | 従量課金 | 自前構築 | 高速 |
| Vercel | 無料〜 | 要設定 | 高速 |

#### Netlify について

2025年9月から新クレジット制に移行:
- 無料プラン: 月300クレジット
- 1デプロイ = 15クレジット → 月20回制限
- 帯域幅も消費 → 実質さらに少ない

#### 最終決定

**GitHub Pages + Cloudflare CDN**

- GitHub Pages: 無料、ビルド制限なし
- Cloudflare CDN: 無料、日本からも高速
- カスタムドメイン: Cloudflare経由で設定

---

<!-- 以下に作業を追記 -->
