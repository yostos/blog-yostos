#!/usr/bin/env python3
"""One-off migration: rewrite Zola shortcode calls into Tera 2 component calls.

Zola 0.23 removed shortcodes and now renders the whole Markdown body with
Tera 2. This script rewrites content/**/*.md in place:

  {{ name(a="x", b=true) }}        -> {{< name a="x" b={true} />}}
  {% name(a="x") %} ... {% end %}  -> {% <name a="x"> %} ... {% </name> %}
  {{/* name(...) */}}              -> {% raw %}{{ name(...) }}{% endraw %}
  other literal {{ .. }} / {% .. %} -> wrapped in {% raw %} .. {% endraw %}

The last two keep the rendered output identical to Zola 0.22: escaped
shortcodes used to render as literal text, and literal delimiters
(GitHub Actions `${{ secrets.X }}`, template examples) were never templated.

Usage:
  python scripts/migrate-shortcodes-zola-0.23.py            # rewrite files
  python scripts/migrate-shortcodes-zola-0.23.py --dry-run  # report only
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

SHORTCODES = [
    # site components (templates/components/)
    "image", "youtube", "linkcard", "spot", "module",
    # tabi components
    "admonition", "aside", "mermaid", "references", "remote_text",
    "full_width_image", "multilingual_quote", "spoiler",
]
NAMES = "|".join(SHORTCODES)

TOKEN = re.compile(
    r"(?P<esc_inline>\{\{/\*(?P<ei>.*?)\*/\}\})"
    r"|(?P<esc_block>\{%/\*(?P<eb>.*?)\*/%\})"
    rf"|(?P<inline>\{{\{{\s*(?P<iname>{NAMES})\((?P<iargs>.*?)\)\s*\}}\}})"
    rf"|(?P<block>\{{%\s*(?P<bname>{NAMES})\((?P<bargs>.*?)\)\s*%\}})"
    r"|(?P<end>\{%\s*end\s*%\})"
    r"|(?P<literal>\{\{.*?\}\}|\{%.*?%\}|\{#.*?#\})",
    re.S,
)

ARG = re.compile(
    r"""\s*,?\s*(?P<key>\w+)\s*=\s*(?P<val>"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|true|false|-?\d+(?:\.\d+)?)\s*,?""",
    re.S,
)


def convert_args(args: str, where: str) -> str:
    out, pos = [], 0
    while pos < len(args):
        if not args[pos:].strip(" \t\r\n,"):
            break
        m = ARG.match(args, pos)
        if not m:
            raise ValueError(f"{where}: cannot parse arguments: {args!r}")
        key, val = m.group("key"), m.group("val")
        if val.startswith('"'):
            out.append(f"{key}={val}")
        elif val.startswith("'"):
            inner = val[1:-1]
            if '"' in inner:
                raise ValueError(f"{where}: single-quoted value contains '\"': {val}")
            out.append(f'{key}="{inner}"')
        else:
            out.append(f"{key}={{{val}}}")
        pos = m.end()
    return " ".join(out)


def raw(text: str) -> str:
    return "{% raw %}" + text + "{% endraw %}"


def migrate(body: str, path: str, stats: Counter) -> str:
    stack: list[str] = []

    def lineno(pos: int) -> int:
        return body.count("\n", 0, pos) + 1

    def repl(m: re.Match) -> str:
        where = f"{path}:{lineno(m.start())}"
        if m.group("esc_inline") is not None:
            stats["escaped"] += 1
            return raw("{{" + m.group("ei") + "}}")
        if m.group("esc_block") is not None:
            stats["escaped"] += 1
            return raw("{%" + m.group("eb") + "%}")
        if m.group("inline") is not None:
            stats[f"inline:{m.group('iname')}"] += 1
            args = convert_args(m.group("iargs"), where)
            return "{{< " + m.group("iname") + (" " + args if args else "") + " />}}"
        if m.group("block") is not None:
            name = m.group("bname")
            stats[f"block:{name}"] += 1
            stack.append(name)
            args = convert_args(m.group("bargs"), where)
            return "{% <" + name + (" " + args if args else "") + "> %}"
        if m.group("end") is not None:
            if not stack:
                raise ValueError(f"{where}: {{% end %}} without an open block")
            return "{% </" + stack.pop() + "> %}"
        stats["literal"] += 1
        return raw(m.group("literal"))

    result = TOKEN.sub(repl, body)
    if stack:
        raise ValueError(f"{path}: unclosed block(s): {stack}")
    return result


def split_frontmatter(text: str) -> tuple[str, str]:
    m = re.match(r"(\+\+\+\n.*?\n\+\+\+\n)", text, re.S)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("root", nargs="?", default="content")
    opts = parser.parse_args()

    stats: Counter = Counter()
    changed = 0
    for path in sorted(Path(opts.root).rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        front, body = split_frontmatter(text)
        new = front + migrate(body, str(path), stats)
        if new != text:
            changed += 1
            if not opts.dry_run:
                path.write_text(new, encoding="utf-8")

    for key, count in sorted(stats.items()):
        print(f"{count:5d}  {key}")
    print(f"{changed} file(s) {'would be ' if opts.dry_run else ''}changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
