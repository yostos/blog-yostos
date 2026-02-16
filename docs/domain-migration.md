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

### 3-2. 変更をデプロイ

Phase 1 の変更をまとめて push する。

### 3-3. HTTPS の有効化

DNS 浸透後（数分〜最大48時間）に
Settings → Pages → Enforce HTTPS を有効化する。

## Phase 4: 旧ドメインのリダイレクトサイト

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

### 手順

1. `base_url` を `https://blog.yostos.org` に
   戻した状態で `zola build` する
2. スクリプトで `public/` 内の全 HTML を
   meta refresh リダイレクトに差し替える
   （パスから対応する新 URL を生成）
3. 別リポジトリ `blog-yostos-redirect` を作成
4. 生成物を push し GitHub Pages を有効化
5. `blog.yostos.org` をカスタムドメインに設定

### 利点

- 全ページ・全パス（aliases 含む）をカバー
- meta refresh + canonical で SEO 的にも適切
- Fastmail DNS の変更は不要
  （既存の CNAME/A レコードをそのまま利用）
- 新記事追加時はスクリプトを再実行するだけ

## Phase 5: 外部サービスの更新

### 5-1. GoatCounter

GoatCounter の設定画面で
新ドメイン `codedchords.dev` を
許可ドメインに追加する。

### 5-2. Giscus（コメント）

`config.toml` で `mapping = "pathname"` を
使用しているため、パス構造が変わらなければ
既存コメントはそのまま維持される。
移行後に実際のコメント表示を確認すること。

### 5-3. Zenn 記事の内部リンク修正

Zenn リポジトリ内の `articles/` 配下で
`blog.yostos.org` → `codedchords.dev` に
文字列置換する。

### 5-4. RSS/Atom フィードの対応

`generate_feeds = true` のためフィードURLが
変わる。旧ドメインの301リダイレクト（Phase 4）
でフィードURLもカバーされるが、
主要なフィードアグリゲータへの登録を
確認すること。

### 5-5. SNS 上の OGP キャッシュ

旧URLでシェアされた記事の OGP 画像キャッシュは
自動更新されない。重要な記事については
各プラットフォームのキャッシュクリアを検討する。

- X (Twitter): Card Validator でキャッシュ更新
- Facebook: Sharing Debugger でキャッシュ更新

## チェックリスト

- [x] config.toml の base_url を変更
- [x] 記事本文の内部リンクをパス相対に変換
- [x] 全記事から aliases を削除（226ファイル）
- [x] linkcard の GitHub 専用処理を廃止
- [x] static/CNAME を作成
- [x] Cloudflare で新ドメインの DNS 設定
- [x] GitHub Pages でカスタムドメイン設定
- [ ] 変更を push してデプロイ
- [ ] HTTPS 有効化を確認
- [ ] リダイレクトサイト生成スクリプトの作成
- [ ] blog-yostos-redirect リポジトリ作成・デプロイ
- [ ] GoatCounter の許可ドメイン追加
- [ ] Giscus のコメント表示確認
- [ ] Zenn 記事のリンク修正
- [ ] RSS フィード URL のリダイレクト確認
