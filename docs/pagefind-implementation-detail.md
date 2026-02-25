# Pagefind 導入 実装記録

**関連ドキュメント**:

- `docs/architectural-decision.md` ADR-0001
- `docs/pagefind-implementation-plan.md`

**実施日**: 2026-02-25
**バージョン**: v1.2.0
**PR**: #5 (feature/pagefind-search → main)

## 実装結果サマリー

- Pagefind v1.4.0 (Extended) を導入
- 303ページ / 17,217語をインデックス
- 日本語CJKセグメンテーション対応
- ダークモード・evangelionスキン対応
- CI/CDパイプラインに統合

## 計画からの変更点

導入計画（9ステップ）に対して、実装時に
以下の差異が発生した。

### 1. Pagefind v1.x の出力パス変更

計画では出力先を `_pagefind/`（アンダースコア付き）
と記載していたが、Pagefind v1.4.0 ではデフォルトが
`pagefind/`（アンダースコアなし）に変更されていた。

**対応**: テンプレート・`.gitignore` のパスを
`/pagefind/` に統一した。`pagefind.yml` には
`output_path` を指定せずデフォルトを使用する。

なお `output_path: pagefind` を明示指定すると、
`site` ディレクトリではなくCWD相対で出力される
問題があり、指定しないのが正解だった。

### 2. Zola minify_html との非互換

`minify_html = true` の場合、Zolaは `</head>`
閉じタグを省略する（HTML5仕様上は合法）。
しかしPagefind v1.4.0 のHTMLパーサーは
`</head>` がないとページを正しく解析できず、
「Discovered 0 languages」となりインデックスが
生成されなかった。

**原因特定の経緯**:

1. `npx pagefind` で304ファイル検出、0ページ
   インデックスのエラー
2. 最小HTMLで正常動作を確認
3. 実際のZola生成HTMLをコピーして再現
4. `</head>` の有無で切り分け → 原因特定

**初期対応（廃止済み）**: ビルド後に `sed` で
`</head>` を `<body>` の直前に挿入する
ワークアラウンドを追加していた。

**最終対応**: `config.toml` で
`minify_html = false` に変更した。
ブログ規模でHTML minifyの恩恵は無視でき、
ビルドパイプラインに `sed` による
HTML書き換えを組み込むのは保守性が悪いため。
`deploy.yml` の `Fix HTML for Pagefind`
ステップも削除した。

### 3. `vite_plugin_mode` の削除

計画では `pagefind.yml` に
`vite_plugin_mode: false` を記載していたが、
Vite統合用の設定でありZolaプロジェクトには無関係。
デフォルトが `false` のため削除した。

最終的な `pagefind.yml`:

```yaml
site: public
glob: "blog/**/*.html"
force_language: ja
```

### 4. CSSカスケード順序の問題

計画ではCSS変数を `:root` で宣言する想定だったが、
`pagefind-ui.css` が `<main>` 内で読み込まれるため、
tabi の `<head>` 内の `custom.css` よりも後に
カスケードされ、Pagefindのデフォルト値（`:root`）
が勝つ問題が発生した。

**対応**: セレクタを `.pagefind-ui` に変更し、
クラスセレクタの特異度で確実にオーバーライドする
ようにした。

```css
.pagefind-ui {
  --pagefind-ui-primary: var(--primary-color);
  --pagefind-ui-text: var(--text-color);
  --pagefind-ui-background: var(--background-color);
  --pagefind-ui-border: var(--divider-color);
  --pagefind-ui-tag: var(--bg-0);
  --pagefind-ui-font: var(--sans-serif-font);
}
```

### 5. tabi の a:hover グローバルスタイル干渉

tabiテーマは全リンクに対して
`a:hover { background-color: var(--primary-color) }`
を適用する。Pagefindの検索結果は `<a>` タグで
構成されるため、ホバー時にevangelionの赤
（`#d12e36`）が結果全体の背景に適用される
問題が発生した。

**対応**: `.pagefind-ui` 内のリンクスタイルを
上書きして無効化した。

```css
.pagefind-ui a:hover,
.pagefind-ui a:focus {
  background-color: transparent;
  color: var(--primary-color);
}

.pagefind-ui a:not(.no-hover-padding):hover::before {
  display: none;
}
```

### 6. one_result 翻訳の追加

計画には含まれていなかったが、PRレビューで
検索結果が1件の場合に英語フォールバックが
表示される点を指摘され、`one_result` キーを追加。

### 7. CI での npm キャッシュ追加

`actions/setup-node` に `cache: 'npm'` を追加し、
ビルド時間を短縮した。計画には含まれていなかった。

## 変更ファイル一覧

| ファイル | 操作 | 内容 |
|----------|------|------|
| `package.json` | 変更 | pagefind追加、searchスクリプト追加 |
| `package-lock.json` | 変更 | pagefind依存関係 |
| `pagefind.yml` | 新規 | Pagefind設定 |
| `content/search/_index.md` | 新規 | 検索ページコンテンツ |
| `templates/search.html` | 新規 | 検索ページテンプレート |
| `config.toml` | 変更 | メニューにsearch追加 |
| `static/custom.css` | 変更 | Pagefind UI スタイル |
| `.github/workflows/deploy.yml` | 変更 | CI に Pagefind ステップ追加 |
| `.gitignore` | 変更 | `public/pagefind/` 除外 |
| `CLAUDE.md` | 変更 | コマンド追記 |
| `CHANGELOG.md` | 変更 | v1.2.0 エントリ |
| `docs/architectural-decision.md` | 新規 | ADR-0001 |
| `docs/pagefind-implementation-plan.md` | 新規 | 導入計画 |

## 確認結果

- [x] 検索ページが `/search/` に表示される
- [x] 日本語キーワードで記事がヒットする
- [x] 検索結果から記事ページに遷移できる
- [x] ダークモードでUIが正しく表示される
- [x] スキン変更時にCSS変数で自動追従する
- [x] ナビゲーションにSearchリンクが表示される
- [x] CI/CDワークフローが正常に動作する

## 今後の課題

- Pagefindが日本語ステミングに対応した場合の
  設定更新（現在は未対応）
- `<link>` タグの `<head>` 移動（tabi に
  `extra_head` ブロックが追加された場合）
