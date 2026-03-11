# OGP画像自動生成ツール

## 概要

記事ごとにOGP画像（`ogp.webp`）を自動生成するNode.jsスクリプト。
テンプレート画像の上に記事タイトル・タグをオーバーレイして合成する。

## 出力仕様

| 項目 | 値 |
|------|-----|
| ファイル名 | `ogp.webp` |
| 出力先 | 各記事ディレクトリ（`content/blog/YYYY/MM/slug/`） |
| サイズ | 1200×630px |
| フォーマット | WebP（quality: 85） |

## テンプレート画像

すべてのOGP画像は固定のテンプレート画像を背景として使用する。

- パス: `scripts/images/ogp-template.png`（1200×630px）
- テンプレートに含まれる固定要素（スクリプトでは描画しない）:
  - 上下の水色ライン
  - 左下: Blueskyアイコン + 著者名
  - 右下: Coded Chordsロゴ + URL
- 記事個別の画像（cover.webp等）は背景に使用しない

## オーバーレイレイアウト

スクリプトが描画するのはタイトルとタグのみ。
テンプレート上部の白い余白エリアに配置する。

```
┌═══════════════════════════════════════════════════┐  テンプレート固定: 水色ライン
│                                                   │
│  記事タイトル                                      │  ← オーバーレイ（上端 80px、左端 60px）
│  （最大3行、折り返し対応）                          │
│                                                   │
│  #tag1  #tag2  #tag3  #tag4                       │  ← オーバーレイ（タイトル下 20px）
│                                                   │
│                                                   │
│  [BSky] TOSHIYUKI YOSHIDA    [Logo] codedchords   │  テンプレート固定: 著者名・ロゴ
└═══════════════════════════════════════════════════┘  テンプレート固定: 水色ライン
```

### オーバーレイ要素のスタイル

| 要素 | フォント | サイズ | 色 | 備考 |
|------|---------|--------|-----|------|
| タイトル | IBMPlexSansJP-Medium | 48px | `#1a1a1a` | 行間 1.4、最大3行、左寄せ |
| タグ | BerkeleyMono-Medium | 20px | `#4a9ece` | `#` プレフィックス付き、横並び、最大4つ |

### マージン

| 項目 | 値 |
|------|-----|
| タイトル左端 | 80px |
| タイトル上端 | 100px |
| タイトル右端マージン | 80px（折り返し幅 = 1040px） |
| タグとタイトルの間 | 20px |
| タグ間のスペース | 16px |

## フォント

| フォント | 用途 | 配置ファイル名 |
|---------|------|--------------|
| BerkeleyMono-Medium | ラテン文字・タグ表示 | `BerkeleyMono-Medium.otf` |
| IBMPlexSansJP-Medium | 日本語タイトル（ラテン文字フォールバック含む） | `IBMPlexSansJP-Medium.otf` |

- 配置先: `scripts/fonts/`（`.gitignore` 対象）
- フォントファイルはリポジトリに含めない（有償フォントを含むため）

## タグの取得

- frontmatter の `[taxonomies]` セクションから `tags` 配列を取得
- 最大 **4つ** まで表示（5つ以上ある場合は先頭4つを使用）
- 各タグの先頭に `#` を付与して表示

## コマンド

```bash
npm run ogp           # OGP画像を生成（既存はスキップ）
npm run ogp:dry-run   # 対象確認のみ（実際には生成しない）
npm run ogp --force   # 全記事を強制再生成
```

## ファイル構成

```
scripts/
  generate-ogp.mjs       # メイン生成スクリプト
  ogp-template.mjs       # satori用オーバーレイテンプレート
  images/
    ogp-template.png      # テンプレート背景画像（1200×630px）
  fonts/                  # フォント配置ディレクトリ（gitignore対象）
    BerkeleyMono-Medium.otf
    IBMPlexSansJP-Medium.otf
```

## 技術スタック

| パッケージ | 用途 |
|-----------|------|
| satori | JSX-likeオブジェクトからSVGオーバーレイを生成 |
| @resvg/resvg-js | SVGをPNGに変換（Rust製） |
| sharp | テンプレート画像との合成、WebP変換 |
| glob | 記事ディレクトリの走査 |

## 処理フロー

1. `scripts/fonts/` からフォントファイルを読み込み（1回のみ）
2. `scripts/images/ogp-template.png` をテンプレートとして読み込み
3. `content/blog/` 以下の全 `index.md` を走査
4. 各記事について:
   a. `ogp.webp` が既存ならスキップ（`--force` 時は上書き）
   b. frontmatter から `title` と `tags` を正規表現で抽出
   c. satori でオーバーレイSVGを生成（タイトル + タグ最大4つ）
   d. resvg でSVGをPNGに変換
   e. sharp でテンプレート画像にオーバーレイを合成
   f. WebP（quality: 85）で出力

## frontmatter との連携

記事の frontmatter に以下の設定が必要:

```toml
[taxonomies]
tags = ["タグ1", "タグ2"]

[extra]
social_media_card = "ogp.webp"
```

## セットアップ（新規環境）

1. `npm install`（依存パッケージのインストール）
2. `scripts/fonts/` に以下のフォントを配置:
   - `BerkeleyMono-Medium.otf`
   - `IBMPlexSansJP-Medium.otf`
