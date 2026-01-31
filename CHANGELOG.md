# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
