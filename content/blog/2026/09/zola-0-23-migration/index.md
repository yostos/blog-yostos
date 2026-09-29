+++
title = "Zola 0.23とtabi v5への移行"
description = """
このブログを動かしている静的サイトジェネレーターZolaが0.23になり、作者自ら「最も破壊的なバージョン」と呼ぶ変更が入りました。記事の中で使っていたショートコードも書き換えが必要です。テーマのtabiとあわせて、このブログを移行してみます。
"""
date = 2026-09-29
[extra]
social_media_card = "ogp.webp"
local_image = "cover.avif"

[taxonomies]
tags = ["Tech", "Weblog"]
+++

<!-- textlint-disable -->

{{< image src="cover.avif" alt="Cover" />}}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

このブログは静的サイトジェネレーターのZolaと、そのテーマであるtabiで作っています。tabiに更新が来ていないか確認したところ、最新のv5.0.0はZola 0.23を必須にしていました。Zola 0.23は、作者自身が「おそらくZolaで最も破壊的なバージョン」と書くほど大きな変更を含んでいます。この記事では、Zola 0.23とtabi v5で何が変わったのかを整理し、今回のバージョンアップがユーザーにとってどういう意味を持つのかを考えます。

## Zola 0.23の変更点

Zola 0.23.0は2026年8月5日に公開されました。最大の変更は、テンプレートエンジンのTeraがv2に上がったことと、それに伴ってショートコードが廃止されたことです。

これまでのZolaでは、Markdownの本文に書けるのはショートコードだけで、テンプレート側の部品はマクロという別の仕組みで書いていました。0.23では本文そのものがTeraで処理されるようになり、ショートコードとマクロはTera 2の「コンポーネント」に一本化されました。同じコンポーネントを、テンプレートからも記事の本文からも呼び出せます。

記事の中での書き方は次のように変わります。

```text
{% raw %}# 旧: インライン
{{ youtube(id="dQw4w9WgXcQ", autoplay=true) }}
# 新: インライン
{{< youtube id="dQw4w9WgXcQ" autoplay={true} />}}

# 旧: 本文を持つブロック
{% quote(author="Vincent") %}
A quote
{% end %}
# 新: 本文を持つブロック
{% <quote author="Vincent"> %}
A quote
{% </quote> %}{% endraw %}
```

{% raw %}`{{ }}`の中に`< />`を重ねた形は冗長に見えますが、それぞれに役割があります。`{{ }}`や`{% %}`はTeraに処理させる箇所の目印で、これがないとTeraは中身を見ません。`{{ }}`は従来どおり式の出力にも使うため、{% endraw %}`< />`で「式ではなくコンポーネントの呼び出し」であることを区別しています。Teraの移行ガイドによると、この書き方はJinjaXから着想を得たJinja2とJSXの折衷です。引数もJSXと同じ考え方で、文字列以外の値は`{true}`のように波括弧で囲みます。

本文全体がテンプレートとして処理されるようになったことには、副作用もあります。記事の中にそのまま{% raw %}`{{ }}`や`{% %}`{% endraw %}を書くと、コードブロックの中であってもTeraが解釈しようとしてエラーになります。GitHub Actionsの{% raw %}`${{ secrets.X }}`{% endraw %}を載せた記事などは、<code>&#123;% raw %&#125;</code>と<code>&#123;% endraw %&#125;</code>で囲む必要があります。ファイル単位で処理を止める`skip_content_templating`という設定も追加されました。

ショートコードの廃止以外にも、0.23では多くの機能が追加されました。このブログに関係しそうなものを挙げます。

- これまで`@/`で始まるリンクではMarkdownしか指せなかったが、画像ファイルも対象となった。これにより他の記事の画像を`@/`リンクで指定できる
- ページやセクションに`hidden`を指定すると、一覧から除外できる
- フロントマターの`include_in_feeds`で、個別の記事をRSSやAtomのフィードから外せる
- 読了時間の計算が言語ごとの読む速さを使うようになった
- `get_page`や`get_section`に、対象がなくてもエラーにしない`allow_missing`引数が付いた
- シンタックスハイライトの配色を定義するCSSは、これまでサイト直下の`static/`に生成され、ビルド時に出力先の`public/`へコピーされていた。0.23からは`public/`に直接生成され、`static/`には書き出されなくなった

## tabi v5の変更点

Zola 0.23に対応したtabi v5.0.0は、2026年9月13日にリリースされました。

v5.0.0では、テーマが提供していたショートコードがすべてコンポーネントに置き換わり、テンプレートの内部で使っていたマクロもなくなりました。記事から`admonition`や`references`などを呼び出す書き方も、Zola 0.23の構文に変わります。

```text
{% raw %}# 旧
{% admonition(type="warning", title="注意") %}
ここに警告メッセージを書きます。
{% end %}

{% references() %}
- [サイト名](URL). 「記事タイトル」
{% end %}

# 新
{% <admonition type="warning" title="注意"> %}
ここに警告メッセージを書きます。
{% </admonition> %}

{% <references> %}
- [サイト名](URL). 「記事タイトル」
{% </references> %}{% endraw %}
```

あわせて、後方互換のためだけに残されていた設定が廃止されました。日付の書式も、`%Y-%m-%d`のようなstrftimeの形式ではなく、`y-MM-dd`のようなUnicodeの書式（UTS #35）で書く必要があります。こうした設定やテンプレートの書き換え方は、作者がtabiのサイトで移行ガイドとしてまとめています。

## まとめ

Zola 0.23は、テーマやテンプレートを書く人にとっては大きな改善です。ショートコードとマクロに分かれていた部品がコンポーネントに一本化され、同じ部品をテンプレートと記事の両方から呼び出せるようになりました。引数に型を付けられるので、渡す値の誤りはビルド時にエラーとして見つかります。Tera 2ではオプショナルチェーンや三項演算子なども使えるようになり、エラーメッセージも呼び出し元までたどれる形になりました。

一方で、記事を書くだけの立場では、恩恵を感じる場面はあまりありません。呼び出しは{% raw %}`{{< name ... />}}`{% endraw %}という長い書き方になり、本文全体がテンプレートとして処理されるため、コード例に{% raw %}`{{ }}`{% endraw %}が出てくるたびに`raw`で囲む手間も増えました。記事から使える機能の追加や、サイトの言語を`ja`にすれば日本語の読む速さで読了時間を計算してくれる点はありがたいものの、既存の記事をすべて書き換える作業量に見合うほどではありません。

## References

<!-- textlint-disable -->

{% <references> %}

- [getzola/zola](https://github.com/getzola/zola/blob/master/CHANGELOG.md). "CHANGELOG"
- [Keats/tera](https://github.com/Keats/tera/blob/master/MIGRATION.md). "v1 -> v2 migration guide"
- [welpo/tabi](https://github.com/welpo/tabi/blob/main/CHANGELOG.md). "CHANGELOG"
- [tabi](https://welpo.github.io/tabi/blog/upgrading-to-zola-0-23/). "Upgrade your tabi site to Zola 0.23"

{% </references> %}

<!-- textlint-enable -->
