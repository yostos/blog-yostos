# ブログのドメイン移転計画

`blog.yostos.org` → `codedchords.dev` に移行する。

## Phase 1: 事前準備

### 1-1. 影響範囲の確認

ドメイン変更で影響を受けるファイル：

- `config.toml` の `base_url`
- `content/` 内の記事本文（旧ドメインへの内部リンク）
  - `blog/2025/04/beyond-distortion/index.md`
  - `blog/2025/05/dji-air3s-flight/index.md`
  - `blog/2025/08/government-fails-rice-policy-reversal/index.md`
  - `blog/2025/09/amazon-amplify-node-versionup/index.md`
  - `blog/2026/01/blog-to-zola-aws-cleanup/index.md`
  - `blog/2026/02/claude-code-jrnl-context-handoff/index.md`
- `data/linkcard.json`（自サイトへのlinkcard）

※ `canonical_url` はすべてZenn向けのため変更不要。

### [済] 1-2. config.toml の変更

```toml
base_url = "https://codedchords.dev"
```

### [済] 1-3. 記事本文の内部リンクをパス相対に変換

`content/` 内で `https://blog.yostos.org/...` への
絶対 URL リンクをパス相対リンク（`/blog/...`）に
変換した。ドメインに依存しなくなるため、
今後のドメイン変更にも影響されない。

対象（4ファイル7箇所）：

- `blog/2025/04/beyond-distortion/index.md`
  - `/articles/2025/02/11/simplifier-mk2`
    → `/blog/2025/02/simplifier-mk2/`
  - `/articles/2025/04/04/biscayne-blue`
    → `/blog/2025/04/biscayne-blue/`
- `blog/2025/05/dji-air3s-flight/index.md`
  - `/articles/2025/04/10/drown-lisence`
    → `/blog/2025/04/drone-lisence/`
- `blog/2025/08/government-fails-rice-policy-reversal/index.md`
  - `/articles/2024/09/06/Weekly-buzz-20240906`
    → `/blog/2024/09/Weekly-buzz-20240906/`（3箇所）
- `blog/2026/02/claude-code-jrnl-context-handoff/index.md`
  - `/blog/2025/07/first-mcp-server-development/`
    （ドメイン部分を除去）

除外（過去の構成を説明する歴史的記述）：

- `blog/2026/01/blog-to-zola-aws-cleanup/index.md`
- `blog/2025/09/amazon-amplify-node-versionup/index.md`

### [済] 1-4. aliases の削除

旧 Next.js ブログからの互換性のために設定していた
`aliases` を全記事（226ファイル）から削除した。

旧パスからのアクセスは redirect サイト
（`blog-yostos-redirect`）が担うため、
本体サイトに aliases は不要。

Python スクリプトで `content/**/index.md` の
`aliases = [...]` 行を一括削除。

### [済] 1-5. linkcard の GitHub 専用処理を廃止

GitHub URL もはてなブログカード（iframe）に
統一し、以下を削除した：

- `data/linkcard.json` → 削除（`data/` 自体も削除）
- `scripts/generate-linkcard.mjs` → 削除
- `templates/shortcodes/linkcard.html`
  → GitHub 分岐を削除、はてな iframe のみに簡素化
- `static/custom.css`
  → GitHub カード関連 CSS を削除
    （`.linkcard-*`, `.linkcard-gh-*` 等）
  → はてなブログカード CSS（`.hatenablogcard`）は残す
- `package.json`
  → `linkcard` / `linkcard:dry-run` スクリプトを削除
- `CLAUDE.md`
  → Common Commands から `npm run linkcard` を削除
  → Link Card Shortcode セクションを更新
- `docs/linkcard.md` → 削除

### [済] 1-6. CNAME ファイルの作成

GitHub Pages のカスタムドメイン用に
`static/CNAME` を作成した。

```
codedchords.dev
```

### Phase 1 完了確認

`zola build` で 247ページ + 25セクションの
ビルド成功を確認済み。

## [済] Phase 2: DNS設定（Cloudflare）

### [済] 2-1. 新ドメインのDNSレコード設定

GitHub Pages 用の A レコード4つと www の
CNAME を設定した。すべて DNS only。

| Type  | Name | Content          | Proxy  |
| ----- | ---- | ---------------- | ------ |
| A     | @    | 185.199.108.153  | DNS only |
| A     | @    | 185.199.109.153  | DNS only |
| A     | @    | 185.199.110.153  | DNS only |
| A     | @    | 185.199.111.153  | DNS only |
| CNAME | www  | yostos.github.io | DNS only |

### 2-2. Cloudflare の Proxy 設定

GitHub Pages で HTTPS を管理するため、
DNS レコードは **DNS only**（Proxyなし）に
設定する。Proxy 有効だと証明書の競合が
発生する可能性がある。

## Phase 3: GitHub Pages 設定

### [済] 3-1. カスタムドメインの設定

リポジトリの Settings → Pages → Custom domain に
`codedchords.dev` を設定した。

### [済] 3-2. 変更をデプロイ

Phase 1 の変更をコミット・push した。

コミット:
- `refactor: simplify linkcard and prepare domain migration`
- 237ファイル変更（削除・追加含む）
- GitHub Pages が自動でビルド・デプロイ開始

### [済] 3-3. HTTPS の有効化

DNS 浸透を確認後、Enforce HTTPS を有効化した。

## [済] Phase 4: 旧ドメインのリダイレクトサイト

旧ドメイン `blog.yostos.org` にアクセスした人を
新ドメインの対応ページへ転送する。

`yostos.org` の DNS は Fastmail で管理しており
Cloudflare への移行は行わないため、
Cloudflare Redirect Rules は使えない。

### 方針: リダイレクト専用の静的サイトを生成

現在のブログリポジトリで `zola build` すると
`public/` に全ページの HTML が生成される。
aliases によるリダイレクトページも含まれるため、
旧 Next.js パス（`/articles/...`）もカバーされる。

この `public/` 内の全 HTML を meta refresh
リダイレクトページに差し替えて、別リポジトリ
（例: `blog-yostos-redirect`）に配置し、
`blog.yostos.org` で GitHub Pages 配信する。

各ページの内容：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="canonical"
    href="https://codedchords.dev/（対応パス）">
  <meta http-equiv="refresh"
    content="0; url=https://codedchords.dev/（対応パス）">
</head>
<body></body>
</html>
```

### [済] 手順

1. `base_url` を `https://blog.yostos.org` に
   戻した状態で `zola build` する
2. スクリプトで `public/` 内の全 HTML を
   meta refresh リダイレクトに差し替える
   （パスから対応する新 URL を生成）
3. 別リポジトリ `blog-yostos-redirect` を作成
4. 生成物を push し GitHub Pages を有効化
5. `blog.yostos.org` をカスタムドメインに設定

実績：

- リポジトリ: `yostos/blog-yostos-redirect`
- `build_redirects.py` で Zola ビルド → HTML 差し替え
  → 不要ファイル削除 → CNAME 配置を一括実行
- 通常ページ 367 件 + alias ページ 226 件 = 計 593 件の
  リダイレクトを生成
- alias ページは Zola が生成した meta refresh の
  リダイレクト先（正規パス）を読み取り、
  新ドメインの正規パスに直接リダイレクト
- GitHub Actions でデプロイ自動化
  （push → zola build → スクリプト実行 → Pages デプロイ）
- DNS は既存の CNAME（`yostos.github.io`）をそのまま利用
- 動作確認済み:
  - `blog.yostos.org/` → `codedchords.dev/`
  - `blog.yostos.org/blog/2025/03/claude-code/`
    → `codedchords.dev/blog/2025/03/claude-code/`
  - `blog.yostos.org/articles/2025/03/20/salmon-run/`
    → `codedchords.dev/blog/2025/03/salmon-run/`

### 利点

- 全ページ・全パス（aliases 含む）をカバー
- meta refresh + canonical で SEO 的にも適切
- Fastmail DNS の変更は不要
  （既存の CNAME/A レコードをそのまま利用）
- 新記事追加時はスクリプトを再実行するだけ

### [済] フォント配信（CloudFront）の修正

BerkeleyMono フォントを CloudFront
（`d3w0x7oesq9q1.cloudfront.net`）経由で
S3 から配信しているが、以下の更新が必要だった。

1. CloudFront Function `restrict-font-access` の
   `allowedDomains` を `blog.yostos.org` →
   `codedchords.dev` に変更
2. S3 バケットポリシー（`berkeley-mono`）の
   Referer 条件を `codedchords.dev*` に更新
3. S3 CORS 設定に `codedchords.dev` を追加（済）
4. CloudFront キャッシュポリシーに `Origin`
   ヘッダーを追加（CORS レスポンスを
   正しくキャッシュするため）

## Phase 5: 外部サービスの更新

### [済] 5-1. GoatCounter

GoatCounter の設定画面で
新ドメイン `codedchords.dev` を
許可ドメインに追加した。

### [済] 5-2. Giscus（コメント）

`config.toml` で `mapping = "pathname"` を
使用しているが、既存の Discussion タイトルが
旧パス形式（`articles/YYYY/MM/DD/slug`）の
ままだったため、新パスでマッチしなかった。

`blog-comments` リポジトリの Discussion タイトルを
新パス形式に変更した（2件）：

- #2: `articles/2025/03/08/Portfolio-site-for-engieer`
  → `blog/2025/03/Portfolio-site-for-engieer/`
- #3: `articles/2025/08/15/late-summer-greetings`
  → `blog/2025/08/late-summer-greetings/`

また、Discussion #2, #3 のカテゴリが「General」
だったが、`config.toml` の Giscus 設定では
`category = "Announcements"` を指定しており
不一致だったため、両方を「Announcements」に移動した。

### [済] 5-3. Zenn 記事の内部リンク修正

Zenn リポジトリ内の `articles/` 配下で
`blog.yostos.org` → `codedchords.dev` に
文字列置換した。

### [済] 5-4. RSS/Atom フィードの対応

`generate_feeds = true` のためフィード URL が
`https://codedchords.dev/atom.xml` に変わった。
旧 URL はリダイレクトサイト（Phase 4）で
カバーされる。フィードアグリゲータへの
登録はないため、対応不要。

### [済] 5-5. SNS 上の OGP キャッシュ

OGP 画像にドメイン情報を含めていないため、
対応不要。旧 URL でのシェアはリダイレクト
サイト（Phase 4）経由で新 URL に転送される。

## Phase 6: セキュリティヘッダーの設定

GitHub Pages 単体ではカスタム HTTP レスポンス
ヘッダーを設定できない。Cloudflare のプロキシを
有効にし、Transform Rules または Workers で
セキュリティヘッダーを付与する。

### TODO

1. Cloudflare の DNS レコードを DNS only →
   Proxied に変更
2. Cloudflare の SSL/TLS モードを Full (strict)
   に設定（GitHub Pages の証明書との整合性）
3. Transform Rules でレスポンスヘッダーを追加：
   - `Content-Security-Policy`
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`
   - `Referrer-Policy: strict-origin-when-cross-origin`
   - `Permissions-Policy`
4. 動作確認（ヘッダー付与、HTTPS、フォント配信）

### 方針変更: Cloudflare Workers（静的アセット）への移行

上記の Cloudflare Proxy + Transform Rules 案を
検討したが、以下の理由で Cloudflare Workers
（静的アセット）へのホスティング移行に
方針を変更した。

**Cloudflare Proxy + GitHub Pages の問題点:**

- GitHub Pages の Let's Encrypt 証明書は
  90日ごとに HTTP-01 チャレンジで自動更新される
- Cloudflare Proxy が間に入ると
  チャレンジが GitHub に届かず、
  更新が静かに失敗する可能性がある
- 証明書期限切れでサイトが突然表示不能になる
- 静的ブログで証明書の定期監視は割に合わない

**Cloudflare Workers（静的アセット）で解決:**

Cloudflare は Workers と Pages を統合しており、
今後の機能開発は Workers に集中される。
Workers の静的アセット機能は `_headers` ファイルを
ネイティブにサポートしている。

- `_headers` ファイルでセキュリティヘッダーを
  設定可能
- SSL 証明書は Cloudflare が一元管理
  （更新問題が発生しない）
- DNS も Cloudflare で設計が一貫する
- 無料枠で十分（帯域無制限）

**ビルド方式:**

GitHub Actions でビルドし、
`wrangler deploy` でデプロイする。
現在の `deploy.yml` をほぼ流用でき、
Zola バージョンも自分で管理できる。

### 移行手順

#### [済] 6-1. Cloudflare Workers プロジェクト作成

Cloudflare Dashboard → Workers & Pages →
Create application → Pages タブ →
**Upload your static files** で作成した。

- **Project name**: `coded-chords`
- **URL**: `coded-chords.yostos.workers.dev`

実際のデプロイは GitHub Actions から行う。

#### [済] 6-2. GitHub Actions デプロイ設定

既存の `.github/workflows/deploy.yml` を
GitHub Pages → Cloudflare Workers 向けに
変更した。ビルド部分
（Zola セットアップ・`zola build`）は
そのまま流用し、デプロイ先のみ変更。

変更点：

- `permissions` から `pages` / `id-token` を削除
- GitHub Pages 向けステップ
  （`configure-pages` / `upload-pages-artifact` /
  `deploy-pages`）を削除
- `cloudflare/wrangler-action@v3` で
  `deploy` を実行
- リポジトリに `wrangler.toml` を追加
  （静的アセットのディレクトリ指定等）
- GitHub Repository Secrets
  （Settings → Secrets and variables → Actions）
  に以下を登録済み：
  - `CLOUDFLARE_ACCOUNT_ID`:
    Cloudflare Dashboard → ドメイン選択 →
    Overview ページ右サイドバーから取得
  - `CLOUDFLARE_API_TOKEN`:
    既存の「blog-yostos build token」を使用
    （Workers スクリプト:編集 権限あり）

#### 6-3. カスタムドメイン接続

Workers のプロジェクト設定 →
Custom domains → `codedchords.dev` を追加。
DNS が同じ Cloudflare アカウントのため、
DNS レコードが自動設定される。
SSL 証明書も Cloudflare が自動発行・管理する。

注意: この手順は GitHub Pages 側のカスタム
ドメイン解除（6-5）と DNS 切り替え（6-6）
を同時に行う必要がある。ダウンタイムを
最小化するため、以下の順序で実施する：

1. Workers でドメインを追加
2. GitHub Pages のカスタムドメインを解除
3. DNS レコードを切り替え

#### 6-4. セキュリティヘッダー設定

`static/_headers` ファイルを作成する。
Cloudflare Workers の静的アセット機能は
`_headers` ファイルをビルド出力に含めると
レスポンスヘッダーに自動適用する。

設定するヘッダー：

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy`（カメラ・マイク等を無効化）
- `Content-Security-Policy`

CSP では以下の外部ドメインを許可する：

- `d3w0x7oesq9q1.cloudfront.net`
  （BerkeleyMono フォント配信）
- `*.goatcounter.com`（アクセス解析）
- `giscus.app`（コメント）
- `hatenablog-parts.com`（linkcard iframe）

#### 6-5. GitHub Pages 設定解除

リポジトリの Settings → Pages で：

- Custom domain を削除
- Source を None に変更（GitHub Pages を無効化）

#### 6-6. DNS 切り替え

Cloudflare の DNS 設定で以下を実施：

- 既存の GitHub Pages 向け A レコード
  4つを削除：
  - `185.199.108.153`
  - `185.199.109.153`
  - `185.199.110.153`
  - `185.199.111.153`
- 既存の www CNAME（`yostos.github.io`）を削除
- Cloudflare Pages がカスタムドメイン接続時に
  自動作成した CNAME を確認

#### 6-7. `static/CNAME` 削除

GitHub Pages 用の `static/CNAME` ファイルを
リポジトリから削除する。Cloudflare Workers では
カスタムドメインをダッシュボードで管理するため
不要。

#### 6-8. GitHub Pages 関連の設定削除

GitHub Actions の `deploy.yml` は 6-2 で
Cloudflare Workers 向けに変更済みのため、
追加の削除作業は不要。

以下のワークフローはそのまま残す：

- `deploy.yml`（Cloudflare Workers 向けに変更済み）
- `textlint.yml`（lint チェック）
- `zola-check-scheduled.yml`
  （月次ビルドチェック）
- `claude.yml`（Claude Code）
- `claude-code-review.yml`（コードレビュー）

#### 6-9. フォント配信（CloudFront）の確認

BerkeleyMono フォントは CloudFront 経由で
S3 から配信している（Phase 4 で設定済み）。

ホスティング変更でもフォントリクエストは
ブラウザから CloudFront に直接送信されるため、
基本的に影響なし。以下を確認する：

- CloudFront Function `restrict-font-access` の
  `allowedDomains` に `codedchords.dev` が
  設定済みであること（Phase 4 で対応済み）
- S3 バケットポリシーの Referer 条件が
  `codedchords.dev*` であること（対応済み）
- 実際にフォントが正しく表示されること

## チェックリスト

- [x] config.toml の base_url を変更
- [x] 記事本文の内部リンクをパス相対に変換
- [x] 全記事から aliases を削除（226ファイル）
- [x] linkcard の GitHub 専用処理を廃止
- [x] static/CNAME を作成
- [x] Cloudflare で新ドメインの DNS 設定
- [x] GitHub Pages でカスタムドメイン設定
- [x] 変更を push してデプロイ
- [x] HTTPS 有効化を確認
- [x] リダイレクトサイト生成スクリプトの作成
- [x] blog-yostos-redirect リポジトリ作成・デプロイ
- [x] GoatCounter の許可ドメイン追加
- [x] Giscus のコメント表示確認
- [x] Zenn 記事のリンク修正
- [x] RSS フィード URL のリダイレクト確認
- [ ] ~~Cloudflare プロキシ有効化とセキュリティヘッダー設定~~
      → Cloudflare Workers 移行に方針変更
- [x] 6-1: Cloudflare Workers プロジェクト作成
  （`coded-chords`）
- [x] 6-2: GitHub Actions デプロイ設定変更
  （deploy.yml を Cloudflare Workers 向けに修正）
- [ ] 6-3/6-5/6-6: カスタムドメイン接続・
  GitHub Pages 解除・DNS 切り替え
- [ ] 6-4: セキュリティヘッダー設定
  （`static/_headers`）
- [ ] 6-7: `static/CNAME` 削除
- [ ] 6-8: GitHub Pages 関連の設定削除
- [ ] 6-9: フォント配信の確認
