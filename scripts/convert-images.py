#!/usr/bin/env python3
"""Convert Markdown images ![alt](src) to {{ image() }} shortcode."""
import re
import glob

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    result = []
    in_code_block = False
    in_frontmatter = False
    frontmatter_count = 0
    in_textlint_disable = False
    changed = False

    for line in lines:
        stripped = line.strip()

        # Track frontmatter (between +++ markers)
        if stripped == '+++':
            frontmatter_count += 1
            in_frontmatter = (frontmatter_count % 2 == 1)
            result.append(line)
            continue

        if in_frontmatter:
            result.append(line)
            continue

        # Track code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # Track textlint-disable state
        if 'textlint-disable' in stripped and '<!--' in stripped:
            in_textlint_disable = True
        if 'textlint-enable' in stripped and '<!--' in stripped:
            in_textlint_disable = False

        # Match standalone markdown image (entire line is just an image)
        m = re.match(r'^(\s*)!\[([^\]]*)\]\(([^)]+)\)\s*$', line)
        if m:
            indent = m.group(1)
            alt = m.group(2)
            src = m.group(3)

            if alt:
                shortcode = f'{indent}{{{{ image(src="{src}", alt="{alt}") }}}}'
            else:
                shortcode = f'{indent}{{{{ image(src="{src}") }}}}'

            if in_textlint_disable:
                # Already inside textlint-disable block, just replace syntax
                result.append(shortcode)
            else:
                # Add textlint-disable wrappers
                result.append(f'{indent}<!-- textlint-disable -->')
                result.append('')
                result.append(shortcode)
                result.append('')
                result.append(f'{indent}<!-- textlint-enable -->')
            changed = True
        else:
            result.append(line)

    if changed:
        with open(filepath, 'w') as f:
            f.write('\n'.join(result))
        print(f'Updated: {filepath}')

    return changed

count = 0
for filepath in sorted(glob.glob('content/**/*.md', recursive=True)):
    if process_file(filepath):
        count += 1

print(f'\nTotal files updated: {count}')
