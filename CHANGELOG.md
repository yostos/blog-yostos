# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-09-29

### Changed (BREAKING)
- Migrate to Zola 0.23.6 and tabi v5
  - Shortcodes replaced with Tera 2 components
    (`templates/components/`); article syntax changes from
    `{{ name(key="value") }}` to `{{< name key="value" />}}`
    and from `{% name() %}...{% end %}` to
    `{% <name> %}...{% </name> %}`
  - The whole Markdown body is now rendered by Tera; literal
    `{{ }}` / `{% %}` must be wrapped in `{% raw %}`
  - `image`, `linkcard`, `module`, `spot`, `youtube` and
    `list_posts` moved to components
  - All articles converted with
    `scripts/migrate-shortcodes-zola-0.23.py`
  - Removed `static/giallo.css`
  - CI pinned to Zola 0.23.6
  - Migration log in `docs/zola-0.23-migration-log.md`
- Set site language to `ja`

### Added
- `blockquote` component for quotations with author, source
  and link
- Tag taxonomy rebuilt with vector matching
  - Two-layer tagset in `data/tagset.toml` and tag-name
    embeddings in `data/tag-vectors.json` (Voyage AI)
  - Tags recommended from five extracted keywords per article
  - `scripts/assign-tags.py`, `scripts/build-tag-vectors.py`,
    `scripts/tag_embedding.py`, `article-tag` command
  - All articles retagged
  - ADR-0005 (keep full-content Atom feed) and ADR-0006
    (tag-name vectors instead of article centroids)
- Ask page and navigation menu entry
- `rel=author` link in `<head>`
- Claude Code hook that checks commit message prefixes

### Changed
- Cover images generated as AVIF; image format rules for new
  articles documented (AVIF for photos, lossless WebP for
  diagrams)
- Web fonts served from Cloudflare R2 instead of S3/CloudFront
- Body font switched to system sans-serif (Helvetica Neue /
  Hiragino Sans); Google Fonts import removed
- SixBraille font limited to braille glyphs in the banner header
- Profile images shrunk to 384px bilevel WebP (about 9 KB to
  122 bytes)
- Embedded SoundCloud players replaced with YouTube
- Removed unused neovim-theme submodule

### Fixed
- Broken images on articles whose directory names contained
  uppercase letters; directories renamed to lowercase to match
  permalinks, and internal links updated
- YouTube embeds on Cloudflare: iframe replaced with the
  shortcode, curly quotes replaced with straight quotes
- Bluesky auto-post: strip TOML line continuations from the
  description and upload the OGP image as the link card
  thumbnail
- GitHub Actions upgraded to Node.js 24 compatible versions
  (`actions/checkout@v6`, `actions/setup-node@v6`)

## [1.2.2] - 2026-03-18

### Added
- Bluesky auto-post on new article publish
  - GitHub Actions workflow triggered on push to main
  - Detects new articles via git diff (Added status only)
  - Posts "📝 Just published:" with #blog and article tags
  - Link card with title and description via
    `app.bsky.embed.external`
  - Hashtag facets for rich text rendering
  - `scripts/bluesky-post.sh` for Bluesky AT Protocol API
  - ADR-0002 and specification document

## [1.2.1] - 2026-02-25

### Changed
- Disable `minify_html` to fix Pagefind compatibility
  - Zola's HTML minification stripped `</head>`, causing
    Pagefind to fail language detection
  - Removed `sed` workaround from CI/CD pipeline
  - Simplified local search test procedure in CLAUDE.md

## [1.2.0] - 2026-02-25

### Added
- Site-wide search powered by Pagefind
  - Full-text search indexing for 303 blog articles (17,217
    words)
  - Japanese language support with CJK segmentation (extended
    Pagefind)
  - Static search index generation at build time, no external
    service needed
  - Dark mode support with tabi evangelion skin integration
  - Dedicated `/search/` page with custom search UI
  - Search link in main navigation menu
  - Zola integration: `pagefind.yml` configuration file
  - npm scripts: `search` and `search:dry-run` for local
    testing
  - GitHub Actions CI/CD integration with automatic index
    generation
  - Architectural Decision Record (ADR-0001) and implementation
    plan documentation

## [1.1.0] - 2026-02-13

### Added
- Linkcard feature for displaying URLs as cards in articles
  - GitHub repository cards with Octocat icon, owner/repo,
    description, and language via GitHub API
  - Hatenablog card iframe for automatic OGP preview of other URLs
  - Generate-linkcard.mjs script for GitHub metadata caching
  - Zola shortcode {{ linkcard(url="...") }} for easy integration
  - Dark mode support and mobile responsive design
  - Comprehensive specification document at docs/linkcard.md
  - npm scripts: `linkcard` and `linkcard:dry-run` for metadata
    management with `--force` option for cache refresh

## [1.0.1] - 2026-02-13

### Added
- Blog articles: HHKB, Rain Beatles cover, stagnant system
  migration, Claude Opus 4.6, GitHub Pages security headers,
  shiramazu drone, snow fell, cognitive divergence in AI era,
  OGP image generation, Urusei Yatsura ED guitar cover,
  Claude Code jrnl-tools plugin
- Music page with SoundCloud playlists
- OGP image generation feature and KADOMA font support
- OGP image check in pre-commit hook

### Fixed
- Responsive layout: reduce excessive gap between date and
  article title on narrow screens
- OGP article title, description, and regenerated ogp.webp
- KADOMA font URL updated to CloudFront

### Changed
- Upgrade Zola to 0.22.1 and improve documentation
- Font styling: set date/description font-weight to 400,
  use BerkeleyMono for header
- Home banner subtitle sizing adjustment
- Simplify git staging guidelines

## [1.0.0] - 2026-01-31

### Added
- Claude Code Review workflow
- Claude PR Assistant workflow
- textlint automation with Husky and GitHub Actions
- GitHub Actions workflow for Zola deployment
- MIT License file

### Fixed
- include package-lock.json for GitHub Actions CI caching
- fix theme submodules configuration

### Changed
- use Monaspace Neon for code and enable ligatures
- add Berkeley Mono weights and definition list styling
- skip workflows for Claude bot
- remove deprecated Husky pre-push hook format
- update Zola to 0.22.1 for definition list support
- standardize tags and fix external links
- update styling and fix navigation menu
- rename zola.toml to config.toml
