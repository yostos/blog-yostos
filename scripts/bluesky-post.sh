#!/bin/bash
# Post a new blog article to Bluesky
# Usage: BLUESKY_IDENTIFIER=... BLUESKY_APP_PASSWORD=... ./scripts/bluesky-post.sh content/blog/my-article/index.md

set -euo pipefail

SITE_URL="https://codedchords.dev"
BSKY_API="https://bsky.social/xrpc"
MAX_TAGS=5

article_path="$1"

if [ ! -f "$article_path" ]; then
  echo "Error: File not found: $article_path" >&2
  exit 1
fi

if [ -z "${BLUESKY_IDENTIFIER:-}" ] || [ -z "${BLUESKY_APP_PASSWORD:-}" ]; then
  echo "Error: BLUESKY_IDENTIFIER and BLUESKY_APP_PASSWORD must be set" >&2
  exit 1
fi

# --- Extract frontmatter fields ---

# Extract TOML frontmatter between +++ markers
frontmatter=$(sed -n '/^+++$/,/^+++$/p' "$article_path" | sed '1d;$d')

# Extract title
title=$(echo "$frontmatter" | grep '^title' | head -1 | sed 's/^title *= *"\(.*\)"/\1/')
if [ -z "$title" ]; then
  echo "Error: Could not extract title from $article_path" >&2
  exit 1
fi

# Extract description (handle multi-line """ strings)
if echo "$frontmatter" | grep -q 'description *= *"""'; then
  description=$(echo "$frontmatter" | sed -n '/description *= *"""/,/"""/p' | sed '1s/description *= *"""//' | sed '$s/"""//' | tr '\n' ' ' | sed 's/  */ /g;s/^ *//;s/ *$//')
else
  description=$(echo "$frontmatter" | grep '^description' | head -1 | sed 's/^description *= *"\(.*\)"/\1/')
fi
if [ -z "$description" ]; then
  echo "Error: Could not extract description from $article_path" >&2
  exit 1
fi

# Extract tags
tags=$(echo "$frontmatter" | grep '^tags' | head -1 | sed 's/^tags *= *\[//;s/\]$//' | tr ',' '\n' | sed 's/^ *"//;s/" *$//' | head -n "$MAX_TAGS")

# --- Build article URL ---

# content/blog/my-article/index.md -> blog/my-article/
relative_path=$(echo "$article_path" | sed 's|^content/||;s|/index\.md$|/|')
article_url="${SITE_URL}/${relative_path}"

echo "Title: $title"
echo "Description: $description"
echo "URL: $article_url"
echo "Tags: $tags"

# --- Build post text ---

post_text="📝 Just published:

#blog"

# Add hashtags from tags
while IFS= read -r tag; do
  [ -z "$tag" ] && continue
  # Skip tags containing spaces
  if echo "$tag" | grep -q ' '; then
    continue
  fi
  post_text="${post_text} #${tag}"
done <<< "$tags"

echo "Post text: $post_text"

# --- Build facets (hashtag annotations) ---

# Calculate byte positions for hashtags and build facets JSON
build_facets() {
  local text="$1"
  local facets="[]"

  # Find all #hashtag occurrences
  while IFS= read -r match; do
    [ -z "$match" ] && continue
    local hashtag
    hashtag=$(echo "$match" | awk '{print $1}')
    local tag_value="${hashtag#\#}"

    # Calculate UTF-8 byte start position
    local prefix="${text%%${hashtag}*}"
    local byte_start
    byte_start=$(printf '%s' "$prefix" | wc -c | tr -d ' ')
    local byte_end
    byte_end=$(( byte_start + $(printf '%s' "$hashtag" | wc -c | tr -d ' ') ))

    facets=$(echo "$facets" | jq \
      --argjson bs "$byte_start" \
      --argjson be "$byte_end" \
      --arg tag "$tag_value" \
      '. + [{
        "index": { "byteStart": $bs, "byteEnd": $be },
        "features": [{ "$type": "app.bsky.richtext.facet#tag", "tag": $tag }]
      }]')
  done < <(grep -oE '#[^ ]+' <<< "$text")

  echo "$facets"
}

facets=$(build_facets "$post_text")
echo "Facets: $facets"

# --- Authenticate with Bluesky ---

echo "Authenticating with Bluesky..."
auth_response=$(curl -s -X POST "${BSKY_API}/com.atproto.server.createSession" \
  -H "Content-Type: application/json" \
  -d "{\"identifier\": \"${BLUESKY_IDENTIFIER}\", \"password\": \"${BLUESKY_APP_PASSWORD}\"}")

access_jwt=$(echo "$auth_response" | jq -r '.accessJwt // empty')
did=$(echo "$auth_response" | jq -r '.did // empty')

if [ -z "$access_jwt" ] || [ -z "$did" ]; then
  echo "Error: Authentication failed" >&2
  echo "$auth_response" | jq . >&2
  exit 1
fi

echo "Authenticated as: $did"

# --- Create post ---

now=$(date -u +"%Y-%m-%dT%H:%M:%S.000Z")

record=$(jq -n \
  --arg did "$did" \
  --arg text "$post_text" \
  --arg now "$now" \
  --argjson facets "$facets" \
  --arg uri "$article_url" \
  --arg etitle "$title" \
  --arg edesc "$description" \
  '{
    "repo": $did,
    "collection": "app.bsky.feed.post",
    "record": {
      "$type": "app.bsky.feed.post",
      "text": $text,
      "createdAt": $now,
      "facets": $facets,
      "embed": {
        "$type": "app.bsky.embed.external",
        "external": {
          "uri": $uri,
          "title": $etitle,
          "description": $edesc
        }
      }
    }
  }')

echo "Creating post..."
post_response=$(curl -s -w '\n%{http_code}' -X POST "${BSKY_API}/com.atproto.repo.createRecord" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${access_jwt}" \
  -d "$record")

http_code=$(echo "$post_response" | tail -1)
body=$(echo "$post_response" | sed '$d')

if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 300 ]; then
  echo "Successfully posted to Bluesky!"
  echo "$body" | jq .
else
  echo "Error: Failed to post (HTTP ${http_code})" >&2
  echo "$body" | jq . >&2
  exit 1
fi
