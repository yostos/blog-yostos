# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A blog powered by Zola static site generator. Migration project from Next.js/MDX blog.

## Common Commands

```bash
zola serve          # Dev server with live reload
zola build          # Production build (outputs to public/)
zola check          # Error check
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

## Tag Naming Conventions

See `docs/tag-rule.md` for comprehensive tagging rules and guidelines.

## Writing Style

- **文体**: ですます調（敬体）を使用する
- 技術記事でも読者に語りかける丁寧な文体を維持
- 「：」で終わる文は禁止（「〜します。」「〜です。」などで終える）
- **行の長さ**: 1行80バイト以内に収める（日本語は1文字3バイト）
- **セクション分割**: 過度に細かいセクション分割は避ける
- **太字**: 多用しない。本当に強調が必要な箇所のみ使用

## Migration Source

- Path: `/Users/yostos/ghq/github.com/yostos/blog-yostos/src/app/articles/`
- Format: MDX (Next.js App Router)
- Details: See `docs/TODO.md`
