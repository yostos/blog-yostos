---
# simple-commit plugin local settings
---

## Local Commit Prefix Rules

Use `content:` prefix for article-related changes instead of `feat:`.

| Change Type | Prefix | Example |
|-------------|--------|---------|
| Article tagging, metadata updates, content edits | **content:** | `content: add tags to 2025-07 articles` |
| New features, theme customization, config changes | **feat:** | `feat: add dark mode toggle` |
| Bug fixes | **fix:** | `fix: correct SoundCloud embed URL` |
| Documentation updates | **docs:** | `docs: update CLAUDE.md` |

**Rule**: Article updates (tags, content) use `content:`. `feat:` is only for new functionality.
