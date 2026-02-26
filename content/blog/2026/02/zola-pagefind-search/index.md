+++
title = "ZolaブログにPagefindで日本語検索を導入した"
description = """
静的サイトジェネレーターZolaで運用しているこのブログに、
Pagefindを使った日本語対応のサイト内検索を導入しました。
選定の経緯から実装時のハマりどころまでを記録します。
"""
date = 2026-02-26T07:58:30+09:00
[taxonomies]
tags = ["Tech", "Weblog", "Zola"]
[extra]
social_media_card = "ogp.webp"
tldr = """
Zolaの組み込み検索は日本語非対応のため、
日本語のセグメンテーションに対応したPagefindを導入しました。
Zolaとの組み合わせでいくつか落とし穴があるので解説しています。
"""
+++

## はじめに（Zolaの検索事情）

このブログも記事数が255を超え、
検索機能なしでは目的の記事に
たどり着きにくくなってきました。
タグやアーカイブで絞り込めはしますが、
「あのキーワードで書いた記事どこだっけ」
という場面には対応できません。

このブログで使用している静的サイトジェネレーター
Zolaには検索機能が組み込まれています。
検索エンジンには
[elasticlunr.js](http://elasticlunr.com/)
が使われていますが、
日本語のトークナイズに対応していません。
elasticlunr自体が長期間更新されておらず、
今後の対応も期待できない状況です。

適用しているテーマ
[tabi](https://github.com/welpo/tabi)
の検索UIもelasticlunrを前提としており、
日本語ブログでは実質的に使えません。
`config.toml`では`build_search_index = false`
として無効化していました。

そこで、日本語対応の検索機能を導入することにしました。

## 検索エンジンの選定

静的サイトで使える検索エンジンを
いくつか比較検討しましたが、
下表のような理由で見送りました。

| 候補        | 見送った理由                                                           |
| ----------- | ---------------------------------------------------------------------- |
| Algolia     | SaaS依存。無料枠に月10,000リクエスト制限。検索クエリが外部に送信される |
| Meilisearch | サーバーの常時稼働が必要で、静的サイトとは根本的に合わない             |
| Fuse.js     | 全インデックスをクライアントにダウンロードする設計。記事数の増加に弱い |
| Google PSE  | 無料版は広告表示あり。サービス縮小傾向。プライバシーの懸念             |

最終的に選定したのは、[Pagefind](https://pagefind.app/)
です。

## Pagefind とは

[Pagefind](https://pagefind.app/)は
CloudCannonが開発した静的サイト向けの
全文検索ライブラリです。

サイトのビルド後にHTMLを解析して
検索インデックスを静的ファイルとして生成し、
検索時にはWebAssemblyで動作する
クライアントサイドの検索エンジンが
必要なチャンクだけを読み込んで結果を返します。
外部サーバーへの通信は一切発生しません。

<!-- textlint-disable -->

{% aside(position="right") %}
セグメンテーションとは、
文章を単語に分割する処理。
英語のように単語がスペースで
区切られていない日本語・中国語・韓国語は
単語を区切る処理が必要。
{% end %}

<!-- textlint-enable -->

Extended版ではCJK（中国語・日本語・韓国語）の
セグメンテーションに対応しており、
`npx pagefind`を実行するだけで
Extended版が自動的にダウンロードされます。
検索UIコンポーネントも同梱されているため、
数行のHTMLを追加するだけで
検索ページを構築できます。

<!-- textlint-disable -->

{% admonition(type="note", title="Note") %}
PagefindのセグメンテーションはMeCabのような
品詞分解を行う形態素解析ではなく、
Unicode標準に基づく単語境界の検出です。
そのため「走る」で「走った」がヒットするような
活用形の展開（ステミング）には対応していません。
{% end %}

<!-- textlint-enable -->

このブログでPagefindを採用した
決め手は次の点です。

- **日本語対応**:
  Extended版がCJKセグメンテーションに対応している
- **静的サイトとの親和性**:
  ビルド時にインデックスを静的ファイルとして生成する。
  外部サービスが不要
- **軽量**:
  インデックスはチャンク分割され、
  検索時に必要な部分だけが転送される
- **プライバシー**:
  完全にクライアントサイドで動作する。
  このブログの
  設計思想とも一致する
- **コスト**: ゼロ

## 実装のアプローチ

tabiテーマにはできるだけ手を入れない
方針を採りました。
テーマを直接編集すると、
アップデートのたびに変更が衝突して
追従が面倒になるためです。
Zolaでは`templates/`に同名のファイルを
置くことでテーマのテンプレートを
上書きでき、CSSも`static/custom.css`で
追記できます。

tabiの検索UIは`build_search_index = true`
のときにだけ表示される仕組みです。
Pagefindは独自のUIコンポーネントを持っているため、
tabiの検索モーダルは使わず、
Pagefind UIを載せた専用の検索ページを
新設する方式にしました。
ナビゲーションメニューに「search」を
追加し、読者はそこから検索を利用します。

## Pagefindの実装

<!-- author-approved: Pagefindの実装セクション配下の分類に必要 -->

### 実装概要

まずPagefindをインストールします。

```bash
npm install -D pagefind
```

次にプロジェクトルートにPagefindの設定ファイル
`pagefind.yml`を作成します。

```yaml,name=pagefind.yml
site: public
glob: "blog/**/*.html"
force_language: ja
```

`glob`でインデックス対象を`blog/`配下の
記事に限定し、トップページやaboutなどの
固定ページは除外しています。
`force_language: ja`は
日本語のCJKセグメンテーションを強制する設定です。

検索ページはZolaのセクションとして作成します。
`content/search/_index.md`でテンプレートを指定し、
`templates/search.html`にPagefind UIを配置します。

```html,name=templates/search.html
{% extends "base.html" %}

{% block main_content %}
<main>
  <div class="wide-container">
    <link
      href="/pagefind/pagefind-ui.css"
      rel="stylesheet"
    />
    <div id="search"></div>
    <script
      src="/pagefind/pagefind-ui.js"
    ></script>
    <script>
      window.addEventListener(
        'DOMContentLoaded', () => {
        new PagefindUI({
          element: "#search",
          showSubResults: true,
          showImages: false,
          translations: {
            placeholder:
              "検索キーワードを入力…",
            zero_results:
              "[SEARCH_TERM] の検索結果は"
              + "ありません",
            one_result:
              "[SEARCH_TERM] の検索結果: 1件",
            many_results:
              "[COUNT] 件の検索結果",
            clear_search: "クリア",
          }
        });
      });
    </script>
  </div>
</main>
{% endblock main_content %}
```

tabiの`base.html`を継承することで、
ヘッダーやフッター、
スキンの設定がそのまま反映されます。
`translations`で検索UIの
日本語メッセージを指定しています。

<!-- author-approved: Pagefindの実装セクション配下の分類に必要 -->

### minify_htmlの罠

`zola build`後にPagefindを実行したところ、
304個のHTMLファイルを検出しながら
インデックスされたページは0件、
「Discovered 0 languages」という
結果になりました。

原因の切り分けは次のように進めました。

1. 最小限のHTMLファイルを作成して
   Pagefindを実行 → 正常動作
2. Zolaが実際に生成したHTMLをコピーして
   Pagefindを実行 → 再現
3. HTMLの要素を削りながら比較
   → `</head>`の有無で結果が変わることを特定

Zolaの`config.toml`で`minify_html = true`を
設定すると、HTML5の仕様上省略可能な
`</head>`閉じタグが除去されます。
これ自体はHTML5として合法ですが、
Pagefind v1.4.0のHTMLパーサーは
`</head>`がないとページを正しく解析できず、
言語検出に失敗していました。

このブログの規模ではHTML minifyの
恩恵は無視できるため、
`config.toml`で`minify_html = false`に
変更して対処しました。

```toml,name=config.toml
minify_html = false
```

これはZolaの不具合ではなく
Pagefindのパーサー側の制約です。
将来Pagefindが`</head>`省略に
対応すれば`minify_html`を
再度有効化できます。

<!-- author-approved: Pagefindの実装セクション配下の分類に必要 -->

### テーマとの共存で踏んだCSS問題

Pagefind UIにはCSS Custom Propertiesで
スタイルをカスタマイズする仕組みがあります。
テーマカラーに合わせるため
`:root`で変数を宣言したところ、
期待どおりに適用されませんでした。

原因はCSSのカスケード順序にあります。
`pagefind-ui.css`は検索ページの`<main>`内で
読み込まれるため、tabiが`<head>`内で
読み込む`custom.css`よりも後にカスケードされます。
結果として、Pagefindのデフォルト値が
こちらの`:root`宣言に勝っていました。

セレクタを`.pagefind-ui`に変更し、
クラスセレクタの詳細度で
確実にオーバーライドするようにしました。

```css,name=static/custom.css
.pagefind-ui {
  --pagefind-ui-primary:
    var(--primary-color);
  --pagefind-ui-text:
    var(--text-color);
  --pagefind-ui-background:
    var(--background-color);
  --pagefind-ui-border:
    var(--divider-color);
  --pagefind-ui-tag: var(--bg-0);
  --pagefind-ui-font:
    var(--sans-serif-font);
}
```

tabiの既存のCSS変数を参照することで、
ダークモードやevangelionスキンの
カラースキームに自動で追従します。

もうひとつ、tabiテーマは全リンクに対して
`a:hover { background-color: var(--primary-color) }`
を適用するグローバルスタイルを持っています。
Pagefindの検索結果は`<a>`タグで構成されるため、
ホバーするとevangelionスキンの赤
（`#d12e36`）が結果全体の背景に
適用されてしまいました。

検索結果エリア内のリンクスタイルを個別に
上書きして解消しています。

```css,name=static/custom.css
.pagefind-ui a:hover,
.pagefind-ui a:focus {
  background-color: transparent;
  color: var(--primary-color);
}
```

## CI/CDへの組み込み

このブログはGitHub Actionsで
Cloudflare Workersにデプロイしています。
ワークフローに検索インデックス生成の
ステップを追加しました。

```yaml,name=.github/workflows/deploy.yml
- name: Build
  run: zola build

- name: Build search index
  run: npx pagefind
```

`zola build` → `npx pagefind`の
2ステップだけで完結します。

## まとめ

Pagefindの導入により、
303ページ（セクションページ含む）・
17,217語のインデックスが生成され、
日本語キーワードでの検索が
機能するようになりました。

実装自体はシンプルでしたが、
`minify_html`によるHTML構造の変化や
テーマとのCSS競合など、
組み合わせ固有の問題に時間を取られました。
単独では正しく動くものが
組み合わせると壊れるパターンは、
静的サイトのツールチェーンでは
よくある話かもしれません。

現時点での制約として、
日本語のステミングには未対応です。
「走る」で検索しても
「走った」はヒットしません。
ただし単語単位の検索は安定しており、
現在の規模では実用上十分です。
