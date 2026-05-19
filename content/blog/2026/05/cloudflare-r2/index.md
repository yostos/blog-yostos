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

### デプロイ前の留意点

- GitHub Actions の `CLOUDFLARE_API_TOKEN` は元々 Static Assets 用で
  発行されている。`[[r2_buckets]]` バインディングを含む Worker を
  `wrangler deploy` するには Workers R2 Storage の編集権限が必要。
  CI で deploy が失敗した場合はトークン権限を見直す



## 確定事項 / 未確定事項

確定:

- Worker は JavaScript (`src/index.js`)。ハンドオフ書で確定済。
- パスプレフィックス: `/fonts/`
- バインディング名: `FONTS` / `ASSETS`
- 容易には壊れない置き換え: 公開 URL を持たない R2 binding 経由なので
  Referer 制限・API キー・CORS が全て不要

未確定:

- AWS リソース停止 (S3 + CloudFront + CloudFront Function) を
  本記事に含めるか別記事にするか
- 記事タイトル / description (最終調整は公開直前)

<!-- 公開直前に: draft=false, description確定, cover.webp/ogp.webp 生成 -->

<!-- textlint-enable -->
