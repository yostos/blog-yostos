#!/bin/bash
# IndexNow: Notify Bing (and other search engines) of new/updated URLs
# Usage: ./scripts/indexnow.sh https://codedchords.dev/posts/my-article/
#        ./scripts/indexnow.sh --no-wait https://codedchords.dev/posts/my-article/

set -euo pipefail

HOST="codedchords.dev"
KEY="ceaaeaf047f940dcbed3b040f48f1a27"
KEY_LOCATION="https://${HOST}/${KEY}.txt"
POLL_INTERVAL=15
POLL_TIMEOUT=300

no_wait=false
urls=()

for arg in "$@"; do
  case "$arg" in
    --no-wait) no_wait=true ;;
    *) urls+=("$arg") ;;
  esac
done

if [ ${#urls[@]} -eq 0 ]; then
  echo "Usage: $0 [--no-wait] <url> [<url> ...]" >&2
  exit 1
fi

# Wait for URL to return 200
wait_for_url() {
  local url="$1"
  local elapsed=0

  echo "Waiting for ${url} to become available..."
  while [ "$elapsed" -lt "$POLL_TIMEOUT" ]; do
    status=$(curl -s -o /dev/null -w '%{http_code}' "$url") || true
    if [ "$status" = "200" ]; then
      echo "  -> OK (200)"
      return 0
    fi
    echo "  -> ${status} (retrying in ${POLL_INTERVAL}s, ${elapsed}/${POLL_TIMEOUT}s)"
    sleep "$POLL_INTERVAL"
    elapsed=$((elapsed + POLL_INTERVAL))
  done

  echo "  -> Timed out after ${POLL_TIMEOUT}s" >&2
  return 1
}

# Poll each URL before submitting
if [ "$no_wait" = false ]; then
  echo "Waiting 180s for GitHub Actions deploy to complete..."
  sleep 180
  for url in "${urls[@]}"; do
    wait_for_url "$url"
  done
fi

# Build JSON urlList
url_json=$(printf '%s\n' "${urls[@]}" | jq -R . | jq -s .)

payload=$(jq -n \
  --arg host "$HOST" \
  --arg key "$KEY" \
  --arg keyLocation "$KEY_LOCATION" \
  --argjson urlList "$url_json" \
  '{host: $host, key: $key, keyLocation: $keyLocation, urlList: $urlList}')

echo "Submitting to IndexNow:"
echo "$payload" | jq .

response=$(curl -s -w '\n%{http_code}' -X POST "https://api.indexnow.org/IndexNow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$payload")

http_code=$(echo "$response" | tail -1)
body=$(echo "$response" | sed '$d')

echo "Response: HTTP ${http_code}"
[ -n "$body" ] && echo "$body"

case "$http_code" in
  200) echo "OK: URL submitted and indexed." ;;
  202) echo "Accepted: URL received, will be processed later." ;;
  400) echo "Error: Bad request." >&2; exit 1 ;;
  403) echo "Error: Key not valid." >&2; exit 1 ;;
  422) echo "Error: Invalid URL." >&2; exit 1 ;;
  429) echo "Error: Too many requests." >&2; exit 1 ;;
  *)   echo "Unexpected response." >&2; exit 1 ;;
esac
