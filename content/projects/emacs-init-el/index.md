+++
title = "Emacs init.el"
description = """\
My Emacs configuration for Emacs 31 on macOS, \
built to make Emacs a hub for everyday text work."""
weight = 20

[taxonomies]
tags = ["Tech", "Editor"]

[extra]
local_image = "cover.webp"
social_media_card = "cover.webp"
show_reading_time = false
+++

<!-- textlint-disable -->

{{< image src="cover.webp" alt="Emacs init.el" />}}

<!-- textlint-enable -->

The init.el I use every day on Emacs 31
and macOS. It aims to make Emacs a hub
for all kinds of text work, not just
programming.

It covers writing in Japanese and
managing tasks and notes with Org mode
and Howm. Claude Code and LLMs run inside
Emacs through claude-code.el and gptel.
Mail, RSS and the web are read in Emacs
buffers, and development relies on Eglot
and tree-sitter.

The whole configuration lives in a single
file. Each package gets its own
use-package block, and every section
header lists the external commands it
requires.

Released under the MIT License.

## Links

- [Gist](https://gist.github.com/yostos/631d858c283b1a15fc487f474c837a86)
- [Blog post (ja): Why Emacs in the age of generative AI](@/blog/2026/10/migrate-to-emacs/index.md)
- [Blog series (ja): Emacs configuration for the AI era](@/blog/2026/10/emacs-init-el/_index.md)
