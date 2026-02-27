#!/bin/bash
set -euo pipefail

# Generate cover image using OpenAI DALL-E 3 API
# Requires: OPENAI_API_KEY, curl, jq

SIZE="1792x1024"
QUALITY="hd"
MODEL="dall-e-3"

usage() {
  cat <<'USAGE'
Usage: generate-cover.sh -p <prompt> -o <output> [-s size] [-q quality]

Options:
  -p  Image generation prompt (required)
  -o  Output file path, e.g. cover.jpg (required)
  -s  Size: 1792x1024, 1024x1792, 1024x1024
      (default: 1792x1024 = 16:9)
  -q  Quality: standard or hd (default: hd)

Examples:
  # 16:9 cover image
  ./scripts/generate-cover.sh \
    -p "A futuristic cityscape" \
    -o content/blog/2026/02/my-article/cover.jpg

  # Square image
  ./scripts/generate-cover.sh \
    -p "Abstract pattern" \
    -o output.jpg -s 1024x1024
USAGE
  exit 1
}

while getopts "p:o:s:q:" opt; do
  case $opt in
    p) PROMPT="$OPTARG" ;;
    o) OUTPUT="$OPTARG" ;;
    s) SIZE="$OPTARG" ;;
    q) QUALITY="$OPTARG" ;;
    *) usage ;;
  esac
done

if [ -z "${PROMPT:-}" ] || [ -z "${OUTPUT:-}" ]; then
  usage
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "Error: OPENAI_API_KEY is not set"
  exit 1
fi

echo "Generating image with DALL-E 3..."
echo "  Size: $SIZE"
echo "  Quality: $QUALITY"
echo "  Prompt: ${PROMPT:0:80}..."

RESPONSE=$(curl -s \
  https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "$(jq -n \
    --arg model "$MODEL" \
    --arg prompt "$PROMPT" \
    --arg size "$SIZE" \
    --arg quality "$QUALITY" \
    '{model: $model, prompt: $prompt, n: 1,
      size: $size, quality: $quality}')")

ERROR=$(echo "$RESPONSE" | jq -r '.error.message // empty')
if [ -n "$ERROR" ]; then
  echo "Error: $ERROR"
  exit 1
fi

URL=$(echo "$RESPONSE" | jq -r '.data[0].url')
if [ -z "$URL" ] || [ "$URL" = "null" ]; then
  echo "Error: No image URL in response"
  echo "$RESPONSE" | jq .
  exit 1
fi

echo "Downloading image..."
curl -s "$URL" -o "$OUTPUT"
echo "Saved: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
