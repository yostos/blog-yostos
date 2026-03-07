---
description: Generate a cover image for an article using OpenAI DALL-E 3 API. Read article content, craft a prompt, generate 1792x1024 image, and convert to cover.webp.
---

# Article Cover Image Generation

Generate a cover image (cover.webp) for an article using OpenAI DALL-E 3 API.

## Steps

### 1. Identify Target Article

Ask the user which article to generate a cover image for.
Read the article content to understand the theme and key topics.

### 2. Craft Image Prompt

Based on the article content:

- Identify the core theme and visual concepts
- Craft a DALL-E 3 prompt that captures the article's essence
- Show the prompt to the user for approval before generating

### 3. Generate Image

Run `./scripts/generate-cover.sh`:

```
./scripts/generate-cover.sh \
  -p "<approved prompt>" \
  -o content/blog/YYYY/MM/slug/cover.jpg
```

### 4. Convert to WebP

Convert the generated JPG to WebP and remove the JPG:

```
cwebp -q 80 content/blog/YYYY/MM/slug/cover.jpg -o content/blog/YYYY/MM/slug/cover.webp
rm content/blog/YYYY/MM/slug/cover.jpg
```

### 5. Verify Frontmatter

Ensure the article frontmatter has:

```toml
[extra]
local_image = "cover.webp"
social_media_card = "ogp.webp"
```
