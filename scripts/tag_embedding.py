"""記事とタグのベクター算出で共有する処理。

build-tag-vectors.py と assign-tags.py の双方が使う。埋め込み対象テキストの
作り方は両者で完全に一致していなければ、記事とタグの比較が成立しない。

選定理由と API の詳細は docs/architectural-decision.md の ADR-0004 を参照。
"""

import json
import math
import os
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAGSET = os.path.join(ROOT, "data", "tagset.toml")
VECTORS = os.path.join(ROOT, "data", "tag-vectors.json")
CONTENT = os.path.join(ROOT, "content")

MODEL = "voyage-4"
DIM = 1024
INPUT_TYPE = "document"
ENDPOINT = "https://api.voyageai.com/v1/embeddings"
BATCH_SIZE = 48
WORKERS = 3

FRONTMATTER = re.compile(r"\+\+\+\n(.*?)\n\+\+\+\n(.*)", re.S)


def split_frontmatter(text):
    """記事を (frontmatter, 本文) に分ける。形式が違えば None を返す。"""
    m = FRONTMATTER.match(text)
    return (m.group(1), m.group(2)) if m else None


def strip_markup(body):
    """HTML タグとショートコードを除去する。

    Markdown 記法とコードブロックは残す。記法記号は意味を変えず、
    コードは技術記事の主題を直接示すため。
    """
    body = re.sub(r"\{\{.*?\}\}|\{%.*?%\}", "", body, flags=re.S)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"<[^>]+>", "", body)
    return re.sub(r"\s+", " ", body).strip()


def field(front, name):
    m = re.search(rf'^{name}\s*=\s*"(.*?)"', front, re.M)
    return m.group(1) if m else ""


def tags_of(front):
    m = re.search(r"^tags\s*=\s*\[(.*?)\]", front, re.M | re.S)
    return re.findall(r'"([^"]*)"', m.group(1)) if m else []


def embed_text(front, body):
    """埋め込みに渡すテキストを組み立てる。title + description + 本文全文。"""
    return f'{field(front, "title")}。{field(front, "description")} {strip_markup(body)}'


def normalize(vector):
    length = math.sqrt(sum(x * x for x in vector))
    return [x / length for x in vector] if length else vector


def centroid(vectors):
    """平均して L2 再正規化する。正規化を省くと記事数の多いタグが有利になる。"""
    total = [sum(axis) for axis in zip(*vectors)]
    return normalize([x / len(vectors) for x in total])


def api_key():
    key = os.environ.get("VOYAGE_API_KEY")
    if not key:
        raise SystemExit("Error: VOYAGE_API_KEY is not set")
    return key


def embed(texts, key):
    """Voyage AI で埋め込み、(L2正規化したベクター, 消費トークン) を返す。"""
    def one(start):
        payload = {
            "input": texts[start:start + BATCH_SIZE],
            "model": MODEL,
            "input_type": INPUT_TYPE,
            "output_dimension": DIM,
            "truncation": True,
        }
        for attempt in range(6):
            req = urllib.request.Request(
                ENDPOINT,
                data=json.dumps(payload).encode(),
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json",
                },
            )
            try:
                res = json.load(urllib.request.urlopen(req, timeout=240))
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 5:
                    time.sleep(2 ** attempt)
                    continue
                raise
            return ([d["embedding"] for d in res["data"]],
                    res.get("usage", {}).get("total_tokens", 0))

    starts = list(range(0, len(texts), BATCH_SIZE))
    with ThreadPoolExecutor(WORKERS) as pool:
        results = list(pool.map(one, starts))
    return ([normalize(v) for chunk, _ in results for v in chunk],
            sum(tokens for _, tokens in results))


def load_vectors():
    """tag-vectors.json を読み、モデルと次元の一致を確認する。"""
    if not os.path.exists(VECTORS):
        raise SystemExit(
            f"Error: {os.path.relpath(VECTORS, ROOT)} がありません。"
            " scripts/build-tag-vectors.py を実行してください")
    data = json.load(open(VECTORS, encoding="utf-8"))
    if data.get("model") != MODEL or data.get("dim") != DIM:
        raise SystemExit(
            f"Error: tag-vectors.json は {data.get('model')} / {data.get('dim')}次元 で"
            f" 算出されていますが、現在の設定は {MODEL} / {DIM}次元 です。"
            " scripts/build-tag-vectors.py で再算出してください")
    return data
