# tabi テーマ ショートコード一覧

tabi テーマで使用できるショートコードのリファレンスです。

## Admonition（注意書き）

注意書きや警告を目立たせるブロックを表示します。

タイプ: `note`（グレー）, `tip`（緑）, `info`（青）, `warning`（オレンジ）,
`danger`（赤）

```markdown
{{ admonition(type="warning", text="短い警告メッセージ") }}
```

複数行の場合:

```markdown
{% admonition(type="warning", title="カスタムタイトル") %}
長い内容をここに書けます。
Markdown も使用可能です。
{% end %}
```

パラメータ:
- `type`: 必須。note, tip, info, warning, danger のいずれか
- `title`: 任意。デフォルトは type の大文字
- `icon`: 任意。アイコンを変更（他の type 名を指定可能）
- `text`: インライン形式の場合の内容

## Aside（サイドノート）

本文の横に補足情報を表示します（PC では余白に、モバイルでは独立ブロックに）。

```markdown
{{ aside(text="補足情報をここに書きます。") }}
```

複数行の場合:

```markdown
{% aside(position="right") %}
長い補足情報。
Markdown も使用可能。
{% end %}
```

パラメータ:
- `position`: 任意。"right" で右側に配置（デフォルトは左）
- `text`: インライン形式の場合の内容

## 画像ショートコード

すべての画像ショートコードで使用可能な共通パラメータ:
- `raw_path`: true にすると src をそのまま使用
- `inline`: true にするとインライン表示
- `full_width`: true にするとヘッダー幅まで拡大
- `lazy_loading`: デフォルト true

### dual_theme_image（ライト/ダーク切り替え画像）

ライトモードとダークモードで異なる画像を表示します。

```markdown
{{ dual_theme_image(light_src="img/day.webp", dark_src="img/night.webp",
   alt="説明") }}
```

### invertible_image（反転画像）

ダークモードで色を反転します。グラフや図に適しています。

```markdown
{{ invertible_image(src="img/graph.webp", alt="グラフ") }}
```

### dimmable_image（減光画像）

ダークモードで画像を暗くします。明るい写真に適しています。

```markdown
{{ dimmable_image(src="img/photo.webp", alt="写真") }}
```

### image_hover（ホバー切り替え画像）

マウスホバーで画像を切り替えます。ビフォー/アフターの比較に適しています。

```markdown
{{ image_hover(default_src="img/before.webp", hovered_src="img/after.webp",
   default_alt="変更前", hovered_alt="変更後") }}
```

### image_toggler（クリック切り替え画像）

クリックで画像を切り替えます。

```markdown
{{ image_toggler(default_src="img/a.webp", toggled_src="img/b.webp",
   default_alt="画像A", toggled_alt="画像B") }}
```

### full_width_image（全幅画像）

ヘッダー幅まで拡大した画像を表示します。

```markdown
{{ full_width_image(src="img/wide.webp", alt="ワイド画像") }}
```

## Mermaid（ダイアグラム）

Mermaid 記法でダイアグラムを描画します。使用するには frontmatter に
`mermaid = true` を設定する必要があります。

```markdown
{% mermaid() %}
flowchart LR
    A[開始] --> B[処理]
    B --> C[終了]
{% end %}
```

パラメータ:
- `invertible`: ダークモードで反転（デフォルト true）
- `full_width`: ヘッダー幅まで拡大

## remote_text（外部テキスト埋め込み）

リモート URL またはローカルファイルの内容を埋め込みます。

````markdown
```python
{{ remote_text(src="https://example.com/script.py") }}
```
````

パラメータ:
- `src`: 必須。URL またはファイルパス
- `start`: 開始行番号（1から）
- `end`: 終了行番号

## multilingual_quote（多言語引用）

原文と翻訳の両方を表示する引用ブロックです。

```markdown
{{ multilingual_quote(original="原文", translated="翻訳", author="著者名") }}
```

## references（参考文献）

ハンギングインデントの参考文献リストを作成します。

```markdown
{% references() %}
著者名 (年). タイトル. *ジャーナル名*, 巻(号), ページ.

次の参考文献...
{% end %}
```

## spoiler（ネタバレ/スポイラー）

クリックするまでテキストをぼかして隠します。

```markdown
答えは {{ spoiler(text="42") }} です。
```

パラメータ:
- `text`: 必須。隠すテキスト
- `fixed_blur`: true にすると固定の「SPOILER」表示

## wide_container（幅広コンテナ）

テーブルやコードブロックをヘッダー幅まで拡大します。

```markdown
{% wide_container() %}

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |

{% end %}
```

## force_text_direction（テキスト方向強制）

テキストの方向を強制的に変更します。

```markdown
{% force_text_direction(direction="rtl") %}
右から左に表示されるテキスト
{% end %}
```

パラメータ:
- `direction`: "ltr"（左から右）または "rtl"（右から左）

## iine（いいねボタン）

iine.to のいいねボタンを追加します。

```markdown
{{ iine(slug="/blog/post/like", icon="heart", label="いいね") }}
```

パラメータ:
- `slug`: ボタンの識別子（デフォルトはページパス）
- `icon`: heart, thumbs_up, upvote, または絵文字
- `label`: アクセシビリティラベル

## コードブロックのファイル名表示

Zola 0.20.0 以降の標準機能です（ショートコードではありません）。

````markdown
```rust,name=src/main.rs
fn main() {
    println!("Hello!");
}
```
````

URL を指定すると、`code_block_name_links = true` 設定でリンクになります。
