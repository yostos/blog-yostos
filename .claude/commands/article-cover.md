---
description: Generate a cover image for an article using OpenAI gpt-image-2 API. Read article content, craft a prompt, generate 1536x864 (16:9) AVIF image.
---

# Article Cover Image Generation

Generate a cover image (cover.avif) for an article using OpenAI gpt-image-2 API.

## Steps

### 1. Identify Target Article

Ask the user which article to generate a cover image for.
Read the article content to understand the theme and key topics.

### 2. Craft Image Prompt

Based on the article content:

- Identify the core theme and visual concepts
- Craft a gpt-image-2 prompt that captures the article's essence
- Show the prompt to the user for approval before generating

### 3. Generate Image

Run `./scripts/generate-cover.sh`:

```
./scripts/generate-cover.sh \
  -p "<approved prompt>" \
  -o content/blog/YYYY/MM/slug/cover.avif
```

The script defaults to 1536x864 (16:9), high quality, and AVIF output.

### 4. Verify Frontmatter

Ensure the article frontmatter has:

```toml
[extra]
local_image = "cover.avif"
social_media_card = "ogp.webp"
```
