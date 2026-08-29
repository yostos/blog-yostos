+++
title = "技術文書用フォーマット AsciiDoc"
description = """
ソースコードの解説を含む技術文書を書く必要があり、AsciiDocとその処理系Asciidoctorを
導入しました。Markdownが標準となった今あえてAsciiDocを選ぶ理由と、
Mac環境での導入手順、実際の変換サンプルを紹介します。
"""
date = 2026-07-10T05:00:00+09:00
[taxonomies]
tags = ["Tech", "Documentation"]
[extra]
social_media_card = "ogp.webp"
local_image = "cover.webp"
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="Cover") }}

<!-- textlint-enable -->

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

<!-- more -->

AsciiDocで書かれたドキュメントを修正する必要があったので、
AsciiDoctorを導入しました。

## AsciiDocとは

AsciiDocは、2002年にStuart Rackham氏が開発したマークアップ言語です。
もともとはDocBook XMLを人間が書きやすい記法で表現するためのPython製ツールとして
誕生しました。プレーンテキストで書いた文書を、HTMLやPDF、EPUBなど複数の形式に
変換できる点が特徴です。

2013年にはRuby実装のAsciidoctorが登場し、現在ではこちらが主流の処理系となっています。
本記事でも、AsciiDocの処理系としてAsciidoctorを使用します。

2019年からはEclipse Foundation傘下の
AsciiDoc Working Groupによって言語仕様の標準化も進められており、
処理系間の互換性が高まりつつあります。

ただし、技術文書での採用率では明確にMarkdownが優位です。
技術文書作成者の主要フォーマットとしてMarkdownを使う割合が约65%とされ、デファクトスタンダードの地位にあります。学習コストの低さとツールの豊富さ、生成AIで扱う文書形式の標準となっていることが理由です。
実際にはAsciiDocは全体の採用率では大きく水を開けられています。

## MacへのAsciiDocの導入

AsciiDocの処理系としてAsciiDoctorを使用します。

ランタイムにRubyを使用するので、Rubyのインストールから行っています。
前提として、私の環境では
[mise](https://mise.jdx.dev)で言語のバージョンを管理しています。

```sh,name=install.sh
# Rubyのインストール
mise use -g ruby@latest
gem install asciidoctor asciidoctor-pdf asciidoctor-rouge
gem install asciidoctor-pdf-cjk asciidoctor-diagram
```

## AsciiDocのサンプル

似たようなマークアップ言語にMarkdownがありますが、
以下のような点でAsciiDocが優れているので作る文書の特性で
使い分けています。

- 目次や表紙の生成が可能
- 細かいテーブルの表現が可能
- ソースコードにシンタックスハイライトや吹き出しが使える

GitHubやGitLabでもネイティブでAsciiDocのレンダリングに対応しています。
始めからHTMLやPDFへの変換を意識して作られている点でも優れています。

次にサンプルを提示します。
Frontmatterを除くと、ソースのままでも読みやすい形式です。
特に今回はソースコードの解説だったので、以下の例ではソースコードへの解説を追記する例となっています。

```asciidoc,name=sample.adoc
= サンプル
:toc: left
:toc-title: 目次
:toclevel: 4
:imagesdir: images
:figure-caption: 図
:chapter-signifier:
:scripts: cjk
:pdf-theme: default-with-font-fallbacks
:doctype: book
:sectnumlevels: 4
:sectnums:
:source-highlighter: rouge
:rouge-style: gruvbox

== Hello World

.hello.py
[source,python]
----
print("Hello World!")  <1>

i = 3

if i == 1:             <2>
  print("i = 1")
elif i == 2:
  print("i = 2")
elif i == 3:
  print("i = 3")
else:
  print("i = 4")

----
<1> やっぱりサンプルといえばコレな
<2> IF文です！
```

## AsciiDocを変換する

作成したAsciiDocのソースは以下のコマンドでHTMLやPDFに変換します。

```sh,name=convert.sh
# HTMLの生成
asciidoctor --backend html5 sample.adoc -o sample.html
# PDFの生成
asciidoctor-pdf sample.adoc -o sample.pdf
```

以下が生成したサンプルです。

<!-- textlint-disable -->

{{ image(src="sample.webp", alt="AsciiDoc生成結果") }}

<!-- textlint-enable -->

## まとめ

AsciiDocは
Markdownと似ているので混乱する部分もありますが、
Markdownよりやりたいことをストレートに書けると思います。

サンプルのようにAsciiDocのメタデータにいろいろ記載すると生成するスタイルも
変更できるのでいろんな文章に柔軟に対応できると思います。
