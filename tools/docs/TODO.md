# 記事移行 TODO

## 完了した作業

### Zolaサイトのセットアップ
- [x] Zolaプロジェクト初期化
- [x] tabiテーマのインストール（`themes/tabi/`にclone）
- [x] `zola.toml` の設定（日本語、テーマ設定など）
- [x] 検索機能は無効（日本語未サポート）

### 記事移行（1件完了）
- [x] `building-ttt-with-claude-code` の移行

## 移行元・移行先の構造

### 移行元（Next.js/MDX）
```
src/app/articles/YYYY/MM/DD/slug/
├── page.mdx
└── [images...]
```

### 移行先（Zola）
```
content/slug/
├── index.md
└── [images...]
```

## MDXからZola Markdownへの変換ルール

### 1. frontmatterの変換

**MDX（JavaScript形式）:**
```javascript
export const article = {
  title: "タイトル",
  description: "説明",
  author: siteConfig.author,
  date: "2026-01-23",
  path: "slug-name",
  canonicalUrl: "https://zenn.dev/...",
};
```

**Zola（TOML形式）:**
```toml
+++
title = "タイトル"
description = "説明"
date = 2026-01-23
aliases = ["/articles/YYYY/MM/DD/slug-name"]

[extra]
canonical_url = "https://zenn.dev/..."
+++
```

### 2. 削除が必要な行
- `import` 文すべて
- `export const article = {...}`
- `export const metadata = ...`
- `export default function ...`
- `{/* コメント */}` 形式のJSXコメント

### 3. 画像の変換

**MDX:**
```jsx
import DEMO from "./demo.gif";
<Image src={DEMO} alt="..." width={800} height={450} unoptimized />
```

**Zola:**
```markdown
![alt text](demo.gif)
```

### 4. aliasesの設定
元のURLからのリダイレクトを維持するため、`aliases`に旧URLパスを追加：
```toml
aliases = ["/articles/YYYY/MM/DD/slug-name"]
```

### 5. canonical_urlの設定
Zennなど別サイトが正規URLの場合：
```toml
[extra]
canonical_url = "https://zenn.dev/yostos/articles/..."
```

## 移行スクリプトの要件

### 入力
- 移行元ディレクトリ: `/Users/yostos/ghq/github.com/yostos/blog-yostos/src/app/articles/`

### 処理
1. `page.mdx` ファイルを検索
2. frontmatter（JavaScript object）をパース
3. TOML形式のfrontmatterに変換
4. MDX固有の構文を標準Markdownに変換
5. 画像ファイルをコピー
6. `aliases` に元のURLパスを追加
7. `canonical_url` があれば `[extra]` に追加

### 出力
- 移行先: `/Users/yostos/Desktop/zola/my-blog/content/`

## 注意事項

- 日付形式: `YYYY-MM-DD`（クォートなし）
- 画像パス: 相対パス（同一ディレクトリ内）
- aliasesはリダイレクトページを生成（HTMLメタリフレッシュ）

## 現在の設定ファイル

### zola.toml の主要設定
```toml
theme = "tabi"
default_language = "ja"
build_search_index = false  # 日本語未サポート
```

## 残タスク

- [ ] 移行スクリプトの作成
- [ ] 他の記事の移行
- [ ] `base_url` を本番URLに変更
- [ ] サイトタイトル・説明の更新
