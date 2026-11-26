---
description: Publish an article. Run review, regenerate OGP, check links, commit on a branch, open a PR, wait for checks, and squash-merge it.
---

# Article Publish

Execute the full publish workflow automatically.
Prerequisite: the user has already confirmed the article via `zola serve` preview.

`main` is protected: publishing means squash-merging a pull request.
See `docs/repository-workflow.md` for the rules.

## Steps

Execute in order. Stop and report if any step fails.

### 0. Check the Branch

- Run `git branch --show-current`
- If on `main`: create a branch with `git switch -c content/<slug>`
  (`<slug>` is the article directory name)
- If already on a branch (including a draft branch created by automation): stay on it

### 1. Run /article-review

Execute the full article quality review.
If issues are found, stop and fix them before continuing.

### 2. Regenerate OGP Image

- Move the existing OGP image to the Trash, only if it exists. A new article has no
  `ogp.webp` yet, and `trash` fails on a missing file, which would stop this procedure.
  Write out the single target file in full (the file specified by social_media_card in
  frontmatter), in both places. Never pass a wildcard or a directory, and never regenerate
  by deleting more than the one article's image:

```bash
test -f content/blog/YYYY/MM/slug/ogp.webp && trash content/blog/YYYY/MM/slug/ogp.webp
```

- Do NOT use `rm`. `trash` is reversible, so a mistaken target can be recovered
- Run `npm run ogp` to regenerate

### 3. Link Check

Check only the target article's links with `lychee` (do NOT run site-wide `zola check`, it scans ~350 articles and is too slow):

```bash
lychee -s https -s http -u "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36" content/blog/YYYY/MM/slug/index.md
```

- `-s https -s http` restricts checking to external URLs and skips Zola's internal `@/...` link syntax (lychee misinterprets these as local file paths and reports false-positive errors)
- `-u` sends a browser User-Agent. The default (`lychee/x.y.z`) is rejected as a bot by several sites, producing 403 false positives
- Verify internal `@/...` references separately by confirming the target file exists, e.g. `test -f content/blog/YYYY/MM/other-slug/index.md`
- Fix any real errors before continuing

### 4. Stage & Commit

- `git add .` to stage all changes
- Use `/simple-commit:commit` skill to create the commit

### 5. Open a PR and Merge

- `git push -u origin <branch>`
- If the branch has no PR yet, create one with `gh pr create`
  - Title: follow the "PR のタイトル" section of `docs/repository-workflow.md`
    (article changes use `content:`, e.g. `content: add <topic> article`)
  - The title becomes the commit title on `main`
- Wait for the required checks: `gh pr checks --watch`
  - If `textlint` or `ogp-check` fails, fix the errors, commit, push, and wait again
- Merge and clean up. Goal: once the merge succeeds, the local repo is on an up-to-date
  `main` and the merged branch is gone
  1. `gh pr merge --squash --delete-branch`. If the merge fails, stop here and report
     the cause; do not delete the branch. On success, gh switches to `main` and deletes
     the local branch (GitHub deletes the remote branch)
  2. `git switch main` (no-op if gh already switched)
  3. `git pull origin main`
  4. If the local branch still exists, confirm the PR state is `MERGED` with
     `gh pr view <number> --json state`, then delete it with `git branch -D <branch>`

Merging updates `main`, and the deploy workflow deploys to Cloudflare Workers.

### 6. IndexNow Notification

Notify search engines of the new/updated article URL via IndexNow.

- Determine the article URL by converting the content path directly:
  - `content/blog/YYYY/MM/slug/index.md` → `https://codedchords.dev/blog/YYYY/MM/slug/`
  - Example: `content/blog/2026/03/cloudflare-free-security/index.md` → `https://codedchords.dev/blog/2026/03/cloudflare-free-security/`
  - IMPORTANT: The date path (YYYY/MM) must be included. Do NOT omit it.
- Run `./scripts/indexnow.sh <article-url>`
- The script will wait for the URL to return HTTP 200 (deploy completion) before submitting
- Report the IndexNow result to the user
