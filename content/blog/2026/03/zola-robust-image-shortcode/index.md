+++
title = "CLS改善のためにZolaの画像ショートコードを自作した"
description = """\
Zolaで構築したブログのCLS（Cumulative Layout Shift）を改善するため、\
画像サイズを自動取得するショートコードを作成しました。\
実装の詳細と、caption対応によるfigure要素の出力まで解説します。"""
date = 2026-03-01T06:35:31+09:00
[taxonomies]
tags = ["Tech", "Weblog"]
[extra]
social_media_card = "ogp.webp"
local_image = "cls.webp"
tldr = """\
Zolaの画像にwidth/heightが未設定でCLSが悪化していたため、\
get_image_metadataで画像サイズを自動取得するショートコードを作成しました。\
caption指定時にはfigure/figcaption要素を出力します。"""
+++

<details>
<summary>Table of Contents</summary>
<!-- toc -->
</details>

## CLSとは

Cloudflare Pagesにブログを移行したことで、Cloudflare Web Analyticsが利用できるようになりました。アクセス数だけでなくCore Web Vitalsの各指標も確認できるのですが、そのなかでCLS（Cumulative Layout Shift）のスコアが気になる結果でした。

<!-- textlint-disable -->

{{ image(src="cls.webp", alt="CLS", caption="Cloudflare Web Analytics画面") }}

<!-- textlint-enable -->

Core Web VitalsはGoogleが提唱するWebページのユーザー体験を測定する指標群で、LCP（Largest Contentful Paint：読み込み速度）、INP（Interaction to Next Paint：応答性）、CLS（Cumulative Layout Shift：視覚的安定性）の3つで構成されます。いずれもGoogleの検索ランキングに影響するため、サイト運営者にとって無視できない指標です。

CLSはページの読み込み中にコンテンツが予期せずずれる現象を数値化したもので、0.1以下が「良好」とされています。CLSが悪化する代表的な原因は、画像や広告などの要素にサイズ（`width`と`height`）が指定されていないことです。サイズが未指定の画像は、読み込まれるまでブラウザが表示領域を確保できません。画像の読み込みが完了した瞬間にページ全体がガクッとずれてしまい、ユーザーが読んでいた箇所を見失うことになります。

私のブログを調べてみると、ほぼすべての記事画像に`width`と`height`が設定されていませんでした。

## 画像要素の改善

このブログは静的サイトジェネレーターのZolaを使用しており、記事はMarkdownで書いています。Markdownの画像記法は以下のとおりですが、`width`や`height`などのメタ情報を記述する手段がありません[^1]。

```Markdown
![カバー画像](cover.jpg)
```

[^1]:
    ZolaはCommonMarkをベースとしたpulldown-cmarkというRustのライブラリ
    を使用しているため画像にメタ情報を付与できませんが、Markdownの処理系によっては記述可能なものも存在します。

そこでZolaのショートコードを利用して、画像サイズなどのメタ情報を自動でセットする仕組みを作りました。以下はコードの抜粋です。

<!-- textlint-disable -->

```html,name=templates/shortcodes/image.html
{{ remote_text(src="templates/shortcodes/image.html", start=37, end=43) }}
```

<!-- textlint-enable -->

Zolaの`get_image_metadata`関数はビルド時に画像ファイルを読み取り、幅と高さを返してくれます。これを利用して`width`と`height`を`img`要素に指定しています。あわせて`get_url`関数の`cachebust=true`オプションでファイルのハッシュ値をURLに付与し、キャッシュバスティングにも対応しました。

あとはHTMLの`img`要素として画像サイズが出力されるように組み立てるだけです。

<!-- textlint-disable -->

```html,name=templates/shortcodes/image.html
{{ remote_text(src="templates/shortcodes/image.html", start=89, end=95) }}
```

<!-- textlint-enable -->

この結果、記事には以下のように書くだけで、画像サイズとキャッシュバスティングに対応した`img`要素を自動出力できるようになりました。

<!-- textlint-disable -->

```Markdown
{{ remote_text(src="example-usage.txt") }}
```

<!-- textlint-enable -->

Zola依存にはなりますが、記述を複雑にせずCLS対策ができました。

## figure対応

記事内の画像にキャプションを付けたい場合もあります。そこで`caption`パラメータが指定された場合には、`img`要素を`figure`要素で囲み、`figcaption`要素でキャプションを出力するようにしました。`caption`を省略した場合は従来どおり`img`要素のみを出力します。

以下がショートコードの全容です。

<details>
  <summary>imageショートコード</summary>
<!-- textlint-disable -->

```html,name=templates/shortcodes/image.html
{{ remote_text(src="templates/shortcodes/image.html") }}
```

  <!-- textlint-enable -->

</details>

## References

<!-- textlint-disable -->

{% references() %}

- web.dev. 「[Cumulative Layout Shift (CLS)](https://web.dev/articles/cls)」
- web.dev. 「[Core Web Vitals](https://web.dev/articles/vitals)」
- Zola. "[Shortcodes](https://www.getzola.org/documentation/content/shortcodes/)"
- Zola. "[Overview - get_image_metadata](https://www.getzola.org/documentation/templates/overview/#get-image-metadata)"
  {% end %}

<!-- textlint-enable -->
