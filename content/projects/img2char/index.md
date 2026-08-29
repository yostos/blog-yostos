+++
title = "img2char"
description = """\
A Go CLI tool that converts monochrome images \
to ASCII art using 8x8 dot pattern matching."""
weight = 10

[taxonomies]
tags = ["Tech", "CLI"]

[extra]
local_image = "cover.webp"
social_media_card = "cover.webp"
show_reading_time = false
+++

<!-- textlint-disable -->

{{ image(src="cover.webp", alt="img2char") }}

<!-- textlint-enable -->

In 1986, I wrote a BASIC program on a Sharp X1
that converted graphics into ASCII characters
using the character ROM and graphic VRAM.
It was used to post images on BBS forums
in the early days of Japanese personal
computer networks.

img2char recreates that algorithm in Go.
It uses 8x8 dot pattern matching with
Hamming distance instead of density-based
conversion, preserving contours and line
directions in the output.

## Install

```bash
brew install yostos/tap/img2char
```

## Links

- [GitHub](https://github.com/yostos/img2char)
- [Blog post (ja)](@/blog/2026/02/img2char-ascii-art-1986/index.md)
