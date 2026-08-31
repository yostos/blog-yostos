#!/usr/bin/env python3
"""記事から選んだキーワードでタグを決め、frontmatter にセットする。

キーワードは記事を読んだ Claude が選ぶ。本スクリプトは受け取った語を
空白で連結して1つの文字列として埋め込み、data/tag-vectors.json の
各第2層タグ（タグ名の埋め込み）とコサイン類似度を取って、
最上位のタグとその親の第1層タグを書き込む。

語を1語ずつタグと突き合わせてはならない。組み合わせでしか表せない意味が
失われ、精度が大きく落ちる。理由は docs/architectural-decision.md の
ADR-0006 を参照。

Requires: VOYAGE_API_KEY
"""

import argparse
import os
import re
import sys
import tomllib

import tag_embedding as te

EXPECTED_KEYWORDS = 5


def load_parents():
    with open(te.TAGSET, "rb") as f:
        data = tomllib.load(f)
    return {t["name"]: t["parent"] for t in data["layer2"]}


def rank(vector, tags):
    """タグを類似度の降順で返す。双方とも長さ1なので内積がコサイン類似度になる。"""
    scored = [(sum(x * y for x, y in zip(vector, t["vector"])), name)
              for name, t in tags.items() if t["vector"]]
    return sorted(scored, reverse=True)


def set_tags(front, layer1, layer2):
    """frontmatter の tags を差し替える。第1層を先頭に置く。"""
    line = f'tags = ["{layer1}", "{layer2}"]'
    if re.search(r"^tags\s*=\s*\[.*?\]", front, re.M | re.S):
        return re.sub(r"^tags\s*=\s*\[.*?\]", line, front, count=1, flags=re.M | re.S)
    if re.search(r"^\[taxonomies\]", front, re.M):
        return re.sub(r"^\[taxonomies\]", f"[taxonomies]\n{line}", front, count=1, flags=re.M)
    return f"{front}\n\n[taxonomies]\n{line}"


def main():
    parser = argparse.ArgumentParser(
        description="キーワードから記事のタグを決めて frontmatter にセットする")
    parser.add_argument("article", help="記事のパス（content/.../index.md）")
    parser.add_argument("keywords", nargs="+",
                        help=f"記事の内容を表す英単語（{EXPECTED_KEYWORDS}語）。"
                             " 名詞句は引用符でまとめる")
    parser.add_argument("--top", type=int, default=3, help="表示する候補数（既定 3）")
    parser.add_argument("--dry-run", action="store_true",
                        help="類似度を表示するだけで frontmatter を書き換えない")
    args = parser.parse_args()

    path = os.path.abspath(args.article)
    if not os.path.exists(path):
        raise SystemExit(f"Error: {args.article} がありません")
    if len(args.keywords) != EXPECTED_KEYWORDS:
        print(f"Warning: キーワードは{EXPECTED_KEYWORDS}語を想定しています"
              f"（{len(args.keywords)}語が渡されました）", file=sys.stderr)

    data = te.load_vectors()
    parents = load_parents()

    text = open(path, encoding="utf-8").read()
    parts = te.split_frontmatter(text)
    if not parts:
        raise SystemExit(f"Error: {args.article} に frontmatter がありません")
    front, body = parts

    query = " ".join(args.keywords)
    vectors, tokens = te.embed([query], te.api_key())
    ranked = rank(vectors[0], data["tags"])
    if not ranked:
        raise SystemExit("Error: 比較できるタグがありません")

    print(f"キーワード: {query}", file=sys.stderr)
    print(f"消費 {tokens:,} トークン", file=sys.stderr)
    print(f"現在のタグ: {te.tags_of(front) or 'なし'}", file=sys.stderr)
    for i, (score, name) in enumerate(ranked[:args.top], 1):
        mark = "→" if i == 1 else " "
        print(f" {mark} {i}. {name} ({parents.get(name, '?')}) {score:.4f}", file=sys.stderr)

    best = ranked[0][1]
    layer1 = parents.get(best)
    if not layer1:
        raise SystemExit(f"Error: {best} の親が tagset.toml にありません")

    if args.dry_run:
        print("--dry-run のため書き換えません", file=sys.stderr)
        return

    updated = set_tags(front, layer1, best)
    open(path, "w", encoding="utf-8").write(f"+++\n{updated}\n+++\n{body}")
    print(f'セット: tags = ["{layer1}", "{best}"]', file=sys.stderr)


if __name__ == "__main__":
    main()
