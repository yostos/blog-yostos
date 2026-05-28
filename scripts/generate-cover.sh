#!/bin/bash
set -euo pipefail

# Generate cover image using OpenAI gpt-image-2 API
# Requires: OPENAI_API_KEY, curl, jq, cwebp
# Note: gpt-image-2's output_format=webp is currently not honored
# (returns PNG bytes despite metadata claiming webp). We request PNG
# and convert to WebP via cwebp.

SIZE="1536x864"
QUALITY="high"
MODEL="gpt-image-2"        # image_generation tool model
HOST_MODEL="gpt-4.1-mini"  # host model that drives the image tool
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

RESP_FILE=$(mktemp -t cover-resp-XXXXXX)
TMP_PNG=$(mktemp -t cover-XXXXXX).png
trap 'rm -f "$RESP_FILE" "$TMP_PNG"' EXIT

# A high-quality gpt-image-2 render can take several minutes — longer than the
# ~60s idle timeout that closes a synchronous (or streamed) connection before
# the image is ready. Submit the job in background mode via the Responses API
# and poll for it, so every HTTP request is short-lived and never hits the
# timeout. The image_generation tool drives gpt-image-2; the host model just
# forwards the prompt verbatim.
echo "Submitting background job..."
SUBMIT=$(curl -s --max-time 60 https://api.openai.com/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "$(jq -n \
    --arg host "$HOST_MODEL" \
    --arg model "$MODEL" \
    --arg prompt "$PROMPT" \
    --arg size "$SIZE" \
    --arg quality "$QUALITY" \
    '{model: $host, background: true, store: true,
      instructions: "The user message is the exact image prompt. Call the image_generation tool once using that text verbatim as the prompt; do not paraphrase, summarize, translate, or add to it.",
      input: $prompt,
      tools: [{type: "image_generation", model: $model, size: $size, quality: $quality}],
      tool_choice: {type: "image_generation"}}')")

JOB_ID=$(echo "$SUBMIT" | jq -r '.id // empty')
if [ -z "$JOB_ID" ]; then
  echo "Error: $(echo "$SUBMIT" | jq -r '.error.message // "failed to submit job"')"
  exit 1
fi
echo "  Job: $JOB_ID"

echo "Polling for completion (high quality can take a few minutes)..."
STATUS=""
for _ in $(seq 1 120); do
  curl -s --max-time 30 "https://api.openai.com/v1/responses/$JOB_ID" \
    -H "Authorization: Bearer $OPENAI_API_KEY" > "$RESP_FILE"
  STATUS=$(jq -r '.status // "unknown"' "$RESP_FILE")
  case "$STATUS" in
    completed) break ;;
    failed|cancelled|incomplete)
      echo "Error: job $STATUS — $(jq -r '.error.message // .incomplete_details.reason // "no detail"' "$RESP_FILE")"
      exit 1 ;;
  esac
  sleep 5
done

if [ "$STATUS" != "completed" ]; then
  echo "Error: job did not complete (last status: $STATUS)"
  exit 1
fi

B64=$(jq -r '[.output[]? | select(.type=="image_generation_call") | .result][0] // empty' "$RESP_FILE")
if [ -z "$B64" ]; then
  echo "Error: no image in completed response"
  jq -r '.output[]? | select(.type=="message") | .content[]?.text // empty' "$RESP_FILE" | head -c 500
  echo
  exit 1
fi

echo "Decoding base64 image..."
printf '%s' "$B64" | base64 -d > "$TMP_PNG"

echo "Converting to WebP (quality=$WEBP_QUALITY)..."
cwebp -quiet -q "$WEBP_QUALITY" "$TMP_PNG" -o "$OUTPUT"

echo "Saved: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
