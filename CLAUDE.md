# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Zola静的サイトジェネレーターによるブログ。Next.js/MDXブログからの移行プロジェクト。

## Common Commands

```bash
zola serve          # 開発サーバー起動（ライブリロード）
zola build          # 本番ビルド（public/に出力）
zola check          # エラーチェック
```

## Project Structure

```
content/           # 記事（各記事はディレクトリ形式）
  _index.md        # ホームページ設定
  slug-name/
    index.md       # 記事本体
    image.png      # 記事内画像
themes/tabi/       # tabiテーマ
docs/TODO.md       # 移行作業のドキュメント
```

## Theme: tabi

- テーマ: [tabi](https://github.com/welpo/tabi)
- 言語: 日本語（`default_language = "ja"`）
- 検索: 無効（日本語未サポート）

## 記事のfrontmatter形式

```toml
+++
title = "記事タイトル"
description = "説明"
date = 2026-01-23
aliases = ["/old/url/path"]  # リダイレクト用

[extra]
canonical_url = "https://..."  # 正規URL（他サイトがオリジナルの場合）
+++
```

## 移行元

- パス: `/Users/yostos/ghq/github.com/yostos/blog-yostos/src/app/articles/`
- 形式: MDX（Next.js App Router）
- 詳細: `docs/TODO.md` 参照
