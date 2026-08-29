+++
title = "ブログ記事をBlueskyに自動投稿する — GitHub Actions + AT Protocol"
description = """\
ブログの新規記事をmainにpushするだけで、Blueskyに自動投稿される\
仕組みをGitHub ActionsとAT Protocol APIで構築しました。\
git diffによる新規記事の判定、リンクカード付き投稿、\
ハッシュタグのfacet生成まで、シェルスクリプト一本で実現しています。\
"""
date = 2026-03-18
[taxonomies]
tags = ["Tech", "Weblog"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
tldr = """\
GitHub Actionsでmainへのpush時にgit diffで新規記事を検出し、\
Bluesky AT Protocol APIでリンクカード付き投稿を行うように自動化しました。\
"""
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<!-- more -->

## なぜBlueskyなのか

Blueskyは、AT Protocolという分散型プロトコル上に構築されたSNSです。ブログの告知先としてSNSを選ぶなら、X（旧Twitter）が最初の候補に挙がるかもしれません。しかし、XのAPIは2023年に有料化され、無料プランでは月1,500件の投稿しかできません。自動投稿の仕組みを維持するために月額の課金が必要になります。rate limitも厳しく、突然の仕様変更で動かなくなるリスクも無視できません。そもそも、a chaotic messと化したプラットフォームに技術記事の告知を流す意味があるのかという根本的な疑問もあります。

一方、BlueskyのAT Protocol APIは完全に無料で、認証もアプリパスワード1つで済みます。プロトコル仕様が公開されており、`curl` で直接叩ける素朴さがあります。個人ブログの告知先としては、APIの安定性とコストの両面でBlueskyに優位性があると判断しました。

## 手動投稿の煩わしさ

ブログ記事を書き上げてpushした後、Blueskyを開いてURLを貼り、説明文を添えて投稿する。この手作業は1分で終わりますが、毎回やるのは面倒です。忘れることもあります。

このブログはZolaで生成し、Cloudflare Pagesでホスティングしています。記事の公開は `git push origin main` で完了します。であれば、Blueskyへの告知もこのpushをトリガーにして自動化するのが自然な流れです。

## なぜGitHub Actionsなのか

自動投稿の実現方法について、いくつか検討してみました。

1.Cloudflare Worker + Deploy Hook

- インフラをCloudflareで統一できる利点があるが、「新規記事かどうか」の判定にKV等の状態管理が必要になる。

2. ローカルのフック（Claude Code Hookなど）

- シンプルだが、別マシンからの投稿時に動作しない。また、GitHub Actionの完了との同期が面倒である。

3. IFTTT/Zapier等のSaaS

- 簡単だが、RSSベースのため遅延が発生する。また、プライバシーの懸念もある。

結局、GitHub Actionsへ組み込むことにしました。

GitHub Actionsを選んだ決め手は、`git diff` が使えることです。`git diff --name-status HEAD~1 HEAD` の出力で `A`（Added）ステータスかつ `content/**/index.md` に一致するファイルを検出すれば、新規記事だけを正確に判別できます。更新や削除では発動しません。

## 仕組みの全体像

処理フローはシンプルです。

1. mainブランチへのpushでワークフローが起動
2. `git diff` で新規記事（`A` ステータスの `index.md`）を検出
3. frontmatter（TOML形式）からtitle、description、tagsを抽出
4. Bluesky AT Protocol APIで認証
5. OGP画像を `com.atproto.repo.uploadBlob` でアップロード
6. リンクカード（サムネイル付き）のポストを作成

ワークフローとスクリプトの2ファイル構成です。

## ワークフロー

ワークフローは新規記事の検出と、スクリプトの呼び出しに責務を限定しています。

<!-- textlint-disable -->

```yaml,name=.github/workflows/bluesky-post.yml
name: Post to Bluesky

on:
  push:
    branches: [main]
    paths: ['content/**']

jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 2

      - name: Detect new articles
        id: detect
        run: |
          new_articles=$(git diff --name-status HEAD~1 HEAD \
            | grep '^A' \
            | awk '{print $2}' \
            | grep 'content/.*/index\.md$' || true)
          if [ -z "$new_articles" ]; then
            echo "No new articles found"
            echo "has_new=false" >> "$GITHUB_OUTPUT"
          else
            echo "New articles found:"
            echo "$new_articles"
            {
              echo "articles<<EOF"
              echo "$new_articles"
              echo "EOF"
            } >> "$GITHUB_OUTPUT"
            echo "has_new=true" >> "$GITHUB_OUTPUT"
          fi

      - name: Post to Bluesky
        if: steps.detect.outputs.has_new == 'true'
        env:
          BLUESKY_IDENTIFIER: ${{ secrets.BLUESKY_IDENTIFIER }}
          BLUESKY_APP_PASSWORD: ${{ secrets.BLUESKY_APP_PASSWORD }}
          NEW_ARTICLES: ${{ steps.detect.outputs.articles }}
        run: |
          echo "$NEW_ARTICLES" | while IFS= read -r article; do
            [ -z "$article" ] && continue
            bash scripts/bluesky-post.sh "$article"
          done
```

<!-- textlint-enable -->

`fetch-depth: 2` で直前のコミットとの差分を取得できるようにしています。`paths: ['content/**']` でcontent配下に変更がないpush（設定ファイルの変更など）ではワークフロー自体が起動しません。

## 投稿スクリプト

投稿スクリプトは `curl` と `jq` だけで動作します。外部ライブラリは不要です。

処理は大きく5段階に分かれています。

**frontmatterの抽出。** `sed` でTOMLのfrontmatter領域（`+++` で囲まれた部分）を取り出し、title、description、tags、`social_media_card`（OGP画像パス）を個別にパースします。descriptionはTOMLの複数行文字列（`"""`）にも対応しています。

**投稿テキストの生成。** フォーマットは以下の通りです。

```text
📝 Just published:

#blog #tag1 #tag2
```

descriptionはリンクカードに表示されるため、テキスト本文には含めません。`#blog` は固定で付与し、記事のタグから最大5個のハッシュタグを追加します。スペースを含むタグ（"Generative AI" など）はBlueskyのハッシュタグとして機能しないためスキップします。

**Facetの生成。** Blueskyでハッシュタグをクリック可能にするには、テキスト中の `#tag` の位置をUTF-8バイトオフセットで指定する `facet` が必要です。`wc -c` でバイト位置を算出し、`app.bsky.richtext.facet#tag` を設定しています。

**OGP画像のアップロード。** frontmatterの `social_media_card` で指定されたOGP画像を `com.atproto.repo.uploadBlob` でBlueskyにアップロードし、blobリファレンスを取得します。アップロードに失敗した場合はサムネイルなしで投稿を続行します。

**APIの呼び出し。** `com.atproto.server.createSession` でセッションを作成し、`com.atproto.repo.createRecord` でポストを作成します。リンクカードは `app.bsky.embed.external` で埋め込み、アップロード済みのOGP画像を `thumb` フィールドに設定します。

## リンクカードについて

Blueskyは投稿時にURLからOGPを自動取得しません。リンクカードを表示するには、投稿APIで `app.bsky.embed.external` を明示的に指定する必要があります。サムネイル画像を表示するには、事前に `com.atproto.repo.uploadBlob` で画像をアップロードし、返却されたblobリファレンスを `thumb` フィールドに設定します。

```json
"embed": {
  "$type": "app.bsky.embed.external",
  "external": {
    "uri": "https://codedchords.dev/blog/2026/03/bluesky-auto-post/",
    "title": "記事タイトル",
    "description": "記事の説明文",
    "thumb": { "$type": "blob", ... }
  }
}
```

このスクリプトでは、frontmatterの `social_media_card` で指定されたOGP画像（WebP/PNG/JPEG対応）をアップロードしています。画像のアップロードに失敗した場合でも、サムネイルなしのリンクカードとして投稿が作成されるようにフォールバック処理を入れています。

## GitHub Secretsの設定

ワークフローで使用するシークレットは2つです。

- `BLUESKY_IDENTIFIER` — Blueskyのハンドル
- `BLUESKY_APP_PASSWORD` — Blueskyのアプリパスワード（設定画面から生成）

アプリパスワードはアカウントのパスワードとは別物で、権限を限定して発行できます。

## まとめ

`git push` から自動的にBlueskyへ投稿される仕組みを、GitHub Actionsとシェルスクリプトで構築しました。OGP画像のサムネイル付きリンクカードまで含めて、外部ライブラリに依存せず `curl` と `jq` だけで完結しています。この記事自体が最初の自動投稿テストです。

<!-- textlint-disable -->

## References

{% references() %}

- [Bluesky](https://docs.bsky.app/docs/advanced-guides/posts). "Sending Post with the Bluesky API"
- [AT Protocol](https://atproto.com/specs/xrpc). "XRPC Specification"

{% end %}

<!-- textlint-enable -->
