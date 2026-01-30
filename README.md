# Coded Chords

[![Deploy to GitHub Pages](https://github.com/yostos/blog-yostos/actions/workflows/deploy.yml/badge.svg)](https://github.com/yostos/blog-yostos/actions/workflows/deploy.yml)
[![Textlint](https://github.com/yostos/blog-yostos/actions/workflows/textlint.yml/badge.svg)](https://github.com/yostos/blog-yostos/actions/workflows/textlint.yml)
[![Zola](https://img.shields.io/badge/Zola-0.19.2-blue?logo=zola)](https://www.getzola.org/)
[![Theme: tabi](https://img.shields.io/badge/Theme-tabi-orange)](https://github.com/welpo/tabi)
[![Articles](https://img.shields.io/badge/Articles-226+-green)](https://blog.yostos.org)

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

The blog has been running since 2024, with **226+ articles** covering these topics.

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

## Development

```bash
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

## Project Structure

```
content/
  blog/
    YYYY/MM/slug/     # Blog articles (year/month/slug format)
      index.md        # Article content (TOML frontmatter)
      *.webp          # Article images
themes/tabi/          # tabi theme (git submodule)
config.toml           # Zola configuration
CLAUDE.md             # Claude Code guidance
```

## Author

**Toshiyuki Yoshida** ([@yostos](https://github.com/yostos))

- Based in Japan
- IT professional with interests in cloud, security, and generative AI
- Amateur guitarist who enjoys fusion and instrumental music

## License

Blog content is copyrighted by the author. The [tabi theme](https://github.com/welpo/tabi) is licensed under MIT.
