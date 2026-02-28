# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

<!-- jrnl-project: blog-yostos -->

- **Project Name**: blog-yostos
- **Description**: A blog powered by Zola static site generator.
  Migration project from Next.js/MDX blog.

## General Rules

## Available CLI Tools

- `gh` - GitHub CLI for repository operations
- `jq` - JSON processor for parsing API responses
- `curl` - HTTP client for API requests
- `ffmpeg` - Video/audio processing
- `imagemagick` - Image processing (convert, mogrify, etc.)
- `lychee` - Link checker for broken URLs in Markdown files
- `nb` - Knowledge base for reference and storing discussion notes

## Common Commands

```bash
zola serve          # Dev server with live reload
zola build          # Production build (outputs to public/)
zola check          # Error check
npm run lint        # Run textlint on all content
npm run lint:fix    # Auto-fix textlint errors
npm run ogp         # Generate OGP images for articles without ogp.webp
npm run ogp:dry-run # Preview OGP generation without creating files
npx pagefind           # 検索インデックス生成
npx pagefind --dry-run # インデックス生成のプレビュー
# ローカル検索テスト手順:
# zola build && npx pagefind && zola serve
```

## Git Operations

- **Commit**: Use `/simple-commit:commit` skill (auto-generates Conventional Commits format)
- Do not use `git commit` directly
- Local rules: See `.claude/simple-commit.local.md`
- **Staging**: 常に `git add .` を使用する（ファイルを個別に選ばない）
  - `themes/` はsubmoduleなので自動的に除外される
  - 漏れを防ぐため、全変更をまとめてステージング

## Project Structure

```
content/
  _index.md              # Homepage settings
  blog/
    _index.md            # Blog section settings
    YYYY/MM/slug/        # Blog articles (year/month/slug format)
      index.md           # Article body
      image.png          # Article images
themes/tabi/             # tabi theme
docs/TODO.md             # Migration task documentation
```

## Theme: tabi

- Theme: [tabi](https://github.com/welpo/tabi)
- Language: Japanese (`default_language = "ja"`)
- Search: Disabled (Japanese not supported)
- **`themes/` 配下のファイルを絶対に編集しないこと**
  - テーマのカスタマイズは `static/custom.css` で上書きする
  - テンプレートの変更が必要な場合は `templates/` に
    オーバーライドファイルを作成する

## Table of Contents

To add a collapsible table of contents:

```markdown
<details>
<summary>Table of Contents</summary>

<!-- toc -->

</details>
```

## Code Block Syntax

To display a filename on a code block, use the `name=` parameter (Zola 0.20.0+):

````markdown
```bash,name=script.sh
#!/bin/bash
echo "Hello"
```
````

## Shortcodes

ボディ型ショートコード（`{% %} ... {% end %}`）は
必ず textlint 除外コメントで囲むこと。
インライン型（`{{ }}`）もショートコード構文が
textlint に引っかかるため同様に囲む。

### image — 画像表示

記事内の画像表示には Markdown 記法（`![]()`）ではなく
image ショートコードを使用する。
自動でパス解決、width/height 付与、
キャッシュバスティング、遅延読み込みを行う。

```markdown
<!-- textlint-disable -->

{{ image(src="photo.webp", alt="説明テキスト") }}

<!-- textlint-enable -->
```

- `src`: 画像パスまたはURL（必須）
- `alt`: 代替テキスト（推奨）
- `lazy_loading`: 遅延読み込み（デフォルト: true）

同一ディレクトリの画像は `src="photo.webp"` または
`src="./photo.webp"` のどちらでも指定可能。

### remote_text — 外部ファイル読み込み（tabi組み込み）

リモートURLまたはローカルファイルの内容を
コードブロック内に埋め込む。
ソースコードの引用に使用する。

````markdown
<!-- textlint-disable -->

```html,name=templates/shortcodes/image.html
{{ remote_text(src="templates/shortcodes/image.html") }}
```

<!-- textlint-enable -->
````

行範囲の指定も可能。

````markdown
<!-- textlint-disable -->

```rust
{{ remote_text(src="https://raw.githubusercontent.com/user/repo/main/src/main.rs", start=10, end=25) }}
```

<!-- textlint-enable -->
````

- `src`: ファイルパスまたはURL（必須）
- `start`: 開始行（任意、1始まり）
- `end`: 終了行（任意）
- ローカルファイルは記事ディレクトリからの相対パス
  → プロジェクトルートからのパスの順で解決
- `remote_text` の出力はショートコードとして
  再解釈されないため、Tera構文（`{{ }}`、`{% %}`）を
  含むコードも安全に表示できる

### admonition — 警告・情報ボックス

```markdown
<!-- textlint-disable -->

{% admonition(type="warning", title="注意") %}
内容テキスト（Markdown使用可）
{% end %}

<!-- textlint-enable -->
```

- `type`: info（デフォルト）, warning, tip, note,
  danger, bug, example, quote, abstract, success,
  question, failure
- `title`: 見出し（デフォルトはtypeの大文字表記）
- `icon`: アイコン（デフォルトはtype準拠）

### mermaid — Mermaid図

frontmatterに `[extra] mermaid = true` を追加すること。

```markdown
<!-- textlint-disable -->

{% mermaid(invertible=true, full_width=false) %}
flowchart LR
A[開始] --> B[処理] --> C[終了]
{% end %}

<!-- textlint-enable -->
```

- `invertible`: ダークモードで色反転
  （デフォルト: true）
- `full_width`: 全幅表示（デフォルト: false）

### spoiler — ネタバレ隠し

```markdown
<!-- textlint-disable -->

{% spoiler() %}
隠したいテキスト
{% end %}

<!-- textlint-enable -->
```

- `fixed_blur`: 固定ぼかし（デフォルト: false）
- クリックで内容を表示

### aside — サイドノート

```markdown
<!-- textlint-disable -->

{% aside() %}
補足テキスト
{% end %}

<!-- textlint-enable -->
```

- `position`: 表示位置（任意）

### references — 参考文献

参考サイトを掲載する場合はこのショートコードを使用する。
必ず `## References`（参考文献）セクションを設けること。

記法：

- 日本語: `サイト名. 「[記事タイトル](URL)」`
- 英語: `サイト名. "[Article Title](URL)"`
- 書籍: `著者. (出版年). 『[書籍名](URL)』`

引用符はリンクの外に配置する。
日本語は「」、英語は""を使用する。

```markdown
<!-- textlint-disable -->

{% references() %}
- Zenn. [「Zolaで技術ブログを作る」](https://zenn.dev/example)
- 結城浩. (2020). [『数学ガール』](https://example.com/book)
{% end %}

<!-- textlint-enable -->
```

### multilingual_quote — 多言語引用切替

```markdown
<!-- textlint-disable -->

{{ multilingual_quote(
  translated="翻訳文",
  original="Original text",
  author="著者名",
  lang="en"
) }}

<!-- textlint-enable -->
```

- `translated`: 翻訳テキスト（必須）
- `original`: 原文テキスト（必須）
- `lang`: 原文の言語コード（必須）
- `author`: 著者名（任意）
- クリックで翻訳と原文を切替表示

### wide_container — 全幅コンテナ

```markdown
<!-- textlint-disable -->

{% wide_container() %}
全幅で表示したい内容
{% end %}

<!-- textlint-enable -->
```

### youtube — YouTube埋め込み（カスタム）

```markdown
<!-- textlint-disable -->

{{ youtube(id="VIDEO_ID") }}

<!-- textlint-enable -->
```

`VIDEO_ID` は URL の `v=` または `youtu.be/` の後の部分。

### linkcard — リンクカード（カスタム）

URLをカード形式で表示する。
はてなブログカード（iframe）で表示。

```markdown
<!-- textlint-disable -->

{{ linkcard(url="https://example.com/page") }}

<!-- textlint-enable -->
```

### spot — スポット情報（地図+施設情報）

OpenStreetMap の地図埋め込みと
施設情報を表示するカード。
GEO URIで位置を指定する。

```markdown
<!-- textlint-disable -->

{{ spot(geo="geo:35.76044,140.10773?z=16"
        name="新川千本桜",
        address="千葉県八千代市米本",
        tel="047-XXX-XXXX",
        access="最寄りは米本団地バス停"
) }}

<!-- textlint-enable -->
```

- `geo`: GEO URI（必須）`geo:緯度,経度?z=ズーム`
- `name`: スポット名（任意）
- `address`: 住所（任意）
- `tel`: 電話番号（任意、空文字で非表示）
- `access`: アクセス情報（任意）

## Article Frontmatter Format

```toml
+++
title = "記事タイトル"
description = "説明"
date = 2026-01-23
updated = 2026-01-25        # 更新時に必ずセット
aliases = ["/old/url/path"]  # リダイレクト用

[taxonomies]
tags = ["タグ1", "タグ2"]    # docs/tag-rule.md 参照

[extra]
social_media_card = "ogp.webp"  # OGP画像（必須）
canonical_url = "https://..."   # 正規URL（任意）
tldr = "記事の要約テキスト"      # TL;DRボックス（任意）
katex = true                    # 数式表示（任意）
+++
```

プロジェクトページでカード画像を表示する場合：

```toml
[extra]
local_image = "path/to/image.webp"
local_image_dark = "path/to/image-dark.webp"
```

新規記事作成後、`npm run ogp` を実行して
OGP画像を生成してください。

## OGP画像生成

OGP画像は `npm run ogp` で生成します。日本語フォントが必要です。

```
scripts/fonts/NotoSansJP-Regular.ttf  # または好みのフォント（.ttf/.otf）
```

フォントは `.gitignore` で除外されているため、各自で配置してください。
Noto Sans JPは[Google Fonts](https://fonts.google.com/noto/specimen/Noto+Sans+JP)
から無料でダウンロードできます。

### Description Field Rules

- **必ず完全な文章で終える**: 体言止めや文末が助詞で終わる表現は禁止
- **句点で終える**: 「〜します。」「〜です。」など、必ず句点「。」で終える
- **文字数制限**: 200文字以内（textlintルール準拠）
- **内容の質**:
  - 記事一覧でリード文として使われることを意識する
  - 読者の興味を引く魅力的な内容にする
  - textlintを通すためだけに重要な情報を削除しない
  - 記事の核心的な価値や独自性を伝える
- **フォーマット**: 長い場合はTOMLの複数行文字列（`"""`）を使用

例：

- ❌ 悪い例: `"Claude Codeプラグインの開発方法"`（体言止め）
- ❌ 悪い例: `"Claude Codeプラグインを開発"`（助詞で終わる）
- ❌ 悪い例: `"プラグインを開発しました。"` (情報が少なすぎる)
- ✅ 良い例:

  ```toml
  description = """
  Claude Codeプラグインの開発方法を実践的に解説します。
  実装例とともに、プラグインシステムの設計思想や
  デバッグのコツまで、実務で使える知識をお届けします。
  """
  ```

## Tag Naming Conventions

See `docs/tag-rule.md` for comprehensive tagging rules and guidelines.

## Writing Style

- **文体**: ですます調（敬体）を使用する
- 技術記事でも読者に語りかける丁寧な文体を維持
- 「：」で終わる文は禁止（「〜します。」「〜です。」などで終える）
- **セクション分割**: 細かいセクション分割は禁止
  - 1〜2段落程度の短い内容にセクション見出しを付けない
  - 「撮影機材」「アクセス」など短い情報は本文に自然に組み込む
  - レベル3見出し（`###`）は原則使用禁止。必要な場合はユーザーに確認
  - 太字（`**text**`）だけで独立した行を作り、
    見出し代わりにすることは禁止
    （文中でキーワードを強調する用途は問題ない）
- **太字**: 多用しない。本当に強調が必要な箇所のみ使用

## textlint Rules

- **ドラフト作成時はtextlintを実行しない**:
  記事のドラフト作成中は、ユーザーの指示があるまで
  `npm run lint` を実行しないこと

- **textlint除外コメントの使用禁止**:
  エラー回避のために `<!-- textlint-disable -->` /
  `<!-- textlint-enable -->` を使用することは禁止
  - 例外: ユーザーが明示的に承認した場合
    （`author-approved` コメントを付与する）
  - 例外: ショートコード部分（下記参照）
  - 例外: ライセンス文や引用など、変更すべきでない文章
  - 承認済みの disable には必ず理由コメントを併記する:
    `<!-- textlint-disable --> <!-- author-approved: 理由 -->`
  - 理由なしの `<!-- textlint-disable -->` 単独使用はルール違反
- **ショートコードの除外**:
  `%}` で終わるショートコード（例: `{% admonition %}...{% end %}`）を
  使用する場合は、必ず textlint 除外コメントで囲む

  ```markdown
  <!-- textlint-disable -->

  {% admonition(type="warning", title="タイトル") %}
  内容
  {% end %}

  <!-- textlint-enable -->
  ```

## textlint Automation

このプロジェクトではtextlintの自動チェックが以下のタイミングで実行されます。

### Pre-commit Hook（変更ファイルのみ）

- `git commit` 時に自動実行（Husky + lint-staged）
- ステージングされたMarkdownファイルのみチェック
- エラーがある場合はcommitがブロックされる
- 設定: `.husky/pre-commit`

### Pre-push Hook（全ファイル）

- `git push` 時に自動実行（Husky）
- `content/**/*.md` の全ファイルをチェック
- エラーがある場合はpushがブロックされる
- 設定: `.husky/pre-push`

### GitHub Actions（CI）

- mainブランチへのpush/Pull Request時に自動実行
- 全ファイルをチェック
- CIステータスはGitHub上で確認可能
- 設定: `.github/workflows/textlint.yml`

### Bypass方法（非推奨）

緊急時のみ以下の方法でフックをスキップ可能（非推奨）：

```bash
git commit --no-verify    # pre-commitをスキップ
git push --no-verify      # pre-pushをスキップ
```

ただし、GitHub ActionsのCIは必ず実行されるため、
最終的にはtextlintエラーを修正する必要があります。

## カバー画像生成（OpenAI DALL-E 3）

記事のカバー画像を生成する場合に使用します。
`OPENAI_API_KEY` の設定が必要です。

```bash
# 16:9 カバー画像の生成
./scripts/generate-cover.sh \
  -p "プロンプト" \
  -o content/blog/YYYY/MM/slug/cover.jpg

# 正方形画像
./scripts/generate-cover.sh \
  -p "プロンプト" \
  -o output.jpg -s 1024x1024
```

- `-p`: 画像生成プロンプト（必須）
- `-o`: 出力ファイルパス（必須）
- `-s`: サイズ（デフォルト: 1792x1024 = 16:9）
- `-q`: 品質 standard / hd（デフォルト: hd）

利用シーン:
- ユーザーからカバー画像の作成を依頼された場合
- 記事の内容に即したイメージ画像が必要な場合
- 写真素材がなくコンセプチュアルな画像が適切な場合

## Migration Source

- Path: `src/app/articles/` (relative to project root)
- Format: MDX (Next.js App Router)
- Details: See `docs/TODO.md`
