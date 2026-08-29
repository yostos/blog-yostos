+++
title = "Zolaテーマ「tabi」の活用機能を探る"
description = """
Zolaの高機能テーマ「tabi」には、
普段使っていない便利な機能が数多く眠っています。
ショートコード、テンプレート、Frontmatterオプションまで、
見落としがちな機能をまとめて紹介します。
"""
date = 2026-02-24T12:00:00+09:00
[taxonomies]
tags = ["Tech", "Weblog"]

[extra]
social_media_card = "ogp.webp"

tldr = """
tabiテーマのショートコード18種、
テンプレート3種、Frontmatterオプションを
棚卸しし、未活用の便利機能をまとめました。
"""
+++

<!-- author-approved: ショートコード名・設定項目の列挙に###を使用 -->

このブログはZola静的サイトジェネレーターと
[tabi](https://welpo.github.io/tabi/)テーマで
運用しています。
tabiは多機能なテーマですが、
実際に活用しているのはその一部に過ぎません。
改めてテーマの全機能を棚卸しして、
まだ使っていない機能を洗い出してみました。

<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>

## ショートコード

tabiには18種類のビルトインショートコードと、
このブログ用に自作したカスタムショートコード
2種類があります
（カスタムコードは当然ながらtabiには
含まれません）。

| ショートコード                  | 説明                                                                                                                                                                   |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| admonition                      | info、warning、tipなどのタイプを指定して、注意書きや補足情報を装飾付きボックスで表示します                                                                             |
| add_src_to_code_block（非推奨） | コードブロックの `name=` ラベルをクリック可能なリンクに変換します。現在は `code_block_name_links = true` を設定し、`name=` にURLを直接書く方式が推奨されています       |
| aside                           | 本文の横にサイドバー風の補足情報を表示します。admonitionより控えめな見た目で、ちょっとした注釈を添えるのに向いています                                                 |
| dimmable_image                  | ダークモード時に画像の明るさを自動的に抑えます。白背景のスクリーンショットがダークモードで眩しくなるのを防げます                                                       |
| dual_theme_image                | ライトモードとダークモードで異なる画像を自動的に切り替えて表示します。背景色によって見えにくくなる図表に便利です                                                       |
| force_text_direction            | テキストブロックのLTR（左から右）またはRTL（右から左）の方向を強制的に指定します                                                                                       |
| full_width_image                | 記事の本文幅を超えて、画像をページ全幅で表示します                                                                                                                     |
| iine                            | 特定のブロック単位でいいねボタンを設置できます。tabiの作者が提供するSupabaseインスタンスにカウントが記録されます。導入時はプライバシーポリシーの更新を検討してください |
| image_hover                     | マウスホバーで別の画像に切り替わります。Before/After比較や加工前後の写真を見比べるのに最適です                                                                         |
| image_toggler                   | クリックで2枚の画像をトグル切り替えします。image_hoverと似ていますが、ホバーが使えないモバイル環境でも動作します                                                       |
| invertible_image                | ダークモード時に画像の色を反転します。白背景に黒線で描かれた図表をダークモードでも見やすくできます                                                                     |
| linkcard（自作）                | はてなブログカードのiframeを使い、URLをカード形式で表示します                                                                                                          |
| mermaid                         | Mermaid記法でフローチャートやシーケンス図などの図表を描画します。記事のFrontmatterで `mermaid = true` の設定が必要です                                                 |
| multilingual_quote              | 原文と翻訳をトグルで切り替え表示できる引用ブロックです。英語の技術ドキュメントを引用する際に原文と日本語訳を並べて見せられます                                         |
| references                      | 参考文献をスタイル付きで表示するブロックです。学術的な記事や多くの出典をまとめる場合に適しています                                                                     |
| remote_text                     | 外部URLやローカルファイルの内容を記事内にインラインで埋め込みます。GitHubにあるコンフィグファイルをそのまま表示するような使い方ができます                              |
| spoiler                         | クリックするまで内容が隠されるテキストブロックです。ネタバレを隠したりクイズの答えを伏せるのに使えます                                                                 |
| toc                             | 記事内に `<!-- toc -->` マーカーを挿入するショートコードです。マーカーを直接書くのと同等の動作です                                                                     |
| wide_container                  | 記事の本文幅を超えて、ページ全幅にコンテンツを表示します。大きな表やワイドな画像を見切れずに表示したい場合に使えます                                                   |
| youtube（自作）                 | YouTube動画を埋め込み表示します                                                                                                                                        |

以下、このブログで使用しているショートコードから、
よく使うものに絞ってサンプルを載せておきます。

### admonition

info、warning、danger、tip、noteなどの
タイプを指定できます。

```markdown
{%/* admonition(type="warning", title="注意") */%}
ここに警告メッセージを書きます。
{%/* end */%}
```

<!-- textlint-disable -->

{% admonition(type="warning", title="注意") %}
ここに警告メッセージを書きます。
{% end %}

<!-- textlint-enable -->

### aside

admonitionより控えめな見た目で、
ちょっとした注釈を添えるのに向いています。
PCなどの表示では記事の左右に表示され、
スマートフォンなどでは記事と並んで
表示されます。
`position` パラメータで配置を調整できます。

<!-- textlint-disable -->

{% aside(position="right")%}
右側にも表示できます。
{% end %}

<!-- textlint-enable -->

```markdown
{%/* aside(position="right") */%}
補足情報をここに書きます。
{%/* end */%}
```

### multilingual_quote

原文と翻訳をトグルで切り替え表示できます。
英語の技術ドキュメントを引用する際に、
原文と日本語訳を並べて見せられます。
`author` パラメータで出典も表示できます。

```markdown
{{/* multilingual_quote(
  translated="考える、ゆえに我あり。",
  original="Cogito, ergo sum.",
  author="René Descartes") */}}
```

<!-- textlint-disable -->

{{multilingual_quote(
  translated="考える、ゆえに我あり。",
  original="Cogito, ergo sum.",
  author="René Descartes")}}

<!-- textlint-enable -->

### references

参考文献をスタイル付きで表示するブロックです。
パラメータはなく、内部にMarkdownを記述できます。

```markdown
{%/* references() */%}

- WEBサイト. 「[記事名](https://example.com)」.
- 著者(2026). 『書名』.
  {%/* end */%}
```

<!-- textlint-disable -->

{% references() %}

- Example Site. 「[Zolaで技術ブログを作る](https://example.com/article)」
- 結城浩. (2020). 『[数学ガール](https://example.com/book)』
  {% end %}

<!-- textlint-enable -->

### spoiler

クリックするまで内容がぼかされて隠れます。
JavaScriptを使わず、
CSSとチェックボックスで実装されています。

```markdown
犯人は、{{/* spoiler(text="執事でした。") */}}
```

<!-- textlint-disable -->

犯人は、{{ spoiler(text="執事でした。") }}

<!-- textlint-enable -->

## テンプレート

tabiでは記事に対して3種類のtemplateが
提供されています。
いずれもセクションの `_index.md` で有効にします。

section - 通常のテンプレート
: 通常の記事向けのテンプレートです。

series — 連載記事テンプレート
: 複数回にわたる連載記事を番号付きインデックスで管理できるテンプレートです。
: 複数回にわたる技術解説記事に向いています。

cards — カードグリッドテンプレート
: フィルタ可能なカードグリッドのレイアウトです。
: ポートフォリオやプロジェクト一覧を見せるのに適しています。
: タグによるフィルタリングも可能です。

## サイト設定

`config.toml` の `[extra]` セクションで
設定できるオプションです。
以下の説明は、筆者が気になったものだけを
取り上げており網羅的ではありません。

### skin — カラースキーム

tabiには12種類のカラースキームが用意されています。
sakura、lavender、mint、teal、evangelionなど、
テーマカラーを一行で切り替えられます。

```toml
[extra]
skin = "sakura"
```

このブログでは `custom.css` で
独自にカラーを指定しているため使っていません。

### browser_theme_color — モバイルブラウザのテーマカラー

モバイルブラウザのアドレスバーの色を指定できます。

```toml
[extra]
browser_theme_color = "#087e96"
```

### compact_tags — コンパクトなタグクラウド

タグ一覧をコンパクトな上付き数字スタイルで表示します。
タグ数が多いブログで一覧性を高められます。

```toml
[extra]
compact_tags = true
```

### feed_icon — RSSアイコン

フッターにRSSフィードのアイコンを表示します。
当ブログではsocialsを使ってRSSを
表示しているため使用していません。

```toml
[extra]
feed_icon = true
```

### full_content_in_feed — フィード全文配信

Atomフィードに記事の全文を含めます。
当ブログでは既にこの設定を有効にしています。

```toml
[extra]
full_content_in_feed = true
```

### webmentions — IndieWeb Webmentions

Webmentionによるインタラクションを表示できます。

```toml
[extra.webmentions]
enable = true
domain = "www.example.com"
```

### KaTeX — 数式レンダリング

LaTeX形式の数式をレンダリングできます。
数学や統計を扱う記事で使えます。

記事のFrontmatterで有効化します。

```toml
[extra]
katex = true
```

記事本文では以下のように記述します。

```markdown
インライン数式: $E = mc^2$
ブロック数式: $$\sum_{i=1}^{n} x_i$$
```

## 未使用のFrontmatterオプション

記事ごとに `[extra]` セクションで
個別にオーバーライドできる設定です。

### tldr

これまでセクションを設けて記載していましたが、
Frontmatterで設定できることがわかりました。

### updated — 最終更新日

記事の最終更新日を `date` とは別に表示します。
内容を更新した記事に設定すると、
読者に最新性を伝えられます。
`[extra]` ではなくトップレベルの
Frontmatterフィールドです。

```toml
+++
title = "記事タイトル"
date = 2026-02-01
updated = 2026-02-20
+++
```

### show_reading_time — 読了時間の個別制御

グローバルでは有効にしていますが、
短い記事では非表示にできます。

```toml
[extra]
show_reading_time = false
```

### giscus — コメントの個別制御

グローバルでは全記事で有効ですが、
特定の記事でコメントを無効にできます。

```toml
[extra]
giscus = false
```

### toc — 目次の個別制御

グローバル設定とは別に、
記事ごとに目次の表示を制御できます。

```toml
[extra]
toc = true
```

このブログでは `<!-- toc -->` マーカーを
`details`要素に入れて、畳めるようにしているため利用していませんが、
そのような要件がなければ
Frontmatterで制御するほうがシンプルです。

## まとめ

tabiは使い切れないほど多機能なテーマです。
今回改めて棚卸しをしてみると、
これまで使っていなかった機能のなかにも
便利なものが数多く存在しました。

たとえば `tldr` はこれまで記事本文に
セクションを設けて書いていましたが、
Frontmatterに設定するだけで済むと知り、
今後は積極的に活用していきます。
`updated` による最終更新日の表示なども、
知っていれば必要な場面ですぐに使える
実用的なオプションです。

テンプレートについても、
これまでは通常の `section` テンプレートしか
使っていませんでしたが、
`series` テンプレートは複数回にわたる
連載記事をまとめるのに向いており、
技術解説のシリーズ記事などで
活用していきたいと考えています。
`cards` テンプレートも、
ポートフォリオやプロジェクト一覧のような
通常のブログ記事とは異なるタイプの
コンテンツを見せる場面で使えそうです。

使える機能を把握しておくだけでも、
記事の表現の幅が広がります。
テーマの機能を活かしきれていないと
感じている方は、一度公式ドキュメントを
眺めてみることをおすすめします。

## References

<!-- textlint-disable -->

{% references() %}

- tabi. "[tabi documentation](https://welpo.github.io/tabi/)"

{% end %}

<!-- textlint-enable -->
