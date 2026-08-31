---
description: Assign tags to an article. Pick five keywords from the article, embed them with Voyage AI, match against tag-vectors.json, and set the layer-1 and layer-2 tags in frontmatter.
---

# Article Tag Assignment

Determine the tags for an article and write them into its frontmatter.

The tag system is documented in `docs/tag-rule.md`.
Every article carries exactly one layer-1 tag and one layer-2 tag,
with the layer-1 tag first and matching the layer-2 tag's parent.

`data/tag-vectors.json` holds the embedding of each layer-2 **tag name**,
not a centroid of its articles. Matching therefore relies on the general
language knowledge the embedding model learned during pretraining, not on
how this blog has used the tag before. See ADR-0006 in
`docs/architectural-decision.md`.

## Steps

### 1. Identify Target Article

Ask the user which article to tag, unless a path was given as an argument.

### 2. Pick Five Keywords

Read the article and choose five English keywords that describe what it is about.

- **Do not look at the tag list first.** Choose the words that describe the
  article, then let the vectors decide which tag is closest. Steering the
  words toward an existing tag name defeats the measurement
- Nouns or noun phrases only. No verbs, no adjectives
- Name the subject, not the form. `design pattern` and `paradigm`, not
  `lesson` or `advice`
- Replace product, company, person, and work names with common nouns.
  Write `trackball` and `peripheral`, not `MX ERGO S`
- Cover what the article is actually about, including its stance. An article
  about playing a song and an article about buying a pedal are both about
  guitars, but the first is `cover song recording arrangement` and the
  second is `pedal circuit purchase tone`

### 3. Assign

Run:

```bash
python3 scripts/assign-tags.py <path to index.md> <five keywords>
```

For example:

```bash
python3 scripts/assign-tags.py content/blog/2026/07/example/index.md \
  pedal distortion circuit overdrive guitar
```

Quote any keyword that contains a space (`"command line"`).

The script joins the five words with spaces, embeds the result as a single
string with Voyage AI (`voyage-4`, 1024 dimensions), takes the cosine
similarity against every layer-2 tag, and writes the top match plus its
parent into the frontmatter.

Add `--dry-run` to see the ranking without modifying the file.

The script stops with an error if `VOYAGE_API_KEY` is unset, or if
`tag-vectors.json` was built with a different model, dimension, or vector
source. In those cases, run `python3 scripts/build-tag-vectors.py` first.

### 4. Report

Show the user:

- The five keywords that were used
- The tags that were set
- The top 3 candidates with their similarity scores
- The previous tags, if the article already had some

Do not argue for the result or ask the user to approve it.
The tags are set; whether to keep or change them is the author's call.

## Notes

- Measured accuracy is 71-76% for the top layer-2 match, 88-93% within the
  top 3, and 89-92% for the layer-1 tag. Over half of the misses are
  mix-ups within the same layer-1 tag, so the layer-1 tag still lands
- A low top score across all tags suggests the article needs a tag that
  does not exist yet
- Adding or renaming a tag means editing `data/tagset.toml` by hand, then
  re-running `scripts/build-tag-vectors.py`. Article content never triggers
  a rebuild. Check the pairwise similarities afterwards: the naming rules
  in `docs/tag-rule.md` require every pair to stay below 0.85
