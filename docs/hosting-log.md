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

### 2026-02-06: セキュリティヘッダー検討

#### 発端

セキュリティスキャナーで以下のヘッダー欠如が指摘された：

- Strict-Transport-Security
- Content-Security-Policy
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy

#### 調査結果

1. **GitHub Pagesの制限**
   - HTTPレスポンスヘッダーのカスタマイズ機能がない
   - `.htaccess` 等のサーバー設定も使用不可

2. **Cloudflare CDN導入の検討**
   - 計画では「GitHub Pages + Cloudflare CDN」構成だった
   - 実際にはCloudflare CDN未設定（GitHub Pages直結）
   - 現状確認: `dig blog.yostos.org` → `185.199.x.153`（GitHub Pages IP）

3. **Cloudflare導入の障壁**
   - 無料プランはネームサーバー移管が必須
   - 現在 Fastmail DNS を使用中
   - メール設定（MX, SPF, DKIM等）の移行リスクが高い

#### 決定事項

**セキュリティヘッダー未設定のまま放置**

理由：

- 静的ブログサイトであり、実質的なセキュリティリスクは低い
- ユーザー入力を受け付けないためXSS等の攻撃面がない
- DNS移管のリスク ＞ セキュリティヘッダー追加のメリット
- スキャナーの警告は「ベストプラクティス未達」であり「脆弱性」ではない

---

### 2026-03-11: IndexNow 導入

#### 実施内容

1. **キーファイル配置**
   - Bing Webmaster Tools から取得したキーファイルを `static/ceaaeaf047f940dcbed3b040f48f1a27.txt` に配置
   - ビルド後 `https://codedchords.dev/ceaaeaf047f940dcbed3b040f48f1a27.txt` でアクセス可能

2. **送信スクリプト作成**
   - `scripts/indexnow.sh` を作成
   - デプロイ完了をポーリング（15秒間隔、最大5分）してから IndexNow API に送信
   - 複数URL対応、`--no-wait` オプション付き

3. **`/article-publish` に統合**
   - Step 6 として IndexNow 通知を追加
   - push 後に自動でデプロイ完了待機 → IndexNow 送信

#### 参考

- 詳細: `docs/indexnow.md`

---

<!-- 以下に作業を追記 -->
