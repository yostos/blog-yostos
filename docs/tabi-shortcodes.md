# tabi テーマ コンポーネント一覧

tabi テーマ（v5 以降）で使用できるコンポーネントのリファレンスです。

Zola 0.23 でショートコードは廃止され、Tera 2 のコンポーネントに置き換わりました。
記事本文からの呼び出し方は次の 2 通りです。

- インライン: `{{< name key="value" />}}`
- ブロック: `{% <name key="value"> %}` 〜 `{% </name> %}`

文字列以外の値（真偽値・数値など）は `{...}` で囲みます（例: `full_width={true}`）。
本文全体が Tera で処理されるため、`{{ }}` や `{% %}` をそのまま表示したいコード例は
`{% raw %}` 〜 `{% endraw %}` で囲みます。

## Admonition（注意書き）

注意書きや警告を目立たせるブロックを表示します。

タイプ: `note`（グレー）, `tip`（緑）, `info`（青）, `warning`（オレンジ）,
`danger`（赤）

```markdown
{{< admonition type="warning" text="短い警告メッセージ" />}}
```

複数行の場合:

```markdown
{% <admonition type="warning" title="カスタムタイトル"> %}
長い内容をここに書けます。
Markdown も使用可能です。
{% </admonition> %}
```

パラメータ:
- `type`: 必須。note, tip, info, warning, danger のいずれか
- `title`: 任意。デフォルトは type の大文字
- `icon`: 任意。アイコンを変更（他の type 名を指定可能）
- `text`: インライン形式の場合の内容

**使用例:**

```markdown
{% <admonition type="warning" title="互換性に関する注意"> %}
この機能は Chrome 90 以降でのみ動作します。
古いブラウザでは正常に表示されない可能性があります。
{% </admonition> %}

{{< admonition type="tip" text="npm install --save-dev を使うと開発依存関係として追加されます。" />}}

{% <admonition type="danger" title="データ損失の危険性"> %}
この操作を実行すると、既存のデータが**完全に削除**されます。
バックアップを取ってから実行してください。
{% </admonition> %}
```

## Aside（サイドノート）

本文の横に補足情報を表示します（PC では余白に、モバイルでは独立ブロックに）。

```markdown
{{< aside text="補足情報をここに書きます。" />}}
```

複数行の場合:

```markdown
{% <aside position="right"> %}
長い補足情報。
Markdown も使用可能。
{% </aside> %}
```

パラメータ:
- `position`: 任意。"right" で右側に配置（デフォルトは左）
- `text`: インライン形式の場合の内容

**使用例:**

```markdown
React は Facebook が開発した JavaScript ライブラリです。
{% <aside> %}
2013年にオープンソース化され、現在では最も人気のある
フロントエンドフレームワークの一つとなっています。
{% </aside> %}

{{< aside text="TypeScript は Microsoft が開発した JavaScript の
スーパーセットです。" />}}
```

## 画像コンポーネント

すべての画像コンポーネントで使用可能な共通パラメータ:
- `raw_path`: true にすると src をそのまま使用
- `inline`: true にするとインライン表示
- `full_width`: true にするとヘッダー幅まで拡大
- `lazy_loading`: デフォルト true

**共通パラメータの使用例:**

```markdown
{{< invertible_image src="diagram.webp" alt="図" full_width={true} />}}

{{< dimmable_image src="photo.webp" alt="写真" inline={true} lazy_loading={false} />}}

{{< dual_theme_image light_src="ui-light.webp" dark_src="ui-dark.webp" alt="UI" raw_path={true} />}}
```

### dual_theme_image（ライト/ダーク切り替え画像）

ライトモードとダークモードで異なる画像を表示します。

```markdown
{{< dual_theme_image light_src="img/day.webp" dark_src="img/night.webp" alt="説明" />}}
```

**使用例:**

```markdown
{{< dual_theme_image light_src="screenshots/ui-light.webp" dark_src="screenshots/ui-dark.webp" alt="アプリケーションのUI" />}}
```

### invertible_image（反転画像）

ダークモードで色を反転します。グラフや図に適しています。

```markdown
{{< invertible_image src="img/graph.webp" alt="グラフ" />}}
```

**使用例:**

```markdown
{{< invertible_image src="diagrams/architecture.webp" alt="システムアーキテクチャ図" />}}

{{< invertible_image src="charts/performance.webp" alt="パフォーマンス比較グラフ" full_width={true} />}}
```

### dimmable_image（減光画像）

ダークモードで画像を暗くします。明るい写真に適しています。

```markdown
{{< dimmable_image src="img/photo.webp" alt="写真" />}}
```

**使用例:**

```markdown
{{< dimmable_image src="photos/sunset.webp" alt="夕焼けの風景写真" />}}
```

### image_hover（ホバー切り替え画像）

マウスホバーで画像を切り替えます。ビフォー/アフターの比較に適しています。

```markdown
{{< image_hover default_src="img/before.webp" hovered_src="img/after.webp" default_alt="変更前" hovered_alt="変更後" />}}
```

**使用例:**

```markdown
{{< image_hover default_src="optimization/before.webp" hovered_src="optimization/after.webp" default_alt="最適化前のパフォーマンス" hovered_alt="最適化後のパフォーマンス" />}}
```

### image_toggler（クリック切り替え画像）

クリックで画像を切り替えます。

```markdown
{{< image_toggler default_src="img/a.webp" toggled_src="img/b.webp" default_alt="画像A" toggled_alt="画像B" />}}
```

**使用例:**

```markdown
{{< image_toggler default_src="settings/default.webp" toggled_src="settings/custom.webp" default_alt="デフォルト設定" toggled_alt="カスタム設定" />}}
```

### full_width_image（全幅画像）

ヘッダー幅まで拡大した画像を表示します。

```markdown
{{< full_width_image src="img/wide.webp" alt="ワイド画像" />}}
```

**使用例:**

```markdown
{{< full_width_image src="screenshots/dashboard.webp" alt="ダッシュボード全体のスクリーンショット" />}}
```

## Mermaid（ダイアグラム）

Mermaid 記法でダイアグラムを描画します。使用するには frontmatter に
`mermaid = true` を設定する必要があります。

```markdown
{% <mermaid> %}
flowchart LR
    A[開始] --> B[処理]
    B --> C[終了]
{% </mermaid> %}
```

パラメータ:
- `invertible`: ダークモードで反転（デフォルト true）
- `full_width`: ヘッダー幅まで拡大

**使用例:**

```markdown
{% <mermaid> %}
sequenceDiagram
    participant User
    participant App
    participant API
    User->>App: ログイン
    App->>API: 認証リクエスト
    API-->>App: トークン
    App-->>User: ログイン成功
{% </mermaid> %}

{% <mermaid full_width={true}> %}
graph TD
    A[ユーザー入力] --> B{バリデーション}
    B -->|OK| C[データ保存]
    B -->|NG| D[エラー表示]
    C --> E[成功メッセージ]
{% </mermaid> %}
```

## remote_text（外部テキスト埋め込み）

リモート URL またはローカルファイルの内容を埋め込みます。

````markdown
```python
{{< remote_text src="https://example.com/script.py" />}}
```
````

パラメータ:
- `src`: 必須。URL またはファイルパス
- `start`: 開始行番号（1から）
- `end`: 終了行番号

**使用例:**

````markdown
```python
{{< remote_text src="https://raw.githubusercontent.com/user/repo/main/example.py" />}}
```

```rust
{{< remote_text src="https://raw.githubusercontent.com/user/repo/main/src/main.rs" start={10} end={25} />}}
```
````

## multilingual_quote（多言語引用）

原文と翻訳の両方を表示する引用ブロックです。

```markdown
{{< multilingual_quote original="原文" translated="翻訳" author="著者名" />}}
```

**使用例:**

```markdown
{{< multilingual_quote original="The only way to do great work is to love what you do." translated="偉大な仕事をする唯一の方法は、
   自分がやっていることを愛することです。" author="Steve Jobs" />}}
```

## references（参考文献）

ハンギングインデントの参考文献リストを作成します。

```markdown
{% <references> %}
著者名 (年). タイトル. *ジャーナル名*, 巻(号), ページ.

次の参考文献...
{% </references> %}
```

**使用例:**

```markdown
{% <references> %}
Smith, J. (2024). Understanding Web Performance. *Journal of Web
Development*, 15(3), 234-256.

Tanaka, T. (2023). Modern JavaScript Patterns. O'Reilly Media.

Mozilla Developer Network. (2024). CSS Grid Layout.
https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout
{% </references> %}
```

## spoiler（ネタバレ/スポイラー）

クリックするまでテキストをぼかして隠します。

```markdown
答えは {{< spoiler text="42" />}} です。
```

パラメータ:
- `text`: 必須。隠すテキスト
- `fixed_blur`: true にすると固定の「SPOILER」表示

**使用例:**

```markdown
クイズ: JavaScriptで非同期処理を扱う方法は？
答え: {{< spoiler text="Promise、async/await、コールバック" />}}

映画のラスト: {{< spoiler text="主人公は実は幽霊だった" fixed_blur={true} />}}
```

## wide_container（幅広コンテナ）

テーブルやコードブロックをヘッダー幅まで拡大します。

```markdown
{% <wide_container> %}

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |

{% </wide_container> %}
```

**使用例:**

```markdown
{% <wide_container> %}

| フレームワーク | 初回読込 | バンドルサイズ | TypeScript | 学習曲線 |
|---------------|---------|--------------|-----------|---------|
| React         | 速い    | 40 KB        | ✅        | 中      |
| Vue           | 速い    | 33 KB        | ✅        | 低      |
| Angular       | 普通    | 130 KB       | ✅        | 高      |
| Svelte        | 非常に速い | 2 KB      | ✅        | 低      |

{% </wide_container> %}
```

## force_text_direction（テキスト方向強制）

テキストの方向を強制的に変更します。

```markdown
{% <force_text_direction direction="rtl"> %}
右から左に表示されるテキスト
{% </force_text_direction> %}
```

パラメータ:
- `direction`: "ltr"（左から右）または "rtl"（右から左）

**使用例:**

```markdown
{% <force_text_direction direction="rtl"> %}
مرحبا بك في مدونتي
{% </force_text_direction> %}

{% <force_text_direction direction="ltr"> %}
This text is forced left-to-right even in RTL context
{% </force_text_direction> %}
```

## iine（いいねボタン）

iine.to のいいねボタンを追加します。

```markdown
{{< iine slug="/blog/post/like" icon="heart" label="いいね" />}}
```

パラメータ:
- `slug`: ボタンの識別子（デフォルトはページパス）
- `icon`: heart, thumbs_up, upvote, または絵文字
- `label`: アクセシビリティラベル

**使用例:**

```markdown
記事は役に立ちましたか？
{{< iine icon="👍" label="役に立った" />}}

{{< iine slug="/blog/tutorial/react" icon="heart" label="この記事にいいね" />}}
```

## コードブロックのファイル名表示

Zola 0.20.0 以降の標準機能です（コンポーネントではありません）。

````markdown
```rust,name=src/main.rs
fn main() {
    println!("Hello!");
}
```
````

URL を指定すると、`code_block_name_links = true` 設定でリンクになります。

**使用例:**

````markdown
```typescript,name=src/components/Button.tsx
export const Button: React.FC<ButtonProps> = ({ children, onClick }) => {
  return <button onClick={onClick}>{children}</button>;
};
```

```python,name=https://github.com/user/repo/blob/main/example.py
def calculate_sum(numbers: list[int]) -> int:
    return sum(numbers)
```

```bash,name=deploy.sh
#!/bin/bash
npm run build
npm run deploy
```
````
