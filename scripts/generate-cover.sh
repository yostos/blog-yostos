#!/bin/bash
set -euo pipefail

# Generate cover image using OpenAI gpt-image-2 API
# Requires: OPENAI_API_KEY, curl, jq, cwebp
# Note: gpt-image-2's output_format=webp is currently not honored
# (returns PNG bytes despite metadata claiming webp). We request PNG
# and convert to WebP via cwebp.

SIZE="1536x864"
QUALITY="high"
MODEL="gpt-image-2"
WEBP_QUALITY="80"

usage() {
  cat <<'USAGE'
Usage: generate-cover.sh -p <prompt> -o <output> [-s size] [-q quality] [-w webp_quality]

Options:
  -p  Image generation prompt (required)
  -o  Output file path, e.g. cover.webp (required)
  -s  Size: 1536x864, 2048x1152, 1024x1024, etc.
      Must be multiples of 16, aspect ratio within 3:1 to 1:3.
      (default: 1536x864 = 16:9)
  -q  Quality: low, medium, or high (default: high)
  -w  WebP encoder quality (0-100, default: 80)

Examples:
  # 16:9 cover image (default)
  ./scripts/generate-cover.sh \
    -p "A futuristic cityscape" \
    -o content/blog/2026/05/my-article/cover.webp

  # Lower-compression WebP encoding
  ./scripts/generate-cover.sh \
    -p "Abstract pattern" \
    -o output.webp -w 60
USAGE
  exit 1
}

while getopts "p:o:s:q:w:" opt; do
  case $opt in
    p) PROMPT="$OPTARG" ;;
    o) OUTPUT="$OPTARG" ;;
    s) SIZE="$OPTARG" ;;
    q) QUALITY="$OPTARG" ;;
    w) WEBP_QUALITY="$OPTARG" ;;
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

echo "Generating image with $MODEL..."
echo "  Size: $SIZE"
echo "  Quality: $QUALITY"
echo "  WebP quality: $WEBP_QUALITY"
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

B64=$(echo "$RESPONSE" | jq -r '.data[0].b64_json // empty')

if [ -z "$B64" ]; then
  echo "Error: No image data in response"
  echo "$RESPONSE" | jq .
  exit 1
fi

TMP_PNG=$(mktemp -t cover-XXXXXX).png
trap 'rm -f "$TMP_PNG"' EXIT

echo "Decoding base64 image..."
echo "$B64" | base64 -d > "$TMP_PNG"

echo "Converting to WebP (quality=$WEBP_QUALITY)..."
cwebp -quiet -q "$WEBP_QUALITY" "$TMP_PNG" -o "$OUTPUT"

echo "Saved: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
