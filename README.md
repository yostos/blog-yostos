# Coded Chords

[![Deploy to GitHub Pages](https://github.com/yostos/blog-yostos/actions/workflows/deploy.yml/badge.svg)](https://github.com/yostos/blog-yostos/actions/workflows/deploy.yml)
[![Textlint](https://github.com/yostos/blog-yostos/actions/workflows/textlint.yml/badge.svg)](https://github.com/yostos/blog-yostos/actions/workflows/textlint.yml)
[![Zola](https://img.shields.io/badge/Zola-0.22.1-blue?logo=zola)](https://www.getzola.org/)
[![Theme: tabi](https://img.shields.io/badge/Theme-tabi-orange)](https://github.com/welpo/tabi)
[![Articles](https://img.shields.io/badge/Articles-237+-green)](https://blog.yostos.org)

**Live Site**: [https://blog.yostos.org](https://blog.yostos.org)

## About This Blog

**Coded Chords** is a personal blog by Toshiyuki Yoshida — the name reflects the intersection of two passions: **code** (technology) and **chords** (music, especially guitar).

This blog covers a diverse range of topics:

- **Technology** — Generative AI (Claude, LLMs), software development, security, cloud (AWS), CLI tools
- **Music & Guitar** — Guitar gear reviews, playing techniques, effects pedals, music production
- **Current Affairs** — Commentary on news and events, particularly in Japan and Korea
- **Drone** — FPV flying, aerial photography
- **Gaming** — Splatoon series
- **Travel & Photography** — Trip reports, scenic photography
- **Books & Manga** — Reviews and recommendations
- **Life & Career** — Personal reflections

The blog has been running since 2024, with **237+ articles** covering these topics.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Static Site Generator | [Zola](https://www.getzola.org/) |
| Theme | [tabi](https://github.com/welpo/tabi) |
| Hosting | GitHub Pages |
| Comments | [giscus](https://giscus.app/) |
| CI/CD | GitHub Actions |
| Linting | [textlint](https://textlint.github.io/) |
| Git Hooks | [Husky](https://typicode.github.io/husky/) + [lint-staged](https://github.com/lint-staged/lint-staged) |

## CI/CD Pipeline

This project has a 3-stage quality gate for content:

```
[Local Development]
     │
     ├─ git commit → pre-commit (OGP check + lint-staged)
     │
     └─ git push   → pre-push (npm run lint: all files)
            │
            ▼
[GitHub Actions]
     │
     ├─ textlint.yml ──────────── Text quality check
     │
     ├─ deploy.yml ────────────── zola build (internal link validation)
     │
     └─ zola-check-scheduled.yml ─ Monthly external link check
```

### Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **Textlint** | Push/PR to main | Lint all Markdown files |
| **Deploy** | Push to main | Build and deploy to GitHub Pages |
| **Zola Check** | Monthly (15th) / Manual | Validate external links |

### Local Hooks (Husky)

| Hook | Command | Scope |
|------|---------|-------|
| **pre-commit** | OGP check + `npx lint-staged` | Staged article files |
| **pre-push** | `npm run lint` | All `content/**/*.md` |

To bypass hooks in emergencies (not recommended):

```bash
git commit --no-verify  # Skip pre-commit
git push --no-verify    # Skip pre-push
```

## Development

### Prerequisites

- [Zola](https://www.getzola.org/) 0.22.1+
- [Node.js](https://nodejs.org/) 20+

```bash
# Install dependencies
npm install

# Start dev server with live reload
zola serve

# Build for production (outputs to public/)
zola build

# Check for errors
zola check

# Run textlint
npm run lint

# Fix textlint errors automatically
npm run lint:fix
```

## OGP Image Generation

Each article has an auto-generated OGP image (`ogp.webp`) for social media sharing.

**How it works**:
- If an article has an image ≥1200×630px, it's used as the background
- Otherwise, the default background (`static/images/coded-chords.webp`) is used
- Title, blog name, and author are overlaid on all images

**Usage**:

```bash
# Generate OGP images for new articles (skips existing)
npm run ogp

# Preview what would be generated (dry-run)
npm run ogp:dry-run

# Regenerate all OGP images (force overwrite)
npm run ogp -- --force
```

**Font Setup** (required for first run):

Place a Japanese font (`.ttf` or `.otf`) in `scripts/fonts/`.
This directory is gitignored to allow use of licensed fonts.

## Project Structure

```
content/
  blog/
    YYYY/MM/slug/     # Blog articles (year/month/slug format)
      index.md        # Article content (TOML frontmatter)
      ogp.webp        # OGP image (auto-generated)
      *.webp          # Article images
templates/            # Custom templates and shortcodes
static/               # Static assets (CSS, images, favicon)
themes/tabi/          # tabi theme (git submodule)
scripts/
  generate-ogp.mjs    # OGP image generator
  fonts/              # Japanese fonts (gitignored)
config.toml           # Zola configuration
CLAUDE.md             # Claude Code AI assistant configuration
```

## Author

**Toshiyuki Yoshida** ([@yostos](https://github.com/yostos))

- Based in Japan
- IT professional with interests in cloud, security, and generative AI
- Amateur guitarist who enjoys fusion and instrumental music

## License

- **Blog content** (`content/`) — [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- **Everything else** — [MIT](./LICENSE)
