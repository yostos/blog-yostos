# リンクカード機能 仕様書

## 概要

記事中のURLをカード型リンクで表示する機能。
URLの種類に応じて2つの方式を使い分ける。

- **GitHub リポジトリURL** —
  GitHub API でリポジトリ情報を取得し、
  専用カードを描画（ローカルJSON経由）
- **その他のURL** —
  はてなブログカードの iframe で表示

## コンポーネント構成

| ファイル | 役割 |
|---|---|
| `scripts/generate-linkcard.mjs` | GitHub リポジトリ情報取得 |
| `data/linkcard.json` | GitHub メタデータ保存 |
| `templates/shortcodes/linkcard.html` | カード描画テンプレート |
| `static/custom.css` | カードのスタイル（追記） |

## 使い方

### 記事中のショートコード記法

記事の Markdown に以下のように記述する。
ショートコードは textlint 除外コメントで囲む。

```markdown
<!-- textlint-disable -->

{{ linkcard(url="https://github.com/owner/repo") }}

<!-- textlint-enable -->
```

GitHub URL でもその他の URL でも同じ記法を使う。
テンプレート側で自動的に描画方式を切り替える。

### npm scripts

GitHub リポジトリのメタデータ取得が必要な場合のみ
スクリプトを実行する。
はてなブログカード（GitHub 以外の URL）は
iframe のため事前取得は不要。

```bash
npm run linkcard           # メタデータを取得・更新
npm run linkcard:dry-run   # 取得対象を確認（実行しない）
npm run linkcard -- --force  # 全件再取得（キャッシュ無視）
```

### オプション

| オプション | 説明 |
|---|---|
| `--dry-run` | 取得対象URLの一覧を表示。実際の取得は行わない |
| `--force` | 既存エントリを無視して全件再取得 |

## カード種別

### GitHub リポジトリカード

`https://github.com/{owner}/{repo}` 形式の URL を検出し、
GitHub API (`/repos/{owner}/{repo}`) から情報を取得する。

表示内容:

- Octocat アイコン（SVG インライン）
- `owner / **repo**`（リポジトリ名は太字、青色リンク）
- description（リポジトリの説明文）
- `</> Language`（主要言語）

### はてなブログカード

GitHub 以外の URL はすべて
はてなブログカードの iframe で表示する。

```html
<iframe
  src="https://hatenablog-parts.com/embed?url={URL}"
  width="100%" height="155"
  frameborder="0" scrolling="no" loading="lazy">
</iframe>
```

OGP メタデータの取得・管理ははてな側が行うため、
`npm run linkcard` の実行は不要。

## データ形式

`data/linkcard.json` には GitHub リポジトリの
メタデータのみ保存する。

```json
{
  "https://github.com/owner/repo": {
    "type": "github",
    "owner": "owner",
    "repo": "repo",
    "description": "リポジトリの説明",
    "language": "Shell",
    "fetched_at": "2026-02-13T12:00:00Z"
  }
}
```

| フィールド | 取得元 |
|---|---|
| `type` | 固定値 `"github"` |
| `owner` | `data.owner.login` |
| `repo` | `data.name` |
| `description` | `data.description` |
| `language` | `data.language` |
| `fetched_at` | 取得時の ISO 8601 タイムスタンプ |

## テンプレート処理フロー

`templates/shortcodes/linkcard.html` の分岐:

1. `data/linkcard.json` を `load_data()` で読み込み
2. URL に対応するエントリが存在し、
   `type == "github"` の場合 → GitHub 専用カード
3. それ以外 → はてなブログカード iframe

### Zola ショートコードの注意点

- テンプレートの HTML 出力に改行を入れない
  （Zola の Markdown パーサーが `<p>` で囲み、
  `<div>` が壊れるため）
- ブロック要素（`<div>`）ではなく
  インライン要素（`<span>`）を使用し、
  CSS で `display: block` 等を指定する

## スタイル仕様

`static/custom.css` に追記。
`config.toml` の `stylesheets = ["custom.css"]` で
読み込み済み。

### GitHub カード

- 角丸ボーダー（`border-radius: 8px`）
- tabi テーマのリンクスタイルを
  `a.linkcard` で上書き（`:visited` 等含む）
- Octocat アイコン: `color: #57606a`
- リポジトリ名: `color: #0969da`（青）
- ダークモード対応
  （`[data-theme="dark"]` で色を調整）

### はてなブログカード

- `border: none` で iframe の枠線を除去
- `margin: 1em 0` で前後に余白

## ワークフロー

記事にリンクカードを追加する手順:

1. 記事の Markdown にショートコードを記述
2. GitHub URL が含まれる場合のみ
   `npm run linkcard` を実行
3. `zola serve` で表示を確認
4. コミット（`data/linkcard.json` を含める）

## 注意事項

- `data/linkcard.json` は Git 管理対象に含める
  （Zola ビルド時に `load_data()` で読み込むため）
- GitHub リポジトリ情報が変更された場合は
  `--force` で再取得する
- はてなブログカードは外部サービスのため、
  サービス停止時は表示されない
- GitHub API はレート制限あり
  （認証なしで 60 回/時間）
