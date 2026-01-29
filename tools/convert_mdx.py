#!/usr/bin/env python3
"""MDX→Zola記事コンバーター

Usage:
    python convert_mdx.py <src_dir> <dest_dir>

Example:
    python tools/convert_mdx.py \
        /Users/yostos/ghq/github.com/yostos/blog-yostos/src/app/articles \
        /Users/yostos/Desktop/zola/my-blog/content/blog
"""

import os
import re
import shutil
import sys
from pathlib import Path


def find_mdx_files(src_dir: str) -> list[Path]:
    """移行元ディレクトリからpage.mdxファイルを再帰的に検索する。"""
    return sorted(Path(src_dir).rglob("page.mdx"))


def extract_slug(mdx_path: Path) -> str:
    """MDXファイルのパスからslug（記事ディレクトリ名）を取得する。"""
    return mdx_path.parent.name


def extract_url_path(mdx_path: Path, src_dir: str) -> str:
    """MDXファイルのパスから旧URLパスを生成する。

    例: src/articles/2026/01/23/slug-name/page.mdx → /articles/2026/01/23/slug-name
    """
    rel = mdx_path.parent.relative_to(src_dir)
    return f"/articles/{rel}"


def build_import_map(content: str) -> dict[str, str]:
    """import文から変数名→ファイル名のマッピングを構築する。

    例: import DEMO from "./demo.gif" → {"DEMO": "demo.gif"}
    """
    mapping = {}
    for m in re.finditer(r'import\s+(\w+)\s+from\s+["\']\.\/([^"\']+)["\']', content):
        var_name, filename = m.group(1), m.group(2)
        mapping[var_name] = filename
    return mapping


def parse_article_metadata(content: str) -> dict[str, str]:
    """export const article = {...} ブロックからメタデータを抽出する。"""
    block_match = re.search(
        r"export\s+const\s+article\s*=\s*\{(.*?)\};",
        content,
        re.DOTALL,
    )
    if not block_match:
        return {}

    block = block_match.group(1)
    metadata = {}

    # title: "..." or title: '...' or title: `...`
    title_m = re.search(r'title:\s*"([^"]*)"', block)
    if not title_m:
        title_m = re.search(r"title:\s*'([^']*)'", block)
    if not title_m:
        title_m = re.search(r"title:\s*`([^`]*)`", block)
    if title_m:
        metadata["title"] = title_m.group(1).strip()

    # description: "..." or description: `...`
    desc_m = re.search(r'description:\s*"([^"]*)"', block)
    if not desc_m:
        desc_m = re.search(r"description:\s*`([^`]*)`", block, re.DOTALL)
    if desc_m:
        desc = desc_m.group(1).strip()
        # 複数行のdescriptionを1行に結合
        desc = re.sub(r"\s*\n\s*", "", desc)
        metadata["description"] = desc

    # date: "YYYY-MM-DD" or "YYYY-M-D"
    date_m = re.search(r'date:\s*"(\d{4})-(\d{1,2})-(\d{1,2})"', block)
    if date_m:
        y, m, d = date_m.group(1), date_m.group(2), date_m.group(3)
        metadata["date"] = f"{y}-{m.zfill(2)}-{d.zfill(2)}"

    # canonicalUrl: "..." or canonicalUrl: "<...>"
    canon_m = re.search(r'canonicalUrl:\s*"([^"]*)"', block)
    if not canon_m:
        canon_m = re.search(r"canonicalUrl:\s*\n?\s*\"([^\"]*?)\"", block)
    if canon_m:
        url = canon_m.group(1).strip()
        url = url.strip("<>")
        metadata["canonicalUrl"] = url

    return metadata


def build_frontmatter(metadata: dict[str, str], aliases: list[str]) -> str:
    """ZolaのTOMLフロントマターを構築する。"""
    lines = ["+++"]

    if "title" in metadata:
        escaped_title = metadata["title"].replace('"', '\\"')
        lines.append(f'title = "{escaped_title}"')

    if "description" in metadata:
        escaped_desc = metadata["description"].replace('"', '\\"')
        lines.append(f'description = "{escaped_desc}"')

    if "date" in metadata:
        lines.append(f'date = {metadata["date"]}')

    if aliases:
        alias_str = ", ".join(f'"{a}"' for a in aliases)
        lines.append(f"aliases = [{alias_str}]")

    if "canonicalUrl" in metadata:
        lines.append("")
        lines.append("[extra]")
        lines.append(f'canonical_url = "{metadata["canonicalUrl"]}"')

    lines.append("+++")
    return "\n".join(lines)


def extract_youtube_id(url: str) -> str | None:
    """YouTube URLからVideo IDを抽出する。"""
    # https://www.youtube.com/watch?v=VIDEO_ID
    m = re.search(r"youtube\.com/watch\?v=([^&\"'\s]+)", url)
    if m:
        return m.group(1)
    # https://youtu.be/VIDEO_ID or https://youtu.be/VIDEO_ID?si=...
    m = re.search(r"youtu\.be/([^?\"'\s]+)", url)
    if m:
        return m.group(1)
    return None


def convert_body(content: str, import_map: dict[str, str]) -> str:
    """MDX本文をZola Markdownに変換する。"""
    lines = content.split("\n")
    result = []
    skip_block = None  # "article" | "function" | "import" | None
    brace_depth = 0
    html_depth = 0  # HTML要素のネスト深さ
    youtube_buf = []  # 複数行YouTubeタグの蓄積用

    for line in lines:
        stripped = line.strip()

        # --- ブロックスキップ処理 ---
        if skip_block == "article":
            if stripped.endswith("};"):
                skip_block = None
            continue

        if skip_block == "function":
            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                skip_block = None
            continue

        if skip_block == "import":
            # 複数行import: } from "..." で終了
            if re.search(r'from\s+["\']', stripped):
                skip_block = None
            continue

        # --- 複数行YouTubeタグの蓄積処理 ---
        if youtube_buf is not None and len(youtube_buf) > 0:
            youtube_buf.append(line)
            if stripped == "/>":
                joined = " ".join(l.strip() for l in youtube_buf)
                url_m = re.search(r'url="([^"]+)"', joined)
                if url_m:
                    video_id = extract_youtube_id(url_m.group(1))
                    if video_id:
                        result.append('{{ youtube(id="' + video_id + '") }}')
                    else:
                        result.extend(youtube_buf)
                else:
                    result.extend(youtube_buf)
                youtube_buf = []
            continue

        # --- 削除対象の検出 ---

        # import文（単一行 or 複数行の開始）
        if re.match(r"^import\s+", stripped):
            # 複数行import: import { で始まり } from が同一行にない
            if "{" in stripped and "from" not in stripped:
                skip_block = "import"
            continue

        # export const article = { ... }
        if re.match(r"^export\s+const\s+article\s*=", stripped):
            if stripped.endswith("};"):
                continue  # 1行で完結
            skip_block = "article"
            continue

        # export const metadata = ... （単一行 or 複数行）
        if re.match(r"^export\s+const\s+metadata\s*=", stripped):
            if stripped.endswith("};") or stripped.endswith(");"):
                continue  # 1行で完結
            if "{" in stripped:
                skip_block = "article"  # articleと同じ };で終了するパターンを再利用
            continue

        # export default function ...
        if re.match(r"^export\s+default\s+function", stripped):
            skip_block = "function"
            brace_depth = line.count("{") - line.count("}")
            if brace_depth <= 0:
                skip_block = None
            continue

        # JSXコメント {/* ... */}
        if re.match(r"^\{/\*.*\*/\}$", stripped):
            continue

        # --- 変換処理 ---

        # HTMLブロック深さ追跡（Image変換の形式判定用）
        html_depth += len(re.findall(r"<(figure|table|thead|tbody|tr|td|th|dl|dd)\b", line))
        closing = len(re.findall(r"</(figure|table|thead|tbody|tr|td|th|dl|dd)>", line))

        # <Image src={VAR} alt="..." ... /> → Markdown画像 or <img>
        img_match = re.search(
            r'<Image\s+src=\{(\w+)\}\s+alt="([^"]*)".*?/>', line
        )
        if img_match:
            var_name = img_match.group(1)
            alt_text = img_match.group(2)
            filename = import_map.get(var_name, f"{var_name.lower()}")
            if html_depth > 0:
                line = line.replace(img_match.group(0), f'<img src="{filename}" alt="{alt_text}" />')
            else:
                line = f"![{alt_text}]({filename})"

        # <TableOfContents /> → <!-- toc -->
        if re.search(r"<TableOfContents\s*/>", line):
            line = re.sub(r"<TableOfContents\s*/>", "<!-- toc -->", line)

        # <YouTube ... /> （単一行）→ {{ youtube(id="VIDEO_ID") }}
        yt_match = re.search(r'<YouTube\s+url="([^"]+)".*?/>', line)
        if yt_match:
            video_id = extract_youtube_id(yt_match.group(1))
            if video_id:
                line = re.sub(
                    r"<YouTube\s.*?/>",
                    '{{ youtube(id="' + video_id + '") }}',
                    line,
                )

        # 複数行YouTube: <YouTube で始まり /> が同一行にない場合
        if re.match(r"^\s*<YouTube\s*$", line) or (
            re.match(r"^\s*<YouTube\b", line) and "/>" not in line
        ):
            youtube_buf = [line]
            continue

        # <DescriptionList> → <dl> 等
        line = re.sub(r"<DescriptionList>", "<dl>", line)
        line = re.sub(r"</DescriptionList>", "</dl>", line)
        line = re.sub(r"<DescriptionTerm>", "<dt>", line)
        line = re.sub(r"</DescriptionTerm>", "</dt>", line)
        line = re.sub(r"<DescriptionDetails>", "<dd>", line)
        line = re.sub(r"</DescriptionDetails>", "</dd>", line)

        # JSX属性: colSpan={N} → colspan="N"
        line = re.sub(r'colSpan=\{(\d+)\}', r'colspan="\1"', line)

        # HTML深さ更新（閉じタグ分）
        html_depth -= closing

        result.append(line)

    # 先頭の空行を除去
    while result and result[0].strip() == "":
        result.pop(0)

    # 手動目次（アンカーリンクのリスト）を <!-- toc --> に置換
    output_lines = []
    toc_block = []
    for line in result:
        if re.match(r"^\s*-\s*\[.*\]\(#.*\)\s*$", line):
            toc_block.append(line)
        else:
            if toc_block:
                output_lines.append("<!-- toc -->")
                toc_block = []
            output_lines.append(line)
    if toc_block:
        output_lines.append("<!-- toc -->")

    return "\n".join(output_lines)


def copy_assets(src_article_dir: Path, dest_article_dir: Path) -> list[str]:
    """画像などのアセットファイルをコピーする。page.mdx以外の全ファイル。"""
    copied = []
    for f in src_article_dir.iterdir():
        if f.is_file() and f.name != "page.mdx":
            shutil.copy2(f, dest_article_dir / f.name)
            copied.append(f.name)
    return copied


def ensure_section_indexes(dest_dir: Path, year: str, month: str) -> None:
    """年・月のセクション用_index.mdを必要に応じて作成する。"""
    year_dir = dest_dir / year
    year_dir.mkdir(parents=True, exist_ok=True)
    year_index = year_dir / "_index.md"
    if not year_index.exists():
        year_index.write_text(
            f"+++\ntitle = \"{year}\"\nsort_by = \"date\"\ntransparent = true\n+++\n",
            encoding="utf-8",
        )

    month_dir = year_dir / month
    month_dir.mkdir(parents=True, exist_ok=True)
    month_index = month_dir / "_index.md"
    if not month_index.exists():
        month_index.write_text(
            f"+++\ntitle = \"{year}/{month}\"\nsort_by = \"date\"\ntransparent = true\n+++\n",
            encoding="utf-8",
        )


def convert_article(mdx_path: Path, src_dir: str, dest_dir: str) -> dict:
    """1記事を変換する。結果情報を辞書で返す。"""
    slug = extract_slug(mdx_path)
    url_path = extract_url_path(mdx_path, src_dir)
    content = mdx_path.read_text(encoding="utf-8")

    metadata = parse_article_metadata(content)
    import_map = build_import_map(content)
    frontmatter = build_frontmatter(metadata, [url_path])
    body = convert_body(content, import_map)

    # YYYY/MM をソースパスから取得
    rel_parts = mdx_path.parent.relative_to(src_dir).parts
    year, month = rel_parts[0], rel_parts[1]

    dest_base = Path(dest_dir)
    ensure_section_indexes(dest_base, year, month)

    dest_article_dir = dest_base / year / month / slug
    dest_article_dir.mkdir(parents=True, exist_ok=True)

    output = f"{frontmatter}\n\n{body}"
    (dest_article_dir / "index.md").write_text(output, encoding="utf-8")

    assets = copy_assets(mdx_path.parent, dest_article_dir)

    return {
        "slug": slug,
        "title": metadata.get("title", "(no title)"),
        "assets": assets,
    }


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <src_dir> <dest_dir>")
        sys.exit(1)

    src_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    if not os.path.isdir(src_dir):
        print(f"Error: {src_dir} is not a directory")
        sys.exit(1)

    mdx_files = find_mdx_files(src_dir)
    print(f"Found {len(mdx_files)} articles to convert\n")

    success_count = 0
    error_count = 0

    for mdx_path in mdx_files:
        slug = extract_slug(mdx_path)
        try:
            result = convert_article(mdx_path, src_dir, dest_dir)
            asset_info = f" (+{len(result['assets'])} files)" if result["assets"] else ""
            print(f"  OK: {result['slug']}{asset_info} - {result['title']}")
            success_count += 1
        except Exception as e:
            print(f"  FAIL: {slug} - {e}")
            error_count += 1

    print(f"\nDone: {success_count} converted, {error_count} failed (total {len(mdx_files)})")


if __name__ == "__main__":
    main()
