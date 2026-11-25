---
# simple-commit plugin local settings
---

## Local Commit Prefix Rules

Use the same prefixes as the PR title rules in `docs/repository-workflow.md`
("PR のタイトル"). With squash merge, the PR title becomes the commit title on `main`.

| Prefix | Use for | Example |
|--------|---------|---------|
| **content:** | Article additions, updates, fixes (typos, tags, metadata, article images) | `content: add tags to 2025-07 articles` |
| **feat:** | Site features: templates, components, scripts, workflows | `feat: add dark mode toggle` |
| **fix:** | Bug fixes in site features | `fix: correct SoundCloud embed URL` |
| **style:** | Visual-only changes: CSS, fonts, layout, site-wide images | `style: tighten top spacing` |
| **refactor:** | Restructuring without behavior change | `refactor: simplify OGP template` |
| **perf:** | Page speed or file size improvements | `perf: shrink profile images` |
| **docs:** | Repository documents: `docs/`, README, CLAUDE.md | `docs: update CLAUDE.md` |
| **chore:** | Other maintenance: dependencies, theme updates, removing unused files | `chore: update tabi theme` |

**Rules**:

- Article-only changes always use `content:`, even when fixing a mistake in an article (not `fix:`)
- When articles and other files change together, choose by the main purpose
- Add `!` for breaking changes (e.g. `refactor!:`)
- Write the subject in English, starting lowercase, with no trailing period
