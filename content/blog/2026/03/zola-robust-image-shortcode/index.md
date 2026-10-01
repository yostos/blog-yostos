+++
title = "CLS改善のためにZolaの画像ショートコードを自作した"
description = """\
Zolaで構築したブログのCLS（Cumulative Layout Shift）を改善するため、\
画像サイズを自動取得するショートコードを作成しました。\
実装の詳細と、caption対応によるfigure要素の出力まで解説します。"""
date = 2026-03-01T06:35:31+09:00
updated = 2026-10-01
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

{{< image src="cls.webp" alt="CLS" caption="Cloudflare Web Analytics画面" />}}

<!-- textlint-enable -->

Core Web VitalsはGoogleが提唱するWebページのユーザー体験を測定する指標群で、LCP（Largest Contentful Paint：読み込み速度）、INP（Interaction to Next Paint：応答性）、CLS（Cumulative Layout Shift：視覚的安定性）の3つで構成されます。いずれもGoogleの検索ランキングに影響するため、サイト運営者にとって無視できない指標です。

CLSはページの読み込み中にコンテンツが予期せずずれる現象を数値化したもので、0.1以下が「良好」とされています。CLSが悪化する代表的な原因は、画像や広告などの要素にサイズ（`width`と`height`）が指定されていないことです。サイズが未指定の画像は、読み込まれるまでブラウザが表示領域を確保できません。画像の読み込みが完了した瞬間にページ全体がガクッとずれてしまい、ユーザーが読んでいた箇所を見失うことになります。

私のブログを調べてみると、ほぼすべての記事画像に`width`と`height`が設定されていませんでした。

## 画像要素の改善

<!-- textlint-disable -->

{% <admonition type="warning" title="Zola 0.23以降をお使いの方へ"> %}
この記事で紹介しているコードと記法はZola 0.22以前のものです。Zola 0.23でショートコードは廃止されたため、このままでは動作しません。0.23に対応したコードは、記事末尾の「Zola 0.23でコンポーネントへ移植」を参照してください。
{% </admonition> %}

<!-- textlint-enable -->

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
{{< remote_text src="image-shortcode.txt" start={37} end={43} />}}
```

<!-- textlint-enable -->

Zolaの`get_image_metadata`関数はビルド時に画像ファイルを読み取り、幅と高さを返してくれます。これを利用して`width`と`height`を`img`要素に指定しています。あわせて`get_url`関数の`cachebust=true`オプションでファイルのハッシュ値をURLに付与し、キャッシュバスティングにも対応しました。

あとはHTMLの`img`要素として画像サイズが出力されるように組み立てるだけです。

<!-- textlint-disable -->

```html,name=templates/shortcodes/image.html
{{< remote_text src="image-shortcode.txt" start={89} end={95} />}}
```

<!-- textlint-enable -->

この結果、記事には以下のように書くだけで、画像サイズとキャッシュバスティングに対応した`img`要素を自動出力できるようになりました。

<!-- textlint-disable -->

```Markdown
{{< remote_text src="example-usage.txt" />}}
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
{{< remote_text src="image-shortcode.txt" />}}
```

  <!-- textlint-enable -->

</details>

## Zola 0.23でコンポーネントへ移植

2026年8月に公開されたZola 0.23で、テンプレートエンジンのTeraがv2に上がり、ショートコードは廃止されました。ショートコードとマクロはTera 2の「コンポーネント」に一本化され、記事からの呼び出し方も変わっています。変更の全体は「[Zola 0.23とtabi v5への移行](@/blog/2026/09/zola-0-23-migration/index.md)」にまとめました。

この画像ショートコードも`templates/components/image.html`へ移し、コンポーネントとして書き直しました。記事からは次のように呼び出します。

```Markdown
{% raw %}{{< image src="cover.jpg" alt="カバー画像" />}}{% endraw %}
```

Tera 2に合わせて書き換えた点は次のとおりです。

- ファイル全体を{% raw %}`{% component image(...) %}`と`{% endcomponent image %}`{% endraw %}で囲み、引数とデフォルト値を宣言した。`alt | default(value="")`のような既定値の処理は不要になった
- テストの引数は名前付きが必須になったため、`starting_with("http")`を`starting_with(pat="http")`に変えた
- trim系フィルタの統合にあわせて、`trim_start_matches`を`trim_start`に変えた
- Tera 2は未定義の変数を参照するとエラーになるため、`meta`を最初に`{}`で初期化した
- 記事ディレクトリは、`@page`暗黙引数で受け取ったページの`relative_path`から求めるようにした。`@page`には呼び出し側で渡さなくても呼び出し元の`page`が自動で入る

もう1つ、出力の組み立て方も変える必要がありました。ショートコードの出力はMarkdownの変換後に差し込まれていましたが、コンポーネントの出力はMarkdownの変換前に本文へ埋め込まれます。旧コードのように`<img`を複数行に分けて出力すると、CommonMarkはこれをHTMLブロックとみなさず、`<p>`要素で囲んでしまいます。そこで`<img>`要素を`set`ブロックで1行に組み立て、`safe`フィルタで出力するようにしました。

<!-- textlint-disable -->

```html,name=templates/components/image.html
{{< remote_text src="image-component.txt" start={72} end={81} />}}
```

<!-- textlint-enable -->

以下がコンポーネントの全容です。

<details>
  <summary>imageコンポーネント</summary>
<!-- textlint-disable -->

```html,name=templates/components/image.html
{{< remote_text src="image-component.txt" />}}
```

  <!-- textlint-enable -->

</details>

## References

<!-- textlint-disable -->

{% <references> %}

- web.dev. 「[Cumulative Layout Shift (CLS)](https://web.dev/articles/cls)」
- web.dev. 「[Core Web Vitals](https://web.dev/articles/vitals)」
- Zola. "[Overview - Templating your content](https://www.getzola.org/documentation/content/overview/#templating-your-content)"
- Zola. "[Overview - get_image_metadata](https://www.getzola.org/documentation/templates/overview/#get-image-metadata)"
  {% </references> %}

<!-- textlint-enable -->
