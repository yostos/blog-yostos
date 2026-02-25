# Pagefind 導入計画

**関連ADR**: `docs/architectural-decision.md` ADR-0001
**作成日**: 2026-02-25

## 前提

- Zola 0.22.1 + tabiテーマ
- デプロイ: Cloudflare Workers（`deploy.yml`）
- `themes/` 配下は編集禁止
  - テンプレート変更は `templates/` にオーバーライド
  - スタイル変更は `static/custom.css` に追記
- `build_search_index = false` を維持
  （Pagefindが独自にインデックスを生成するため）

## 統合方針

tabiテーマの検索UIは `build_search_index` が `true` の
ときのみ表示される（nav.html:33, header.html:155,
footer.html:125）。Pagefindは独自のUI
コンポーネントを持つため、tabi の検索モーダルは使わず
**Pagefind UIを専用の検索ページとして設置**する。

ナビゲーションメニューに検索ページへのリンクを追加し、
読者はそこからサイト内検索を利用する。

## 実施手順

### Step 1: pagefind のインストール

`devDependencies` に pagefind を追加する。

```bash
npm install -D pagefind
```

`package.json` の `scripts` に追加:

```json
"search": "pagefind --site public",
"search:dry-run": "pagefind --site public --dry-run"
```

### Step 2: Pagefind 設定ファイルの作成

プロジェクトルートに `pagefind.yml` を作成する。

```yaml
site: public
vite_plugin_mode: false
glob: "blog/**/*.html"
force_language: ja
```

- `glob`: `blog/` 配下の記事のみをインデックス対象に
  する（トップページ、about等の固定ページは除外）
- `force_language: ja`: 日本語のCJKセグメンテーションを
  強制有効化

### Step 3: 検索ページの作成

`content/search/_index.md` を作成する。

```toml
+++
title = "Search"
template = "search.html"
+++
```

`templates/search.html` を作成し、
Pagefind UIコンポーネントを配置する。
tabiテーマの `base.html` を継承して
サイト全体のレイアウトと統一する。

```html
{% extends "base.html" %}

{% block main_content %}
<main>
  <div class="wide-container">
    <link
      href="/_pagefind/pagefind-ui.css"
      rel="stylesheet"
    />
    <div id="search"></div>
    <script
      src="/_pagefind/pagefind-ui.js"
    ></script>
    <script>
      window.addEventListener('DOMContentLoaded', () => {
        new PagefindUI({
          element: "#search",
          showSubResults: true,
          showImages: false,
          translations: {
            placeholder: "検索キーワードを入力…",
            zero_results: "[SEARCH_TERM] の検索結果はありません",
            many_results: "[COUNT] 件の検索結果",
            clear_search: "クリア",
          }
        });
      });
    </script>
  </div>
</main>
{% endblock main_content %}
```

### Step 4: ナビゲーションに検索リンクを追加

`config.toml` の `menu` に検索ページを追加する。

```toml
menu = [
    { name = "blog", url = "blog", trailing_slash = true },
    { name = "archive", url = "archive", trailing_slash = true },
    { name = "tags", url = "tags", trailing_slash = true },
    { name = "music", url = "music", trailing_slash = true },
    { name = "projects", url = "projects", trailing_slash = true },
    { name = "uses", url = "uses", trailing_slash = true },
    { name = "about", url = "about", trailing_slash = true },
    { name = "search", url = "search", trailing_slash = true },
]
```

### Step 5: ダークモード対応のCSS追加

`static/custom.css` にPagefind UIのテーマ変数を追記する。

tabiテーマの既存カラー変数を参照し、
ライトモード・ダークモードの両方に対応する。
具体的なCSS変数（`--pagefind-ui-primary` 等）の値は
実装時にtabiのカラースキーム（evangelion skin）を
確認して決定する。

### Step 6: デプロイワークフローの更新

`.github/workflows/deploy.yml` のBuildステップの後に
Pagefindインデックス生成を追加する。

```yaml
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: zola build

      - name: Build search index
        run: npx pagefind
```

`npx pagefind` は `pagefind.yml` を自動検出し、
`public/_pagefind/` にインデックスファイルを生成する。
`wrangler.toml` の `[assets] directory = "./public"` により
そのままCloudflare Workersにデプロイされる。

### Step 7: .gitignore の更新

ローカルビルドで生成されるPagefindファイルを
gitから除外する。

```
public/_pagefind/
```

### Step 8: ローカル動作確認

```bash
zola build && npx pagefind && zola serve
```

確認項目:

- [ ] 検索ページが表示される
- [ ] 日本語キーワードで記事がヒットする
- [ ] 検索結果から記事ページに遷移できる
- [ ] ダークモードでUIが正しく表示される
- [ ] モバイル表示で崩れない

### Step 9: CLAUDE.md の更新

Common Commands セクションに追記:

```bash
npx pagefind           # 検索インデックス生成
npx pagefind --dry-run # インデックス生成のプレビュー
```

## 注意事項

- `zola serve` の開発サーバーでは `_pagefind/` が
  自動生成されない。ローカルで検索を試すには
  先に `zola build && npx pagefind` を実行してから
  `public/` を別のHTTPサーバーで配信するか、
  再度 `zola serve` する必要がある
- Pagefindのextended版（CJK対応）は `npx pagefind` 実行時に
  自動でダウンロードされる。追加設定は不要
- `build_search_index` は `false` のまま維持する。
  `true` にするとtabiのelasticlunr検索UIも
  同時に有効化されてしまう
