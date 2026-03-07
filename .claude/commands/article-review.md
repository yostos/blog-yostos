---
description: Run article quality review. Check frontmatter, shortcode conventions, writing style, and assets.
---

# Article Quality Review

Ask the user which article to review, then execute the following checks in order.

## 1. Frontmatter Validation

Read the article frontmatter and verify:

- Required fields exist: title, description, date, tags, social_media_card
- description rules:
  - Ends with a complete sentence (no noun-ending or particle-ending)
  - Ends with Japanese period "。"
  - Within 200 characters
- date format is valid (YYYY-MM-DD)

## 2. Shortcode Conventions

Check the article body:

- No Markdown image syntax `![alt](path)` is used
  - If found, propose replacement with image shortcode wrapped in textlint-disable/enable
- Body shortcodes (`{% %} ... {% end %}`) are wrapped in
  `<!-- textlint-disable -->` / `<!-- textlint-enable -->`
- Inline shortcodes (`{{ }}`) are also wrapped

## 3. Writing Style

Check the article body:

- Consistent use of desu/masu style (敬体)
- No sentences ending with "："
- No level-3 headings (`###`) used
- No bold text (`**text**`) as standalone lines (heading substitute)
- No excessive section splitting (headings on 1-2 paragraph content)

## 4. Asset Verification

- OGP image file (social_media_card) exists
- Cover image file (local_image) exists if specified

## Report

After all checks, summarize results:

- No issues: report "Review complete, no issues found"
- Issues found: list all problems and propose fixes
