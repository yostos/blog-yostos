#!/bin/bash
set -euo pipefail

# Generate cover image using OpenAI gpt-image-2.5 Flare API
# Requires: OPENAI_API_KEY, curl, jq, avifenc
# Note: gpt-image-2.5 can return png, jpeg or webp, but we deliberately
# keep the default PNG. It is the only lossless option among them, and
# feeding a lossless intermediate to avifenc avoids stacking a second
# generation of lossy artifacts on top of the AVIF encode.
#
# AVIF is used for photographic and AI-generated cover images only.
# Diagrams, charts and screenshots must stay lossless WebP:
#   cwebp -lossless -z 9 -exact input.png -o output.webp

SIZE="1536x864"
QUALITY="high"
MODEL="gpt-image-2.5-flare"
AVIF_QUALITY="60"

usage() {
  cat <<'USAGE'
Usage: generate-cover.sh -p <prompt> -o <output> [-s size] [-q quality] [-w avif_quality]

Options:
  -p  Image generation prompt (required)
  -o  Output file path, e.g. cover.avif (required)
  -s  Size: 1536x864, 2048x1152, 1024x1024, etc.
      Must be multiples of 16, aspect ratio within 3:1 to 1:3.
      (default: 1536x864 = 16:9)
  -q  Quality: low, medium, high, xhigh, or max (default: high)
      gpt-image-2.5 adds xhigh and max above high. They cost more per
      image, so covers stay at high unless asked otherwise.
  -w  AVIF encoder quality (0-100, default: 60)
      60 is roughly equivalent to the previous cwebp -q 80.

Examples:
  # 16:9 cover image (default)
  ./scripts/generate-cover.sh \
    -p "A futuristic cityscape" \
    -o content/blog/2026/05/my-article/cover.avif

  # Higher-quality AVIF encoding
  ./scripts/generate-cover.sh \
    -p "Abstract pattern" \
    -o output.avif -w 75
USAGE
  exit 1
}

while getopts "p:o:s:q:w:" opt; do
  case $opt in
    p) PROMPT="$OPTARG" ;;
    o) OUTPUT="$OPTARG" ;;
    s) SIZE="$OPTARG" ;;
    q) QUALITY="$OPTARG" ;;
    w) AVIF_QUALITY="$OPTARG" ;;
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
echo "  AVIF quality: $AVIF_QUALITY"
echo "  Prompt: ${PROMPT:0:80}..."

RESP_FILE=$(mktemp -t cover-resp-XXXXXX)
TMP_PNG=$(mktemp -t cover-XXXXXX).png
trap 'rm -f "$RESP_FILE" "$TMP_PNG"' EXIT

# Call the Image API directly. Flare renders a high-quality 1536x864 image
# in about 25 seconds, so a synchronous request is enough; no background job
# or host model is needed. --max-time leaves headroom for a congested server.
echo "Requesting image..."
HTTP_CODE=$(curl -s --max-time 180 -o "$RESP_FILE" -w '%{http_code}' \
  https://api.openai.com/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "$(jq -n \
    --arg model "$MODEL" \
    --arg prompt "$PROMPT" \
    --arg size "$SIZE" \
    --arg quality "$QUALITY" \
    '{model: $model, prompt: $prompt, size: $size, quality: $quality, n: 1}')") || {
  echo "Error: request failed or timed out"
  exit 1
}

if [ "$HTTP_CODE" != "200" ]; then
  echo "Error: HTTP $HTTP_CODE — $(jq -r '.error.message // "no detail"' "$RESP_FILE" 2>/dev/null)"
  exit 1
fi

B64=$(jq -r '.data[0].b64_json // empty' "$RESP_FILE")
if [ -z "$B64" ]; then
  echo "Error: no image in response"
  exit 1
fi

echo "Decoding base64 image..."
printf '%s' "$B64" | base64 -d > "$TMP_PNG"

echo "Converting to AVIF (quality=$AVIF_QUALITY)..."
avifenc -q "$AVIF_QUALITY" -y 420 -s 6 --ignore-exif --ignore-xmp \
  "$TMP_PNG" "$OUTPUT" > /dev/null

echo "Saved: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
