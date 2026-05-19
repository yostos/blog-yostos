+++
title = "WEBフォントをAmazon S3からCloudflare R2に移行する"
description = "(TBD)"
date = 2026-05-20
draft = true

[taxonomies]
tags = ["Tech", "Cloudflare", "AWS"]

[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

<!-- textlint-disable -->

<!-- =========================================================
作業ドラフト。記事執筆に必要な事実・コマンド・気付きをここに
積み上げる。最終構成は作業完了後に整える。
========================================================= -->

## 記事の方向性メモ (草稿前メモ・本文化前に削除)

- 「やったこと」の作業ログにしない。読者が「自分も S3+CloudFront からの
  脱出を検討するか」を判断できる材料を提示する (feedback_migration_as_benefits)
- 過去記事 `blog-to-zola-aws-cleanup` の続編。Amplify は閉じたが
  Berkeley Mono 配信のための S3+CloudFront だけは残っていた。
  本記事でその最後の AWS リソースを閉じる。
- 主な軸 (なぜ移行するに足るか):
  - **元々の制約**: Berkeley Mono は有償フォントで、簡単にダウンロード
    されたくない。S3 では公開バケット + CloudFront Function による Referer
    制限 + バケットポリシー + CORS で守っていた
  - **きっかけ**: ブログのワークロードが Cloudflare に移った。
    フォントだけ AWS に残しておく理由が薄れた
  - **R2 binding の利点**: 公開 URL を持たないので「Referer 偽装で守る」
    思想自体が不要になる。CORS も API キーも消える
  - **副次効果**: 同一オリジン配信になり CSP / preconnect が単純化
  - **コスト**: R2 の無料枠 (10GB / 月) に余裕で収まる
- 記事スコープ: R2 移行 + AWS リソース停止まで含めて 1 本にまとめる

## 移行前の構成 (事実確認済)

- 配信元: S3 バケット `berkeley-mono`
- 配信経路: CloudFront `d3w0x7oesq9q1.cloudfront.net`
- アクセス制御:
  - CloudFront Function `restrict-font-access` で Referer の
    allowedDomains を `codedchords.dev` に限定
  - S3 バケットポリシーで Referer 条件 `codedchords.dev*`
- CORS: S3 側で `codedchords.dev` を許可
- ホスト側 (blog-yostos): Cloudflare Workers (Static Assets only)
  - `wrangler.toml` は `[assets] directory = "./public"` のみ
  - Worker スクリプトは未配置
- CSS: `static/custom.css` 内で 14 個の `@font-face` が
  `https://d3w0x7oesq9q1.cloudfront.net/<file>.woff2` を参照
  - 利用ウェイト: Regular/Medium/SemiBold/Bold/ExtraBold/Black + 各 Oblique
  - KADOMA はコメントアウト済
- 既存 OGP 生成 (`scripts/generate-ogp.mjs`) はローカル OTF を使うため無関係

## 移行後の構成 (ハンドオフ書通り)

- Cloudflare R2 バケット `web-fonts` (private, r2.dev 無効)
- バケット直下に 21 個の woff2 (S3 のキーと 1:1) + KADOMA
- アクセス手段は Worker からの R2 Binding (`FONTS`) のみ
- CORS 設定なし / API トークン未発行 / 公開 URL 無効のまま
- Worker が `/fonts/<filename>` を R2 binding に橋渡し
- CSS は同一オリジンの `/fonts/<filename>` を指す

### protection-model 4 レイヤー (記事引用用要約)

| # | 仕組み | 設定実体 | 遮断する脅威 |
|---|---|---|---|
| 1 | バケット非公開 | r2.dev 無効・カスタムドメイン未割当・CORS なし | バケット URL の直接スクレイプ・検索エンジン索引・汎用 S3 クライアント |
| 2 | R2 Binding 経由のみ | `[[r2_buckets]] bucket_name="web-fonts"`、同一アカウント内に限定 | 他アカウントからの参照・外部ネットワーク経由・bucket 名推測 |
| 3 | Worker が公開面を制限 | `codedchords.dev/fonts/<file>` のみ・`..` `/` を 400 で拒否 | パストラバーサル・任意キー READ・bucket 列挙 |
| 4 | 長寿命クレデンシャル不在 | R2 API トークン未発行・`.dev.vars`/`wrangler secret`/S3 互換キーなし | GitHub commit・CI ログ・開発機紛失経由のトークン漏洩 |

設計の本質は「ライセンス違反の最大の発生経路 (公開 bucket URL がクローラに
拾われる) を消すこと」。閲覧者の DevTools 経由ダウンロードや第三者ホット
リンクは別レイヤーの話で、Web フォント配信の原理上完全には防げない。

### 最終ソース (記事に貼る分)

`wrangler.toml`:

```toml
name = "coded-chords"
main = "src/index.js"
compatibility_date = "2026-02-17"

[assets]
directory = "./public"
binding = "ASSETS"

[[r2_buckets]]
binding = "FONTS"
bucket_name = "web-fonts"
```

`src/index.js` (26 行):

```js
const FONTS_PREFIX = "/fonts/";

export default {
  async fetch(req, env) {
    const url = new URL(req.url);

    if (url.pathname.startsWith(FONTS_PREFIX)) {
      const key = decodeURIComponent(url.pathname.slice(FONTS_PREFIX.length));
      // Only flat keys in R2 (no subdir, no traversal). Anything else falls
      // through to static assets — the theme also publishes under /fonts/.
      if (key && !key.includes("..") && !key.includes("/")) {
        const obj = await env.FONTS.get(key);
        if (obj) {
          const headers = new Headers();
          obj.writeHttpMetadata(headers);
          headers.set("Content-Type", "font/woff2");
          headers.set("Cache-Control", "public, max-age=31536000, immutable");
          headers.set("ETag", obj.httpEtag);
          return new Response(obj.body, { headers });
        }
      }
    }

    return env.ASSETS.fetch(req);
  },
};
```

## 工程 (作業計画ドラフト)

1. ローカル設定
   - `wrangler.toml` に `main`, `[assets] binding="ASSETS"`,
     `[[r2_buckets]]` を追記
   - `src/index.js` (or `.ts`) を新規作成
   - `.gitignore` に `.wrangler/` を追加
2. CSS 書き換え
   - `static/custom.css` の `d3w0x7oesq9q1.cloudfront.net/` を
     `/fonts/` に置換
3. ローカル検証
   - `npx wrangler dev` で `/fonts/BerkeleyMono-Regular.woff2` を curl
   - 静的アセット (`/` など) が落ちないこと
4. デプロイ
   - main へ push → GitHub Actions の `cloudflare/wrangler-action` で deploy
5. 本番確認
   - Network パネルで同一オリジン配信を確認
   - 描画崩れがないか目視
6. AWS リソース停止 (次フェーズ)
   - CloudFront ディストリビューションを disable → 削除
   - CloudFront Function `restrict-font-access` を解除
   - S3 バケット `berkeley-mono` を空にして削除
   - ACM 証明書(該当があれば)を削除

## 作業ログ・観測値・コマンド出力 (随時追記)

### 落とし穴: テーマと `/fonts/` ネームスペースが衝突

ハンドオフ書通りに `/fonts/<filename>` を R2 に直結すると、テーマ
(tabi) が静的に配信している以下のフォントがすべて 404 になる。

```text
public/fonts/Inter4.woff2
public/fonts/SourceSerif4Variable-Roman.ttf.woff2
public/fonts/CascadiaCode-SemiLight.woff2
public/fonts/KaTeX/*.woff2  (KaTeX サブディレクトリ)
```

対処: Worker は R2 ミス時に `env.ASSETS.fetch(req)` へフォールスルー。
R2 に Berkeley Mono が無ければテーマの `/fonts/` 静的配信に渡す。

`key.includes("/")` の拒否条件も問題で、KaTeX の `KaTeX/KaTeX_AMS-Regular.woff2`
のようなサブディレクトリつきリクエストを 400 で潰してしまうため、
「R2 を試す条件」に降格させ、満たさなければそのまま静的配信に渡す。

教訓: 「同一オリジン化」の代償として URL ネームスペースが
テーマと衝突しやすい。Worker を CDN 風に組むときはフォールスルーを
基本動作にする方が安全。

### Referer 制限を Worker に入れるかの判断

旧構成の CloudFront Function `restrict-font-access` を踏まえ、Worker にも
Referer 許可リストを入れるべきか検討した。結論は **入れない**。

protection-model の保護レイヤは:

- Layer 1: バケットが非公開 (r2.dev 無効・カスタムドメイン未割当・CORS なし)
- Layer 2: R2 Binding 経由のみ。同一 Cloudflare アカウント内に限定
- Layer 3: Worker が公開面を `codedchords.dev/fonts/<file>` に制限し
  `..` や `/` を含むキーを 400 で拒否
- Layer 4: 長寿命クレデンシャル不在 (R2 トークン未発行)

そして protection-model は「第三者サイトからのホットリンクは現状ブロック
していない (Referer は任意で追加可)」と明示している。本質的価値は
「公開 bucket URL がクローラに拾われないこと」であって、リクエスト元
の検査ではない。商用フォントライセンスが求めるのは
「ライセンシー所有ドメインからの same-origin 配信」と
「再配布可能な形で公開しない」の 2 点で、現構成はそれを満たす。

旧構成の Referer 検査は S3 が「世界中から READ 可能な状態」だったために
必要だった補完策で、R2 binding 化により前提自体が消えている。

### デプロイ前の留意点 → 実際にここで詰まった

- GitHub Actions の `CLOUDFLARE_API_TOKEN` は旧構成 (Static Assets only)
  用で発行されており、R2 binding を含む Worker を `wrangler deploy` する
  には Workers R2 Storage の編集権限が必要だった
- 初回 push で `wrangler deploy` が `code: 10000 Authentication error` で
  失敗。`/accounts/***/r2/buckets/web-fonts` への API 呼び出しが弾かれた
- 救いは「デプロイ失敗時は旧 Worker のまま」という Cloudflare Workers の
  原子性。`curl https://codedchords.dev/custom.css` で旧 CloudFront URL が
  まだ配信されていることを確認できた → CloudFront 経由で Berkeley Mono は
  生きており、復旧作業中もサイトは見た目を保てた
- 対応: API トークンを「Edit Cloudflare Workers」テンプレートで再発行し、
  さらに **Account: Workers R2 Storage → Edit** を追加

CI トークンに最終的に付与した権限セット:

| スコープ | パーミッション | 用途 |
|---|---|---|
| Account | Workers Scripts: Edit | Worker スクリプトの deploy |
| Account | Workers R2 Storage: Edit | R2 binding 宣言時の bucket 存在確認 (テンプレ未収載) |
| Account | Account Settings: Read | アカウント情報照会 |
| Zone | Workers Routes: Edit | カスタムルート設定 |
| User | Memberships: Read | `/memberships` API |
| User | User Details: Read | `wrangler whoami` 相当 |

GitHub Secrets `CLOUDFLARE_API_TOKEN` を新トークンで上書きし、失敗ジョブを
再実行:

```bash
DEPLOY_ID=$(gh run list --branch main \
  --workflow="Deploy to Cloudflare Workers" --limit 1 \
  --json databaseId --jq '.[0].databaseId')
gh run rerun "$DEPLOY_ID" --failed
```

教訓: 新しい binding (R2 / D1 / KV / Queues 等) を Worker に追加するときは、
CI トークンの権限を **デプロイ前に** 見直す。Cloudflare 公式の
「Edit Cloudflare Workers」テンプレートは Workers Scripts までで R2 は含まない。

### 本番検証 (deploy 成功後)

```bash
curl -sI https://codedchords.dev/fonts/BerkeleyMono-Regular.woff2
# HTTP/2 200
# content-type: font/woff2
# cache-control: public, max-age=31536000, immutable
# etag: "e11e9fa99f2aead221822f3bb30eb35a"

curl -sI https://codedchords.dev/fonts/Inter4.woff2
# HTTP/2 200  ← テーマ静的フォントへフォールスルー

curl -sI "https://codedchords.dev/fonts/..%2Fevil"
# HTTP/2 404  ← パストラバーサル拒否

curl -sI https://codedchords.dev/fonts/does-not-exist.woff2
# HTTP/2 404  ← R2 ミス → ASSETS で 404
```

### AWS リソース停止

事前確認:

```bash
aws sts get-caller-identity  # Account 376851978118 (yostos-admin)

aws cloudfront list-distributions \
  --query 'DistributionList.Items[*].[Id,DomainName,Enabled]' --output table
# E263MFQG5J21GH  d3w0x7oesq9q1.cloudfront.net  True

aws s3 ls s3://berkeley-mono/ | wc -l  # 21 ファイル
```

#### 1. CloudFront ディストリビューションを disable

```bash
aws cloudfront get-distribution-config --id E263MFQG5J21GH \
  > /tmp/dist-config.json
jq -r '.ETag' /tmp/dist-config.json > /tmp/dist-etag.txt
jq '.DistributionConfig | .Enabled = false' /tmp/dist-config.json \
  > /tmp/dist-config-disabled.json
aws cloudfront update-distribution --id E263MFQG5J21GH \
  --if-match "$(cat /tmp/dist-etag.txt)" \
  --distribution-config "file:///tmp/dist-config-disabled.json"
```

`update-distribution` は `Status: InProgress` を返す。`Status: Deployed` に
なるまで CloudFront の伝播を待つ (実測 約 3 分)。

```bash
until [ "$(aws cloudfront get-distribution --id E263MFQG5J21GH \
  --query 'Distribution.Status' --output text)" = "Deployed" ]; do
  sleep 30
done
```

#### 2. CloudFront ディストリビューション削除

```bash
ETAG=$(aws cloudfront get-distribution --id E263MFQG5J21GH \
  --query 'ETag' --output text)
aws cloudfront delete-distribution --id E263MFQG5J21GH --if-match "$ETAG"
```

#### 3. CloudFront Function `restrict-font-access` 削除

落とし穴: Function は DEVELOPMENT と LIVE の 2 stage を持つ。
`delete-function` は **DEVELOPMENT 側の ETag** を要求する。LIVE 側の ETag
を渡すと `PreconditionFailed`。

```bash
ETAG=$(aws cloudfront describe-function --name restrict-font-access \
  --stage DEVELOPMENT --query 'ETag' --output text)
aws cloudfront delete-function --name restrict-font-access --if-match "$ETAG"
```

#### 4. S3 バケット `berkeley-mono` 削除

```bash
aws s3 rm s3://berkeley-mono --recursive   # 21 オブジェクト
aws s3api delete-bucket --bucket berkeley-mono
```

#### 5. 削除確認

```bash
aws cloudfront list-distributions \
  --query 'DistributionList.Items[?Origins.Items[0].DomainName==`berkeley-mono.s3.ap-northeast-1.amazonaws.com`]'
# []

aws cloudfront list-functions \
  --query 'FunctionList.Items[?Name==`restrict-font-access`]'
# []

aws s3 ls | grep berkeley
# (出力なし)

curl -sI https://codedchords.dev/fonts/BerkeleyMono-Regular.woff2 | head -1
# HTTP/2 200  ← R2 経由で配信継続
```

ACM 証明書は今回 `*.cloudfront.net` デフォルトドメインのまま運用していた
ため発行されておらず、追加削除なし。




## 確定事項

- Worker は JavaScript (`src/index.js`)
- パスプレフィックス: `/fonts/` (R2 ミス時はテーマ静的アセットへフォールスルー)
- バインディング名: `FONTS` / `ASSETS`
- 記事スコープ: R2 移行 + AWS 全停止を 1 本にまとめる
- Referer 制限は不要 (protection-model Layer 1〜4 で要件充足)

## 清書時の構成案 (草稿)

1. 導入: blog-to-zola-aws-cleanup の続編位置付け / 残っていた最後の
   AWS リソースが Berkeley Mono 配信
2. 動機 (Why): 元の要件 (有償フォントの簡単 DL 防止) と、Cloudflare 集約に
   寄せることで「Referer 偽装で守る」前提自体が不要になる話
3. 保護モデル: protection-model の 4 レイヤー表 + 「公開 URL を消すのが本質」
4. 実装: wrangler.toml + src/index.js のソース掲載 + CSS の URL 差し替え
5. 落とし穴 (読者の参考になる順):
   - テーマと `/fonts/` ネームスペース衝突 → ASSETS フォールスルー
   - CI トークンの R2 権限不足 (テンプレ非収載)
   - CloudFront Function 削除は DEVELOPMENT ETag
6. AWS 撤去手順 (コマンド一式)
7. 結び: コスト・運用負荷の差分

## 公開時 TODO

- [ ] draft = false
- [ ] description 確定 (200 文字以内・「。」で完結)
- [ ] cover.webp 生成 (article-cover skill)
- [ ] ogp.webp 生成 (`npm run ogp`)
- [ ] 草稿前メモ・確定事項・清書時の構成案・本 TODO の各ブロックを削除
- [ ] textlint-disable / textlint-enable ラッパも削除
- [ ] 記事冒頭の `{{ image(src="cover.webp", alt="Cover") }}` を追加 -->

<!-- textlint-enable -->

<!-- textlint-enable -->
