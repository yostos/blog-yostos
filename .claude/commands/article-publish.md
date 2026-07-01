---
description: Publish an article. Run review, regenerate OGP, verify build, commit, and push to main automatically.
---

# Article Publish

Execute the full publish workflow automatically.
Prerequisite: the user has already confirmed the article via `zola serve` preview.

## Steps

Execute in order. Stop and report if any step fails.

### 1. Run /article-review

Execute the full article quality review.
If issues are found, stop and fix them before continuing.

### 2. Regenerate OGP Image

- Delete the existing OGP image (the file specified by social_media_card in frontmatter)
- Run `npm run ogp` to regenerate

### 3. Link Check

Check only the target article's links with `lychee` (do NOT run site-wide `zola check`, it scans ~350 articles and is too slow):

```bash
lychee -s https -s http content/blog/YYYY/MM/slug/index.md
```

- `-s https -s http` restricts checking to external URLs and skips Zola's internal `@/...` link syntax (lychee misinterprets these as local file paths and reports false-positive errors)
- Verify internal `@/...` references separately by confirming the target file exists, e.g. `test -f content/blog/YYYY/MM/other-slug/index.md`
- Fix any real errors before continuing

### 4. Stage & Commit

- `git add .` to stage all changes
- Use `/simple-commit:commit` skill to create the commit
  - lint-staged runs textlint automatically on commit
  - If textlint fails, fix the errors and retry

### 5. Push

Run `git push origin main` to publish.
GitHub Actions deploy workflow will auto-trigger and deploy to Cloudflare Workers.

### 6. IndexNow Notification

Notify search engines of the new/updated article URL via IndexNow.

- Determine the article URL by converting the content path directly:
  - `content/blog/YYYY/MM/slug/index.md` → `https://codedchords.dev/blog/YYYY/MM/slug/`
  - Example: `content/blog/2026/03/cloudflare-free-security/index.md` → `https://codedchords.dev/blog/2026/03/cloudflare-free-security/`
  - IMPORTANT: The date path (YYYY/MM) must be included. Do NOT omit it.
- Run `./scripts/indexnow.sh <article-url>`
- The script will wait for the URL to return HTTP 200 (deploy completion) before submitting
- Report the IndexNow result to the user
