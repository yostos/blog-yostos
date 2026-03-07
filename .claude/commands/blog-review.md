---
description: Code review for blog config, templates, shortcodes, and workflows.
---

# Blog Config/Template Code Review

Review changes to blog infrastructure (not article content).

## 1. Identify Changes

Run `git diff` to identify changed files and their content.

## 2. Target-Specific Checks

Review based on what was changed:

- **config.toml**: TOML syntax validity, setting values, consistency with tabi theme
- **templates/**: Tera template syntax, correctness of theme overrides
- **shortcodes/**: Shortcode behavior, consistency with CLAUDE.md documentation
- **GitHub Actions (.github/workflows/)**: Workflow syntax, deploy configuration consistency
- **package.json / npm scripts**: Dependency changes, script consistency

## 3. Build Verification

- Run `zola check`
- Run `zola build` to confirm successful build

## 4. Report

Summarize findings:

- Issues and risks identified
- Improvement suggestions
- Confirmation that build passes
