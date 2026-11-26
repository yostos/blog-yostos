# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

<!-- jrnl-project: blog-yostos -->

- **Project Name**: blog-yostos
- **Description**: A blog powered by Zola static site generator.
  Migration project from Next.js/MDX blog.

## Git Operations

- **Workflow**: GitHub Flow. `main` is protected; every change, including typo fixes,
  goes through a branch and a PR, and publishing means squash-merging the PR.
  See `docs/repository-workflow.md`
- **Before starting work**: Check the current branch. If on `main`, create a branch first
  (`content/<slug>` for articles; `feature/`, `fix/`, `refactor/` for other changes).
  If already on a branch (e.g. a branch that `@claude` pushed), keep working on it
- **PR title**: Follow the prefix rules in `docs/repository-workflow.md` ("PR のタイトル").
  The PR title becomes the commit title on `main`
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
npm run search:dry-run           # Preview pagefind index
npm run lint                     # textlint (content/**/*.md)
npm run lint:fix                 # textlint auto-fix
bash scripts/indexnow.sh <path>  # Notify IndexNow
bash scripts/generate-cover.sh   # Generate article cover image (used by article-cover skill)
python scripts/convert-images.py # One-off migration: rewrite ![](  ) to {{< image />}}
```

## Directory Structure

```
content/          # Blog articles (Markdown + assets)
templates/        # Zola template overrides (components, partials)
themes/tabi/      # tabi theme (git submodule — run `git submodule update --init --recursive` after clone)
scripts/          # OGP generation, image conversion, IndexNow
tools/            # Additional tooling and docs
static/           # Static assets served at site root
docs/             # Project documentation (repository workflow, tag rules, architecture decisions)
```

## Hosting

- Cloudflare Workers (`wrangler.toml`), domain: `codedchords.dev`
- Deploy: merging a PR updates `main`, which triggers GitHub Actions → zola build → Cloudflare Workers

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

## Components

Zola 0.23 replaced shortcodes with Tera 2 components (see `docs/zola-0.23-migration-log.md`).
See `docs/tabi-shortcodes.md` for component syntax details.

- Inline: `{{< name key="value" />}}`
- Block: `{% <name key="value"> %}` ... `{% </name> %}`
- Non-string values go in braces: `link_to_self={true}`

All components must be wrapped in textlint-disable/enable comments:

```markdown
<!-- textlint-disable -->

{{< image src="photo.webp" alt="説明テキスト" />}}

<!-- textlint-enable -->
```

The whole Markdown body is rendered by Tera. Literal `{{ }}`, `{% %}` or `{# #}` in an article
(e.g. GitHub Actions `${{ secrets.X }}`, template examples) must be wrapped in
`{% raw %}` ... `{% endraw %}`, even inside code blocks.

For a quotation with attribution, use the site's `blockquote` component
(`templates/components/blockquote.html`). All parameters are optional; the attribution
renders as "— author、source", with `source` (or `author`) linked to `cite`:

```markdown
<!-- textlint-disable -->

{% <blockquote cite="https://..." source="記事・文書の名前" author="発言者・発行元"> %}
引用文（Markdown 可）
{% </blockquote> %}

<!-- textlint-enable -->
```

When the user requests a references section, place it as `## References` using the `references` component.
**IMPORTANT**: `references` is a block component (`{% <references> %}`), NOT an inline one (`{{< />}}`):

```markdown
{% <references> %}

- [サイト名](URL). 「記事タイトル」
- [Site](URL). "Title"

{% </references> %}
```

Do NOT list news media outlets (newspapers, TV, wire services, news sites) in References.
Cite primary sources instead: government agencies, municipalities, companies, and
official statistics. Facts sourced from news reports may still appear in the body text.

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
local_image = "cover.avif"      # cover image (required for new articles; checked by cover-check)
tldr = "記事の要約テキスト"      # TL;DR box (optional)
katex = true                    # math rendering (optional)
+++
```

Cover image is also used within the article.
Place the following line at the beginning of the article body, unless the author leaves it out on purpose:
`{{< image src="cover.avif" alt="Cover" />}}`

### Image Format

Applies to new articles only. Existing articles keep their current files.

| Content | Format | Command |
|---|---|---|
| Photos, AI-generated covers | AVIF (lossy) | `avifenc -q 60 -y 420 -s 6 --ignore-exif --ignore-xmp in.png out.avif` |
| Diagrams, charts, screenshots | WebP (lossless) | `cwebp -lossless -z 9 -exact in.png -o out.webp` |
| OGP (`social_media_card`) | WebP | generated by `npm run ogp` |

Diagrams must not be encoded as AVIF: detail loss defeats their purpose, and AVIF
lossless is 2.5-3.6x larger than WebP lossless. OGP stays WebP because most social
media crawlers do not support AVIF.

### Description Field Rules

- Must end with a complete sentence (no noun-ending or particle-ending)
- Must end with Japanese period "。"
- Within 200 characters
- Should be attractive as a lead text in article listings
- Use TOML multi-line strings (`"""`) for longer descriptions
- It is a lead that makes readers want to open the article, not a summary. State the situation
  and the question; do not give away the conclusion. If a reader could skip the article after
  reading it, rewrite it
- The author writes the description. You may draft it once in a first draft, but do not
  shorten, rephrase or rewrite it afterwards unless asked, including when asked to revise the body
- "リード文" means the first paragraph of the body, not the description. If it is unclear
  which one is meant, ask

### Tags, OGP and Cover Images

- Do not write, change, reformat or suggest `[taxonomies]` tags unless explicitly asked.
  The author sets tags after the article is finished (`/article-tag`)
- Do not generate, delete or regenerate `ogp.webp`, and do not run `npm run ogp`.
  `/article-publish` generates it. A missing `ogp.webp` while drafting is normal.
  Never propose regenerating many OGP images: binary diffs bloat the repository
- `scripts/generate-cover.sh` (used by `/article-cover`) calls a paid API. Get approval for
  the prompt first and generate only the one approved version. When showing an English prompt
  for approval, add a Japanese translation

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
- **List items**: Write list items in plain style (である調) or noun-ending, while body text stays
  敬体. textlint (`no-mix-dearu-desumasu`) expects ですます in the body and である in lists
- **Aside**: Write `aside` text in である調. Place the aside *before* the paragraph it explains
  (it renders beside the next paragraph). Start with the term it explains ("Critical とは、"),
  and keep it to one or two short, concrete sentences that help the reader decide what to do
- **Tables**: Choose alignment per column by content (text left, numbers right).
  Do not left-align everything by rule
- **Headings**
  - Each heading alone must tell what the section is about; no generic or poetic headings.
    Check by reading the list of headings by itself
  - Name the topic, but do not enumerate the section's contents in the heading
  - For a section that tests or examines something, state the question, not the conclusion
    (「図版にAVIFを使えるか」). Sections that evaluate or score use a noun form instead
  - Do not put package names unknown to readers in headings unless the section is about them
- **Links**: Link sources inline on the relevant words. Do not use footnotes to present links,
  and do not repeat links to the same source; one or two places are enough
- **Lead paragraph**: Must stand alone for a first-time reader. Do not start with
  「前回の記事では」; state facts from earlier articles directly
- **Series**: In the newest installment, do not preview the next one, even if the notes do.
  Leave previews in earlier installments and the automatic next links as they are
- **Repository internals**: When the body mentions a command, file or frontmatter key, assume
  readers do not know it and add what it does, or remove it
- **No defensive hedging**: Write a disclaimer once, where it matters most. Do not add sentences
  that give the reader no information, do not write which facts you verified, and do not soften
  facts with 「〜と思われる」. Facts are stated; guesses are limited to the author's own case
- **No invented details**: Do not add numbers, durations or scenes the author did not state.
  Ask if a specific number is needed
- **Font names**: In prose, write 更紗ゴシック. Use `Sarasa Term J` only where the family
  must be identified
- **Read through before finishing**: Reread what you wrote for flow, not only facts. Watch for
  stacked hearsay and quotation, sentences that describe the document's structure, sentences that
  only restate the previous one, and reassuring sentences after a conclusion

## Editing Existing Articles

- Change only what was asked. Do not widen or narrow the scope. When asked to review or verify,
  report problems; do not fix them, even typos or factual errors
- When a quoted part is to be deleted, delete only that part. Do not add items to a table or list
  the author narrowed down; propose them one by one instead. Apply multiple instructions individually
- Edit files in place; do not rebuild a whole file, which silently replaces unrelated parts such as
  the description. "ブラッシュアップ" is about the body, not the title or description
- List every change you made on your own judgment in your report
- Keep the author's wording unless a clearly better alternative exists. Fix typos, factual errors
  and broken syntax; leave stylistic preferences alone
- If a sentence has an omitted subject that can be read two ways, keep it and ask which is meant
- Text that was in an earlier draft but is gone now was removed on purpose; do not restore it
- When the author sets a heading or title wording (「〜にしましょう」), use it verbatim. Suggest
  improvements separately
- Keep items the author listed separately as separate items, and do not split one item into several.
  A checklist has one check per line

## Research and Sources

- When asked where a statement comes from, fetch the primary source and check it. Never blur the
  subject (「〜とされています」) to hide a missing source. Mark unverified items as such, or drop them
- Do not question the author's first-hand statements (equipment used, own performance, intended meaning).
  Verify only external facts, and report briefly
- When citing the author's past articles, take the stated opinion, not a closing rhetorical question,
  which may be ironic

## Save Destination

- When the user explicitly specifies a save destination (e.g. "CLAUDE.mdに記録して"), always follow that instruction exactly
- Do not substitute memory or other storage when a specific destination is given
- Only use your own judgment for save destination when none is specified

## textlint Rules

- In interactive sessions, do not run `npm run lint` during drafting (only on user request).
  When working in GitHub Actions (`@claude`), run it before pushing and fix the errors
- Using `<!-- textlint-disable -->` to bypass errors is prohibited
  - Exceptions: components, license text, user-approved cases
  - Approved cases must include `<!-- author-approved: reason -->` comment
- The same comment records any approved exception to other writing rules (e.g. a level-3 heading).
  Add it in the same edit that applies the exception. Reviews must not report approved exceptions

## Build

- In interactive sessions, do not run `zola build` or `zola serve` to check your edits. The author
  builds and previews. Workflows the author starts (e.g. `/article-publish`) may build
- When working in GitHub Actions (`@claude`), run `zola build` with a temporary output directory
  before pushing. The `zola-build` required check runs it again on the PR

## Work Logs

- For infrastructure work such as Zola or theme upgrades, create a log in `docs/` before starting,
  and record each step's commands, results, problems and new features as you go.
  The author uses these logs as material for articles
