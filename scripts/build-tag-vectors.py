#!/usr/bin/env python3
"""data/tag-vectors.json を算出する。

第2層タグごとに、そのタグを持つ全記事のベクターを平均し、L2再正規化した値を
書き出す。埋め込みは Voyage AI の voyage-4 を使う。選定理由と呼び出し方は
docs/architectural-decision.md の ADR-0004 を参照。

Requires: VOYAGE_API_KEY
"""

import argparse
import collections
import glob
import json
import os
import sys
import tomllib
from datetime import date

import tag_embedding as te


def load_tagset():
    with open(te.TAGSET, "rb") as f:
        data = tomllib.load(f)
    return {t["name"]: t["parent"] for t in data["layer2"]}


def load_articles(layer2):
    """記事を読み、(第2層タグ, 埋め込み対象テキスト) の一覧を返す。"""
    articles = []
    skipped = []
    for path in sorted(glob.glob(os.path.join(te.CONTENT, "**", "index.md"), recursive=True)):
        parts = te.split_frontmatter(open(path, encoding="utf-8").read())
        if not parts:
            skipped.append((path, "frontmatter なし"))
            continue
        front, body = parts
        tags = [t for t in te.tags_of(front) if t in layer2]
        if len(tags) != 1:
            skipped.append((path, f"第2層タグが{len(tags)}件"))
            continue
        articles.append((tags[0], te.embed_text(front, body)))
    return articles, skipped


def main():
    parser = argparse.ArgumentParser(description="tag-vectors.json を算出する")
    parser.add_argument("--dry-run", action="store_true",
                        help="対象と概算トークン数のみ表示し、APIを呼ばない")
    args = parser.parse_args()

    layer2 = load_tagset()
    articles, skipped = load_articles(layer2)
    used = {tag for tag, _ in articles}

    chars = sum(len(t) for _, t in articles)
    print(f"タグ {len(layer2)}件 / 記事 {len(articles)}件 / {chars:,}文字", file=sys.stderr)
    print(f"概算 {int(chars * 0.51):,} トークン（実測 0.51 トークン/文字）", file=sys.stderr)
    for path, reason in skipped:
        print(f"  除外: {os.path.relpath(path, te.ROOT)} ({reason})", file=sys.stderr)
    empty = sorted(set(layer2) - used)
    if empty:
        print(f"  記事0件のタグ（vector は null）: {', '.join(empty)}", file=sys.stderr)

    if args.dry_run:
        return

    vectors, tokens = te.embed([t for _, t in articles], te.api_key())
    print(f"消費 {tokens:,} トークン", file=sys.stderr)

    grouped = collections.defaultdict(list)
    for (tag, _), vector in zip(articles, vectors):
        grouped[tag].append(vector)

    output = {
        "schema_version": 1,
        "model": te.MODEL,
        "dim": te.DIM,
        "input_type": te.INPUT_TYPE,
        "normalized": True,
        "updated": date.today().isoformat(),
        "tags": {
            name: {
                "article_count": len(grouped.get(name, [])),
                "vector": te.centroid(grouped[name]) if grouped.get(name) else None,
            }
            for name in sorted(layer2)
        },
    }
    with open(te.VECTORS, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"書き出し: {os.path.relpath(te.VECTORS, te.ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
