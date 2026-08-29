+++
title = "無料で始める Cloudflare セキュリティ対策"
description = "個人ブログにAI Chat機能を追加した翌日、スキャンボットの集中アクセスを確認しました。Cloudflareの無料プランだけで実施できるBot Fight Mode、WAFカスタムルール、Rate Limitingの3つの対策を紹介します。"
date = 2026-03-23
[taxonomies]
tags = ["Tech", "Security"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
tldr = """\
Cloudflare 無料プランで使える Bot Fight Mode、\
WAF カスタムルール（スキャンパス遮断＋許可パス制限）、\
Rate Limiting の3層防御を設定しました。\
公開直後のスキャンアクセスを即日で遮断できています。\
"""
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<!-- more -->

## 公開翌日に何が起きたか

先日の記事で紹介した生成AIを使った[Ask](https://ask.codedchords.dev) ページを公開した翌日、CloudflareのObservabilityを確認したところ、攻撃と思われるリクエストが並んでいました。

- `GET /.env` — 環境変数ファイルの探索
- `/checkout`, `/plans`, `/signup` — SaaS系パスの総当たり
- `/wp-login`, `/wp-admin`, `/xmlrpc.php` — WordPress管理画面の探索
- `/api/v1/stripe/config.js`, `/api/v2/payment/keys.js` — 決済APIの設定ファイル探索（Stripeはオンライン決済プラットフォーム）
- `config.php`, `/api/system/info` — サーバー情報の収集

主にWordPressなどのCMSやStripeなどの決済サービスを狙ったスキャンです。静的サイト＋Workerという構成なのでそんなサービスは乗せていないのですが。公開されているエンドポイントに対してよく狙われる既知のパスを片っ端から叩いているのでしょう。

実害はありませんが、放置するのも気持ちが悪いですし、Workers AIのNeuronsを無駄に消費されるのは避けたいところです。Cloudflareの無料プランのセキュリティ機能で対策しました。

## 対策1: Bot Fight Mode

最も手軽な対策です。Cloudflareダッシュボードの **Security > Bots** から、ワンクリックで有効化できます。

Bot Fight ModeはCloudflareが持つボットの行動パターンデータベースを使い、自動化されたアクセスを検出して計算コストの高いチャレンジを返します。検索エンジンのクローラーなど検証済みの正当なボットは通過させる仕組みです。

設定はON/OFFだけで、細かなチューニングは有料プラン（Super Bot Fight Mode）の機能になります。それでも、汎用的なスキャンボットの大半はこれで弾けます。

注意点として、Bot Fight Modeは外部サービスからのWebhookやRSSリーダーのフィード取得など、正当な自動アクセスもブロックする場合があります。無料プランではWAFルールによるバイパス（Skip）ができないため、これらのサービスに影響が出た場合はBot Fight Mode自体を無効にする必要があります。

## 対策2: WAF カスタムルール

Bot Fight Modeをすり抜けるアクセスに対しては、WAF（Web Application Firewall）のカスタムルールで対処します。無料プランでは5つまでルールを作成できます。

### ルール1: 許可パスの制限（ホワイトリスト）

最も効果が高いルールを最優先に配置します。ask.codedchords.devは `/`（フロントエンド）と `/api/`（Workers API）しか使わないので、それ以外を全てブロックします。

```text,name=Expression
(http.host eq "ask.codedchords.dev")
and not (http.request.uri.path eq "/" or http.request.uri.path contains "/api/")
```

Actionは **Block**、Place atは **First** に設定します。

「正当なパスだけを許可する」ホワイトリスト方式なので、攻撃者がどんなパスを試してもすり抜けられません。ただし、対象サイトの構成を把握している必要があります。新しいパスを追加した際にルールの更新を忘れると自分自身のコンテンツがブロックされるため、サイト構成を変更したらルールも見直してください。

### ルール2: スキャンパスの遮断（ブラックリスト）

ルール1はaskサブドメイン限定なので、ドメイン全体に適用する汎用ルールも設定します。WordPressやphpMyAdminなど、よく狙われるパスへのアクセスを一括でブロックします。

**Security > Security rules > Create rule** から、以下のExpressionを設定します。

```text,name=Expression
(http.request.uri.path contains ".env")
or (http.request.uri.path contains "wp-login")
or (http.request.uri.path contains "wp-admin")
or (http.request.uri.path contains "xmlrpc.php")
or (http.request.uri.path contains "phpmyadmin")
or (http.request.uri.path contains "wp-content")
or (http.request.uri.path contains "wp-includes")
```

Actionは **Block** です。

このルールはサイトの構成に依存しないため、Cloudflareで管理しているドメイン全体に適用できます。WordPressを使っていないサイトであれば、デメリットはありません。

## 対策3: Rate Limiting

Bot Fight ModeとWAFルールを通過したリクエストに対する最後の砦です。同一IPからの過剰なリクエストを制限します。

**Security > Security rules > Rate limiting rules** から設定します。

| 項目     | 設定値                               |
| -------- | ------------------------------------ |
| 対象     | `http.host eq "ask.codedchords.dev"` |
| 判定基準 | IP                                   |
| レート   | 10リクエスト / 10秒                  |
| Action   | Block（10秒間）                      |

無料プランではRate Limitingルールは1つまで、ブロック期間は最大10秒という制約があります。大規模な攻撃には有料プランのRate Limiting（より長いブロック期間、より多くのルール）が必要ですが、スキャンボット対策としては十分です。上記の設定値は一例です。ページ内のリソース数や想定されるアクセスパターンに応じて調整してください。

なお、今回はWorkers側にも `/api/ask` エンドポイントに対して同一IP 60秒間10リクエストの制限を入れています。CloudflareのRate Limitingはインフラ層での粗いフィルタリング、Workers側はアプリケーション層での細かな制御という役割分担です。

## 3層防御の全体像

設定した対策を整理します。

| レイヤー | 対策               | 役割                           |
| -------- | ------------------ | ------------------------------ |
| 第1層    | Bot Fight Mode     | 既知のボットパターンを自動検出 |
| 第2層    | WAF カスタムルール | 不正なパス・不要なパスを遮断   |
| 第3層    | Rate Limiting      | 過剰なリクエストを制限         |

いずれもCloudflareの無料プランで利用でき、設定はダッシュボードからの操作だけで完結します。

## まとめ

これらの設定を適用した直後から、Observability上でスキャン系のリクエストがブロックされていることを確認できました。Workers AIのNeuronsが無駄に消費されることもなくなっています。

個人サイトであっても、公開すればスキャンボットは来ます。「小規模だから狙われない」ということはありません。ボットは規模を問わず、見つけたエンドポイントを片っ端から叩きます。

Cloudflareを使っているなら、無料プランの範囲でもBot Fight Mode、WAFカスタムルール、Rate Limitingの3つを設定するだけで、大半の自動化されたスキャンは防げます。設定にかかる時間は10分程度です。特にWorkers AIやAPIエンドポイントを公開している場合は、不要なリクエストによるリソース消費を防ぐためにも早めの対策をおすすめします。

## References

<!-- textlint-disable -->

{% references() %}

- [Cloudflare](https://developers.cloudflare.com/bots/get-started/free/). "Bot Fight Mode"
- [Cloudflare](https://developers.cloudflare.com/waf/custom-rules/). "Custom rules"
- [Cloudflare](https://developers.cloudflare.com/waf/rate-limiting-rules/). "Rate limiting rules"

{% end %}

<!-- textlint-enable -->
