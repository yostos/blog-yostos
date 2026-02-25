# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
    generation and HTML compatibility fix for Zola minification
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
