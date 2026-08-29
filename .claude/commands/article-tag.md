---
description: Assign tags to an article. Embed the article with Voyage AI, match against tag-vectors.json, and set the layer-1 and layer-2 tags in frontmatter.
---

# Article Tag Assignment

Determine the tags for an article and write them into its frontmatter.

The tag system is documented in `docs/tag-rule.md`.
Every article carries exactly one layer-1 tag and one layer-2 tag,
with the layer-1 tag first and matching the layer-2 tag's parent.

## Steps

### 1. Identify Target Article

Ask the user which article to tag, unless a path was given as an argument.

### 2. Assign

Run:

```bash
python3 scripts/assign-tags.py <path to index.md>
```

The script embeds the article with Voyage AI (`voyage-4`, 1024 dimensions),
takes the cosine similarity against every layer-2 tag in `data/tag-vectors.json`,
and writes the top match plus its parent into the frontmatter.

Add `--dry-run` to see the ranking without modifying the file.

The script stops with an error if `VOYAGE_API_KEY` is unset, or if
`tag-vectors.json` was built with a different model or dimension.
In the latter case, run `python3 scripts/build-tag-vectors.py` first.

### 3. Report

Show the user:

- The tags that were set
- The top 3 candidates with their similarity scores
- The previous tags, if the article already had some

Do not argue for the result or ask the user to approve it.
The tags are set; whether to keep or change them is the author's call.

## Notes

- Roughly 75% of articles get the correct tag as the top match, and 89%
  have it within the top 3. A low top score across all tags suggests the
  article needs a tag that does not exist yet
- Adding a tag means editing `data/tagset.toml` by hand, then re-running
  `scripts/build-tag-vectors.py`
- A newly written article is not yet in `tag-vectors.json`. That is fine
  and matches the conditions the accuracy was measured under
