#!/usr/bin/env python3
"""data/tag-vectors.json を算出する。

第2層タグごとに、タグ名そのものを埋め込んだ値を書き出す。記事は参照しない
（article_count のみ集計する）。埋め込みは Voyage AI の voyage-4 を使う。
選定理由と呼び出し方は docs/architectural-decision.md の ADR-0004 を参照。

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


def count_articles(layer2):
    """タグごとの記事数を数える。ベクターには使わず、参考値として持つ。"""
    counts = collections.Counter()
    for path in glob.glob(os.path.join(te.CONTENT, "**", "index.md"), recursive=True):
        parts = te.split_frontmatter(open(path, encoding="utf-8").read())
        if not parts:
            continue
        for tag in te.tags_of(parts[0]):
            if tag in layer2:
                counts[tag] += 1
    return counts


def main():
    parser = argparse.ArgumentParser(description="tag-vectors.json を算出する")
    parser.add_argument("--dry-run", action="store_true",
                        help="対象のみ表示し、APIを呼ばない")
    args = parser.parse_args()

    layer2 = load_tagset()
    names = sorted(layer2)
    counts = count_articles(layer2)

    print(f"タグ {len(names)}件を埋め込みます", file=sys.stderr)
    empty = [n for n in names if not counts[n]]
    if empty:
        print(f"  記事0件のタグ: {', '.join(empty)}", file=sys.stderr)

    if args.dry_run:
        return

    vectors, tokens = te.embed(names, te.api_key())
    print(f"消費 {tokens:,} トークン", file=sys.stderr)

    output = {
        "schema_version": 2,
        "model": te.MODEL,
        "dim": te.DIM,
        "input_type": te.INPUT_TYPE,
        "vector_source": te.VECTOR_SOURCE,
        "normalized": True,
        "updated": date.today().isoformat(),
        "tags": {
            name: {"article_count": counts[name], "vector": vector}
            for name, vector in zip(names, vectors)
        },
    }
    with open(te.VECTORS, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"書き出し: {os.path.relpath(te.VECTORS, te.ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
