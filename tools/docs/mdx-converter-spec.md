# MDX→Zola記事コンバーター 仕様書

## 1. 目的

Next.js/MDXブログの記事をZola静的サイトの記事形式に変換する。

## 2. ユースケース

ユーザーは移行元フォルダを指定し、配下のMDX記事を再帰的に検索して、Zolaの記事形式に一括変換する。

## 3. 入力

- 移行元フォルダ（MDX記事を含むディレクトリ）
- 移行先フォルダ（Zolaのcontentディレクトリ）

### 移行元の構造

```
指定フォルダ/
  YYYY/MM/DD/slug-name/
    page.mdx          # 記事本体
    image.png ...      # 記事に使われる画像等
```

## 4. 出力

- 移行先フォルダにZola形式の記事ディレクトリが生成される

### 移行先の構造

```
content/
  YYYY/
    _index.md          # 年セクション
    MM/
      _index.md        # 月セクション
      slug-name/
        index.md       # 変換後の記事
        image.png ...  # コピーされた画像等
```

## 5. 変換内容

### 5.1 メタデータの変換

MDXファイル内のJavaScriptオブジェクトとして記述されたメタデータを、ZolaのTOMLフロントマターに変換する。

**変換対象フィールド:**

| MDX（元） | Zola（先） | 備考 |
|---|---|---|
| `title` | `title` | |
| `description` | `description` | |
| `date` | `date` | YYYY-MM-DD形式、クォートなし |
| （ソースのディレクトリ名） | （出力ディレクトリ名） | `path`フィールドではなくディレクトリ名を使用 |
| URLパス `YYYY/MM/DD/slug` | `aliases` | 旧URLからのリダイレクト用 |
| `canonicalUrl` | `[extra] canonical_url` | 存在する場合のみ |

### 5.2 本文の変換

MDX固有の構文を標準Markdownに変換する。

| 変換元 | 変換先 | 説明 |
|---|---|---|
| `import`文 | （削除） | JavaScript import文を除去 |
| `export const article = {...}` | （削除→フロントマターへ） | メタデータとして処理済み |
| `export const metadata = ...` | （削除） | |
| `export default function ...` | （削除） | |
| `{/* コメント */}` | （削除） | JSXコメント |
| `<Image src={VAR} alt="..." ... />` | `![alt](filename)` | 画像をMarkdown記法に変換 |

### 5.3 コンポーネントの変換

MDXで使用されているReactコンポーネントをZola対応形式に変換する。

| コンポーネント | 変換先 | 説明 |
|---|---|---|
| `<TableOfContents />` | `<!-- toc -->` | tabiテーマのTOCマーカーに置換 |
| `<YouTube url="..." />` | `{{ youtube(id="VIDEO_ID") }}` | URLからVideo IDを抽出しZolaビルトインショートコードに変換 |
| `<SoundCloudEmbed ... />` | （そのまま残す） | Zola対応なし。移行不能のためソースをそのまま保持 |
| `<DescriptionList>` | `<dl>` | 標準HTMLの定義リストに変換 |
| `<DescriptionTerm>` | `<dt>` | 同上 |
| `<DescriptionDetails>` | `<dd>` | 同上 |

**YouTube Video IDの抽出ルール:**

以下のURL形式からVideo IDを取得する。

- `https://www.youtube.com/watch?v=VIDEO_ID` → `VIDEO_ID`
- `https://youtu.be/VIDEO_ID` → `VIDEO_ID`
- `https://youtu.be/VIDEO_ID?si=...` → `VIDEO_ID`（クエリパラメータを除去）

### 5.4 画像ファイルのコピー

MDX記事と同じディレクトリにある画像ファイルを、変換先ディレクトリにコピーする。

## 6. 動作仕様

- 移行先に同名のディレクトリが既に存在する場合は**上書き**する
- 変換処理の進捗と結果を**ログ出力**する
  - 処理した記事数
  - 各記事の変換結果（成功/失敗）
  - エラーがあればその内容

## 7. 対象外（スコープ外）

- 5.3に記載されていないカスタムReactコンポーネントの変換
- 記事内容の校正・修正
