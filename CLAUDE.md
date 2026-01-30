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

Follow English-language blog/media site conventions.

| Category | Format | Reference |
|----------|--------|-----------|
| Books | **Books** | NYT, The Guardian, NPR |
| Manga | **Manga** | Japanese comics recognized as "Manga" |
| Movies | **Movies** | NYT (Movies) |
| Music | **Music** | Singular/uncountable |
| Music Production | **Music Production** | DAW, Synthesizer V, etc. "DTM" is Japanese-only term |
| Guitar | **Guitar** | Singular |
| Effects pedals | **Pedals** or **Effects** | "Effector" is Japanese-only term |
| Technology | **Tech** or **Technology** | Medium, BBC, The Verge |
| Travel | **Travel** | Singular |
| Certification | **Certification** | Singular |
| Photography | **Photography** | As activity/hobby |
| Security | **Security** | Singular |
| Design | **Design** | Medium |
| Culture | **Culture** | The Guardian |
| Korea | **Korea** | Use "North Korea" explicitly for DPRK |
| Accessibility | **Accessibility** | Uncountable |
| Seasons | **Seasons** | Seasonal topics (cherry blossoms, autumn leaves, etc.) |
| Productivity | **Productivity** | Productivity tools in general |
| Note-taking | **Note-taking** | LogSeq, Workflowy, nb, etc. |

**Principle**: Singular form is standard. Books and Movies are exceptions where plural is established.

## Migration Source

- Path: `/Users/yostos/ghq/github.com/yostos/blog-yostos/src/app/articles/`
- Format: MDX (Next.js App Router)
- Details: See `docs/TODO.md`
