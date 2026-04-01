# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

<!-- jrnl-project: blog-yostos -->

- **Project Name**: blog-yostos
- **Description**: A blog powered by Zola static site generator.
  Migration project from Next.js/MDX blog.

## Git Operations

- **Staging**: Always use `git add .` to stage all changes. Never stage individual files.
- **Commit**: Use `/simple-commit:commit` skill (auto-generates Conventional Commits format)
- Local rules: See `.claude/simple-commit.local.md`

## Commands

```bash
zola serve                       # Dev server (http://127.0.0.1:1111)
zola build                       # Build to public/
npm run ogp                      # Generate OGP images
npm run ogp:dry-run              # Preview OGP generation
npm run search                   # Build pagefind search index
npm run lint                     # textlint (content/**/*.md)
npm run lint:fix                 # textlint auto-fix
bash scripts/indexnow.sh <path>  # Notify IndexNow
```

## Directory Structure

```
content/          # Blog articles (Markdown + assets)
templates/        # Zola template overrides (macros, partials, shortcodes)
themes/tabi/      # tabi theme (submodule)
scripts/          # OGP generation, image conversion, IndexNow
tools/            # Additional tooling and docs
static/           # Static assets served at site root
docs/             # Project documentation (tag rules, architecture decisions)
```

## Hosting

- Cloudflare Workers (`wrangler.toml`), domain: `codedchords.dev`
- Deploy: push to main triggers GitHub Actions → zola build → Cloudflare Workers

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

See `docs/tabi-shortcodes.md` for shortcode syntax details.

All shortcodes must be wrapped in textlint-disable/enable comments:

```markdown
<!-- textlint-disable -->

{{ image(src="photo.webp", alt="説明テキスト") }}

<!-- textlint-enable -->
```

When the user requests a references section, place it as `## References` using the `references` shortcode.
**IMPORTANT**: `references` is a body shortcode (`{% %}`), NOT a function shortcode (`{{ }}`):

```markdown
{% references() %}

- [サイト名](URL). 「記事タイトル」
- [Site](URL). "Title"

{% end %}
```

## Article Frontmatter Format

```toml
+++
title = "記事タイトル"
description = "説明"
date = 2026-01-23
updated = 2026-01-25        # set on update
aliases = ["/old/url/path"]  # redirect

[taxonomies]
tags = ["タグ1", "タグ2"]    # see docs/tag-rule.md

[extra]
social_media_card = "ogp.webp"  # OGP image (required)
canonical_url = "https://..."   # canonical URL (optional)
local_image = "cover.webp"      # cover image (required)
tldr = "記事の要約テキスト"      # TL;DR box (optional)
katex = true                    # math rendering (optional)
+++
```

Cover image is also used within the article.
The following line is required at the beginning of the article body:
`{{ image(src="cover.webp", alt="Cover") }}`

### Description Field Rules

- Must end with a complete sentence (no noun-ending or particle-ending)
- Must end with Japanese period "。"
- Within 200 characters
- Should be attractive as a lead text in article listings
- Use TOML multi-line strings (`"""`) for longer descriptions

## Tag Naming Conventions

See `docs/tag-rule.md` for comprehensive tagging rules and guidelines.

## Writing Style

- **Tone**: Use desu/masu style (敬体). Maintain polite tone even in technical articles
- Sentences must not end with "："
- **No em-dash paraphrase in Japanese**: Do not use `— 補足説明 —` style inline parenthetical rephrasing. Use natural Japanese syntax instead (e.g. `〜と同様に「補足」という課題`)
- **Section splitting**: Avoid excessive section splitting
  - Do not add headings to short content (1-2 paragraphs)
  - Integrate short info (e.g. equipment, access) naturally into body text
  - Level-3 headings (`###`) are generally prohibited. Ask user if needed
  - Bold text (`**text**`) as standalone heading-substitute lines is prohibited
    (inline emphasis for keywords is fine)
- **Bold**: Use sparingly. Only where emphasis is truly needed

## Save Destination

- When the user explicitly specifies a save destination (e.g. "CLAUDE.mdに記録して"), always follow that instruction exactly
- Do not substitute memory or other storage when a specific destination is given
- Only use your own judgment for save destination when none is specified

## textlint Rules

- Do not run `npm run lint` during drafting (only on user request)
- Using `<!-- textlint-disable -->` to bypass errors is prohibited
  - Exceptions: shortcodes, license text, user-approved cases
  - Approved cases must include `<!-- author-approved: reason -->` comment
