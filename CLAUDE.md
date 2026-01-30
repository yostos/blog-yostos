# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A blog powered by Zola static site generator. Migration project from Next.js/MDX blog.

## General Rules

- **Line Length**: Wrap lines at 80 bytes maximum
  - Japanese characters: 3 bytes per character
  - Apply to all text files: Markdown, code, configuration files, etc.

## Common Commands

```bash
zola serve          # Dev server with live reload
zola build          # Production build (outputs to public/)
zola check          # Error check
npm run lint        # Run textlint on all content
npm run lint:fix    # Auto-fix textlint errors
```

## Git Operations

- **Commit**: Use `/simple-commit:commit` skill (auto-generates Conventional Commits format)
- Do not use `git commit` directly
- Local rules: See `.claude/simple-commit.local.md`

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

## Article Frontmatter Format

```toml
+++
title = "記事タイトル"
description = "説明"
date = 2026-01-23
aliases = ["/old/url/path"]  # For redirects

[extra]
canonical_url = "https://..."  # Canonical URL (when another site is the original)
+++
```

### Description Field Rules

- **必ず完全な文章で終える**: 体言止めや文末が助詞で終わる表現は禁止
- **句点で終える**: 「〜します。」「〜です。」など、必ず句点「。」で終える
- **文字数制限**: 200文字以内（textlintルール準拠）
- **行の折り返し**: 80バイト前後で折り返す（複数行の場合）
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
- **行の長さ**: 1行80バイト以内に収める（日本語は1文字3バイト）
- **セクション分割**: 過度に細かいセクション分割は避ける
- **太字**: 多用しない。本当に強調が必要な箇所のみ使用

## textlint Rules

- **textlint除外コメントの使用禁止**:
  エラー回避のために `<!-- textlint-disable -->` /
  `<!-- textlint-enable -->` を使用することは禁止
  - 例外: ユーザーが明示的に承認した場合
  - 例外: ショートコード部分（下記参照）
  - 例外: ライセンス文や引用など、変更すべきでない文章
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

## Migration Source

- Path: `/Users/yostos/ghq/github.com/yostos/blog-yostos/src/app/articles/`
- Format: MDX (Next.js App Router)
- Details: See `docs/TODO.md`
