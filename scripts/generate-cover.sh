#!/bin/bash
set -euo pipefail

# Generate cover image using OpenAI gpt-image-1-mini API
# Requires: OPENAI_API_KEY, curl, jq

SIZE="1536x1024"
QUALITY="high"
MODEL="gpt-image-1-mini"

usage() {
  cat <<'USAGE'
Usage: generate-cover.sh -p <prompt> -o <output> [-s size] [-q quality]

Options:
  -p  Image generation prompt (required)
  -o  Output file path, e.g. cover.jpg (required)
  -s  Size: 1536x1024, 1024x1536, 1024x1024
      (default: 1536x1024 = 3:2)
  -q  Quality: low, medium, or high (default: high)

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

echo "Generating image with gpt-image-1-mini..."
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

# gpt-image-1-mini returns b64_json; fall back to URL for other models
B64=$(echo "$RESPONSE" | jq -r '.data[0].b64_json // empty')
URL=$(echo "$RESPONSE" | jq -r '.data[0].url // empty')

if [ -n "$B64" ]; then
  echo "Decoding base64 image..."
  echo "$B64" | base64 -d > "$OUTPUT"
elif [ -n "$URL" ]; then
  echo "Downloading image..."
  curl -s "$URL" -o "$OUTPUT"
else
  echo "Error: No image data in response"
  echo "$RESPONSE" | jq .
  exit 1
fi

echo "Saved: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
